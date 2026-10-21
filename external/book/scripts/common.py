"""Shared project paths and validation; production sources never live in dist."""
import hashlib
import json
import re
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
PRODUCT_DIRS = ('source', 'artwork/source', 'artwork/scenes', 'artwork/exports', 'artwork/portal', 'book', 'web', 'audio', 'video', 'social/instagram', 'social/facebook', 'social/tiktok', 'social/youtube', 'docs', 'previews', 'references')

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sha256(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def safe_path(base, relative):
    if not isinstance(relative, str) or not relative or '\\' in relative:
        raise ValueError(f'Expected a relative POSIX path: {relative!r}')
    parts = PurePosixPath(relative)
    if parts.is_absolute() or '..' in parts.parts or ':' in relative:
        raise ValueError(f'Path leaves its source folder: {relative}')
    target = (base / relative).resolve()
    if not target.is_relative_to(base.resolve()):
        raise ValueError(f'Path leaves its source folder: {relative}')
    return target

def chapter_entries(root=ROOT):
    registry = read_json(root / 'book.json')
    for slug in registry['chapters'] + registry.get('archive_chapters', []):
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
            raise ValueError(f'Invalid chapter slug: {slug}')
        folder = safe_path(root, 'chapters/' + slug)
        yield folder, read_json(folder / 'chapter.json')

def validate_project(root=ROOT):
    registry = read_json(root / 'book.json')
    slugs = registry['chapters'] + registry.get('archive_chapters', [])
    if len(slugs) != len(set(slugs)):
        raise ValueError('Duplicate chapter slug in book.json')
    numbers = []
    for folder, meta in chapter_entries(root):
        if meta['slug'] != folder.name:
            raise ValueError(f'Chapter folder and slug disagree: {folder.name}')
        in_book = folder.name in registry['chapters']
        if in_book:
            if not re.fullmatch(r'\d{2}', meta.get('number') or ''):
                raise ValueError(f'Book chapter needs a two-digit editorial number: {folder.name}')
            numbers.append(meta['number'])
        elif meta['number'] is not None:
            raise ValueError('Archive essays must not take a portal number')
        for directory in PRODUCT_DIRS:
            if not safe_path(folder, directory).is_dir():
                raise ValueError(f'Missing production directory: {folder.name}/{directory}')
        if meta['publish']:
            source = safe_path(folder, meta['canonical_text'])
            if not source.is_file() or not source.read_text(encoding='utf-8').strip():
                raise ValueError(f'Published chapter has no selected manuscript: {folder.name}')
            if sha256(source) != meta['manuscript_sha256']:
                raise ValueError(f'Selected manuscript hash changed: {folder.name}; record author-approved selection before building')
        for product in read_json(folder / 'docs/PRODUCTS.json')['products']:
            if not safe_path(folder, product['path']).is_file():
                raise ValueError(f'Product claims a missing file: {folder.name}/{product["path"]}')
    if numbers != [f'{number:02d}' for number in range(len(numbers))] or len(numbers) > 99:
        raise ValueError('Portal chapters must be ordered consecutively from 00, with at most 99 slots')
    for asset in read_json(safe_path(root, registry['asset_manifest']))['assets']:
        if not safe_path(root, asset['source']).is_file():
            raise ValueError(f'Missing public asset source: {asset["source"]}')
        safe_path(root / 'dist', asset['public_path'])
    return registry
