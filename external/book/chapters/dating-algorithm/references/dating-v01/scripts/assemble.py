from pathlib import Path
import json,html,re,csv
from PIL import Image
from reportlab.lib.pagesizes import A5,A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image as RImage,PageBreak,KeepTogether,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import fitz
R=Path('/mnt/data/Dating_Algorithm_Chapter04_v01')
ms=(R/'manuscript'/'VERSION_B_VERBATIM.md').read_text(encoding='utf-8')
paras=[p.strip() for p in ms.split('\n\n')[2:] if p.strip()]
CREAM='#F7EBD6';DEEP='#092B25';PINK='#EF7DA9'
font_reg='/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf'
font_bold='/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf'
font_sans='/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
for a,b in [('Serif',font_reg),('SerifBold',font_bold),('Sans',font_sans)]:pdfmetrics.registerFont(TTFont(a,b))
# Build cover and assembled body
c=Canvas(str(R/'book'/'_cover.pdf'),pagesize=A5)
c.drawImage(str(R/'art'/'00_CHAPTER_04_COVER.jpg'),0,0,width=A5[0],height=A5[1],preserveAspectRatio=False);c.showPage();c.save()
styles={
 'title':ParagraphStyle('ct',fontName='SerifBold',fontSize=27,leading=34,textColor=colors.HexColor(DEEP),spaceAfter=10),
 'deck':ParagraphStyle('deck',fontName='Sans',fontSize=10,leading=15,textColor=colors.HexColor('#92647B'),spaceAfter=16),
 'body':ParagraphStyle('body',fontName='Serif',fontSize=10.4,leading=16.75,textColor=colors.HexColor('#1C2B29'),spaceAfter=11),
 'lead':ParagraphStyle('lead',fontName='SerifBold',fontSize=11.5,leading=18.5,textColor=colors.HexColor(DEEP),spaceAfter=18),
 'caption':ParagraphStyle('cap',fontName='Sans',fontSize=7.7,leading=11,textColor=colors.HexColor('#647568'),spaceAfter=16),
 'subhead':ParagraphStyle('sub',fontName='SerifBold',fontSize=13,leading=18,textColor=colors.HexColor(DEEP),spaceBefore=10,spaceAfter=8),
}
W,H=A5

def on_page(can,doc):
 can.setFillColor(colors.HexColor(CREAM));can.rect(0,0,W,H,fill=1,stroke=0)
 can.setFillColor(colors.HexColor(DEEP));can.rect(0,H-14,W,14,fill=1,stroke=0)
 can.setFont('Sans',7);can.drawString(33,H-29,'.json  /  04   DATING ALGORITHM')
 can.setFillColor(colors.HexColor('#AE8492'));can.drawRightString(W-35,21,'JASON, UNDER REVISION')
 can.setFillColor(colors.HexColor(DEEP));can.drawString(33,21,f'{doc.page+1:02d}')

def clean(s):
 s=html.escape(s)
 s=re.sub(r'\*(.*?)\*',r'<i>\1</i>',s)
 return s

def fig(path, maxw=344,maxh=215,caption=None):
 im=Image.open(path); iw,ih=im.size; sc=min(maxw/iw,maxh/ih)
 f=[RImage(str(path),width=iw*sc,height=ih*sc)]
 if caption:f.append(Paragraph(html.escape(caption),styles['caption']))
 return f

story=[Spacer(1,20),Paragraph('Dating Algorithm',styles['title']),Paragraph('18_feature_importance  /  VERSION B / TINDER EDITION',styles['deck'])]
for i,p in enumerate(paras):
 if i==0:sty='lead'
 elif len(p)<60 and not p.startswith('“') and not p.startswith('['):sty='lead'
 else:sty='body'
 story.append(Paragraph(clean(p),styles[sty]))
 if i==7: story.extend(fig(R/'art'/'03_the_model_PREVIS.jpg',caption='A staged lecture about optimization, confidence and unknown outcomes — illustrative art.'))
 if i==16:story.extend(fig(R/'art'/'10_matching_hypothetical.png',caption='Rank-matching schema: matching alone does not establish Nash equilibrium.'))
 if i==28:story.extend(fig(R/'art'/'09_funnel_original_diagram.png',caption='Observational study design, not the missing results from ten participants.'))
 if i==46:story.extend(fig(R/'art'/'11_invitation_decision_tree.png',caption='The right to say no is not a pipeline error.'))
story.append(PageBreak())
story.append(Paragraph('Appendix / Experiment data',styles['title']))
story.append(Paragraph('BLANK DATA — NO OBSERVATIONS PROVIDED',styles['deck']))
story.append(Paragraph('The source draft calls for 10 anonymized Tinder profiles, five M IDs and five F IDs. It provides no actual swipes, matches, conversation counts or verified consent. This intentionally empty table must not be mistaken for experimental results.',styles['body']))
head=['Profile','Score','Swipes','Matches','Chats']
rows=[head]+[[f'{g}{i}','—','—','—','—'] for g in ('M','F') for i in range(1,6)]
t=Table(rows,colWidths=[69,65,70,70,70],repeatRows=1)
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor(DEEP)),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Sans'),('FONTNAME',(0,1),(-1,-1),'Sans'),('FONTSIZE',(0,0),(-1,-1),8),('GRID',(0,0),(-1,-1),.5,colors.HexColor('#ABAD9E')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#FFF7E9'),colors.HexColor('#F0E2D7')]),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('BOTTOMPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7)]))
story.append(t)
story.append(Spacer(1,20));story.append(Paragraph('Editorial release gates',styles['subhead']))
for s in ['Author approval of public manuscript and quoted TED Talk title usage; no affiliation implied.','Verify Jiang lecture and research claims from primary sources.','Real anonymized data, collection period and consent before publishing any measured results.','Independent print preflight, artwork rights, recorded narration and website QA.']:
 story.append(Paragraph('• '+html.escape(s),styles['body']))
body=R/'book'/'_body.pdf'
SimpleDocTemplate(str(body),pagesize=A5,rightMargin=37,leftMargin=37,topMargin=47,bottomMargin=45,title='Dating Algorithm – Version B Editorial Proof').build(story,onFirstPage=on_page,onLaterPages=on_page)
merged=fitz.open();merged.insert_pdf(fitz.open(str(R/'book'/'_cover.pdf')));merged.insert_pdf(fitz.open(str(body)));merged.set_metadata({'title':'Dating Algorithm — A5 Editorial Proof','author':'Jason / .json','subject':'Version B draft; author review required'})
merged.save(str(R/'book'/'04_Dating_Algorithm_A5_EDITORIAL_PROOF.pdf'),garbage=4,deflate=True)
# A4 collectible poster with cover art
c=Canvas(str(R/'book'/'04_Dating_Algorithm_A4_POSTER_PROOF.pdf'),pagesize=A4)
a,b=A4;c.setFillColor(colors.HexColor(CREAM));c.rect(0,0,a,b,fill=1,stroke=0)
im=R/'art'/'00_CHAPTER_04_COVER.jpg'; c.drawImage(str(im),30,30,width=a-60,height=b-60,preserveAspectRatio=False)
c.showPage();c.save()
print('pdf pages',len(fitz.open(str(R/'book'/'04_Dating_Algorithm_A5_EDITORIAL_PROOF.pdf'))),'paragraphs',len(paras))

# Website, fully self-contained when ZIP extracted.
# Text inline (no remote fetch). All conclusions distinguish human worth from a game-theory metaphor.
textjson=json.dumps(paras,ensure_ascii=False)
htmlfile=r'''<!DOCTYPE html><html lang="vi"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>.json / 04 — Dating Algorithm</title><meta name="description" content="Jason, under revision: Dating Algorithm, Tinder edition. An illustrated essay and interactive model critique.">
<style>
:root{--pine:#092b25;--black:#061e1b;--pink:#ef7da9;--paper:#f7ebd6;--soft:#bbcebe;--white:#fff9f0}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--pine);color:var(--paper);font-family:Georgia,'Times New Roman',serif}button,a,input{font:inherit}a{color:inherit}a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid var(--pink);outline-offset:3px}.top{font:12px/1.7 monospace;letter-spacing:.13em;padding:15px clamp(22px,5vw,85px);display:flex;justify-content:space-between;align-items:center;background:var(--black)}.pink{color:var(--pink)}.hero{min-height:620px;display:grid;grid-template-columns:.84fr 1.16fr;align-items:stretch;background:linear-gradient(110deg,#092b25,#183c32)}.hero-copy{padding:clamp(40px,6vw,88px);align-self:center}.hero h1{font-size:clamp(54px,7vw,112px);letter-spacing:-.065em;line-height:.98;margin:13px 0}.hero h1 span{color:var(--pink);font-style:italic}.hero p{font-size:clamp(18px,2vw,25px);line-height:1.55;max-width:560px}.hero .pic{background:url('assets/01_stage_hero_PREVIS.jpg') center/cover;position:relative}.hero .pic::after{content:'';position:absolute;inset:0;box-shadow:inset 80px 0 90px var(--pine)}.kicker,nav,.label,.badge,.foot{font:12px/1.7 monospace;letter-spacing:.08em}.kicker{color:var(--pink)}.cta{display:inline-block;background:var(--pink);padding:13px 18px;color:var(--black);font:700 13px monospace;text-decoration:none;border:0;margin:15px 9px 0 0;cursor:pointer}.cta.alt{background:transparent;color:var(--paper);border:1px solid var(--pink)}.strip{display:flex;gap:24px;flex-wrap:wrap;background:var(--black);padding:15px 5vw;font:12px monospace}.read{background:var(--paper);color:var(--black);padding:80px 20px}.reader{max-width:760px;margin:auto;font-size:18px;line-height:1.8}.reader h2{font-weight:normal;font-size:clamp(36px,5vw,64px);line-height:1.2;margin:8px 0}.reader p{margin:0 0 1.38em}.reader p:nth-child(2){font-size:1.22em}.reader p:nth-child(3){font-size:1.2em;font-style:italic}.read .version{color:#8a516c;font:13px monospace;letter-spacing:.06em}.callout{padding:22px;margin:38px 0;border-left:5px solid var(--pink);background:#efe0d4;font-size:15px}.model{max-width:1150px;margin:auto;padding:82px 24px}.model h2,.research h2{font-size:clamp(38px,5vw,68px);font-weight:normal;margin:12px 0}.info{font-size:19px;max-width:860px;line-height:1.7}.controls{background:#123b31;border:1px solid #b9879a;padding:32px;margin:36px 0}.weight-row{display:grid;grid-template-columns:165px 1fr 65px;gap:20px;align-items:center;margin:18px 0;font:14px monospace}.weight-row input{width:100%;accent-color:var(--pink)}.bar{display:flex;width:100%;height:32px;border-radius:5px;overflow:hidden;background:#4b5c52;margin:25px 0}.bar span{transition:width .15s}.result{font:14px/1.8 monospace;color:var(--soft)}.research{background:var(--paper);color:var(--black);padding:85px 20px}.research-inner{max-width:1020px;margin:auto}.table-scroll{overflow-x:auto}.research table{width:100%;border-collapse:collapse;margin:26px 0;font:13px/1.4 monospace;min-width:580px}.research th{background:var(--pine);color:var(--paper)}.research th,.research td{border:1px solid #ada69a;padding:12px;text-align:center}.research tr:nth-child(even){background:#eaddcf}.diagram{width:100%;max-width:1000px;border:2px solid var(--pink);margin:30px auto}.pill{display:inline-block;border:1px solid #b28b96;padding:4px 10px;font:12px monospace;color:#6a4b52}.links{display:flex;gap:16px;flex-wrap:wrap}.links a{color:var(--pink);font:12px monospace}.decision{border:1px solid #cb8aa8;padding:25px;margin:30px 0}.decision button{padding:14px 20px;background:#15453a;color:white;border:1px solid var(--pink);margin:0 8px 10px 0;cursor:pointer}.decision button[aria-pressed=true]{background:var(--pink);color:var(--black)}#outcome{font-size:19px;line-height:1.7;min-height:85px}.foot{padding:36px 6vw;border-top:1px solid #456b59;color:#cbd8c5}.rule{border:0;border-top:1px solid #cfb6b2;margin:38px 0}@media(max-width:820px){.hero{grid-template-columns:1fr}.hero .pic{min-height:360px;grid-row:1}.hero .pic::after{box-shadow:inset 0 -45px 50px var(--pine)}.hero-copy{padding:28px 24px 60px}.weight-row{grid-template-columns:110px 1fr 50px;gap:8px}.controls{padding:20px}.read{padding:55px 22px}.reader{font-size:16.5px}.model{padding:50px 20px}.research{padding:55px 18px}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{scroll-behavior:auto!important;transition:none!important}}
</style></head><body><header class="top"><strong>.json <span class="pink">/ 04</span></strong><span>JASON, UNDER REVISION</span><span>EDITORIAL PROOF</span></header>
<section class="hero"><div class="hero-copy"><p class="kicker">RELATIONSHIP_MODELING / VERSION B</p><h1>Dating <span>Algorithm</span></h1><p>Để một data scientist dạy bạn cách tối ưu chuyện hẹn hò. And then watch his model fail.</p><p class="kicker">A fictionalized stage illustration — not a TED event.</p><a href="#chapter" class="cta">READ CHAPTER →</a><a href="#interactive" class="cta alt">EXPLORE MODEL ↗</a></div><div class="pic" role="img" aria-label="Consultant-style Jason wearing clear glasses on stage, with a pink heart and a lecture chart"></div></section>
<div class="strip"><span>01 / READ</span><span>02 / QUESTION THE WEIGHTS</span><span>03 / DATA STILL MISSING</span><span>04 / UPDATE THE MODEL</span></div>
<section class="read" id="chapter"><article class="reader"><span class="version">18_feature_importance / VERSION B / SOURCE PRESERVED</span><h2>Dating Algorithm</h2><div id="chaptext"></div><div class="callout"><b>Editorial note:</b> The essay's 70%/90% gender weights are deliberately invented by the narrator. Its Tinder study has a blank data slot. This reading prototype preserves those statements in context; they are not claims about real people's value.</div></article></section>
<section class="model" id="interactive"><span class="kicker">02 / A MODEL, NOT A PERSON</span><h2>Choose your own weights</h2><p class="info">Jason's original model tries to reduce dating to an optimization problem. Move the sliders to see how quickly a supposed “importance” ranking changes. There is no scientific calibration, no gender defaults, and no score for a human being.</p><div class="controls"><div id="weights"></div><div id="weightbars" class="bar" aria-label="Relative illustrative weights"></div><div id="feedback" class="result" aria-live="polite"></div></div><img class="diagram" src="assets/10_matching_hypothetical.png" alt="Five-to-five rank correspondence only, not a formal proof of Nash equilibrium"><p class="result">Illustration only: a matching diagram needs defined strategies/payoffs and possible deviations to establish Nash equilibrium.</p><div class="decision"><p class="kicker">03 / ONE SMALL DECISION</p><h2>Invite or keep thinking?</h2><p class="info">This is a literary counterfactual, not a relationship predictor.</p><button type="button" data-opt="invite">INVITE RESPECTFULLY</button><button type="button" data-opt="wait">DON'T INVITE</button><button type="button" data-opt="reset">RESET</button><p id="outcome" aria-live="polite">Both outcomes are unknown. Another person always has their own choice.</p></div></section>
<section class="research"><div class="research-inner"><p class="kicker">04 / OBSERVATIONAL DATA SLOT</p><h2>Ten profiles. Zero published results.</h2><p class="info">The manuscript mentions five male and five female friends' Tinder profiles but contains no completed metrics. We can't recover real swipe counts from that story. The table below is intentionally empty and should remain so until consent, actual logs and methodology are checked.</p><div class="table-scroll"><table id="datatable"><thead><tr><th>ID</th><th>Visual profile score*</th><th>Right swipes</th><th>Matches</th><th>Conversations</th><th>Consent</th></tr></thead><tbody></tbody></table></div><p class="pill">* A subjective description of one profile presentation — never a measure of human worth.</p><img class="diagram" src="assets/09_funnel_original_diagram.png" alt="Distinction between profile, swipe, match and conversation"><hr class="rule"><h2>What the model misses</h2><p class="info">“Getting liked,” “getting matched,” and “being worth meeting again” are different outcomes. The later chapter questions the very ranking system with which it opens. Chemistry, agency, consent and wanting to meet again are not interchangeable with a Tinder conversion rate.</p><p class="info"><strong>Release note:</strong> This chapter needs author sign-off, source fact-checking and real participant consent before public publication. No user behavior on this page is stored or uploaded.</p></div></section>
<footer class="foot">.json  /  JASON, UNDER REVISION · Editorial proof only · The book is the story. The artifact is a question.</footer>
<script>
const paragraphs = __PARAGRAPHS__;
const holder=document.getElementById('chaptext');paragraphs.forEach((p,i)=>{let el=document.createElement('p');el.textContent=p;holder.appendChild(el)});
const features=['Appearance','Intelligence','Lifestyle','Shared values'];let vals=[25,25,25,25];const colors=['#ef7da9','#ddae82','#91c3ac','#8caabd'];let names=features.map((f,i)=>{const row=document.createElement('div');row.className='weight-row';const label=document.createElement('label');const id='feature'+i;label.setAttribute('for',id);label.textContent=f;const input=document.createElement('input');input.type='range';input.id=id;input.min='0';input.max='100';input.value='25';const out=document.createElement('span');out.id='v'+i;out.textContent='25';input.addEventListener('input',()=>{vals[i]=+input.value;draw()});row.append(label,input,out);document.getElementById('weights').appendChild(row)});function draw(){let total=vals.reduce((a,b)=>a+b,0);let bars=document.getElementById('weightbars');bars.replaceChildren();vals.forEach((v,i)=>{document.getElementById('v'+i).textContent=v;let span=document.createElement('span');span.style.background=colors[i];span.style.width=(total?100*v/total:25)+'%';span.title=features[i]+': '+(total?(100*v/total).toFixed(1):'undefined')+'% of total';bars.appendChild(span)});document.getElementById('feedback').textContent=total?'This arbitrary preference vector gives '+features[vals.indexOf(Math.max(...vals))]+' the highest weight. No population claim follows.':'All weights are zero. This model cannot distinguish priorities.'};draw();
const tbody=document.querySelector('#datatable tbody');['M1','M2','M3','M4','M5','F1','F2','F3','F4','F5'].forEach(id=>{let row=document.createElement('tr');[id,'—','—','—','—','NOT VERIFIED'].forEach(v=>{let cell=document.createElement('td');cell.textContent=v;row.appendChild(cell)});tbody.appendChild(row)});
document.querySelectorAll('[data-opt]').forEach(b=>b.addEventListener('click',()=>{let a=b.dataset.opt;document.querySelectorAll('[data-opt]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));document.getElementById('outcome').textContent=a==='invite'?'Invitation made. The other person may accept or decline freely; no probabilities are known.':a==='wait'?'You waited. The unchosen invitation remains counterfactual; you cannot know how it would have gone.':'Both outcomes are unknown. Another person always has their own choice.'}));
</script></body></html>'''
htmlfile=htmlfile.replace('__PARAGRAPHS__',textjson)
(R/'web'/'index.html').write_text(htmlfile,encoding='utf-8')
# duplicate only needed art assets for standalone website
for f in ['01_stage_hero_PREVIS.jpg','10_matching_hypothetical.png','09_funnel_original_diagram.png']:
 (R/'web'/'assets'/f).write_bytes((R/'art'/f).read_bytes())
print('website written,',len(htmlfile),'characters')

# Build 64-task editable HTML board plus machine-readable artifacts
streams={
 'Editorial & Research':[
 'Preserve Version B source DOCX','Select canonical manuscript','Review abusive/chauvinistic opening in narrated context','Verify Jiang lecture and game theory terminology','Verify cross-cultural mate preference citations','Verify 3,600-evaluation research claim','Verify speed-dating research attribution','Resolve Tinder study data slot','Collect explicit participant consent','Approve source and fact notes'],
 'Illustrations & Visual Design':[
 'Confirm consultant look and clear glasses','Approve stage poster with pink heart','Export original standalone hero at print grade','Illustrate SMV slider with invented parameters notice','Illustrate lecture-audience scene','Draw graph separating equilibrium and matching','Draw profile/swipe/match/conversation funnel','Create phone and notebook illustration','Prepare alternate 9:16 poster crop','Brand/logo and trademark rights audit'],
 'Book & Print':[
 'Lay out full A5 essay','Place chapter illustrations without interrupting text','Create A4 collectible poster proof','Check Vietnamese fonts/diacritics','Render all A5 pages','Proofread final page and appendix','Confirm trim and gutter with printer','Generate printer-required PDF/X with bleed','Inspect physical printed sample'],
 'Interactive Website':[
 'Build responsive chapter reader','Include full manuscript text offline','Build adjustable feature weight simulator','Make simulator disclaimer explicit','Build model matching visualization','Add blank dataset table','Build invitation outcome interaction','Keyboard and focus accessibility','Desktop browser QA','Mobile browser QA','Host on permanent approved URL'],
 'Video & Audio':[
 'Write 24s storyboard','Produce 9:16 concept stills','Encode 9:16 ambient animatic','Draft voiceover script','Record or authorize narrator','Create actual voiced subtitle SRT/VTT','Produce final 1080x1920 film','Mix licensed/original sound','Mobile caption safe-zone QA'],
 'Social & Launch':[
 'Build 5-card Instagram carousel','Export 3:4 stills','Create Facebook image and post','Create YouTube Short thumbnail','Write TikTok/Reel caption','Write YouTube metadata','Confirm rights for logos/people/media','Approve social copy','Upload approved files to repo','Publish website after authorization','Issue tested QR once URL is final','Release social posts through authorized accounts','Track consent and post-publication feedback']
}
tasks=[];i=1
for stream,items in streams.items():
 for j,title in enumerate(items):
  status='TODO'
  if title in ['Preserve Version B source DOCX','Build responsive chapter reader','Include full manuscript text offline','Build adjustable feature weight simulator','Make simulator disclaimer explicit','Add blank dataset table','Build invitation outcome interaction','Lay out full A5 essay','Create A4 collectible poster proof','Check Vietnamese fonts/diacritics','Render all A5 pages','Write 24s storyboard','Produce 9:16 concept stills','Encode 9:16 ambient animatic','Build 5-card Instagram carousel','Export 3:4 stills','Create Facebook image and post','Create YouTube Short thumbnail','Write TikTok/Reel caption','Write YouTube metadata']:
   status='PROOF'
  if title in ['Confirm consultant look and clear glasses','Approve stage poster with pink heart']:
   status='PROOF'
  if title in ['Collect explicit participant consent','Resolve Tinder study data slot','Select canonical manuscript','Confirm trim and gutter with printer','Generate printer-required PDF/X with bleed','Inspect physical printed sample','Record or authorize narrator','Create actual voiced subtitle SRT/VTT','Host on permanent approved URL','Publish website after authorization','Release social posts through authorized accounts']:
   status='BLOCKED'
  tasks.append({'id':f'DA-{i:03d}','stream':stream,'title':title,'status':status,'priority':'P0' if status=='BLOCKED' or j<3 else 'P1','owner':'Jason / editor' if status=='BLOCKED' else 'Production team','acceptance':'File or verified evidence attached; approved for stated scope.','notes':''});i+=1
(R/'docs'/'TASKS.json').write_text(json.dumps(tasks,indent=2,ensure_ascii=False),encoding='utf-8')
with (R/'docs'/'CHECKLIST.csv').open('w',newline='',encoding='utf-8-sig') as f:
 writer=csv.DictWriter(f,fieldnames=tasks[0].keys());writer.writeheader();writer.writerows(tasks)
(R/'docs'/'RELEASE_CHECKLIST.md').write_text('''# Dating Algorithm — Release gate

## Completed as **production proofs**, not public assets
- [x] Source DOCX contents preserved in Markdown unchanged
- [x] A5 illustrated full chapter PDF and A4 poster proof
- [x] Standalone art / crops from selected stage design
- [x] Full offline-responsive reader with subjective feature sliders and blank ten-profile table
- [x] 5 × Instagram 3:4 cards, FB/YT image exports
- [x] 24-second 9:16 ambient video proof and visual-only SRT
- [x] Editable production board, CSV/JSON, script assets

## Still required
- [ ] Approve canonical chapter and first-person claims (including real Tinder experiment)
- [ ] Actual numbers/consent for M1–M5 and F1–F5 (or clarify hypothetical study)
- [ ] Verify published research / Jiang references
- [ ] Original professional layered art; review TED/brand usage
- [ ] Record narrator with rights; retime SRT and finish 1080×1920 video
- [ ] Printer-specified PDF/X with bleeds, physical proof, QR
- [ ] Public-site deploy and independent mobile accessibility checks
- [ ] Authorized platform publishing

**DO NOT publish the appendix as results. Current illustrations are proof-level crops from an AI-made project-board concept.**
''',encoding='utf-8')
(R/'docs'/'NARRATION_SCRIPT.md').write_text('''# Dating Algorithm — suggested narration, NOT RECORDED

“Welcome to my TED Talk on dating.”

T từng giải thích chuyện hẹn hò bằng một scoring function. Appearance, status, money, intelligence. Rồi tự assign weights, nói một tràng về Nash equilibrium như thể vừa giải xong bài toán.

Dataset đâu? Well, tôi có mười cái Tinder profiles. Nhưng điều buồn cười là, matches đâu có giống conversations, và conversations lại không giống chuyện hai người có muốn gặp nhau thêm lần nữa.

70% và 90%? They're hyperparameters. Assigned by Jason, peer-reviewed by Jason, approved by Jason.

Thế nên maybe the first date isn't an optimization problem. Maybe it's where the data finally contradicts your model.

—
**Recording/permission pending.** Adapted from author-provided Version B, not an existing audio file. Storyboard is a distinct 24-second ambient *visual proof*; narration pacing has not been timed.
''',encoding='utf-8')
(R/'docs'/'STORYBOARD.md').write_text('''# Dating Algorithm — vertical video proof (24 seconds)

| Seconds | Scene | Visual subtitle |
|---|---|---|
| 0.0–4.8 | A consultant on a pink/green lecture stage | Welcome to my TED Talk on dating |
| 4.8–9.6 | Clear glasses / confident headshot | A very confident model |
| 9.6–14.4 | Matching ranks graphic | Matching ≠ demonstrated equilibrium |
| 14.4–19.2 | Tinder funnel | Ten profiles. No supplied results. |
| 19.2–24.0 | Invitation choice diagram | People aren't equations |

**Not a real lecture, empirical animation, voice recording or scientifically calibrated matching engine.** The original user-approved art direction combines retro album poster and formal consulting stage; this kit uses crops of the concept board.
''',encoding='utf-8')
(R/'docs'/'SOCIAL_COPY.md').write_text('''# Social posts / drafts only

**Instagram:**
Welcome to my TED Talk on dating. T từng nghĩ chỉ cần scoring function, vài weights và game theory là có thể optimize đời sống tình cảm. Then reality asked for the dataset. — Dating Algorithm / .json. [Approved website link pending]

**Facebook:**
Có một thời Jason tưởng mình giải được bài toán hẹn hò bằng SMV, Nash equilibrium và một đống công thức. Nhưng cái model này có bug: nó đo profile performance, không phải giá trị của người thật. Chapter 04 — Dating Algorithm. Link sẽ cập nhật khi phát hành.

**YouTube Short title:** Dating Algorithm | The TED Talk That Failed Its Own Model — .json

**TikTok/Reels caption:** A data scientist trying to optimize love, and forgetting human beings aren't feature vectors. 04 / .json.

**No posts have been published.** No video is narrated. No actual profile results are presented.
''',encoding='utf-8')
board=r'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Dating Algorithm — Production Board</title><style>*{box-sizing:border-box}body{margin:0;background:#082921;color:#f7ebd6;font:14px/1.6 system-ui,sans-serif}header{padding:60px 5vw 40px;background:linear-gradient(100deg,#06231e,#25483c);border-bottom:5px solid #ed7da9}h1{font-size:clamp(50px,7vw,95px);line-height:1;letter-spacing:-.05em;margin:10px 0;color:#f17ca6}header p{font-size:17px;max-width:800px}main{padding:35px 5vw}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:30px 0}.stat{border:1px solid #af7e92;background:#113b31;padding:18px;border-radius:9px}.stat b{display:block;font-size:30px}.toolbar{display:flex;flex-wrap:wrap;gap:10px;margin:25px 0}.toolbar input,.toolbar select,.toolbar button{background:#173e35;color:#fff1df;border:1px solid #ab8394;padding:12px;border-radius:5px}.toolbar input{min-width:240px;flex:1}.toolbar button{cursor:pointer}.stream{margin:40px 0 18px;font-size:24px;color:#f17ca6}.tasks{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:11px}.task{background:#123a30;border:1px solid #3d685b;padding:17px;border-radius:8px}.task small{font:11px monospace;color:#d0bea7}.task strong{display:block;font-size:15px;margin:8px 0}.task select{margin-top:12px;border:1px solid #bf8ba0;background:#092b25;color:white;padding:8px;width:100%}.task em{font-style:normal;color:#cfbab5;font-size:12px}.pills{margin-top:12px;display:flex;flex-wrap:wrap;gap:6px}.pill{background:#204d40;border-radius:4px;padding:4px 9px;font:11px monospace}.hero{height:290px;background:url('../art/01_stage_hero_PREVIS.jpg') center/cover;border-radius:10px;border:2px solid #ef7da9}.muted{color:#e0cabc}@media(max-width:720px){.stats,.tasks{grid-template-columns:1fr 1fr}.hero{height:200px}}@media(max-width:480px){.stats,.tasks{grid-template-columns:1fr}}button:focus-visible,select:focus-visible,input:focus-visible{outline:3px solid #ee7da9;outline-offset:3px}</style><header><small>.json / CHAPTER 04 / PRIVATE EDITORIAL PROOF</small><h1>Dating Algorithm</h1><p>A formal stage, pink heart, black suit and clear glasses. The production pipeline behind the book, cinematic media and data-model critique.</p><div class="pills"><span class="pill">PINK × PINE</span><span class="pill">VERSION B</span><span class="pill">N=10 DATA UNVERIFIED</span><span class="pill">RELEASE HOLD</span></div></header><main><div class="hero" role="img" aria-label="Illustrated dating TED-style conference stage"></div><section class="stats" id="stats"></section><div class="toolbar"><input id="search" placeholder="Search 64+ tasks..." aria-label="Search tasks"><select id="status"><option value="">All statuses</option><option>TODO</option><option>PROOF</option><option>BLOCKED</option><option>READY</option><option>IN_PROGRESS</option></select><select id="stream"><option value="">All workstreams</option></select><button id="export">Export CSV</button><button id="reset">Reset states</button></div><div id="list"></div><p class="muted">Status changes are local to this browser, exported CSV is the portable source of truth. No API, cloud storage or analytics.</p></main><script>const tasks=__TASKS__;let state={};try{state=JSON.parse(localStorage.getItem('datingBoard_v1')||'{}')}catch{};tasks.forEach(t=>{if(state[t.id])t.status=state[t.id]});const streamEl=document.querySelector('#stream');[...new Set(tasks.map(t=>t.stream))].forEach(v=>{const x=document.createElement('option');x.textContent=v;streamEl.append(x)});function render(){const stats=document.querySelector('#stats');stats.replaceChildren();['READY','PROOF','TODO','BLOCKED'].forEach(key=>{let a=document.createElement('div');a.className='stat';let count=tasks.filter(t=>t.status===key).length;a.innerHTML='<b>'+count+'</b>'+key;stats.appendChild(a)});const target=document.querySelector('#list');target.replaceChildren();let q=document.querySelector('#search').value.toLowerCase(),fs=document.querySelector('#status').value,st=document.querySelector('#stream').value;let found=tasks.filter(t=>(!q||(t.title+t.stream+t.id).toLowerCase().includes(q))&&(!fs||t.status===fs)&&(!st||t.stream===st));[...new Set(found.map(t=>t.stream))].forEach(stream=>{let h=document.createElement('h2');h.className='stream';h.textContent=stream;target.append(h);let grid=document.createElement('div');grid.className='tasks';found.filter(t=>t.stream===stream).forEach(t=>{let el=document.createElement('div');el.className='task';let sm=document.createElement('small');sm.textContent=t.id+'  /  '+t.priority;let title=document.createElement('strong');title.textContent=t.title;let foot=document.createElement('em');foot.textContent=t.owner;let sel=document.createElement('select');sel.setAttribute('aria-label','Status for '+t.title);['TODO','IN_PROGRESS','PROOF','BLOCKED','READY'].forEach(v=>{const o=document.createElement('option');o.textContent=v;o.value=v;sel.append(o)});sel.value=t.status;sel.onchange=()=>{t.status=sel.value;state[t.id]=t.status;try{localStorage.setItem('datingBoard_v1',JSON.stringify(state))}catch{};render()};el.append(sm,title,foot,sel);grid.append(el)});target.append(grid)})}['search','status','stream'].forEach(id=>document.getElementById(id).addEventListener(id==='search'?'input':'change',render));document.getElementById('reset').onclick=()=>{tasks.forEach(t=>delete state[t.id]);try{localStorage.removeItem('datingBoard_v1')}catch{};location.reload()};document.getElementById('export').onclick=()=>{let cols=['id','stream','title','status','priority','owner','acceptance','notes'];let esc=s=>'"'+String(s??'').replaceAll('"','""')+'"';let csv=[cols.join(','),...tasks.map(t=>cols.map(c=>esc(t[c])).join(','))].join('\r\n');let a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));a.download='Dating_Algorithm_UPDATED_TASKS.csv';a.click();URL.revokeObjectURL(a.href)};render();</script></html>'''
board=board.replace('__TASKS__',json.dumps(tasks,ensure_ascii=False))
(R/'docs'/'PROJECT_BOARD.html').write_text(board,encoding='utf-8')
print('tasks',len(tasks))
