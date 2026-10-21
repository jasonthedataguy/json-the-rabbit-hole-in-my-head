"""Cut screen artwork for Chapter 09 from the author's Dream World board.

The flattened design board stays unchanged in references/design. These crops
are for the digital book and interactive essay, not print-resolution layers.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "references/design/data colletion - dream world.png"
PORTAL = ROOT / "chapters/the-gioi-trong-mo-cua-toi/artwork/portal"
WEB = ROOT / "chapters/the-gioi-trong-mo-cua-toi/web/assets"
QA = ROOT / "docs/qa"
SIZE = 1000
MAIN_BOX = (20, 24, 860, 864)


def circle_mask(inner_radius: int = 0) -> Image.Image:
    mask = Image.new("L", (SIZE, SIZE))
    draw = ImageDraw.Draw(mask)
    draw.ellipse((5, 5, 995, 995), fill=255)
    if inner_radius:
        draw.ellipse((500-inner_radius, 500-inner_radius,
                      500+inner_radius, 500+inner_radius), fill=0)
    return mask.filter(ImageFilter.GaussianBlur(1.1))


def framed_crop(image: Image.Image, box: tuple[int, int, int, int], size=(1200, 750)) -> Image.Image:
    """Preserve the source crop's full content inside a shared navy frame."""
    source = image.crop(box)
    scale = min((size[0]-42)/source.width, (size[1]-42)/source.height)
    source = source.resize((round(source.width*scale), round(source.height*scale)),
                           Image.Resampling.LANCZOS)
    result = Image.new("RGB", size, "#102433")
    result.paste(source, ((size[0]-source.width)//2, (size[1]-source.height)//2))
    return result


def cut() -> None:
    board = Image.open(SOURCE).convert("RGB")
    if board.size != (3072, 2048):
        raise ValueError(f"Unexpected Dream World board size: {board.size}")

    main = board.crop(MAIN_BOX).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    ring = main.convert("RGBA")
    # Jason's head reaches inside the usual aperture. A smaller hole keeps
    # head, body and suitcases together on the rotating layer.
    ring.putalpha(circle_mask(238))
    scene = main.crop((188, 188, 812, 812)).resize(
        (SIZE, SIZE), Image.Resampling.LANCZOS
    )
    # Keep the imagined family visible beneath the constant homepage book ring,
    # without introducing a second Jason in its stationary centre.
    cover_scene = board.crop((286, 370, 560, 644)).resize(
        (SIZE, SIZE), Image.Resampling.LANCZOS
    )

    objects = board.crop((25, 917, 2355, 1365))
    spread = Image.new("RGB", (1600, 520), board.getpixel((2400, 1070)))
    objects.thumbnail((1550, 430), Image.Resampling.LANCZOS)
    spread.paste(objects, ((1600-objects.width)//2, (520-objects.height)//2))

    PORTAL.mkdir(parents=True, exist_ok=True)
    WEB.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    ring.save(PORTAL / "dream-world-ring-v2.png", optimize=True)
    scene.save(PORTAL / "dream-world-scene-v2.png", optimize=True)
    cover_scene.save(PORTAL / "dream-world-cover-scene-v2.png", optimize=True)
    spread.save(PORTAL / "dream-world-spread-v2.webp", "WEBP", quality=96, method=6)

    portal = Image.new("RGBA", (SIZE, SIZE))
    centre = scene.resize((624, 624), Image.Resampling.LANCZOS).convert("RGBA")
    aperture = Image.new("L", (624, 624))
    ImageDraw.Draw(aperture).ellipse((1, 1, 623, 623), fill=255)
    centre.putalpha(aperture.filter(ImageFilter.GaussianBlur(1.1)))
    portal.alpha_composite(centre, (188, 188))
    portal.alpha_composite(ring)
    portal.save(PORTAL / "dream-world-portal-v2.png", optimize=True)
    portal.save(WEB / "dream-world-portal-v2.png", optimize=True)
    spread.save(WEB / "dream-world-spread-v2.webp", "WEBP", quality=96, method=6)
    framed_crop(board, (104, 74, 772, 442)).save(
        WEB / "dream-world-observed-v2.webp", "WEBP", quality=95, method=6)
    framed_crop(board, (273, 375, 628, 668)).save(
        WEB / "dream-world-imagined-v2.webp", "WEBP", quality=95, method=6)
    framed_crop(board, (195, 305, 690, 650)).save(
        WEB / "dream-world-afterimage-v2.webp", "WEBP", quality=95, method=6)

    proof = Image.new("RGBA", (SIZE, SIZE), "#102433")
    proof.alpha_composite(portal)
    proof.convert("RGB").resize((700, 700), Image.Resampling.LANCZOS).save(
        QA / "dream-world-board-portal-composition.png", optimize=True)


if __name__ == "__main__":
    cut()
