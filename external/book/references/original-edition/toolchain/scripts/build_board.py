"""Compose review boards from the files that actually exist in each product set."""
import argparse
from PIL import Image,ImageDraw
from common import chapters,read_json
from build_products import cover,font,save,text_block

parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--chapter');args=parser.parse_args()
for folder,meta in chapters(args.chapter):
    if not meta['publish'] or meta.get('release_stage','multimedia')!='multimedia':continue
    vector=meta['illustration'].endswith('.svg')
    extras=read_json(folder/'production.json').get('print_extras',False)
    W,H=2400,2200 if extras else 1760;palette=meta['palette']
    image=Image.new('RGB',(W,H),palette['paper']);draw=ImageDraw.Draw(image)
    draw.rectangle((0,0,W,125),fill=palette['dark'])
    draw.text((40,26),f'.json / {meta["number"]} — {meta["title"]}',font=font(53,2),fill=palette['paper'])
    art_label='APPROVED VECTOR ART' if vector else 'ARTWORK CROPS'
    draw.text((40,92),f'ACTUAL PRODUCT SET / {art_label} / VIDEO EDIT PREVIEWS AWAITING AUTHOR RECORDING',font=font(16,3),fill=palette['accent'])
    panels=[
       ('01 / CHAPTER COVER','artwork/exports/cover-a5.jpg',(30,150,510,850)),
       ('02 / ILLUSTRATED A5 PROOF','previews/book.jpg',(540,150,1570,850)),
       ('03 / RESPONSIVE CHAPTER','previews/web-390.png',(1600,150,2020,850)),
       ('04 / FILM EDIT PREVIEW','previews/video-frame.jpg',(2050,150,2370,850)),
       ('05 / FIVE-CARD CAROUSEL · 1080 × 1440','previews/carousel.jpg',(30,890,1450,1340)),
       ('06 / SOURCE-ART SCENE LIBRARY','previews/artwork.jpg',(1480,890,2370,1340)),
       ('07 / FACEBOOK','social/facebook/post.jpg',(30,1380,650,1715)),
       ('08 / YOUTUBE','social/youtube/thumbnail.jpg',(680,1380,1280,1715)),
    ]
    if extras:panels.extend([
        ('10 / POSTER + BOOKMARK PROOFS','previews/print-extras.jpg',(30,1770,850,2165)),
        ('11 / THREE STORIES + HIGHLIGHT','previews/stories.jpg',(880,1770,1680,2165)),
        ('12 / INTERACTIVE BELIEFS EXPLORER','previews/matrix-mobile.png',(1710,1770,2370,2165)),
    ])
    for title,relative,bounds in panels:
        x1,y1,x2,y2=bounds;draw.rectangle(bounds,outline=palette['dark'],width=2)
        draw.rectangle((x1,y1,x2,y1+38),fill=palette['dark']);draw.text((x1+10,y1+9),title,font=font(16,3),fill=palette['paper'])
        art=Image.open(folder/relative).convert('RGB');art.thumbnail((x2-x1-22,y2-y1-60))
        image.paste(art,(x1+(x2-x1-art.width)//2,y1+47+(y2-y1-60-art.height)//2))
    draw=ImageDraw.Draw(image)
    draw.text((1320,1380),'09 / PRODUCT STATE',font=font(23,1),fill=palette['dark'])
    films=len(read_json(folder/'video/timeline.json'))
    text=(f'Ready: original prose, six vector scenes, web artifact,\ncarousel, stories, poster, bookmark and platform copy.\nA5: complete illustrated editorial proof.\nVideo: {films} playable cuts + scripts + SRT/VTT.\nNext: Jason recording → retime → mix → review.' if vector else f'Ready: selected text, scene crops, web artifact,\n5-card carousel, poster and platform copy.\nA5: editorial proof; source art limits print detail.\nVideo: {films} playable cuts + provisional SRT/VTT.\nNext: Jason recording → retime → mix → review.')
    text_block(draw,text,(1320,1425),1000,font(24),palette['dark'],1.55)
    save(image,folder/'previews/product-board.jpg')
    print('Composed product board:',meta['slug'])
