"""Cut the For Mother Russia digital portal from the supplied concept board.

The original 1448x1086 board remains unchanged in references/design. These
crops are for the screen edition, not printer-resolution separated layers.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'references/design/data_collection - for mother russia.png'
PORTAL = ROOT / 'chapters/for-mother-russia/artwork/portal'
WEB_ASSETS = ROOT / 'chapters/for-mother-russia/web/assets'
QA = ROOT / 'docs/qa'
SIZE = 1000


def cut():
    board = Image.open(SOURCE).convert('RGB')
    if board.size != (1448, 1086):
        raise ValueError(f'Unexpected For Mother Russia board size: {board.size}')

    # All circular cuts share the main illustration's centre at (215, 314).
    circle = board.crop((18, 117, 412, 511)).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    scene = board.crop((92, 191, 338, 437)).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    cover_scene = board.crop((128, 228, 308, 408)).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    cabin = board.crop((9, 543, 249, 693))

    ring = circle.convert('RGBA')
    mask = Image.new('L', (SIZE, SIZE))
    draw = ImageDraw.Draw(mask)
    draw.ellipse((20, 20, 980, 980), fill=255)
    # Keep the child entirely on the rotating ring; the head must not stay
    # behind in the stationary picture when the reader turns the page.
    draw.ellipse((240, 240, 760, 760), fill=0)
    ring.putalpha(mask.filter(ImageFilter.GaussianBlur(1.1)))

    PORTAL.mkdir(parents=True, exist_ok=True)
    WEB_ASSETS.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    ring.save(PORTAL / 'mother-russia-ring-v2.png', optimize=True)
    scene.save(PORTAL / 'mother-russia-scene-v2.png', optimize=True)
    cover_scene.save(PORTAL / 'mother-russia-cover-scene-v2.png', optimize=True)
    cabin.save(PORTAL / 'mother-russia-cabin-v2.webp', 'WEBP', quality=96, method=6)

    portal = Image.new('RGBA', (SIZE, SIZE))
    slot = scene.resize((624, 624), Image.Resampling.LANCZOS).convert('RGBA')
    slot_mask = Image.new('L', (624, 624))
    ImageDraw.Draw(slot_mask).ellipse((1, 1, 623, 623), fill=255)
    slot.putalpha(slot_mask.filter(ImageFilter.GaussianBlur(1.1)))
    portal.alpha_composite(slot, (188, 188))
    portal.alpha_composite(ring)
    portal.save(PORTAL / 'mother-russia-portal-v2.png', optimize=True)
    portal.save(WEB_ASSETS / 'mother-russia-portal-v2.png', optimize=True)
    cabin.save(WEB_ASSETS / 'mother-russia-cabin-v2.webp', 'WEBP', quality=96, method=6)

    proof = Image.new('RGBA', (SIZE, SIZE), '#102331')
    proof.alpha_composite(portal)
    proof.convert('RGB').resize((700, 700), Image.Resampling.LANCZOS).save(
        QA / 'mother-russia-board-portal-composition.png', optimize=True
    )


if __name__ == '__main__':
    cut()
