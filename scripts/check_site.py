"""Validate sources, preserved manuscripts, generated files and local web links."""
import re
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from common import ROOT, read_json, safe_path, sha256, chapter_entries, validate_project

DIST = ROOT / 'dist'

class Assets(HTMLParser):
    def __init__(self):
        super().__init__(); self.paths = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ('src', 'href', 'poster', 'data-image'):
            if attrs.get(key):
                self.paths.append(attrs[key])
        if attrs.get('srcset'):
            self.paths += [part.strip().split()[0] for part in attrs['srcset'].split(',') if part.strip()]

def local_link(source, value):
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    if parsed.path.startswith('/'):
        raise ValueError(f'Non-relative public link in {source.relative_to(DIST)}: {value}')
    target = (source.parent / unquote(parsed.path)).resolve()
    if not target.is_relative_to(DIST.resolve()):
        raise ValueError(f'Public link escapes the site: {value}')
    if target.is_dir():
        target = target / 'index.html'
    return target

def check_site():
    registry = validate_project()
    library = read_json(DIST / 'content/manuscripts.json')
    expected = {m['slug'] for _, m in chapter_entries() if m['publish']}
    assert {c['slug'] for c in library['chapters']} == expected, 'Published manuscript coverage changed'
    for chapter in library['chapters']:
        source = safe_path(ROOT, chapter['sourcePath'])
        assert sha256(source) == chapter['sha256'], chapter['slug']
        assert source.read_bytes() == safe_path(DIST, chapter['downloadUrl']).read_bytes(), chapter['slug']
        assert chapter['bodyHtml'] and '<script' not in chapter['html'].lower(), chapter['slug']
        meta = read_json(ROOT / 'chapters' / chapter['slug'] / 'chapter.json')
        assert chapter['editorialId'] == meta['number'], chapter['slug']
        for field in ('experienceUrl', 'printUrl', 'filmUrl'):
            if chapter.get(field):
                assert safe_path(DIST, chapter[field]).is_file(), chapter[field]
    mapping = read_json(ROOT / 'references/original-edition/manuscript-map.json')
    for item in mapping['chapters']:
        original = ROOT / 'chapters' / item['slug'] / 'references/original-edition/approved.md'
        assert sha256(original) == item['manuscriptSha256'], f'Pinned original changed: {item["slug"]}'
    for record in read_json(ROOT / 'docs/MIGRATION.json')['files']:
        path = record['path']
        if '/references/' in path or path.startswith('references/') or path.endswith('/source/original.md'):
            assert sha256(safe_path(ROOT, path)) == record['sha256'], f'Preserved input changed: {path}'
    manifest = read_json(DIST / 'build-manifest.json')
    for relative, digest in manifest['inputs'].items():
        assert sha256(safe_path(ROOT, relative)) == digest, f'Source changed; rebuild dist: {relative}'
    for record in manifest['generated_files']:
        assert sha256(safe_path(DIST, record['path'])) == record['sha256'], f'Generated output changed: {record["path"]}'
    failures = []
    for page in sorted(DIST.rglob('*.html')):
        parser = Assets(); parser.feed(page.read_text(encoding='utf-8'))
        for value in parser.paths:
            target = local_link(page, value)
            if target is not None and not target.is_file():
                failures.append(f'{page.relative_to(DIST)} -> {value}')
    for source in sorted(DIST.glob('*.js')):
        for value in re.findall(r'(?:from\s*|import\s*)[\"\']([^\"\']+)[\"\']', source.read_text(encoding='utf-8')):
            target = local_link(source, value)
            if target is not None and not target.is_file():
                failures.append(f'{source.name} -> {value}')
    for source in sorted(DIST.rglob('*.css')):
        for value in re.findall(r'url\([\"\']?([^\)\"\']+)', source.read_text(encoding='utf-8')):
            target = local_link(source, value)
            if target is not None and not target.is_file():
                failures.append(f'{source.relative_to(DIST)} -> {value}')
    assert not failures, 'Missing local links:\n' + '\n'.join(sorted(set(failures)))
    print(f'Passed: {len(registry["chapters"])} editorial chapters, {len(library["chapters"])} exact manuscripts, protected originals, generated files and local web links.')

if __name__ == '__main__':
    check_site()
