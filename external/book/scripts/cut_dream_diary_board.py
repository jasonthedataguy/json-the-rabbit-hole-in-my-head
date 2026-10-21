"""Cut aligned screen art from the author's flattened Dream Diary board."""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "references/design/data_collection - dream-diary.png"
PORTAL = ROOT / "chapters/nhung-thu-khong-duoc-luu-lai/artwork/portal"
WEB = ROOT / "chapters/nhung-thu-khong-duoc-luu-lai/web/assets"
QA = ROOT / "docs/qa"
MAIN_BOX = (50, 22, 900, 966)
SPREAD_BOX = (22, 968, 2305, 1400)
SIZE = 1000


def cut() -> None:
    board = Image.open(SOURCE).convert("RGB")
    if board.size != (3072, 2048):
        raise ValueError(f"Unexpected Dream Diary board size: {board.size}")
    for folder in (PORTAL, WEB, QA):
        folder.mkdir(parents=True, exist_ok=True)

    main = board.crop(MAIN_BOX).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    ring = main.convert("RGBA")
    ring_mask = Image.new("L", (SIZE, SIZE))
    draw = ImageDraw.Draw(ring_mask)
    draw.ellipse((18, 18, 982, 982), fill=255)
    draw.ellipse((188, 188, 812, 812), fill=0)
    # The board's main artwork is slightly oval. Remove the connected paper
    # surrounding its actual edge so it cannot rotate as a pale wedge.
    background = main.copy()
    for point in ((0, 0), (999, 0), (0, 999), (999, 999), (999, 800), (900, 999)):
        ImageDraw.floodfill(background, point, (255, 0, 255), thresh=40)
    artwork_mask = Image.new("L", (SIZE, SIZE))
    artwork_mask.putdata([0 if pixel == (255, 0, 255) else 255 for pixel in background.getdata()])
    ring.putalpha(ImageChops.multiply(ring_mask, artwork_mask).filter(ImageFilter.GaussianBlur(1.1)))
    centre = main.crop((188, 188, 812, 812)).resize(
        (SIZE, SIZE), Image.Resampling.LANCZOS
    )

    spread = board.crop(SPREAD_BOX)
    ImageDraw.Draw(spread).rectangle((0, 0, 265, 20), fill=spread.getpixel((280, 12)))
    spread = spread.resize((1632, 289), Image.Resampling.LANCZOS)

    ring.save(PORTAL / "dream-diary-ring-v1.png", optimize=True)
    centre.save(PORTAL / "dream-diary-scene-v1.png", optimize=True)
    spread.save(PORTAL / "dream-diary-spread-v1.webp", "WEBP", quality=95, method=6)

    portal = Image.new("RGBA", (SIZE, SIZE))
    aperture = centre.resize((624, 624), Image.Resampling.LANCZOS).convert("RGBA")
    mask = Image.new("L", (624, 624))
    ImageDraw.Draw(mask).ellipse((1, 1, 623, 623), fill=255)
    aperture.putalpha(mask.filter(ImageFilter.GaussianBlur(1.1)))
    portal.alpha_composite(aperture, (188, 188))
    portal.alpha_composite(ring)
    portal.save(PORTAL / "dream-diary-portal-v1.png", optimize=True)
    portal.save(WEB / "dream-diary-portal-v1.png", optimize=True)
    spread.save(WEB / "dream-diary-spread-v1.webp", "WEBP", quality=95, method=6)

    proof = Image.new("RGBA", (SIZE, SIZE), "#112637")
    proof.alpha_composite(portal)
    proof.convert("RGB").resize((700, 700), Image.Resampling.LANCZOS).save(
        QA / "dream-diary-board-portal-composition.png", optimize=True
    )


if __name__ == "__main__":
    cut()
