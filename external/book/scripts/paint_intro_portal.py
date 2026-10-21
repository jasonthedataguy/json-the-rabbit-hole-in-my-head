"""Paint the Introduction's scene-only paper-book portal.

The scene shares the design board's navy, dusk, terracotta and parchment
palette. The rotating ring is supplied separately by the website.
"""

from pathlib import Path
import random
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'shared/artwork/portal/introduction-scene.png'
SIZE = 1000


def gradient():
    stops = [(0, (18, 38, 55)), (340, (46, 74, 88)),
             (535, (196, 112, 83)), (665, (58, 77, 81)),
             (1000, (13, 32, 46))]
    image = Image.new('RGB', (SIZE, SIZE))
    px = image.load()
    for y in range(SIZE):
        for (a, ca), (b, cb) in zip(stops, stops[1:]):
            if a <= y <= b:
                t = (y - a) / (b - a)
                c = tuple(round(ca[i] * (1 - t) + cb[i] * t) for i in range(3))
                break
        for x in range(SIZE):
            px[x, y] = c
    return image


def textured_paper(size, base, seed):
    rng = random.Random(seed)
    paper = Image.new('RGB', size, base)
    pixels = paper.load()
    for y in range(size[1]):
        for x in range(size[0]):
            n = rng.randrange(-12, 13)
            pixels[x, y] = tuple(max(0, min(255, v + n)) for v in base)
    return paper


def paste_shape(canvas, texture, points, offset=(0, 0)):
    mask = Image.new('L', canvas.size)
    ImageDraw.Draw(mask).polygon(points, fill=255)
    canvas.paste(texture, offset, mask)


def paint(target=TARGET):
    rng = random.Random(1408)
    image = gradient()
    draw = ImageDraw.Draw(image)
    # Far sky: a softened sun and a few paper flecks.
    glow = Image.new('RGBA', image.size)
    g = ImageDraw.Draw(glow)
    g.ellipse((328, 224, 672, 568), fill=(248, 184, 120, 92))
    image = Image.alpha_composite(image.convert('RGBA'), glow.filter(ImageFilter.GaussianBlur(54)))
    draw = ImageDraw.Draw(image)
    draw.ellipse((410, 315, 590, 495), fill='#e8ba82')
    draw.ellipse((433, 338, 567, 472), fill='#f1c998')
    for x, y, r in [(241, 253, 4), (330, 195, 3), (711, 221, 4),
                    (776, 324, 3), (617, 196, 2), (186, 395, 3)]:
        draw.line((x-r*2, y, x+r*2, y), fill='#d8b68b', width=2)
        draw.line((x, y-r*2, x, y+r*2), fill='#d8b68b', width=2)

    # Layered dusk skyline follows the board palette without added landmarks.
    draw.polygon([(90, 608), (90, 514), (132, 514), (132, 474), (168, 474),
                  (168, 560), (210, 560), (210, 440), (248, 440),
                  (248, 601)], fill='#273d4c')
    draw.polygon([(740, 603), (740, 493), (773, 493), (773, 454),
                  (813, 454), (813, 542), (850, 542), (850, 505),
                  (901, 505), (901, 612)], fill='#273d4c')
    draw.polygon([(619, 587), (619, 477), (654, 477), (654, 439),
                  (687, 439), (687, 525), (714, 525), (714, 587)], fill='#1d3446')
    draw.polygon([(260, 591), (260, 530), (307, 530), (307, 481),
                  (341, 481), (341, 557), (384, 557), (384, 590)], fill='#253e4b')
    draw.polygon([(387, 590), (387, 541), (421, 541), (421, 499),
                  (454, 499), (454, 552), (496, 552), (496, 590)], fill='#223b4a')
    for _ in range(36):
        x = rng.randrange(150, 855)
        y = rng.randrange(478, 603)
        if (x < 260 or x > 630) and rng.random() < .6:
            draw.rectangle((x, y, x+3, y+5), fill='#e6ac72')

    # River and foreground layers keep the circular crop filled edge-to-edge.
    draw.polygon([(0, 618), (210, 598), (460, 616), (720, 596),
                  (1000, 629), (1000, 1000), (0, 1000)], fill='#1c3545')
    for y in range(637, 752, 19):
        draw.line((317 + (y % 3)*16, y, 692 - (y % 5)*13, y+2),
                  fill='#8e7968', width=2)
    draw.polygon([(0, 785), (230, 733), (502, 771), (770, 716),
                  (1000, 780), (1000, 1000), (0, 1000)], fill='#162d3b')

    # Book shadow and dark cloth backing.
    shadow = Image.new('RGBA', image.size)
    ImageDraw.Draw(shadow).ellipse((177, 729, 842, 892), fill=(0, 0, 0, 120))
    image = Image.alpha_composite(image, shadow.filter(ImageFilter.GaussianBlur(28)))
    draw = ImageDraw.Draw(image)
    draw.polygon([(177, 609), (340, 568), (500, 622), (663, 568),
                  (823, 611), (795, 812), (500, 854), (207, 813)], fill='#0c2231')
    draw.line((178, 610, 340, 568, 500, 622, 663, 568, 822, 611),
              fill='#b98b62', width=7, joint='curve')
    draw.polygon([(204, 614), (337, 584), (498, 636), (498, 821),
                  (351, 764), (226, 786)], fill='#c99f78')
    draw.polygon([(502, 636), (664, 584), (798, 614), (774, 786),
                  (648, 764), (502, 821)], fill='#c99f78')

    # Two rough, luminous parchment leaves, with subtly different edges.
    paper = textured_paper(image.size, (237, 215, 178), 704)
    left = [(217, 607), (339, 578), (492, 631), (495, 807),
            (354, 748), (237, 769)]
    right = [(505, 631), (661, 578), (783, 607), (762, 769),
             (647, 748), (505, 807)]
    paste_shape(image, paper, left)
    paste_shape(image, paper, right)
    draw = ImageDraw.Draw(image)
    draw.line((217, 607, 339, 578, 492, 631, 495, 807),
              fill='#fff0cb', width=5, joint='curve')
    draw.line((505, 807, 505, 631, 661, 578, 783, 607),
              fill='#fff0cb', width=5, joint='curve')
    draw.line((497, 627, 500, 817), fill='#9f735e', width=5)
    draw.line((504, 631, 501, 814), fill='#f9e8c1', width=3)
    draw.line((238, 771, 354, 751, 495, 810, 505, 810, 647, 751, 763, 771),
              fill='#b2785c', width=4, joint='curve')

    # Left page: mathematical diagram; right page: lines of open prose.
    for x in range(283, 439, 29):
        draw.line((x, 635, x+5, 724), fill='#d3b894', width=2)
    for y in range(638, 727, 26):
        draw.line((268, y, 459, y+11), fill='#d3b894', width=2)
    draw.arc((305, 648, 418, 739), 190, 345, fill='#8f9283', width=4)
    draw.line((312, 722, 382, 652, 429, 718), fill='#a07768', width=4)
    for y, width in [(635, 153), (661, 171), (687, 139), (713, 160)]:
        draw.line((544, y, 544+width, y-20), fill='#a9977d', width=4)
    draw.arc((626, 702, 718, 754), 195, 344, fill='#9c7867', width=3)

    # Tiny lifted paper fragments lead into the skyline.
    draw.polygon([(354, 528), (390, 516), (404, 548), (374, 541)], fill='#e5b886')
    draw.line((354, 528, 374, 541, 404, 548), fill='#fff0c8', width=2)
    draw.polygon([(706, 516), (733, 498), (725, 532), (694, 539)], fill='#d76f56')
    draw.line((706, 516, 733, 498, 725, 532), fill='#f8bc8c', width=2)

    # Fine film grain links the painted elements with the reference board.
    image = image.convert('RGB')
    noise = Image.new('RGB', image.size)
    data = [tuple(max(0, min(255, channel + rng.randrange(-5, 6)))
                  for channel in pixel) for pixel in image.getdata()]
    noise.putdata(data)
    target.parent.mkdir(parents=True, exist_ok=True)
    noise.save(target, optimize=True)
    print(f'Painted Introduction portal: {target.relative_to(ROOT)}')


if __name__ == '__main__':
    paint()
