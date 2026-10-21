"""Cut the Play to Win digital ring and aligned game-table scene from its board.

The unchanged 1448x1086 concept board is preserved in references/design.
These raster crops are for screen display, not printer-resolution layers.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'references/design/model_specification - play to win dont play not to lose.png'
PORTAL = ROOT / 'chapters/play-to-win/artwork/portal'
WEB_ASSETS = ROOT / 'chapters/play-to-win/web/assets'
QA = ROOT / 'docs/qa'
SIZE = 1000


def cut():
    board = Image.open(SOURCE).convert('RGB')
    if board.size != (1448, 1086):
        raise ValueError(f'Unexpected Play to Win board size: {board.size}')

    # The main illustration's concentric layers share a centre at (285, 383).
    circle = board.crop((42, 140, 528, 626)).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    scene = board.crop((133, 231, 437, 535)).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    table = board.crop((114, 283, 458, 493))

    ring = circle.convert('RGBA')
    mask = Image.new('L', (SIZE, SIZE))
    draw = ImageDraw.Draw(mask)
    draw.ellipse((20, 20, 980, 980), fill=255)
    draw.ellipse((188, 188, 812, 812), fill=0)
    ring.putalpha(mask.filter(ImageFilter.GaussianBlur(1.1)))

    PORTAL.mkdir(parents=True, exist_ok=True)
    ring.save(PORTAL / 'play-to-win-ring-v2.png', optimize=True)
    scene.save(PORTAL / 'play-to-win-scene-v2.png', optimize=True)
    table.save(PORTAL / 'play-to-win-table-v2.webp', 'WEBP', quality=95, method=6)

    portal = Image.new('RGBA', (SIZE, SIZE))
    slot = scene.resize((624, 624), Image.Resampling.LANCZOS).convert('RGBA')
    slot_mask = Image.new('L', (624, 624))
    ImageDraw.Draw(slot_mask).ellipse((1, 1, 623, 623), fill=255)
    slot.putalpha(slot_mask.filter(ImageFilter.GaussianBlur(1.1)))
    portal.alpha_composite(slot, (188, 188))
    portal.alpha_composite(ring)
    portal.save(PORTAL / 'play-to-win-portal-v2.png', optimize=True)

    WEB_ASSETS.mkdir(parents=True, exist_ok=True)
    portal.save(WEB_ASSETS / 'play-to-win-portal-v2.png', optimize=True)
    table.save(WEB_ASSETS / 'play-to-win-table-v2.webp', 'WEBP', quality=95, method=6)

    QA.mkdir(parents=True, exist_ok=True)
    proof = Image.new('RGBA', (SIZE, SIZE), '#102331')
    proof.alpha_composite(portal)
    proof.convert('RGB').resize((700, 700), Image.Resampling.LANCZOS).save(
        QA / 'play-to-win-board-portal-composition.png', optimize=True
    )


if __name__ == '__main__':
    cut()
