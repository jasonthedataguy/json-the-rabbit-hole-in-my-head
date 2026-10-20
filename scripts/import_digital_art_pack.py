"""Install the web artwork roles from the author's digital-book asset archive.

The 5.4 GB archive contains native masters and historical references. This
imports its independently versioned screen exports; the archive remains the
source for edit masters and reusable cutouts.
"""
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

from common import ROOT

DEFAULT_ARCHIVE = Path(r'C:\Users\Administrator\Documents\Codex\2026-10-19\can\outputs\json-digital-book-assets.zip')
ARCHIVE_ROOT = 'json-digital-book-assets/'
ROLES = {
    'main_book': 'mainBook',
    'chapter_map': 'map',
    'chapter_opening': 'opening',
    'reader_hero': 'hero',
    'inline_illustration': 'inline',
}


def intake(zf, source, destination, expected_hash=None):
    data = zf.read(ARCHIVE_ROOT + source)
    digest = hashlib.sha256(data).hexdigest()
    if expected_hash and digest != expected_hash:
        raise ValueError(f'Hash mismatch: {source}')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    return digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, default=DEFAULT_ARCHIVE)
    args = parser.parse_args()
    chapter_slugs = {json.loads(path.read_text(encoding='utf-8'))['slug'] for path in (ROOT / 'chapters').glob('*/chapter.json')}
    with ZipFile(args.archive) as zf:
        raw_manifest = zf.read(ARCHIVE_ROOT + 'assets-manifest.json')
        manifest = json.loads(raw_manifest)
        entries = manifest['chapters']
        pack_slugs = {entry['slug'] for entry in entries}
        if pack_slugs != chapter_slugs | {'introduction'}:
            raise ValueError(f'Chapter-slug mismatch: missing {chapter_slugs - pack_slugs}; extra {pack_slugs - chapter_slugs - {"introduction"}}')
        library = {}
        additions = {}
        for entry in entries:
            slug = entry['slug']
            roles = {}
            for source_role, key in ROLES.items():
                web = entry['roles'][source_role]['web']
                source = web['path']
                local = f'shared/artwork/digital-book/{slug}/{key}.webp'
                public = f'assets/digital-book/{slug}/{key}.webp'
                digest = intake(zf, source, ROOT / local, web['sha256'])
                roles[key] = f'{public}?v={digest[:12]}'
                additions[public] = {
                    'source': local, 'public_path': public, 'sha256_at_intake': digest,
                    'provenance': f'Author asset archive: {source}. Placement: {source_role}; native master retained in the supplied ZIP.'
                }
            centre_source = f'chapters/{slug}/artwork/main-book/centre-scene.webp'
            local = f'shared/artwork/digital-book/{slug}/centre.webp'
            public = f'assets/digital-book/{slug}/centre.webp'
            digest = intake(zf, centre_source, ROOT / local)
            roles['centre'] = f'{public}?v={digest[:12]}'
            additions[public] = {
                'source': local, 'public_path': public, 'sha256_at_intake': digest,
                'provenance': f'Author asset archive: {centre_source}. Stationary centre for the rotating main-book ring.'
            }
            extras = []
            for number, illustration in enumerate(entry.get('additional_illustrations', []), start=2):
                web = illustration.get('web', illustration)
                source = web.get('path')
                if not source:
                    raise ValueError(f'Missing additional illustration path for {slug}')
                local = f'shared/artwork/digital-book/{slug}/inline-{number:02d}.webp'
                public = f'assets/digital-book/{slug}/inline-{number:02d}.webp'
                digest = intake(zf, source, ROOT / local, web.get('sha256'))
                extras.append(f'{public}?v={digest[:12]}')
                additions[public] = {
                    'source': local, 'public_path': public, 'sha256_at_intake': digest,
                    'provenance': f'Author asset archive: {source}. Additional in-content illustration.'
                }
            roles['extras'] = extras
            library[slug] = roles
        ring_source = 'shared/main-book/rotating-ring-no-observer.png'
        ring_local = 'shared/artwork/digital-book/rotating-ring-no-observer.png'
        ring_public = 'assets/digital-book/rotating-ring-no-observer.png'
        ring_digest = intake(zf, ring_source, ROOT / ring_local)
        additions[ring_public] = {
            'source': ring_local, 'public_path': ring_public, 'sha256_at_intake': ring_digest,
            'provenance': f'Author asset archive: {ring_source}. Observer-free shared rotating book ring.'
        }
        cover_source = 'shared/main-book/main-book-portal.webp'
        cover_local = 'shared/artwork/digital-book/main-book-cover-portal.webp'
        cover_public = 'assets/digital-book/main-book-cover-portal.webp'
        cover_digest = intake(zf, cover_source, ROOT / cover_local)
        additions[cover_public] = {
            'source': cover_local, 'public_path': cover_public, 'sha256_at_intake': cover_digest,
            'provenance': f'Author asset archive: {cover_source}. Complete portal for the default book-cover stop.'
        }
        reference = ROOT / 'references/digital-book-asset-pack'
        for source, target in [
            ('assets-manifest.json', 'assets-manifest.json'),
            ('quality-report.json', 'quality-report.json'),
            ('integration/runtime-asset-map.json', 'runtime-asset-map.json'),
        ]:
            intake(zf, source, reference / target)
    assets_path = ROOT / 'shared/assets.json'
    assets = json.loads(assets_path.read_text(encoding='utf-8'))
    assets['assets'] = [item for item in assets['assets'] if not item['public_path'].startswith('assets/digital-book/')]
    assets['assets'].extend(additions.values())
    assets_path.write_text(json.dumps(assets, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    module = ROOT / 'shared/web/digital-art.js'
    module.write_text('// Screen exports from the author-supplied digital-book asset library.\n'
                      'export const digitalArt = Object.freeze(' + json.dumps(library, ensure_ascii=False, indent=2) + ');\n'
                      f'export const digitalRing = {json.dumps(ring_public + "?v=" + ring_digest[:12])};\n'
                      f'export const digitalCoverPortal = {json.dumps(cover_public + "?v=" + cover_digest[:12])};\n', encoding='utf-8')
    print(f'Installed {len(additions)} screen assets for {len(library)} portal sets; all archive hashes matched.')


if __name__ == '__main__':
    main()
