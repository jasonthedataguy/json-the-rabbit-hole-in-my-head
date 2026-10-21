"""Check vapor localization, protected cold bowl and exact scene-loop boundary."""
from pathlib import Path
import sys
import subprocess
from PIL import Image, ImageChops, ImageStat

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'scripts'))
from studio import load, save, sha
from portable_paths import runtime_binary


def score(difference, box):
    return sum(ImageStat.Stat(difference.crop(box)).mean)/3


def main():
    app=ROOT/'studio/apps/video'
    cache=ROOT/'studio/.cache/render/com-nguoi/v5-living-illustrations'
    qa=ROOT/'studio/projects/com-nguoi/video/review/v5-living-illustrations/motion-controls'
    qa.mkdir(parents=True,exist_ok=True)
    props=load(app/'manifests/com-nguoi-v5.json')
    cli=app/'node_modules/@remotion/cli/remotion-cli.js'
    node=Path(runtime_binary('node'))

    def render(label, data, frame, composition):
        settings=qa/(label+'-props.json')
        save(settings,data)
        target=qa/(label+'.png')
        result=subprocess.run([str(node),str(cli),'still','src/com-nguoi-v5-entry.tsx',composition,
                               str(target),'--public-dir='+str(cache/'public'),'--props='+str(settings),
                               '--frame='+str(frame),'--timeout=120000'],cwd=app,capture_output=True,text=True)
        (qa/(label+'.log')).write_text(result.stdout+'\n'+result.stderr,encoding='utf-8')
        if result.returncode:
            raise RuntimeError(result.stderr[-3000:])
        return target

    checks=[]
    for scene,frame,region in [('dinner',390,(520,735,625,860)),('child',2340,(825,645,940,782))]:
        visible=render(scene+'-vapor',props,frame,'ComNguoiV5')
        disabled=render(scene+'-no-vapor',{**props,'proofNoSteam':True},frame,'ComNguoiV5')
        with Image.open(visible) as a,Image.open(disabled) as b:
            difference=ImageChops.difference(a.convert('RGB'),b.convert('RGB'))
        steam=score(difference,region)
        protected=score(difference,(560,885,675,940)) if scene=='child' else score(difference,(400,790,475,860))
        captions=score(difference,(50,1350,1030,1700))
        assert steam>.1,('Vapor is not visible',scene,steam)
        assert protected==0 and captions==0,('Vapor reaches protected bowl/body/text',scene)
        difference.save(qa/(scene+'-vapor-difference.png'))
        checks.append({'scene':scene,'frame':frame,'steam_region_mean_pixel_change':steam,
                       'protected_cold_bowl_or_child_region_change':protected,'caption_change':captions})
        print(checks[-1],flush=True)
    boundaries=[]
    for scene in ('dinner','child'):
        start=render(scene+'-loop-zero',{**props,'loopScene':scene,'loopTime':0},0,'ComNguoiV5Loop')
        end=render(scene+'-loop-eight',{**props,'loopScene':scene,'loopTime':8},0,'ComNguoiV5Loop')
        with Image.open(start) as a,Image.open(end) as b:
            difference=ImageChops.difference(a.convert('RGB'),b.convert('RGB'))
        assert difference.getbbox() is None,'Scene endpoints are not identical'
        boundaries.append({'scene':scene,'zero_and_eight_second_pixels_identical':True})
        print('Seam pass',scene,flush=True)
    save(qa/'verification.json',{'status':'pass','method':'Matched frames differ only by vapor enabled/disabled; exact loop end pose rendered separately.',
                                'checks':checks,'loop_boundaries':boundaries,'renderer_sha256':sha(app/'src/com-nguoi-v5.tsx'),
                                'steam_component_sha256':sha(app/'src/LivingSteam.tsx'),'author_quality_approved':False})


if __name__=='__main__':
    main()
