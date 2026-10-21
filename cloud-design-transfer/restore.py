"""Restore exact artwork files from the private Drive archives without overwriting changes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import zipfile


def digest(path):
    with Path(path).open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def safe_target(root, relative):
    root = Path(root).resolve()
    target = (root / relative).resolve()
    if not target.is_relative_to(root) or target == root:
        raise ValueError('Backup file path leaves the restore directory.')
    if os.name == 'nt' and len(str(target)) > 230 and not str(target).startswith('\\\\?\\'):
        # Extended-length paths preserve deeply nested historical archive names.
        text = str(target)
        return Path('\\\\?\\UNC\\' + text[2:] if text.startswith('\\\\') else '\\\\?\\' + text)
    return target


def join_library(archives):
    """The private GitHub fallback splits the unchanged large ZIP into binary parts."""
    archives = Path(archives)
    index = archives / 'canonical-zip-parts.json'
    if not index.is_file():
        return
    info = json.loads(index.read_text(encoding='utf-8'))
    target = safe_target(archives, info['name'])
    if target.exists():
        if digest(target) != info['sha256']:
            raise ValueError('Existing complete-library ZIP differs; preserve it first.')
        return
    partial = target.with_name(target.name + '.join-partial')
    with partial.open('xb') as output:
        for part in info['parts']:
            path = safe_target(archives, part['name'])
            if path.stat().st_size != part['bytes'] or digest(path) != part['sha256']:
                raise ValueError('Library ZIP part is missing or incorrect: ' + part['name'])
            with path.open('rb') as source:
                shutil.copyfileobj(source, output)
    if digest(partial) != info['sha256']:
        raise ValueError('Joined library ZIP hash differs.')
    partial.rename(target)


def restore(manifest, archives, destination):
    archives, destination = Path(archives), Path(destination)
    verified = restored = 0
    for archive in manifest['archives']:
        bundle = safe_target(archives, archive['name'])
        if not bundle.is_file() or digest(bundle) != archive['sha256']:
            raise ValueError('Missing or incorrect archive: ' + archive['name'])
        rows = [r for r in manifest['files'] if r['archive'] == archive['name']]
        with zipfile.ZipFile(bundle) as zipped:
            for row in rows:
                target = safe_target(destination, row['path'])
                if target.exists():
                    if not target.is_file() or digest(target) != row['sha256']:
                        raise ValueError('Existing file differs; preserve it before restoring: ' + str(target))
                    verified += 1
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                temporary = target.with_name(target.name + '.restore-partial')
                if temporary.exists():
                    raise ValueError('Partial file already exists; inspect before continuing: ' + str(temporary))
                if row['member'] is None:
                    shutil.copyfile(bundle, temporary)
                else:
                    with zipped.open(row['member']) as source, temporary.open('xb') as output:
                        shutil.copyfileobj(source, output)
                if digest(temporary) != row['sha256']:
                    raise ValueError('Restored bytes failed SHA-256: ' + row['path'])
                temporary.rename(target)
                restored += 1
        print(archive['name'] + ': verified/restored', flush=True)
    return {'restored_files': restored, 'existing_verified_files': verified}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archives', type=Path, required=True)
    parser.add_argument('--destination', type=Path, required=True)
    args = parser.parse_args()
    join_library(args.archives)
    manifest = json.loads((args.archives / 'artwork-manifest.json').read_text(encoding='utf-8'))
    print(json.dumps(restore(manifest, args.archives, args.destination), indent=2))


if __name__ == '__main__':
    main()
