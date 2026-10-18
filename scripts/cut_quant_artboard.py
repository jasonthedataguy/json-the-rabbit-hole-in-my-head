"""Reproducibly cut the Chapter 01 digital portal from the supplied artboard.

The board is an editorial reference, not a print-resolution master. The scene
and ring exports here are intended for the web reader at their displayed size.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / 'chapters/i-was-born-a-quant'
SOURCE = CHAPTER / 'references/editorial-artboard.png'
OUTPUT = CHAPTER / 'artwork/portal'

def cut():
    board = Image.open(SOURCE).convert('RGBA')
    if board.size != (1536, 1024):
        raise ValueError(f'Unexpected editorial artboard size: {board.size}')
    OUTPUT.mkdir(parents=True, exist_ok=True)

    # Alternative A / Expected Value is also the board's chapter-page choice.
    ring = board.crop((552, 70, 883, 416)).resize((1000, 1000), Image.Resampling.LANCZOS)
    mask = Image.new('L', (1000, 1000))
    draw = ImageDraw.Draw(mask)
    draw.ellipse((36, 15, 964, 985), fill=255)
    draw.ellipse((307, 310, 693, 690), fill=0)
    ring.putalpha(mask.filter(ImageFilter.GaussianBlur(1.2)))
    ring.save(OUTPUT / 'quant-ring.png', optimize=True)

    # The digital icon includes Jason, skyline and chart without baked-in type.
    # A square cut supports both the fixed homepage ring and the chapter portal.
    scene = board.crop((737, 688, 947, 898)).resize((1000, 1000), Image.Resampling.LANCZOS)
    scene.save(OUTPUT / 'quant-scene.png', optimize=True)

if __name__ == '__main__':
    cut()
