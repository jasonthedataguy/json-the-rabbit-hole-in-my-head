"""Audit or restore missing files from the pinned original edition without overwriting v2 work."""
import argparse
import hashlib
import subprocess
from pathlib import Path
from common import ROOT, read_json, safe_path

TEXT_SUFFIXES = {'.md', '.json', '.log', '.html', '.css', '.js', '.py', '.txt', '.srt', '.vtt', '.svg', '.csv'}

def original_bytes(source, expected):
    data = source.read_bytes()
    variants = [data]
    if source.suffix.lower() in TEXT_SUFFIXES:
        lf = data.replace(b'\r\n', b'\n')
        variants += [lf, lf.replace(b'\n', b'\r\n')]
    for variant in variants:
        if hashlib.sha256(variant).hexdigest() == expected:
            return variant
    raise ValueError(f'Original source differs from recorded intake: {source}')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--check', action='store_true', help='Read-only audit (the default)')
    parser.add_argument('--restore-missing', action='store_true', help='Restore only missing imported files; never overwrite an existing destination')
    args = parser.parse_args()
    if args.check and args.restore_missing:
        parser.error('Choose an audit or a missing-file restore')
    migration = read_json(ROOT / 'docs/MIGRATION.json')
    commit = subprocess.check_output(['git', '-C', str(args.source), 'rev-parse', 'HEAD'], text=True).strip()
    if commit != migration['source_commit']:
        parser.error('Source checkout must be at the pinned migration commit')
    checked = restored = 0
    changed = []
    for item in migration['files']:
        if item['origin'] != 'original-edition':
            continue
        raw = original_bytes(safe_path(args.source, item['source']), item['sha256'])
        target = safe_path(ROOT, item['path'])
        if target.exists():
            if target.read_bytes() != raw:
                changed.append(item['path'])
        elif args.restore_missing:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw); restored += 1
        else:
            raise ValueError(f'Missing imported file: {item["path"]}')
        checked += 1
    print(f'Audited {checked} original inputs; restored {restored}; {len(changed)} local derivatives differ from their intake version.')
    if changed:
        print('\n'.join(changed))

if __name__ == '__main__':
    main()
