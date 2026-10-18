"""Browser regression checks. Requires Playwright; run against a built local site."""
import argparse
import json
import math
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--url', default='http://127.0.0.1:4173/')
parser.add_argument('--browser', help='Optional Chromium executable')
parser.add_argument('--output', default='.build/browser-qa')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
output = Path(args.output); output.mkdir(parents=True, exist_ok=True)
base = args.url.rstrip('/') + '/'
errors, failed = [], []

def selected(page, index):
    stage = page.locator('#cover-stage')
    expect(stage).to_have_attribute('data-page-index', str(index))
    expect(page.locator(f'[data-cover-page="{index}"]')).to_have_attribute('aria-pressed', 'true')
    route = '#introduction' if index < 2 else '#chapter/' + f'{index - 2:02d}'
    expect(page.locator('#cover-chapter-link')).to_have_attribute('href', route)
    assert page.locator('#cover-scene').evaluate('(el)=>getComputedStyle(el).transform') == 'none'

def no_overflow(page):
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), page.url

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, **({'executable_path': args.browser} if args.browser else {}))
    context = browser.new_context(viewport={'width': 1440, 'height': 1000})
    context.route('**/*', lambda route: route.continue_() if route.request.url.startswith(base) or route.request.url.startswith('data:') else route.abort())
    page = context.new_page()
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('response', lambda r: failed.append([r.status, r.url]) if r.status >= 400 else None)
    page.goto(base, wait_until='networkidle')
    expect(page.locator('.cover-orbit-mark')).to_have_count(35)
    selected(page, 0)
    expect(page.locator('#cover-scene image')).to_have_attribute('href', 'assets/cover-scene-landscape.png')
    expect(page.locator('#cover-chapter-label')).to_have_text('Book cover')
    page.screenshot(path=str(output / 'cover-desktop.png'), full_page=True)
    page.locator('#cover-next').click(); selected(page, 1)
    expect(page.locator('#cover-chapter-label')).to_have_text('Introduction')
    page.screenshot(path=str(output / 'ring-introduction-desktop.png'), full_page=True)
    page.locator('#cover-next').click(); selected(page, 2)
    expect(page.locator('#cover-chapter-label')).to_have_text('00 · Cold Rice')
    expect(page.locator('#cover-scene image')).to_have_attribute('href', 'assets/rice-scene-v2.png')
    page.screenshot(path=str(output / 'ring-rice-desktop.png'), full_page=True)
    page.locator('#cover-prev').click(); selected(page, 1)
    page.locator('#cover-stage').focus()
    page.keyboard.press('Home'); selected(page, 0)
    for index in range(1, 36):
        page.keyboard.press('ArrowRight'); selected(page, index % 35)
    page.keyboard.press('ArrowLeft'); selected(page, 34)
    page.keyboard.press('Home')
    box = page.locator('#cover-stage').bounding_box()
    cx, cy, radius = box['x']+box['width']/2, box['y']+box['height']/2, box['width']*.38
    page.mouse.move(cx+radius,cy); page.mouse.down()
    for step in range(1, 21):
        angle = math.radians(-5*360/35*step/20)
        page.mouse.move(cx+radius*math.cos(angle),cy+radius*math.sin(angle))
    selected(page, 5)  # Live update before release.
    page.mouse.up(); selected(page, 5)
    page.mouse.move(cx,cy); page.mouse.wheel(0,100); selected(page, 6)
    page.wait_for_timeout(250)
    page.locator('[data-cover-page="1"]').click(); selected(page, 1)
    page.locator('#cover-stage').focus(); page.keyboard.press('Enter')
    expect(page.locator('#intro-heading')).to_have_text('Introduction')
    expect(page.locator('#introduction-text h2')).to_have_text(['Tác phẩm trong một câu', 'Giới thiệu nội dung', 'Lời hứa dành cho độc giả'])
    expect(page.locator('#introduction-text em')).to_have_text('.json')
    expect(page.locator('#introduction-view .book-subtitle')).to_have_text('Jason, under revision')
    expect(page.locator('#introduction-view .title-author')).to_have_count(0)
    expect(page.locator('.intro-leaf-navigation .next-leaf')).to_have_attribute('href','#chapter/00')
    page.screenshot(path=str(output / 'introduction-desktop.png'), full_page=True)
    page.locator('.book-brand').click(); selected(page,0)
    page.locator('#cover-stage').focus(); page.keyboard.press('Enter')
    expect(page).to_have_url(base+'#introduction')

    library = json.loads((root/'dist/content/manuscripts.json').read_text(encoding='utf-8'))
    assert next(c for c in library['chapters'] if c['slug']=='dating-102')['editorialId']=='19'
    page.goto(base+'#chapter/19', wait_until='networkidle')
    expect(page.locator('#chapter-heading')).to_have_text('Dating 102')
    expect(page.locator('.chapter-prose')).to_be_visible()
    expect(page.locator('.chapter-nav-link[href="#chapter/19"] .nav-chapter-icon svg')).to_have_count(1)
    expect(page.locator('.next-leaf')).to_have_attribute('href','#chapter/20')
    page.goto(base+'#chapter/18', wait_until='networkidle')
    expect(page.locator('.next-leaf')).to_have_attribute('href','#chapter/19')
    page.goto(base+'#contents', wait_until='networkidle')
    expect(page.locator('.toc-row[href="#chapter/19"] .toc-title')).to_have_text('Dating 102')
    expect(page.locator('.toc-row[href="#archive/dating-102"]')).to_have_count(0)
    for chapter in library['chapters']:
        route = '#chapter/'+chapter['editorialId'] if chapter['editorialId'] is not None else '#archive/'+chapter['slug']
        page.goto(base+route, wait_until='networkidle')
        expect(page.locator('#chapter-heading')).to_have_text(chapter['title'])
        normalized = page.evaluate('(html)=>{const el=document.createElement("div");el.innerHTML=html;return el.innerHTML}',chapter['bodyHtml'])
        expect(page.locator('.chapter-prose')).to_have_js_property('innerHTML', normalized)
        assert page.locator('.chapter-prose').evaluate('(el)=>getComputedStyle(el).fontFamily').startswith('"Noto Serif"')
        assert page.evaluate('document.fonts.check(\'22px "Noto Serif"\')')
        assert context.request.get(base+chapter['downloadUrl']).body() == (root/chapter['sourcePath']).read_bytes()
        no_overflow(page)
        if chapter['editorialId']=='00':
            page.screenshot(path=str(output / 'reader-desktop.png'))
            page.locator('.chapter-prose').scroll_into_view_if_needed()
            page.screenshot(path=str(output / 'prose-desktop.png'))
    page.goto(base+'#chapter/31',wait_until='networkidle')
    no_overflow(page)
    page.screenshot(path=str(output/'long-title-desktop.png'))
    page.goto(base+'#map',wait_until='networkidle')
    page.locator('#portal-stage').focus();page.keyboard.press('Home')
    expect(page.locator('#map-number')).to_have_text('00')
    page.keyboard.press('End');expect(page.locator('#map-number')).to_have_text('32')
    page.keyboard.press('ArrowRight');expect(page.locator('#map-number')).to_have_text('00')

    phone = browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,reduced_motion='reduce')
    mobile = phone.new_page()
    mobile.on('pageerror', lambda e: errors.append(str(e)))
    mobile.goto(base,wait_until='networkidle');selected(mobile,0);no_overflow(mobile)
    mobile.screenshot(path=str(output/'cover-mobile.png'),full_page=True)
    box=mobile.locator('#cover-stage').bounding_box()
    cx,cy=box['x']+box['width']/2,box['y']+box['height']/2
    touch=phone.new_cdp_session(mobile)
    touch.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':cx,'y':cy}]})
    touch.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':cx-60,'y':cy}]})
    touch.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    selected(mobile,1)
    assert mobile.locator('#cover-rotor').evaluate('(el)=>getComputedStyle(el).transitionDuration')=='0s'
    mobile.locator('#cover-next').click();selected(mobile,2)
    mobile.locator('#cover-chapter-link').click()
    expect(mobile.locator('#chapter-heading')).to_have_text('Cold Rice');no_overflow(mobile)
    mobile.screenshot(path=str(output/'reader-mobile.png'))
    mobile.set_viewport_size({'width':320,'height':740})
    mobile.goto(base,wait_until='networkidle');selected(mobile,0);no_overflow(mobile)
    mobile.screenshot(path=str(output/'cover-small.png'),full_page=True)
    browser.close()
assert not errors, errors
assert not failed, failed
print(json.dumps({'result':'passed','cover_stops':35,'manuscripts_unchanged':len(library['chapters']),'browser_errors':errors,'http_failures':failed,'screenshots':str(output)},indent=2))
