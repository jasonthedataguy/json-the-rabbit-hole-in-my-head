"""Cut screen assets for Dating 102 from the author's flattened concept board.

The board remains the source of truth. These are aligned digital crops, not
separate illustrated layers or print-resolution production assets.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'references/design/relationshio_modelling - dating 102.png'
PORTAL = ROOT / 'chapters/dating-102/artwork/portal'
WEB = ROOT / 'chapters/dating-102/web/assets'
QA = ROOT / 'docs/qa'
SIZE = 1000


def cut() -> None:
    board = Image.open(SOURCE).convert('RGB')
    if board.size != (1448, 1086):
        raise ValueError(f'Unexpected Dating 102 board size: {board.size}')

    circle = board.crop((17, 112, 428, 523)).resize(
        (SIZE, SIZE), Image.Resampling.LANCZOS
    )
    ring = circle.convert('RGBA')
    mask = Image.new('L', (SIZE, SIZE))
    draw = ImageDraw.Draw(mask)
    draw.ellipse((5, 5, 995, 995), fill=255)
    draw.ellipse((286, 286, 714, 714), fill=0)
    ring.putalpha(mask.filter(ImageFilter.GaussianBlur(1.1)))

    # The portal's picture occupies a 624 px circle; crop the matching source
    # pixels so its arch, window and shared sketch meet the revolving layers.
    scene = circle.crop((188, 188, 812, 812)).resize(
        (SIZE, SIZE), Image.Resampling.LANCZOS
    )
    # The homepage uses the common book ring, with both readers in its centre.
    cover_scene = board.crop((108, 210, 336, 438)).resize(
        (SIZE, SIZE), Image.Resampling.LANCZOS
    )
    # A complete rectangular vignette is provided separately on the board.
    # Preserve its full edges and aspect ratio for the reading-page spread.
    spread = board.crop((17, 563, 331, 713)).resize(
        (1600, 764), Image.Resampling.LANCZOS
    )

    PORTAL.mkdir(parents=True, exist_ok=True)
    WEB.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    ring.save(PORTAL / 'dating-102-ring-v2.png', optimize=True)
    scene.save(PORTAL / 'dating-102-scene-v2.png', optimize=True)
    cover_scene.save(PORTAL / 'dating-102-cover-scene-v2.png', optimize=True)
    spread.save(PORTAL / 'dating-102-spread-v2.webp', 'WEBP', quality=96, method=6)

    portal = Image.new('RGBA', (SIZE, SIZE))
    centre = scene.resize((624, 624), Image.Resampling.LANCZOS).convert('RGBA')
    centre_mask = Image.new('L', (624, 624))
    ImageDraw.Draw(centre_mask).ellipse((1, 1, 623, 623), fill=255)
    centre.putalpha(centre_mask.filter(ImageFilter.GaussianBlur(1.1)))
    portal.alpha_composite(centre, (188, 188))
    portal.alpha_composite(ring)
    portal.save(PORTAL / 'dating-102-portal-v2.png', optimize=True)
    portal.save(WEB / 'dating-102-portal-v2.png', optimize=True)
    spread.save(WEB / 'dating-102-spread-v2.webp', 'WEBP', quality=96, method=6)

    proof = Image.new('RGBA', (SIZE, SIZE), '#112635')
    proof.alpha_composite(portal)
    proof.convert('RGB').resize((700, 700), Image.Resampling.LANCZOS).save(
        QA / 'dating-102-board-portal-composition.png', optimize=True
    )


if __name__ == '__main__':
    cut()
