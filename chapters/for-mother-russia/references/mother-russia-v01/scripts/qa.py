from pathlib import Path
import json,subprocess,zipfile,base64,re
import fitz
from PIL import Image,ImageOps,ImageDraw
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
checks={}
pdf=fitz.open(str(R/'book/03_For_Mother_Russia_A5_EDITORIAL_PROOF.pdf'))
checks['pdf_pages']=len(pdf)
checks['pdf_full_ending']='Anw, chúc mừng muộn Ngày Chiến Thắng' in ''.join(p.get_text() for p in pdf)
checks['pdf_first_page_contains_cover_image']=bool(pdf[0].get_images())
checks['a5_dimensions_points']=[round(pdf[0].rect.width,1),round(pdf[0].rect.height,1)]
checks['social_cards']={p.name:Image.open(p).size for p in sorted((R/'social/instagram').glob('*.jpg'))}
cmd=['ffprobe','-v','error','-show_entries','stream=codec_name,width,height','-show_entries','format=duration','-of','json',str(R/'video/03_Mother_Russia_ANIMATIC_9x16.mp4')]
checks['video']=json.loads(subprocess.check_output(cmd,text=True))
with sync_playwright() as p:
 for (label,w,h) in [('desktop',1440,900),('mobile',390,844)]:
  browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
  errors=[];page.on('pageerror',lambda x: errors.append(str(x)))
  html_doc=(R/'web/index.html').read_text()
  def inline_ref(name):
   path=R/'web'/name; encoded=base64.b64encode(path.read_bytes()).decode();return 'data:image/jpeg;base64,'+encoded
  html_doc=re.sub(r'assets/[A-Za-z0-9_]+\.jpg',lambda m:inline_ref(m.group(0)),html_doc)
  page.set_content(html_doc,wait_until='load')
  page.locator('#read').scroll_into_view_if_needed()
  expected=len((R/'manuscript/original.md').read_text().split('\n\n'))-1
  checks[f'{label}_story_paragraphs']=page.locator('#story > p').count()
  page.locator('[data-v="original"]').click()
  checks[f'{label}_original_para']=page.locator('#story > p').count()
  page.locator('button').filter(has_text='Salad Nga').first.click()
  checks[f'{label}_node_selection']='Salad Nga' in page.locator('#node-title').inner_text()
  checks[f'{label}_gallery_count']=page.locator('#gallery-items > figure').count()
  checks[f'{label}_horizontal_overflow']=page.evaluate('document.documentElement.scrollWidth > innerWidth')
  checks[f'{label}_page_errors']=errors
  board=(R/'docs/PROJECT_BOARD.html').read_text(); art=R/'art/01_HERO_beanie_Gau_blue_winter.jpg';board=board.replace('../art/01_HERO_beanie_Gau_blue_winter.jpg','data:image/jpeg;base64,'+base64.b64encode(art.read_bytes()).decode());page.goto("about:blank");page.set_content(board)
  checks[f'{label}_board_count']=page.locator('#tasks article').count()
  page.locator('#q').fill('animatic')
  checks[f'{label}_board_search']=page.locator('#tasks article').count()>0
  page.goto("about:blank");page.set_content(html_doc)
  page.screenshot(path=str(R/f'previews/website_{label}.png'),full_page=False)
  browser.close()
(R/'docs/QA_REPORT.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in checks.items() if k in ['pdf_pages','pdf_full_ending','pdf_first_page_contains_cover_image','desktop_story_paragraphs','mobile_story_paragraphs','desktop_node_selection','mobile_node_selection','desktop_horizontal_overflow','mobile_horizontal_overflow','desktop_board_count','mobile_board_count','desktop_page_errors','mobile_page_errors']},indent=2))
