from pathlib import Path
from reportlab.lib.pagesizes import A5, A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,PageBreak,Spacer,Image as RLImage,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from xml.sax.saxutils import escape
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
for name,path in [('NotoSerif','/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf'),('NotoSerifBold','/usr/share/fonts/truetype/noto/NotoSerif-SemiBold.ttf'),('NotoSans','/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf')]:pdfmetrics.registerFont(TTFont(name,path))
W,H=A5; paper=HexColor('#F6F1E5');navy=HexColor('#0A223A');blue=HexColor('#23548C')
body=ParagraphStyle('body',fontName='NotoSerif',fontSize=9.65,leading=16.0,textColor=navy,spaceAfter=9,alignment=4)
title=ParagraphStyle('title',fontName='NotoSerifBold',fontSize=29,leading=37,textColor=navy,spaceAfter=18)
strap=ParagraphStyle('strap',fontName='NotoSans',fontSize=8,leading=12,textColor=blue,spaceAfter=10)
source=(ROOT/'manuscript/proposed-edit.md').read_text().split('\n\n')
text=[v for v in source[1:] if v.strip()]
pdf=ROOT/'book/03_For_Mother_Russia_A5_EDITORIAL_PROOF.pdf'
def page(canvas,doc):
 canvas.saveState();canvas.setFillColor(paper);canvas.rect(0,0,W,H,fill=1,stroke=0)
 if doc.page>1:
  canvas.setStrokeColor(blue);canvas.setLineWidth(.5);canvas.line(31,H-30,W-31,H-30)
  canvas.setFont('NotoSans',7);canvas.setFillColor(blue)
  canvas.drawString(32,H-23,'.json / 03 — FOR MOTHER RUSSIA')
  canvas.drawRightString(W-31,19,str(doc.page).zfill(2))
 canvas.restoreState()

doc=SimpleDocTemplate(str(pdf),pagesize=A5,rightMargin=37,leftMargin=37,topMargin=42,bottomMargin=40,title='For Mother Russia — A5 Editorial Proof',author='Jason / under revision')
items=[]
# Full bleed cover as a flowable within page (slim margin, no special cover engine needed)
cover=RLImage(str(ROOT/'art/00_CHAPTER_POSTER_A4.jpg'),width=W-86,height=(W-86)*2500/1900);items.extend([Spacer(1,8),cover,PageBreak()])
items += [Paragraph('03 / MODEL OF A PLACE I HAVE NEVER BEEN',strap),Paragraph('For Mother Russia',title),Paragraph('Về những giấc mơ, ký ức mượn và một nước Nga chưa từng sống ở đó.',strap),Spacer(1,6)]
art_indices={2:'07_wood_cabin.jpg',6:'03_grandfather.jpg',11:'06_stalingrad_game_memory.jpg',20:'02_snowy_path.jpg'}
for idx,v in enumerate(text):
 if idx in art_indices:
  f=ROOT/'art'/art_indices[idx]
  im=Image.open(f); iw,ih=im.size
  flow=RLImage(str(f),width=W-84,height=(W-84)*ih/iw)
  flow.hAlign='CENTER'
  items.extend([Spacer(1,6),flow,Spacer(1,10)])
 # Keep quoted short dialogue separate with indentation through paragraph style
 pstyle=body
 if v.startswith('“') and (len(v)<140):
  pstyle=ParagraphStyle('quote'+str(idx),parent=body,fontName='NotoSerifBold',fontSize=10.1,leftIndent=18,spaceBefore=4,spaceAfter=8,textColor=blue)
 items.append(Paragraph(escape(v).replace('\n','<br/>'),pstyle))
items.extend([Spacer(1,12),Paragraph('EDITORIAL PROOF · NOT PRINTER-READY · AGE 23 IS A RECOLLECTED PERSPECTIVE',strap)])
doc.build(items,onFirstPage=page,onLaterPages=page)
# separate art print
from reportlab.pdfgen import canvas
A4w,A4h=A4
p=canvas.Canvas(str(ROOT/'book/03_For_Mother_Russia_A4_POSTER_PROOF.pdf'),pagesize=A4)
p.drawImage(str(ROOT/'art/00_CHAPTER_POSTER_A4.jpg'),0,0,width=A4w,height=A4h,mask='auto');p.showPage();p.save()
print(pdf)
