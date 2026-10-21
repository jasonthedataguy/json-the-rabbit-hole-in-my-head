"""Cut Chapter 22 screen artwork from the supplied flattened Run away board.

The unchanged source board is retained in references/design. Enlarged crops
are digital assets, not separated print-resolution artwork.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "references/design/relationship_modelling - run away.jpg"
PORTAL = ROOT / "chapters/runaway/artwork/portal"
WEB = ROOT / "chapters/runaway/web/assets"
QA = ROOT / "docs/qa"
MAIN_BOX = (28, 16, 518, 506)
SIZE = 1000


def cut() -> None:
    board = Image.open(SOURCE).convert("RGB")
    if board.size != (1800, 1200):
        raise ValueError(f"Unexpected Run away board size: {board.size}")
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

    # This horizontal strip is the board's individually extracted key elements.
    # It illustrates the reading page without distorting the circular source.
    spread = board.crop((18, 544, 1378, 824))
    spread = spread.resize((1632, 336), Image.Resampling.LANCZOS)

    ring.save(PORTAL / "runaway-ring-v1.png", optimize=True)
    centre.save(PORTAL / "runaway-scene-v1.png", optimize=True)
    spread.save(PORTAL / "runaway-spread-v1.webp", "WEBP", quality=95, method=6)

    portal = Image.new("RGBA", (SIZE, SIZE))
    aperture = centre.resize((624, 624), Image.Resampling.LANCZOS).convert("RGBA")
    mask = Image.new("L", (624, 624))
    ImageDraw.Draw(mask).ellipse((1, 1, 623, 623), fill=255)
    aperture.putalpha(mask.filter(ImageFilter.GaussianBlur(1.1)))
    portal.alpha_composite(aperture, (188, 188))
    portal.alpha_composite(ring)
    portal.save(PORTAL / "runaway-portal-v1.png", optimize=True)
    portal.save(WEB / "runaway-portal-v1.png", optimize=True)
    spread.save(WEB / "runaway-spread-v1.webp", "WEBP", quality=95, method=6)

    proof = Image.new("RGBA", (SIZE, SIZE), "#112637")
    proof.alpha_composite(portal)
    proof.convert("RGB").resize((700, 700), Image.Resampling.LANCZOS).save(
        QA / "runaway-board-portal-composition.png", optimize=True
    )


if __name__ == "__main__":
    cut()
