"""Record actual artifact files and explicit remaining production work."""
import hashlib
import argparse
from common import ROOT, chapters, read_json, write_json, artifact_hash
from build_site import reader_release

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--chapter')
args=parser.parse_args()
for folder,meta in chapters(args.chapter):
    if not meta['publish']:continue
    if meta.get('release_stage')=='supplied':
        inventory=[]
        for directory in ['source','artwork','book','audio','video','social','web','previews']:
            for path in sorted((folder/directory).rglob('*')):
                if path.is_file():inventory.append({'path':path.relative_to(folder).as_posix(),'bytes_at_build':path.stat().st_size,'sha256_normalized_text_lf':artifact_hash(path)})
        write_json(folder/'docs/INVENTORY.json',inventory)
        # Imported products keep their actual filenames and documented proof states.
        for product in read_json(folder/'docs/PRODUCTS.json')['products']:
            assert (folder/product['path']).is_file(),product
        print(meta['slug'],len(inventory),'supplied product files inventoried')
        continue
    if reader_release(meta):
        inventory=[]
        for directory in ['source','artwork','web','previews']:
            for path in sorted((folder/directory).rglob('*')):
                if path.is_file():inventory.append({'path':path.relative_to(folder).as_posix(),'bytes_at_build':path.stat().st_size,'sha256_normalized_text_lf':artifact_hash(path)})
        write_json(folder/'docs/INVENTORY.json',inventory)
        products=[
            {'product':'Selected manuscript','state':'ready for publication','path':meta['canonical_text']},
            {'product':meta.get('reader_product_name','Responsive chapter website and memory journey'),'state':'ready for publication','path':'web/index.html'},
            {'product':'Homepage and chapter artwork','state':meta.get('artwork_status','supplied-art derivative'),'path':'artwork/exports/hero.jpg'},
            {'product':'Artwork provenance','state':'documented','path':'artwork/scenes/index.json'},
        ]
        if meta.get('reference_board'):products.append({'product':'Supplied project board','state':'preserved reference','path':meta['reference_board']})
        remaining=['A5 proof and print production','Video edit cuts, author-recorded narration and captions','Social platform packs; posting remains author-managed','QR remains deferred']
        write_json(folder/'docs/PRODUCTS.json',{'chapter':meta['slug'],'release_stage':'reader','products':products,'remaining':remaining})
        table=['# Product set — '+meta['title'],'','This release includes the selected reader chapter, artwork and interactive artifact. Multimedia products are tracked separately.','','| Product | Actual state | File |','|---|---|---|']
        table += [f'| {p["product"]} | {p["state"]} | [{p["path"]}](../{p["path"]}) |' for p in products]
        table += ['','Remaining: '+ '; '.join(remaining)+'.','',f'Inventory: {len(inventory)} files; LF-normalized text and raw binary SHA-256 checksums. Supplied references retain their separate import manifest when present.']
        (folder/'docs/PRODUCT_SET.md').write_text('\n'.join(table)+'\n',encoding='utf-8')
        print(meta['slug'],len(inventory),'reader files inventoried')
        continue
    meta['video_mode']='edit cuts awaiting author-recorded narration'
    write_json(folder/'chapter.json',meta)
    inventory=[]
    for directory in ['source','artwork','book','audio','video','social','web','previews']:
        for path in sorted((folder/directory).rglob('*')):
            if path.is_file():inventory.append({'path':path.relative_to(folder).as_posix(),'bytes_at_build':path.stat().st_size,'sha256_normalized_text_lf':artifact_hash(path)})
    write_json(folder/'docs/INVENTORY.json',inventory)
    products=[
       {'product':'Selected prose','state':'ready','path':meta['canonical_text']},
       {'product':meta.get('artwork_product_name','Source illustration and scene crops'),'state':meta.get('artwork_product_state','ready as supplied-art derivatives'),'path':'artwork/scenes/index.json'},
       {'product':'Illustrated A5 chapter','state':'editorial proof','path':'book/chapter-A5-proof.pdf'},
       {'product':'Interactive website','state':'ready for deployment','path':'web/index.html'},
       {'product':'Instagram carousel (five 3:4 cards)','state':'ready','path':'social/instagram/slide-01.jpg'},
       {'product':'Facebook image and copy','state':'ready','path':'social/facebook/post.jpg'},
       {'product':'YouTube thumbnail and description','state':'ready','path':'social/youtube/thumbnail.jpg'},
       {'product':'TikTok cover and caption','state':'ready','path':'social/tiktok/cover.jpg'},
       {'product':'9:16 discovery cut','state':'edit preview; author narration pending','path':'video/discovery-9x16.mp4'},
       {'product':'9:16 YouTube cut','state':'edit preview; author narration pending','path':'video/youtube-9x16.mp4'},
       {'product':'3:4 feed cut','state':'edit preview; author narration pending','path':'video/feed-3x4.mp4'},
       {'product':'SRT/VTT text timings','state':'provisional; retime to recorded narration','path':'video/timeline.json'},
       {'product':'Author reading script','state':'ready for recording','path':'audio/reading-script.md'},
    ]
    products.extend(read_json(folder/'production.json').get('supplemental',{}).get('products',[]))
    for product in products:
        if not (folder/product['path']).is_file():product['state']='missing'
    write_json(folder/'docs/PRODUCTS.json',{'chapter':meta['slug'],'products':products,'remaining':['Jason recorded narration and final timing/mix','Printer specifications and final print production','Physical-device and human screen-reader review','Author-managed social uploads; QR remains deferred']})
    table=['# Product set — '+meta['title'],'','| Product | Actual state | File |','|---|---|---|']
    table += [f'| {p["product"]} | {p["state"]} | [{p["path"]}](../{p["path"]}) |' for p in products]
    table += ['','Remaining: author recording, retimed narration captions, print-specific production and human device review. Social files are prepared; no platform post is claimed.','',f'Inventory: {len(inventory)} files, {sum(p["bytes_at_build"] for p in inventory):,} bytes. Checksums use LF-normalized text and raw binary bytes.']
    (folder/'docs/PRODUCT_SET.md').write_text('\n'.join(table)+'\n',encoding='utf-8')
    print(meta['slug'],len(inventory),'files inventoried')
