#!/usr/bin/env python3
"""Check that the deployed edition preserves all imported published manuscripts."""
import hashlib
import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'

class Assets(HTMLParser):
    def __init__(self):
        super().__init__(); self.paths = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {'script', 'img'} and attrs.get('src'): self.paths.append(attrs['src'])
        if tag == 'link' and attrs.get('href'): self.paths.append(attrs['href'])

def main():
    library = json.loads((DIST / 'content/manuscripts.json').read_text())
    assert len(library['chapters']) == 10, 'The original archive contains ten published chapters'
    ids = [c['editorialId'] for c in library['chapters'] if c['editorialId'] is not None]
    assert len(ids) == 9 and len(set(ids)) == 9, 'Nine evidence-based portal mappings are required'
    assert next(c for c in library['chapters'] if c['slug'] == 'dating-102')['editorialId'] is None
    total = 0
    for chapter in library['chapters']:
        raw = (ROOT / chapter['sourcePath']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == chapter['sha256'], chapter['slug']
        deployed = (DIST / 'content/manuscripts' / (chapter['slug'] + '.md')).read_bytes()
        assert raw == deployed, f'Deployed manuscript differs: {chapter["slug"]}'
        assert '<script' not in chapter['html'].lower(), 'Rendered manuscripts must be inert'
        assert chapter['bodyHtml'] and chapter['plainText'], chapter['slug']
        assert chapter['archiveUrl'].startswith('https://jasonthedataguy.github.io/json-under-revision/chapters/')
        total += len(raw)
    parser = Assets(); parser.feed((DIST / 'index.html').read_text())
    for src in parser.paths:
        parsed = urlsplit(src)
        if parsed.scheme or parsed.netloc: continue
        assert not parsed.path.startswith('/'), f'Use a relative asset URL for GitHub Pages: {src}'
        assert (DIST / unquote(parsed.path)).is_file(), f'Missing public asset: {src}'
    for name in ['app.js', 'book.js', 'chapters.js', 'ring.js', 'markers.js', 'style.css', 'assets/bowl-reference.jpg']:
        assert (DIST / name).is_file(), name
    print(f'Passed: 10 byte-identical manuscripts ({total:,} bytes), 9 portal mappings, complete static assets.')

if __name__ == '__main__':
    main()
