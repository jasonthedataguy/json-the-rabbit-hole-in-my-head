from pathlib import Path
import base64
import json, os, zipfile, subprocess
from PIL import Image
import fitz
root=Path(__file__).resolve().parents[1]
result={}
pdf=fitz.open(str(root/'book'/'06_The_Gioi_Trong_Mo_A5_EDITORIAL_PROOF.pdf'))
whole=' '.join(p.get_text() for p in pdf)
result['a5_pages']=len(pdf)
result['source_ending_preserved']='Chỉ biết rằng tôi luôn tìm thấy chúng, và chúng cũng luôn tìm thấy tôi.' in whole
result['pdf_page_dimensions_A5']=all(abs(p.rect.width-419.53)<1 and abs(p.rect.height-595.28)<1 for p in pdf)
result['instagram_dimensions']={p.name:Image.open(p).size for p in (root/'social/instagram').glob('*.jpg')}
result['video']=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height','-show_entries','format=duration','-of','json',str(root/'video'/'06_The_Gioi_Trong_Mo_ANIMATIC_9x16.mp4')]))
result['source_paragraphs']=len((root/'manuscript'/'ORIGINAL_UNCHANGED.md').read_text().strip().split('\n\n'))-1
result['task_count']=len(json.loads((root/'docs'/'TASKS.json').read_text()))
assert result['source_paragraphs']==19 and result['task_count']==72 and result['source_ending_preserved'] and result['pdf_page_dimensions_A5']
assert all(x==(1080,1440) for x in result['instagram_dimensions'].values())
assert float(result['video']['format']['duration'])==24
assert {'h264','aac'}=={x['codec_name'] for x in result['video']['streams']}
try:
 from playwright.sync_api import sync_playwright
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
  result['browser']={}
  def image_data(path):
   return 'data:image/jpeg;base64,'+base64.b64encode(path.read_bytes()).decode('ascii')
  css=(root/'web'/'styles.css').read_text()
  js=(root/'web'/'app.js').read_text()
  for im in (root/'web'/'assets').glob('*.jpg'):
   css=css.replace('assets/'+im.name,image_data(im))
   js=js.replace('assets/'+im.name,image_data(im))
  site=(root/'web'/'index.html').read_text().replace('<link rel="stylesheet" href="styles.css">','<style>'+css+'</style>').replace('<script src="app.js"></script>','<script>'+js+'</script>')
  site=site.replace('src="assets/observed.jpg"','src="'+image_data(root/'web'/'assets'/'observed.jpg')+'"')
  board=(root/'docs'/'PROJECT_BOARD.html').read_text().replace('src="assets/visual_board.jpg"','src="'+image_data(root/'docs'/'assets'/'visual_board.jpg')+'"')
  for viewport in [(1440,900),(390,844)]:
   ctx=browser.new_context(viewport={'width':viewport[0],'height':viewport[1]})
   page=ctx.new_page();errs=[];page.on('pageerror',lambda e:errs.append(str(e)))
   page.set_content(site,wait_until='load')
   page.wait_for_timeout(150)
   initial=page.locator('#article p').count()
   page.locator('[data-layer="imagined"]').click()
   imaginary=page.locator('#layer-title').inner_text()
   page.locator('[data-layer="afterimage"]').click()
   afterimage=page.locator('#layer-title').inner_text()
   page.locator('#grade').fill('90')
   grade=page.locator('#grade-val').inner_text()
   horizontal=page.evaluate('document.documentElement.scrollWidth>window.innerWidth')
   shot=root/'previews'/('website_desktop.png' if viewport[0]>600 else 'website_mobile.png')
   page.screenshot(path=str(shot),full_page=False)
   result['browser'][f'{viewport[0]}x{viewport[1]}']={'paragraphs':initial,'imagined':imaginary,'afterimage':afterimage,'grade':grade,'horizontal_overflow':horizontal,'page_errors':errs}
   print('webQA', viewport, result['browser'][f'{viewport[0]}x{viewport[1]}']); assert initial==19 and 'dinner' in imaginary.lower() and grade=='90%' and not horizontal and not errs
   page.set_content(board,wait_until='load')
   count=page.locator('.item').count()
   page.locator('#search').fill('Bastille')
   matches=page.locator('.item').count()
   page.locator('#search').fill('')
   page.locator('.item select').first.select_option('IN_PROGRESS')
   page.screenshot(path=str(root/'previews'/('board_desktop.png' if viewport[0]>600 else 'board_mobile.png')))
   result['browser'][f'{viewport[0]}x{viewport[1]}'].update({'board_task_count':count,'board_search_matches':matches})
   assert count==72 and matches>0
   ctx.close()
  browser.close()
except Exception as e:
 result['browser_error']=repr(e)
 if isinstance(e,AssertionError):raise
(root/'docs'/'QA_REPORT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,default=list)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2,default=list))
