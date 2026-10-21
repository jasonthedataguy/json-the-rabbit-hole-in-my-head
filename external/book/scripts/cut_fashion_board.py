"""Cut Fashion's digital portal and room scene from the supplied design board.

The board is preserved unchanged in references/design. These crops are for the
web edition; the board does not contain print-resolution illustration layers.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'references/design/Fashion Chapter Digital Book Board - final.png'
PORTAL = ROOT / 'chapters/fashion/artwork/portal'
WEB_ASSETS = ROOT / 'chapters/fashion/web/assets'
QA = ROOT / 'docs/qa'
SIZE = 1000


def cut():
    board = Image.open(SOURCE).convert('RGB')
    if board.size != (1448, 1086):
        raise ValueError(f'Unexpected Fashion artboard size: {board.size}')

    # Main laptop illustration. Cropping just inside the overlaid navigation
    # arrows keeps the chapter artwork free of controls from the mockup.
    circle = board.crop((230, 107, 528, 405)).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    # The mockup's previous/next buttons overlap a few outer pixels at 3 and
    # 9 o'clock. Continue the adjacent paper artwork over those small areas.
    for angle, box in ((-24, (-16, 458, 78, 612)), (24, (925, 451, 1018, 605))):
        donor = circle.rotate(angle, Image.Resampling.BICUBIC, center=(500, 500))
        repair = Image.new('L', (SIZE, SIZE))
        ImageDraw.Draw(repair).ellipse(box, fill=255)
        circle = Image.composite(donor, circle, repair.filter(ImageFilter.GaussianBlur(12)))
    # This is exactly the centre 62.4% of the same square crop. The picture
    # therefore meets the transparent ring aperture without an alignment seam.
    scene = board.crop((286, 163, 472, 349)).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    room = board.crop((822, 794, 1415, 958))

    ring = circle.convert('RGBA')
    mask = Image.new('L', (SIZE, SIZE))
    draw = ImageDraw.Draw(mask)
    draw.ellipse((20, 20, 980, 980), fill=255)
    draw.ellipse((188, 188, 812, 812), fill=0)
    ring.putalpha(mask.filter(ImageFilter.GaussianBlur(1.1)))

    PORTAL.mkdir(parents=True, exist_ok=True)
    ring.save(PORTAL / 'fashion-ring-v2.png', optimize=True)
    scene.save(PORTAL / 'fashion-scene-v2.png', optimize=True)
    room.save(PORTAL / 'fashion-room-v2.webp', 'WEBP', quality=94, method=6)
    WEB_ASSETS.mkdir(parents=True, exist_ok=True)
    room.save(WEB_ASSETS / 'fashion-room-v2.webp', 'WEBP', quality=94, method=6)

    portal = Image.new('RGBA', (SIZE, SIZE))
    slot = scene.resize((624, 624), Image.Resampling.LANCZOS).convert('RGBA')
    slot_mask = Image.new('L', (624, 624))
    ImageDraw.Draw(slot_mask).ellipse((1, 1, 623, 623), fill=255)
    slot.putalpha(slot_mask.filter(ImageFilter.GaussianBlur(1.1)))
    portal.alpha_composite(slot, (188, 188))
    portal.alpha_composite(ring)
    portal.save(PORTAL / 'fashion-portal-v2.png', optimize=True)
    portal.save(WEB_ASSETS / 'fashion-portal-v2.png', optimize=True)

    QA.mkdir(parents=True, exist_ok=True)
    proof = Image.new('RGBA', (SIZE, SIZE), '#10202c')
    proof.alpha_composite(portal)
    proof.convert('RGB').resize((700, 700), Image.Resampling.LANCZOS).save(
        QA / 'fashion-board-portal-composition.png', optimize=True
    )


if __name__ == '__main__':
    cut()
