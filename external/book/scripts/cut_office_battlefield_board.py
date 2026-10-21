"""Cut screen artwork from the author's flattened Office Battlefield board.

The unchanged board remains in references/design/. Re-run this recipe to
recreate the ring, stationary centre, rectangular illustration and proof.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "references/design/model_failure -office-battlefield-the-23-word-nuclear-warhead.jpg"
PORTAL = ROOT / "chapters/the-23-word-nuclear-warhead/artwork/portal"
WEB = ROOT / "chapters/the-23-word-nuclear-warhead/web/assets"
QA = ROOT / "docs/qa"
MAIN_BOX = (26, 48, 490, 512)
SPREAD_BOX = (22, 554, 1386, 827)
SIZE = 1000


def cut() -> None:
    board = Image.open(SOURCE).convert("RGB")
    if board.size != (1800, 1200):
        raise ValueError(f"Unexpected Office Battlefield board size: {board.size}")
    for folder in (PORTAL, WEB, QA):
        folder.mkdir(parents=True, exist_ok=True)

    main = board.crop(MAIN_BOX).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    ring = main.convert("RGBA")
    ring_mask = Image.new("L", (SIZE, SIZE))
    draw = ImageDraw.Draw(ring_mask)
    draw.ellipse((18, 18, 982, 982), fill=255)
    draw.ellipse((188, 188, 812, 812), fill=0)
    ring.putalpha(ring_mask.filter(ImageFilter.GaussianBlur(1.1)))
    centre = main.crop((188, 188, 812, 812)).resize(
        (SIZE, SIZE), Image.Resampling.LANCZOS
    )
    spread = board.crop(SPREAD_BOX).resize((1632, 327), Image.Resampling.LANCZOS)

    ring.save(PORTAL / "office-battlefield-ring-v1.png", optimize=True)
    centre.save(PORTAL / "office-battlefield-scene-v1.png", optimize=True)
    spread.save(PORTAL / "office-battlefield-spread-v1.webp", "WEBP", quality=95, method=6)

    portal = Image.new("RGBA", (SIZE, SIZE))
    aperture = centre.resize((624, 624), Image.Resampling.LANCZOS).convert("RGBA")
    mask = Image.new("L", (624, 624))
    ImageDraw.Draw(mask).ellipse((1, 1, 623, 623), fill=255)
    aperture.putalpha(mask.filter(ImageFilter.GaussianBlur(1.1)))
    portal.alpha_composite(aperture, (188, 188))
    portal.alpha_composite(ring)
    portal.save(PORTAL / "office-battlefield-portal-v1.png", optimize=True)
    portal.save(WEB / "office-battlefield-portal-v1.png", optimize=True)
    spread.save(WEB / "office-battlefield-spread-v1.webp", "WEBP", quality=95, method=6)

    proof = Image.new("RGBA", (SIZE, SIZE), "#112637")
    proof.alpha_composite(portal)
    proof.convert("RGB").resize((700, 700), Image.Resampling.LANCZOS).save(
        QA / "office-battlefield-board-portal-composition.png", optimize=True
    )


if __name__ == "__main__":
    cut()
