"""Small independent chapter delivery bundles + complete source archive."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib
root=Path(__file__).resolve().parents[1];dst=root.parent
# Manifest lists paths only (avoids self-referential hash after re-zipping).
parts=[
 ('CH06_A_Book_and_Website.zip',['book','web','manuscript','README.md']),
 ('CH06_B1_Illustration_Artwork.zip',['art']),
 ('CH06_B2_Social_Media_Images.zip',['social']),
 ('CH06_C_Video_and_Audio.zip',['video']),
 ('CH06_D_Project_Board_and_Scripts.zip',['docs','source/build_chapter.py','source/validate_chapter.py','source/package_chapter.py','README.md']),
]
inputs=sorted((root/'source'/'inputs').glob('*.png'))
for i,f in enumerate(inputs,1):parts.append((f'CH06_E{i}_Original_Artwork_Input.zip',[str(f.relative_to(root))]))
manifest={'chapter':'.json / 06 — Thế giới trong mơ của tôi','release_status':'EDITORIAL_PROOFS_ONLY_NOT_PUBLISHED','source_text':'preserved exactly','small_packages':[name for name,_ in parts],'source_master_inputs':[str(f.relative_to(root)) for f in inputs],'artwork_caveat':'Illustrative crops/composites of approved concept-board art, not independent layered print masters','video_caveat':'24 sec H.264 AAC original synthetic ambience, no narrator','complete_kit':'CH06_The_Gioi_Trong_Mo_FULL_Production_Kit_v01.zip'}
(root/'docs'/'DELIVERY_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
files=[p for p in root.rglob('*') if p.is_file()]
def select(spec):
 out=set()
 for item in spec:
  p=root/item
  if p.is_dir():out.update(x for x in p.rglob('*') if x.is_file())
  elif p.is_file():out.add(p)
 return sorted(out)
def write_zip(name,subset):
 target=dst/name
 with ZipFile(target,'w',compression=ZIP_DEFLATED,compresslevel=5) as z:
  for f in subset:z.write(f,arcname=str(f.relative_to(root)))
 with ZipFile(target) as z:assert z.testzip() is None
 return {'name':name,'bytes':target.stat().st_size,'entries':len(subset)}
small=[write_zip(name,select(spec)) for name,spec in parts]
allfiles=[p for p in root.rglob('*') if p.is_file()]
full=write_zip(manifest['complete_kit'],allfiles)
print(json.dumps({'full':full,'small':small},ensure_ascii=False,indent=2))
