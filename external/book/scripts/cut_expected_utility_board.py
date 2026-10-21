"""Derive the Expected Utility digital portal from the supplied concept board.

The unchanged board lives in references/design. Its 604-pixel main illustration
supports screen artwork, not a printer-resolution master.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'references/design/Expected Utility_ Portal Layers Board.png'
PORTAL = ROOT / 'chapters/expected-utility/artwork/portal'
WEB_ASSETS = ROOT / 'chapters/expected-utility/web/assets'
QA = ROOT / 'docs/qa'
SIZE = 1000


def cut():
    board = Image.open(SOURCE).convert('RGB')
    if board.size != (1536, 1024):
        raise ValueError(f'Unexpected Expected Utility board size: {board.size}')

    # The upper-left artwork is centred at (322, 315). Both cuts share that
    # centre, so the laptop and eyes meet the annular collage without a seam.
    circle = board.crop((20, 13, 624, 617)).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    scene = board.crop((134, 127, 510, 503)).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    desk = board.crop((132, 247, 514, 447))

    ring = circle.convert('RGBA')
    mask = Image.new('L', (SIZE, SIZE))
    draw = ImageDraw.Draw(mask)
    draw.ellipse((20, 20, 980, 980), fill=255)
    draw.ellipse((188, 188, 812, 812), fill=0)
    ring.putalpha(mask.filter(ImageFilter.GaussianBlur(1.1)))

    PORTAL.mkdir(parents=True, exist_ok=True)
    ring.save(PORTAL / 'expected-utility-ring-v2.png', optimize=True)
    scene.save(PORTAL / 'expected-utility-scene-v2.png', optimize=True)
    desk.save(PORTAL / 'expected-utility-desk-v2.webp', 'WEBP', quality=95, method=6)

    portal = Image.new('RGBA', (SIZE, SIZE))
    slot = scene.resize((624, 624), Image.Resampling.LANCZOS).convert('RGBA')
    slot_mask = Image.new('L', (624, 624))
    ImageDraw.Draw(slot_mask).ellipse((1, 1, 623, 623), fill=255)
    slot.putalpha(slot_mask.filter(ImageFilter.GaussianBlur(1.1)))
    portal.alpha_composite(slot, (188, 188))
    portal.alpha_composite(ring)
    portal.save(PORTAL / 'expected-utility-portal-v2.png', optimize=True)

    WEB_ASSETS.mkdir(parents=True, exist_ok=True)
    portal.save(WEB_ASSETS / 'expected-utility-portal-v2.png', optimize=True)
    desk.save(WEB_ASSETS / 'expected-utility-desk-v2.webp', 'WEBP', quality=95, method=6)

    QA.mkdir(parents=True, exist_ok=True)
    proof = Image.new('RGBA', (SIZE, SIZE), '#102331')
    proof.alpha_composite(portal)
    proof.convert('RGB').resize((700, 700), Image.Resampling.LANCZOS).save(
        QA / 'expected-utility-board-portal-composition.png', optimize=True
    )


if __name__ == '__main__':
    cut()
