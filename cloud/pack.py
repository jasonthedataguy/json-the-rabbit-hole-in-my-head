"""Build a private, hash-deduplicated handoff of studio, artwork and book snapshots."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import zipfile
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from studio import load
OUT = ROOT/'.handoff'
REPOSITORY = OUT/'repository'
ASSETS = OUT/'assets'
EXCLUDED = {'.git','node_modules','.cache','__pycache__','.build','.handoff','.venv','venv',
            '.pytest_cache','__MACOSX','.aws','.ssh','.gnupg','.codex','.agents',
            '.design-handoff','cloud-design-transfer'}
TEXT = {'.md','.json','.py','.ts','.tsx','.js','.mjs','.cjs','.html','.css','.yml','.yaml',
        '.csv','.tsv','.toml','.txt','.sh','.ps1','.bat','.xml','.lock','.ini'}
SECRET = re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,}|sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{24,}|AKIA[A-Z0-9]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)')
LIMIT = 512*1024*1024
TRANSIENT = {'studio/apps/video/manifests/active-preview.json',
             'studio/apps/video/manifests/com-nguoi-v4.json',
             'studio/apps/video/manifests/com-nguoi-v5.json',
             'studio/reports/workspace-audit.json'}


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def files(root):
    for base,dirs,names in os.walk(root):
        dirs[:]=sorted(d for d in dirs if d not in EXCLUDED)
        if Path(base)==ROOT:
            dirs[:]=[d for d in dirs if d!='external']
        for name in sorted(names):
            path=Path(base)/name
            if path.is_relative_to(ROOT) and path.relative_to(ROOT).as_posix() in TRANSIENT:
                continue
            if name in ('.DS_Store','Thumbs.db','.npmrc','.pypirc','.netrc','.git-credentials') or (name.startswith('.env') and name!='.env.example'):
                continue
            if path.suffix.lower() in ('.pem','.p12','.pfx','.key'):
                continue
            if name in ('local-paths.json','asset-inventory.local.json','handoff-manifest.json'):
                continue
            yield path


def main():
    if (REPOSITORY/'.git').exists():
        raise RuntimeError('A handoff repository already exists. Do not overwrite a committed snapshot.')
    cfg=load(ROOT/'studio/studio.json')
    roots=[('studio',ROOT,Path('.')),('artwork',Path(cfg['asset_library']),Path('external/artwork')),
           ('book',Path(cfg['book_repository']),Path('external/book'))]
    REPOSITORY.mkdir(parents=True,exist_ok=True)
    ASSETS.mkdir(parents=True,exist_ok=True)
    records=[]
    objects={}
    for label,root,prefix in roots:
        for source in files(root):
            relative=prefix/source.relative_to(root)
            size=source.stat().st_size
            checksum=digest(source)
            text=label!='artwork' and (source.suffix.lower() in TEXT or source.name in ('.gitignore','.gitattributes','Dockerfile','LICENSE','CNAME'))
            if text:
                body=source.read_bytes()
                if SECRET.search(body):
                    raise ValueError('Credential-like content detected; review this file locally before upload: '+str(source))
                destination=REPOSITORY/relative
                destination.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(source,destination)
                storage='git'
            else:
                storage='asset'
                objects.setdefault(checksum,{'source':source,'bytes':size})
            records.append({'path':relative.as_posix(),'sha256':checksum,'bytes':size,'storage':storage,'root':label})
        print(label+': indexed '+str(sum(row['root']==label for row in records))+' files',flush=True)
    archives=[]
    current=None
    weight=0
    number=0
    try:
        for checksum,item in objects.items():
            if current is None or weight+item['bytes']>LIMIT:
                if current:
                    current.close()
                number+=1
                name='studio-assets-'+str(number).zfill(3)+'.zip'
                current=zipfile.ZipFile(ASSETS/name,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True)
                archives.append({'name':name})
                weight=0
                print('Packing '+name,flush=True)
            current.write(item['source'],'objects/'+checksum)
            item['archive']=archives[-1]['name']
            weight+=item['bytes']
    finally:
        if current:
            current.close()
    for entry in archives:
        path=ASSETS/entry['name']
        entry.update(bytes=path.stat().st_size,sha256=digest(path))
    for record in records:
        if record['storage']=='asset':
            record['archive']=objects[record['sha256']]['archive']
    source_mappings=[{'original':str(root),'relative':prefix.as_posix()} for _,root,prefix in roots]
    existing_mapping=ROOT/'cloud/local-paths.json'
    if existing_mapping.is_file():
        source_mappings.extend(json.loads(existing_mapping.read_text(encoding='utf-8'))['mappings'])
    manifest={
        'schema_version':'1.0','date':'2026-10-21','repository':'jasonthedataguy/json-studio',
        'asset_release_tag':'studio-handoff-2026-10-21-v5','visibility':'private',
        'source_mappings':source_mappings,
        'book_upstream':'https://github.com/jasonthedataguy/json-the-rabbit-hole-in-my-head',
        'snapshot_note':'Current book working-tree files included, including local approved text changes. Upstream public book is unchanged.',
        'excluded':'Dependencies, caches/browser profiles, Git internals, local credentials and private keys. No art regenerated.',
        'files':records,'archives':archives,
        'summary':{'files':len(records),'git_files':sum(r['storage']=='git' for r in records),
                   'asset_files':sum(r['storage']=='asset' for r in records),'raw_bytes':sum(r['bytes'] for r in records),
                   'unique_asset_objects':len(objects),'unique_asset_bytes':sum(r['bytes'] for r in objects.values()),
                   'upload_asset_bytes':sum(r['bytes'] for r in archives)},
        'public_story_release_approved':False,'paid_release_approved':False,
    }
    save(REPOSITORY/'cloud/handoff-manifest.json',manifest)
    save(OUT/'package-receipt.json',{'repository':str(REPOSITORY),'assets':str(ASSETS),
                                  'summary':manifest['summary'],'archives':archives,
                                  'manifest_sha256':digest(REPOSITORY/'cloud/handoff-manifest.json')})
    print(json.dumps(manifest['summary'],indent=2))


if __name__=='__main__':
    main()
