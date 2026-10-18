from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess,fitz,math,json,csv,shutil,zipfile,hashlib
O=Path(__file__).resolve().parents[1]
# contact-sheet preview
with fitz.open(O/'book/02_Fashion_Room_in_Revision_A5_PROOF.pdf') as p:
 ims=[]
 for page in p:
  pix=page.get_pixmap(matrix=fitz.Matrix(.6,.6),alpha=False)
  ims.append(Image.frombytes('RGB',(pix.width,pix.height),pix.samples))
 w,h=ims[0].size;sheet=Image.new('RGB',(3*w,3*h),'#f5ebd8')
 for i,im in enumerate(ims):sheet.paste(im,((i%3)*w,(i//3)*h))
 sheet.save(O/'previews/pdf_contact_sheet.jpg',quality=86)
images=[Image.open(p).convert('RGB') for p in sorted((O/'social/instagram').glob('slide_*'))];k=0.31
th=[im.resize((int(im.width*k),int(im.height*k))) for im in images]
s=Image.new('RGB',(len(th)*th[0].width,th[0].height),'#062f26')
for i,im in enumerate(th):s.paste(im,(i*im.width,0))
s.save(O/'previews/social_contact_sheet.jpg',quality=90)
# video uses slide images only, no fabricated narration
lst=O/'video/frames/concat.txt'
with lst.open('w') as f:
 for p in sorted((O/'video/frames').glob('frame_*.jpg')):
  f.write("file '%s'\nduration 4.8\n"%p.name)
 f.write("file '%s'\n"%sorted((O/'video/frames').glob('frame_*.jpg'))[-1].name)
cmd=['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(lst),'-stream_loop','-1','-i',str(O/'video/ambient_synthetic.wav'),'-t','24','-r','24','-vf','scale=720:1280,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','26','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-shortest',str(O/'video/02_Fashion_RoomInRevision_ANIMATIC_9x16.mp4')]
subprocess.run(cmd,check=True,timeout=160)
# landscape YouTube proof: distinct aspect ratio, no fake 3-minute full film
from PIL import ImageOps
frames=[]
sources=[O/'assets/master/05_WIDE_HERO.png',O/'assets/illustrations/scene_01.jpg',O/'assets/illustrations/scene_03.jpg',O/'assets/illustrations/scene_05.jpg',O/'assets/illustrations/scene_06.jpg']
for i,source in enumerate(sources,1):
 img=Image.open(source).convert('RGB'); img=ImageOps.fit(img,(1280,720),method=Image.Resampling.LANCZOS,centering=(.5,.5))
 target=O/f'video/frames/landscape_{i:02}.jpg';img.save(target,quality=85);frames.append(target)
lst2=O/'video/frames/landscape_concat.txt'
with lst2.open('w') as f:
 for p in frames:f.write("file '%s'\nduration 4.8\n"%p.name)
 f.write("file '%s'\n"%frames[-1].name)
cmd=['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(lst2),'-stream_loop','-1','-i',str(O/'video/ambient_synthetic.wav'),'-t','24','-r','24','-vf','scale=1280:720,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','26','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-shortest',str(O/'video/02_Fashion_YouTube_LANDSCAPE_ANIMATIC_16x9.mp4')]
subprocess.run(cmd,check=True,timeout=160)
# Textual artifacts
(O/'video/STORYBOARD.md').write_text('''# .json / Fashion — video storyboard v0.2

**Two exports are 24-second image-sequence proofs with synthetic ambient audio, not finished narrated videos.** No unlicensed music, endorsements, artist audio, or fake documentary footage.

| Time | Visual | Narrative beat |
|---|---|---|
| 00–04.8 | Album-cover wardrobe room | A small room, a bigger tomorrow |
| 04.8–09.6 | Sneaker detail | The winter dream of a new drop |
| 09.6–14.4 | Rulebook/wardrobe | Fashion rules learned from others |
| 14.4–19.2 | Worn clothes and marks | Wear becomes evidence of living |
| 19.2–24 | Dad's side of wardrobe | Be your own label, not a hanger |

## Final production to do

Record an approved 50–75 second reading of the chosen chapter excerpt, timestamp the transcript to actual voice, create VN SRT and export 1080×1920 with platform-safe subtitles. Consider a separate **16:9 longform YouTube narrative**, not simply the existing landscape 24-second ambient visual. Current VTT/SRT is intentionally absent: generating timed spoken subtitles without speech would be misleading.
''',encoding='utf-8')
(O/'video/NARRATION_DRAFT.md').write_text('''# Fashion / proposed 60-second voiceover (not recorded)

Hồi trẻ tôi chỉ có một ước mơ rất đơn giản: hustle học hành, kiếm tiền, rồi mỗi mùa đông tự thưởng cho mình một đôi sneakers trendy nhất season.

NMD, Yeezy, rồi đủ thứ high-end street fashion. Tôi nghĩ một đôi giày hay một cái jacket có thể nói hộ identity của mình.

Sau này, tôi bắt đầu thấy buồn cười với những rulebook: techwear thì phải thế này, món này tuyệt đối không được mix với món kia. Nhưng ngày trước chính tôi cũng như vậy.

Style chắc phải bắt đầu từ việc copy, thử, bớt đi, rồi giữ lại thứ thật sự hợp với mình.

Giờ tôi thích một món đồ đủ tốt để mặc thật lâu. Vài vết stain, chỗ bạc màu, vài đường chỉ lệch lại trở thành câu chuyện của chính nó.

Và có khi, một hidden gem nằm trong tủ đồ của bố hai mươi năm còn thú vị hơn một item mới tinh.

Be your own label, not a hanger, my man.

---

Draft script only. Timings, subtitles, and audio rights will be finalized after a real recording. May be edited for cadence, not newly invented memoir events.
''',encoding='utf-8')
(O/'social/instagram_caption.md').write_text('''# Instagram caption / DRAFT — NOT POSTED

Một thời, ước mơ mỗi mùa đông của tôi là một đôi sneakers trendy nhất season. Bây giờ lại thấy cái áo cũ trong tủ bố thú vị hơn một brand-new drop.

Trend có thể đổi mỗi season, nhưng style thì phải được mặc lên người, đi qua vài chuyện, bạc màu một chút — rồi mới thành của mình.

**Be your own label, not a hanger, my man.**

Fashion / .json — Jason, under revision. Chapter draft pending editorial and artwork approval.

**Slides:** Cover → The Drop → Whose Rulebook → Patina → Hidden Gem. **Aspect:** 3:4 1080×1440. Alternative 4:5/1:1 included.

#jsonunderrevision #Fashion #Streetwear #Memoir
''',encoding='utf-8')
(O/'social/facebook_post.md').write_text('''# Facebook Page post / DRAFT — NOT POSTED

Hồi trẻ, ước mơ của tôi là cứ đến mùa đông sẽ có tiền mua đôi sneakers hot nhất season. Hình như khi bản thân chưa biết mình là ai, một logo đúng trend cũng giúp người ta cảm thấy mình thuộc về một nhóm nào đó.

Nhưng càng lớn, tôi càng thấy thú vị với những dấu vết cũ: một cái áo bạc màu, đường chỉ bị sờn, một món đồ đã nằm trong tủ của bố hai mươi năm.

Có thể fashion chưa bao giờ chỉ là mặc đẹp. Nó còn là những gì một người đi qua trong bộ quần áo ấy.

**Be your own label, not a hanger, my man.**

Fashion — một chương của .json, Jason, under revision. Link sẽ được cập nhật khi chương chính thức được duyệt xuất bản.
''',encoding='utf-8')
(O/'social/tiktok_youtube.md').write_text('''# TikTok, Reels, YouTube / distribution package — DRAFT

- Hook: “My best fashion find might be twenty years old.”
- TikTok / Reels caption: “From sneaker drops to Dad's wardrobe. Be your own label.”
- YouTube Short title: “Fashion: Be your own label | .json / 02”
- YouTube description: “An illustrated Vietnamese/Vinglish memoir about hip-hop streetwear, trend cycles, and finding style beyond labels. Official reading link: TBD.”
- Vertical cover: social/instagram/slide_01_3x4.jpg (requires a separate 9:16 crop for video thumbnail).
- Video status: **24s silent-narration / ambient-only animatic**. No actual voice, synced SRT or uploaded post.
- Longform YouTube: 16:9 24-second **landscape ambient proof**, not a 3–5 minute narrated episode.
- Final uploads require approved public excerpt, commercial use and music/graphic rights; platform account access.
''',encoding='utf-8')
(O/'docs/EDITOR_NOTES.md').write_text((O/'docs/EDITOR_NOTES.md').read_text(),encoding='utf-8')
(O/'docs/ART_DIRECTION.md').write_text('''# Fashion — A Room in Revision / v0.2 visual system

## Selected hero
The user-provided album-cover direction is the authoritative **visual concept**: a young narrator sitting among old sneaker boxes, a glowing city window, a wardrobe of mixed-era garments, father's shelf and a loud pink 'FASHION' title inside cream-edged dark green framing.

## Colour and type
- Deep bottle / pine green: `#062F26`
- Fluorescent dusty pink: `#F47EAC`
- Yellowed publication paper: `#F5EBD8`
- Ink shadow: `#0F1E1A`
- Denim blue-grey: `#72838A`
- Sunset pink-peach: `#E9A29B`
- Faded leather: `#BB807C`

Use rough print grain, flawed registration, brush-like pink headlines, documentary-looking room composition, imperfect film print texture. Do **not** clone a named contemporary living artist. All derivative exports in this kit are crops/layout compositions of the **specific artwork supplied by the author**. Other variant renders are mockups, not actual purchased/printed products.

## Literary anchors
Hip-hop/sneaker ambition → consumer trend cycle → borrowed fashion rulebook → personal remix → marks/stains → father's closet / hidden gem.

## Packaging
Book: A5 cream paper + art inserts. Web: poster hero, manuscript toggle, six-stop interactive Wardrobe Explorer, ambient preview accurately labeled. Social: five 3:4 chapter carousel cards plus 4:5/1:1; video frames 9:16; FB/YouTube landscape crops. PDF/X and commercial printing not performed.

## Rights
The supplied poster artwork visually includes recognizable sneaker/brand marks and framed imagery. Clear any third-party artwork, photograph, marks or likeness reproduction before commercial distribution; references in the text are not product endorsements. Dad's wardrobe is illustrative, not an authenticated source photograph.
''',encoding='utf-8')
(O/'docs/QA_REPORT.md').write_text('''# QA report — Fashion v0.2

- A5 PDF: built programmatically from the approved-to-edit proposed draft, full 14-paragraph essay retained, source ending `Peace and love!` preserved. **Editorial proof, not printer-ready**.
- Visual concept: five user-selected source renders in `assets/master/` and six story-detail plates; print/social/web crops created from those supplied images.
- Website: offline static HTML/JS with the complete original and proposed draft, **six working interactions**, ambient preview; no tracking/payments. Real-device and browser QA needed if not recorded below.
- Social: five 1080×1440 JPG cards, 1080×1350 feed crop, 1080×1080 square, 1600×900 Facebook, 1280×720 YouTube.
- Videos: two **24-second** ambient proofs, one vertical 720×1280 and one horizontal 1280×720. No voice; no subtitles synchronized to speech.
- Rights: commercial use of visible logos, wall posters, possible likenesses and music needs clearance. Do not release based only on selected creative direction.
- Author editorial and publication approvals are separate gates.
''',encoding='utf-8')
# 64 task board from v01 as baseline, update evidence to v02 and use honest statuses
source=json.loads((Path('/mnt/data/fashion_chapter_v01/docs/TASKS.json')).read_text())
for t in source:
 if any(x in t['task'].lower() for x in ['original','source','metadata','illustration','poster','visual','proof','website','wardrobe','interactive','instagram','facebook','youtube thumbnail','storyboard','video animatic','video proof','social caption','qa review','checklist']):
  if t['status'] in ('TODO','BLOCKED'):t['status']='PROOF'
 # ensure external release gates remain blocked
 if any(x in t['task'].lower() for x in ['publish','printer','press-ready','pdf/x','narrat','consent','approval','record voice','subtitle','deploy','print ready','merge','qr','license','rights']):t['status']='BLOCKED'
counts={x:sum(t['status']==x for t in source) for x in ('READY','PROOF','TODO','BLOCKED','IN_PROGRESS')}
(O/'docs/TASKS.json').write_text(json.dumps(source,ensure_ascii=False,indent=2))
with (O/'docs/CHECKLIST.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=['id','stream','task','status','owner','priority']);w.writeheader();w.writerows(source)
(O/'docs/PROJECT_BOARD.md').write_text('# .json — Fashion / Full project board v0.2\n\n**Visual:** A Room in Revision — bottle green / pink / cream.\n\n**Status:** private author-review, not deployed.\n\n**64 tracked tasks:** '+', '.join(f'{k} {v}' for k,v in counts.items() if v)+'\n\n'+''.join(f'## {stream}\n\n'+''.join(f'- [ ] **{t["id"]} · {t["task"]}** — {t["status"]} · {t["priority"]} · {t["owner"]}\n' for t in source if t['stream']==stream)+'\n' for stream in dict.fromkeys(t['stream'] for t in source))+'\n## Release gates\nApprove manuscript and poster copyright/trademark/likeness use; record narration and timed subtitles; obtain print vendor specifications; test HTTPS site/QR; approve social channel upload.\n',encoding='utf-8')
# project board locally functional with search/status/edit/export
board='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>.json / Fashion — production board</title><style>:root{--green:#062f26;--pink:#f47eac;--paper:#f5ebd8}*{box-sizing:border-box}body{margin:0;background:var(--green);color:var(--paper);font:15px/1.6 system-ui,sans-serif}header{background:linear-gradient(90deg,rgba(6,47,38,.8),rgba(6,47,38,.1)),url('../assets/master/05_WIDE_HERO.png') center/cover;padding:5rem 6vw;min-height:350px}h1{font-size:clamp(3rem,9vw,8rem);font-style:italic;letter-spacing:-.06em;color:var(--pink);margin:0}h2{margin-top:1rem}.eyebrow{font:12px monospace;letter-spacing:.16em;color:var(--pink)}.stats{display:flex;gap:12px;flex-wrap:wrap;margin:35px 0}.stat{padding:15px 22px;border:1px solid #8a576c}.stat strong{font-size:26px;display:block}.shell{padding:20px 5vw 100px}.filters{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:24px}input,select,button{background:#163d33;color:white;border:1px solid var(--pink);border-radius:0;padding:12px 14px;min-height:43px}input{flex:1;min-width:200px}button{cursor:pointer}button:hover{background:#31564a}table{width:100%;border-collapse:collapse;font-size:13px}th{text-align:left;color:var(--pink);font:11px monospace;padding:14px 10px;border-bottom:2px solid var(--pink)}td{padding:14px 10px;border-bottom:1px solid #547469;vertical-align:top}.tag{font:12px monospace;color:var(--pink)}.status{min-width:120px}footer{padding:20px 5vw;font:12px monospace}a{color:var(--pink)}@media(max-width:740px){table{display:block;overflow-x:auto;white-space:nowrap}}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}</style></head><body><header><div class="eyebrow">.JSON / CHAPTER 02 / IMMERSIVE RELEASE</div><h1>FASHION</h1><p>Full asset production board · A Room in Revision · proof, not public release.</p></header><main class="shell"><div class="stats" id="stats"></div><div class="filters"><input id="search" placeholder="Search tasks / owners / streams" aria-label="Search tasks"><select id="stream" aria-label="Filter stream"><option value="">All workstreams</option></select><select id="status" aria-label="Filter status"><option value="">All statuses</option></select><button type="button" id="export">Export CSV</button><button type="button" id="reset">Reset statuses</button></div><table><thead><tr><th>ID</th><th>Workstream</th><th>Task</th><th>Owner</th><th>Priority</th><th>Status / edit</th></tr></thead><tbody id="rows"></tbody></table></main><footer>Editable progress is saved only inside your own browser. The public GitHub PR must be updated separately. Proofs are not approved commercial releases.</footer><script src="BOARD_DATA.js"></script><script>const base=window.PROJECT_TASKS;let statusMap={};try{statusMap=JSON.parse(localStorage.getItem('fashion-board-v02')||'{}')}catch(e){}const kinds=['READY','PROOF','IN_PROGRESS','TODO','BLOCKED'];let sel=document.getElementById('stream'),state=document.getElementById('status'),search=document.getElementById('search'),rows=document.getElementById('rows');for(const st of [...new Set(base.map(t=>t.stream))]){const o=document.createElement('option');o.value=o.textContent=st;sel.append(o)}for(const st of kinds){const o=document.createElement('option');o.value=o.textContent=st;state.append(o)}function get(t){return statusMap[t.id]||t.status}function draw(){rows.replaceChildren();const q=search.value.toLowerCase();let chosen=base.filter(t=>(!q||[t.id,t.task,t.stream,t.owner].some(x=>x.toLowerCase().includes(q)))&&(!sel.value||t.stream===sel.value)&&(!state.value||get(t)===state.value));for(const t of chosen){const tr=document.createElement('tr');for(const val of [t.id,t.stream,t.task,t.owner,t.priority]){let td=document.createElement('td');td.textContent=val;tr.append(td)}let td=document.createElement('td');let input=document.createElement('select');input.className='status';input.setAttribute('aria-label','Task '+t.id+' status');for(const st of kinds){let op=document.createElement('option');op.value=op.textContent=st;input.append(op)}input.value=get(t);input.addEventListener('change',()=>{statusMap[t.id]=input.value;localStorage.setItem('fashion-board-v02',JSON.stringify(statusMap));draw()});td.append(input);tr.append(td);rows.append(tr)}const st=document.getElementById('stats');st.replaceChildren();for(const k of kinds){let b=document.createElement('div');b.className='stat';b.innerHTML='<strong>'+base.filter(x=>get(x)===k).length+'</strong>'+k;st.append(b)}let b=document.createElement('div');b.className='stat';b.innerHTML='<strong>'+chosen.length+'</strong>VISIBLE';st.append(b)}[sel,state,search].forEach(x=>x.addEventListener('input',draw));document.getElementById('reset').onclick=()=>{statusMap={};localStorage.removeItem('fashion-board-v02');draw()};document.getElementById('export').onclick=()=>{const fields=['id','stream','task','owner','priority','status'];const csv=[fields.join(','),...base.map(t=>fields.map(k=>JSON.stringify(k==='status'?get(t):t[k])).join(','))].join('\\r\\n');const url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));let a=document.createElement('a');a.href=url;a.download='fashion_status_v02.csv';a.click();URL.revokeObjectURL(url)};draw();</script></body></html>'''
(O/'docs/PROJECT_BOARD.html').write_text(board,encoding='utf-8')
(O/'docs/BOARD_DATA.js').write_text('window.PROJECT_TASKS='+json.dumps(source,ensure_ascii=False)+';',encoding='utf-8')
(O/'README.md').write_text('''# .json — Fashion · Chapter 02 / A Room in Revision

This kit is the complete **author-review production prototype** built from the five chosen forest-green/pink poster and mockup artworks.

## Open first
- `docs/PROJECT_BOARD.html` — **interactive 64-task board**, local status editing, CSV export.
- `website/index.html` — full original/proposed chapter + six-stop interactive Wardrobe Explorer. Open this file with its `assets/` directory intact; works offline.
- `book/02_Fashion_Room_in_Revision_A5_PROOF.pdf` — illustrated A5 editorial proof, **not print-ready**.
- `assets/master/` — five original uploaded selected design renders.
- `assets/illustrations/` — six storyboard panels derived from selected source art.
- `social/instagram/` — five 3:4 cards and alternate feed crops. Other social copy/art in `social/`.
- `video/` — separate 9:16 and 16:9 24-second ambient **animatics**, plus draft narration/storyboard. Neither is narrated or uploaded.
- `docs/QA_REPORT.md`, `docs/ART_DIRECTION.md`, `docs/METADATA.json`, `docs/CHECKLIST.csv` — QA, design system, publish controls and task ledger.

## Important release distinction
Approval of this design is not approval of publishing the full manuscript or recognizable third-party marks/photos. The art includes logos and wall-poster-like material that must be checked for commercial release. Other real-world descriptions and chronology also deserve author review. The website is a **local review prototype**; no live site or social platform was changed.

## For the real book release
Approve canonical text, obtain licensed/authorized voice, create timed subtitles, verify artwork rights, get printer PDF/X/color/gutter requirements, test final QR and deploy verified site; post to accounts only after author authorization.

## Repo
`jasonthedataguy/json-under-revision` — all files are kept locally here until verified safe for public GitHub. The review PR tracks source, design decisions and import instructions.
''',encoding='utf-8')
# build_assets.py is included as an independent script
print('Video/social/docs generated; statuses',counts)
