"""Package the exact artwork bytes once, reusing the existing complete-library ZIP."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '.design-handoff'
SKIP = {'.git', 'node_modules', '__pycache__', '.cache', 'imagegen-deps', '.venv', 'venv'}
SECRET = re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,}|sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{40,}|AKIA[A-Z0-9]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)')
TEXT = {'.py', '.md', '.txt', '.json', '.html', '.js', '.mjs', '.ts', '.tsx', '.css', '.ps1', '.sh', '.toml', '.yaml', '.yml', '.csv', '.xml'}


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def selected_files(root, excluded):
    for base, dirs, names in os.walk(root, onerror=lambda e: (_ for _ in ()).throw(e)):
        for name in list(dirs):
            if name in SKIP:
                excluded.append({'path': str(Path(base) / name), 'reason': 'reinstallable dependency/cache/Git internals'})
                dirs.remove(name)
        for name in sorted(names):
            path = Path(base) / name
            if ((name.startswith('.env') and name != '.env.example') or
                    path.suffix.lower() in {'.pem', '.p12', '.pfx', '.key'}):
                excluded.append({'path': str(path), 'reason': 'local credential/private-key filename'})
                continue
            if name in {'Thumbs.db', '.DS_Store'}:
                excluded.append({'path': str(path), 'reason': 'operating-system cache'})
                continue
            if path.suffix.lower() in TEXT and SECRET.search(path.read_bytes()):
                raise ValueError('Credential-like bytes detected; not uploaded: ' + str(path))
            yield path


def main():
    if (OUT / 'artwork-manifest.json').exists():
        raise RuntimeError('Existing snapshot is retained; use a new snapshot location for a new version.')
    OUT.mkdir(parents=True, exist_ok=True)
    uploads = OUT / 'uploads'
    uploads.mkdir(exist_ok=True)
    baseline = Path('E:/books/.json/outputs/json-digital-book-assets.zip')
    baseline_sha = digest(baseline)
    base_index = {}
    with zipfile.ZipFile(baseline) as z:
        for i, entry in enumerate(z.infolist()):
            if entry.is_dir():
                continue
            with z.open(entry) as source:
                checksum = hashlib.file_digest(source, 'sha256').hexdigest()
            base_index.setdefault(checksum, entry.filename)
            if i % 1000 == 0:
                print('Indexed complete ZIP: ' + str(i) + ' members', flush=True)
    roots = [
        ('artwork-outputs', Path('E:/books/.json/outputs')),
        ('generation-workspace', Path('C:/Users/Administrator/Documents/Codex/2026-10-19/can')),
        ('original-design-boards', Path('C:/Users/Administrator/OneDrive/Desktop/.json book/json_assets_book_cover')),
    ]
    records, excluded, objects = [], [], {}
    for label, root in roots:
        count = 0
        for source in selected_files(root, excluded):
            checksum = digest(source)
            row = {'path': label + '/' + source.relative_to(root).as_posix(),
                   'sha256': checksum, 'bytes': source.stat().st_size}
            if checksum == baseline_sha:
                row.update(archive=baseline.name, member=None)
            elif checksum in base_index:
                row.update(archive=baseline.name, member=base_index[checksum])
            else:
                objects.setdefault(checksum, source)
            records.append(row)
            count += 1
        print(label + ': ' + str(count) + ' exact files', flush=True)
    archives = [{'name': baseline.name, 'bytes': baseline.stat().st_size,
                 'sha256': baseline_sha, 'role': 'complete current library; also reusable archive objects'}]
    object_locations = {}
    weight, current, number = 0, None, 0
    try:
        for checksum, source in objects.items():
            size = source.stat().st_size
            if current is None or weight + size > 512 * 1024 ** 2:
                if current:
                    current.close()
                number += 1
                name = 'artwork-history-' + str(number).zfill(3) + '.zip'
                current = zipfile.ZipFile(uploads / name, 'w', compression=zipfile.ZIP_DEFLATED,
                                          compresslevel=1, allowZip64=True)
                weight = 0
                archives.append({'name': name, 'role': 'unique historical/source files'})
                print('Packing ' + name, flush=True)
            member = 'objects/' + checksum
            current.write(source, member)
            object_locations[checksum] = {'archive': name, 'member': member}
            weight += size
    finally:
        if current:
            current.close()
    for archive in archives[1:]:
        path = uploads / archive['name']
        archive.update(bytes=path.stat().st_size, sha256=digest(path))
        with zipfile.ZipFile(path) as z:
            if z.testzip() is not None:
                raise ValueError('Archive CRC check failed: ' + archive['name'])
    for row in records:
        if 'archive' not in row:
            row.update(object_locations[row['sha256']])
    manifest = {
        'schema_version': '1.0', 'date': '2026-10-21', 'visibility': 'private',
        'scope': 'Private backup, not a change of manuscript/artwork authority or public release approval.',
        'source_roots': [{'label': label, 'original_path': str(root)} for label, root in roots],
        'base_archive_member_prefix': 'json-digital-book-assets/',
        'archives': archives, 'files': records, 'excluded': excluded,
        'summary': {'files': len(records), 'original_file_bytes': sum(r['bytes'] for r in records),
                    'base_archive_references': sum(r['archive'] == baseline.name for r in records),
                    'unique_supplement_objects': len(objects),
                    'upload_bytes': sum(r['bytes'] for r in archives)},
    }
    if manifest['summary']['upload_bytes'] > 14_800_000_000:
        raise ValueError('Upload exceeds the observed 15 GB Drive capacity; no files were removed.')
    save(OUT / 'artwork-manifest.json', manifest)
    shutil.copy2(OUT / 'artwork-manifest.json', uploads / 'artwork-manifest.json')
    shutil.copy2(ROOT / 'cloud-design-transfer/restore.py', uploads / 'restore-artwork.py')
    save(OUT / 'upload-files.local.json', [str(baseline), *[str(p) for p in uploads.iterdir()]])
    print(json.dumps(manifest['summary'], indent=2), flush=True)


if __name__ == '__main__':
    main()
