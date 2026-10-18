"""Build the portal reader and local immersive chapter collections from sources."""
import argparse
import json
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, urlsplit, unquote
from common import ROOT, chapter_entries, read_json, write_json, safe_path, sha256, validate_project
from manuscript import render_markdown, inline, PlainText

MARKER = 'json-under-revision-v2 generated site\n'
PUBLIC_GROUPS = ('book', 'audio', 'video', 'social', 'previews')
PUBLIC_SUFFIXES = {'.jpg', '.jpeg', '.png', '.webp', '.svg', '.pdf', '.mp4', '.wav', '.mp3', '.m4a', '.srt', '.vtt', '.md', '.txt', '.html', '.css', '.js', '.json', '.zip', '.csv', '.log'}
BUILD_INPUTS = {}

class RuntimeLinks(HTMLParser):
    def __init__(self):
        super().__init__(); self.paths = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.paths.extend(attrs[key] for key in ('href', 'src', 'poster', 'data-image') if attrs.get(key))
        if attrs.get('srcset'):
            self.paths.extend(item.strip().split()[0] for item in attrs['srcset'].split(',') if item.strip())

def immersive_page(folder, target):
    source = folder / 'web/index.html'
    page = source.read_text(encoding='utf-8')
    # Some old offline pages missed poster/srcset paths during their original build.
    page = re.sub(r'((?:href|src|srcset|poster|data-image)=[\"\'])(artwork|book|audio|video|social|source|docs|previews)/', r'\1../\2/', page)
    parser = RuntimeLinks(); parser.feed(page)
    for value in parser.paths:
        url = urlsplit(value)
        if url.scheme or url.netloc or not url.path:
            continue
        dependency = (source.parent / unquote(url.path)).resolve()
        if dependency.is_relative_to(folder.resolve()) and dependency.is_file():
            if dependency.suffix.lower() not in PUBLIC_SUFFIXES:
                raise ValueError(f'Unsupported public dependency: {dependency}')
            # Only explicitly linked source SVGs, notes or blank worksheets are exposed.
            copy_file(dependency, target / dependency.relative_to(folder.resolve()))
    (target / 'web').mkdir(parents=True, exist_ok=True)
    (target / 'web/index.html').write_text(page, encoding='utf-8')
    BUILD_INPUTS[source.relative_to(ROOT).as_posix()] = sha256(source)

def generated_directory(path):
    allowed = {ROOT.resolve() / 'dist', ROOT.resolve() / '.build/site'}
    if path.is_symlink() or path.resolve() not in allowed:
        raise ValueError(f'Refusing to clean non-generated directory: {path}')
    if path.exists():
        marker = path / '.build-output'
        if not marker.is_file() or marker.read_text(encoding='utf-8') != MARKER:
            raise ValueError(f'Refusing to replace directory without build marker: {path}')
        shutil.rmtree(path)
    path.mkdir(parents=True)
    (path / '.build-output').write_text(MARKER, encoding='utf-8')

def copy_file(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    if source.resolve().is_relative_to(ROOT.resolve()):
        BUILD_INPUTS[source.relative_to(ROOT).as_posix()] = sha256(source)

def copy_public_tree(source, target):
    if source.exists():
        for path in sorted(source.rglob('*')):
            if path.is_file() and path.suffix.lower() in PUBLIC_SUFFIXES:
                copy_file(path, target / path.relative_to(source))

def build_library(output, entries):
    chapters = []
    for folder, meta in entries:
        if not meta['publish']:
            continue
        manuscript = safe_path(folder, meta['canonical_text'])
        raw = manuscript.read_bytes()
        body, heading, count = render_markdown(raw.decode('utf-8'))
        full = (f'<h2>{inline(heading)}</h2>\n' if heading else '') + body
        plain = PlainText(); plain.feed(full)
        original = meta['original_edition']
        old = read_json(safe_path(folder, original['metadata'])) if original else {}
        public_path = f'content/manuscripts/{meta["slug"]}.md'
        copy_file(manuscript, output / public_path)
        chapters.append({
            'slug': meta['slug'], 'editorialId': meta['number'],
            'legacyId': original['number'] if original else None,
            'originalTitle': old.get('title', meta['title']), 'title': old.get('title', meta['title']),
            'originalHeading': heading, 'language': meta['language'], 'subtitle': old.get('subtitle', ''),
            'html': full, 'bodyHtml': body, 'plainText': plain.result(), 'paragraphCount': count,
            'sourcePath': manuscript.relative_to(ROOT).as_posix(),
            'sha256': sha256(manuscript), 'bytes': len(raw), 'downloadUrl': public_path,
            'archiveUrl': original['archive_url'] if original else None,
            'sourceUrl': original['repo'] + '/blob/' + original['commit'] + '/' + quote('chapters/' + meta['slug'] + '/' + old['canonical_text']) if original else None,
            'experienceUrl': f'chapters/{meta["slug"]}/web/index.html' if (folder / 'web/index.html').is_file() else None,
            'originalSourcePath': 'chapters/' + meta['slug'] + '/' + old['canonical_text'] if original else None,
            'originalMetadataPath': 'chapters/' + meta['slug'] + '/chapter.json' if original else None,
        })
    mapping = read_json(ROOT / 'references/original-edition/manuscript-map.json')
    source = {'repo': mapping['sourceRepo'], 'commit': mapping['sourceCommit'], 'url': mapping['sourceRepo'] + '/tree/' + mapping['sourceCommit']}
    library = {'source': source, 'chapters': chapters}
    write_json(output / 'content/manuscripts.json', library)
    return library

def build_site():
    BUILD_INPUTS.clear()
    registry = validate_project()
    entries = list(chapter_entries())
    dependencies = [ROOT / 'book.json', ROOT / registry['asset_manifest'], ROOT / 'references/original-edition/manuscript-map.json']
    dependencies += list((ROOT / 'scripts').glob('*.py'))
    for folder, meta in entries:
        dependencies += [folder / 'chapter.json', folder / 'docs/PRODUCTS.json']
        if meta['original_edition']:
            dependencies.append(safe_path(folder, meta['original_edition']['metadata']))
    for source in dependencies:
        BUILD_INPUTS[source.relative_to(ROOT).as_posix()] = sha256(source)
    staging = ROOT / '.build/site'
    generated_directory(staging)
    for source in (ROOT / 'shared/web').iterdir():
        if source.is_file():
            copy_file(source, staging / source.name)
    for asset in read_json(ROOT / registry['asset_manifest'])['assets']:
        copy_file(safe_path(ROOT, asset['source']), safe_path(staging, asset['public_path']))
    portals = []
    notes = {}
    for folder, meta in entries:
        if meta['number'] is not None:
            portals.append({'id': meta['number'], 'slug': meta['slug'], 'title': meta['title'], 'shortTitle': meta['short_title'], 'act': meta['part'], **meta['portal']})
            notes[meta['number']] = {'title': meta.get('outline_title', meta['title']), 'summary': meta['summary']}
    def js(value):
        return json.dumps(value, ensure_ascii=False, indent=2)
    (staging / 'chapter-data.js').write_text('// Generated from book.json and chapters/*/chapter.json.\nexport const chapters = ' + js(portals) + ';\nexport const acts = ' + js(registry['acts']) + ';\n', encoding='utf-8')
    (staging / 'book.js').write_text('// Generated from the source registry; edit book.json or chapter.json.\n' + '\n'.join('export const ' + name + ' = ' + js(value) + ';' for name, value in [('introduction', registry['introduction']), ('parts', registry['parts']), ('chapterNotes', notes)]) + '\n', encoding='utf-8')
    library = build_library(staging, entries)
    products = []
    for folder, meta in entries:
        if not meta['publish']:
            continue
        target = staging / 'chapters' / meta['slug']
        for group in PUBLIC_GROUPS:
            copy_public_tree(folder / group, target / group)
        for group in ('artwork/exports', 'artwork/scenes', 'web/assets'):
            copy_public_tree(folder / group, target / group)
        for path in (folder / 'web').iterdir():
            if path.is_file() and path.suffix in {'.css', '.js'}:
                copy_file(path, target / 'web' / path.name)
        for name in ('original.md', 'approved.md', 'revisions.log'):
            source = folder / 'source' / name
            if source.is_file():
                copy_file(source, target / 'source' / name)
        if (folder / 'web/index.html').is_file():
            immersive_page(folder, target)
        chapter_products = []
        for product in read_json(folder / 'docs/PRODUCTS.json')['products']:
            candidate = safe_path(target, product['path'])
            if candidate.is_file():
                chapter_products.append({**product, 'url': candidate.relative_to(staging).as_posix()})
        products.append({'slug': meta['slug'], 'edition': 'original' if meta['original_edition'] else 'v2', 'originalNumber': (meta['original_edition'] or {}).get('number'), 'products': chapter_products})
        manuscript = next(c for c in library['chapters'] if c['slug'] == meta['slug'])
        manuscript['printUrl'] = next((p['url'] for p in chapter_products if p['path'].startswith('book/') and p['path'].endswith('.pdf')), None)
        manuscript['filmUrl'] = next((p['url'] for p in chapter_products if p['path'].endswith('.mp4')), None)
    for name in ('site.css', 'site.js'):
        copy_file(ROOT / 'shared' / name, staging / 'shared' / name)
    write_json(staging / 'content/products.json', {'chapters': products})
    write_json(staging / 'content/manuscripts.json', library)
    (staging / '.nojekyll').touch()
    write_json(staging / 'build-manifest.json', {'source': 'book.json', 'chapters': len(portals), 'manuscripts': len(library['chapters']), 'inputs': BUILD_INPUTS, 'generated_files': [{'path': p.relative_to(staging).as_posix(), 'bytes': p.stat().st_size, 'sha256': sha256(p)} for p in sorted(staging.rglob('*')) if p.is_file() and p.name != 'build-manifest.json']})
    generated_directory(ROOT / 'dist')
    # Both paths were verified as this repository's generated directories above.
    for path in staging.iterdir():
        destination = ROOT / 'dist' / path.name
        if path.is_dir():
            shutil.move(str(path), str(destination))
        else:
            shutil.copyfile(path, destination)
    write_json(ROOT / 'docs/source-provenance.json', {'source': library['source'], 'policy': 'The selected sourcePath lives in the chapter source folder. Pinned original manuscripts and metadata are retained under chapter references. Editorial and original numbers remain independent.', 'chapters': [{key: c[key] for key in ('slug', 'editorialId', 'legacyId', 'originalTitle', 'sourcePath', 'sha256', 'bytes', 'archiveUrl', 'sourceUrl')} for c in library['chapters']]})
    print(f'Built {len(portals)} portal chapters, {len(library["chapters"])} manuscripts and local immersive product collections in dist/.')

if __name__ == '__main__':
    argparse.ArgumentParser(description=__doc__).parse_args()
    build_site()
