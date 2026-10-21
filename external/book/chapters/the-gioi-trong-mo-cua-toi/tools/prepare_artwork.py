"""Crop board labels from supplied concepts; retain every original unchanged."""
from pathlib import Path
import hashlib,json,shutil
from PIL import Image,ImageOps
p=Path(__file__).resolve().parents[1]
boxes={
 '01_rooftop_skyline.jpg':(720,0,1125,600),
 '02_metro_children.jpg':(35,112,1600,920),
 '03_bastille_station.jpg':(0,150,915,730),
 '04_telephone.jpg':(125,110,1000,695),
 '05_imagined_kitchen.jpg':(60,140,1100,880),
 '06_rooftop_afterimage.jpg':(115,145,1000,850),
 '07_old_photographs.jpg':(85,110,1000,660),
 '08_both_children.jpg':(105,110,900,720),
}
records=[]
for name,box in boxes.items():
    source=p/'artwork/source'/name
    im=Image.open(source);cropped=im.crop(box)
    target=p/'artwork/scenes'/name
    cropped.save(target,quality=94)
    records.append({'path':target.relative_to(p).as_posix(),'source':'references/dream-world-v01/art/'+name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_size':list(im.size),'crop_box':list(box),'native_size':list(cropped.size),'kind':'label-free crop of supplied concept artwork; not a documentary photograph or independent print master'})
    shutil.copy2(target,p/'web/assets'/name)
for target,source in [('observed.jpg','02_metro_children.jpg'),('imagined.jpg','05_imagined_kitchen.jpg'),('afterimage.jpg','06_rooftop_afterimage.jpg')]:
    shutil.copy2(p/'artwork/scenes'/source,p/'web/assets'/target)
hero=Image.open(p/'artwork/scenes/06_rooftop_afterimage.jpg')
for target,size in [('artwork/exports/hero.jpg',(1600,960)),('web/assets/hero.jpg',(1600,960)),('artwork/exports/hero-mobile.jpg',(900,1200))]:
    ImageOps.fit(hero,size,method=Image.Resampling.LANCZOS).save(p/target,quality=94)
(p/'artwork/scenes/index.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Eight clean crops and reader derivatives; original artwork unchanged.')
