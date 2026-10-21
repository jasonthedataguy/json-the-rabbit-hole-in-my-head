"""Cut screen artwork for Three Meeting Theory from the author's concept board.

The unchanged board lives in references/design. These 386-pixel source crops
are for the digital book, not separated or print-resolution production art.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'references/design/relationshio_modelling - three meeting theory.png'
PORTAL = ROOT / 'chapters/three-meeting-theory/artwork/portal'
WEB_ASSETS = ROOT / 'chapters/three-meeting-theory/web/assets'
QA = ROOT / 'docs/qa'
SIZE = 1000
MAIN_BOX = (18, 27, 406, 415)


def cut():
    board = Image.open(SOURCE).convert('RGB')
    if board.size != (1448, 1086):
        raise ValueError(f'Unexpected Three Meeting Theory board size: {board.size}')

    circle = board.crop(MAIN_BOX).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    ring = circle.convert('RGBA')
    mask = Image.new('L', (SIZE, SIZE))
    draw = ImageDraw.Draw(mask)
    draw.ellipse((5, 5, 995, 995), fill=255)
    # The board supplies a complete circular composition, not an empty river
    # layer behind the figures. Keep its collage, skyline and couple intact on
    # one turning sheet instead of fabricating a background inside a cutout.
    ring.putalpha(mask.filter(ImageFilter.GaussianBlur(1.15)))

    # Retain an aligned centre derivative for reuse in the homepage/artwork
    # library. The chapter portal shows the intact circle above this picture.
    aperture_size = round((MAIN_BOX[2] - MAIN_BOX[0]) * 624 / SIZE)
    centre_x = (MAIN_BOX[0] + MAIN_BOX[2]) // 2
    centre_y = (MAIN_BOX[1] + MAIN_BOX[3]) // 2
    scene_box = (centre_x - aperture_size // 2, centre_y - aperture_size // 2,
                 centre_x + aperture_size // 2, centre_y + aperture_size // 2)
    scene_source = board.crop(scene_box)
    scene = scene_source.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    # The shared homepage cover ring has no chapter-specific foreground.
    # Keep the board's complete meeting pair in that stop's centre picture.
    cover_scene = board.crop((100, 180, 330, 410)).resize((SIZE, SIZE), Image.Resampling.LANCZOS)

    # A full rectangular reading illustration. Keep the author-provided
    # couple, cafe, bridge and skyline in view, with paper-coloured margins.
    panorama = board.crop((13, 475, 812, 653))
    spread = Image.new('RGB', (1600, 600), board.getpixel((1100, 460)))
    panorama = panorama.resize((1550, 345), Image.Resampling.LANCZOS)
    spread.paste(panorama, (25, 128))

    PORTAL.mkdir(parents=True, exist_ok=True)
    WEB_ASSETS.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    ring.save(PORTAL / 'three-meeting-ring-v2.png', optimize=True)
    scene.save(PORTAL / 'three-meeting-scene-v2.png', optimize=True)
    cover_scene.save(PORTAL / 'three-meeting-cover-scene-v2.png', optimize=True)
    spread.save(PORTAL / 'three-meeting-spread-v2.webp', 'WEBP', quality=96, method=6)

    portal = Image.new('RGBA', (SIZE, SIZE))
    slot = scene.resize((624, 624), Image.Resampling.LANCZOS).convert('RGBA')
    slot_mask = Image.new('L', (624, 624))
    ImageDraw.Draw(slot_mask).ellipse((1, 1, 623, 623), fill=255)
    slot.putalpha(slot_mask.filter(ImageFilter.GaussianBlur(1.1)))
    portal.alpha_composite(slot, (188, 188))
    portal.alpha_composite(ring)
    portal.save(PORTAL / 'three-meeting-portal-v2.png', optimize=True)
    portal.save(WEB_ASSETS / 'three-meeting-portal-v2.png', optimize=True)
    spread.save(WEB_ASSETS / 'three-meeting-spread-v2.webp', 'WEBP', quality=96, method=6)

    proof = Image.new('RGBA', (SIZE, SIZE), '#102331')
    proof.alpha_composite(portal)
    proof.convert('RGB').resize((700, 700), Image.Resampling.LANCZOS).save(
        QA / 'three-meeting-board-portal-composition.png', optimize=True
    )


if __name__ == '__main__':
    cut()
