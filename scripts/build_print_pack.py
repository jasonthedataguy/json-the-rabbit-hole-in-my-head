"""Build the 6 x 9 inch layered-book print prototype.

The PDFs are 300 ppi RGB proofs. The SVGs carry dimensioned trim, fold, and
optional portal-cut paths. Set --spine-mm when the printer's page count and
paper stock are known. This script never changes protected source artwork.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT=Path(__file__).resolve().parents[1]
PRINT=ROOT/'print'
ASSETS=PRINT/'assets'
PROOFS=PRINT/'proofs'
CUT=PRINT/'cut'
PDF=ROOT/'output/pdf'
DPI=300
MM= DPI/25.4
TRIM_W=152.4
TRIM_H=228.6
BLEED=3.175
NAVY='#102332'
CREAM='#f0d3a3'
PAPER='#ebd5b1'
GOLD='#cba26e'
INK='#172f3e'


def px(mm):return round(mm*MM)


def font(name,point):
    path=ROOT/'shared/fonts'/name
    return ImageFont.truetype(str(path),round(point*DPI/72))


def paper(size,base,seed):
    im=Image.new('RGB',size,base)
    rng=random.Random(seed)
    d=ImageDraw.Draw(im)
    for _ in range(size[0]*size[1]//1250):
        x=rng.randrange(size[0]);y=rng.randrange(size[1])
        shade=rng.choice(('#f6e7c8','#dcc4a0','#e4cda9'))
        d.point((x,y),fill=shade)
    return im


def alpha_circle(image,diameter):
    art=image.convert('RGBA').resize((diameter,diameter),Image.Resampling.LANCZOS)
    mask=Image.new('L',(diameter,diameter))
    ImageDraw.Draw(mask).ellipse((0,0,diameter-1,diameter-1),fill=255)
    art.putalpha(mask)
    return art


def ring_assets():
    for source,name in [('board-cover-ring.png','cover-ring-3000.png'),('board-ring-cut.png','chapter-ring-3000.png')]:
        ring=Image.open(ROOT/'shared/artwork/portal'/source).convert('RGBA')
        ring=ring.resize((3000,3000),Image.Resampling.LANCZOS)
        ring=ring.filter(ImageFilter.UnsharpMask(radius=1.1,percent=60,threshold=3))
        ring.save(ASSETS/name,optimize=True,dpi=(600,600))
        alpha=ring.getchannel('A')
        alpha.save(ASSETS/name.replace('.png','-alpha.png'),optimize=True)


def paste_portal(canvas,scene_path,ring_path,cx,cy,diameter,show_scene=True):
    canvas=canvas.convert('RGBA')
    if show_scene:
        scene=Image.open(scene_path).convert('RGB')
        inner=round(diameter*.624)
        circle=alpha_circle(scene,inner)
        canvas.alpha_composite(circle,(cx-inner//2,cy-inner//2))
    else:
        # This area is physically removed when using the matching cut guide.
        inner=round(diameter*.624)
        d=ImageDraw.Draw(canvas)
        d.ellipse((cx-inner//2,cy-inner//2,cx+inner//2,cy+inner//2),fill=INK)
    ring=Image.open(ring_path).convert('RGBA').resize((diameter,diameter),Image.Resampling.LANCZOS)
    canvas.alpha_composite(ring,(cx-diameter//2,cy-diameter//2))
    return canvas.convert('RGB')


def cover_wrap(spine_mm,show_scene):
    w=px(2*TRIM_W+spine_mm+2*BLEED);h=px(TRIM_H+2*BLEED)
    page=paper((w,h),NAVY,21)
    d=ImageDraw.Draw(page)
    bx=px(BLEED); sx=px(BLEED+TRIM_W); fx=px(BLEED+TRIM_W+spine_mm)
    front_cx=fx+px(TRIM_W/2); back_cx=bx+px(TRIM_W/2)
    # Cloth grain and a quiet back-cover scene band.
    rng=random.Random(1944)
    for _ in range(5000):
        x=rng.randrange(w);y=rng.randrange(h)
        d.line((x,y,x+rng.randrange(1,4),y),fill='#213a48',width=1)
    landscape=Image.open(ASSETS/'cover-saigon-scene-3000.png').convert('RGB')
    band=landscape.crop((0,900,3000,2550)).resize((px(TRIM_W),px(63)),Image.Resampling.LANCZOS)
    band=Image.blend(Image.new('RGB',band.size,NAVY),band,.29)
    fade=Image.new('L',band.size)
    fade_pixels=fade.load()
    fade_depth=px(22)
    bottom_fade=px(10)
    side_fade=px(6)
    for row in range(band.height):
        vertical=min(1,row/fade_depth,(band.height-1-row)/bottom_fade)
        for column in range(band.width):
            horizontal=min(1,column/side_fade,(band.width-1-column)/side_fade)
            fade_pixels[column,row]=round(255*min(vertical,horizontal))
    page.paste(band,(bx,px(BLEED+TRIM_H-63)),fade)
    # Back typography keeps the exact concept-board line; no placeholder ISBN.
    d=ImageDraw.Draw(page)
    d.ellipse((back_cx-px(5),px(45),back_cx+px(5),px(55)),fill=GOLD)
    lines=['One book.','32 portals.','A continuous journey','into the many versions','of myself.']
    quote=font('Libre-Caslon-Display-Regular.ttf',19)
    for i,text in enumerate(lines):
        d.text((back_cx,px(76+i*12.5)),text,font=quote,anchor='mm',fill='#f3dfbd')
    d.line((back_cx-px(13),px(151),back_cx+px(13),px(151)),fill=GOLD,width=px(.3))
    # A narrow, adjustable spine. Text stays inside a conservative safe zone.
    spine_center=sx+px(spine_mm/2)
    d.line((sx,px(BLEED+8),sx,px(TRIM_H+BLEED-8)),fill='#425467',width=px(.22))
    d.line((fx,px(BLEED+8),fx,px(TRIM_H+BLEED-8)),fill='#425467',width=px(.22))
    label=Image.new('RGBA',(px(60),px(max(7,spine_mm-3))),(0,0,0,0))
    ld=ImageDraw.Draw(label)
    ld.text((label.width//2,label.height//2),'.json',font=font('Libre-Caslon-Display-Regular.ttf',16),anchor='mm',fill=CREAM)
    label=label.rotate(90,expand=True)
    page.paste(label,(spine_center-label.width//2,h//2-label.height//2),label)
    # Front board layout: cloth, title, portal and small lower ornament.
    d=ImageDraw.Draw(page)
    d.text((front_cx,px(BLEED+25)),'.json',font=font('Libre-Caslon-Display-Regular.ttf',72),anchor='mm',fill='#f4d8ad')
    d.text((front_cx,px(BLEED+43)),'JASON, UNDER REVISION',font=font('DM-Sans-Medium.ttf',10),anchor='mm',fill=CREAM,stroke_width=0)
    portal_d=px(130)
    page=paste_portal(page,ASSETS/'cover-saigon-scene-3000.png',ASSETS/'cover-ring-3000.png',front_cx,px(BLEED+128),portal_d,show_scene)
    d=ImageDraw.Draw(page)
    d.line((front_cx-px(11),px(BLEED+207),front_cx+px(11),px(BLEED+207)),fill=GOLD,width=px(.3))
    d.text((front_cx,px(BLEED+218)),'ONE BOOK · THIRTY-TWO PORTALS',font=font('DM-Sans-Medium.ttf',7),anchor='mm',fill='#c8b08b')
    return page


def underlay(scene_path,seed):
    size=(px(TRIM_W+2*BLEED),px(TRIM_H+2*BLEED))
    page=paper(size,NAVY,seed)
    cx=px(BLEED+TRIM_W/2);cy=px(BLEED+128)
    # 6 mm art overlap beyond the cover aperture compensates for assembly.
    d=px(92)
    scene=alpha_circle(Image.open(scene_path),d)
    page=page.convert('RGBA');page.alpha_composite(scene,(cx-d//2,cy-d//2))
    return page.convert('RGB')


def chapter_opener(show_scene):
    size=(px(TRIM_W+2*BLEED),px(TRIM_H+2*BLEED))
    page=paper(size,PAPER,53)
    d=ImageDraw.Draw(page)
    cx=px(BLEED+TRIM_W/2)
    d.text((cx,px(BLEED+19)),'00  /  PROLOGUE',font=font('DM-Sans-Medium.ttf',9),anchor='mm',fill=INK)
    d.line((cx-px(14),px(BLEED+27),cx+px(14),px(BLEED+27)),fill='#a8795c',width=px(.28))
    d=px(118);cy=px(BLEED+106)
    page=paste_portal(page,ASSETS/'cold-rice-scene-3000.png',ASSETS/'chapter-ring-3000.png',cx,cy,d,show_scene)
    dr=ImageDraw.Draw(page)
    dr.text((cx,px(BLEED+181)),'COLD RICE',font=font('Libre-Caslon-Display-Regular.ttf',34),anchor='mm',fill=INK)
    dr.text((cx,px(BLEED+196)),'Cơm nguội',font=font('Noto-Serif-Italic.ttf',10),anchor='mm',fill='#775f53')
    dr.line((cx-px(24),px(BLEED+208),cx+px(24),px(BLEED+208)),fill='#aa8565',width=px(.25))
    return page


def chapter_underlay():
    size=(px(TRIM_W+2*BLEED),px(TRIM_H+2*BLEED))
    page=paper(size,PAPER,54).convert('RGBA')
    cx=px(BLEED+TRIM_W/2);cy=px(BLEED+106)
    d=px(84)
    scene=alpha_circle(Image.open(ASSETS/'cold-rice-scene-3000.png'),d)
    page.alpha_composite(scene,(cx-d//2,cy-d//2))
    return page.convert('RGB')


def svg_header(width,height):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.3f}mm" height="{height:.3f}mm" viewBox="0 0 {width:.3f} {height:.3f}">\n'


def cut_guides(spine_mm):
    total_w=2*TRIM_W+spine_mm+2*BLEED;total_h=TRIM_H+2*BLEED
    bx=BLEED; sx=BLEED+TRIM_W; fx=sx+spine_mm
    cx=fx+TRIM_W/2;cy=BLEED+128
    svg=svg_header(total_w,total_h)
    svg+='  <g fill="none" stroke-width="0.25">\n'
    svg+=f'    <rect id="back-trim" x="{bx:.3f}" y="{BLEED:.3f}" width="{TRIM_W:.3f}" height="{TRIM_H:.3f}" stroke="#00a7ba"/>\n'
    svg+=f'    <rect id="front-trim" x="{fx:.3f}" y="{BLEED:.3f}" width="{TRIM_W:.3f}" height="{TRIM_H:.3f}" stroke="#00a7ba"/>\n'
    svg+=f'    <line id="back-fold" x1="{sx:.3f}" y1="{BLEED:.3f}" x2="{sx:.3f}" y2="{BLEED+TRIM_H:.3f}" stroke="#00a7ba" stroke-dasharray="2 1"/>\n'
    svg+=f'    <line id="front-fold" x1="{fx:.3f}" y1="{BLEED:.3f}" x2="{fx:.3f}" y2="{BLEED+TRIM_H:.3f}" stroke="#00a7ba" stroke-dasharray="2 1"/>\n'
    svg+=f'    <circle id="optional-cover-aperture-cut" cx="{cx:.3f}" cy="{cy:.3f}" r="{130*.31:.3f}" stroke="#ff00b3"/>\n'
    svg+='  </g>\n</svg>\n'
    (CUT/'cover-wrap-dieline.svg').write_text(svg,encoding='utf-8')
    width=TRIM_W+2*BLEED
    ccx=BLEED+TRIM_W/2;ccy=BLEED+106
    chapter=svg_header(width,total_h)
    chapter+='  <g fill="none" stroke-width="0.25">\n'
    chapter+=f'    <rect id="trim" x="{BLEED:.3f}" y="{BLEED:.3f}" width="{TRIM_W:.3f}" height="{TRIM_H:.3f}" stroke="#00a7ba"/>\n'
    chapter+=f'    <circle id="chapter-aperture-cut" cx="{ccx:.3f}" cy="{ccy:.3f}" r="{118*.31:.3f}" stroke="#ff00b3"/>\n'
    chapter+='  </g>\n</svg>\n'
    (CUT/'chapter-00-dieline.svg').write_text(chapter,encoding='utf-8')
    # Concentric paper-band paths are optional guides for layered fabrication.
    layers=svg_header(130,130)
    layers+='  <g fill="none" stroke="#ff00b3" stroke-width="0.25">\n'
    for i,r in enumerate((62.4,58.5,53.5,48.5,43.5,38.5,40.3),1):
        layers+=f'    <circle id="paper-band-{i}" cx="65" cy="65" r="{r:.2f}"/>\n'
    layers+='  </g>\n</svg>\n'
    (CUT/'portal-ring-band-guides.svg').write_text(layers,encoding='utf-8')


def save_proof(image,name):
    image.save(PROOFS/f'{name}.png',dpi=(DPI,DPI),optimize=True)
    image.save(PDF/f'{name}.pdf','PDF',resolution=DPI,quality=95)


def build(spine_mm):
    if not 6<=spine_mm<=35:raise ValueError('Prototype spine must be 6-35 mm')
    for directory in (ASSETS,PROOFS,CUT,PDF):directory.mkdir(parents=True,exist_ok=True)
    ring_assets()
    save_proof(cover_wrap(spine_mm,True),'cover-wrap-flat-6x9')
    save_proof(cover_wrap(spine_mm,False),'cover-wrap-diecut-face-6x9')
    save_proof(underlay(ASSETS/'cover-saigon-scene-3000.png',62),'cover-portal-underlay-6x9')
    save_proof(chapter_opener(False),'chapter-00-diecut-face-6x9')
    save_proof(chapter_underlay(),'chapter-00-underlay-6x9')
    # A flat chapter composition is useful for proofing or a no-cut edition.
    chapter_opener(True).save(PROOFS/'chapter-00-flat-6x9.png',dpi=(DPI,DPI),optimize=True)
    cut_guides(spine_mm)
    files=[]
    for folder in (ASSETS,PROOFS,CUT,PDF):
        for path in sorted(folder.iterdir()):
            if path.is_file():
                files.append({'path':path.relative_to(ROOT).as_posix(),
                              'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                              'bytes':path.stat().st_size})
    manifest={'schema_version':1,'status':'prototype','trim_mm':[TRIM_W,TRIM_H],
              'bleed_mm':BLEED,'spine_mm':spine_mm,'raster_ppi':DPI,
              'color_mode':'RGB proof; convert to printer profile before production',
              'files':files}
    (PRINT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Built {len(files)} prototype assets, including 5 PDFs; spine {spine_mm:g} mm.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spine-mm',type=float,default=12.0)
    build(parser.parse_args().spine_mm)
