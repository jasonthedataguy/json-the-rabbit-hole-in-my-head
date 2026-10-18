"""Cut screen artwork from the author's revised Expected Utility concept board.

The flattened board is preserved in references/design. These crops are digital
derivatives, not separated print masters. The earlier v2 board/assets remain.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "references/design/model_specification - expected utility.png"
PORTAL = ROOT / "chapters/expected-utility/artwork/portal"
WEB = ROOT / "chapters/expected-utility/web/assets"
QA = ROOT / "docs/qa"
SIZE = 1000
MAIN_BOX = (25, 25, 865, 865)


def circle_mask(radius: int) -> Image.Image:
    mask = Image.new("L", (SIZE, SIZE))
    draw = ImageDraw.Draw(mask)
    draw.ellipse((500-radius, 500-radius, 500+radius, 500+radius), fill=255)
    return mask


def cut() -> None:
    board = Image.open(SOURCE).convert("RGB")
    if board.size != (3072, 2048):
        raise ValueError(f"Unexpected Expected Utility board size: {board.size}")

    main = board.crop(MAIN_BOX).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    ring = main.convert("RGBA")
    mask = circle_mask(484)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((188, 188, 812, 812), fill=0)
    # Jason crosses the aperture. Keep his head and body on the rotating art
    # with a narrow feathered silhouette instead of cutting him at the neck.
    draw.polygon([
        (482, 665), (516, 665), (539, 683), (550, 719),
        (563, 742), (573, 817), (578, 961), (421, 961),
        (426, 817), (436, 742), (449, 719), (460, 683),
    ], fill=255)
    ring.putalpha(mask.filter(ImageFilter.GaussianBlur(1.2)))

    scene = main.crop((188, 188, 812, 812)).resize(
        (SIZE, SIZE), Image.Resampling.LANCZOS
    )
    # The common book-cover ring already contains Jason, so its centre shows
    # only the woman's face from the same illustrated scene.
    cover_scene = board.crop((275, 241, 630, 580)).resize(
        (SIZE, SIZE), Image.Resampling.LANCZOS
    )

    gaze = board.crop((75, 235, 835, 555)).resize(
        (1600, 674), Image.Resampling.LANCZOS
    )

    objects = board.crop((26, 886, 2335, 1366))
    spread = Image.new("RGB", (1600, 520), board.getpixel((2450, 1110)))
    objects.thumbnail((1550, 450), Image.Resampling.LANCZOS)
    spread.paste(objects, ((1600-objects.width)//2, (520-objects.height)//2))

    PORTAL.mkdir(parents=True, exist_ok=True)
    WEB.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    ring.save(PORTAL / "expected-utility-ring-v3.png", optimize=True)
    scene.save(PORTAL / "expected-utility-scene-v3.png", optimize=True)
    cover_scene.save(PORTAL / "expected-utility-cover-scene-v3.png", optimize=True)
    gaze.save(PORTAL / "expected-utility-gaze-v3.webp", "WEBP", quality=96, method=6)
    spread.save(PORTAL / "expected-utility-spread-v3.webp", "WEBP", quality=96, method=6)

    portal = Image.new("RGBA", (SIZE, SIZE))
    centre = scene.resize((624, 624), Image.Resampling.LANCZOS).convert("RGBA")
    aperture = Image.new("L", (624, 624))
    ImageDraw.Draw(aperture).ellipse((1, 1, 623, 623), fill=255)
    centre.putalpha(aperture.filter(ImageFilter.GaussianBlur(1.2)))
    portal.alpha_composite(centre, (188, 188))
    portal.alpha_composite(ring)
    portal.save(PORTAL / "expected-utility-portal-v3.png", optimize=True)
    portal.save(WEB / "expected-utility-portal-v3.png", optimize=True)
    gaze.save(WEB / "expected-utility-gaze-v3.webp", "WEBP", quality=96, method=6)
    spread.save(WEB / "expected-utility-spread-v3.webp", "WEBP", quality=96, method=6)

    proof = Image.new("RGBA", (SIZE, SIZE), "#102331")
    proof.alpha_composite(portal)
    proof.convert("RGB").resize((700, 700), Image.Resampling.LANCZOS).save(
        QA / "expected-utility-v3-portal-composition.png", optimize=True
    )


if __name__ == "__main__":
    cut()
