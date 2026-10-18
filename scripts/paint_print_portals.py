"""Paint scalable-resolution paper-cut scenes for the digital and print editions.

The artwork is original code-native illustration based on the supplied board's
palette and the approved Cold Rice illustration. No protected source is edited.
Pillow and NumPy are required only when regenerating these images.
"""

from pathlib import Path
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SIZE = 3000
SCALE = SIZE / 1000
PRINT = ROOT / 'print/assets'
COVER_WEB = ROOT / 'shared/artwork/book-cover/cover-scene-saigon-v3.png'
RICE_WEB = ROOT / 'chapters/com-nguoi/artwork/portal/rice-scene-board-v3.png'

NAVY = '#142c3d'
INK = '#1d3444'
SLATE = '#345667'
TEAL = '#496c68'
GOLD = '#e7ad71'
CREAM = '#f1d3a4'
CORAL = '#d9735c'
PAPER = '#e9c99c'


def q(value):
    return round(value * SCALE)


def points(seq):
    return [(q(x), q(y)) for x, y in seq]


def polygon(draw, coords, fill, shadow=None, offset=5):
    if shadow:
        draw.polygon(points([(x + offset, y + offset) for x, y in coords]), fill=shadow)
    draw.polygon(points(coords), fill=fill)


def line(draw, coords, fill, width=2):
    draw.line(points(coords), fill=fill, width=max(1, q(width)), joint='curve')


def ellipse(draw, box, fill, outline=None, width=1):
    draw.ellipse(tuple(q(v) for v in box), fill=fill, outline=outline, width=max(1, q(width)))


def gradient(stops):
    rows = np.empty((SIZE, 3), dtype=np.float32)
    for (y0, a), (y1, b) in zip(stops, stops[1:]):
        lo, hi = q(y0), min(q(y1), SIZE - 1)
        t = np.linspace(0, 1, hi - lo + 1)[:, None]
        rows[lo:hi + 1] = np.asarray(a) * (1 - t) + np.asarray(b) * t
    return Image.fromarray(np.broadcast_to(rows[:, None, :], (SIZE, SIZE, 3)).astype('uint8').copy(), 'RGB')


def grain(image, seed, strength=4):
    rng = np.random.default_rng(seed)
    arr = np.asarray(image).astype(np.int16)
    texture = rng.integers(-strength, strength + 1, (SIZE, SIZE, 1), dtype=np.int16)
    arr = np.clip(arr + texture, 0, 255).astype('uint8')
    return Image.fromarray(arr, 'RGB')


def paper_flecks(draw, seed, count, y0=0, y1=1000):
    rng = random.Random(seed)
    for _ in range(count):
        x, y = rng.randrange(20, 980), rng.randrange(y0, y1)
        r = rng.choice((.6, 1, 1.5, 2))
        ellipse(draw, (x-r, y-r, x+r, y+r), rng.choice(('#f1d7a9', '#dfae79', '#b3b5a3')))


def paint_cover():
    image = gradient([
        (0, (18, 40, 57)), (320, (51, 86, 103)),
        (550, (206, 113, 89)), (685, (232, 155, 104)),
        (780, (86, 108, 111)), (1000, (21, 47, 60)),
    ])
    d = ImageDraw.Draw(image)
    # Moon, torn-paper clouds, and a few marks from the board's night sky.
    ellipse(d, (422, 225, 562, 365), '#eec48d', '#f7dda9', 3)
    ellipse(d, (438, 241, 546, 349), '#f1c995')
    polygon(d, [(50,490),(150,466),(214,480),(280,455),(365,476),(365,495),(50,510)], '#d8a08a')
    polygon(d, [(620,447),(701,422),(777,437),(830,414),(950,444),(950,460),(620,467)], '#d2a18a')
    paper_flecks(d, 219, 155, 70, 445)

    # Receding paper banks and skyline. Building shadows are displaced a few
    # pixels like stacked card rather than outlined computer geometry.
    polygon(d, [(0,634),(90,598),(160,608),(245,570),(330,599),(413,575),(502,604),(620,572),(720,594),(818,561),(1000,600),(1000,710),(0,710)], '#68777a', '#344f5d', 6)
    rng = random.Random(802)
    buildings = [(45,605,92,690),(118,569,160,690),(179,590,219,690),
                 (261,538,300,690),(308,586,350,690),(385,571,423,690),
                 (564,582,603,690),(612,551,655,690),(825,568,864,690),
                 (878,530,925,690),(935,587,986,690)]
    for x0,y0,x1,y1 in buildings:
        polygon(d, [(x0,y1),(x0,y0),(x1,y0),(x1,y1)], '#314a59', '#213848', 5)
        for wy in range(y0+19, y1-10, 25):
            for wx in range(x0+10, x1-8, 14):
                if rng.random() < .64:
                    d.rectangle((q(wx),q(wy),q(wx+3),q(wy+5)), fill='#d9a879')

    # Bitexco: the tapering lotus-bud outline and the unmistakable cantilevered
    # helipad are simplified into two card layers, not a copied photograph.
    tower = [(704,690),(709,518),(719,424),(737,354),(752,326),
             (766,340),(779,402),(785,509),(780,690)]
    polygon(d, tower, '#213b4d', '#102a3b', 7)
    polygon(d, [(712,690),(717,517),(730,421),(749,348),(753,337),(748,494),(748,690)], '#3f6573')
    polygon(d, [(778,466),(834,458),(847,465),(788,479)], '#1a3546', '#0e2636', 3)
    line(d, [(778,463),(838,458)], '#d5a475', 2)
    for y in range(390, 676, 21):
        t=(y-326)/364
        x=739-18*t
        line(d, [(x,y),(x+24+5*t,y)], '#a98270', 1)

    # Ba Son Bridge: one leaning arched pylon and an asymmetric cable fan.
    # The deck crosses the river in front of the skyline.
    polygon(d, [(68,632),(232,612),(437,606),(694,611),(936,631),
                (936,647),(694,629),(437,624),(230,631),(68,651)], '#243b4a', '#142d3d', 4)
    polygon(d, [(480,624),(481,494),(490,431),(506,390),(520,368),
                (534,361),(532,378),(515,427),(504,498),(502,626)], '#1a3445', '#102838', 4)
    line(d, [(487,495),(501,430),(522,378)], '#bd9374', 2)
    anchors=[(160,641),(225,634),(290,629),(355,625),(420,624),
             (561,626),(634,629),(711,634),(795,641),(875,646)]
    for i,(ax,ay) in enumerate(anchors):
        py=401+min(i, 8)*12 if i<5 else 415+(i-5)*22
        px=517 if i<5 else 510
        line(d, [(px,py),(ax,ay)], '#dfb493', 1.6)
    line(d, [(68,633),(230,614),(437,607),(695,612),(936,632)], '#e6a778', 2)

    # River, paper-cut shore and broken warm reflections.
    polygon(d, [(0,669),(210,653),(448,677),(693,653),(1000,668),(1000,1000),(0,1000)], '#385669', '#17394b', 7)
    polygon(d, [(0,770),(166,744),(303,762),(475,744),(628,765),(799,739),(1000,775),(1000,1000),(0,1000)], '#29495b')
    polygon(d, [(0,925),(187,877),(382,915),(562,882),(767,913),(1000,862),(1000,1000),(0,1000)], '#1c394b')
    rng=random.Random(454)
    for _ in range(320):
        y=rng.randrange(680,940);x=rng.randrange(130,880)
        near=abs(x-(480+(y-680)*.11))
        if near>190 and rng.random()<.65:continue
        length=rng.randrange(3,18)+int((y-680)/52)
        color=rng.choice(('#e8ad78','#bf8f72','#839596','#d8a37a'))
        line(d,[(x,y),(x+length,y)],color,rng.choice((.6,.9,1.2)))
    polygon(d, [(0,948),(130,891),(266,919),(335,1000),(0,1000)], '#173443')
    polygon(d, [(1000,920),(865,875),(766,915),(685,1000),(1000,1000)], '#173443')
    return grain(image, 20261018, 4)


def paint_rice():
    image=gradient([(0,(20,43,58)),(380,(59,76,78)),(655,(177,112,82)),(1000,(34,54,62))])
    d=ImageDraw.Draw(image)
    # Broad, stacked paper walls: the same navy / dusty teal / terracotta
    # family as the main cover, with the meal held in a warmer centre.
    polygon(d,[(0,0),(176,0),(176,1000),(0,1000)],'#203d4e')
    polygon(d,[(824,0),(1000,0),(1000,1000),(824,1000)],'#203d4e')
    polygon(d,[(155,0),(310,0),(310,620),(168,670)],'#456b6e','#284b59')
    polygon(d,[(692,0),(842,0),(842,662),(692,622)],'#466a6d','#284a58')
    polygon(d,[(286,103),(715,103),(745,583),(254,583)],'#8b7a6d','#263e4b',8)
    polygon(d,[(310,126),(692,126),(711,551),(287,551)],'#33576a')
    polygon(d,[(310,126),(692,126),(692,360),(310,360)],'#456d7a')
    ellipse(d,(456,177,552,273),'#deb789')
    polygon(d,[(311,429),(350,389),(391,411),(425,356),(471,414),
               (531,365),(571,413),(627,377),(697,421),(711,551),(287,551)],'#213f50')
    for x,y,w,h in [(345,390,20,80),(394,385,24,102),(475,409,32,96),
                    (566,380,28,100),(639,415,27,95)]:
        polygon(d,[(x,y+h),(x,y),(x+w,y),(x+w,y+h)],'#294859')
    rng=random.Random(779)
    for _ in range(50):
        x=rng.randrange(320,690);y=rng.randrange(410,540)
        d.rectangle((q(x),q(y),q(x+3),q(y+6)),fill='#d7a67a')
    # Window mullions and shelf, with paper edge highlights.
    polygon(d,[(287,126),(312,126),(312,551),(287,551)],'#1a3445')
    polygon(d,[(687,126),(711,126),(711,551),(687,551)],'#1a3445')
    polygon(d,[(488,126),(510,126),(510,551),(488,551)],'#1a3445')
    polygon(d,[(287,322),(711,322),(711,343),(287,343)],'#1a3445')
    polygon(d,[(263,551),(736,551),(754,570),(246,570)],'#c58968','#513e44',5)

    # Pendant lamp, a calm circle of light, and a rim like the board's moon.
    polygon(d,[(491,0),(509,0),(506,169),(494,169)],'#192e3e')
    ellipse(d,(469,165,531,198),'#203646')
    polygon(d,[(389,249),(407,200),(445,182),(555,182),(593,200),(612,249),
               (591,262),(409,262)],'#263a47','#172b3b',6)
    polygon(d,[(409,250),(591,250),(574,266),(426,266)],'#dca46e')
    ellipse(d,(468,250,532,310),'#f3d195')
    ellipse(d,(479,259,521,301),'#f7dca7')
    # Soft cone is a translucent layer, retained below the character shapes.
    glow=Image.new('RGBA',image.size)
    gd=ImageDraw.Draw(glow)
    gd.polygon(points([(429,264),(571,264),(744,703),(260,703)]),fill=(247,183,113,35))
    image=Image.alpha_composite(image.convert('RGBA'),glow)
    d=ImageDraw.Draw(image)

    # Family table and father/child figures. Skin is warm card; clothes and
    # hair echo Jason's navy silhouette in the outer ring.
    polygon(d,[(78,693),(922,693),(955,732),(46,732)],'#bd805d','#584b4a',6)
    polygon(d,[(75,729),(925,729),(925,808),(75,808)],'#5a4b48')
    polygon(d,[(128,804),(184,804),(172,1000),(137,1000)],'#293e4b')
    polygon(d,[(816,804),(872,804),(866,1000),(830,1000)],'#293e4b')
    # Father: turned toward the bowl.
    polygon(d,[(155,803),(170,610),(200,548),(255,515),(315,537),
               (353,589),(377,713),(341,788)],'#263f50','#132d3d',6)
    ellipse(d,(225,405,330,536),'#b78065')
    polygon(d,[(222,472),(228,423),(249,397),(302,397),(327,427),
               (322,471),(297,451),(266,457),(247,484)],'#183346')
    polygon(d,[(319,598),(405,654),(450,695),(424,721),(339,679)],'#315166')
    ellipse(d,(419,686,451,719),'#b98369')
    # Child: smaller profile, reaching for the shared meal.
    polygon(d,[(693,802),(650,616),(663,560),(703,542),(747,565),
               (804,649),(834,802)],'#496c71','#243e4d',5)
    ellipse(d,(657,452,750,558),'#bf886b')
    polygon(d,[(651,505),(660,464),(682,443),(727,447),(753,475),
               (743,508),(718,493),(685,515)],'#20394b')
    polygon(d,[(667,617),(590,673),(558,696),(573,720),(681,676)],'#527a7c')
    ellipse(d,(548,687,577,720),'#c18b6e')

    # Porcelain bowl and cold rice are the chapter's focal still life.
    polygon(d,[(394,690),(608,690),(587,770),(560,795),(440,795),(415,770)],'#efe1c3','#263c4a',6)
    ellipse(d,(390,667,610,715),'#f8e9cd','#305268',4)
    polygon(d,[(417,669),(441,647),(474,654),(496,637),(519,653),
               (552,644),(582,673)],'#f8edcf')
    ellipse(d,(426,676,572,699),'#f8eccf')
    for x,y in [(460,726),(488,734),(518,726),(541,739)]:
        ellipse(d,(x-7,y-7,x+7,y+7),'#416a77')
    line(d,[(446,755),(555,755)],'#3c6877',2)
    # Two modest side dishes and chopsticks.
    for cx in (337,667):
        polygon(d,[(cx-39,713),(cx+39,713),(cx+29,743),(cx-30,743)],'#ead2a9')
        ellipse(d,(cx-40,697,cx+40,722),'#eee0bd')
        ellipse(d,(cx-26,696,cx+26,710),'#9c725c')
    line(d,[(322,629),(436,681)],'#3a333b',3)
    line(d,[(329,622),(442,674)],'#cf9c71',2)
    line(d,[(686,630),(571,680)],'#3a333b',3)
    line(d,[(693,638),(578,688)],'#cf9c71',2)
    # The rice is cold: a small, restrained wisp rather than hot steam.
    line(d,[(503,638),(498,620),(509,608),(504,591)],'#e7c9a0',2)
    polygon(d,[(0,916),(198,866),(332,912),(503,882),(697,918),(839,874),
               (1000,920),(1000,1000),(0,1000)],'#193747')
    paper_flecks(d, 717, 130, 30, 980)
    return grain(image.convert('RGB'), 20261019, 4)


def export(image, print_path, web_path):
    print_path.parent.mkdir(parents=True, exist_ok=True)
    web_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(print_path, dpi=(600,600), optimize=True)
    image.resize((1000,1000),Image.Resampling.LANCZOS).save(web_path, optimize=True)
    print(f'{print_path.relative_to(ROOT)} -> {web_path.relative_to(ROOT)}')


if __name__ == '__main__':
    export(paint_cover(), PRINT/'cover-saigon-scene-3000.png', COVER_WEB)
    export(paint_rice(), PRINT/'cold-rice-scene-3000.png', RICE_WEB)
