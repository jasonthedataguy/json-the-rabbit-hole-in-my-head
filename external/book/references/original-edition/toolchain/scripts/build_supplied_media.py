"""Reframe supplied diagrams and artwork without changing the imported originals.

The recipe's publish_media section selects exact excerpts and supplied scenes.
Usage: python scripts/build_supplied_media.py --chapter dating-algorithm --ffmpeg PATH
"""
import argparse
from PIL import Image
from common import chapters,read_json,write_json
from build_products import card,save,film_plan,render_film

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--chapter',required=True);parser.add_argument('--ffmpeg',required=True)
args=parser.parse_args()
for folder,meta in chapters(args.chapter):
    recipe=read_json(folder/'production.json')
    assert meta.get('release_stage')=='supplied'
    alts=[]
    for index,item in enumerate(recipe['publish_media']['carousel'],1):
        path=f'social/instagram/slide-{index:02d}.jpg'
        save(card(meta,Image.open(folder/item['scene']),item['text'],number=f'{index:02d}',scene_fit='contain'),folder/path)
        alts.append({'file':path,'alt':item['text']+' — conceptual illustration or diagram from '+meta['title']+'.'})
    write_json(folder/'social/alt-text.json',alts)
    first=recipe['publish_media']['carousel'][0]
    poster=card(meta,Image.open(folder/first['scene']),meta['title'],(1080,1920),cover_card=True,scene_fit='contain')
    save(poster,folder/'artwork/exports/poster-9x16.jpg');save(poster,folder/'social/tiktok/cover.jpg')
    variants=film_plan(folder,meta,[],[])
    for variant in variants:render_film(folder,meta,variant,args.ffmpeg)
    print('Built framed social cards and films:',meta['slug'])
