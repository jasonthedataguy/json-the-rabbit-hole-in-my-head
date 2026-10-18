"""Extract Cold Rice's own paper-and-floral ring for map and reader use.

The author-supplied portal stays untouched. The cut uses a transparent centre
so the approved full-bleed dinner scene remains upright beneath the ring.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'chapters/com-nguoi/artwork/portal/rice-portal.png'
OUTPUT = ROOT / 'chapters/com-nguoi/artwork/portal/rice-ring.png'


def cut():
    source = Image.open(SOURCE).convert('RGBA')
    if source.size != (1254, 1254):
        raise ValueError(f'Unexpected Cold Rice portal size: {source.size}')
    ring = source.crop((44, 20, 1194, 1170)).resize((1000, 1000), Image.Resampling.LANCZOS)
    mask = Image.new('L', ring.size)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((20, 20, 980, 980), fill=255)
    draw.ellipse((188, 188, 812, 812), fill=0)
    ring.putalpha(mask.filter(ImageFilter.GaussianBlur(1.2)))
    ring.save(OUTPUT, optimize=True)


if __name__ == '__main__':
    cut()
