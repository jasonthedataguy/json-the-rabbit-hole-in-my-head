"""Export documented supplied-art crops for a reader release. Requires Pillow."""
import argparse
from PIL import Image, ImageOps
from common import chapters, read_json, safe_path, write_json

def build(folder,meta):
    recipe=read_json(folder/'production.json')
    with Image.open(safe_path(folder,meta['illustration'])) as original:
        source=original.convert('RGB')
    scenes=[];records=[]
    for index,scene in enumerate(recipe['scenes'],1):
        box=scene['box']
        if not (len(box)==4 and 0<=box[0]<box[2]<=1 and 0<=box[1]<box[3]<=1):
            raise ValueError('Invalid normalized scene box: '+scene['id'])
        pixels=[round(value*source.size[axis%2]) for axis,value in enumerate(box)]
        crop=source.crop(pixels)
        relative=f'artwork/scenes/{index:02d}-{scene["id"]}.jpg'
        path=safe_path(folder,relative);path.parent.mkdir(parents=True,exist_ok=True)
        crop.save(path,quality=92,optimize=True)
        records.append({'path':relative,'source':meta['illustration'],'box_normalized':box,'box_pixels':pixels,'native_dimensions':list(crop.size),'type':'crop of supplied illustration'})
        scenes.append(crop)
    write_json(folder/'artwork/scenes/index.json',records)
    for name,export in recipe['reader_artwork'].items():
        path=safe_path(folder,'artwork/exports/'+name);path.parent.mkdir(parents=True,exist_ok=True)
        ImageOps.fit(scenes[export['scene']],tuple(export['size']),method=Image.Resampling.LANCZOS).save(path,quality=90,optimize=True)
    print(meta['slug'],len(scenes),'source crops; reader artwork exported')

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--chapter');args=parser.parse_args()
    for folder,meta in chapters(args.chapter):
        if meta.get('release_stage')=='reader':build(folder,meta)

if __name__=='__main__':main()
