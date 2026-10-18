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
    draw.ellipse((248, 248, 752, 752), fill=0)

    # The pair lean into the aperture. Keep both entire people on the rotating
    # sheet rather than slicing their heads away from their bodies.
    pair_outline = [
        (157, 274), (163, 265), (178, 259), (191, 262), (201, 274),
        (205, 286), (210, 279), (212, 266), (221, 256), (233, 257),
        (243, 266), (244, 280), (239, 290), (251, 300), (262, 323),
        (262, 372), (256, 392), (246, 404), (225, 405), (214, 389),
        (205, 392), (191, 403), (171, 401), (160, 391), (157, 365),
        (147, 344), (151, 320), (147, 301), (151, 287),
    ]
    scale = SIZE / (MAIN_BOX[2] - MAIN_BOX[0])
    draw.polygon([((x - MAIN_BOX[0]) * scale, (y - MAIN_BOX[1]) * scale)
                  for x, y in pair_outline], fill=255)
    ring.putalpha(mask.filter(ImageFilter.GaussianBlur(1.15)))

    # Match the aperture's field of view in the 388 px source circle. Its
    # 624/1000 diameter is 242 source pixels, centred on the same point as
    # MAIN_BOX. The old 150 px crop enlarged the bridge and broke the seam.
    # Remove the foreground pair from this stationary layer; their complete
    # silhouettes remain on the rotating ring above it.
    aperture_size = round((MAIN_BOX[2] - MAIN_BOX[0]) * 624 / SIZE)
    centre_x = (MAIN_BOX[0] + MAIN_BOX[2]) // 2
    centre_y = (MAIN_BOX[1] + MAIN_BOX[3]) // 2
    scene_box = (centre_x - aperture_size // 2, centre_y - aperture_size // 2,
                 centre_x + aperture_size // 2, centre_y + aperture_size // 2)
    scene_source = board.crop(scene_box)
    people_mask = Image.new('L', scene_source.size)
    ImageDraw.Draw(people_mask).polygon([(x - scene_box[0], y - scene_box[1])
                                         for x, y in pair_outline], fill=255)
    people_mask = people_mask.filter(ImageFilter.MaxFilter(5))
    for y in range(scene_source.height):
        occupied = [x for x in range(scene_source.width) if people_mask.getpixel((x, y))]
        if not occupied:
            continue
        left, right = occupied[0], occupied[-1]
        left_colour = scene_source.getpixel((max(0, left - 3), y))
        right_colour = scene_source.getpixel((min(scene_source.width - 1, right + 3), y))
        for x in occupied:
            blend = (x - left) / max(1, right - left)
            scene_source.putpixel((x, y), tuple(round(a * (1 - blend) + b * blend)
                                                 for a, b in zip(left_colour, right_colour)))
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
