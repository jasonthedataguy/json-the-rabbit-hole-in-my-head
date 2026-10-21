"""Create a draft chapter without publishing it or overwriting existing files."""
import argparse
import re
import shutil
from common import ROOT, read_json, write_json

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--slug',required=True);parser.add_argument('--number',required=True);parser.add_argument('--title',required=True)
    args=parser.parse_args()
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',args.slug):parser.error('Use a lowercase URL-safe slug')
    if not re.fullmatch(r'\d{2}',args.number):parser.error('Use a two-digit chapter number')
    target=ROOT/'chapters'/args.slug
    registry=read_json(ROOT/'book.json')
    if target.exists() or args.slug in registry['chapters']:parser.error('Chapter already exists')
    for slug in registry['chapters']:
        if read_json(ROOT/'chapters'/slug/'chapter.json')['number']==args.number:parser.error('Chapter number already in use')
    shutil.copytree(ROOT/'templates/chapter',target)
    for directory in ['artwork/source','artwork/scenes','artwork/exports','audio','video','book','web','social/instagram','social/facebook','social/youtube','social/tiktok','previews','docs']:
        (target/directory).mkdir(parents=True,exist_ok=True)
    meta=read_json(target/'chapter.json')
    meta.update(slug=args.slug,number=args.number,title=args.title,canonical_path=f'chapters/{args.number}/',aliases=[f'chapters/{args.slug}/'])
    write_json(target/'chapter.json',meta)
    registry['chapters'].append(args.slug);write_json(ROOT/'book.json',registry)
    print('Created draft:',target,'(publish=false)')

if __name__=='__main__':main()
