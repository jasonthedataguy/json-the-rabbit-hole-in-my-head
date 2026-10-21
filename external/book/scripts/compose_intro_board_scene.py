"""Make the Introduction centre scene from the supplied board's city artwork.

The board's illustrated chapter-page skyline is extended with matching dusk
and river colour so it can fill the square portal aperture without page type.
"""
from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'references/design/Jason, Under Revision Concept Board - introduction.png'
OUTPUT = ROOT / 'shared/artwork/portal/introduction-scene-board.png'
SIZE = 1000


def colour_at(y):
    stops = [
        (0, (13, 34, 51)),
        (220, (27, 48, 65)),
        (470, (206, 112, 78)),
        (620, (45, 75, 88)),
        (1000, (13, 35, 52)),
    ]
    for (y0, first), (y1, second) in zip(stops, stops[1:]):
        if y <= y1:
            t = max(0, min(1, (y-y0)/(y1-y0)))
            return tuple(round(a+(b-a)*t) for a,b in zip(first, second))
    return stops[-1][1]


def compose():
    board = Image.open(SOURCE).convert('RGB')
    if board.size != (1672, 941):
        raise ValueError(f'Unexpected Introduction artboard size: {board.size}')

    scene = Image.new('RGB', (SIZE, SIZE))
    painter = ImageDraw.Draw(scene)
    for y in range(SIZE):
        painter.line((0, y, SIZE, y), fill=colour_at(y))

    # The right-hand illustrated page of the board has no baked-in copy here.
    # Preserve its bridge, skyline, moon and river at their original proportion.
    artwork = board.crop((1108, 802, 1261, 906)).resize((SIZE, 650), Image.Resampling.LANCZOS)
    alpha = Image.new('L', artwork.size)
    mask_draw = ImageDraw.Draw(alpha)
    for y in range(650):
        opacity = min(255, max(0, round(255*y/85)), max(0, round(255*(650-y)/95)))
        mask_draw.line((0, y, SIZE, y), fill=opacity)
    scene.paste(artwork, (0, 240), alpha.filter(ImageFilter.GaussianBlur(2)))

    # Re-cut the skyline and Ba Son-style cable fan as sharp paper silhouettes.
    # The board crop provides colour and texture; these edges stay legible when
    # the scene is reduced to the small opening on the Introduction leaf.
    painter = ImageDraw.Draw(scene)
    ink = (17, 42, 58)
    edge = (52, 84, 98)
    buildings = [
        [(53, 607), (53, 361), (89, 361), (89, 327), (99, 308), (109, 327), (109, 361), (139, 361), (139, 607)],
        [(151, 608), (151, 474), (202, 474), (202, 608)],
        [(214, 608), (214, 423), (229, 423), (229, 404), (249, 404), (249, 423), (270, 423), (270, 608)],
        [(572, 608), (572, 405), (593, 405), (593, 383), (610, 383), (610, 405), (648, 405), (648, 608)],
        [(661, 608), (661, 322), (715, 322), (715, 608)],
        [(722, 608), (722, 260), (771, 260), (771, 608)],
        [(779, 608), (779, 331), (831, 331), (831, 608)],
        [(840, 608), (840, 236), (898, 236), (898, 608)],
        [(908, 608), (908, 300), (959, 300), (959, 608)],
    ]
    for shape in buildings:
        painter.polygon(shape, fill=ink)
        painter.line(shape[:3], fill=edge, width=3)
    for x0, y0, x1, y1 in [(65, 385, 129, 588), (223, 444, 260, 583), (586, 425, 638, 584),
                           (676, 350, 704, 583), (734, 283, 764, 574), (853, 259, 890, 570),
                           (918, 330, 950, 575)]:
        for y in range(y0, y1, 43):
            for x in range(x0, x1, 19):
                if (x+y) % 4:
                    painter.rectangle((x, y, x+5, y+9), fill=(220, 162, 111))

    painter.ellipse((500, 292, 620, 412), fill=(245, 198, 137), outline=(255, 225, 175), width=5)
    painter.arc((506, 299, 614, 407), 200, 335, fill=(255, 236, 185), width=4)
    painter.rectangle((270, 566, 590, 585), fill=ink)
    painter.line((267, 564, 592, 564), fill=(228, 166, 105), width=5)
    painter.rectangle((420, 421, 438, 593), fill=ink)
    painter.polygon([(415, 431), (429, 405), (443, 431)], fill=ink)
    for x in (288, 320, 350, 381, 463, 494, 526, 557, 587):
        painter.line((429, 433, x, 563), fill=(233, 175, 116), width=3)
    for x in (300, 375, 500, 566):
        painter.rectangle((x, 582, x+12, 624), fill=ink)

    rng = random.Random(2607)
    for y in range(632, 884, 14):
        for _ in range(9):
            x = rng.randrange(35, 955)
            width = rng.randrange(15, 92)
            colour = (232, 156, 101) if abs(x-550) < 130 else (102, 140, 151)
            painter.line((x, y, x+width, y+rng.choice((-1, 0, 1))), fill=colour, width=rng.choice((2, 3, 4)))

    # A few tiny cut-paper stars carry the board texture into the extended sky.
    rng = random.Random(1607)
    for _ in range(20):
        x, y = rng.randrange(70, 930), rng.randrange(45, 250)
        r = rng.choice((1, 2, 3))
        painter.ellipse((x-r, y-r, x+r, y+r), fill=(234, 190, 133))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    scene.save(OUTPUT, optimize=True)


if __name__ == '__main__':
    compose()
