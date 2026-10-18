from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import json, math, random
ROOT=Path(__file__).resolve().parents[1]
SRC=Image.open('/mnt/data/winter_memory_project_board.png').convert('RGB')
SRC2=Image.open('/mnt/data/for_mother_russia_a_creative_chapter_board.png').convert('RGB')
# Remove the large lettering *inside the scenic excerpt only*. The approved complete main banner remains unchanged.
import cv2,numpy as np
scene_arr=np.array(SRC);mask=np.zeros(scene_arr.shape[:2],dtype=np.uint8)
mask[169:239,300:403]=255
clean=cv2.inpaint(cv2.cvtColor(scene_arr,cv2.COLOR_RGB2BGR),mask,9,cv2.INPAINT_TELEA)
SCENE_SOURCE=Image.fromarray(cv2.cvtColor(clean,cv2.COLOR_BGR2RGB))
COLORS={'navy':'#0A223A','night':'#061724','blue':'#23548C','ice':'#C8DDF1','paper':'#F6F1E5','gold':'#F6C16E','rose':'#BCA8D4','gray':'#879DAF'}
serif='/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf';bold='/usr/share/fonts/truetype/noto/NotoSerif-SemiBold.ttf';sans='/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
F=lambda x,s:ImageFont.truetype(x,s)
random.seed(26)
def textured(img,scale=0.10):
 p=img.load(); w,h=img.size
 noise=Image.effect_noise((max(1,w//2),max(1,h//2)),14).resize((w,h),Image.Resampling.BILINEAR)
 n=noise.load()
 # Subtle printed grain
 for y in range(h):
  for x in range(w):
   r,g,b=p[x,y];v=(n[x,y]-128)*scale;p[x,y]=(max(0,min(255,int(r+v))),max(0,min(255,int(g+v))),max(0,min(255,int(b+v))))
 return img

def border_fit(im, size, border=0, color=COLORS['night']):
 w,h=size
 fit=ImageOps.fit(im, size, Image.Resampling.LANCZOS, centering=(.5,.5))
 return fit

# Banner precisely from approved first version with changed yellow beanie and dog
hero=SRC.crop((3,3,678,401));hero=hero.resize((2400,1415),Image.Resampling.LANCZOS)
hero.save(ROOT/'art/01_HERO_beanie_Gau_blue_winter.jpg',quality=92,optimize=True)
# Zoomed unlettered scene for chapter spots
scenehero=SCENE_SOURCE.crop((270,55,675,398))
# Approved art board includes tiny pre-rendered illustrations. These are concept-source crops, never claim native high-res originals.
scenes=[
 ('02_snowy_path',scenehero,'Jason and Gấu crossing an imagined snowy path'),
 ('03_grandfather',SRC.crop((149,438,265,552)),'Grandfather stories, imagined recollection'),
 ('04_soviet_apartments',SRC.crop((270,438,396,552)),'Soviet-era apartment facades as imagined'),
 ('05_russian_salad',SRC.crop((402,437,537,552)),'The salad Jason could never quite appreciate'),
 ('06_stalingrad_game_memory',SRC.crop((541,438,671,555)),'Stalingrad, remembered through a videogame, not war reportage'),
 ('07_wood_cabin',SRC2.crop((120,653,224,728)),'Dream cabin with warm light'),
 ('08_snow_forest',SRC2.crop((232,690,348,744)),'Snowy forest imagined from family stories'),
 ('09_volga_dream',SRC2.crop((338,690,446,743)),'An imaginary Volga river winter landscape'),
 ('10_game_screen',SRC2.crop((442,690,553,745)),'Old screen and imagined battlefield'),
 ('11_room_at_night',SRC2.crop((555,690,662,749)),'Bedroom holding borrowed memories'),
]
# produce art prints scene plate 1600x1000 with framed cinema composition
for i,(slug,img,desc) in enumerate(scenes):
 W,H=1600,1000
 out=Image.new('RGB',(W,H),COLORS['night'])
 backdrop=ImageOps.fit(img,(W,H),Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(32))
 out.paste(Image.blend(backdrop,Image.new('RGB',(W,H),COLORS['night']),.26))
 center=ImageOps.fit(img,(1376,780),Image.Resampling.LANCZOS)
 out.paste(center,(112,90))
 d=ImageDraw.Draw(out)
 d.rectangle((94,72,1506,892),outline=COLORS['paper'],width=5)
 d.rectangle((112,900,1488,970),fill=COLORS['night'])
 d.text((134,915),f'{i+2:02d}  /  {slug.replace("_"," ").upper()}',font=F(sans,26),fill=COLORS['paper'])
 d.text((1460,920),'.json  /  03',font=F(sans,22),fill=COLORS['gold'],anchor='ra')
 out.save(ROOT/f'art/{slug}.jpg',quality=88,optimize=True)
# Main portrait book poster
W,H=1900,2500
p=Image.new('RGB',(W,H),COLORS['night']);d=ImageDraw.Draw(p)
# image first 68% of portrait, vivid winter atmosphere
wide=ImageOps.fit(SCENE_SOURCE.crop((352,0,680,400)),(W,1750),Image.Resampling.LANCZOS)
p.paste(wide,(0,650));d=ImageDraw.Draw(p)
d.rectangle((36,36,W-36,H-36),outline=COLORS['gold'],width=12)
d.rectangle((60,60,W-60,H-60),outline=COLORS['paper'],width=4)
d.text((145,125),'.json / 03',font=F(sans,70),fill=COLORS['gold'])
d.text((145,262),'For',font=F(bold,138),fill=COLORS['paper'])
d.text((145,425),'Mother Russia',font=F(bold,123),fill=COLORS['paper'])
d.text((148,600),'MỘT NƯỚC NGA CHỈ TỒN TẠI TRONG KÝ ỨC',font=F(sans,32),fill=COLORS['ice'])
d.rectangle((78,2302,1822,2398),fill=COLORS['night'])
d.text((145,2320),'YELLOW BEANIE  /  ALL BLACK  /  GẤU',font=F(sans,36),fill=COLORS['gold'])
p.save(ROOT/'art/00_CHAPTER_POSTER_A4.jpg',quality=91,optimize=True)
# standalone quote + accompanying history diagram
ins=Image.new('RGB',(1600,1000),COLORS['paper']);dr=ImageDraw.Draw(ins)
dr.rectangle((28,28,1572,972),outline=COLORS['blue'],width=7)
dr.text((95,100),'A MEMORY, NOT A MAP',font=F(sans,29),fill=COLORS['blue'])
nodes=[('Ông nội','family',235,430),('Soviet blocks','places',510,300),('Salad Nga','objects',820,300),('voz / internet','media',1110,430),('Stalingrad','game memory',840,650),('Tuyết & Volga','dream',410,670)]
center=(790,485)
for label,sub,x,y in nodes:
 dr.line((center[0],center[1],x,y),fill=COLORS['blue'],width=4)
 dr.ellipse((x-86,y-61,x+86,y+61),fill=COLORS['night'],outline=COLORS['gold'],width=3)
 box=dr.textbbox((0,0),label,font=F(sans,20));dr.text((x-(box[2]-box[0])/2,y-14),label,font=F(sans,20),fill=COLORS['paper'])
 dr.text((x,y+68),sub,font=F(sans,15),fill=COLORS['blue'],anchor='mt')
dr.ellipse((center[0]-117,center[1]-75,center[0]+117,center[1]+75),fill=COLORS['blue'],outline=COLORS['night'],width=4)
dr.text(center,'MY IMAGINED\nRUSSIA',font=F(bold,30),fill=COLORS['paper'],anchor='mm',align='center')
ins.save(ROOT/'art/12_memory_graph.jpg',quality=90,optimize=True)

# Instagram 3:4 1080x1440 styled cards: hero + four moments
story=[
('For Mother Russia','Một nơi tôi chưa từng đặt chân tới.','01_HERO_beanie_Gau_blue_winter.jpg'),
('Những câu chuyện của ông','Một chút tự hào, một chút hoài niệm.','03_grandfather.jpg'),
('Món salad Nga','Một món ăn mà tôi vẫn không hiểu sao ngon.','05_russian_salad.jpg'),
('Stalingrad','Một đứa trẻ đã tưởng mình ở trong trận đánh.','06_stalingrad_game_memory.jpg'),
('A place I never knew','Liệu nước Nga ấy có từng tồn tại ngoài đầu mình?','02_snowy_path.jpg')]
for i,(tit,sub,filename) in enumerate(story,1):
 out=Image.new('RGB',(1080,1440),COLORS['paper']);im=Image.open(ROOT/'art'/filename).convert('RGB')
 fit=ImageOps.fit(im,(1000,925),Image.Resampling.LANCZOS)
 out.paste(fit,(40,40));dd=ImageDraw.Draw(out)
 dd.rectangle((40,40,1040,965),outline=COLORS['blue'],width=8)
 dd.text((57,1000),f'0{i} / .json',font=F(sans,28),fill=COLORS['blue'])
 # wrap large text
 def wrap(txt,font,maxw):
  words=txt.split();res=[];current=''
  for w in words:
   q=(current+' '+w).strip()
   if dd.textbbox((0,0),q,font=font)[2] > maxw and current:res.append(current);current=w
   else:current=q
  if current:res.append(current)
  return res
 y=1055
 for line in wrap(tit,F(bold,45),950):dd.text((57,y),line,font=F(bold,45),fill=COLORS['navy']);y+=65
 for line in wrap(sub,F(serif,29),950):dd.text((57,y),line,font=F(serif,29),fill=COLORS['blue']);y+=46
 dd.text((1016,1390),'UNDER REVISION',font=F(sans,18),fill=COLORS['blue'],anchor='ra')
 out.save(ROOT/f'social/instagram/{i:02d}_card_3x4.jpg',quality=88,optimize=True)
# social special variants
for name,sz in [('facebook_1600x900.jpg',(1600,900)),('youtube_thumbnail_1280x720.jpg',(1280,720)),('cover_1080x1920.jpg',(1080,1920))]:
 art=Image.open(ROOT/'art/01_HERO_beanie_Gau_blue_winter.jpg').convert('RGB')
 v=ImageOps.fit(art,sz,Image.Resampling.LANCZOS)
 overlay=Image.new('RGBA',sz,(0,0,0,0));ov=ImageDraw.Draw(overlay)
 ov.rectangle((0,0,sz[0],int(sz[1]*.19)),fill=(6,24,42,195))
 ov.text((int(sz[0]*.05),int(sz[1]*.03)),'.json / 03',font=F(sans,max(27,int(sz[0]*.035))),fill=COLORS['gold'])
 ov.text((int(sz[0]*.05),int(sz[1]*.095)),'For Mother Russia',font=F(bold,max(40,int(sz[0]*.056))),fill=COLORS['paper'])
 v=Image.alpha_composite(v.convert('RGBA'),overlay).convert('RGB')
 v.save(ROOT/('social/'+name if name!='cover_1080x1920.jpg' else 'video/'+name.replace('.jpg','.jpg')),quality=87,optimize=True)
print('art complete',len(list((ROOT/'art').iterdir())))
