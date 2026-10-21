"""Keep current-project runtime art in GitHub; full design archive is handled in Drive."""
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.handoff'


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def strings(value):
    if isinstance(value,str):
        yield value
    elif isinstance(value,dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value,list):
        for item in value:
            yield from strings(item)


def main():
    checkout=OUT/'repository'
    path=checkout/'cloud/handoff-manifest.json'
    manifest=json.loads(path.read_text(encoding='utf-8'))
    if manifest.get('local_bundle_directory')=='runtime-assets':
        raise ValueError('Provider split already completed.')
    records=manifest['files']
    art={row['path']:row for row in records if row['root']=='artwork'}
    prefix=next(row['original'] for row in manifest['source_mappings'] if row['relative']=='external/artwork')
    normalized=prefix.replace('\\','/').rstrip('/')
    needed={row['sha256'] for row in records if row['storage']=='asset' and row['root']!='artwork'}
    # Preserve the full registry, and all exact library files referenced by studio JSON.
    needed.update(row['sha256'] for row in art.values() if row['path'].endswith('.json'))
    for row in records:
        if row['storage']!='git' or not row['path'].endswith('.json') or row['root']!='studio':
            continue
        try:
            data=json.loads((checkout/row['path']).read_text(encoding='utf-8'))
        except (ValueError,UnicodeError):
            continue
        for value in strings(data):
            value=value.replace('\\','/')
            if value.casefold().startswith(normalized.casefold()+'/'):
                target='external/artwork/'+value[len(normalized)+1:]
                if target in art:
                    needed.add(art[target]['sha256'])
    selected={row['sha256'] for row in records if row['storage']=='asset' and row['sha256'] in needed}
    output=OUT/'runtime-assets'
    output.mkdir(parents=True,exist_ok=True)
    archives=[]
    assignments={}
    current=None
    weight=0
    try:
        for previous in manifest['archives']:
            members={row['sha256'] for row in records if row.get('archive')==previous['name']} & selected
            if not members:
                continue
            with zipfile.ZipFile(OUT/'assets'/previous['name']) as source:
                for checksum in sorted(members):
                    if checksum in assignments:
                        continue
                    entry=source.getinfo('objects/'+checksum)
                    if current is None or weight+entry.file_size>512*1024*1024:
                        if current:
                            current.close()
                        name='studio-runtime-'+str(len(archives)+1).zfill(3)+'.zip'
                        current=zipfile.ZipFile(output/name,'w',compression=zipfile.ZIP_STORED,allowZip64=True)
                        archives.append({'name':name})
                        weight=0
                    with source.open(entry) as src,current.open('objects/'+checksum,'w') as dst:
                        shutil.copyfileobj(src,dst,1024*1024)
                    assignments[checksum]=archives[-1]['name']
                    weight+=entry.file_size
    finally:
        if current:
            current.close()
    for archive in archives:
        local=output/archive['name']
        archive.update(bytes=local.stat().st_size,sha256=digest(local))
    for row in records:
        if row['storage']!='asset':
            continue
        if row['sha256'] in assignments:
            row['archive']=assignments[row['sha256']]
        else:
            assert row['root']=='artwork'
            row.update(storage='external_asset',provider='google-drive-design-archive')
            row.pop('archive',None)
    manifest['archives']=archives
    manifest['local_bundle_directory']='runtime-assets'
    manifest['full_artwork_provider']={'type':'google_drive','managed_by_chat':'design workspace',
                                       'receipt':'cloud/design-provider.json',
                                       'note':'Full design/generation archive is uploaded by the coordinated design chat. GitHub bundles include current-project runtime artwork only.'}
    manifest['summary'].update(github_asset_files=sum(r['storage']=='asset' for r in records),
                               drive_asset_files=sum(r['storage']=='external_asset' for r in records),
                               upload_asset_bytes=sum(a['bytes'] for a in archives),github_unique_asset_objects=len(assignments))
    path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'package-receipt.json').write_text(json.dumps({'repository':str(checkout),'assets':str(output),
        'summary':manifest['summary'],'archives':archives,'manifest_sha256':digest(path)},indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest['summary'],indent=2))


if __name__=='__main__':
    main()
