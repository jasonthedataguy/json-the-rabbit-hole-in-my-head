"""Cut the new Introduction board into matching digital ring and scene assets.

The supplied board remains unchanged. The chapter-page scene uses the exact
pixels beneath the ring, while the cover-stop scene focuses on the same city.
These are digital crops, not printer-resolution masters.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'references/design/Introduction Portal Ring Concept Board.png'
PORTAL = ROOT / 'shared/artwork/portal'
SIZE = 1000


def cut():
    board = Image.open(SOURCE).convert('RGBA')
    if board.size != (1672, 941):
        raise ValueError(f'Unexpected Introduction artboard size: {board.size}')

    main = board.crop((18, 55, 718, 745)).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    leaf_scene = main.crop((188, 188, 812, 812)).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    cover_scene = main.crop((292, 299, 708, 715)).resize((SIZE, SIZE), Image.Resampling.LANCZOS)

    ring = main.copy()
    mask = Image.new('L', (SIZE, SIZE))
    draw = ImageDraw.Draw(mask)
    draw.ellipse((12, 10, 988, 985), fill=255)
    draw.ellipse((294, 303, 707, 725), fill=0)
    ring.putalpha(mask.filter(ImageFilter.GaussianBlur(1.2)))

    PORTAL.mkdir(parents=True, exist_ok=True)
    ring.save(PORTAL / 'introduction-ring-v2.png', optimize=True)
    leaf_scene.save(PORTAL / 'introduction-scene-v2.png', optimize=True)
    cover_scene.save(PORTAL / 'introduction-cover-scene-v2.png', optimize=True)

    # The Introduction page is a stationary illustration. Export one transparent
    # circular composition so its aperture can never appear as a square image.
    portal = Image.new('RGBA', (SIZE, SIZE))
    slot = leaf_scene.resize((624, 624), Image.Resampling.LANCZOS)
    slot_mask = Image.new('L', slot.size)
    ImageDraw.Draw(slot_mask).ellipse((1, 1, 623, 623), fill=255)
    slot.putalpha(slot_mask.filter(ImageFilter.GaussianBlur(1.2)))
    portal.alpha_composite(slot, (188, 188))
    portal.alpha_composite(ring)
    portal.save(PORTAL / 'introduction-portal-v2.png', optimize=True)

    qa = ROOT / 'docs/qa'
    qa.mkdir(parents=True, exist_ok=True)
    for name, picture, frame in (
        ('introduction-concept-leaf-composition.png', leaf_scene, ring),
        ('introduction-concept-cover-stop-composition.png', cover_scene,
         Image.open(PORTAL / 'board-cover-ring.png').convert('RGBA')),
    ):
        proof = Image.new('RGBA', (SIZE, SIZE), '#efe1c7')
        if name == 'introduction-concept-leaf-composition.png':
            proof.alpha_composite(portal)
        else:
            proof.alpha_composite(picture.resize((624, 624), Image.Resampling.LANCZOS), (188, 188))
            proof.alpha_composite(frame)
        proof.convert('RGB').resize((700, 700), Image.Resampling.LANCZOS).save(qa / name, optimize=True)


if __name__ == '__main__':
    cut()
