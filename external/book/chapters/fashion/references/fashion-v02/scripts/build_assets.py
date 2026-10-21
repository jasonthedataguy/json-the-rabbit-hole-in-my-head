from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image as RLImage,PageBreak,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A5
from xml.sax.saxutils import escape
import json,re,shutil,math,subprocess,zipfile,csv,io,os
O=Path(__file__).resolve().parents[1]
SRC=O
for d in ['content','assets/master','assets/illustrations','assets/web','book','website/assets','social/instagram','social','video/frames','docs','previews','scripts']:(O/d).mkdir(parents=True,exist_ok=True)
PALETTE={'pine':'#062F26','pink':'#F47EAC','paper':'#F5EBD8','charcoal':'#0F1E1A','denim':'#72838A','peach':'#E9A29B','dust':'#BB807C','muted':'#C7B4A6'}
FONT='/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
BOLD='/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'
SERIF='/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf'
SERIF_B='/usr/share/fonts/truetype/noto/NotoSerif-SemiBold.ttf'
assert Path(FONT).exists(),FONT
P=lambda k: tuple(bytes.fromhex(PALETTE[k].strip('#')))
F=lambda size,bold=False,serif=False: ImageFont.truetype(SERIF_B if serif and bold else SERIF if serif else BOLD if bold else FONT,size)
# Preserve existing source without revising author prose.
orig=(O/'content/original.md').read_text(); edited=(O/'content/proposed-edit.md').read_text()
para=[p.strip() for p in re.split(r'\n\s*\n',edited) if p.strip()][1:]
assert len(para)==14 and para[-1]=='Peace and love!'
inputs=[('01_COVER_SQUARE.png','ChatGPT Image Oct 16, 2026, 09_21_43 PM-1.png'),('02_BOOK_POSTER.png','ChatGPT Image Oct 16, 2026, 09_21_44 PM-2.png'),('03_MOBILE_MOCKUP.png','ChatGPT Image Oct 16, 2026, 09_21_45 PM-3.png'),('04_COLLECTOR_MOCKUP.png','ChatGPT Image Oct 16, 2026, 09_21_46 PM-4.png'),('05_WIDE_HERO.png','ChatGPT Image Oct 16, 2026, 09_21_48 PM-5.png')]
# Five source images already exist in assets/master; never overwrite them.
assert all((O/'assets/master'/p).exists() for p,_ in inputs)
art={k:Image.open(O/'assets/master'/f).convert('RGB') for k,f in [('square',inputs[0][0]),('portrait',inputs[1][0]),('mobile',inputs[2][0]),('collector',inputs[3][0]),('wide',inputs[4][0])]}
art['square'].save(O/'website/assets/cover.webp',format='WEBP',quality=89)
art['wide'].save(O/'website/assets/hero.webp',format='WEBP',quality=89)
art['portrait'].save(O/'website/assets/poster-portrait.webp',format='WEBP',quality=87)
art['collector'].save(O/'website/assets/collector.webp',format='WEBP',quality=85)
# Scene plates are crops of selected source art, never invented documentary scenes.
SCENES=[
('01','THE DROP','Dreaming of a new sneaker every winter','square',(0.00,0.31,0.38,0.84)),
('02','THE CYCLE','Another season, another reason','wide',(0.52,0.20,0.96,0.75)),
('03','THE RULEBOOK','A borrowed style is still a beginning','square',(0.55,0.23,0.98,0.79)),
('04','THE REMIX','Copy, adopt, subtract, keep','wide',(0.04,0.24,0.70,0.88)),
('05','PATINA','Stains, folds, fades and marks','square',(0.54,0.55,0.96,0.97)),
('06','HIDDEN GEM','A garment that outlived the season','portrait',(0.65,0.30,0.96,0.81))]
def cover_crop(im,target):
 w,h=im.size;tw,th=target;s=max(tw/w,th/h);n=im.resize((math.ceil(w*s),math.ceil(h*s)),Image.Resampling.LANCZOS);x=(n.width-tw)//2;y=(n.height-th)//2;return n.crop((x,y,x+tw,y+th))
def wrap_lines(text,font,maxwidth,draw):
 line='';out=[]
 for word in text.split():
  n=(line+' '+word).strip()
  if draw.textbbox((0,0),n,font=font)[2]>maxwidth and line:out.append(line);line=word
  else:line=n
 if line:out.append(line)
 return out
for num,title,subtitle,key,cr in SCENES:
 im=art[key];w,h=im.size;box=(int(cr[0]*w),int(cr[1]*h),int(cr[2]*w),int(cr[3]*h));source=im.crop(box)
 W,H=1500,1125;board=Image.new('RGB',(W,H),P('paper'));d=ImageDraw.Draw(board)
 board.paste(cover_crop(source,(W-100,795)),(50,50))
 d.rectangle((50,845,W-50,H-50),fill=P('pine'))
 d.text((85,874),'.JSON  /  FASHION  /  '+num,font=F(30,bold=True),fill=P('pink'))
 d.text((85,930),title,font=F(67,bold=True),fill=P('paper'))
 d.text((85,1021),subtitle,font=F(30),fill=P('paper'))
 board.save(O/f'assets/illustrations/scene_{num}.jpg',quality=92)
 board.resize((1000,750),Image.Resampling.LANCZOS).save(O/f'website/assets/scene_{num}.webp',quality=85)
# printable 2-page A5 opener + full 14-paragraph chapter with scene inserts
pdfmetrics.registerFont(TTFont('NotoSerif',SERIF));pdfmetrics.registerFont(TTFont('NotoSerifBold',SERIF_B));pdfmetrics.registerFont(TTFont('NotoSans',FONT))
pdfmetrics.registerFontFamily('NotoSerif',normal='NotoSerif',bold='NotoSerifBold',italic='NotoSerif',boldItalic='NotoSerifBold')
W,H=A5;pdfpath=O/'book/02_Fashion_Room_in_Revision_A5_PROOF.pdf'
style=ParagraphStyle('story',fontName='NotoSerif',fontSize=9.0,leading=15.6,spaceAfter=11.6,textColor=HexColor(PALETTE['charcoal']),allowWidows=0,allowOrphans=0)
caption=ParagraphStyle('cap',fontName='NotoSans',fontSize=7.1,leading=10.4,spaceAfter=15,textColor=HexColor(PALETTE['pine']))
heading=ParagraphStyle('heading',fontName='NotoSerifBold',fontSize=33,leading=40,spaceAfter=17,textColor=HexColor(PALETTE['pine']))
quote=ParagraphStyle('q',fontName='NotoSerifBold',fontSize=13,leading=19,spaceBefore=18,spaceAfter=18,textColor=HexColor(PALETTE['pine']))
doc=SimpleDocTemplate(str(pdfpath),pagesize=A5,leftMargin=39,rightMargin=39,topMargin=43,bottomMargin=44,allowSplitting=True,title='.json - Fashion (illustrated editorial proof)',author='Jason')
def bg(can,doc):
 can.saveState();can.setFillColor(HexColor(PALETTE['paper']));can.rect(0,0,W,H,fill=1,stroke=0)
 can.setStrokeColor(HexColor(PALETTE['pink']));can.setLineWidth(.8);can.line(35,34,W-35,34)
 can.setFillColor(HexColor(PALETTE['pine']));can.setFont('NotoSans',6.5);can.drawString(35,23,'.json  /  FASHION  /  JASON, UNDER REVISION');can.drawRightString(W-35,23,f'{doc.page:02}')
 can.restoreState()
aw=W-78
flow=[]
# cover portrait 1055x1491 consistent with book proportions, leave no huge text overlay
flow.append(RLImage(str(O/'assets/master/02_BOOK_POSTER.png'),width=aw,height=aw*1491/1055));flow.append(PageBreak())
flow.extend([Paragraph('.JSON / WORKING CHAPTER 02 / AUTHOR REVIEW',caption),Paragraph('Fashion',heading),Paragraph('Be your own label, not a hanger, my man.',quote),Spacer(1,6)])
insert={1:'scene_01.jpg',4:'scene_02.jpg',6:'scene_03.jpg',9:'scene_04.jpg',11:'scene_05.jpg',12:'scene_06.jpg'}
for i,p in enumerate(para):
 if p in ['Peace and love!'] or p.startswith('Be your own label,'):flow.append(Paragraph(escape(p),quote))
 else:flow.append(Paragraph(escape(p),style))
 if i in insert:
  fp=O/'assets/illustrations'/insert[i];flow.extend([Spacer(1,5),RLImage(str(fp),width=aw,height=aw*.75),Spacer(1,10)])
flow.extend([Spacer(1,15),Paragraph('EDITORIAL PROOF / not an approved print-production PDF. Art is a symbolic rendition of the essay.',caption)])
doc.build(flow,onFirstPage=bg,onLaterPages=bg)
# cover export social, cards with coordinated design, no pseudo-date.
main=art['square']
main.save(O/'assets/illustrations/cover_final_concept.jpg',quality=94)
CARDS=[('FASHION','Be your own label, not a hanger.','square'),('THE DROP','Một mùa đông. Một đôi sneakers.','01'),('WHOSE RULEBOOK?','Fashion làm gì có biên giới rõ như vậy.','03'),('PATINA','Dấu mark, stains và những chỗ bạc màu.','05'),('HIDDEN GEM','Hai mươi năm trong tủ đồ của bố.','06')]
for i,(title,sub,src) in enumerate(CARDS,1):
 im=art['square'] if src=='square' else Image.open(O/f'assets/illustrations/scene_{src}.jpg')
 W2,H2=1080,1440;card=Image.new('RGB',(W2,H2),P('paper'));d=ImageDraw.Draw(card)
 card.paste(cover_crop(im,(1030,1015)),(25,25))
 d.rectangle((25,1040,1055,1415),fill=P('pine'))
 d.text((65,1070),f'.JSON / 02 / {i:02}',font=F(28,True),fill=P('pink'))
 d.text((65,1125),title,font=F(64 if len(title)<13 else 49,True),fill=P('paper'))
 for n,line in enumerate(wrap_lines(sub,F(35),935,d)):d.text((65,1230+n*51),line,font=F(35),fill=P('paper'))
 d.rectangle((16,16,W2-16,H2-16),outline=P('pink'),width=9)
 card.save(O/f'social/instagram/slide_{i:02}_3x4.jpg',quality=92)
# 4:5 and 1:1 variants, wide FB/YT
cover_crop(main,(1080,1350)).save(O/'social/instagram/feed_4x5.jpg',quality=92)
cover_crop(main,(1080,1080)).save(O/'social/instagram/square_1x1.jpg',quality=91)
wide=art['wide'];cover_crop(wide,(1600,900)).save(O/'social/facebook_post_1600x900.jpg',quality=92)
cover_crop(wide,(1280,720)).save(O/'social/youtube_thumbnail_1280x720.jpg',quality=92)
# Vertical storyboard frames
for i,(title,sub,src) in enumerate(CARDS,1):
 im=art['portrait'] if i==1 else art['square'] if i==5 else Image.open(O/f"assets/illustrations/scene_{['01','01','03','05','06'][i-1]}.jpg")
 frame=Image.new('RGB',(720,1280),P('pine'));d=ImageDraw.Draw(frame)
 frame.paste(cover_crop(im,(720,1010)),(0,0));d.rectangle((0,1010,720,1280),fill=P('pine'))
 d.text((35,1030),f'FASHION / {i:02}',font=F(28,True),fill=P('pink'))
 for j,ln in enumerate(wrap_lines(sub,F(33),650,d)[:3]):d.text((35,1090+j*46),ln,font=F(33),fill=P('paper'))
 frame.save(O/f'video/frames/frame_{i:02}.jpg',quality=92)
# native HTML full reader & interactive explorer, standalone offline via local relative files
metadata={'chapter':'02','title':'Fashion','slug':'fashion','book':'.json','subtitle':'Jason, under revision','release_status':'review_proof','text_status':'proposed_edit_not_approved','source_date':None,'narrator_age':None,'poster_art_status':'user_selected_concept','palette':PALETTE,'themes':['fashion','hip-hop','streetwear','consumerism','identity','aging','patina','family'], 'estimated_read_minutes':None, 'artifacts':{'pdf':'proof','video':'animatic_without_narration','website':'offline_review','social':'drafts_not_published'},'artwork_credits':'Illustrative concept approved as a direction, final commercial rights review pending'}
(O/'docs/metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2))
(O/'website/assets/manuscript.json').write_text(json.dumps({'original':orig,'proposed':edited},ensure_ascii=False))
STEPS=[
('01 · THE DROP','Dreaming of sneakers','A new season felt like a new identity.','scene_01.webp'),
('02 · THE CYCLE','Always another collection','Fashion is a business, but Jason is describing a personal interpretation—not a causal research claim.','scene_02.webp'),
('03 · RULEBOOK','Learning the rules','Imitating others can be the beginning of a style, not its conclusion.','scene_03.webp'),
('04 · REMIX','Finding what fits','Observe, adopt, remove and keep what is yours.','scene_04.webp'),
('05 · PATINA','A garment lived in','Marks and repairs carry more meaning than a loudly repeated logo.','scene_05.webp'),
('06 · HIDDEN GEM',"A father's wardrobe",'A garment that still fits decades later is more surprising than another new drop.','scene_06.webp')]
(O/'docs/wardrobe_timeline.json').write_text(json.dumps([{'step':i+1,'name':s[0],'title':s[1],'description':s[2],'image':s[3]} for i,s in enumerate(STEPS)],ensure_ascii=False,indent=2))
html='''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#062F26"><meta name="description" content="Fashion | a .json memoir chapter about streetwear, trend cycles, and finding a style of your own."><title>.json / 02 — Fashion · immersive preview</title>
<style>:root{--pine:#062f26;--pink:#f47eac;--paper:#f5ebd8;--char:#0f1e1a;--peach:#e9a29b}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--pine);color:var(--paper);font-family:Georgia,'Times New Roman',serif}a{color:inherit}button{cursor:pointer}a:focus-visible,button:focus-visible{outline:3px solid var(--pink);outline-offset:4px}.skip{position:absolute;top:-99px;left:10px;background:var(--paper);color:var(--char);padding:12px}.skip:focus{top:10px}.top{height:65px;display:flex;align-items:center;justify-content:space-between;padding:0 5vw;gap:16px;font:12px monospace;letter-spacing:.13em}.top b{color:var(--pink)}.hero{min-height:80vh;position:relative;background:linear-gradient(90deg,rgba(6,47,38,.83) 0%,rgba(6,47,38,.37) 63%,rgba(6,47,38,.17) 100%),url('assets/hero.webp') center/cover;display:flex;flex-direction:column;justify-content:flex-end;padding:6vw 5vw 7vw;isolation:isolate}.eyebrow{font:12px monospace;letter-spacing:.17em;color:var(--pink)}.hero h1{font-family:Arial,sans-serif;letter-spacing:-.07em;font-weight:900;font-style:italic;font-size:clamp(70px,14vw,190px);color:var(--pink);line-height:.92;text-shadow:5px 6px 0 var(--pine);margin:16px 0}.hero p{max-width:630px;font-size:clamp(19px,2.2vw,30px);line-height:1.4}.nav{display:flex;gap:10px;flex-wrap:wrap;margin-top:25px}.nav a{display:inline-block;padding:13px 23px;background:var(--pink);color:var(--char);font:14px monospace;text-decoration:none}.nav a.alt{background:transparent;color:var(--paper);border:1px solid var(--pink)}.reel{height:35px;display:flex;align-items:center;padding:0 5vw;color:var(--pink);font:12px monospace;border-block:1px solid #56665a}.reader{background:var(--paper);color:var(--char);padding:70px 20px 85px}.reader .textbody{max-width:720px;margin:0 auto;font-size:18px;line-height:1.91}.textbody p{margin:0 0 1.35em}.textbody p:first-child{font-size:1.2em}.textbody p:last-child{font-style:italic}.reader h2,.explore h2,.revisit h2{font:normal clamp(29px,5vw,56px) Georgia,serif;margin:12px 0 28px}.toggle{max-width:720px;margin:auto auto 32px;display:flex;flex-wrap:wrap;gap:12px}.toggle button{border:1px solid var(--pine);padding:12px 15px;background:transparent;color:var(--char);font:12px monospace}.toggle button[aria-pressed=true]{background:var(--pine);color:var(--paper)}.explore{max-width:1100px;margin:auto;padding:75px 22px 95px}.explore>p{max-width:700px;line-height:1.8}.explorer{display:grid;grid-template-columns:1fr 1.2fr;gap:24px}.picks{display:grid;gap:9px;align-content:start}.picks button{text-align:left;border:1px solid #719185;background:#123d32;padding:15px 19px;color:var(--paper);font:14px monospace}.picks button[aria-pressed=true]{background:var(--pink);color:var(--char)}.memory{background:#0d3b30;border:1px solid var(--pink);padding:15px}.memory img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}.memory h3{font-size:27px;margin:21px 8px 5px}.memory p{margin:5px 8px 20px;line-height:1.6}.revisit{background:var(--paper);color:var(--char);padding:72px 20px}.revisit-inner{max-width:750px;margin:auto}.revisit blockquote{margin:35px 0;padding:22px 25px;border-left:5px solid var(--pink);font-size:28px}.revisit p{line-height:1.8}details{border:1px solid #a5a08e;padding:20px;margin-top:25px}summary{cursor:pointer;font:13px monospace}.audio{margin-top:32px}.audio audio{width:100%;max-width:480px}.disclaimer{font:13px/1.7 monospace;opacity:.85}.foot{padding:33px 5vw;font:12px monospace;color:#c2d0c8}@media(max-width:800px){.hero{min-height:73vh;background-position:54% center}.explorer{grid-template-columns:1fr}.picks{grid-template-columns:repeat(2,minmax(0,1fr))}.reader .textbody{font-size:17px}}@media(max-width:470px){.hero{min-height:67vh;padding:44px 23px}.hero h1{font-size:clamp(59px,15vw,100px)}.picks{grid-template-columns:1fr}.top{padding:0 20px}.reader{padding:54px 21px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
</style></head><body><a class="skip" href="#read">Skip to reading</a><header class="top"><span>.json <b>/ 02</b></span><span>JASON, UNDER REVISION</span></header><section class="hero"><span class="eyebrow">A SMALL ROOM. A BIGGER TOMORROW.</span><h1>FASHION</h1><p>Không chỉ để mặc. Có khi quần áo đang kể hộ mình một câu chuyện.</p><div class="nav"><a href="#read">READ ↘</a><a href="#trace" class="alt">TRACE ↘</a><a href="#revisit" class="alt">LISTEN / REVISIT ↘</a></div></section><div class="reel">WORKING CHAPTER 02　 /　 ARTWORK AND TEXT UNDER REVIEW　 /　 NO LIVE RELEASE</div><main><section class="reader" id="read"><div class="toggle" role="group" aria-label="Choose manuscript version"><button type="button" data-version="proposed" aria-pressed="true">PROPOSED EDIT</button><button type="button" data-version="original" aria-pressed="false">ORIGINAL</button></div><article id="prose" class="textbody" aria-live="polite"></article></section><section class="explore" id="trace"><span class="eyebrow">AN INTERACTIVE ARTIFACT</span><h2>Wardrobe Explorer</h2><p>Không có style quiz, chẳng có đúng sai. Chỉ có sáu lần thay đổi cách nhìn về một món đồ, từ “new drop” cho đến chiếc áo cũ trong tủ bố.</p><div class="explorer"><div class="picks" id="choices" role="group" aria-label="Choose a wardrobe memory"></div><div class="memory"><img id="memory-img" alt="Detail from illustrated wardrobe poster" src="assets/scene_01.webp"><h3 id="memory-title"></h3><p id="memory-desc" role="status" aria-live="polite"></p></div></div></section><section class="revisit" id="revisit"><div class="revisit-inner"><span class="eyebrow">THE ARCHIVE / VERSION NOTES</span><h2>Less is more?</h2><p>This is not a prescription for everyone to dress minimally. The narrator is questioning whether a logo, a trend, or an approved formula still needs to define him.</p><blockquote>Be your own label, not a hanger, my man.</blockquote><details><summary>OPEN THE EDITOR'S NOTE</summary><p>The economic discussion about fast fashion remains a personal interpretation. The old jacket and wardrobe art are a visual metaphor, not an archival photograph of an identified item.</p></details><div class="audio"><p><b>LISTEN — ambient preview</b></p><audio controls preload="none" src="assets/ambient_preview.wav"></audio><p class="disclaimer">Synthetic ambient sound only, not Jason's voice. Narration is still awaiting approval and recording.</p></div></div></section></main><footer class="foot">.JSON / FASHION / PROOF ONLY — THE BOOK IS THE STORY. THE ARCHIVE IS WHAT REMAINS.</footer><script src="assets/chapter.js"></script></body></html>'''
(O/'website/index.html').write_text(html,encoding='utf-8')
js='''const beats=__BEATS__;
const textBlock=document.querySelector('#prose');
function renderVersion(which){const raw=window.CHAPTER_TEXT[which];const parts=raw.trim().split(/\\n\\s*\\n/).slice(1);textBlock.replaceChildren();parts.forEach(p=>{const el=document.createElement('p');el.textContent=p.replace(/\\*(.*?)\\*/g,'$1');textBlock.append(el)});document.querySelectorAll('[data-version]').forEach(el=>el.setAttribute('aria-pressed',String(el.dataset.version===which)))}
document.querySelectorAll('[data-version]').forEach(btn=>btn.addEventListener('click',()=>renderVersion(btn.dataset.version)));
const pick=document.querySelector('#choices');function change(i){pick.querySelectorAll('button').forEach((b,k)=>b.setAttribute('aria-pressed',String(i===k)));document.querySelector('#memory-img').src='assets/'+beats[i][3];document.querySelector('#memory-img').alt='Poster-art detail: '+beats[i][1];document.querySelector('#memory-title').textContent=beats[i][1];document.querySelector('#memory-desc').textContent=beats[i][2]}
beats.forEach((it,i)=>{const b=document.createElement('button');b.type='button';b.textContent=it[0];b.addEventListener('click',()=>change(i));pick.append(b)});renderVersion('proposed');change(0);
'''.replace('__BEATS__',json.dumps(STEPS,ensure_ascii=False))
js='window.CHAPTER_TEXT='+json.dumps({'original':orig,'proposed':edited},ensure_ascii=False)+';\n'+js
(O/'website/assets/chapter.js').write_text(js,encoding='utf-8')
# ambient copy from previous project to avoid invented voice / labeled preview
shutil.copy2(SRC/'video/ambient_synthetic.wav',O/'website/assets/ambient_preview.wav')
shutil.copy2(SRC/'video/ambient_synthetic.wav',O/'video/ambient_synthetic.wav')
# copy editable source scripts later
print('Created website/PDF/art/social assets',pdfpath.stat().st_size)
