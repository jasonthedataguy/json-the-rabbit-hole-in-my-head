"""Verify the generated print prototype without a PDF rendering dependency."""

import hashlib
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'print/manifest.json').read_text(encoding='utf-8'))
assert manifest['trim_mm'] == [152.4, 228.6]
assert manifest['bleed_mm'] == 3.175
assert manifest['raster_ppi'] == 300

for entry in manifest['files']:
    path = ROOT / entry['path']
    assert path.is_file(), path
    assert path.stat().st_size == entry['bytes'], path
    assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256'], path

for name in ('cover-saigon-scene-3000.png', 'cold-rice-scene-3000.png'):
    with Image.open(ROOT / 'print/assets' / name) as image:
        assert image.size == (3000, 3000), name

for name in ('cover-ring-3000.png', 'chapter-ring-3000.png'):
    with Image.open(ROOT / 'print/assets' / name) as ring:
        assert ring.mode == 'RGBA' and ring.size == (3000, 3000), name
        minimum, maximum = ring.getchannel('A').getextrema()
        assert minimum == 0 and maximum == 255, name

pdfs = sorted((ROOT / 'output/pdf').glob('*.pdf'))
assert len(pdfs) == 5, pdfs
for path in pdfs:
    data = path.read_bytes()
    assert data.startswith(b'%PDF-'), path
    assert len(re.findall(rb'/Type\s*/Page\b', data)) == 1, path
    box = re.search(rb'/MediaBox\s*\[([^]]+)\]', data)
    assert box, path
    x0, y0, x1, y1 = map(float, box.group(1).split())
    with Image.open(ROOT / 'print/proofs' / (path.stem + '.png')) as proof:
        expected = (proof.width / 300 * 72, proof.height / 300 * 72)
        actual = (x1 - x0, y1 - y0)
        assert all(abs(a - b) <= 0.02 for a, b in zip(actual, expected)), (path, actual, expected)
    print(f'{path.name}: {actual[0]:.2f} x {actual[1]:.2f} pt, 1 page, 300 ppi')

for name in ('cover-wrap-dieline.svg', 'chapter-00-dieline.svg'):
    data = (ROOT / 'print/cut' / name).read_text(encoding='utf-8')
    assert 'optional-cover-aperture-cut' in data or 'chapter-aperture-cut' in data
print('Manifest hashes, scene sizes, and cut paths: OK')
