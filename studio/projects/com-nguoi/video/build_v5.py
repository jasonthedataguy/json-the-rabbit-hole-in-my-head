"""Reuse v4 extracted art and replace frozen vapor with a source-anchored living loop."""
from pathlib import Path
import copy
import math
import shutil
import subprocess
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import binary_fill_holes, label

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT/'scripts'))
from studio import load, save, sha
PROJECT = ROOT/'studio/projects/com-nguoi'
ANIMATION = PROJECT/'animation/v5'
CACHE = ROOT/'studio/.cache/render/com-nguoi/v5-living-illustrations'
ART = Path(load(ROOT/'studio/studio.json')['asset_library'])/'chapters/com-nguoi/artwork'
PERIOD = 8


def atomic_image(image, path):
    temporary = path.with_name(path.stem+'-next.png')
    image.save(temporary, optimize=True)
    temporary.replace(path)


def remove_painted_steam():
    source = ART/'chapter-page/hero.webp'
    base = Image.open(PROJECT/'animation/v4/assets/dinner-base.png').convert('RGB')
    mask = Image.new('L', base.size, 0)
    # The cream paper plume is distinct from the dark wall. Keep only its connected
    # component and fill texture holes, excluding chopsticks and the rice below.
    rgb = np.asarray(base)
    roi = rgb[680:837,970:1080]
    bright = (roi[:,:,0]>155)&(roi[:,:,1]>110)&(roi[:,:,2]>55)
    components,count = label(bright)
    sizes = np.bincount(components.ravel())
    sizes[0] = 0
    selected = binary_fill_holes(components==sizes.argmax())
    mask.paste(Image.fromarray(selected.astype('uint8')*255),(970,680))
    mask = mask.filter(ImageFilter.MaxFilter(7))
    ImageDraw.Draw(mask).rectangle((0,838,1920,1280), fill=0)
    repaired = np.asarray(base).astype(float).copy()
    original = repaired.copy()
    selection = np.asarray(mask) > 0
    texture = np.asarray(base).astype(float) - np.asarray(base.filter(ImageFilter.GaussianBlur(2))).astype(float)
    for y in np.flatnonzero(selection.any(axis=1)):
        xs = np.flatnonzero(selection[y])
        left, right = int(xs.min()), int(xs.max())
        a = np.mean(original[y,left-5:left-2], axis=0)
        b = np.mean(original[y,right+3:right+6], axis=0)
        for x in xs:
            weight = (x-left+1)/(right-left+2)
            repaired[y,x] = (1-weight)*a + weight*b + texture[y,x-90]*.7
    alpha = np.asarray(mask.filter(ImageFilter.GaussianBlur(1.2)))/255
    result = original*(1-alpha[:,:,None])+repaired*alpha[:,:,None]
    target = ANIMATION/'assets/dinner-base-living.png'
    target.parent.mkdir(parents=True, exist_ok=True)
    atomic_image(Image.fromarray(np.clip(result,0,255).astype('uint8')), target)
    mask_path = ANIMATION/'assets/dinner-frozen-steam-mask.png'
    atomic_image(mask, mask_path)
    return target, mask_path, source


def main():
    ANIMATION.mkdir(parents=True, exist_ok=True)
    props = copy.deepcopy(load(PROJECT/'animation/v4/motion-manifest.json'))
    timeline = copy.deepcopy(props['timeline'])
    timeline.update(version='v5-living-illustrations', animation_manifest=str(ANIMATION/'motion-manifest.json'))
    for shot in timeline['cuts']['master']['shots']:
        if shot['kind']=='story':
            shot['visual']='Living illustration: curling vapor rises from the hot serving bowl/pot, leaves sway and warm light breathes. Cold bowl, faces and family poses remain still.'
    props['timeline'] = timeline
    base_path, mask_path, original = remove_painted_steam()
    for asset in props['assets']:
        if asset['id']=='dinner-base':
            asset.update(path=str(base_path), sha256=sha(base_path))
            asset['provenance'].update(operation='Reuse v4 environmental clean plate and remove the frozen painted steam locally. Per-row neighboring surface interpolation with source-sampled texture, feathered mask; no people, rice or bowl edited.',
                                       intermediate_path=str(PROJECT/'animation/v4/assets/dinner-base.png'),
                                       intermediate_sha256=sha(PROJECT/'animation/v4/assets/dinner-base.png'),
                                       mask_path=str(mask_path), mask_sha256=sha(mask_path))
    for layer in props['layers']:
        tracks = {}
        if 'rotation' in layer['tracks']:
            identifier = layer['id']
            amplitude = .85 if 'lamp' in identifier else (1.8 if 'crown' in identifier else 1.3)
            phase = 0 if 'lamp' in identifier else (1.2 if 'left' in identifier else 2.5)
            tracks['rotation'] = [{'t':i/8,'value':round(amplitude*math.sin(2*math.pi*(i/8)/PERIOD+phase),6)} for i in range(65)]
        if layer.get('kind')=='glow':
            tracks['opacity'] = [{'t':i/8,'value':round(.105+.025*math.sin(2*math.pi*(i/8)/PERIOD+1.1),6)} for i in range(65)]
        layer['tracks'] = tracks
    scale = 1032/1920
    for scene, anchor, size, note in [
        ('dinner',(1017,846),(150,190),'Existing steam over the shared hot serving bowl; not the child’s cold bowl.'),
        ('child',(1590,697),(164,204),'Hot cooking pot at right; child’s foreground bowl intentionally has no steam.'),
    ]:
        width,height = size
        props['layers'].append({
            'id':scene+'-living-steam','scene_id':scene,'kind':'steam',
            'x':24+(anchor[0]-width/2)*scale,'y':396+(anchor[1]-height)*scale,
            'width':width*scale,'height':height*scale,'z':8,
            'color':'#F8DFB1','source_anchor_px':list(anchor),
            'source_region_px':[anchor[0]-width/2,anchor[1]-height,width,height],
            'narrative_basis':note,'tracks':{'opacity':[{'t':0,'value':.92},{'t':4,'value':1},{'t':8,'value':.92}]},
        })
    props.update(loop_period_s=PERIOD, rendering_mode='living_illustration',
                 outputPath=str(PROJECT/'video/exports/com-nguoi-v5-living-illustrations-silent-review-1080x1920.mp4'),
                 intent='Full story with source-anchored curling, rising and fading vapor; GIF loops use the same scene engine. Family poses, cold bowl and exact words preserved.',
                 gif_exports=[{'scene_id':scene,'path':str(ANIMATION/f'exports/com-nguoi-v5-{scene}-living.gif'),'width':960,'height':640,'fps':12.5,'duration_s':8,'loop':0} for scene in ('dinner','child')])
    save(ANIMATION/'motion-manifest.json', props)
    save(PROJECT/'video/timeline-v5.json', timeline)
    save(ANIMATION/'derivation-receipt.json',{
        'source_path':str(original),'source_sha256':sha(original),'previous_version':'v4-layer-animation',
        'changed_asset':next(a for a in props['assets'] if a['id']=='dinner-base'),
        'reuse':'Other source and extracted assets referenced in place, not duplicated.',
        'procedural_effect':'Animated vapor is a local illustrative effect, not archival footage or character animation.',
        'protected_region':'Cold child bowl and all family faces/poses are unchanged.',
        'author_quality_approved':False,
    })
    subprocess.run([sys.executable,str(ROOT/'skills/json-asset-animation/scripts/motion_assets.py'),'stage',str(ANIMATION/'motion-manifest.json'),'--output',str(CACHE)],check=True)
    shutil.copy2(CACHE/'render-props.json', ROOT/'studio/apps/video/manifests/com-nguoi-v5.json')
    shutil.copy2(ROOT/'skills/json-asset-animation/assets/LivingSteam.tsx', ROOT/'studio/apps/video/src/LivingSteam.tsx')
    print({'version':timeline['version'],'loop_s':PERIOD,'active_v4_preserved_until_verified':True})


if __name__=='__main__':
    main()
