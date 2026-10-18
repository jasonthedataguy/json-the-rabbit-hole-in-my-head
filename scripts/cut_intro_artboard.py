"""Cut the Introduction's editorial ring from the author-supplied concept board.

The source artboard stays unchanged in references/design/. This export is for
the digital Introduction leaf; the editorial board is not a print master.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'references/design/Jason, Under Revision Concept Board - introduction.png'
OUTPUT = ROOT / 'shared/artwork/portal/introduction-ring.png'


def cut():
    board = Image.open(SOURCE).convert('RGBA')
    if board.size != (1672, 941):
        raise ValueError(f'Unexpected Introduction artboard size: {board.size}')

    ring = board.crop((18, 55, 718, 745)).resize((1000, 1000), Image.Resampling.LANCZOS)
    mask = Image.new('L', ring.size)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((12, 10, 988, 985), fill=255)
    draw.ellipse((294, 303, 707, 725), fill=0)
    ring.putalpha(mask.filter(ImageFilter.GaussianBlur(1.2)))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    ring.save(OUTPUT, optimize=True)


if __name__ == '__main__':
    cut()
