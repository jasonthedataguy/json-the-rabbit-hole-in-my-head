"""Restore the private asset snapshot and stage the selected film in any checkout."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def destination(relative):
    target=(ROOT/relative).resolve()
    if not target.is_relative_to(ROOT):
        raise ValueError('Snapshot path escapes the checkout.')
    return target


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--download',action='store_true')
    parser.add_argument('--archives',type=Path)
    parser.add_argument('--project',default='com-nguoi')
    args=parser.parse_args()
    manifest=json.loads((ROOT/'cloud/handoff-manifest.json').read_text(encoding='utf-8'))
    downloads=args.archives or ROOT/'.handoff/downloads'
    downloads.mkdir(parents=True,exist_ok=True)
    if args.download:
        for archive in manifest['archives']:
            local=downloads/archive['name']
            if local.is_file() and digest(local)==archive['sha256']:
                continue
            subprocess.run(['gh','release','download',manifest['asset_release_tag'],'--repo',manifest['repository'],
                            '--pattern',archive['name'],'--dir',str(downloads),'--clobber'],check=True)
    needed={row['sha256'] for row in manifest['files'] if row['storage']=='asset' and not destination(row['path']).is_file()}
    objects=ROOT/'.handoff/objects'
    objects.mkdir(parents=True,exist_ok=True)
    for archive in manifest['archives']:
        members={row['sha256'] for row in manifest['files'] if row.get('archive')==archive['name']} & needed
        if not members:
            continue
        local=downloads/archive['name']
        if not local.is_file() or digest(local)!=archive['sha256']:
            raise ValueError('Missing or stale private bundle '+archive['name']+'. Use --download.')
        with zipfile.ZipFile(local) as zipped:
            for checksum in members:
                target=objects/checksum
                with zipped.open('objects/'+checksum) as source,target.open('wb') as output:
                    shutil.copyfileobj(source,output)
                if digest(target)!=checksum:
                    raise ValueError('Asset hash differs from the original.')
    for row in manifest['files']:
        target=destination(row['path'])
        if row['storage']=='external_asset':
            continue
        if row['storage']=='git':
            if not target.is_file():
                raise ValueError('Code file missing from checkout: '+row['path'])
            continue  # Git tracks subsequent authorized edits separately from the snapshot.
        if target.is_file():
            if digest(target)!=row['sha256']:
                raise ValueError('Existing asset differs; preserve/review before replacing: '+row['path'])
            continue
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(objects/row['sha256'],target)
    # Only this generated mapping changes. Original manifests/evidence bytes remain intact.
    (ROOT/'cloud/local-paths.json').write_text(json.dumps({'mappings':manifest['source_mappings']},indent=2)+'\n',encoding='utf-8')
    sys.path.insert(0,str(ROOT/'scripts'))
    from studio import load
    project=load(ROOT/'studio/projects'/args.project/'project.json')
    motion=project.get('animation_manifest')
    if motion:
        cache=ROOT/'studio/.cache/render'/args.project/'v5-living-illustrations'
        subprocess.run([sys.executable,str(ROOT/'skills/json-asset-animation/scripts/motion_assets.py'),
                        'stage',motion['path'],'--output',str(cache)],cwd=ROOT,check=True)
        shutil.copy2(cache/'render-props.json',ROOT/'studio/apps/video/manifests/com-nguoi-v5.json')
    subprocess.run([sys.executable,str(ROOT/'scripts/studio.py'),'audit'],cwd=ROOT,check=True)
    print('Restored and verified. Start the video editor: npm run studio:v5 --prefix studio/apps/video -- --port=3000')
    if manifest.get('full_artwork_provider'):
        print('Current projects are ready. Full historical/design art is stored separately in Google Drive; see cloud/design-provider.json.')


if __name__=='__main__':
    main()
