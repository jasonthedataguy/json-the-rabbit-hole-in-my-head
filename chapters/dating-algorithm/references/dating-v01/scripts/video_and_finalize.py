from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import numpy as np, wave, math, subprocess, json, zipfile, os, shutil
R=Path('/mnt/data/Dating_Algorithm_Chapter04_v01')
font='/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf';reg='/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
# 24s timeline: five visual beats.
titles=['WELCOME TO MY TED TALK','A VERY CONFIDENT MODEL','MATCHING IS NOT EQUILIBRIUM','TEN PROFILES. NO RESULTS.','PEOPLE ARE NOT EQUATIONS']
subs=['Opening / satirical lecture','70% and 90% are invented weights','Strategies and payoffs matter','Study outcomes are still missing','Chemistry cannot be scored']

def srt_time(v):
 h=int(v//3600);m=int(v%3600//60);s=int(v%60);ms=int(round((v-int(v))*1000));return f'{h:02}:{m:02}:{s:02},{ms:03}'
with (R/'video'/'VISUAL_BEAT_CAPTIONS_NOT_VOICE.srt').open('w',encoding='utf-8') as f:
 for i,(a,b) in enumerate(zip(titles,subs)):
  f.write(f'{i+1}\n{srt_time(i*4.8)} --> {srt_time((i+1)*4.8)}\n{a}\n{b}\n\n')
# original ambient audio, not music sampled from others
rate=22050; sec=24; t=np.arange(rate*sec)/rate
np.random.seed(11)
a=.013*np.sin(t*2*np.pi*72)+.008*np.sin(t*2*np.pi*109)+.004*np.random.randn(len(t))
env=np.minimum(1,np.minimum(t/1.6,(24-t)/1.8));a=np.int16(np.clip(a*env,-.8,.8)*32767)
with wave.open(str(R/'video'/'ORIGINAL_SYNTHETIC_AMBIENCE.wav'),'wb') as f:
 f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate);f.writeframes(a.tobytes())
# video stems concat demuxer uses absolute paths
lst=R/'video'/'_frames.txt'
with lst.open('w') as f:
 for i in range(1,6):f.write("file '"+str(R/'video'/'stills'/f'{i:02d}.jpg')+"'\n"+'duration 4.8\n')
 f.write("file '"+str(R/'video'/'stills'/'05.jpg')+"'\n")
cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(lst),'-i',str(R/'video'/'ORIGINAL_SYNTHETIC_AMBIENCE.wav'),'-vf','fps=12,format=yuv420p','-c:v','libx264','-preset','ultrafast','-crf','23','-c:a','aac','-b:a','96k','-shortest','-t','24','-movflags','+faststart',str(R/'video'/'04_Dating_Algorithm_ANIMATIC_9x16.mp4')]
r=subprocess.run(cmd,capture_output=True,text=True);print('ffmpeg vertical',r.returncode,r.stderr[:350]);assert r.returncode==0
# Landscape visual frames for optional 16:9 storyboard cut
p=R/'video'/'landscape_stills';p.mkdir(exist_ok=True)
for i in range(1,6):
 im=Image.open(R/'video'/'stills'/f'{i:02d}.jpg').convert('RGB')
 canvas=Image.new('RGB',(1280,720),'#092B25')
 img=ImageOps.fit(im,(510,720),method=Image.Resampling.LANCZOS)
 canvas.paste(img,(0,0));d=ImageDraw.Draw(canvas)
 d.text((550,115),'JASON / 04',font=ImageFont.truetype(font,35),fill='#EF7DA9')
 title=titles[i-1]
 lines=[];acc=''
 for w in title.split():
  test=(acc+' '+w).strip()
  if d.textbbox((0,0),test,font=ImageFont.truetype(font,57))[2]>665:lines.append(acc);acc=w
  else:acc=test
 lines.append(acc)
 for j,l in enumerate(lines):d.text((550,215+j*77),l,font=ImageFont.truetype(font,57),fill='#F7EBD6')
 d.text((550,620),subs[i-1],font=ImageFont.truetype(reg,21),fill='#EF7DA9')
 canvas.save(p/f'{i:02d}.jpg',quality=86)
lst2=R/'video'/'_landscape.txt'
with lst2.open('w') as f:
 for i in range(1,6):f.write("file '"+str(p/f'{i:02d}.jpg')+"'\n"+'duration 4.8\n')
 f.write("file '"+str(p/'05.jpg')+"'\n")
cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(lst2),'-i',str(R/'video'/'ORIGINAL_SYNTHETIC_AMBIENCE.wav'),'-vf','fps=12,format=yuv420p','-c:v','libx264','-preset','ultrafast','-crf','24','-c:a','aac','-b:a','96k','-shortest','-t','24','-movflags','+faststart',str(R/'video'/'04_Dating_Algorithm_YOUTUBE_16x9_AMBIENT_PROOF.mp4')]
r=subprocess.run(cmd,capture_output=True,text=True);print('ffmpeg landscape',r.returncode,r.stderr[:350]);assert r.returncode==0
# Contact sheet / asset overview
files=[R/'art'/'00_CHAPTER_04_COVER.jpg',R/'art'/'01_stage_hero_PREVIS.jpg',R/'art'/'10_matching_hypothetical.png',R/'art'/'09_funnel_original_diagram.png',R/'social'/'instagram'/'01_dating_algorithm_3x4.jpg',R/'social'/'instagram'/'03_dating_algorithm_3x4.jpg',R/'video'/'stills'/'01.jpg',R/'video'/'stills'/'05.jpg']
W,H=1600,1450;cs=Image.new('RGB',(W,H),'#f7ebd6');d=ImageDraw.Draw(cs)
d.text((45,27),'DATING ALGORITHM  /  PRODUCTION ASSET OVERVIEW',font=ImageFont.truetype(font,44),fill='#092B25')
for i,fp in enumerate(files):
 x=35+(i%4)*390;y=115+(i//4)*635
 img=Image.open(fp).convert('RGB');img.thumbnail((372,560))
 cx=x+(372-img.width)//2;cy=y+(555-img.height)//2
 cs.paste(img,(cx,cy));d.text((x+4,y+567),fp.name[:29],font=ImageFont.truetype(reg,18),fill='#092B25')
cs.save(R/'previews'/'ASSET_OVERVIEW.jpg',quality=86)
print('video sizes',[(p.name,round(p.stat().st_size/1e6,2)) for p in (R/'video').glob('*.mp4')])
