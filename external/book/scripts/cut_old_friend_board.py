"""Cut Chapter 07 screen artwork from the author's flattened An Old Friend board.

The board is retained unchanged. These enlarged crops are not print masters.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "references/design/data_collection - an old friend.jpg"
PORTAL = ROOT / "chapters/mot-nguoi-ban-cu/artwork/portal"
WEB = ROOT / "chapters/mot-nguoi-ban-cu/web/assets"
QA = ROOT / "docs/qa"
MAIN_BOX = (26, 17, 513, 504)
SIZE = 1000


def cut() -> None:
    board = Image.open(SOURCE).convert("RGB")
    if board.size != (1800, 1200):
        raise ValueError(f"Unexpected An Old Friend board size: {board.size}")
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
    # The complete key-elements strip is a rectangular reading illustration.
    # It retains the candy, friends, game console, school papers and gate
    # rather than stretching the round composition.
    spread = board.crop((15, 540, 1380, 825))
    spread = spread.resize((1638, 342), Image.Resampling.LANCZOS)

    ring.save(PORTAL / "old-friend-ring-v1.png", optimize=True)
    centre.save(PORTAL / "old-friend-scene-v1.png", optimize=True)
    spread.save(PORTAL / "old-friend-spread-v1.webp", "WEBP", quality=95, method=6)

    portal = Image.new("RGBA", (SIZE, SIZE))
    aperture = centre.resize((624, 624), Image.Resampling.LANCZOS).convert("RGBA")
    mask = Image.new("L", (624, 624))
    ImageDraw.Draw(mask).ellipse((1, 1, 623, 623), fill=255)
    aperture.putalpha(mask.filter(ImageFilter.GaussianBlur(1.1)))
    portal.alpha_composite(aperture, (188, 188))
    portal.alpha_composite(ring)
    portal.save(PORTAL / "old-friend-portal-v1.png", optimize=True)
    portal.save(WEB / "old-friend-portal-v1.png", optimize=True)
    spread.save(WEB / "old-friend-spread-v1.webp", "WEBP", quality=95, method=6)

    proof = Image.new("RGBA", (SIZE, SIZE), "#112637")
    proof.alpha_composite(portal)
    proof.convert("RGB").resize((700, 700), Image.Resampling.LANCZOS).save(
        QA / "old-friend-board-portal-composition.png", optimize=True
    )


if __name__ == "__main__":
    cut()
