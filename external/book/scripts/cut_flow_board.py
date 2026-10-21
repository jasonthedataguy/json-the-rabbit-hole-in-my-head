"""Cut digital Flow artwork from the author's unchanged concept board.

The flattened board is the source of truth. Its enlargements are screen assets,
not separated illustration layers or print-resolution production artwork.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "references/design/model_specification - flow.png"
PORTAL = ROOT / "chapters/flow/artwork/portal"
QA = ROOT / "docs/qa"
SIZE = 1000
MAIN_BOX = (43, 29, 833, 819)


def circle_mask(inner_radius: int = 0) -> Image.Image:
    mask = Image.new("L", (SIZE, SIZE))
    draw = ImageDraw.Draw(mask)
    draw.ellipse((5, 5, 995, 995), fill=255)
    if inner_radius:
        draw.ellipse((500-inner_radius, 500-inner_radius,
                      500+inner_radius, 500+inner_radius), fill=0)
    return mask.filter(ImageFilter.GaussianBlur(1.1))


def cut() -> None:
    board = Image.open(SOURCE).convert("RGB")
    if board.size != (3072, 2048):
        raise ValueError(f"Unexpected Flow board size: {board.size}")

    main = board.crop(MAIN_BOX).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    ring = main.convert("RGBA")
    # Jason stands across the bottom bands, outside the opening. Keep his
    # complete head and body on the turning image; the river remains still.
    ring.putalpha(circle_mask(286))
    scene = main.crop((188, 188, 812, 812)).resize(
        (SIZE, SIZE), Image.Resampling.LANCZOS
    )
    cover_scene = board.crop((227, 219, 650, 642)).resize(
        (SIZE, SIZE), Image.Resampling.LANCZOS
    )

    # The key-elements strip supplies a readable rectangular illustration.
    # Retain every depicted object and remove the board's baked label.
    objects = board.crop((25, 905, 2355, 1326))
    spread = Image.new("RGB", (1600, 480), board.getpixel((2400, 1000)))
    objects.thumbnail((1550, 385), Image.Resampling.LANCZOS)
    spread.paste(objects, ((1600-objects.width)//2, (480-objects.height)//2))

    PORTAL.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    ring.save(PORTAL / "flow-ring-v2.png", optimize=True)
    scene.save(PORTAL / "flow-scene-v2.png", optimize=True)
    cover_scene.save(PORTAL / "flow-cover-scene-v2.png", optimize=True)
    spread.save(PORTAL / "flow-spread-v2.webp", "WEBP", quality=96, method=6)

    portal = Image.new("RGBA", (SIZE, SIZE))
    centre = scene.resize((624, 624), Image.Resampling.LANCZOS).convert("RGBA")
    aperture = Image.new("L", (624, 624))
    ImageDraw.Draw(aperture).ellipse((1, 1, 623, 623), fill=255)
    centre.putalpha(aperture.filter(ImageFilter.GaussianBlur(1.1)))
    portal.alpha_composite(centre, (188, 188))
    portal.alpha_composite(ring)
    portal.save(PORTAL / "flow-portal-v2.png", optimize=True)
    proof = Image.new("RGBA", (SIZE, SIZE), "#102331")
    proof.alpha_composite(portal)
    proof.convert("RGB").resize((700, 700), Image.Resampling.LANCZOS).save(
        QA / "flow-board-portal-composition.png", optimize=True
    )


if __name__ == "__main__":
    cut()
