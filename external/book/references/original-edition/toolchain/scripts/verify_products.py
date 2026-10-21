"""Inspect images, PDF prose and video decoding. Requires PyMuPDF and ffmpeg."""
import argparse
import re
import subprocess
from pathlib import Path
import pymupdf
from PIL import Image
from common import ROOT,chapters,paragraphs,plain,read_json,write_json

parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--ffmpeg',required=True);parser.add_argument('--chapter');args=parser.parse_args()
for folder,meta in chapters(args.chapter):
    if not meta['publish'] or meta.get('release_stage','multimedia')!='multimedia':continue
    images=[p for directory in ['artwork','social','previews'] for p in (folder/directory).rglob('*') if p.suffix in ['.jpg','.png']]
    for path in images:
        with Image.open(path) as image:image.verify()
    for i in range(1,6):assert Image.open(folder/f'social/instagram/slide-{i:02d}.jpg').size==(1080,1440)
    document=pymupdf.open(folder/'book/chapter-A5-proof.pdf')
    full=' '.join(' '.join(page.get_text(clip=pymupdf.Rect(30,40,page.rect.width-30,page.rect.height-40)).split()) for page in document)
    assert '\ufffd' not in full
    for paragraph in paragraphs(folder/meta['canonical_text']):
        cleaned=' '.join(plain(paragraph).split())
        assert cleaned in full,f'PDF text missing or changed: {cleaned[:75]}'
    for page in document:assert abs(page.rect.width-419.528)<1 and abs(page.rect.height-595.276)<1
    media=[]
    for plan in read_json(folder/'video/timeline.json'):
        path=folder/f'video/{plan["name"]}.mp4'
        probe=subprocess.run([args.ffmpeg,'-hide_banner','-i',str(path)],capture_output=True,text=True,encoding='utf-8',errors='replace')
        data=probe.stderr
        assert 'Video: h264' in data and 'Audio: aac' in data,data
        assert f'{plan["size"][0]}x{plan["size"][1]}' in data,data
        duration=re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',data)
        actual=sum(float(v)*f for v,f in zip(duration.groups(),[3600,60,1]))
        assert abs(actual-plan['duration'])<.2,(path,actual,plan['duration'])
        decoded=subprocess.run([args.ffmpeg,'-v','error','-threads','2','-i',str(path),'-f','null','-'],capture_output=True,text=True)
        assert decoded.returncode==0 and not decoded.stderr,decoded.stderr
        if plan['name']=='discovery-9x16':
            subprocess.run([args.ffmpeg,'-y','-v','error','-ss','12','-i',str(path),'-frames:v','1',str(folder/'previews/video-frame.jpg')],check=True)
        media.append({'file':path.relative_to(folder).as_posix(),'dimensions':plan['size'],'duration':actual,'decode':'pass','narration':'not present; author recording pending'})
    source=folder/meta['illustration']
    source_resolution='scalable SVG; raster export dimensions in artwork/scenes/index.json' if source.suffix=='.svg' else list(Image.open(source).size)
    evidence={'images_decoded':len(images),'pdf_pages':len(document),'pdf_selected_prose':'all paragraphs preserved','video':media,'source_resolution':source_resolution}
    write_json(folder/'docs/MEDIA_QA.json',evidence)
    print(meta['slug'],len(images),'images,',len(document),'PDF pages,',len(media),'videos: PASS',flush=True)
