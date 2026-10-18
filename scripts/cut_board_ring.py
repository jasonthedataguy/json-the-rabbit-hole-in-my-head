"""Cut the cover picture and matching annular frame from the design board.

This is an optional design-time command; the committed PNG is used by the site.
Requires Pillow. The source board stays untouched in references/design/.
"""

from pathlib import Path
from collections import deque
import random
from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'references/design/Jason Under Revision_ Design Asset Board.png'
TARGET = ROOT / 'shared/artwork/portal/board-ring-cut.png'
COVER_FRAME = ROOT / 'shared/artwork/portal/board-cover-ring.png'
SCENE = ROOT / 'shared/artwork/book-cover/cover-scene-board.png'
CLEAN_SCENE = ROOT / 'shared/artwork/book-cover/cover-scene-board-clean.png'
LANDSCAPE_SCENE = ROOT / 'shared/artwork/book-cover/cover-scene-landscape.png'


def remove_stationary_figure(scene):
    """Fill the overlapping figure in the centre crop with the card behind it.

    The original crop remains available for comparison. Jason belongs to the
    foreground ring, so leaving his head in this upright scene would create a
    second, stationary copy as the ring turns.
    """
    clean = scene.copy()
    pixels = clean.load()
    original = scene.load()
    left, right = 397, 511
    for y in range(895, 1000):
        for x in range(left, right + 1):
            t = (x - left) / (right - left)
            # Sample card texture outside the silhouette at the same height.
            a = original[max(0, left - 15 + (x % 7)), y]
            b = original[min(999, right + 13 + (x % 9)), y]
            fill = tuple(round(a[c] * (1 - t) + b[c] * t) for c in range(3))
            feather = min(1, (x - left) / 9, (right - x) / 9, (y - 895) / 9)
            old = original[x, y]
            pixels[x, y] = tuple(round(old[c] * (1 - feather) + fill[c] * feather) for c in range(3))
    return clean


def extract_landscape_scene(board):
    """Use the board's separate portal layer, without its static Jason.

    This board panel already shows the same paper-cut city, bridge and river,
    but has no bowl or pedestal. The small figure at its base is filled with
    neighbouring river colour; the rotating ring supplies Jason instead.
    """
    scene = board.crop((1006, 143, 1150, 287)).resize((1000, 1000), Image.Resampling.LANCZOS)
    fill = scene.copy()
    source = scene.load()
    pixels = fill.load()
    rng = random.Random(72)
    for y in range(805, 1000):
        left, right = source[375, y], source[635, y]
        for x in range(380, 625):
            t = (x - 380) / 245
            grain = rng.randrange(-4, 5)
            pixels[x, y] = tuple(max(0, min(255, round(left[c] * (1-t) + right[c] * t + grain))) for c in range(3))
    mask = Image.new('L', scene.size)
    ImageDraw.Draw(mask).polygon(
        [(423, 808), (561, 808), (582, 845), (592, 920),
         (622, 1000), (382, 1000), (401, 920), (410, 845)],
        fill=255,
    )
    return Image.composite(fill, scene, mask.filter(ImageFilter.GaussianBlur(8)))


def cut_board_ring(source=SOURCE, target=TARGET, scene_target=SCENE, clean_scene_target=CLEAN_SCENE, landscape_scene_target=LANDSCAPE_SCENE, cover_target=COVER_FRAME):
    board = Image.open(source).convert('RGB')
    if board.size != (1536, 1024):
        raise ValueError(f'Unexpected design board dimensions: {board.size}')

    # The board's upper-left artwork has centre (224, 235) and a roughly
    # 200-pixel radius. The two crops meet at radius 124 in board coordinates.
    # The homepage keeps the complete ring, including the foreground figure,
    # across all its stops. The chapter map and reader use mirrored lower
    # bands where a figure in the frame would compete with chapter scenes.
    crop = board.crop((24, 35, 424, 435)).resize((1000, 1000), Image.Resampling.LANCZOS)
    scene = board.crop((100, 111, 348, 359)).resize((1000, 1000), Image.Resampling.LANCZOS)
    scene_target.parent.mkdir(parents=True, exist_ok=True)
    scene.save(scene_target)
    clean_scene = remove_stationary_figure(scene)
    clean_scene.save(clean_scene_target)
    extract_landscape_scene(board).save(landscape_scene_target)

    alpha = Image.new('L', (1000, 1000))
    draw = ImageDraw.Draw(alpha)
    draw.ellipse((20, 20, 980, 980), fill=255)
    draw.ellipse((190, 190, 810, 810), fill=0)
    # The boy overlaps the circular opening. Carry his head and shoulders in
    # the same rotating frame so a new centre picture never cuts him in half.
    cover_alpha = alpha.copy()
    boy = Image.new('L', (1000, 1000))
    boy_pixels = boy.load()
    source_pixels = crop.load()
    queued = {(470, 780)}
    frontier = deque(queued)
    while frontier:
        x, y = frontier.popleft()
        r, g, b = source_pixels[x, y]
        if not (r < 115 and g < 135 and b > r + 9):
            continue
        boy_pixels[x, y] = 255
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            neighbor = (x + dx, y + dy)
            if 428 <= neighbor[0] <= 520 and 735 <= neighbor[1] <= 840 and neighbor not in queued:
                queued.add(neighbor)
                frontier.append(neighbor)
    # The hair is dark blue, but the short neck is warm skin colour. The
    # colour flood fill therefore stops just above the coat. Bridge that
    # eight-pixel gap with the original neck pixels, keeping one silhouette.
    ImageDraw.Draw(boy).polygon(
        [(458, 794), (482, 794), (482, 801), (485, 806),
         (486, 812), (452, 812), (455, 806), (458, 801)],
        fill=255,
    )
    cover_alpha = ImageChops.lighter(cover_alpha, boy)
    cover_frame = Image.new('RGBA', (1000, 1000))
    cover_frame.paste(crop, (0, 0), cover_alpha)
    mirrored = crop.copy()
    upper = crop.crop((0, 0, 1000, 500))
    mirrored.paste(upper.transpose(Image.Transpose.FLIP_TOP_BOTTOM), (0, 500))
    frame = Image.new('RGBA', (1000, 1000))
    frame.paste(mirrored, (0, 0), alpha)
    target.parent.mkdir(parents=True, exist_ok=True)
    cover_target.parent.mkdir(parents=True, exist_ok=True)
    cover_frame.save(cover_target)
    frame.save(target)
    print(f'Cut board cover scene: {scene_target.relative_to(ROOT)}')
    print(f'Cut cover scene without stationary figure: {clean_scene_target.relative_to(ROOT)}')
    print(f'Cut landscape-only cover scene: {landscape_scene_target.relative_to(ROOT)}')
    print(f'Cut constant homepage ring: {cover_target.relative_to(ROOT)}')
    print(f'Cut clean chapter/map ring: {target.relative_to(ROOT)}')


if __name__ == '__main__':
    cut_board_ring()
