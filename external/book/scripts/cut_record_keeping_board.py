"""Cut aligned screen artwork from the author's flattened Record Keeping board."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "references/design/model_failure -office-battlefield-masterclass-in-record-keeping.png"
PORTAL = ROOT / "chapters/masterclass-in-record-keeping/artwork/portal"
WEB = ROOT / "chapters/masterclass-in-record-keeping/web/assets"
QA = ROOT / "docs/qa"
MAIN_BOX = (28, 73, 850, 895)
SPREAD_BOX = (22, 962, 2350, 1375)
SIZE = 1000


def cut() -> None:
    board = Image.open(SOURCE).convert("RGB")
    if board.size != (3072, 2048):
        raise ValueError(f"Unexpected Record Keeping board size: {board.size}")
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

    spread = board.crop(SPREAD_BOX)
    ImageDraw.Draw(spread).rectangle((0, 0, 265, 20), fill=spread.getpixel((280, 12)))
    spread = spread.resize((1632, 289), Image.Resampling.LANCZOS)

    ring.save(PORTAL / "record-keeping-ring-v1.png", optimize=True)
    centre.save(PORTAL / "record-keeping-scene-v1.png", optimize=True)
    spread.save(PORTAL / "record-keeping-spread-v1.webp", "WEBP", quality=95, method=6)

    portal = Image.new("RGBA", (SIZE, SIZE))
    aperture = centre.resize((624, 624), Image.Resampling.LANCZOS).convert("RGBA")
    mask = Image.new("L", (624, 624))
    ImageDraw.Draw(mask).ellipse((1, 1, 623, 623), fill=255)
    aperture.putalpha(mask.filter(ImageFilter.GaussianBlur(1.1)))
    portal.alpha_composite(aperture, (188, 188))
    portal.alpha_composite(ring)
    portal.save(PORTAL / "record-keeping-portal-v1.png", optimize=True)
    portal.save(WEB / "record-keeping-portal-v1.png", optimize=True)
    spread.save(WEB / "record-keeping-spread-v1.webp", "WEBP", quality=95, method=6)

    proof = Image.new("RGBA", (SIZE, SIZE), "#112637")
    proof.alpha_composite(portal)
    proof.convert("RGB").resize((700, 700), Image.Resampling.LANCZOS).save(
        QA / "record-keeping-board-portal-composition.png", optimize=True
    )


if __name__ == "__main__":
    cut()
