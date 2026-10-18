"""Create a draft chapter or archive essay without replacing existing sources."""
import argparse
import re
import shutil
from common import ROOT, PRODUCT_DIRS, read_json, write_json

def create_chapter(root, slug, title, number=None, part=None, archive=False):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
        raise ValueError('Use a lowercase URL-safe slug')
    registry = read_json(root / 'book.json')
    destination = root / 'chapters' / slug
    if destination.exists() or slug in registry['chapters'] + registry.get('archive_chapters', []):
        raise ValueError('Chapter already exists; edit its existing folder')
    if archive:
        if number is not None or part is not None:
            raise ValueError('An archive essay must not take a portal number or part')
    else:
        expected = f'{len(registry["chapters"]):02d}'
        if len(registry['chapters']) >= 32:
            raise ValueError('All 32 portal slots already exist; edit a chapter folder or use --archive')
        if number != expected or part not in range(1, 6):
            raise ValueError(f'Use the next free editorial slot {expected} and a part from 1 to 5')
    shutil.copytree(root / 'templates/chapter', destination)
    for directory in PRODUCT_DIRS:
        target = destination / directory
        target.mkdir(parents=True, exist_ok=True)
        if not any(target.iterdir()):
            (target / '.gitkeep').touch()
    meta = read_json(destination / 'chapter.json')
    meta.update(slug=slug, title=title, short_title=title, number=number, part=part, canonical_path=f'#archive/{slug}' if archive else f'#chapter/{number}')
    write_json(destination / 'chapter.json', meta)
    products = read_json(destination / 'docs/PRODUCTS.json')
    products['chapter'] = slug
    write_json(destination / 'docs/PRODUCTS.json', products)
    registry.setdefault('archive_chapters' if archive else 'chapters', []).append(slug)
    write_json(root / 'book.json', registry)
    return destination

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--slug', required=True)
    parser.add_argument('--title', required=True)
    parser.add_argument('--number')
    parser.add_argument('--part', type=int)
    parser.add_argument('--archive', action='store_true')
    args = parser.parse_args()
    try:
        target = create_chapter(ROOT, **vars(args))
    except ValueError as error:
        parser.error(str(error))
    print(f'Created draft: {target} (publish=false).')

if __name__ == '__main__':
    main()
