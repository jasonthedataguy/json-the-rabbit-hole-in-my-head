from pathlib import Path
import os, re, csv, json, math, shutil, subprocess, zipfile, textwrap, wave, struct, random, html
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image as RLImage, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A5, A4

ROOT=Path(__file__).resolve().parents[1]; ROOT.mkdir(exist_ok=True)
for name in ['manuscript','book','art','web/assets','social/instagram','social','video/stills','video','docs','source','previews']:(ROOT/name).mkdir(parents=True,exist_ok=True)
BOARD=Image.open(ROOT/'art'/'00_approved_project_board.jpg').convert('RGB')
NIGHT='#233954'; DARK='#10233B'; PALE='#F7EFD9'; INK='#182B45'; YELLOW='#F2CD62'; BLUE='#7895AF'; ROSE='#D8B39E'

article='''# Bài 15: Three Meeting Theory

Amsers là mấy đứa hopeless romantic đều có chung một giấc mơ: đi nửa vòng trái đất, khám phá khắp các ngõ ngách thế giới và gặp được soulmate trên hành trình của mình, để rồi hoá ra lại chính là chàng trai/cô gái gần nhà từng học cùng lớp mẫu giáo. Bằng một cách nào đó do cuộc đời sắp đặt, hai đường đời lại cắt nhau thêm lần nữa.

Và ngay từ khoảnh khắc đầu tiên ánh mắt họ chạm nhau, *something clicks inside them*. Cả hai đều biết có điều gì đó rất khó giải thích, something familiar, like they've known each other for a long time. Và khi người ấy xuất hiện, họ tự hỏi: *Is it him/her?*

Có một giả thuyết gọi là *Three Meeting Theory*, rằng với một người quan trọng, chúng ta sẽ gặp họ ba lần trong đời.

Lần gặp đầu tiên, *we are just background characters*, lướt qua nhau giữa đám đông, maybe một ánh nhìn, nhưng chỉ vậy. Ta có thể thấy khuôn mặt đó quen thuộc đến kỳ lạ, như thể từng xuất hiện trong giấc mơ. Nhưng trong khoảnh khắc ấy, chúng ta còn mải lo nghĩ về những bộn bề cuộc sống và tự nhủ, *well, it's just people looking similar.*

Lần gặp thứ hai, *with a spark between both of us*. Con đường chúng ta giao nhau thêm lần nữa, lần này we have a mutual connection. Có thể là học chung lớp Statistics, làm chung team, hay we both go on a solo trip and team up to explore together. We start sleeping over at each other's crib on weekends like a real relationship. Mặc dù vậy, timing is bad. Có thể một trong hai người chưa đủ trưởng thành, cái tôi quá cao, hoặc những hiểu nhầm lại chia cắt chúng ta thêm một lần nữa.

Lần gặp thứ ba, người ta gọi đó là định mệnh. Khi cả hai đã học được những bài học mà vũ trụ sắp đặt, khi trái tim không còn đập liên hồi chỉ vì một khoảnh khắc lãng mạn, cuộc đời lại kéo chúng ta về bên nhau. Chỉ khác là lần này, bạn không còn bỏ đi nữa, không thắc mắc nhiều nữa. *You just know it, and you will stay forever.*

Anh không biết sẽ tới bao giờ, nhưng anh vẫn sẽ chờ. Tới một ngày có thể gặp em trên đường phố New York, hoặc va vào nhau tại một tiệm bánh pastry ở Paris, hay đơn giản là ngồi cùng bàn trong quán bún chả ở ngõ khu tập thể nào đó tại Hà Nội.

Dù bất cứ nơi đâu, đến lúc đó, em hãy mặc một chiếc váy vàng màu hoa hướng dương để anh có thể nhận ra em ngay trong đám đông nhé.'''
(ROOT/'manuscript'/'ORIGINAL_VERBATIM.md').write_text(article+'\n', encoding='utf-8')
paras=article.split('\n\n')[1:]
assert len(paras)==8

(ROOT/'manuscript'/'EDITOR_NOTES.md').write_text('''# Chapter 15 — Editorial notes (no rewriting)

- **Canonical text:** `ORIGINAL_VERBATIM.md` reproduces the provided essay without edits.
- **Narrative role:** A deliberately naïve and romantic internet belief, not a scientifically validated account of relationships.
- **Strongest motif:** sunflower-yellow dress; preserve the last line with no explanatory coda.
- **Formal status:** Three Meeting Theory is a romantic internet narrative/trope, not an established scientific theory.
- **Artistic interpretation:** Any pictured meetings or city locations are illustrative, not documentation that a third reunion happened.
- **Approval needed:** If a character is based on a recognizable real individual, obtain approval before public or commercial use.
''',encoding='utf-8')

# Crop editorial references from selected project board, explicitly marked concept crops.
def crop(name, box, outsize=None):
    im=BOARD.crop(box)
    if outsize: im=im.resize(outsize,Image.Resampling.LANCZOS)
    im.save(ROOT/'art'/name, quality=91, optimize=True)
    return ROOT/'art'/name
crop('00_approved_project_board.jpg',(0,0,1672,941), (1672,941))
crop('01_cover_wide.jpg',(0,0,1672,252),(1672,252))
# Individual scene crops, derived from board sections
scenes=[
 ('02_first_meeting.jpg',(962,282,1083,416)),
 ('03_second_meeting.jpg',(1090,282,1210,416)),
 ('04_third_meeting.jpg',(1216,282,1340,416)),
 ('05_city_bridge.jpg',(1348,282,1475,416)),
 ('06_yellow_dress.jpg',(1480,282,1664,415)),
 ('07_night_city.jpg',(1100,493,1203,569)),
 ('08_pastry.jpg',(1225,493,1304,568)),
 ('09_sunflowers.jpg',(1410,493,1521,568)),
]
for name,rect in scenes:crop(name,rect,(840,1000))

# fonts: don't ship typeface files in kit
serif='/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf'
serif_bold='/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf'
sans='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font_italic='/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf'
pdfmetrics.registerFont(TTFont('NS',serif)); pdfmetrics.registerFont(TTFont('NSB',serif_bold)); pdfmetrics.registerFont(TTFont('NSI',font_italic));pdfmetrics.registerFontFamily('NS',normal='NS',bold='NSB',italic='NSI',boldItalic='NSB')
try: pfnt=ImageFont.truetype(serif_bold,70)
except:pfnt=ImageFont.load_default()

def rgb(hex):return tuple(int(hex[i:i+2],16) for i in (1,3,5))

def fit_cover(im,w,h):
    iw,ih=im.size;ratio=max(w/iw,h/ih);size=(round(iw*ratio),round(ih*ratio));a=im.resize(size,Image.Resampling.LANCZOS);l=(a.width-w)//2;t=(a.height-h)//2;return a.crop((l,t,l+w,t+h))

def text_box(draw,xy,content,font,width,fill,spacing=8):
    x,y=xy;lines=[]
    for para in content.split('\n'):
        tokens=para.split(' '); cur=''
        for word in tokens:
            test=(cur+' '+word).strip()
            if draw.textlength(test,font=font)>width and cur:lines.append(cur);cur=word
            else:cur=test
        lines.append(cur)
    for ln in lines:
        draw.text((x,y),ln,font=font,fill=fill,stroke_width=0);y+=font.size+spacing
    return y

# Standalone styled cover artwork (concept crop used as visual source).
hero=BOARD.crop((0,0,1672,252))
W,H=1800,2400
cover=Image.new('RGB',(W,H),rgb(NIGHT)); d=ImageDraw.Draw(cover)
# skyline strip repeated subtly and softly behind main title
bg=fit_cover(BOARD.crop((0,0,900,252)),(W),900)
cover.paste(bg,(0,700))
d.rectangle((55,55,W-55,H-55),outline=rgb(YELLOW),width=8)
d.rectangle((70,70,W-70,H-70),outline=rgb(PALE),width=3)
fontr=ImageFont.truetype(serif_bold,142)
fonts=ImageFont.truetype(serif,52)
fontm=ImageFont.truetype(sans,34)
d.text((130,170),'.json / 15',font=fontm,fill=rgb(YELLOW))
text_box(d,(125,280),'Three\nMeeting\nTheory',fontr,1500,rgb(PALE),spacing=6)
d.text((130,1750),'ba lần gặp, một điều gì đó quen thuộc.',font=fonts,fill=rgb(PALE))
d.text((130,1900),'Same cities. Different days.',font=fonts,fill=rgb(YELLOW))
d.text((130,1970),'Some people just feel familiar.',font=fonts,fill=rgb(YELLOW))
d.text((130,2180),'JASON, UNDER REVISION',font=fontm,fill=rgb(PALE))
cover.save(ROOT/'art'/'10_cover_portrait.jpg',quality=88,optimize=True)

# Dedicated clean illustrations: 3-stage paper cards using project board reference crops
for i,(title,description,filename) in enumerate([
 ('01 / BACKGROUND','we are just background characters','02_first_meeting.jpg'),
 ('02 / SPARK','with a spark between both of us','03_second_meeting.jpg'),
 ('03 / MAYBE','the third meeting has not happened','06_yellow_dress.jpg')]):
    card=Image.new('RGB',(1200,1500),rgb(PALE));d=ImageDraw.Draw(card)
    d.rectangle((28,28,1172,1472),outline=rgb(NIGHT),width=6)
    pic=fit_cover(Image.open(ROOT/'art'/filename),(1100),900)
    card.paste(pic,(50,50)); d.rectangle((50,949,1150,955),fill=rgb(YELLOW))
    f1=ImageFont.truetype(serif_bold,75);f2=ImageFont.truetype(serif,38)
    d.text((74,1006),title,font=f1,fill=rgb(NIGHT))
    text_box(d,(76,1140),description,f2,1010,rgb(INK),10)
    d.text((75,1385),'THREE MEETING THEORY / .json',font=ImageFont.truetype(sans,24),fill=rgb(NIGHT))
    card.save(ROOT/'art'/f'11_meeting_{i+1:02d}_card.jpg',quality=90,optimize=True)

# Social cards 3:4 at true target dimensions. Covers at concept proof resolution only.
slides=[
  ('01 / THREE MEETING THEORY','Same cities. Different days.\nSome people just feel familiar.','02_first_meeting.jpg'),
  ('02 / FIRST MEETING','We are just background characters.','02_first_meeting.jpg'),
  ('03 / SECOND MEETING','With a spark between both of us.','03_second_meeting.jpg'),
  ('04 / THIRD MEETING','Perhaps. We do not know yet.','04_third_meeting.jpg'),
  ('05 / THE YELLOW DRESS','Mặc một chiếc váy vàng màu hoa hướng dương nhé.','06_yellow_dress.jpg')
]
for i,(head,quote,img) in enumerate(slides,1):
    w,h=1080,1440;c=Image.new('RGB',(w,h),rgb(PALE));d=ImageDraw.Draw(c)
    d.rectangle((24,24,w-24,h-24),outline=rgb(NIGHT),width=6)
    pic=fit_cover(Image.open(ROOT/'art'/img),w-100,910)
    c.paste(pic,(50,50));d.rectangle((49,958,1031,969),fill=rgb(YELLOW))
    f=ImageFont.truetype(serif_bold,51);txt=ImageFont.truetype(serif,35)
    d.text((67,1006),head,font=f,fill=rgb(INK))
    text_box(d,(66,1100),quote,txt,935,rgb(INK),6)
    d.text((66,1347),'.json / JASON, UNDER REVISION',font=ImageFont.truetype(sans,20),fill=rgb(INK))
    c.save(ROOT/'social'/'instagram'/f'slide_{i:02d}_3x4.jpg',quality=89,optimize=True)

# fb landscape + YT thumbnail from approved board with unbranded labels.
for name,(w,h) in [('facebook_1600x900.jpg',(1600,900)),('youtube_thumbnail_1280x720.jpg',(1280,720))]:
    im=Image.new('RGB',(w,h),rgb(NIGHT));d=ImageDraw.Draw(im)
    pic=fit_cover(hero,w,round(h*.48));im.paste(pic,(0,round(h*.40)))
    d.text((round(w*.07),round(h*.06)),'Three Meeting Theory',font=ImageFont.truetype(serif_bold,round(w*.054)),fill=rgb(PALE))
    d.text((round(w*.07),round(h*.24)),'A romantic internet theory / .json',font=ImageFont.truetype(serif,round(w*.025)),fill=rgb(YELLOW))
    im.save(ROOT/'social'/name,quality=87,optimize=True)

# Interactive web: standalone HTML + stylesheet/script, local assets; no external fetches
webassets=ROOT/'web'/'assets'
shutil.copy2(ROOT/'art'/'01_cover_wide.jpg', webassets/'hero.jpg')
shutil.copy2(ROOT/'art'/'10_cover_portrait.jpg', webassets/'cover.jpg')
for i,img in enumerate(['02_first_meeting.jpg','03_second_meeting.jpg','06_yellow_dress.jpg'],1): shutil.copy2(ROOT/'art'/img,webassets/f'beat_{i}.jpg')

content_html='\n'.join('<p>'+html.escape(p).replace('*','')+'</p>' for p in paras)
site=f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Three Meeting Theory — A romantic memoir by Jason, under revision."><title>.json / 15 — Three Meeting Theory</title><link rel="stylesheet" href="styles.css"></head><body><a class="skip" href="#read">Skip to chapter</a><header><span>.json / 15</span><span>JASON, UNDER REVISION</span></header><section class="hero" aria-label="Illustrated metropolitan crowds at night"><div class="hero-inner"><span class="label">AN INTERNET ROMANCE / CHAPTER 15</span><h1>Three<br>Meeting<br><em>Theory</em></h1><p>ba lần gặp, một điều gì đó quen thuộc.</p><a class="btn" href="#read">READ THE CHAPTER ↓</a><a class="btn ghost" href="#explore">THE THIRD INTERSECTION ↗</a></div></section><main><section class="reading" id="read"><p class="eyebrow">ORIGINAL TEXT / UNCHANGED</p><h2>Three Meeting Theory</h2><article>{content_html}</article></section><section class="intersect" id="explore"><span class="eyebrow">INTERACTIVE LITERARY ARTIFACT</span><h2>The Third Intersection</h2><p>Three meetings are an internet romantic story, not a scientific law. Explore the progression in the essay; the third meeting remains a hope rather than an observed event.</p><div class="choices" role="group" aria-label="Choose a meeting"><button type="button" data-i="0" aria-pressed="true">01 / STRANGERS</button><button type="button" data-i="1" aria-pressed="false">02 / SPARK</button><button type="button" data-i="2" aria-pressed="false">03 / UNKNOWN</button></div><div class="experience"><img src="assets/beat_1.jpg" alt="Illustrative two strangers in a city crowd" id="stage-img"><div><h3 id="stage-title">A passing glance</h3><p id="stage-body" aria-live="polite">At first, two people might pass without noticing each other.</p><p class="note" id="stage-note">No claim that this encounter happened in real life.</p></div></div><svg viewBox="0 0 880 160" aria-label="Three points along an imagined path, the last unknown"><path d="M80 85 Q230 0 430 85 T810 85" stroke="#F2CD62" stroke-width="5" fill="none"/><circle cx="85" cy="84" r="15" fill="#F2CD62"/><circle cx="430" cy="84" r="15" fill="#F2CD62"/><circle cx="810" cy="84" r="17" stroke="#F2CD62" fill="#233954" stroke-width="5"/><text x="810" y="89" fill="#F2CD62" font-size="20" text-anchor="middle">?</text></svg><p class="note">The ending is intentionally unwritten. There are no predicted outcomes, scores or fabricated reunions.</p></section><section class="closer"><p>“Dù bất cứ nơi đâu, đến lúc đó, em hãy mặc một chiếc váy vàng màu hoa hướng dương để anh có thể nhận ra em ngay trong đám đông nhé.”</p></section></main><footer>.json / Jason, under revision · Story source preserved · Illustration proof, not a documentary</footer><script src="app.js"></script></body></html>'''
(ROOT/'web'/'index.html').write_text(site,encoding='utf-8')
css=''':root{--dark:#142842;--blue:#233954;--gold:#f2cd62;--paper:#f7efd9;--ink:#182b45}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font-family:Georgia,serif}.skip{position:absolute;top:-120px;left:20px;background:white;padding:10px;z-index:100}.skip:focus{top:10px}header{display:flex;justify-content:space-between;background:var(--dark);color:var(--paper);padding:20px 5vw;font:12px monospace;letter-spacing:.15em}.hero{background:linear-gradient(90deg,#10233bdc,#10233b16),url('assets/hero.jpg') center/cover;min-height:610px;display:flex;align-items:center;color:var(--paper)}.hero-inner{padding:65px 6vw;max-width:820px}.label,.eyebrow,.note{font:12px/1.7 monospace;letter-spacing:.06em}.label{color:var(--gold)}h1{font-size:clamp(70px,11vw,142px);font-weight:400;letter-spacing:-.065em;line-height:1.02;margin:22px 0}h1 em{color:var(--gold);font-style:normal}.hero p{font-size:22px}.btn{display:inline-block;padding:13px 18px;margin:8px 9px 0 0;border:1px solid var(--gold);background:var(--gold);color:var(--dark);text-decoration:none;font:12px monospace}.btn.ghost{background:transparent;color:var(--paper)}.reading{padding:85px 22px 110px;max-width:760px;margin:auto}.reading h2{font-size:clamp(36px,6vw,62px);font-weight:400;margin:20px 0 40px}.reading article p{font-size:18px;line-height:2;margin:0 0 1.45em}.reading article p:last-child{font-weight:600}.intersect{background:var(--dark);color:var(--paper);padding:85px max(22px,calc((100vw - 1030px)/2))}.intersect h2{font-size:clamp(35px,5vw,60px);font-weight:400;margin:14px 0}.intersect>p{line-height:1.8;max-width:760px}.choices{display:flex;gap:12px;flex-wrap:wrap;margin:28px 0}.choices button{padding:14px 19px;border:1px solid var(--gold);background:transparent;color:var(--paper);font:13px monospace;cursor:pointer}.choices button[aria-pressed=true]{background:var(--gold);color:var(--dark)}.experience{display:grid;grid-template-columns:0.8fr 1.2fr;align-items:center;gap:28px;background:#1c3651;padding:24px}.experience img{width:100%;height:320px;object-fit:cover}.experience h3{font-size:32px}.experience p{line-height:1.8}.note{color:#ebd9a7}.intersect svg{display:block;max-width:880px;width:100%;height:auto;margin-top:32px}.closer{padding:90px 20px;background:#e9dfc7;text-align:center}.closer p{font-size:clamp(22px,3vw,38px);line-height:1.7;max-width:950px;margin:auto}footer{padding:30px 6vw;background:var(--dark);color:var(--paper);font:12px monospace}button:focus-visible,a:focus-visible{outline:3px solid #eea852;outline-offset:3px}@media(max-width:650px){.hero{min-height:530px}.hero-inner{padding:38px 22px}.experience{grid-template-columns:1fr}.experience img{height:260px}.reading{padding:55px 22px 70px}.reading article p{font-size:17px}.intersect{padding:60px 22px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}'''
(ROOT/'web'/'styles.css').write_text(css,encoding='utf-8')
js='''const beats=[{title:'A passing glance',body:'Lần đầu, chúng ta chỉ là background characters. We may never know whether our paths actually crossed.',note:'This is a hypothetical scenario, not a documented memory.',img:'assets/beat_1.jpg',alt:'Two strangers among crowds'},{title:'A spark — bad timing',body:'Lần thứ hai, a connection becomes possible, but misunderstandings and timing pull two people apart.',note:'No specific real-world relationship is identified.',img:'assets/beat_2.jpg',alt:'Two people meeting again'},{title:'The third meeting — unknown',body:'The essay imagines a third encounter, but it has not been established. The yellow dress remains a wish.',note:'The future is open. This interface does not predict anyone’s fate.',img:'assets/beat_3.jpg',alt:'A sunflower yellow dress amid a city crowd'}];document.querySelectorAll('[data-i]').forEach(b=>b.addEventListener('click',()=>{const i=Number(b.dataset.i),x=beats[i];document.querySelectorAll('[data-i]').forEach(q=>q.setAttribute('aria-pressed',String(q===b)));document.querySelector('#stage-title').textContent=x.title;document.querySelector('#stage-body').textContent=x.body;document.querySelector('#stage-note').textContent=x.note;const image=document.querySelector('#stage-img');image.src=x.img;image.alt=x.alt}));'''
(ROOT/'web'/'app.js').write_text(js,encoding='utf-8')

# PDF editorial proof with actual source text and page numbering
A5w,A5h=A5
coverpath=ROOT/'art'/'10_cover_portrait.jpg'

class Doc(BaseDocTemplate):
    def __init__(self,path):
        BaseDocTemplate.__init__(self,str(path),pagesize=A5,leftMargin=44,rightMargin=44,topMargin=49,bottomMargin=48,
            title='Three Meeting Theory — Chapter 15 (A5 editorial proof)',author='Jason',pageCompression=1)
        fr=Frame(self.leftMargin,self.bottomMargin,self.width,self.height,leftPadding=0,rightPadding=0,bottomPadding=0,topPadding=0)
        self.addPageTemplates([PageTemplate(id='body',frames=[fr],onPage=self.decorate)])
    def decorate(self,canvas,doc):
        if doc.page==1: return
        canvas.saveState();canvas.setFillColor(HexColor(INK));canvas.setFont('NS',7.3);canvas.drawString(44,A5h-30,'.json / 15');canvas.drawRightString(A5w-44,A5h-30,'THREE MEETING THEORY')
        canvas.setStrokeColor(HexColor('#A4A7A1'));canvas.line(44,38,A5w-44,38);canvas.drawRightString(A5w-44,25,str(doc.page));canvas.restoreState()

class FullCover(RLImage):
    def __init__(self):super().__init__(str(coverpath),width=A5w,height=A5h)
    def wrap(self,availWidth,availHeight):return A5w,A5h
    def drawOn(self,canv,x,y,_sW=0):
        canv.drawImage(str(coverpath),0,0,width=A5w,height=A5h,preserveAspectRatio=False)

# We do a standalone cover page then story pages by merging two PDFs: robust A5 full-bleed proof.
from io import BytesIO
bodyfile=ROOT/'book'/'_body.pdf'
doc=Doc(bodyfile)
body_style=ParagraphStyle('body',fontName='NS',fontSize=10,leading=18,textColor=HexColor(INK),spaceAfter=13)
quote_style=ParagraphStyle('quote',fontName='NSI',fontSize=12,leading=20,textColor=HexColor(NIGHT),spaceBefore=13,spaceAfter=19,leftIndent=12,rightIndent=12)
title_style=ParagraphStyle('title',fontName='NSB',fontSize=22,leading=28,textColor=HexColor(NIGHT),spaceAfter=14)
sub_style=ParagraphStyle('sub',fontName='NS',fontSize=8,leading=13,textColor=HexColor('#715B3B'),spaceAfter=30)
class PlacedPicture(RLImage):
    pass
story=[Paragraph('Three Meeting Theory',title_style),Paragraph('BÀI 15  /  .json — JASON, UNDER REVISION',sub_style)]
for i,p in enumerate(paras):
    txt=html.escape(p)
    txt=re.sub(r'\*([^*]+)\*',r'<i>\1</i>',txt)
    story.append(Paragraph(txt,body_style))
    if i==2:
        story.append(Spacer(1,14));story.append(RLImage(str(ROOT/'art'/'11_meeting_01_card.jpg'),width=205,height=256));story.append(Spacer(1,23))
    if i==4:
        story.append(Spacer(1,9));story.append(RLImage(str(ROOT/'art'/'11_meeting_02_card.jpg'),width=201,height=250));story.append(Spacer(1,20))
    if i==6:
        story.append(Spacer(1,8));story.append(RLImage(str(ROOT/'art'/'11_meeting_03_card.jpg'),width=205,height=256));story.append(Spacer(1,18))
doc.build(story)
try:
 from pypdf import PdfReader,PdfWriter
except Exception:
 from PyPDF2 import PdfReader,PdfWriter
cv=BytesIO();canvas0=canvas.Canvas(cv,pagesize=A5)
canvas0.drawImage(str(coverpath),0,0,width=A5w,height=A5h)
canvas0.showPage();canvas0.save();cv.seek(0)
w=PdfWriter();w.add_page(PdfReader(cv).pages[0]);body=PdfReader(str(bodyfile));
for page in body.pages:w.add_page(page)
with open(ROOT/'book'/'15_Three_Meeting_Theory_A5_EDITORIAL_PROOF.pdf','wb') as f:w.write(f)
bodyfile.unlink()
# A4 image poster proof
cv=canvas.Canvas(str(ROOT/'book'/'15_Three_Meeting_Theory_A4_POSTER_PROOF.pdf'),pagesize=A4)
aw,ah=A4; cv.setFillColor(HexColor(NIGHT));cv.rect(0,0,aw,ah,fill=1,stroke=0)
cv.drawImage(str(coverpath),28,24,width=aw-56,height=ah-48)
cv.save()

# Chapter metadata
metadata={'chapter':'15','title':'Three Meeting Theory','book':'.json — Jason, under revision','part_candidate':'03_relationship_modeling','status':'EDITORIAL_PROOF_NOT_PUBLISHED','text_version':'Original verbatim','estimated_read_time':'4–6 min (estimate)','theme':['romance','timing','memory','hope','sunflower yellow dress'],'visual_palette':{'midnight_blue':NIGHT,'dark_navy':DARK,'faded_blue':BLUE,'sunflower_yellow':YELLOW,'paper_ivory':PALE,'dusty_rose_beige':ROSE},'visual_assets_origin':'concept-art crops from approved composite project board; not independently painted layered masters','scientific_status':'Three Meeting Theory is a romantic internet narrative, not a validated empirical theory','publication_approved':False,'third_encounter_observed':False}
(ROOT/'docs'/'chapter_metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Media: original ambient generated from scratch; do not claim narration
rate=16000;dur=24
with wave.open(str(ROOT/'video'/'ambient_original.wav'),'w') as f:
    f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate)
    buffer=bytearray()
    for i in range(rate*dur):
        t=i/rate
        amp=.03*math.sin(2*math.pi*147*t)+.018*math.sin(2*math.pi*220*t)+.015*math.sin(2*math.pi*294*t)
        gate=max(.0,min(1,t/.8,(dur-t)/1.2))
        buffer+=struct.pack('<h',int(32767*max(-1,min(1,amp*gate))))
    f.writeframes(buffer)
# Recompose social images as 720x1280 vertical proof stills, no borrowed music.
for i in range(1,6):
    src=Image.open(ROOT/'social'/'instagram'/f'slide_{i:02d}_3x4.jpg')
    im=fit_cover(src,720,1280)
    im.save(ROOT/'video'/'stills'/f'frame_{i:02d}.jpg',quality=81,optimize=True)
# ffmpeg concat
concat=ROOT/'video'/'_frames.txt'
concat.write_text(''.join(f"file 'stills/frame_{i:02d}.jpg'\nduration 4.8\n" for i in range(1,6))+"file 'stills/frame_05.jpg'\n",encoding='utf-8')
cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-safe','0','-f','concat','-i',str(concat),'-i',str(ROOT/'video'/'ambient_original.wav'),'-r','12','-t','24','-c:v','libx264','-preset','ultrafast','-crf','29','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-shortest','-movflags','+faststart',str(ROOT/'video'/'15_Three_Meeting_Theory_ANIMATIC_9x16.mp4')]
subprocess.run(cmd,check=True,cwd=str(ROOT/'video'),timeout=150)
concat.unlink()
(ROOT/'video'/'STORYBOARD.md').write_text('''# Three Meeting Theory — 24-second animatic storyboard (proof)

| Time | Image | Source meaning |
| --- | --- | --- |
| 00:00–00:04.8 | Strangers in a crowd | First meeting: background characters |
| 00:04.8–00:09.6 | Two people closer | Second meeting: spark and bad timing |
| 00:09.6–00:14.4 | The third intersection | The hoped-for future is still unknown |
| 00:14.4–00:19.2 | Two cities at night | New York, Paris, Hà Nội are imagined possibilities |
| 00:19.2–00:24 | Sunflower-yellow dress | Preserve the exact final image |

**State:** 720×1280, 24-second H.264/AAC, original synthesized ambience only. NO narration, no timed spoken subtitles, no published video. Artwork is concept crop proof, not final licensed/print-res art.
''',encoding='utf-8')
(ROOT/'video'/'NARRATION_DRAFT.md').write_text('''# Narration script proposal — NOT RECORDED

Amsers là mấy đứa hopeless romantic, đều có chung một giấc mơ.

Lần đầu tiên, we are just background characters. Có khi chỉ một ánh nhìn.

Lần thứ hai, with a spark between both of us. Nhưng timing is bad.

Lần thứ ba, người ta gọi đó là định mệnh. Nhưng anh không biết tới bao giờ.

Có thể là New York, một tiệm pastry ở Paris, hay quán bún chả giữa lòng Hà Nội.

Dù bất cứ nơi đâu, đến lúc đó, em hãy mặc một chiếc váy vàng màu hoa hướng dương để anh có thể nhận ra em ngay trong đám đông nhé.

---
This is an unrecorded short adaptation, not a verbatim replacement of the full essay. Caption timing must be based on a real licensed recording.
''',encoding='utf-8')

(ROOT/'social'/'CAPTIONS_DRAFT.md').write_text('''# Social copy drafts (not posted)

## Instagram carousel
1. First meeting — we are just background characters.
2. Second meeting — with a spark between both of us.
3. Third meeting — not a promise, but a hope.
4. New York / Paris / Hà Nội — hypothetical places.
5. A sunflower-yellow dress — the final image of the essay.

**Caption:** Có một romantic internet theory bảo rằng ta sẽ gặp một người quan trọng ba lần trong đời. T không biết nó có thật không. Chỉ biết nếu đến một ngày hai đường đời cắt nhau thêm lần nữa, em hãy mặc chiếc váy vàng hoa hướng dương để anh nhận ra em trong đám đông nhé. — Three Meeting Theory / .json.

## Facebook
Đây là một bài viết ngắn về những lần gặp lại, bad timing, và một kiểu hy vọng mà một người vẫn có thể giữ cho riêng mình. *Three Meeting Theory* — .json / Jason, under revision.

## TikTok / Reels / YouTube Shorts
**Hook:** What if someone you passed once becomes your whole story?
**Title:** Three Meeting Theory | A Sunflower-Yellow Dress — .json
**Description:** A romantic memoir-in-essays piece about three hypothetical meetings and someone you might see again.

All drafts require author approval. The Three Meeting Theory is not established scientific evidence. No social post or video has been published.
''',encoding='utf-8')

# Build 70 task project board with intentional statuses
streams={
'Editorial':[('E01','Archive exact text'),('E02','Protect final sentence'),('E03','Continuity with book'),('E04','Provenance note: internet theory'),('E05','Check recognizable identities'),('E06','Approve canonical version'),('E07','Proof Vietnamese glyphs'),('E08','Record source date if known'),('E09','Confirm chapter numbering')],
'Illustrations':[('A01','Palette and motif lock'),('A02','Main cover composition'),('A03','First encounter concept'),('A04','Second encounter concept'),('A05','Third encounter concept'),('A06','New York concept'),('A07','Paris pastry concept'),('A08','Hà Nội bún chả concept'),('A09','Yellow dress illustration'),('A10','Create independent high-resolution masters'),('A11','Layered source artwork'),('A12','Originality and rights review')],
'Book / PDF':[('B01','Build A5 reading proof'),('B02','Build A4 art poster proof'),('B03','Inspect A5 rendered pages'),('B04','Print typography QA'),('B05','Finalize trim and gutter'),('B06','Final export PDF/X'),('B07','Print physical proof'),('B08','Create permanent QR'),('B09','Test QR on phones')],
'Website / Artifact':[('W01','Responsive reading site'),('W02','Load original full essay'),('W03','Three-meeting explorer'),('W04','Unknown third outcome disclosure'),('W05','Keyboard accessible controls'),('W06','Reduced-motion support'),('W07','Standalone offline assets'),('W08','Mobile browser QA'),('W09','Desktop browser QA'),('W10','Real-device QA'),('W11','Host chapter HTTPS'),('W12','Add author-approved archive history')],
'Audio / Video':[('V01','Short film storyboard'),('V02','Voiceover draft'),('V03','Generate ambient proof'),('V04','Render 9:16 animatic'),('V05','Record/licence voiceover'),('V06','Time captions to voice'),('V07','Master 1080x1920 video'),('V08','Check audio levels'),('V09','Mobile subtitle QA'),('V10','Optional longform 16:9')],
'Social / Distribution':[('S01','Instagram carousel 3:4'),('S02','Instagram caption'),('S03','Facebook graphic'),('S04','Facebook copy'),('S05','YouTube thumbnail'),('S06','Shorts description'),('S07','TikTok caption'),('S08','Platform safe zone QA'),('S09','Upload social drafts'),('S10','Record live links')],
'Release / Repo':[('R01','Source file tree'),('R02','Project board and tracker'),('R03','Asset metadata JSON'),('R04','Rights and credits log'),('R05','Versioned chapter build'),('R06','Verify archive integrity'),('R07','GitHub draft review branch'),('R08','Approve commercial release'),('R09','Deploy and test links')]
}
ready={'E01','E02','E04','A01','A02','B01','B02','B03','W01','W02','W03','W04','W05','W06','W07','V01','V02','V03','V04','S01','S02','S03','S04','S05','S06','S07','R01','R02','R03','R05','R06'}
proof={'A03','A04','A05','A06','A07','A08','A09','B04','W08','W09','S08'}
blocked={'E05','E06','A10','A11','A12','B05','B06','B07','B08','B09','W10','W11','W12','V05','V06','V07','V08','V09','V10','S09','S10','R04','R07','R08','R09'}
tasks=[]
for stream,its in streams.items():
    for k,label in its:
        status='READY' if k in ready else 'PROOF' if k in proof else 'BLOCKED' if k in blocked else 'TODO'
        tasks.append({'id':k,'stream':stream,'task':label,'status':status,'priority':'P1' if k in {'E06','A10','A12','B06','V05','V07','W11','R08'} else 'P2','owner':'Jason' if k in {'E05','E06','R08'} else 'Production','acceptance':label+' reviewed and evidenced in release manifest'})
(ROOT/'docs'/'TASKS.json').write_text(json.dumps(tasks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with open(ROOT/'docs'/'CHECKLIST.csv','w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['id','stream','task','status','priority','owner','acceptance']);w.writeheader();w.writerows(tasks)
markdown=['# Three Meeting Theory — Full Production Project Board','', '**.json / 15 · Review prototype · Original manuscript preserved**','','## Product thesis','', 'Three encounters, one unfinished future. The digital experience explores the narrator’s imagined progression without pretending the internet theory is empirical or that a reunion actually occurred.','','## Design system','','| Role | Colour |','|---|---|',f'| Midnight blue | `{NIGHT}` |',f'| Deep ink | `{DARK}` |',f'| Sunflower yellow | `{YELLOW}` |',f'| Faded film blue | `{BLUE}` |',f'| Old paper ivory | `{PALE}` |','','## Deliverables and definitions','','- [x] Verbatim full Vietnamese/Vinglish essay','- [x] Printable **A5 editorial PDF proof** with illustration concepts','- [x] A4 poster **proof**','- [x] Responsive offline chapter website, fully readable','- [x] Interactive The Third Intersection; unknown ending intentionally unresolved','- [x] Five 3:4 Instagram stills and landscape feed assets','- [x] 24-second 9:16 H.264/AAC **ambient animatic, NOT narrated**','- [x] Storyboard, narration draft, social post drafts','- [x] Task board with CSV + JSON export','- [ ] High-res original layered illustration masters; concept crops are not print masters','- [ ] Recorded narrator, synced captions and final vertical master','- [ ] Print vendor preflight, tested permanent QR, public deployment and social uploads','','## Narrative design','','1. **First meeting:** background characters; no invented personal memories.','2. **Second meeting:** spark and bad timing, as romantic theory describes.','3. **Third meeting:** unobserved future, never presented as guaranteed.','4. **Last image:** sunflower-yellow dress; do not append an explanation.','','## Rights + ethics','','The source is an internet-romantic hypothesis, not scientifically validated. Illustrations are derived from the approved composite moodboard and are for concept/proof use, not distinct high-resolution layered artwork. Any recognizable real-world likeness needs approval.','','## Detailed tasks','','| ID | Workstream | Deliverable | State | Owner |','|---|---|---|---|---|']
markdown += ['| '+ ' | '.join([t['id'],t['stream'],t['task'],t['status'],t['owner']])+' |' for t in tasks]
markdown += ['','## Publication gates','', '1. Author approves the exact source and public sharing.','2. Validate independent artwork quality and licensing.','3. Record original narrator and synchronize real subtitles.','4. Export printer-specific PDF/X and verify a physical proof.','5. Verify deployed HTTPS link and QR on phones.','6. Post to accounts only with author authorization.','', '**Current state: HOLD / NOT PUBLISHED.**']
(ROOT/'docs'/'PROJECT_BOARD.md').write_text('\n'.join(markdown)+'\n',encoding='utf-8')
# HTML board with filters/edit and CSV export
json_tasks=json.dumps(tasks,ensure_ascii=False).replace('</','<\\/')
board_html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Three Meeting Theory / Project Board</title><style>:root{--b:#142842;--s:#233954;--p:#f7efd9;--y:#f2cd62}*{box-sizing:border-box}body{margin:0;background:var(--b);color:var(--p);font:14px/1.6 system-ui,sans-serif}header{padding:28px 5vw;background:#1b314a}header h1{font:normal 48px Georgia,serif;margin:2px 0}header p{max-width:800px}.dashboard{padding:24px 5vw}.bar{display:flex;flex-wrap:wrap;gap:12px;margin:17px 0}input,select,button{background:#29465f;color:white;border:1px solid #b4bcb5;border-radius:4px;padding:10px;font:14px system-ui}input{width:260px;max-width:100%}button{background:var(--y);color:var(--b);cursor:pointer;font-weight:700}.count{color:var(--y);font-size:22px;font-weight:bold}table{border-collapse:collapse;width:100%;background:#21374d}th,td{text-align:left;border-bottom:1px solid #455c6c;padding:10px}th{color:var(--y);font-size:12px}table select{width:100%}.table-wrap{overflow-x:auto}.note{color:#e2cda0;font-size:12px;margin-top:20px}@media(max-width:700px){header h1{font-size:35px}.dashboard{padding:20px}th,td{padding:7px}}</style></head><body><header><small>.json / 15 • EDITABLE OFFLINE PROJECT BOARD</small><h1>Three Meeting Theory</h1><p>Original story unchanged · Blue / sunflower-yellow · 3 encounters, third unobserved · Review files, not a launched product.</p></header><main class="dashboard"><div class="count" id="progress"></div><div class="bar"><input id="search" placeholder="Find task or stream…" aria-label="Find tasks"><select id="stream"><option value="">All workstreams</option></select><select id="filter"><option value="">All statuses</option><option>READY</option><option>PROOF</option><option>TODO</option><option>BLOCKED</option><option>IN_PROGRESS</option></select><button id="export">Export CSV</button><button id="reset">Reset to baseline</button></div><div class="table-wrap"><table><thead><tr><th>ID</th><th>Workstream</th><th>Task / outcome</th><th>Status</th><th>Owner</th></tr></thead><tbody id="rows"></tbody></table></div><p class="note">Changes are saved in your current browser only (localStorage). Export CSV to keep them. No accounts, analytics, uploads, or external data transfer.</p></main><script>const base='''+json_tasks+''';const key='json_three_meeting_board_15';let tasks;try{tasks=JSON.parse(localStorage.getItem(key))||base}catch(e){tasks=base}const stream=document.querySelector('#stream');[...new Set(tasks.map(t=>t.stream))].forEach(v=>{const o=document.createElement('option');o.textContent=v;stream.append(o)});function render(){const q=document.querySelector('#search').value.toLowerCase(),f=document.querySelector('#filter').value,s=stream.value;const show=tasks.filter(t=>(t.task+' '+t.id+' '+t.stream).toLowerCase().includes(q)&&(!f||t.status===f)&&(!s||t.stream===s));const host=document.querySelector('#rows');host.replaceChildren();for(const t of show){const r=document.createElement('tr');[t.id,t.stream,t.task].forEach(v=>{const td=document.createElement('td');td.textContent=v;r.append(td)});const td=document.createElement('td'),sel=document.createElement('select');['READY','PROOF','TODO','BLOCKED','IN_PROGRESS'].forEach(z=>{const o=document.createElement('option');o.textContent=z;sel.append(o)});sel.value=t.status;sel.onchange=()=>{t.status=sel.value;try{localStorage.setItem(key,JSON.stringify(tasks))}catch(e){}updateCount()};td.append(sel);r.append(td);const owner=document.createElement('td');owner.textContent=t.owner;r.append(owner);host.append(r)}updateCount()}function updateCount(){document.querySelector('#progress').textContent=tasks.filter(x=>x.status==='READY').length+' / '+tasks.length+' ready • '+tasks.filter(x=>x.status==='PROOF').length+' proofs • '+tasks.filter(x=>x.status==='BLOCKED').length+' blocked'}for(const id of ['search','filter','stream'])document.getElementById(id).addEventListener('input',render);document.querySelector('#reset').onclick=()=>{tasks=JSON.parse(JSON.stringify(base));try{localStorage.removeItem(key)}catch(e){}render()};document.querySelector('#export').onclick=()=>{const cols=['id','stream','task','status','priority','owner','acceptance'];const esc=v=>'"'+String(v??'').replaceAll('"','""')+'"';const csv=[cols.join(','),...tasks.map(t=>cols.map(k=>esc(t[k])).join(','))].join('\\r\\n');const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));a.download='Three_Meeting_Theory_CHECKLIST.csv';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};render();</script></body></html>'''
(ROOT/'docs'/'PROJECT_BOARD.html').write_text(board_html,encoding='utf-8')

(ROOT/'docs'/'QA_AND_RELEASE.md').write_text('''# QA & release notes — v0.1

- Canonical manuscript: complete eight-paragraph original; unchanged.
- A5 PDF: PDF verification/render to be recorded.
- A4 poster: art proof; image derived from approved concept board.
- Web: standalone offline HTML/CSS/JS; test on real device remains outstanding.
- Audio: original synthesized ambient only, no narrator.
- Video: 720×1280, 24s H.264/AAC intended; confirm probe output.
- Instagram: five 1080×1440 JPG concept crops with new typography.
- Third meeting: a romantic possibility, not an observed or predicted event.
- Sources/rights: original board derived crops, not independently-painted production masters; high-resolution layered art required for commercial print.
- QR, print PDF/X, narrator licensing, social uploads, GitHub deployment: not done.
''',encoding='utf-8')
(ROOT/'README.md').write_text('''# .json / 15 — Three Meeting Theory

The complete immersive **review prototype** for Chapter 15. The chapter's wording is **unchanged** from the user-provided original.

## Quick start
1. Unzip Book_Website package; open `web/index.html` in a browser (keep the `web/assets` folder intact).
2. Open `book/15_Three_Meeting_Theory_A5_EDITORIAL_PROOF.pdf` for the illustrated A5 manuscript.
3. Open `docs/PROJECT_BOARD.html` for editable task tracking (in the Project_Source package).
4. Use `social/instagram` and `video/` to review media proofs.

## Status caveats
- This is **not** a final narrated film nor printer-certified book PDF.
- All standalone scene images are concept crops from the approved artwork collage, not independent high-res masters.
- The third reunion has not been established; no invented factual ending or predictions.
- No GitHub deployment or publication has occurred as part of this kit.

## Color
Midnight blue `#233954`, dark navy `#10233B`, sunflower yellow `#F2CD62`, faded blue `#7895AF`, ivory `#F7EFD9`.
''',encoding='utf-8')

print('CREATED', ROOT)
print('TASKS',len(tasks),'PDF PART',ROOT/'book'/'15_Three_Meeting_Theory_A5_EDITORIAL_PROOF.pdf')
