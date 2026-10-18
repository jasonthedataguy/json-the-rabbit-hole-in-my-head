#!/usr/bin/env python3
"""Reproducible local editorial proof builder. Inputs: approved concept-board image(s), unchanged essay."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from reportlab.lib.pagesizes import A5, A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as PImage, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter
import os, re, html, json, csv, wave, math, struct, random, subprocess, zipfile, textwrap, shutil
ROOT=Path(__file__).resolve().parents[1]; DATA=Path('/mnt/data')
for d in ['manuscript','book','art','web/assets','social/instagram','social','video/stills','video','docs','previews','source']: (ROOT/d).mkdir(parents=True,exist_ok=True)
INPUTS=ROOT/'source'/'inputs'  # bundled artwork board masters for offline regeneration
BOARD=Image.open(INPUTS/'paris_dreamworld_editorial_storyboard.png').convert('RGB')
PRINTBOARD=Image.open(INPUTS/'chapter_06_a_dream_in_paris.png').convert('RGB')
WEBBOARD=Image.open(INPUTS/'paris_twilight_storyboard_ui.png').convert('RGB')
SOCIALBOARD=Image.open(INPUTS/'dream_worlds_in_paris_moodboard.png').convert('RGB')
NAVY='#172B3A'; DEEP='#12283A'; AMBER='#DAB073'; CREAM='#F4EADB'; WARM='#E0A474'; INK='#263542'; BLU='#718C9D'; PAPER='#FBF4E8'
serif='/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf'
bold='/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf'
italic='/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf'
sans='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

article=r'''# 6. **Thế giới trong mơ của tôi**

Thế giới trong mơ của tôi có một điều khá kỳ lạ. Ở đó, mọi thứ dường như luôn bắt đầu từ lúc chập tối, sau giờ tan làm, và kết thúc trước khi những ánh sáng đầu tiên của ngày mới xuất hiện.

Tôi cũng chẳng biết tại sao lại như vậy. Chỉ là đôi khi, ngay giữa một khung cảnh rất đỗi bình thường, tôi lại có cảm giác như mình đang ở trong một giấc mơ, thay vì thực sự sống trong khoảnh khắc ấy.

Ngày đầu tiên đặt chân tới thành phố này, khi đang chật vật với hai chiếc vali trên tàu số 5 để tới ga Bastille gặp người bạn của mình, tôi đã có cảm giác đó.

Mọi thứ lúc ấy thật lạ. Tôi biết mình vừa đến một nơi hoàn toàn xa lạ, nhưng khung cảnh trước mắt lại có gì đó rất quen thuộc, như thể nó đã từng xuất hiện trong một giấc mơ nào đó của tôi, chứ không phải đang thực sự diễn ra.

Trên hàng ghế đối diện là hai đứa trẻ. Chúng mặc quần áo rộng thùng thình, đeo balo, chân mang những đôi giày thể thao đã sờn rách, bên cạnh là một tấm ván trượt cũ. Hai đứa trò chuyện với nhau bằng thứ ngôn ngữ mà tôi, ít nhất là trước khi tới đất nước này, đã học qua loa được một chút, nên cũng hiểu lõm bõm, chữ được chữ mất.

Đại ý là chúng đang bàn luận xem ngày mai sẽ hẹn nhau ở đâu, trước hay sau bữa ăn tối.

Một đứa trong hai đứa rút chiếc điện thoại cũ ra. Kiểu điện thoại màn hình đen trắng, có bàn phím bấm giống những chiếc điện thoại ngày xưa. Dường như mẹ cậu bé gọi tới, hỏi xem cậu đã sắp về nhà chưa, bảo rằng bà ấy đã về rồi và sẽ chuẩn bị xong bữa tối nhanh thôi.

Không hiểu sao ngay lúc ấy, trong đầu tôi lại hiện lên một khung cảnh hoàn toàn khác.

Trời đã xẩm tối. Cả gia đình cậu bé đang ngồi bên bàn ăn, cậu vừa mở cửa bước vào nhà, đặt đồ đạc xuống rồi ngồi vào chiếc ghế cạnh bố mẹ. Ánh sáng vàng từ đèn xe ngoài đường chiếu hắt lên trần căn bếp qua một khung cửa sổ nhỏ, xen lẫn tiếng còi xe và tiếng động cơ ô tô hối hả bên ngoài.

Bố mẹ hỏi cậu rằng hôm nay ở trường thế nào, có chuyện gì mới không. Cậu trả lời nhát gừng rằng mọi thứ vẫn ổn, rằng hôm nay lớp cậu có một bạn nữ mới chuyển đến, rằng hôm nay được học về lịch sử thế giới cận đại. Rồi cậu kể rằng bữa trưa ở trường hôm nay có cá hồi áp chảo, ăn kèm măng tây và cơm. Cậu cũng không quên xin phép bố mẹ rằng ngày mai, sau khi tan học, cậu sẽ đi trượt ván với lũ bạn.

Cả nhà nhanh chóng kết thúc bữa cơm tối. Mẹ bảo cậu đi tắm rửa rồi học bài, còn bố giúp mẹ dọn dẹp.

Tất cả cứ thế diễn ra trong đầu tôi, từ một cuộc điện thoại mà tôi thậm chí còn chẳng hiểu hết nội dung. Tôi không biết cậu bé có thực sự ăn cá hồi vào bữa trưa hôm ấy không, có một bạn nữ mới chuyển đến lớp không, hay bố mẹ cậu có hỏi han về ngày đi học của con mình như tôi tưởng tượng. Tôi cũng chẳng biết căn bếp nhà cậu trông như thế nào.

Nhưng không hiểu sao tôi lại hình dung ra chúng rõ ràng đến vậy.

Có một điều đặc biệt là những khung cảnh ấy luôn xuất hiện trong một gam màu ám vàng nhẹ, độ tương phản không cao, hình ảnh hơi bị nhiễu đôi chút, giống như những thước phim cũ đầu thập niên 20s.

Từ ánh đèn xe hắt lên trần nhà, căn bếp nhỏ, đến khuôn mặt của những người mà tôi chưa từng gặp, tất cả đều mang cùng một màu sắc ấy. Một thứ màu vàng hơi cũ, không thực sự rực rỡ, cũng không hẳn là u tối. Giống như tôi đang xem lại một đoạn phim đã được quay từ rất lâu, dù chẳng có ký ức nào của mình thực sự nằm trong đó.

Tôi cũng không biết mình có mối liên hệ gì với những màu sắc ấy. Tại sao khi tưởng tượng về cuộc sống của những người xa lạ, tôi lại luôn nhìn thấy chúng qua cùng một lớp màu, cùng một thứ ánh sáng.

Chỉ là sau này, khi nhìn lại những bức ảnh mình chụp và chỉnh sửa, tôi nhận ra rất nhiều trong số chúng cũng mang gam màu tương tự.

Tôi không nhớ mình đã cố tình chọn nó từ bao giờ.

Chỉ biết rằng tôi luôn tìm thấy chúng, và chúng cũng luôn tìm thấy tôi.'''
(ROOT/'manuscript'/'ORIGINAL_UNCHANGED.md').write_text(article+'\n',encoding='utf-8')
paras=article.split('\n\n')[1:]; assert len(paras)==19,len(paras)
(ROOT/'manuscript'/'EDITORIAL_NOTES.md').write_text('''# .json / 06 — Editorial guardrails

- Canonical version: `ORIGINAL_UNCHANGED.md` (unchanged, exactly as provided by author). No new dialogue or details inserted.
- Observation (train): two suitcases, Line 5 to Bastille, two children, clothes/bags/worn trainers/skateboard, fragments of French, keypad phone and inferred mother calling. Blond/brunette appearance is approved **visual characterization**, not specified in original prose.
- Imagination (kitchen): dinner dialogue, salmon/asparagus, schoolmate, family members and lighting are imagined by narrator; label clearly.
- Metaphor (rooftop rat): symbolic, original animal silhouette to suggest a cinematic Parisian vantage point. This animal **does not appear in the text** and is not a depiction of a named film character.
- Geographical care: Métro Line 5 and Bastille sign inside station. Skyline/eiffel imagery belongs to separate city/imagined viewpoint, not an actual view from the Bastille platform.
- No named tourist attraction or restaurant in Paris is a recommended visit here; images are literary illustrations.
- Original finish preserved: “Chỉ biết rằng tôi luôn tìm thấy chúng, và chúng cũng luôn tìm thấy tôi.” No new coda.
- Image proof uses crops/composites of approved concept boards, not independent layered hi-res print masters. Final commercial/print treatment requires rights review.
''',encoding='utf-8')

def rgb(x):return tuple(int(x[i:i+2],16) for i in [1,3,5])
def font(px,b=False,i=False):return ImageFont.truetype((bold if b else italic if i else serif),px)
def fit(im,w,h):
 ratio=max(w/im.width,h/im.height);s=im.resize((round(im.width*ratio),round(im.height*ratio)),Image.Resampling.LANCZOS);return s.crop(((s.width-w)//2,(s.height-h)//2,(s.width+w)//2,(s.height+h)//2))
def save_crop(name,im,xy,size=None):
 x=im.crop(xy)
 if size:x=x.resize(size,Image.Resampling.LANCZOS)
 x.save(ROOT/'art'/name,quality=90,optimize=True)
 return ROOT/'art'/name

def wrap(d,text,x,y,f,maxw,fill,line_gap=8):
 for p in text.split('\n'):
  current=''
  for tok in p.split(' '):
   s=(current+' '+tok).strip()
   if current and d.textlength(s,font=f)>maxw:
    d.text((x,y),current,font=f,fill=fill);y+=f.size+line_gap;current=tok
   else:current=s
  d.text((x,y),current,font=f,fill=fill);y+=f.size+line_gap
 return y

# Approved artwork boards, symbolic crops — no artwork input hidden.
save_crop('00_approved_storyboard.jpg',BOARD,(0,0,1672,941))
save_crop('01_rooftop_skyline.jpg',BOARD,(0,0,1672,193),(2000,600))
save_crop('02_metro_children.jpg',BOARD,(0,200,792,505),(1600,930))
save_crop('03_bastille_station.jpg',BOARD,(1320,205,1668,497),(950,800))
save_crop('04_telephone.jpg',BOARD,(415,520,616,682),(1000,880))
save_crop('05_imagined_kitchen.jpg',BOARD,(628,520,832,644),(1100,880))
save_crop('06_rooftop_afterimage.jpg',BOARD,(835,520,1066,641),(1000,850))
save_crop('07_old_photographs.jpg',BOARD,(1070,520,1270,683),(1000,840))
save_crop('08_both_children.jpg',BOARD,(205,525,410,685),(900,940))
save_crop('09_paper_print_detail.jpg',PRINTBOARD,(0,230,790,730),(1300,950))
# Extra: use actual separate print/social/website board as visual references.
save_crop('10_poster_reference.jpg',PRINTBOARD,(0,0,1672,187),(1600,360))
save_crop('11_web_reference.jpg',WEBBOARD,(0,0,1672,941),(1672,941))
save_crop('12_social_reference.jpg',SOCIALBOARD,(0,0,1672,941),(1672,941))

# Stylized portrait cover from the approved panoramic rooftop, rather than falsely claiming a photographic master.
w,h=1500,2100; out=Image.new('RGB',(w,h),rgb(NAVY));out.paste(fit(BOARD.crop((0,0,1672,194)),w,720),(0,660));d=ImageDraw.Draw(out)
d.rectangle((33,33,w-33,h-33),outline=rgb(AMBER),width=7);d.rectangle((47,47,w-47,h-47),outline=rgb(CREAM),width=2)
d.text((100,112),'.json   /   06',font=font(34,True),fill=rgb(AMBER));d.text((98,236),'Thế giới',font=font(130,True),fill=rgb(CREAM));d.text((98,390),'trong mơ',font=font(128,True),fill=rgb(CREAM));d.text((98,542),'của tôi',font=font(128,True),fill=rgb(CREAM))
d.rectangle((110,1490,1390,1497),fill=rgb(AMBER));wrap(d,'Một cuộc điện thoại, một khung cảnh,\nvà cả một thế giới hiện ra trong đầu tôi.',115,1545,font(43),1240,rgb(CREAM),18)
d.text((112,1970),'JASON, UNDER REVISION',font=font(30,True),fill=rgb(AMBER))
out.save(ROOT/'art'/'13_main_book_cover.jpg',quality=91,optimize=True)
# A4 poster independent editorial composition
PW,PH=1654,2339;po=Image.new('RGB',(PW,PH),rgb(CREAM));pdraw=ImageDraw.Draw(po)
pdraw.rectangle((24,24,PW-24,PH-24),outline=rgb(NAVY),width=8)
po.paste(fit(BOARD.crop((0,0,1672,193)),PW-130,770),(65,58));pdraw.rectangle((65,860,PW-65,875),fill=rgb(AMBER))
pdraw.text((95,975),'THẾ GIỚI',font=font(113,True),fill=rgb(NAVY));pdraw.text((95,1120),'TRONG MƠ',font=font(114,True),fill=rgb(NAVY));pdraw.text((95,1265),'CỦA TÔI',font=font(114,True),fill=rgb(NAVY))
po.paste(fit(BOARD.crop((0,200,792,505)),650,510),(85,1570));po.paste(fit(BOARD.crop((625,515,832,688)),645,510),(920,1570));pdraw.text((85,2195),'CHAPTER 06   /   JASON, UNDER REVISION',font=font(27,True),fill=rgb(NAVY))
po.save(ROOT/'art'/'14_A4_poster_master_proof.jpg',quality=89,optimize=True)
# social 5x 3:4 cards
social=[('01','Mọi thứ luôn bắt đầu lúc chập tối.', '01_rooftop_skyline.jpg'),('02','Hai đứa trẻ, một tấm ván trượt cũ.','02_metro_children.jpg'),('03','Một cuộc điện thoại. Một thế giới tưởng tượng.','04_telephone.jpg'),('04','Có những bữa tối tôi chưa từng nhìn thấy.','05_imagined_kitchen.jpg'),('05','Tôi luôn tìm thấy chúng, và chúng cũng luôn tìm thấy tôi.','06_rooftop_afterimage.jpg')]
for n,(num,caption,imgname) in enumerate(social,1):
 W,H=1080,1440;card=Image.new('RGB',(W,H),rgb(CREAM));cd=ImageDraw.Draw(card);cd.rectangle((20,20,1060,1420),outline=rgb(NAVY),width=6)
 card.paste(fit(Image.open(ROOT/'art'/imgname),980,890),(50,50));cd.rectangle((50,948,1030,961),fill=rgb(AMBER));cd.text((65,989),f'{num} / THẾ GIỚI TRONG MƠ',font=font(37,True),fill=rgb(NAVY))
 wrap(cd,caption,65,1075,font(35),950,rgb(INK),9);cd.text((65,1340),'.json / JASON, UNDER REVISION',font=ImageFont.truetype(sans,21),fill=rgb(INK))
 card.save(ROOT/'social'/'instagram'/f'slide_{n:02d}_3x4.jpg',quality=86,optimize=True)
# social cover/thumb still
for file,size in [('facebook_1600x900.jpg',(1600,900)),('youtube_thumbnail_1280x720.jpg',(1280,720))]:
 WW,HH=size;img=fit(BOARD.crop((0,0,1672,195)),WW,HH);img=img.convert('RGBA');veil=Image.new('RGBA',(WW,HH),(13,30,42,0));vd=ImageDraw.Draw(veil);vd.rectangle((0,0,WW*.48,HH),fill=(12,30,44,172));img=Image.alpha_composite(img,veil);fd=ImageDraw.Draw(img)
 fd.text((55,HH*.18),'Thế giới',font=font(int(HH*.085),True),fill=rgb(CREAM));fd.text((55,HH*.31),'trong mơ của tôi',font=font(int(HH*.078),True),fill=rgb(CREAM));fd.text((60,HH*.78),'.json / CHAPTER 06',font=font(int(HH*.035),True),fill=rgb(AMBER))
 img.convert('RGB').save(ROOT/'social'/file,quality=89,optimize=True)

# PDF: independent A5 cover + wrapped text and scene plates
for n,p in [('NotoText',serif),('NotoBold',bold),('NotoItalic',italic)]:pdfmetrics.registerFont(TTFont(n,p))
pdfmetrics.registerFontFamily('NotoText',normal='NotoText',bold='NotoBold',italic='NotoItalic',boldItalic='NotoBold')
aw,ah=A5
coverpdf=ROOT/'book'/'_cover.pdf';c=canvas.Canvas(str(coverpdf),pagesize=A5);c.drawImage(str(ROOT/'art'/'13_main_book_cover.jpg'),0,0,width=aw,height=ah);c.save()
bodypdf=ROOT/'book'/'_body.pdf'
styles={
 'tit':ParagraphStyle('tit',fontName='NotoBold',fontSize=20,leading=27,spaceAfter=16,textColor=HexColor(NAVY)),
 'tiny':ParagraphStyle('tiny',fontName='NotoBold',fontSize=8.4,leading=13,spaceAfter=22,textColor=HexColor('#976B3D')),
 'para':ParagraphStyle('para',fontName='NotoText',fontSize=9.4,leading=16.6,spaceAfter=11,textColor=HexColor(INK)),
 'note':ParagraphStyle('note',fontName='NotoItalic',fontSize=7.9,leading=11.5,spaceAfter=13,textColor=HexColor('#72685C')),
}

def decorate(c,doc):
 c.saveState();c.setFont('NotoText',7);c.setFillColor(HexColor(NAVY));c.drawString(40,ah-27,'.json / 06');c.drawRightString(aw-40,ah-27,'THẾ GIỚI TRONG MƠ CỦA TÔI');c.setStrokeColor(HexColor('#AAA095'));c.line(40,36,aw-40,36);c.drawRightString(aw-40,22,str(doc.page+1));c.restoreState()
doc=SimpleDocTemplate(str(bodypdf),pagesize=A5,leftMargin=40,rightMargin=40,topMargin=45,bottomMargin=45,title='Thế giới trong mơ của tôi — editorial proof',author='Jason')
items=[Paragraph('Thế giới trong mơ của tôi',styles['tit']),Paragraph('CHAPTER 06   /   JASON, UNDER REVISION',styles['tiny'])]
for i,p in enumerate(paras):
 text=html.escape(p).replace('\n',' ')
 items.append(Paragraph(text,styles['para']))
 if i in (4,9,14):
  photo={4:'02_metro_children.jpg',9:'05_imagined_kitchen.jpg',14:'06_rooftop_afterimage.jpg'}[i]
  items.append(Spacer(1,5));items.append(PImage(str(ROOT/'art'/photo),width=aw-83,height=143));items.append(Spacer(1,7))
  label={4:'OBSERVED / on the train',9:'IMAGINED / in an unknown kitchen',14:'AFTERIMAGE / a recurring colour'}[i]
  items.append(Paragraph(label,styles['note']))
doc.build(items,onFirstPage=decorate,onLaterPages=decorate)
writer=PdfWriter()
for pg in PdfReader(str(coverpdf)).pages:writer.add_page(pg)
for pg in PdfReader(str(bodypdf)).pages:writer.add_page(pg)
finalpdf=ROOT/'book'/'06_The_Gioi_Trong_Mo_A5_EDITORIAL_PROOF.pdf'
with open(finalpdf,'wb') as f:writer.write(f)
coverpdf.unlink();bodypdf.unlink()
# A4 printable proof (not press ready)
a4pdf=ROOT/'book'/'06_The_Gioi_Trong_Mo_A4_POSTER_PROOF.pdf';ca=canvas.Canvas(str(a4pdf),pagesize=A4);ca.drawImage(str(ROOT/'art'/'14_A4_poster_master_proof.jpg'),0,0,width=A4[0],height=A4[1]);ca.save()

# Website version: no data exports, no network, no false documentary claims
website='''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#172B3A"><title>.json / 06 — Thế giới trong mơ của tôi</title><meta name="description" content="Thế giới trong mơ của tôi — Paris, một cuộc điện thoại, và một thước phim mượn lại."><link rel="stylesheet" href="styles.css"></head><body><a class="skip" href="#read">Đọc chương</a><header><strong>.json</strong><span>JASON, UNDER REVISION / 06</span></header><main><section class="hero"><div class="hero-content"><div class="eyebrow">CHAPTER 06 / THE BORROWED REEL</div><h1>Thế giới<br>trong mơ<br>của tôi</h1><p>Một cuộc điện thoại, một khung cảnh, và cả một thế giới hiện ra trong đầu tôi.</p><a href="#read" class="btn">ĐỌC CHƯƠNG →</a><a href="#artifact" class="btn ghost">KHÁM PHÁ FILM →</a></div></section><section id="read" class="reader"><p class="eyebrow">THE ORIGINAL / UNCHANGED</p><h2>Thế giới trong mơ của tôi</h2><article id="article"></article><p class="footnote">Nguyên văn của Jason. Cảnh hai đứa trẻ trên tàu là điều anh quan sát; câu chuyện bữa tối là điều anh tưởng tượng. Con vật ngồi trên mái nhà là một ẩn dụ thị giác, không có trong bản thảo.</p></section><section id="artifact" class="artifact"><p class="eyebrow">AN INTERACTIVE LITERARY ARTIFACT</p><h2>The Borrowed Reel</h2><p>Ba lớp cùng một khoảnh khắc: điều đã quan sát, điều đã tưởng tượng, và màu phim còn sót lại.</p><div class="tabs" role="group" aria-label="Chọn lớp ký ức"><button data-layer="observed" aria-pressed="true">01 OBSERVED</button><button data-layer="imagined" aria-pressed="false">02 IMAGINED</button><button data-layer="afterimage" aria-pressed="false">03 AFTERIMAGE</button></div><div class="film"><div class="film-frame"><img id="frame-img" src="assets/observed.jpg" alt="Two children aboard a Paris train"/><div class="film-label" id="frame-label">OBSERVED / a conversation on Métro Line 5</div></div><div class="film-content"><h3 id="layer-title">The real moment</h3><p id="layer-body" role="status" aria-live="polite">Two children, worn sneakers, a skateboard, a call home. The rest is still unknown.</p><p class="warning" id="layer-note">Only details Jason says he saw or partially heard belong to the observed layer.</p><label for="grade">FILM GRADE <span id="grade-val">55%</span></label><input type="range" id="grade" min="0" max="100" value="55" step="5" aria-label="Adjust imagined sepia color grading"/><p class="warning">The slider changes the image treatment, not what actually happened.</p></div></div><div class="cards" id="cards"></div></section></main><footer>ILLUSTRATED EDITORIAL PROOF · NO REAL PHOTOGRAPHS OR RECORDED DIALOGUE · .json</footer><script src="app.js"></script></body></html>'''
(ROOT/'web'/'index.html').write_text(website,encoding='utf-8')
css='''*{box-sizing:border-box}html{scroll-behavior:smooth}:root{--navy:#172b3a;--cream:#f4eadb;--amber:#dab073}body{margin:0;font-family:Georgia,'Times New Roman',serif;color:#263542;background:var(--cream)}.skip{position:absolute;top:-100px;left:10px;padding:12px;background:white;z-index:5}.skip:focus{top:0}header{padding:16px 5vw;background:var(--navy);color:var(--cream);display:flex;justify-content:space-between;font:12px monospace;letter-spacing:.06em}header strong{font:26px Georgia,serif}.eyebrow{font:12px monospace;letter-spacing:.15em;color:#d6a667}.hero{height:min(88vh,800px);min-height:580px;background:linear-gradient(90deg,#12283ade,#12283a25),url('assets/hero.jpg') center/cover;display:flex;align-items:center;color:white}.hero-content{padding:50px 6vw;max-width:760px}.hero h1{font-weight:normal;font-size:clamp(48px,6.5vw,100px);line-height:1.13;letter-spacing:-.055em;margin:22px 0}.hero p{max-width:580px;font-size:21px;line-height:1.65}.btn{display:inline-block;padding:13px 19px;margin:12px 10px 0 0;border:1px solid var(--amber);background:var(--amber);text-decoration:none;color:var(--navy);font:12px monospace}.btn.ghost{background:transparent;color:white}.reader{max-width:810px;padding:85px 25px 115px;margin:auto}.reader h2{font-size:clamp(37px,5vw,65px);font-weight:normal;line-height:1.15}.reader article p{font-size:18px;line-height:1.92;margin-bottom:1.32em}.reader article p:last-child{font-weight:bold}.footnote{font:12px/1.75 monospace;border-top:1px solid #aaa;margin-top:35px;padding-top:20px;color:#756c62}.artifact{background:var(--navy);color:var(--cream);padding:88px max(24px,calc((100vw - 1100px)/2))}.artifact>p{line-height:1.75;max-width:860px}.artifact h2{font-size:clamp(36px,6vw,65px);font-weight:normal;margin:17px 0}.tabs{display:flex;flex-wrap:wrap;gap:10px;margin:30px 0 20px}.tabs button{padding:13px 15px;background:transparent;color:var(--cream);border:1px solid var(--amber);font:12px monospace;cursor:pointer}.tabs button[aria-pressed=true]{background:var(--amber);color:var(--navy)}button:focus-visible,a:focus-visible,input:focus-visible{outline:3px solid #f4c56d;outline-offset:4px}.film{display:grid;grid-template-columns:1.25fr .95fr;gap:27px;background:#233f4b;padding:18px;border:1px solid #ad8b68}.film-frame{position:relative;overflow:hidden;min-height:350px}.film-frame img{display:block;width:100%;height:100%;object-fit:cover;filter:sepia(.55) saturate(1.06) contrast(.97)}.film-label{position:absolute;bottom:0;left:0;right:0;background:#0c2533df;padding:16px;font:12px monospace}.film-content{padding:12px}.film-content h3{font-size:30px;font-weight:normal}.film-content p{line-height:1.8}.warning{font:12px/1.8 monospace;color:#efcfaa}.film-content label{display:flex;justify-content:space-between;font:12px monospace;margin-top:30px}.film-content input{display:block;width:100%;accent-color:var(--amber);margin-top:16px}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:17px;margin-top:30px}.cards img{height:150px;width:100%;object-fit:cover}.cards figure{margin:0;background:#213b49;padding:8px}.cards figcaption{padding:8px;font:12px/1.5 monospace}footer{padding:32px 5vw;background:#071a25;color:#d3c8bc;font:12px/1.6 monospace}@media(max-width:720px){.hero{min-height:560px}.film{grid-template-columns:1fr}.film-frame{min-height:310px}.cards{grid-template-columns:repeat(2,1fr)}.reader{padding:55px 22px}.reader article p{font-size:17px}.artifact{padding:65px 20px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}'''
(ROOT/'web'/'styles.css').write_text(css,encoding='utf-8')
for src,name in [('01_rooftop_skyline.jpg','hero.jpg'),('02_metro_children.jpg','observed.jpg'),('05_imagined_kitchen.jpg','imagined.jpg'),('06_rooftop_afterimage.jpg','afterimage.jpg')]:shutil.copyfile(ROOT/'art'/src,ROOT/'web'/'assets'/name)
for src in ['04_telephone.jpg','03_bastille_station.jpg','07_old_photographs.jpg']:shutil.copyfile(ROOT/'art'/src,ROOT/'web'/'assets'/src)
para_json=json.dumps(paras,ensure_ascii=False)
js='''const paragraphs=PARAGRAPHS;const article=document.getElementById('article');paragraphs.forEach(v=>{const p=document.createElement('p');p.textContent=v;article.append(p)});const modes={observed:{image:'assets/observed.jpg',title:'The real moment',label:'OBSERVED / Métro Line 5',body:'Two children, worn sneakers, a skateboard and a phone call Jason only partially understands.',note:'Visual appearance of one blond child and one brunette is an approved illustration choice, not recorded in the manuscript.'},imagined:{image:'assets/imagined.jpg',title:'Somewhere, a family dinner',label:'IMAGINED / an unseen kitchen',body:'School, grilled salmon, asparagus, a newly transferred classmate and light from passing cars. Jason imagines these details; he does not know if they happened.',note:'This visual is a fictional reconstruction of Jason’s imagination, not evidence about the children.'},afterimage:{image:'assets/afterimage.jpg',title:'A recurring shade of yellow',label:'AFTERIMAGE / a familiar colour',body:'Low contrast, slight grain and amber light recur in scenes he imagines and photographs he later edits.',note:'The rooftop animal is a symbolic illustrator’s motif, not part of the factual story.'}};let selected='observed';function drawMode(mode){selected=mode;const x=modes[mode];document.querySelectorAll('[data-layer]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.layer===mode)));const img=document.getElementById('frame-img');img.src=x.image;img.alt=x.title;document.getElementById('frame-label').textContent=x.label;document.getElementById('layer-title').textContent=x.title;document.getElementById('layer-body').textContent=x.body;document.getElementById('layer-note').textContent=x.note;gradeImage()}document.querySelectorAll('[data-layer]').forEach(b=>b.addEventListener('click',()=>drawMode(b.dataset.layer)));const slider=document.getElementById('grade');function gradeImage(){let v=Number(slider.value);document.getElementById('grade-val').textContent=v+'%';document.getElementById('frame-img').style.filter=`sepia(${(v*.009).toFixed(2)}) saturate(${(1+v*.005).toFixed(2)}) contrast(${(1.13-v*.0025).toFixed(2)}) brightness(${(1.02-v*.0005).toFixed(2)})`}slider.addEventListener('input',gradeImage);drawMode('observed');const more=[['assets/04_telephone.jpg','The phone call / observed'],['assets/03_bastille_station.jpg','Métro / observed'],['assets/07_old_photographs.jpg','A color remembered / afterimage']];const el=document.getElementById('cards');more.forEach(([src,alt])=>{const f=document.createElement('figure');const i=document.createElement('img');i.src=src;i.loading='lazy';i.alt=alt;const cap=document.createElement('figcaption');cap.textContent=alt;f.append(i,cap);el.append(f)});'''.replace('PARAGRAPHS',para_json)
(ROOT/'web'/'app.js').write_text(js,encoding='utf-8')

# Video storyboard and scripts
(ROOT/'video'/'STORYBOARD.md').write_text('''# Chapter 06 — A Borrowed Reel: 24-second ambient animatic proof

| Time | Visual beat | Type |
|---|---|---|
| 00–04 | Paris roof at dusk, a small original rat silhouette looking across city | Symbolic art, not source event |
| 04–08 | Two children (one blond, one brunette) in Métro Line 5 | Observation / visual-character choice |
| 08–12 | Old monochrome phone and a call from home | Observed/inferred from limited French |
| 12–16 | Family at dinner in a yellow-lit kitchen | Narrator's imagination only |
| 16–20 | Rooftop afterimage, yellow color | Recurring subjective image |
| 20–24 | Dark city and the quiet last line | Metaphor, no documentary claim |

**Proof format:** 720×1280, 24 s H.264 video + original synthesized stereo ambient. No spoken narration, no timed spoken subtitles, no external copyrighted film footage. Future narrated version requires an authorized recording and true caption synchronization.\n''',encoding='utf-8')
(ROOT/'video'/'NARRATION_DRAFT.md').write_text('''# Voiceover — unrecorded draft (not the original essay)

Mọi thứ trong mơ của tôi thường bắt đầu lúc chập tối.

Ngày đầu tới Paris, tôi kéo hai chiếc vali trên tàu số năm về Bastille. Đối diện là hai đứa trẻ và một tấm ván trượt cũ.

Một cuộc điện thoại từ mẹ. Một bữa cơm tối mà tôi chưa từng nhìn thấy. Nhưng trong đầu tôi, căn bếp ấy lại rõ ràng như một đoạn phim.

Có lẽ bởi vậy mà khi nhìn lại những bức ảnh của mình, tôi vẫn thấy cùng một thứ ánh sáng vàng hơi cũ.

Tôi luôn tìm thấy chúng, và chúng cũng luôn tìm thấy tôi.

**Status:** draft script; user has not approved or recorded this text. This is not included as a real voice in the current video.\n''',encoding='utf-8')
beats=[(0,4,'Mọi thứ bắt đầu lúc chập tối'),(4,8,'Hai đứa trẻ trên tàu số 5'),(8,12,'Một cuộc điện thoại từ nhà'),(12,16,'Một căn bếp tôi chưa từng nhìn thấy'),(16,20,'Một lớp màu vàng hơi cũ'),(20,24,'Tôi luôn tìm thấy chúng…')]
def srt(t):h=int(t//3600);m=int((t%3600)//60);s=int(t%60);ms=int(round((t-int(t))*1000));return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
(ROOT/'video'/'VISUAL_BEAT_CAPTIONS_NOT_SYNCED_TO_VOICE.srt').write_text(''.join(f'{i}\n{srt(a)} --> {srt(b)}\n{t}\n\n' for i,(a,b,t) in enumerate(beats,1)),encoding='utf-8')
# Build complete silent/ambient visual-proof clip from images; user can replace with owned voice/sound later.
videoimages=['01_rooftop_skyline.jpg','02_metro_children.jpg','04_telephone.jpg','05_imagined_kitchen.jpg','06_rooftop_afterimage.jpg','07_old_photographs.jpg']
for i,file in enumerate(videoimages):
 image=Image.open(ROOT/'art'/file);frame=fit(image,720,1280);dd=ImageDraw.Draw(frame)
 dd.rectangle((0,0,720,120),fill=(15,35,49));dd.text((28,30),'.json / 06 — THE BORROWED REEL',font=ImageFont.truetype(sans,20),fill=rgb(CREAM))
 dd.rectangle((0,1020,720,1280),fill=(12,27,38));wrap(dd,beats[i][2],36,1070,font(31,True),645,rgb(CREAM),6)
 frame.save(ROOT/'video'/'stills'/f'beat_{i+1:02d}.jpg',quality=87,optimize=True)
# ambient tone: gentle designed original synthetic, not a real metro sound recording
sr=22050; wav=ROOT/'video'/'original_synthetic_ambience.wav';frames=24*sr
with wave.open(str(wav),'w') as fw:
 fw.setnchannels(1);fw.setsampwidth(2);fw.setframerate(sr)
 samples=bytearray();random.seed(16)
 for k in range(frames):
  t=k/sr;wind=math.sin(t*math.pi/24)**2;v=(.045*math.sin(2*math.pi*72*t)+.023*math.sin(2*math.pi*144*t)+.009*(random.random()-.5))*wind
  samples+=struct.pack('<h',max(-32767,min(32767,int(32767*v))))
 fw.writeframes(bytes(samples))
concat=ROOT/'video'/'frames.txt';concat.write_text(''.join(f"file '{(ROOT/'video'/'stills'/f'beat_{i+1:02d}.jpg').resolve()}'\nduration 4\n" for i in range(6))+f"file '{(ROOT/'video'/'stills'/'beat_06.jpg').resolve()}'\n")
outmp4=ROOT/'video'/'06_The_Gioi_Trong_Mo_ANIMATIC_9x16.mp4'
cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-safe','0','-f','concat','-i',str(concat),'-i',str(wav),'-vf','fps=24,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','26','-c:a','aac','-b:a','80k','-t','24','-movflags','+faststart',str(outmp4)]
subprocess.run(cmd,check=True)
concat.unlink()
# storyboard still contact sheet
sc=Image.new('RGB',(1480,1050),rgb(CREAM));sd=ImageDraw.Draw(sc);sd.text((30,22),'06 / THE BORROWED REEL — VIDEO BEATS',font=font(46,True),fill=rgb(NAVY))
for i in range(6):
 im=fit(Image.open(ROOT/'video'/'stills'/f'beat_{i+1:02d}.jpg'),420,650);x=30+(i%3)*480;y=105+(i//3)*430;im=fit(im,420,360);sc.paste(im,(x,y));sd.text((x,y+366),f'{i+1:02d} / {beats[i][2][:25]}',font=font(20),fill=rgb(INK))
sc.save(ROOT/'previews'/'VIDEO_STORYBOARD.jpg',quality=86)

# Metadata, markdown board and real task inventory: statuses with acceptance criteria.
stages=[('Editorial & provenance',11),('Art direction & illustration',12),('A5 print, A4 poster',9),('Website & interactive reel',12),('Video & audio',9),('Social channels',8),('QA, rights & release',11)]
tasks=[];n=0
for stream,count in stages:
 for i in range(count):
  n+=1
  title={
   'Editorial & provenance':['Preserve verbatim source','Annotate observed / imagined scenes','Keep ending unmodified','Review date/setting wording','Check use of old film reference','Review all scene captions','Approve print text','Privacy scope','Approve cover tagline','Translation accuracy','Approve canonical manuscript'],
   'Art direction & illustration':['Lock color palette','Approve symbolic rat rooftop','Approve blonde/brunette design','Create cover concept','Create Line 5 scene','Create phone scene','Create fictional kitchen scene','Create afterimage scene','Create Bastille environment','Export gallery plates','Create independent high-resolution art','Commercial artwork/likeness review'],
   'A5 print, A4 poster':['Typeset entire A5 essay','Create A5 cover','Illustrate body pages','Export A5 editorial PDF','Create A4 print poster','Inspect every PDF page','Printer bleed / trim / PDF-X','Proof-print A5 book','Sign off physical print'],
   'Website & interactive reel':['Implement offline reader','Load complete original chapter','Observed / Imagined toggle','Afterimage mode','Working film-grade slider','Mobile breakpoints','Keyboard focus / aria','Gallery assets','Browser functional QA','Public host staging','Live URL + QR verification','Production web accessibility'],
   'Video & audio':['Draft storyboard','Render 9:16 animatic proof','Original ambient audio','Create beat-caption SRT','Write narration draft','Record authorized voice','Sync actual speech subtitles','Final 1080x1920 master','Phone video QA'],
   'Social channels':['Five Instagram 3:4 cards','Facebook 16:9 art','YouTube thumbnail','Draft IG caption','Draft Facebook post','Draft video captions','Approve public posting','Publish on owned accounts'],
   'QA, rights & release':['Build source manifest','Package editable files','Split into small downloads','Verify ZIPs','Check master source text','Document proof-only status','License/provenance audit','Final author release approval','Upload vetted binaries to repo','Deploy publicly','Post-publication link audit']
  }[stream][i]
  proof_keywords=['verbatim','palette','symbolic rat','blonde/brunette','cover concept','line 5 scene','phone scene','fictional kitchen','afterimage scene','bastille environment','gallery plates','typeset','a5 cover','body pages','a5 editorial','a4 print poster','inspect every','offline reader','complete original','toggle','afterimage mode','film-grade','mobile breakpoints','keyboard focus','gallery assets','browser functional','draft storyboard','animatic proof','ambient audio','beat-caption','narration draft','instagram 3:4','facebook 16:9','youtube thumbnail','draft ig','draft facebook','draft video','source manifest','editable files','small downloads','zips','source text','proof-only']
  is_ready=any(k in title.lower() for k in proof_keywords)
  blocked_words=['approve','printer','proof-print','physical','public host','live url','production web','record authorized','sync actual','final 1080','phone video','publish','license','final author','upload vetted','deploy','post-publication','independent high-resolution']
  status='BLOCKED' if any(k in title.lower() for k in blocked_words) else ('PROOF' if is_ready and stream=='Art direction & illustration' else 'READY' if is_ready else 'TODO')
  tasks.append({'id':f'CH06-{n:03}', 'stream':stream,'task':title,'status':status,'priority':'P0' if i<3 else 'P1','acceptance':('Author explicitly approves release scope and related third-party rights.' if status=='BLOCKED' else 'File/task is present in production kit and checked, or retained as an explicit TODO.\nNo scene is represented as documentary evidence beyond the manuscript.'),'owner':'Jason + production'})
assert len(tasks)==72,len(tasks)
(ROOT/'docs'/'TASKS.json').write_text(json.dumps(tasks,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
with open(ROOT/'docs'/'CHECKLIST.csv','w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(tasks[0]));w.writeheader();w.writerows(tasks)
metadata={'book':'.json','chapter':'06','title':'Thế giới trong mơ của tôi','slug':'the-gioi-trong-mo-cua-toi','status':'PRODUCTION_PROOF_AUTHOR_REVIEW','source_text':'unchanged','observed':'Metro Line 5 to Bastille, two suitcases, two children and a call','imagined':'unknown French family at dinner','symbol':'rooftop rat at Paris dusk (visual only, not source event)','color_palette':{'navy':NAVY,'amber':AMBER,'cream':CREAM,'slate':BLU},'interactive':'The Borrowed Reel / Observed-Imagined-Afterimage','video':'24s vertical H.264/AAC proof; no narration','publication_approved':False,'artwork_print_master':False,'notes':'Stylized crops of approved image board, not independent high-resolution layered masters.'}
(ROOT/'docs'/'METADATA.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'docs'/'FULL_PROJECT_BOARD.md').write_text('''# Chapter 06 — Thế giới trong mơ của tôi / full production board

**Visual concept:** *The Borrowed Reel*: Paris rooftop at dusk with an original small rat silhouette, two French-looking kids (one blond and one brunette) on Métro Line 5, a call home, an invented dinner scene, yellow film-grain and photos. Rat rooftop motif is **not** in the original prose.

**Thesis:** a stranger’s ordinary phone call becomes an involuntary, richly imagined family life; years later the narrator recognizes the same color grade in his own photos.

## Palette
- Petrol / midnight navy `#172B3A`
- Sodium amber `#DAB073`
- Paper ivory `#F4EADB`
- Muted blue `#718C9D`
- Faded rust `#E0A474`

## Deliverables available locally
- Full unchanged manuscript and editorial notes.
- A5 illustrated editor proof, A4 poster proof.
- Approved-concept-board based scene plates and rooftop banner artwork.
- Responsive self-contained website with **Observed / Imagined / Afterimage** controls, functional film-grade slider and the complete essay.
- Five 3:4 Instagram images plus Facebook and YouTube stills.
- Twenty-four-second vertical H.264/AAC ambient-only animatic, beat captions and unrecorded narration text.
- Interactive 72-task board, task JSON/CSV, metadata, build and validation script.

## Workstream checklist
''' + '\n'.join(f'### {s} ({ct} tasks)\n'+'\n'.join(f'- [ ] {t["id"]} **{t["task"]}** — {t["status"]}' for t in tasks if t['stream']==s)+'\n' for s,ct in stages)+'\n## Release blockers\nCanonical copy approval, independent hi-res/licensed art, authorized narration and speech-correct subtitles, PDF/X print vendor preflight, QR and owned URL, real-device QA and author signoff.\n',encoding='utf-8')
(ROOT/'social'/'POSTS_DRAFT.md').write_text('''# Chapter 06 — social drafts (not posted)

**Instagram 5 slides**: 1. Mọi thứ bắt đầu lúc chập tối. 2. Hai đứa trẻ, một tấm ván trượt cũ. 3. Một cuộc điện thoại, một thế giới tưởng tượng. 4. Căn bếp tôi chưa từng nhìn thấy. 5. Những màu sắc cứ tìm thấy tôi.

**Instagram caption:** “Trên tàu số 5 tới Bastille, tôi nghe lõm bõm một cuộc điện thoại. Thế rồi trong đầu hiện ra cả một căn bếp, một gia đình và một bữa tối mà tôi chưa từng thấy. Có những ký ức không thuộc về mình — chỉ có một thứ ánh sáng quen thuộc.” — Thế giới trong mơ của tôi / .json.

**Facebook:** Một cuộc điện thoại trên Métro Paris mở ra một thế giới hoàn toàn tưởng tượng. Một chương ngắn về quan sát, người lạ và gam màu vàng thấp thoáng trong ảnh của chính mình. Website link pending approval.

**TikTok/Reels/YouTube short hook:** “Can you remember a life you never lived?”

**Disclosure:** The family dinner and rooftop rat motif are symbolic visual interpretations, not photographs or a true event. No social accounts connected, no posts published.
''',encoding='utf-8')
# interactive production board all controls wired
board_html='''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CH06 / Full Production Board</title><style>:root{--n:#172b3a;--a:#dab073;--c:#f4eadb}*{box-sizing:border-box}body{margin:0;background:var(--n);color:var(--c);font-family:system-ui,sans-serif}header{padding:26px 5vw;background:#0f2331}h1{font:normal clamp(36px,5vw,70px) Georgia,serif;margin:10px 0}p{line-height:1.65}.top{display:grid;grid-template-columns:1.4fr 1fr;gap:24px;margin:30px 5vw}.hero{width:100%;border:5px solid var(--a)}.meta{background:#1d3b4a;padding:20px}main{padding:10px 5vw 80px}.summary{display:flex;flex-wrap:wrap;gap:10px}.summary span{padding:13px;background:#244a57;border:1px solid #65868a}.tools{margin:30px 0 20px;display:flex;gap:9px;flex-wrap:wrap}input,select,button{font:14px system-ui;padding:12px;border:1px solid var(--a);background:#0e2c37;color:var(--c)}button{cursor:pointer}button:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid white}.table{display:grid;gap:8px}.item{display:grid;grid-template-columns:90px 1fr 160px;gap:16px;background:#1b3846;padding:14px;border-left:4px solid var(--a)}.item small{color:#b1c5ca}.item strong{display:block;margin-bottom:6px}.subtitle{color:var(--a);font:13px monospace}footer{padding:24px 5vw;border-top:1px solid #777;font:12px monospace}@media(max-width:820px){.top{grid-template-columns:1fr}.item{grid-template-columns:1fr}.item select{width:100%}}</style></head><body><header><small>.json / 06 • PRODUCTION PROOF / NOT PUBLISHED</small><h1>Thế giới trong mơ của tôi</h1><p>The Borrowed Reel · Offline production board with editable statuses and export</p></header><div class="top"><img class="hero" src="assets/visual_board.jpg" alt="Approved rooftop and Paris metro illustrated creative board"><div class="meta"><h2>Observed ≠ Imagined</h2><p>A Metro conversation, a family dinner created by imagination, and a recurring color palette. Keep those layers visible throughout the product.</p><p><b>All deliverables are proof-level</b> except the exact source manuscript. Narration, licensing and print preflight still require approval.</p><div class="summary" id="summary"></div></div></div><main><h2>72 production tasks</h2><p>Change statuses for your local planning session, then export CSV or JSON. Changes remain within this open page; download the export to keep them.</p><div class="tools"><input id="search" placeholder="Search title or ID" aria-label="Search tasks"><select id="stream" aria-label="Filter workstream"><option value="">All streams</option></select><select id="state" aria-label="Filter status"><option value="">All statuses</option><option>READY</option><option>PROOF</option><option>TODO</option><option>BLOCKED</option><option>IN_PROGRESS</option></select><button id="exportCSV">Export CSV</button><button id="exportJSON">Export JSON</button><button id="reset">Reset to baseline</button></div><div class="table" id="rows"></div></main><footer>Full article in manuscript/ORIGINAL_UNCHANGED.md; no background sync, no external services. Print/web/social proofs require author approval before publication.</footer><script>const baseline=__TASKS__;let tasks=baseline.map(x=>({...x}));const statusList=['READY','PROOF','TODO','BLOCKED','IN_PROGRESS'];const rows=document.getElementById('rows');const stream=document.getElementById('stream');[...new Set(tasks.map(t=>t.stream))].forEach(s=>{const opt=document.createElement('option');opt.value=s;opt.textContent=s;stream.add(opt)});function draw(){const q=document.getElementById('search').value.toLowerCase(),s=stream.value,v=document.getElementById('state').value;const subset=tasks.filter(t=>(!q||(t.id+' '+t.task+' '+t.stream).toLowerCase().includes(q))&&(!s||t.stream===s)&&(!v||t.status===v));rows.replaceChildren();subset.forEach(t=>{const line=document.createElement('div');line.className='item';const id=document.createElement('small');id.textContent=t.id;const detail=document.createElement('div');const title=document.createElement('strong');title.textContent=t.task;const sub=document.createElement('small');sub.textContent=t.stream+' • '+t.priority;detail.append(title,sub);const select=document.createElement('select');select.setAttribute('aria-label','Status for '+t.id);statusList.forEach(st=>{let op=document.createElement('option');op.value=st;op.textContent=st;select.append(op)});select.value=t.status;select.onchange=()=>{t.status=select.value;summary()};line.append(id,detail,select);rows.append(line)});summary()}function summary(){const counts={};statusList.forEach(st=>counts[st]=tasks.filter(t=>t.status===st).length);document.getElementById('summary').replaceChildren(...Object.entries(counts).filter(x=>x[1]).map(([k,v])=>{const e=document.createElement('span');e.textContent=v+' '+k;return e}))}function download(name,content,type){const blob=new Blob([content],{type});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),3000)}document.getElementById('exportJSON').onclick=()=>download('CH06_tasks_updated.json',JSON.stringify(tasks,null,2),'application/json');document.getElementById('exportCSV').onclick=()=>{const keys=['id','stream','task','status','priority','acceptance','owner'];const esc=v=>'"'+String(v).replaceAll('"','""')+'"';download('CH06_tasks_updated.csv',[keys.join(','),...tasks.map(t=>keys.map(k=>esc(t[k])).join(','))].join('\\r\\n'),'text/csv')};document.getElementById('reset').onclick=()=>{tasks=baseline.map(t=>({...t}));draw()};document.querySelectorAll('#search,#stream,#state').forEach(el=>el.addEventListener(el.tagName==='INPUT'?'input':'change',draw));draw();</script></body></html>'''.replace('__TASKS__',json.dumps(tasks,ensure_ascii=False))
(ROOT/'docs'/'PROJECT_BOARD.html').write_text(board_html,encoding='utf-8')
(ROOT/'docs'/'assets' if False else ROOT/'docs').mkdir(exist_ok=True)
(ROOT/'docs'/'assets').mkdir(exist_ok=True)
shutil.copyfile(ROOT/'art'/'00_approved_storyboard.jpg',ROOT/'docs'/'assets'/'visual_board.jpg')
# README and manifests
readme='''# .json / 06 — Thế giới trong mơ của tôi

**Complete local editorial-production proof v0.1.** Original Vietnamese/Vinglish article has not been revised.

## Product components
- `manuscript/ORIGINAL_UNCHANGED.md`: complete exact source.
- `book/06_The_Gioi_Trong_Mo_A5_EDITORIAL_PROOF.pdf`: illustrated full-text A5 reading proof.
- `book/06_The_Gioi_Trong_Mo_A4_POSTER_PROOF.pdf`: art print proof, not PDF/X.
- `art/`: approved visual-board crops and composited portrait cover; **not independent print-resolution layer masters**.
- `web/index.html` + assets + CSS/JS: offline responsive full reader and `The Borrowed Reel` interaction.
- `social/instagram/`: five 1080×1440 image cards; FB/YT artwork + draft copy.
- `video/`: 24-second 720×1280 ambient animatic, original tone, five/six stills, unrecorded voice script, *visual beat* SRT.
- `docs/PROJECT_BOARD.html`: editable 72-task production board, export CSV/JSON; open offline after extracting ZIP.
- `docs/FULL_PROJECT_BOARD.md`, `TASKS.json`, `CHECKLIST.csv`, `METADATA.json`: detailed handoff and checklist.
- `source/build_chapter.py`: reproduces the assets locally using the approved project-board PNG files located in /mnt/data.

## What is not finished
**Do not call this shipped/published, narrated, or press-ready.** There is no recorded speech or timed spoken subtitles, no actual on-location photographs, final illustration rights verification, printer-specific PDF/X, physical proof, live chapter URL/QR or published social posts. Illustrations are derived from an approved design-board concept.

## How to review
1. Extract the ZIP.
2. Open `book/*.pdf` to review A5 text and poster.
3. Open `web/index.html` to view the complete chapter and play with Observed/Imagined/Afterimage and color-grade slider.
4. Open `docs/PROJECT_BOARD.html` and export updates to CSV/JSON.
5. Open MP4 to preview the ambient animatic (no narration).
6. Approve artwork and text boundaries before any public GitHub deployment or commercial print.

## License/rights
The manuscript belongs to its author. Visual-board imagery is concept/proof artwork. No implication of affiliation with a third-party film character or soundtrack. See `manuscript/EDITORIAL_NOTES.md`.
'''
(ROOT/'README.md').write_text(readme,encoding='utf-8')
print('CH06 build finished',ROOT,'A5 pages',len(PdfReader(str(finalpdf)).pages),'task count',len(tasks))
