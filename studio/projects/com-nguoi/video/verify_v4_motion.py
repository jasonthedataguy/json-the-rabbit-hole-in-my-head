"""Render matched moving/static controls to measure actual scene-element animation."""
from pathlib import Path
import sys
import subprocess
from PIL import Image, ImageChops, ImageStat

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'scripts'))
from studio import load, save, sha
from portable_paths import runtime_binary


def main():
    app=ROOT/'studio/apps/video'
    cache=ROOT/'studio/.cache/render/com-nguoi/v4-layer-animation'
    qa=ROOT/'studio/projects/com-nguoi/video/review/v4-layer-animation/motion-controls'
    qa.mkdir(parents=True,exist_ok=True)
    data=load(app/'manifests/com-nguoi-v4.json')
    control={**data,'proofStatic':True}
    save(cache/'static-control-props.json',control)
    cli=app/'node_modules/@remotion/cli/remotion-cli.js'
    node=Path(runtime_binary('node'))
    checks=[]
    for label,frame,regions in [('dinner',390,{'lamp':(510,530,680,675),'foliage':(715,690,970,895)}),('child',2340,{'lamp':(645,410,785,530),'foliage':(835,790,1040,1050)})]:
        outputs={}
        for mode,props in [('moving',app/'manifests/com-nguoi-v4.json'),('static',cache/'static-control-props.json')]:
            target=qa/f'{label}-{mode}.png'
            result=subprocess.run([str(node),str(cli),'still','src/com-nguoi-v4-entry.tsx','ComNguoiV4',str(target),'--public-dir='+str(cache/'public'),'--props='+str(props),'--frame='+str(frame),'--timeout=120000'],cwd=app,capture_output=True,text=True)
            (qa/f'{label}-{mode}.log').write_text(result.stdout+'\n'+result.stderr,encoding='utf-8')
            if result.returncode:
                raise RuntimeError(result.stderr[-3000:])
            outputs[mode]=target
        with Image.open(outputs['moving']) as first,Image.open(outputs['static']) as second:
            difference=ImageChops.difference(first.convert('RGB'),second.convert('RGB'))
            scores={name:sum(ImageStat.Stat(difference.crop(region)).mean)/3 for name,region in regions.items()}
            outside=sum(ImageStat.Stat(difference.crop((50,1350,1030,1700))).mean)/3
            difference.save(qa/f'{label}-difference.png')
        assert all(score>.03 for score in scores.values()),f'No visible independent motion in {label}: {scores}'
        assert outside<.01,'Text/camera changed between matched control frames'
        checks.append({'scene':label,'frame':frame,'region_mean_absolute_pixel_change':scores,'caption_region_change':outside,'moving_frame':str(outputs['moving']),'static_control':str(outputs['static'])})
        print(label,scores,flush=True)
    save(qa/'verification.json',{'status':'pass','method':'Same source frame, camera and text; only independent layer rotations/light disabled in static control. Non-text scene changes measured separately.','checks':checks,'renderer_sha256':sha(app/'src/com-nguoi-v4.tsx'),'author_quality_approved':False})


if __name__=='__main__':
    main()
