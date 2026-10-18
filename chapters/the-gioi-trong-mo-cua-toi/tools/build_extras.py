"""Build Chapter 09 print, platform artwork and actual production board.

Run after scripts/build_supplied_media.py. Requires Pillow, ReportLab and
PyMuPDF. Browser QA screenshots are included in the board when present.
"""
from pathlib import Path
import json,sys
from PIL import Image,ImageDraw,ImageOps
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from common import read_json,write_json
from build_products import pdf,print_extras,card,save,font,text_block
p=ROOT/'chapters/the-gioi-trong-mo-cua-toi';meta=read_json(p/'chapter.json');scenes=read_json(p/'artwork/scenes/index.json')
pdf(p,meta,scenes);print_extras(p,meta,scenes)
hero=Image.open(p/'artwork/exports/hero.jpg')
save(card(meta,hero,meta['title'],(1480,2100),cover_card=True,scene_fit='contain'),p/'artwork/exports/cover-a5.jpg')
for target,size in [('facebook/post.jpg',(1600,900)),('youtube/thumbnail.jpg',(1280,720))]:
    save(card(meta,hero,meta['title'],size,number='CHAPTER',cover_card=True,scene_fit='contain'),p/'social'/target)
alts=[item for item in read_json(p/'social/alt-text.json') if item['file'].startswith('social/instagram/')]
for target in ['facebook/post.jpg','youtube/thumbnail.jpg','tiktok/cover.jpg']:
    alts.append({'file':'social/'+target,'alt':'Thế giới trong mơ của tôi — Chapter 09. Minh họa mái nhà Paris lúc chập tối, bảng màu xanh và vàng ấm.'})
write_json(p/'social/alt-text.json',alts)
write_json(p/'social/instagram/alt-text.json',[{'file':f'slide-{i:02d}.jpg','alt':item['text']+' — minh họa ý niệm, không phải ảnh tư liệu.'} for i,item in enumerate(read_json(p/'production.json')['publish_media']['carousel'],1)])
sheet=Image.new('RGB',(1500,440),meta['palette']['paper'])
for i in range(5):
    im=Image.open(p/f'social/instagram/slide-{i+1:02d}.jpg');im.thumbnail((280,400));sheet.paste(im,(10+i*300,20))
save(sheet,p/'previews/carousel.jpg')
scene_sheet=Image.new('RGB',(1200,500),meta['palette']['paper']);draw=ImageDraw.Draw(scene_sheet)
for i,scene in enumerate(scenes):
    x=i%4*300;y=i//4*250;im=ImageOps.contain(Image.open(p/scene['path']),(280,195));scene_sheet.paste(im,(x+(300-im.width)//2,y+10));draw.text((x+10,y+215),Path(scene['path']).stem,font=font(16,3),fill=meta['palette']['dark'])
save(scene_sheet,p/'previews/artwork.jpg')
board=Image.new('RGB',(2400,2700),meta['palette']['paper']);d=ImageDraw.Draw(board);dark=meta['palette']['dark'];paper=meta['palette']['paper'];accent=meta['palette']['accent']
d.rectangle((0,0,2400,260),fill=dark);d.text((55,30),'.json / CHAPTER 09 / THE BORROWED REEL',font=font(28,3),fill=accent)
d.text((55,95),meta['title'],font=font(96,2),fill=paper)
d.text((57,213),'OBSERVED → IMAGINED → AFTERIMAGE',font=font(25,3),fill=accent)
def panel(title,path,box):
    x,y,w,h=box;d.rectangle((x,y,x+w,y+h),fill=dark);d.text((x+18,y+14),title,font=font(24,3),fill=paper)
    im=ImageOps.contain(Image.open(p/path).convert('RGB'),(w-30,h-75));board.paste(im,(x+(w-im.width)//2,y+57))
web='previews/web-1440.png' if (p/'previews/web-1440.png').exists() else 'previews/website_desktop.png'
artifact='previews/interactive-1440.png' if (p/'previews/interactive-1440.png').exists() else 'web/assets/observed.jpg'
panel('01 / SUPPLIED SCENE LIBRARY','previews/artwork.jpg',(35,295,1135,420))
panel('02 / RESPONSIVE ORIGINAL READER',web,(1200,295,1165,420))
panel('03 / COMPLETE ORIGINAL ESSAY · A5 EDITORIAL PROOF','previews/book.jpg',(35,745,1135,740))
panel('04 / THREE LAYERS · COLOR GRADE · RESET',artifact,(1200,745,1165,740))
panel('05 / FIVE ORIGINAL EXCERPT CARDS · 1080 × 1440','previews/carousel.jpg',(35,1515,2330,450))
frames='previews/discovery-frames.jpg' if (p/'previews/discovery-frames.jpg').exists() else 'previews/VIDEO_STORYBOARD.jpg'
panel('06 / 24s TEASER · 60s DISCOVERY · 45s FEED · 120s PORTRAIT + LANDSCAPE',frames,(35,1995,1530,425))
d.rectangle((1595,1995,2365,2420),fill=dark)
for i,line in enumerate(['07 / ACTUAL DELIVERY','19 original paragraphs','76 source files preserved','72 reference tasks reviewed','5 edits / author voice pending','Print proofs / concept artwork','Source label 06 → public 09']):d.text((1620,2020+i*52),line,font=font(25,3),fill=accent if i==0 else paper)
d.text((50,2460),'THE ORIGINAL ENDING',font=font(24,3),fill=dark)
text_block(d,'“Chỉ biết rằng tôi luôn tìm thấy chúng, và chúng cũng luôn tìm thấy tôi.”',(50,2510),2300,font(48,2),dark)
d.text((50,2630),'The dinner is imagined. The rooftop animal is a visual metaphor, absent from the manuscript.',font=font(24,3),fill=dark)
save(board,p/'previews/product-board.jpg');board.save(p/'previews/PROJECT_BOARD.pdf','PDF',resolution=180,title=meta['title']+' — Production Board',author='Jason / .json')
print('Chapter 09 print, platform artwork and board updated')
