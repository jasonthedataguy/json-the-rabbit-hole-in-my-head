"""Check shared aperture geometry, the image-placement studio and portable SVG export."""
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--browser')
parser.add_argument('--site',default='http://127.0.0.1:4173/')
parser.add_argument('--studio',default='http://127.0.0.1:4174/docs/PORTAL_STUDIO.html')
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
output=root/'.build/portal-art-qa';output.mkdir(parents=True,exist_ok=True)
errors=[]

def centred(page,picture,frame):
    a=page.locator(picture).bounding_box();b=page.locator(frame).bounding_box()
    assert abs(a['x']+a['width']/2-b['x']-b['width']/2)<.2
    assert abs(a['y']+a['height']/2-b['y']-b['height']/2)<.2

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,**({'executable_path':args.browser} if args.browser else {}))
    page=browser.new_page(viewport={'width':1440,'height':1000})
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(args.site,wait_until='networkidle')
    centred(page,'#cover-scene','#cover-stage')
    expect(page.locator('#cover-scene image')).to_have_attribute('href','assets/cover-scene-landscape.png')
    expect(page.locator('#cover-rotor image')).to_have_attribute('href','assets/board-cover-ring.png?v=2')
    expect(page.locator('#cover-rotor mask')).to_have_count(0)
    assert page.locator('#cover-rotor').evaluate('(el)=>getComputedStyle(el).maskImage')=='none'
    page.evaluate("window.__homepageRing = document.querySelector('#cover-rotor svg')")
    page.screenshot(path=str(output/'cover-desktop.png'),full_page=True)
    page.locator('#cover-next').click()
    expect(page.locator('#cover-stage')).to_have_attribute('data-page-index','1')
    expect(page.locator('#cover-scene image')).to_have_attribute('href','assets/introduction-scene.png')
    expect(page.locator('#cover-rotor image')).to_have_attribute('href','assets/board-cover-ring.png?v=2')
    page.screenshot(path=str(output/'introduction-desktop.png'),full_page=True)
    page.locator('#cover-next').click()
    expect(page.locator('#cover-stage')).to_have_attribute('data-page-index','2')
    expect(page.locator('#cover-scene image')).to_have_attribute('href','assets/rice-scene-v2.png')
    expect(page.locator('#cover-rotor image')).to_have_attribute('href','assets/board-cover-ring.png?v=2')
    assert page.evaluate("window.__homepageRing === document.querySelector('#cover-rotor svg')")
    centred(page,'#cover-scene','#cover-stage')
    assert page.locator('#cover-scene>.fitted-portal-picture').evaluate('(el)=>getComputedStyle(el).transform')=='none'
    page.screenshot(path=str(output/'rice-desktop.png'),full_page=True)
    page.goto(args.site+'#map',wait_until='networkidle')
    page.locator('#portal-stage').focus();page.keyboard.press('Home')
    centred(page,'#portal-scene','#portal-art')
    page.screenshot(path=str(output/'rice-map.png'),full_page=True)
    page.goto(args.site+'#chapter/00',wait_until='networkidle')
    centred(page,'.fitted-portal-slot','.fitted-portal')
    page.screenshot(path=str(output/'rice-reader.png'))
    page.set_viewport_size({'width':390,'height':844})
    page.goto(args.site,wait_until='networkidle')
    centred(page,'#cover-scene','#cover-stage')
    page.screenshot(path=str(output/'cover-mobile.png'),full_page=True)
    page.locator('#cover-next').click();page.locator('#cover-next').click()
    centred(page,'#cover-scene','#cover-stage')
    page.screenshot(path=str(output/'rice-mobile.png'),full_page=True)

    page.set_viewport_size({'width':1440,'height':1000})
    page.goto(args.studio,wait_until='networkidle')
    centred(page,'#picture','#preview')
    expect(page.locator('#frame image')).to_have_attribute('href','../shared/artwork/portal/board-cover-ring.png?v=2')
    page.select_option('#preset','placeholder')
    expect(page.locator('#picture image')).to_have_attribute('href','../shared/artwork/portal/placeholder.svg')
    expect(page.locator('#frame image')).to_have_attribute('href','../shared/artwork/portal/board-ring-cut.png')
    page.screenshot(path=str(output/'template-placeholder.png'),full_page=True)
    page.select_option('#preset','rice')
    expect(page.locator('#zoom')).to_have_value('1')
    expect(page.locator('#x')).to_have_value('0')
    page.locator('#rotation').fill('73');page.locator('#rotation').dispatch_event('input')
    centred(page,'#picture','#preview')
    page.screenshot(path=str(output/'template-rice.png'),full_page=True)
    page.locator('#file').set_input_files(str(root/'shared/artwork/book-cover/cover-scene-landscape.png'))
    expect(page.locator('#status')).to_contain_text('Loaded')
    page.locator('#zoom').fill('1.2');page.locator('#zoom').dispatch_event('input')
    page.locator('#x').fill('-8');page.locator('#x').dispatch_event('input')
    with page.expect_download() as result:page.locator('#download').click()
    destination=output/'exported-portal.svg';result.value.save_as(destination)
    document=ET.parse(destination).getroot()
    images=document.findall('.//{http://www.w3.org/2000/svg}image')
    assert len(images)==2
    assert all(image.attrib['href'].startswith('data:image/') for image in images)
    assert document.attrib['viewBox']=='0 0 1000 1000'
    assert 'guides' not in destination.read_text(encoding='utf-8')
    page.goto(destination.as_uri(),wait_until='networkidle')
    page.screenshot(path=str(output/'exported-portal.png'))
    browser.close()
assert not errors,errors
print('Passed: centred desktop/mobile apertures, map/reader fit, placeholder, upload, adjustments and self-contained SVG export.')
