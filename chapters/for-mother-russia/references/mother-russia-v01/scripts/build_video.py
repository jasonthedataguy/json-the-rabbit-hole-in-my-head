from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import wave, numpy as np, subprocess, math
R=Path(__file__).resolve().parents[1]
F=lambda s:ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSerif-SemiBold.ttf',s)
A=lambda s:ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf',s)
scene=[('01_HERO_beanie_Gau_blue_winter.jpg','Một giấc mơ về tuyết','Chưa từng đặt chân tới Nga'),('03_grandfather.jpg','Những câu chuyện của ông','Một miền đất xa thành thân thuộc'),('05_russian_salad.jpg','Một món salad Nga','Mà tôi vẫn không hiểu sao ngon'),('06_stalingrad_game_memory.jpg','Stalingrad qua màn hình','Không phải lịch sử trọn vẹn'),('02_snowy_path.jpg','Một nước Nga trong đầu','Gấu cùng tôi trở về trong tranh')]
for i,(f,title,sub) in enumerate(scene,1):
 w,h=720,1280; base=ImageOps.fit(Image.open(R/'art'/f).convert('RGB'),(w,h),Image.Resampling.LANCZOS)
 layer=Image.new('RGBA',(w,h),(0,0,0,0));d=ImageDraw.Draw(layer)
 d.rectangle((0,0,w,180),fill=(5,19,35,219));d.rectangle((0,958,w,h),fill=(5,19,35,228))
 d.text((42,53),f'.json / 03 — {i:02d}',fill='#F6C16E',font=A(26))
 # split long into 2 lines
 words=title.split();lines=[];cur=''
 for x in words:
  k=(cur+' '+x).strip()
  if d.textbbox((0,0),k,font=F(38))[2]>650 and cur:lines.append(cur);cur=x
  else:cur=k
 if cur:lines.append(cur)
 for j,line in enumerate(lines):d.text((42,1020+j*54),line,fill='#F6F1E5',font=F(38))
 d.text((42,1170),sub,fill='#C8DDF1',font=A(19))
 base=Image.alpha_composite(base.convert('RGBA'),layer).convert('RGB')
 base.save(R/f'video/stills/{i:02d}.jpg',quality=86,optimize=True)
# mono stereo ambient with filtered noise, original synthesized, not licensed music or narration
sr=24000;t=np.arange(sr*24)/sr;rng=np.random.default_rng(22);r=rng.normal(0,1,len(t));
# soft low pass signal to evoke cold air
kernel=np.ones(650)/650;soft=np.convolve(r,kernel,mode='same');waveform=np.clip((soft*0.40+0.004*np.sin(2*np.pi*95*t))*32767,-32768,32767).astype(np.int16)
with wave.open(str(R/'video/ambient_synth.wav'),'wb') as w:
 w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(waveform.tobytes())
with (R/'video/concat.txt').open('w') as fo:
 for i in range(1,6):
  fo.write(f"file 'stills/{i:02d}.jpg'\nduration 4.8\n")
 fo.write("file 'stills/05.jpg'\n")
cmd=['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(R/'video/concat.txt'),'-i',str(R/'video/ambient_synth.wav'),'-t','24','-vf','fps=12,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','23','-c:a','aac','-b:a','96k','-movflags','+faststart',str(R/'video/03_Mother_Russia_ANIMATIC_9x16.mp4')]
subprocess.run(cmd,check=True)
print('video done')
