"""Chapter 16 print proof and actual product board. Run after build_products.py.

Requires Pillow, ReportLab and PyMuPDF; optional web screenshots come from QA.
"""
from pathlib import Path
import html,json,math,sys
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
from common import read_json,paragraphs
from build_products import font,lines,text_block,save,print_extras
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A5
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Image as PDFImage
import pymupdf as fitz

p=ROOT/'chapters/dating-102';meta=read_json(p/'chapter.json');scenes=read_json(p/'artwork/scenes/index.json')
dark=meta['palette']['dark'];paper=meta['palette']['paper'];accent=meta['palette']['accent']
# Retain the complete stage-and-conversation composition in the homepage hero.
hero=Image.new('RGB',(1600,960),dark)
scene=ImageOps.contain(Image.open(p/'artwork/scenes/01-lecture.jpg'),hero.size,Image.Resampling.LANCZOS)
hero.paste(scene,((hero.width-scene.width)//2,(hero.height-scene.height)//2));save(hero,p/'artwork/exports/hero.jpg')
width,height=A5
style=ParagraphStyle('Text',fontName='Chapter',fontSize=10.5,leading=15.5,spaceAfter=10,textColor=HexColor(dark),allowWidows=0,allowOrphans=0,splitLongWords=False)
label=ParagraphStyle('Label',parent=style,fontName='Label',fontSize=8,leading=12)
heading=ParagraphStyle('Heading',parent=style,fontName='ChapterItalic',fontSize=32,leading=36)
def frame(c,doc):
    c.setFillColor(HexColor(paper));c.rect(0,0,width,height,fill=1,stroke=0)
    c.setFillColor(HexColor(dark));c.setFont('Label',6)
    c.drawString(31,height-24,'.json / JASON, UNDER REVISION');c.drawRightString(width-31,height-24,'16 / DATING 102')
    c.drawString(31,18,'A5 EDITORIAL PROOF');c.drawRightString(width-31,18,str(doc.page))
def art(path,maxh):
    im=Image.open(p/path);w=min(width-72,maxh*im.width/im.height)
    return PDFImage(str(p/path),width=w,height=w*im.height/im.width)
flow=[Paragraph('CHAPTER 16',label),Spacer(1,12),Paragraph('Dating 102',heading),Paragraph('THE WRONG CURRENCY',label),Spacer(1,20),art('artwork/scenes/01-lecture.jpg',300),Spacer(1,25),Paragraph('Rituals are not intimacy.',style),Paragraph('Jason, under revision',label),PageBreak()]
for i,text in enumerate(paragraphs(p/'source/approved.md')):
    if i==8:flow.append(PageBreak())
    flow.append(Paragraph(html.escape(text),style))
    if i==2:
        flow.extend([PageBreak(),Paragraph('THE QUESTION',label),Spacer(1,45),art('artwork/scenes/02-curiosity.jpg',340),Spacer(1,35),Paragraph('“Why do you think that?”',heading),Paragraph('Minh họa ý niệm từ bảng thiết kế được cung cấp.',label),PageBreak()])
flow.extend([Spacer(1,20),art('artwork/scenes/05-picnic.jpg',210)])
flow.extend([PageBreak(),Paragraph('Ghi chú nguồn',heading),Paragraph('Biên tập / kiểm tra ngày 17.10.2026',label)])
notes=[
('Bản văn','Mười đoạn văn giữ nguyên lời tác giả. Chỉ chuẩn hóa định dạng từ nội dung dán. Ngày viết ban đầu và tuổi tác giả khi viết chưa được cung cấp. Các ghi chú này nằm ngoài bài gốc.'),
('Dân số','Korea.net công bố số làm tròn 2024 là 0,75 con/phụ nữ (27/02/2025). Korea Policy Briefing công bố 2025 là 0,80 (26/08/2026). Bản gốc ghi 0.748 không kèm năm; giữ nguyên thay vì đổi ngầm thành số mới.'),
('Việt Nam','Cục Thống kê ghi tổng tỷ suất sinh năm 2025 là 1,93 con/phụ nữ, ở cấp quốc gia. UNFPA mô tả cơ hội dân số đồng thời với già hóa nhanh. Các số đo không tự chứng minh động cơ hẹn hò gây ra suy giảm dân số.'),
('COVID và gene','WHO ghi nhận miễn dịch suy giảm theo thời gian; có kháng thể không đồng nghĩa COVID trở thành cúm mùa. MedlinePlus mô tả nguy cơ bệnh lặn ở con của cha mẹ có quan hệ họ hàng. Điều đó không chứng minh chuỗi suy luận từ lựa chọn địa vị đến diệt vong trong bài.'),
('Giới hạn','Chưa xác định nguồn gốc câu chuyện Boston. Curiosity được dùng như ẩn dụ; phần tương tác không xếp hạng con người. Các khái quát về giới và lời tiên đoán diệt vong thuộc lập luận của người kể, không được xác lập như kết luận khoa học.')]
note_style=ParagraphStyle('Note',parent=style,fontSize=9.5,leading=13,spaceAfter=8)
for title,text in notes:flow.append(Paragraph('<b>'+title+'.</b> '+html.escape(text),note_style))
links=[('Korea.net / 2024','https://www.korea.net/NewsFocus/Society/view?articleId=267262'),('Korea Policy Briefing / 2025','https://www.korea.kr/news/policyNewsView.do?newsId=148970652'),('Vietnam NSO / 2025','https://www.nso.gov.vn/tin-tuc-thong-ke/2026/01/thong-cao-bao-chi-ve-tinh-hinh-dan-so-lao-dong-viec-lam-quy-iv-va-nam-2025/'),('UNFPA Vietnam','https://vietnam.unfpa.org/en/topics/population-matters-2'),('WHO / COVID-19 vaccines','https://www.who.int/news-room/questions-and-answers/item/coronavirus-disease-(covid-19)-vaccines'),('MedlinePlus / Genetics','https://medlineplus.gov/ency/article/002048.htm')]
flow.append(Spacer(1,10))
for title,url in links:flow.append(Paragraph(f'<link href="{html.escape(url,quote=True)}" color="#0b2b32"><u>{html.escape(title)}</u></link>',label))
doc=SimpleDocTemplate(str(p/'book/chapter-A5-proof.pdf'),pagesize=A5,rightMargin=36,leftMargin=36,topMargin=46,bottomMargin=43,title='Dating 102 — The Wrong Currency',author='Jason')
doc.build(flow,onFirstPage=frame,onLaterPages=frame)
print_meta={**meta,'subtitle':'THE WRONG CURRENCY / Rituals are not intimacy.'}
print_extras(p,print_meta,scenes)
document=fitz.open(p/'book/chapter-A5-proof.pdf');thumbs=[]
for page in document:
    pix=page.get_pixmap(matrix=fitz.Matrix(1.5,1.5));im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);im.thumbnail((295,420));thumbs.append(im)
sheet=Image.new('RGB',(4*315,math.ceil(len(thumbs)/4)*450),'#d3d1c6')
for i,im in enumerate(thumbs):sheet.paste(im,((i%4)*315+10,(i//4)*450+10))
save(sheet,p/'previews/book.jpg')

board=Image.new('RGB',(2400,2700),paper);d=ImageDraw.Draw(board)
d.rectangle((0,0,2400,260),fill=dark)
d.text((55,30),'.json / CHAPTER 16 / PRODUCTION BOARD',font=font(27,3),fill=accent)
d.text((55,90),'Dating 102',font=font(100,2),fill=paper)
d.text((1000,110),'THE WRONG CURRENCY',font=font(44,3),fill=accent)
d.text((1000,175),'Status → ordinary details → curiosity → currency',font=font(28,3),fill=paper)
def panel(title,path,box):
    x,y,w,h=box;d.rectangle((x,y,x+w,y+h),fill=dark);d.text((x+18,y+14),title,font=font(25,3),fill=paper)
    im=ImageOps.contain(Image.open(p/path).convert('RGB'),(w-30,h-75));board.paste(im,(x+(w-im.width)//2,y+57))
web='previews/web-1440.png' if (p/'previews/web-1440.png').exists() else 'artwork/exports/hero.jpg'
interactive='previews/interactive-1440.png' if (p/'previews/interactive-1440.png').exists() else 'artwork/scenes/02-curiosity.jpg'
panel('01 / ORIGINAL ART → SIX DOCUMENTED CROPS','previews/artwork.jpg',(35,295,1135,420))
panel('02 / RESPONSIVE CHAPTER READER',web,(1200,295,1165,420))
panel(f'03 / COMPLETE ESSAY · {len(document)}-PAGE A5 PROOF','previews/book.jpg',(35,745,1135,740))
panel('04 / CURRENCY EXCHANGE · EIGHT PERSPECTIVES',interactive,(1200,745,1165,740))
panel('05 / FIVE VERBATIM EXCERPT CARDS · 1080 × 1440','previews/carousel.jpg',(35,1515,2330,450))
frames='previews/discovery-frames.jpg' if (p/'previews/discovery-frames.jpg').exists() else 'previews/carousel.jpg'
panel('06 / 24s TEASER · 60s DISCOVERY · 45s FEED · 120s PORTRAIT + LANDSCAPE',frames,(35,1995,1530,425))
d.rectangle((1595,1995,2365,2420),fill=dark)
y=2020
for line in ['07 / DELIVERY STATES','10 unchanged body paragraphs','13 untouched reference files','5 film edits; author voice pending','Print: editorial proofs','Art: supplied concept crops','QR deferred / no social uploads']:
    d.text((1620,y),line,font=font(26 if y==2020 else 24,3),fill=accent if y==2020 else paper);y+=52
d.text((50,2460),'THE QUESTION',font=font(22,3),fill=dark)
d.text((50,2510),'“If you love someone, just try to know who they are.”',font=font(49,2),fill=dark)
d.text((50,2615),'Dated source notes sit outside the original essay. No people scoring or extinction forecast.',font=font(25,3),fill=dark)
save(board,p/'previews/product-board.jpg')
board.save(p/'previews/PROJECT_BOARD.pdf','PDF',resolution=180.0,title='Dating 102 — Production Board',author='Jason / .json')
print('Chapter 16 extras:',len(document),'A5 pages; JPG and PDF board')
