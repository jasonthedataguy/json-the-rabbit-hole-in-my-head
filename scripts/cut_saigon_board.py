"""Cut the digital To My Saigon portal from the author's flattened board.

The unchanged source stays in references/design. These are screen crops, not
independent print layers; older chapter art and product proofs remain intact.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "references/design/data_collection - to my saigon (2).png"
PORTAL = ROOT / "chapters/viet-cho-sai-gon-cua-t/artwork/portal"
WEB = ROOT / "chapters/viet-cho-sai-gon-cua-t/web/assets"
QA = ROOT / "docs/qa"
MAIN_BOX = (28, 18, 865, 855)
SIZE = 1000


def save_webp(image: Image.Image, path: Path) -> None:
    image.save(path, "WEBP", quality=95, method=6)


def cut() -> None:
    board = Image.open(SOURCE).convert("RGB")
    if board.size != (3072, 2048):
        raise ValueError(f"Unexpected Saigon board size: {board.size}")
    PORTAL.mkdir(parents=True, exist_ok=True)
    WEB.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)

    main = board.crop(MAIN_BOX).resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    ring = main.convert("RGBA")
    mask = Image.new("L", (SIZE, SIZE))
    draw = ImageDraw.Draw(mask)
    draw.ellipse((16, 16, 984, 984), fill=255)
    draw.ellipse((188, 188, 812, 812), fill=0)
    ring.putalpha(mask.filter(ImageFilter.GaussianBlur(1.1)))
    scene = main.crop((188, 188, 812, 812)).resize(
        (SIZE, SIZE), Image.Resampling.LANCZOS
    )
    # The shared cover ring already carries Jason. Keep his second appearance
    # out of this preview and foreground Ba Son Bridge and the skyline.
    cover_scene = board.crop((295, 280, 655, 540)).resize(
        (SIZE, SIZE), Image.Resampling.LANCZOS
    )
    spread = board.crop((120, 235, 770, 695)).resize(
        (1600, 1132), Image.Resampling.LANCZOS
    )
    elements = board.crop((25, 910, 2325, 1385))
    elements.thumbnail((1560, 470), Image.Resampling.LANCZOS)
    element_sheet = Image.new("RGB", (1600, 520), board.getpixel((2460, 1110)))
    element_sheet.paste(
        elements, ((1600-elements.width)//2, (520-elements.height)//2)
    )

    ring.save(PORTAL / "saigon-ring-v1.png", optimize=True)
    scene.save(PORTAL / "saigon-scene-v1.png", optimize=True)
    cover_scene.save(PORTAL / "saigon-cover-scene-v1.png", optimize=True)
    save_webp(spread, PORTAL / "saigon-spread-v1.webp")
    save_webp(element_sheet, PORTAL / "saigon-elements-v1.webp")

    portal = Image.new("RGBA", (SIZE, SIZE))
    centre = scene.resize((624, 624), Image.Resampling.LANCZOS).convert("RGBA")
    aperture = Image.new("L", (624, 624))
    ImageDraw.Draw(aperture).ellipse((1, 1, 623, 623), fill=255)
    centre.putalpha(aperture.filter(ImageFilter.GaussianBlur(1.1)))
    portal.alpha_composite(centre, (188, 188))
    portal.alpha_composite(ring)
    portal.save(PORTAL / "saigon-portal-v1.png", optimize=True)
    portal.save(WEB / "saigon-portal-v1.png", optimize=True)
    save_webp(spread, WEB / "saigon-spread-v1.webp")

    # The eight existing quoted memories now draw from this board. Each crop
    # is a complete 4:3 vignette, retaining the author's original quotations.
    memory_boxes = (
        (275, 235, 690, 546),  # bridge and arrival
        (65, 80, 450, 369),    # work and first opportunity
        (250, 225, 690, 555),  # city and uncertainty
        (555, 180, 860, 409),  # letter and unfinished goodbye
        (55, 365, 395, 620),   # friends at the table
        (375, 485, 710, 736),  # couple and dog
        (55, 425, 355, 650),   # choosing to stay
        (200, 415, 760, 835),  # river, street and city
    )
    for number, box in enumerate(memory_boxes, 1):
        vignette = board.crop(box).resize((960, 720), Image.Resampling.LANCZOS)
        save_webp(vignette, WEB / f"saigon-memory-{number:02d}-v1.webp")

    proof = Image.new("RGBA", (SIZE, SIZE), "#e8cf9a")
    proof.alpha_composite(portal)
    proof.convert("RGB").resize((700, 700), Image.Resampling.LANCZOS).save(
        QA / "saigon-board-portal-composition.png", optimize=True
    )


if __name__ == "__main__":
    cut()
