"""Make screen artwork for Dating Algorithm from the author's concept board.

The reference is a flattened 1448 x 1086 board. These are reproducible screen
crops and masks, not separately illustrated layers or print-resolution art.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'references/design/relationship_modelling - dating algorithm.png'
PORTAL = ROOT / 'chapters/dating-algorithm/artwork/portal'
WEB_ASSETS = ROOT / 'chapters/dating-algorithm/web/assets'
QA = ROOT / 'docs/qa'
SIZE = 1000
MAIN_BOX = (29, 136, 486, 593)


def cut() -> None:
    board = Image.open(SOURCE).convert('RGB')
    if board.size != (1448, 1086):
        raise ValueError(f'Unexpected Dating Algorithm board size: {board.size}')

    # One coordinate system keeps the rotating collage aligned to the still
    # dinner scene. Both figures and their table remain wholly in the opening.
    circle = board.crop(MAIN_BOX).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    ring = circle.convert('RGBA')
    ring_mask = Image.new('L', (SIZE, SIZE))
    draw = ImageDraw.Draw(ring_mask)
    draw.ellipse((5, 5, 995, 995), fill=255)
    draw.ellipse((286, 286, 714, 714), fill=0)
    ring.putalpha(ring_mask.filter(ImageFilter.GaussianBlur(1.1)))

    # The portal runtime places its picture in a 624 px central slot. Crop
    # those exact source coordinates, then rescale, so the paper edges join
    # seamlessly when the ring is at its resting angle.
    scene = circle.crop((188, 188, 812, 812)).resize(
        (SIZE, SIZE), Image.Resampling.LANCZOS
    )
    # The homepage keeps its common cover ring. Frame the full date inside
    # its centre, so neither person is clipped by the shared aperture.
    cover_scene = board.crop((121, 232, 394, 505)).resize(
        (SIZE, SIZE), Image.Resampling.LANCZOS
    )

    # Board's extracted date/profile/compatibility objects form the reading
    # page's rectangular illustration. Omit the board's tiny baked labels;
    # a readable caption belongs to the HTML page instead.
    objects = board.crop((902, 552, 1438, 656))
    spread = Image.new('RGB', (1600, 600), board.getpixel((1110, 500)))
    objects = objects.resize((1530, 297), Image.Resampling.LANCZOS)
    spread.paste(objects, (35, 151))

    PORTAL.mkdir(parents=True, exist_ok=True)
    WEB_ASSETS.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    ring.save(PORTAL / 'dating-algorithm-ring-v2.png', optimize=True)
    scene.save(PORTAL / 'dating-algorithm-scene-v2.png', optimize=True)
    cover_scene.save(PORTAL / 'dating-algorithm-cover-scene-v2.png', optimize=True)
    spread.save(PORTAL / 'dating-algorithm-spread-v2.webp', 'WEBP', quality=96, method=6)

    portal = Image.new('RGBA', (SIZE, SIZE))
    centre = scene.resize((624, 624), Image.Resampling.LANCZOS).convert('RGBA')
    centre_mask = Image.new('L', (624, 624))
    ImageDraw.Draw(centre_mask).ellipse((1, 1, 623, 623), fill=255)
    centre.putalpha(centre_mask.filter(ImageFilter.GaussianBlur(1.1)))
    portal.alpha_composite(centre, (188, 188))
    portal.alpha_composite(ring)
    portal.save(PORTAL / 'dating-algorithm-portal-v2.png', optimize=True)
    portal.save(WEB_ASSETS / 'dating-algorithm-portal-v2.png', optimize=True)
    spread.save(WEB_ASSETS / 'dating-algorithm-spread-v2.webp', 'WEBP', quality=96, method=6)

    proof = Image.new('RGBA', (SIZE, SIZE), '#132334')
    proof.alpha_composite(portal)
    proof.convert('RGB').resize((700, 700), Image.Resampling.LANCZOS).save(
        QA / 'dating-algorithm-board-portal-composition.png', optimize=True
    )


if __name__ == '__main__':
    cut()
