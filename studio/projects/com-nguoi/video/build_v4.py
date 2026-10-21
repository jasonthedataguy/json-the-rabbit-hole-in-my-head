"""Prepare aligned source-derived animation plates and the complete v4 film props."""
from pathlib import Path
import sys
import copy
import math
import json
import shutil
import subprocess
import numpy as np
from scipy.ndimage import distance_transform_edt
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'scripts'))
from studio import load, save, sha, stage_asset
PROJECT = ROOT / 'studio/projects/com-nguoi'
ART = Path(load(ROOT/'studio/studio.json')['asset_library'])/'chapters/com-nguoi/artwork'
DERIVED = PROJECT / 'animation/v4/assets'
CACHE = ROOT / 'studio/.cache/render/com-nguoi/v4-layer-animation'


def save_image(image, path):
    # Replace the source inode atomically: an older private staging hardlink stays immutable.
    path = Path(path)
    temporary = path.with_name(path.stem + '-next.png')
    image.save(temporary, optimize=True)
    temporary.replace(path)


def mask_polygon(points, size, *, green=False, image=None):
    mask = Image.new('L', size, 0)
    ImageDraw.Draw(mask).polygon(points, fill=255)
    if green:
        hsv = np.asarray(image.convert('HSV'))
        selection = ((hsv[:,:,0] >= 29) & (hsv[:,:,0] <= 120) & (hsv[:,:,1] > 55) & (hsv[:,:,2] > 35))
        mask = Image.fromarray((np.asarray(mask) * selection).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    return mask.filter(ImageFilter.GaussianBlur(.8))


def derive_scene(identifier, relative, definitions):
    original = ART / relative
    image = Image.open(original).convert('RGB')
    width, height = image.size
    rgb = np.asarray(image)
    masks = [(name, mask_polygon(points, image.size, green=green, image=image), pivot, angle) for name, points, green, pivot, angle in definitions]
    combined = np.maximum.reduce([np.asarray(mask) for _, mask, _, _ in masks])
    removed = combined > 15
    indices = distance_transform_edt(removed, return_distances=False, return_indices=True)
    nearest = rgb[indices[0], indices[1]]
    # Only masked environmental regions are repaired; original people and all other pixels stay fixed.
    plate = rgb.copy()
    plate[removed] = nearest[removed]
    base_path = DERIVED / f'{identifier}-base.png'
    save_image(Image.fromarray(plate), base_path)
    assets = [{'id': identifier+'-base', 'path': str(base_path), 'sha256': sha(base_path), 'role': 'base', 'provenance': {'source_path': str(original), 'source_sha256': sha(original), 'operation': 'Source-aligned clean plate: nearest existing surface colors fill only masked environmental areas, hidden behind their extracted layers. No people retouched.'}}]
    layers = [{'id': identifier+'-base', 'asset_id': identifier+'-base', 'x': 24, 'y': 396, 'width': 1032, 'height': 688, 'z': 0, 'tracks': {}, 'scene_id': identifier, 'crop_px': [0,0,width,height], 'pivot_x': .5, 'pivot_y': .5}]
    scale = 1032 / width
    for number, (name, mask, pivot, angle) in enumerate(masks, 1):
        bbox = mask.getbbox()
        assert bbox and np.asarray(mask).max() == 255
        rgba = image.convert('RGBA')
        rgba.putalpha(mask)
        path = DERIVED / f'{identifier}-{name}.png'
        save_image(rgba.crop(bbox), path)
        asset_id = identifier+'-'+name
        assets.append({'id': asset_id, 'path': str(path), 'sha256': sha(path), 'role': 'cutout', 'provenance': {'source_path': str(original), 'source_sha256': sha(original), 'operation': 'Aligned polygon/foliage-hue matte and cropped alpha; no new artwork or character pose.', 'crop_px': list(bbox), 'pivot_source_px': list(pivot)}})
        local_pivot = [(pivot[0]-bbox[0])/(bbox[2]-bbox[0]), (pivot[1]-bbox[1])/(bbox[3]-bbox[1])]
        # Keep the physical root within a padded image when necessary (CSS supports outside pivots,
        # but preflight intentionally expects normalized anchors).
        if any(not 0 <= v <= 1 for v in local_pivot):
            padded = (min(bbox[0],pivot[0]),min(bbox[1],pivot[1]),max(bbox[2],pivot[0]+1),max(bbox[3],pivot[1]+1))
            bbox = tuple(int(v) for v in padded)
            save_image(rgba.crop(bbox), path)
            assets[-1]['sha256'] = sha(path)
            assets[-1]['provenance']['crop_px'] = list(bbox)
            local_pivot = [(pivot[0]-bbox[0])/(bbox[2]-bbox[0]),(pivot[1]-bbox[1])/(bbox[3]-bbox[1])]
        duration = 109.5
        period = 9.0 + number * 1.7
        keys = [{'t': round(t,3), 'value': round(angle * math.sin(2*math.pi*t/period),4)} for t in np.arange(0,duration,.75)]
        keys.append({'t': duration, 'value': round(angle*math.sin(2*math.pi*duration/period),4)})
        layers.append({'id': asset_id, 'asset_id': asset_id, 'x': round(24+bbox[0]*scale,3), 'y': round(396+bbox[1]*scale,3), 'width': round((bbox[2]-bbox[0])*scale,3), 'height': round((bbox[3]-bbox[1])*scale,3), 'z': number+1, 'scene_id': identifier, 'pivot_x': local_pivot[0], 'pivot_y': local_pivot[1], 'tracks': {'rotation': keys}, 'crop_px': list(bbox), 'native_pivot': list(pivot)})
    return assets, layers


def main():
    DERIVED.mkdir(parents=True, exist_ok=True)
    hero = [
        ('lamp', [(1041,0),(1052,0),(1052,278),(1067,288),(1068,310),(1097,330),(1126,364),(1153,402),(1167,429),(1157,441),(1110,455),(1045,462),(990,454),(947,440),(922,430),(929,406),(950,367),(981,339),(1026,311),(1028,286),(1041,278)], False, (1046,0), 1.05),
        ('foreground-left', [(0,430),(340,430),(390,650),(370,900),(450,1070),(680,1090),(860,1280),(0,1280)], True, (230,1265), .65),
        ('plant-crown', [(1305,890),(1320,740),(1380,650),(1450,650),(1520,580),(1675,565),(1710,705),(1690,870),(1540,900)], True, (1490,887), 1.1),
    ]
    inline = [
        ('lamp', [(1274,0),(1289,0),(1289,63),(1318,74),(1347,100),(1364,126),(1378,163),(1370,176),(1334,190),(1285,195),(1233,190),(1191,177),(1171,163),(1179,133),(1194,104),(1221,79),(1274,62)], False, (1282,0), .85),
        ('foreground-left', [(0,350),(335,340),(390,550),(390,900),(570,1280),(0,1280)], True, (115,1240), .65),
        ('foreground-right', [(1920,390),(1720,455),(1690,650),(1690,840),(1460,1040),(1320,1280),(1920,1280)], True, (1780,1260), -.85),
    ]
    assets, layers = [], []
    for identifier, relative, definitions in [('dinner','chapter-page/hero.webp',hero),('child','content/illustrations/01-story-detail.webp',inline)]:
        aa,ll = derive_scene(identifier,relative,definitions)
        assets.extend(aa); layers.extend(ll)
    portal = ART/'chapter-page/portal.webp'
    hero_path = ART/'chapter-page/hero.webp'
    assets.extend([{'id':'portal','path':str(portal),'sha256':sha(portal),'role':'portal'}, {'id':'hero-original','path':str(hero_path),'sha256':sha(hero_path),'role':'base'}])
    history = PROJECT/'video/history/timeline-full-portal-v3.json'
    timeline_path = PROJECT/'video/timeline.json'
    previous = load(timeline_path)
    if previous['version'] == 'v3-portal-entry' and not history.exists():
        save(history,previous)
    timeline = copy.deepcopy(load(history))
    timeline.update({'version':'v4-layer-animation','visual_mode':'layer_animation','animation_manifest':str(PROJECT/'animation/v4/motion-manifest.json')})
    for shot in timeline['cuts']['master']['shots']:
        shot['scene_id'] = 'child' if shot['id'] in ('P03','P05','P06') else 'dinner'
        if shot['kind'] == 'story' and shot['id']=='P07':
            shot['scene_id']='dinner'
            shot['asset_path']=str(hero_path); shot['asset_sha256']=sha(hero_path)
        shot['visual'] = 'Source-aligned 2.5D scene: independently pivoting lamp, foreground foliage and local light; family artwork remains unchanged.' if shot['kind']=='story' else shot['visual']
    # Local warm lighting changes independently from the object mattes; these are illustrative effects.
    for scene,x,y,w,h in [('dinner',440,560,300,270),('child',500,440,350,270)]:
        keys=[{'t':float(t),'value':round(.11+.035*math.sin(t*.65),4)} for t in range(110)]
        keys[-1]['t']=109.5
        layers.append({'id':scene+'-light','kind':'glow','x':x,'y':y,'width':w,'height':h,'z':1,'scene_id':scene,'color':'#F4B353','tracks':{'opacity':keys}})
    props = {'schema_version':'1.0','story_slug':'com-nguoi','classification':'layer_animation','source':timeline['source'],'width':1080,'height':1920,'fps':30,'duration_s':120,'background':'#101F31',
             'opening':{'title':'Cơm nguội','portal_asset':'portal','reveal_asset':'hero-original','focus_x':.5,'focus_y':.565,'title_hold_s':2.6,'entry_end_s':7.7,'story_start_s':10.5},
             'assets':assets,'layers':layers,'audio':{'mode':'silent'},'status':'internal_review','author_quality_approved':False,'public_release_approved':False,'paid_release_approved':False,
             'timeline':timeline,'scene_art_box':{'x':24,'y':396,'width':1032,'height':688},'outputPath':str(PROJECT/'video/exports/com-nguoi-v4-animated-silent-review-1080x1920.mp4'),'intent':'Full source-grounded film. No floating proof cards, changed character poses, generated voice or added events.'}
    manifest_path = PROJECT/'animation/v4/motion-manifest.json'
    save(manifest_path, props)
    save(PROJECT/'animation/v4/derivation-receipt.json',{'method':'Aligned extracted environmental layers with small local nearest-existing-surface clean plates. All original family pixels outside environment masks remain unchanged.', 'sources':[{'path':str(ART/p),'sha256':sha(ART/p)} for p in ('chapter-page/hero.webp','content/illustrations/01-story-detail.webp')], 'assets':assets,'author_quality_approved':False})
    # Do not select v4 as active until technical scene preview and full export are verified.
    save(PROJECT/'video/timeline-v4.json',timeline)
    subprocess.run([sys.executable,str(ROOT/'skills/json-asset-animation/scripts/motion_assets.py'),'stage',str(manifest_path),'--output',str(CACHE)],check=True)
    shutil.copy2(CACHE/'render-props.json',ROOT/'studio/apps/video/manifests/com-nguoi-v4.json')
    print({'manifest':str(manifest_path),'layers':len(layers),'assets':len(assets),'duration_s':120,'source_sha256':timeline['source']['sha256'],'active_v3_retained_until_v4_delivery':True})


if __name__=='__main__':
    main()
