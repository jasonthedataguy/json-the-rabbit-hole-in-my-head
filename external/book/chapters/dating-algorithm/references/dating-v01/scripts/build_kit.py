from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps, ImageFilter
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RImage, PageBreak, KeepTogether, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A5, A4
import json, csv, shutil, textwrap, math, re, html, os
R=Path('/mnt/data/Dating_Algorithm_Chapter04_v01')
source=Path('/mnt/data/dating_algorithm_B_tinder_jjiang_draft(1).docx')
board=Image.open('/mnt/data/a_wide_stylized_poster_like_editorial_infographi.png').convert('RGB')
doc=Document(source)
ps=[p.text.strip() for p in doc.paragraphs]
# All Version B narrative text is preserved, including its preliminary hypotheses and source caveats.
paragraphs=[p for p in ps[3:56] if p]
main='\n\n'.join(paragraphs)
(R/'manuscript'/'VERSION_B_VERBATIM.md').write_text('# Dating Algorithm\n\n*18_feature_importance — VERSION B / TINDER EDITION*\n\n'+main+'\n',encoding='utf-8')
(R/'manuscript'/'CANONICAL_CANDIDATE.md').write_text('# Dating Algorithm\n\n*18_feature_importance — VERSION B / TINDER EDITION*\n\n'+main+'\n',encoding='utf-8')
(R/'manuscript'/'EDIT_NOTES.md').write_text('''# Editorial notes / Chapter 04

**Status: author review.** The proposed book text is currently identical to the attached Version B. Nothing from the essay was silently deleted, revised or invented.

## Keep as written
- Arrogant TED Talk opening; the early 70%/90% model later revealed as invented hyperparameters.
- Professor Jiang's hypothetical matching lecture versus Jason's *planned / described* ten-profile observational Tinder dataset.
- Failure of a naïve SMV/numeric dating model to explain human relationships; ending privileges conversation and personal curiosity.
- Voice: Vinglish, provocative self-deprecation, emotional uncertainty.

## Publication blockers
1. Tinder case study: the source's result cells are **empty**. Do not claim that an actual measured result was observed; use the attached blank CSV until consent and numbers are supplied.
2. The source calls the 3,600-evaluation study a field experiment; verify the actual study methodology, population and reported results before publication.
3. Confirm exact scope of Professor Jiang's demonstration, his wording about Nash equilibrium, and the source of quoted lecture material.
4. 70%/90% are explicitly Jason's hyperparameters, **not scientific sex/gender facts**. A person's value is not a score.
5. The preliminary notes mention ten private friends' profiles. Obtain meaningful consent; do not include photographs or traceable profile details in a public artifact.
6. The paragraphs about assigning an evening's budget by appearance are part of the narrator's morally uncomfortable version history, not advice endorsed by the website.
7. Source includes a verbatim initial rant; ensure readers understand it is a younger/self-satirized theory and not empirical consensus.

**Image disclaimer:** Generated poster/stage imagery is interpretive. This is not a photo of a real event or a real TED conference. Don't use TED trademark to imply affiliation.
''',encoding='utf-8')
(R/'manuscript'/'SOURCE_FACTS.md').write_text('# Facts and sources supplied in the DOCX\n\n'+'\n\n'.join(ps[57:65]),encoding='utf-8')
# Blank, explicit data-entry sheet sourced directly from the DOCX table
with (R/'data'/'tinder_ten_profiles_BLANK.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['anon_id','perceived_visual_profile_score_1_to_10','right_swipes','matches','conversations','first_messages','replies','observation_window','consent_status','notes'])
 for i in range(1,6):w.writerow([f'M{i}','','','','','','','','NOT_VERIFIED',''])
 for i in range(1,6):w.writerow([f'F{i}','','','','','','','','NOT_VERIFIED',''])

# Palette and fonts
INK='#082A22'; DEEP='#092B25'; CORAL='#EE89A6'; PINK='#EF7DA9'; CREAM='#F7EBD6'; WHITE='#FFF5E5'; SOFT='#C9D6BC'; GOLD='#D5A879'
FONT='/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
BOLD='/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'
SERIF='/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf'
SERIF_B='/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf'

def ft(px,bold=False,serif=False):return ImageFont.truetype(SERIF_B if bold and serif else SERIF if serif else BOLD if bold else FONT,px)
def rounded(d,xy,r,fill,outline=None,width=1):d.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=width)
def wrap_text(d,s,font,maxw):
 words=s.split(); lines=[];curr=''
 for w in words:
  nxt=(curr+' '+w).strip()
  if d.textbbox((0,0),nxt,font=font)[2]>maxw and curr:lines.append(curr);curr=w
  else:curr=nxt
 if curr:lines.append(curr)
 return lines

def draw_multiline(d,s,xy,font,fill,maxw,spacing=8,max_lines=0):
 x,y=xy;lines=wrap_text(d,s,font,maxw)
 if max_lines:lines=lines[:max_lines]
 for line in lines:d.text((x,y),line,font=font,fill=fill,stroke_width=0);y+=font.size+spacing
 return y

def grain(im,amp=10):
 import numpy as np
 a=np.asarray(im).astype('int16');rng=np.random.default_rng(11);noise=rng.integers(-amp,amp+1,(a.shape[0],a.shape[1],1));return Image.fromarray(np.uint8(np.clip(a+noise,0,255)))

# Hero crop from selected approved *project board* (proof, not professional standalone master).
# Keep the complete 04 stage panel; this image is a previsualization cropped from a composite artwork.
hero=board.crop((10,8,626,407))
hero=hero.resize((1848,1197),Image.Resampling.LANCZOS)
hero=ImageEnhance.Contrast(hero).enhance(1.10)
hero.save(R/'art'/'01_stage_hero_PREVIS.jpg',quality=94,subsampling=0)
# Smaller scene crops extracted from different sections of the author-selected production-board reference.
crops={
 '02_presenter_profile':(235,54,390,235),
 '03_the_model':(265,18,599,237),
 '04_audience':(14,256,627,402),
 '05_lecture':(665,15,880,255),
 '06_tinder':(1057,662,1240,788),
 '07_notebook':(1080,698,1243,827),
 '08_city':(1162,650,1375,815)
}
for name,box in crops.items():
 im=board.crop(box).resize((900,720),Image.Resampling.LANCZOS)
 im.save(R/'art'/(name+'_PREVIS.jpg'),quality=90)
# Original diagram artwork, text-based creative assets using brand palette
W,H=1800,1100
chart=Image.new('RGB',(W,H),CREAM);d=ImageDraw.Draw(chart)
d.rectangle((45,45,W-45,H-45),outline=DEEP,width=10)
d.text((95,100),'THE MODEL ≠ THE PERSON',fill=INK,font=ft(65,True))
d.text((95,192),'A toy model — probabilities and parameters are NOT validated',fill='#7D5A68',font=ft(29))
cols=[('PROFILE','A profile is not a person'),('SWIPE','Visibility is not guaranteed'),('MATCH','A match is not a date'),('CONVERSATION','A chat is not chemistry')]
for i,(a,b) in enumerate(cols):
 x=90+i*427;rounded(d,(x,390,x+372,704),25,DEEP);d.ellipse((x+126,335,x+230,439),fill=PINK)
 d.text((x+24,495),a,font=ft(32,True),fill=WHITE)
 draw_multiline(d,b,(x+25,568),ft(24),WHITE,327,8)
 if i<3:d.text((x+370,520),'→',fill=PINK,font=ft(46,True))
d.text((95,810),'OBSERVATION → ASSUMPTION → EXPERIMENT → MODEL UPDATE',font=ft(31,True),fill=INK)
d.text((96,883),'N = 10 is not a population-level claim. Consent and actual data are required.',font=ft(26),fill=INK)
chart.save(R/'art'/'09_funnel_original_diagram.png')
# Matching problem graphic, explicitly schematic and without invented outcomes
match=Image.new('RGB',(W,H),DEEP);d=ImageDraw.Draw(match)
d.text((95,85),'SAME RANK ≠ EQUILIBRIUM',font=ft(64,True),fill=CREAM)
d.text((98,177),'Matching is a model; Nash equilibrium needs payoffs and strategies.',font=ft(28),fill=PINK)
for i in range(5):
 y=310+i*130
 for x,label in [(200,f'M{i+1}'),(1350,f'F{i+1}')]:
  d.ellipse((x,y-36,x+95,y+60),fill=PINK if i%2==0 else GOLD)
  d.text((x+26,y-7),label,font=ft(30,True),fill=INK)
 d.line((310,y+12,1338,y+12),fill=CREAM,width=4)
 d.text((785,y-31),f'{i+1}  ↔  {i+1}',font=ft(27),fill=CREAM)
d.text((100,1000),'Illustrative correspondence only  •  Not a demonstrated equilibrium.',font=ft(23),fill=WHITE)
match.save(R/'art'/'10_matching_hypothetical.png')
# Decision tree mock
tr=Image.new('RGB',(W,H),CREAM);d=ImageDraw.Draw(tr)
d.text((100,90),'INVITE SOMEONE OUT?',font=ft(73,True),fill=INK)
d.text((100,178),'A thoughtful invitation ≠ guaranteed acceptance',font=ft(30),fill='#765E69')
rounded(d,(646,280,1160,410),24,DEEP);d.text((717,314),'INVITE RESPECTFULLY',font=ft(36,True),fill=WHITE)
for x,lab,sub in [(255,'YES','Make space for a real conversation'),(1085,'NO','Respect the decision; pipeline ends')]:
 d.line((902,411,x+195,580),fill=PINK,width=9)
 rounded(d,(x,585,x+500,800),26,INK)
 d.text((x+35,613),lab,font=ft(55,True),fill=PINK)
 draw_multiline(d,sub,(x+35,695),ft(26),WHITE,440,7)
d.text((105,935),'Consent is not a conversion bug to fix.',font=ft(35,True),fill=INK)
tr.save(R/'art'/'11_invitation_decision_tree.png')

# New primary typographic poster/cover from selected stage illustration, retaining selected glasses and suit style.
cover=Image.new('RGB',(1600,2250),CREAM);dr=ImageDraw.Draw(cover)
dr.rectangle((30,30,1570,2220),fill=DEEP)
# stage hero crop with ratio preservation
hi=ImageOps.fit(hero,(1516,1210),method=Image.Resampling.LANCZOS,centering=(.48,.42));cover.paste(hi,(42,520))
dr.rectangle((42,1715,1558,2210),fill=DEEP)
dr.text((95,112),'JASON / 04',fill=PINK,font=ft(65,True))
dr.text((96,209),'DATING',font=ft(174,True,serif=True),fill=CREAM)
dr.text((96,401),'ALGORITHM',font=ft(150,True,serif=True),fill=PINK)
dr.text((102,1787),'18_feature_importance',font=ft(45),fill=CREAM)
dr.text((103,1865),'VERSION B / TINDER EDITION',font=ft(33,True),fill=PINK)
draw_multiline(dr,'Welcome to my TED Talk on dating.',(103,1960),ft(37,False,True),CREAM,1330,15)
dr.rectangle((43,42,1558,2208),outline=PINK,width=10)
cover=grain(cover,5);cover.save(R/'art'/'00_CHAPTER_04_COVER.jpg',quality=94)
# social squares/cards
slides=[
 ('01 / THE LECTURE','WELCOME TO MY TED TALK','A data scientist explains dating. What could possibly go wrong?', '01_stage_hero_PREVIS.jpg'),
 ('02 / HYPERPARAMETERS','70% AND 90%?','Assigned by Jason. Peer-reviewed by Jason. Approved by Jason.','02_presenter_profile_PREVIS.jpg'),
 ('03 / MATCHING','NASH EQUILIBRIUM?','Not so fast. Matching ranks is not the same as proving an equilibrium.','10_matching_hypothetical.png'),
 ('04 / N = 10','TINDER EXPERIMENT','Ten profiles. Empty result cells. Questions, not population claims.','09_funnel_original_diagram.png'),
 ('05 / THE REVISION','CHEMISTRY > SCORE','An actual conversation can destroy your favorite priors.','11_invitation_decision_tree.png')]
for i,(idx,headline,subtitle,imgname) in enumerate(slides,1):
 canvas=Image.new('RGB',(1080,1440),CREAM);d=ImageDraw.Draw(canvas)
 d.rectangle((18,18,1062,1422),outline=DEEP,width=12)
 d.text((62,66),f'.json  /  {idx}',font=ft(29,True),fill=INK)
 # artwork region to fit
 source_im=Image.open(R/'art'/imgname).convert('RGB')
 box=(47,197,1033,1049)
 canvas.paste(ImageOps.fit(source_im,(box[2]-box[0],box[3]-box[1]),method=Image.Resampling.LANCZOS),(box[0],box[1]))
 d.rectangle((48,1015,1032,1393),fill=DEEP)
 d.text((79,1055),headline,font=ft(57,True),fill=PINK)
 draw_multiline(d,subtitle,(82,1161),ft(32),WHITE,915,14,3)
 d.text((82,1336),'JASON, UNDER REVISION',font=ft(22,True),fill=SOFT)
 canvas.save(R/'social'/'instagram'/f'{i:02d}_dating_algorithm_3x4.jpg',quality=91)
# FB / YT banners
for filename,sz,headline in [('facebook_1600x900.jpg',(1600,900),'WELCOME TO MY TED TALK ON DATING'),('youtube_thumb_1280x720.jpg',(1280,720),'THE DATING ALGORITHM')]:
 w,h=sz;back=ImageOps.fit(hero,sz,method=Image.Resampling.LANCZOS,centering=(.5,.5)).convert('RGBA')
 over=Image.new('RGBA',sz,(0,0,0,0));d=ImageDraw.Draw(over)
 d.rectangle((0,h*.55,w,h),fill=(6,35,29,235))
 d.text((45,int(h*.66)),headline,font=ft(int(w*.046),True),fill=CREAM)
 d.text((49,int(h*.84)),'CHAPTER 04  /  JASON, UNDER REVISION',font=ft(int(w*.02)),fill=PINK)
 Image.alpha_composite(back,over).convert('RGB').save(R/'social'/('facebook' if filename.startswith('facebook') else 'youtube')/filename,quality=92)
# Storyboard still images 9:16 from the same visual images
still_imgs=['01_stage_hero_PREVIS.jpg','02_presenter_profile_PREVIS.jpg','10_matching_hypothetical.png','09_funnel_original_diagram.png','11_invitation_decision_tree.png']
beat_titles=['WELCOME TO MY TED TALK','A VERY CONFIDENT MODEL','NOT AN EQUILIBRIUM','THE DATA IS MISSING','WHAT ACTUALLY MATTERS?']
for i,(stem,title) in enumerate(zip(still_imgs,beat_titles),1):
 cv=Image.new('RGB',(720,1280),DEEP);cd=ImageDraw.Draw(cv)
 im=Image.open(R/'art'/stem).convert('RGB');roi=ImageOps.fit(im,(720,790),method=Image.Resampling.LANCZOS)
 cv.paste(roi,(0,110))
 cd.text((31,32),'.json   /   04',font=ft(27,True),fill=PINK)
 cd.rectangle((0,858,720,1280),fill=DEEP)
 draw_multiline(cd,title,(42,927),ft(51,True),CREAM,650,13,3)
 cd.text((42,1188),'DATING ALGORITHM  •  ANIMATIC PROOF',font=ft(18),fill=PINK)
 cv.save(R/'video'/'stills'/f'{i:02d}.jpg',quality=90)
# Metadata
manifest={'chapter':'04','title':'Dating Algorithm','subtitle':'18_feature_importance','edition':'VERSION B / TINDER EDITION','narrative_part':'03_relationship_modeling','publication_status':'DRAFT_AUTHOR_REVIEW','source_file':source.name,'narration_status':'NOT_RECORDED','study_results_status':'NOT_PROVIDED','provenance':'Author-provided DOCX','style':{'pine':DEEP,'pink':PINK,'paper':CREAM,'glasses':'ordinary clear prescription glasses','wardrobe':'dark consultant suit'},'privacy':{'ten_tinder_participants':'anonymized labels only, consent not verified'},'print':'A5 EDITORIAL PROOF / NOT PDFX','video':'24-second ambient-only visual proof','risks':['fictional weights','unverified experiment result','academic citation verification','author publication approval']}
(R/'docs'/'metadata.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
(R/'docs'/'palette.json').write_text(json.dumps({'deep_pine':DEEP,'coral_pink':PINK,'old_paper':CREAM,'ink':INK,'gold':GOLD},indent=2),encoding='utf-8')
(R/'docs'/'README_ASSETS.md').write_text('''# Dating Algorithm — art asset provenance

The selected storyboard and formal-stage treatment are from an AI-generated chapter moodboard approved in this conversation. The individual photographed-looking stage scenes here are **cropped and enlarged previsualizations**, not separately rendered/layered 300-ppi print masters. Original, editable high-resolution illustration can replace these assets in a final production pass.

The main cover visually features a consultant-style speaker wearing **ordinary clear glasses** (not sunglasses), in a dark suit with green board and large pink heart. The brand/look is editorial illustration, not a real TED event.


author approval needed before distributing the book or public site. No screenshots or identities of actual Tinder participants are in the kit.
''',encoding='utf-8')
print('stage1 ok',len(paragraphs),len(main),'bytes')
