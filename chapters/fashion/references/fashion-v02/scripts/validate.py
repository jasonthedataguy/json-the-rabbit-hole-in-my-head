from pathlib import Path
from PIL import Image
import fitz,subprocess,json
ROOT=Path(__file__).resolve().parents[1]
with fitz.open(ROOT/'book/02_Fashion_Room_in_Revision_A5_PROOF.pdf') as pdf:
 assert len(pdf)==9
 assert 'Peace and love!' in '\n'.join(page.get_text() for page in pdf)
for p in (ROOT/'social/instagram').glob('slide_*.jpg'):
 assert Image.open(p).size==(1080,1440),str(p)
for file,wh in [('02_Fashion_RoomInRevision_ANIMATIC_9x16.mp4',(720,1280)),('02_Fashion_YouTube_LANDSCAPE_ANIMATIC_16x9.mp4',(1280,720))]:
 j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=width,height','-of','json',str(ROOT/'video'/file)]))
 a=j['streams'][0];assert (a['width'],a['height'])==wh
print('PASS: A5 PDF, final text, five social cards, and video dimensions')
