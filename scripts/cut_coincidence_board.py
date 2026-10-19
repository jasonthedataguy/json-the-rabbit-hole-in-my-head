"""Cut digital Chapter 11 artwork from the author's flattened concept board.

The original board is retained unchanged in references/design. These are
screen crops, not separated print layers.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "references/design/data_collection - coincidence.png"
PORTAL = ROOT / "chapters/nhung-su-trung-hop/artwork/portal"
WEB = ROOT / "chapters/nhung-su-trung-hop/web/assets"
QA = ROOT / "docs/qa"
MAIN_BOX = (28, 17, 865, 854)
SIZE = 1000


def cut() -> None:
    board = Image.open(SOURCE).convert("RGB")
    if board.size != (3072, 2048):
        raise ValueError(f"Unexpected Coincidence board size: {board.size}")
    for folder in (PORTAL, WEB, QA):
        folder.mkdir(parents=True, exist_ok=True)

    main = board.crop(MAIN_BOX).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    ring = main.convert("RGBA")
    ring_mask = Image.new("L", (SIZE, SIZE))
    draw = ImageDraw.Draw(ring_mask)
    draw.ellipse((18, 18, 982, 982), fill=255)
    draw.ellipse((188, 188, 812, 812), fill=0)
    ring.putalpha(ring_mask.filter(ImageFilter.GaussianBlur(1.1)))

    scene = main.crop((188, 188, 812, 812)).resize(
        (SIZE, SIZE), Image.Resampling.LANCZOS
    )
    # Preserve the earlier close bookstore alternate. The active homepage
    # uses scene, showing the nested paths as well as the bookshop.
    cover_scene = board.crop((282, 170, 625, 510)).resize(
        (SIZE, SIZE), Image.Resampling.LANCZOS
    )
    spread = board.crop((165, 175, 725, 590)).resize(
        (1600, 1186), Image.Resampling.LANCZOS
    )
    elements = board.crop((12, 880, 2325, 1365))
    elements.thumbnail((1550, 490), Image.Resampling.LANCZOS)
    element_sheet = Image.new("RGB", (1600, 530), board.getpixel((2470, 1110)))
    element_sheet.paste(
        elements, ((1600-elements.width)//2, (530-elements.height)//2)
    )

    ring.save(PORTAL / "coincidence-ring-v1.png", optimize=True)
    scene.save(PORTAL / "coincidence-scene-v1.png", optimize=True)
    cover_scene.save(PORTAL / "coincidence-cover-scene-v1.png", optimize=True)
    spread.save(PORTAL / "coincidence-spread-v1.webp", "WEBP", quality=95, method=6)
    element_sheet.save(PORTAL / "coincidence-elements-v1.webp", "WEBP", quality=95, method=6)

    portal = Image.new("RGBA", (SIZE, SIZE))
    centre = scene.resize((624, 624), Image.Resampling.LANCZOS).convert("RGBA")
    aperture = Image.new("L", (624, 624))
    ImageDraw.Draw(aperture).ellipse((1, 1, 623, 623), fill=255)
    centre.putalpha(aperture.filter(ImageFilter.GaussianBlur(1.1)))
    portal.alpha_composite(centre, (188, 188))
    portal.alpha_composite(ring)
    portal.save(PORTAL / "coincidence-portal-v1.png", optimize=True)
    portal.save(WEB / "coincidence-portal-v1.png", optimize=True)
    spread.save(WEB / "coincidence-spread-v1.webp", "WEBP", quality=95, method=6)
    element_sheet.save(WEB / "coincidence-elements-v1.webp", "WEBP", quality=95, method=6)

    proof = Image.new("RGBA", (SIZE, SIZE), "#112637")
    proof.alpha_composite(portal)
    proof.convert("RGB").resize((700, 700), Image.Resampling.LANCZOS).save(
        QA / "coincidence-board-portal-composition.png", optimize=True
    )


if __name__ == "__main__":
    cut()
