"""Cut aligned digital Cold Rice portal layers from the preserved concept board.

The 1448x1086 reference is never modified. These screen crops are not print masters.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'references/design/prologue - cold rice.png'
PORTAL = ROOT / 'chapters/com-nguoi/artwork/portal'
WEB_ASSETS = ROOT / 'chapters/com-nguoi/web/assets'
QA = ROOT / 'docs/qa'
SIZE = 1000


def cut():
    board = Image.open(SOURCE).convert('RGB')
    if board.size != (1448, 1086):
        raise ValueError(f'Unexpected Cold Rice board size: {board.size}')

    # The upper-left illustration is centred on (212, 312). The scene is
    # exactly the area exposed by the ring's 624 px circular aperture.
    circle = board.crop((16, 116, 408, 508)).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    scene = board.crop((90, 190, 334, 434)).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    dinner = board.crop((66, 205, 362, 403))

    ring = circle.convert('RGBA')
    mask = Image.new('L', (SIZE, SIZE))
    draw = ImageDraw.Draw(mask)
    draw.ellipse((20, 20, 980, 980), fill=255)
    draw.ellipse((188, 188, 812, 812), fill=0)
    ring.putalpha(mask.filter(ImageFilter.GaussianBlur(1.1)))

    PORTAL.mkdir(parents=True, exist_ok=True)
    ring.save(PORTAL / 'rice-ring-board-v2.png', optimize=True)
    scene.save(PORTAL / 'rice-scene-board-v2.png', optimize=True)
    dinner.save(PORTAL / 'rice-family-room-v2.webp', 'WEBP', quality=95, method=6)

    portal = Image.new('RGBA', (SIZE, SIZE))
    slot = scene.resize((624, 624), Image.Resampling.LANCZOS).convert('RGBA')
    slot_mask = Image.new('L', (624, 624))
    ImageDraw.Draw(slot_mask).ellipse((1, 1, 623, 623), fill=255)
    slot.putalpha(slot_mask.filter(ImageFilter.GaussianBlur(1.1)))
    portal.alpha_composite(slot, (188, 188))
    portal.alpha_composite(ring)
    portal.save(PORTAL / 'rice-portal-board-v2.png', optimize=True)

    WEB_ASSETS.mkdir(parents=True, exist_ok=True)
    portal.save(WEB_ASSETS / 'rice-portal-board-v2.png', optimize=True)
    dinner.save(WEB_ASSETS / 'rice-family-room-v2.webp', 'WEBP', quality=95, method=6)

    QA.mkdir(parents=True, exist_ok=True)
    proof = Image.new('RGBA', (SIZE, SIZE), '#102331')
    proof.alpha_composite(portal)
    proof.convert('RGB').resize((700, 700), Image.Resampling.LANCZOS).save(
        QA / 'cold-rice-board-portal-composition.png', optimize=True
    )


if __name__ == '__main__':
    cut()
