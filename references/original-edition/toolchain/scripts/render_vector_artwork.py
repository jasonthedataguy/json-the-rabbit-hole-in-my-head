"""Render approved SVG scene masters using Chromium, before build_products.py.

Requires Playwright and its Chromium installation. Use --browser for an existing
Chromium executable. Vector sources are never modified.
"""
import argparse
from PIL import Image
from playwright.sync_api import sync_playwright
from common import chapters, read_json, safe_path

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--chapter',required=True)
parser.add_argument('--browser')
args=parser.parse_args()
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,**({'executable_path':args.browser} if args.browser else {}))
    for folder,meta in chapters(args.chapter):
        for scene in read_json(folder/'production.json')['scenes']:
            source=safe_path(folder,scene['source'])
            assert source.suffix=='.svg'
            width,height=scene.get('render_size',[2400,1700])
            page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
            page.goto(source.as_uri(),wait_until='networkidle')
            # SVG roots have fixed authoring dimensions; scale to the export viewport.
            page.evaluate('''()=>{const svg=document.documentElement;svg.setAttribute('width','100%');svg.setAttribute('height','100%');}''')
            target=safe_path(folder,scene['raster']);target.parent.mkdir(parents=True,exist_ok=True)
            import io
            Image.open(io.BytesIO(page.screenshot())).convert('RGB').save(target,quality=96,subsampling=0,optimize=True)
            page.close()
            print(target.relative_to(folder),width,height,flush=True)
    browser.close()
