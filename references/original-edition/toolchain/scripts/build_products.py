"""Build illustrations, print proofs, channel art and edit cuts awaiting author narration.

Usage: python scripts/build_products.py [--chapter SLUG] [--video] [--ffmpeg PATH]
The original illustrations and approved manuscripts are never overwritten.
"""
import argparse
import hashlib
import html
import math
import os
import re
import shutil
import subprocess
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image as PDFImage
from reportlab.lib.pagesizes import A5
from common import ROOT, chapters, paragraphs, plain, read_json, write_json, safe_path


def font_files():
    locations=[Path(os.environ.get('CHAPTER_FONT_DIR','fonts')),Path('C:/Windows/Fonts'),Path('/usr/share/fonts/truetype/dejavu')]
    for directory in locations:
        for names in [('times.ttf','timesbd.ttf','timesi.ttf','arial.ttf'),('DejaVuSerif.ttf','DejaVuSerif-Bold.ttf','DejaVuSerif-Italic.ttf','DejaVuSans.ttf')]:
            if all((directory/name).exists() for name in names):
                return [str(directory/name) for name in names]
    raise RuntimeError('Set CHAPTER_FONT_DIR to a directory with Times/Arial or DejaVu TTF fonts.')

FONTS=font_files()
for name,path in zip(['Chapter','ChapterBold','ChapterItalic','Label'],FONTS):
    pdfmetrics.registerFont(TTFont(name,path))
pdfmetrics.registerFontFamily('Chapter',normal='Chapter',bold='ChapterBold',italic='ChapterItalic',boldItalic='ChapterBold')

def font(size,kind=0):
    return ImageFont.truetype(FONTS[kind],size)

def cover(image,size,center=(.5,.5)):
    return ImageOps.fit(image.convert('RGB'),size,Image.Resampling.LANCZOS,centering=center)

def lines(text,face,width):
    draw=ImageDraw.Draw(Image.new('RGB',(1,1)))
    output=[]
    for paragraph in text.split('\n'):
        line=''
        for word in paragraph.split():
            candidate=(line+' '+word).strip()
            if draw.textlength(candidate,font=face)>width and line:
                output.append(line);line=word
            else:
                line=candidate
        output.append(line)
    return output

def text_block(draw,text,xy,width,face,fill,spacing=1.25):
    x,y=xy
    for line in lines(text,face,width):
        draw.text((x,y),line,font=face,fill=fill)
        y+=round(face.size*spacing)
    return y

def save(image,path):
    path.parent.mkdir(parents=True,exist_ok=True)
    image.convert('RGB').save(path,quality=92,optimize=True,subsampling=0)

def crop_scenes(folder,meta):
    production=read_json(folder/'production.json')
    if not production['scenes']:raise ValueError(f'{meta["slug"]}: define scenes in production.json')
    records=[]
    source=None
    for i,scene in enumerate(production['scenes'],1):
        name=scene['id'];box=scene.get('box',[0,0,1,1])
        raster=scene.get('raster',meta['illustration'])
        original=Image.open(safe_path(folder,raster)).convert('RGB')
        if source is None:source=original
        w,h=original.size
        bounds=tuple(round(v*(w if j%2==0 else h)) for j,v in enumerate(box))
        image=original.crop(bounds)
        path=folder/f'artwork/scenes/{i:02d}-{name}.jpg'
        save(image,path)
        records.append({'id':name,'path':path.relative_to(folder).as_posix(),'source':scene.get('source',meta['illustration']),'raster':raster,'source_crop_pixels':bounds,'native_size':list(image.size),'kind':scene.get('kind','crop of supplied illustration')})
    write_json(folder/'artwork/scenes/index.json',records)
    return source,records

def card(meta,image,text,size=(1080,1440),number=None,cover_card=False,scene_fit='cover'):
    w,h=size; palette=meta['palette']; margin=round(w*.065)
    result=Image.new('RGB',size,palette['paper']); draw=ImageDraw.Draw(result)
    def scene(size):
        if scene_fit=='cover':return cover(image,size)
        if scene_fit!='contain':raise ValueError('Unknown scene framing: '+scene_fit)
        framed=Image.new('RGB',size,palette['dark'])
        fitted=ImageOps.contain(image.convert('RGB'),size,Image.Resampling.LANCZOS)
        framed.paste(fitted,((size[0]-fitted.width)//2,(size[1]-fitted.height)//2))
        return framed
    if w>h:
        # Landscape films keep the scene and reading area beside one another.
        left=round(w*.47);x=left+round(w*.04);width=w-x-round(w*.04)
        result.paste(scene((left,h)),(0,0))
        draw=ImageDraw.Draw(result)
        draw.text((x,round(h*.07)),f'.json / {meta["number"]} / {number or "CHAPTER"}',font=font(round(h*.028),3),fill=palette['dark'])
        face=font(round(h*.062))
        while len(lines(text,face,width))*face.size*1.3>h*.62 and face.size>24:
            face=font(face.size-2)
        text_block(draw,text,(x,round(h*.23)),width,face,palette['dark'],1.3)
        text_block(draw,meta['title'],(x,round(h*.89)),width,font(round(h*.024),3),palette['dark'])
        return result
    draw.rectangle((margin//2,margin//2,w-margin//2,h-margin//2),outline=palette['dark'],width=2)
    draw.text((margin,margin),'.json',font=font(round(w*.052),2),fill=palette['dark'])
    label=f'{meta["number"]} / {number or "CHAPTER"}';label_font=font(round(w*.017),3)
    draw.text((w-margin-draw.textlength(label,font=label_font),margin+14),label,font=label_font,fill=palette['dark'])
    top=round(h*.14); bottom=round(h*(.65 if not cover_card else .61))
    result.paste(scene((w-2*margin,bottom-top)),(margin,top))
    draw=ImageDraw.Draw(result)
    size_start=round(w*(.075 if cover_card else .055))
    face=font(size_start,2 if cover_card else 0)
    while len(lines(text,face,w-2*margin))*face.size*1.26 > h-bottom-margin*1.9 and face.size>24:
        face=font(face.size-2,2 if cover_card else 0)
    text_block(draw,text,(margin,bottom+margin*.65),w-2*margin,face,palette['dark'])
    footer=f'{meta["title"]}  /  Jason, under revision';footer_font=font(round(w*.018),3)
    while draw.textlength(footer,font=footer_font)>w-2*margin:footer_font=font(footer_font.size-1,3)
    draw.text((margin,h-margin),footer,font=footer_font,fill=palette['dark'])
    return result

def artwork(folder,meta,source,scenes):
    hero=Image.open(folder/scenes[0]['path'])
    production=read_json(folder/'production.json')
    save(cover(hero,(1600,960)),folder/'artwork/exports/hero.jpg')
    mobile=cover(hero,tuple(production.get('hero_mobile_size',[900,1200])),(.58,.5))
    if production.get('mobile_composition')=='preserve-wide-scene':
        mobile=Image.new('RGB',(900,1200),meta['palette']['dark'])
        scene=cover(hero,(900,600),(.58,.5))
        mask=Image.new('L',scene.size,255);fade=ImageDraw.Draw(mask)
        for y in range(450,600):fade.line((0,y,900,y),fill=round(255*(600-y)/150))
        mobile.paste(scene,(0,0),mask)
    save(mobile,folder/'artwork/exports/hero-mobile.jpg')
    save(card(meta,hero,meta['title'],(1480,2100),cover_card=True),folder/'artwork/exports/cover-a5.jpg')
    save(card(meta,hero,meta['subtitle'],(1080,1920),cover_card=True),folder/'artwork/exports/poster-9x16.jpg')
    carousel=read_json(folder/'production.json')['carousel']
    if len(carousel)!=5:raise ValueError('Define five carousel cards in production.json')
    quotes=[item['text'] for item in carousel];picks=[item['scene'] for item in carousel]
    for i,(quote,pick) in enumerate(zip(quotes,picks),1):
        save(card(meta,Image.open(folder/scenes[pick]['path']),quote,number=f'{i:02d}'),folder/f'social/instagram/slide-{i:02d}.jpg')
    # Landscape layouts keep typography beside the scene instead of shrinking a portrait.
    for target,size in [('facebook/post.jpg',(1200,630)),('youtube/thumbnail.jpg',(1280,720))]:
        w,h=size; image=Image.new('RGB',size,meta['palette']['dark'])
        image.paste(cover(hero,(round(w*.55),h)),(0,0)); draw=ImageDraw.Draw(image)
        x=round(w*.60); width=w-x-45
        draw.text((x,60),f'.json / {meta["number"]}',font=font(24,3),fill=meta['palette']['accent'])
        title=meta['title'].replace('_','_\n')
        face=font(54,2)
        while len(lines(title,face,width))*face.size*1.25+len(lines(meta['subtitle'],font(25),width))*32>h-225:
            face=font(face.size-2,2)
        bottom=text_block(draw,title,(x,145),width,face,meta['palette']['paper'])
        text_block(draw,meta['subtitle'],(x,bottom+28),width,font(25),meta['palette']['paper'])
        save(image,folder/'social'/target)
    shutil.copy2(folder/'artwork/exports/poster-9x16.jpg',folder/'social/tiktok/cover.jpg')
    write_json(folder/'social/instagram/alt-text.json',[{'file':f'slide-{i:02d}.jpg','alt':f'Minh họa từ chương {meta["title"]}. Chữ trên thẻ: {quote}'} for i,quote in enumerate(quotes,1)])
    sheet=Image.new('RGB',(1500,440),meta['palette']['paper'])
    for i in range(5):
        image=Image.open(folder/f'social/instagram/slide-{i+1:02d}.jpg')
        image.thumbnail((280,400));sheet.paste(image,(10+i*300,20))
    save(sheet,folder/'previews/carousel.jpg')
    scene_sheet=Image.new('RGB',(1200,math.ceil(len(scenes)/4)*250),meta['palette']['paper'])
    draw=ImageDraw.Draw(scene_sheet)
    for i,scene in enumerate(scenes):
        x=(i%4)*300;y=(i//4)*250
        scene_sheet.paste(cover(Image.open(folder/scene['path']),(280,195)),(x+10,y+10))
        draw.text((x+10,y+215),scene['id'],font=font(17,3),fill=meta['palette']['dark'])
    save(scene_sheet,folder/'previews/artwork.jpg')
    return quotes

def pdf(folder,meta,scenes):
    path=folder/'book/chapter-A5-proof.pdf'
    palette=meta['palette']; width,height=A5
    def page_art(canvas,doc):
        canvas.setFillColor(HexColor(palette['paper']));canvas.rect(0,0,width,height,fill=1,stroke=0)
        canvas.setFillColor(HexColor(palette['dark']));canvas.setFont('Label',6)
        canvas.drawString(31,height-24,'.json / JASON, UNDER REVISION')
        canvas.drawRightString(width-31,height-24,f'{meta["number"]} / {meta["title"]}')
        canvas.setStrokeColor(HexColor(palette['accent']));canvas.line(31,29,width-31,29)
        canvas.drawString(31,18,'A5 EDITORIAL PROOF');canvas.drawRightString(width-31,18,str(doc.page))
    doc=SimpleDocTemplate(str(path),pagesize=A5,rightMargin=36,leftMargin=36,topMargin=46,bottomMargin=43,title=meta['title'],author='Jason')
    layout=read_json(folder/'production.json').get('print_layout',{})
    style=ParagraphStyle('Prose',fontName='Chapter',fontSize=layout.get('font_size',10.5),leading=layout.get('leading',16),textColor=HexColor(palette['ink']),spaceAfter=layout.get('paragraph_space',10),splitLongWords=False,allowWidows=0,allowOrphans=0)
    heading=ParagraphStyle('Heading',parent=style,fontName='ChapterBold',fontSize=layout.get('heading_size',27),leading=layout.get('heading_leading',33),spaceAfter=15)
    label=ParagraphStyle('Label',parent=style,fontName='Label',fontSize=8,leading=12)
    flow=[Paragraph(f'CHAPTER {meta["number"]}',label),Spacer(1,15),Paragraph(html.escape(meta['title']),heading),Paragraph(html.escape(meta['subtitle']),style),Spacer(1,15)]
    hero=Image.open(folder/'artwork/exports/hero.jpg')
    hero_width=min(width-72,layout.get('hero_height',1000)*hero.width/hero.height)
    flow += [PDFImage(str(folder/'artwork/exports/hero.jpg'),width=hero_width,height=hero_width*hero.height/hero.width),Spacer(1,18),Paragraph('.json — Jason, under revision',label),PageBreak()]
    prose=paragraphs(folder/meta['canonical_text'])
    print_scenes={item['after_paragraph']:item['scene'] for item in read_json(folder/'production.json')['print_scenes']}
    for index,text in enumerate(prose):
        escaped=html.escape(text)
        escaped=re.sub(r'`([^`]+)`',r'<font name="Label">\1</font>',escaped)
        escaped=re.sub(r'\*([^*]+)\*',r'<i>\1</i>',escaped)
        flow.append(Paragraph(escaped,style))
        if index in print_scenes:
            selected=scenes[print_scenes[index]]
            image=Image.open(folder/selected['path'])
            image_width=min(190,width-72);image_height=min(layout.get('image_height',125),image_width*image.height/image.width)
            flow.extend([Spacer(1,4),PDFImage(str(folder/selected['path']),width=image_width,height=image_height,kind='proportional'),Spacer(1,10)])
    doc.build(flow,onFirstPage=page_art,onLaterPages=page_art)
    try:
        import pymupdf as fitz
    except ImportError:
        print('PDF written; install PyMuPDF to render its contact sheet.')
        return
    document=fitz.open(path);thumbs=[]
    for page in document:
        pix=page.get_pixmap(matrix=fitz.Matrix(1.4,1.4))
        image=Image.frombytes('RGB',(pix.width,pix.height),pix.samples); image.thumbnail((295,420));thumbs.append(image)
    sheet=Image.new('RGB',(min(4,len(thumbs))*315,math.ceil(len(thumbs)/4)*450),'#d3d1c6')
    for i,image in enumerate(thumbs):sheet.paste(image,((i%4)*315+10,(i//4)*450+10))
    save(sheet,folder/'previews/book.jpg')
    print(meta['slug'],'PDF pages:',len(document))

def ambience(folder):
    path=folder/'audio/ambience.wav'
    if path.exists():return
    import struct
    rate=24000;seconds=24
    data=bytearray()
    for i in range(rate*seconds):
        t=i/rate;fade=min(1,t/2,(seconds-t)/2)
        sample=int(480*fade*(math.sin(2*math.pi*110*t)+.25*math.sin(2*math.pi*165*t)))
        data.extend(struct.pack('<h',sample))
    with wave.open(str(path),'wb') as out:
        out.setnchannels(1);out.setsampwidth(2);out.setframerate(rate);out.writeframes(data)

def timecode(t,vtt=False):
    ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02}{"." if vtt else ","}{ms:03}'

def film_plan(folder,meta,scenes,quotes):
    # Timed text cards are captions for this visual film, not claimed speech transcripts.
    variants=[]
    for plan in read_json(folder/'production.json')['films']:
        name=plan['name'];size=plan['size']
        timeline=[];clock=0
        for segment in plan['segments']:
            text=segment['text'];duration=segment['duration']
            timeline.append({'start':round(clock,3),'end':round(clock+duration,3),'text':text,'scene':segment['scene']})
            clock+=duration
        variant={'name':name,'size':size,'duration':round(clock,3),'segments':timeline,'status':'edit preview awaiting author narration','timing':'provisional; retime to supplied recording','audio':'synthetic ambience; no spoken narration','caption_kind':'on-screen text timing; not narration subtitles'}
        if 'scene_fit' in plan:variant['scene_fit']=plan['scene_fit']
        variants.append(variant)
        srt=[];vtt=['WEBVTT','']
        for i,seg in enumerate(timeline,1):
            wrapped='\n'.join(lines(seg['text'],font(24),500))
            srt.append(f'{i}\n{timecode(seg["start"])} --> {timecode(seg["end"])}\n{wrapped}\n')
            vtt.append(f'{timecode(seg["start"],True)} --> {timecode(seg["end"],True)}\n{wrapped}\n')
        (folder/f'video/{name}.srt').write_text('\n'.join(srt),encoding='utf-8')
        (folder/f'video/{name}.vtt').write_text('\n'.join(vtt),encoding='utf-8')
        script=['# '+meta['title']+' — '+name,'','Recording script: exact text-card excerpts, in sequence. Timings are provisional; record naturally and retime the edit to the recording.','']
        script.extend(segment['text']+'\n' for segment in timeline)
        (folder/f'audio/{name}-script.md').write_text('\n'.join(script),encoding='utf-8')
    write_json(folder/'video/timeline.json',variants)
    storyboard=['# '+meta['title']+' — film storyboard','','EDIT PREVIEWS — awaiting Jason’s recorded narration. The current text-card timings and ambient mix are provisional. Retime the cuts and regenerate speech subtitles after importing the author’s recording. The 3:4 feed cut is distinct from the 9:16 platform cuts.','']
    for variant in variants:
        storyboard.append(f'## {variant["name"]} — {variant["duration"]} seconds\n')
        storyboard.extend(f'- {s["start"]:.1f}–{s["end"]:.1f}s: {s["text"]}' for s in variant['segments'])
    (folder/'video/STORYBOARD.md').write_text('\n'.join(storyboard)+'\n',encoding='utf-8')
    (folder/'audio/NARRATION.md').write_text('# Narration\n\nVoice generation remains stopped. These films use on-screen manuscript excerpts and synthetic ambience. For a narrated edition, record the approved text or discovery excerpt with Jason, then retime the cut and speech captions to that actual recording. Existing SRT/VTT tracks describe the text-card timing; they are not a narration transcript.\n',encoding='utf-8')
    shutil.copy2(folder/meta['canonical_text'],folder/'audio/reading-script.md')
    return variants

def supplemental_products(folder,meta,scenes):
    """Optional channel formats declared by an individual production board."""
    recipe=read_json(folder/'production.json').get('supplemental',{})
    alts=[]
    for item in recipe.get('cards',[]):
        source=Image.open(folder/scenes[item['scene']]['path'])
        save(card(meta,source,item['text'],tuple(item['size']),number=item.get('label')),safe_path(folder,item['path']))
        alts.append({'file':item['path'],'alt':item['alt']})
    alts.extend(recipe.get('alt_text',[]))
    if alts:write_json(folder/'social/alt-text.json',alts)
    for relative,text in recipe.get('copy',{}).items():
        path=safe_path(folder,relative);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(text.rstrip()+'\n',encoding='utf-8')
    if recipe.get('editable_cover'):
        title_lines=lines(meta['title'],font(110,2),1280)
        spans=''.join(f'<tspan x="100" dy="{0 if i==0 else 138}">{html.escape(line)}</tspan>' for i,line in enumerate(title_lines))
        svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1480" height="2100" viewBox="0 0 1480 2100" role="img" aria-label="{html.escape(meta['title'])}">
<rect width="1480" height="2100" fill="{meta['palette']['paper']}"/>
<rect x="48" y="48" width="1384" height="2004" fill="none" stroke="{meta['palette']['dark']}" stroke-width="3"/>
<g font-family="Times New Roman,Times,serif" fill="{meta['palette']['dark']}"><text x="100" y="170" font-size="76">.json</text><text x="100" y="245" font-size="28">CHAPTER {meta['number']} / JASON, UNDER REVISION</text>
<image href="../scenes/{Path(scenes[0]['path']).name}" x="100" y="320" width="1280" height="950" preserveAspectRatio="xMidYMid slice"/>
<text x="100" y="1460" font-size="110" font-style="italic">{spans}</text>
<text x="100" y="1890" font-size="40">{html.escape(meta['subtitle'])}</text></g></svg>'''
        (folder/'artwork/exports/cover-a5.svg').write_text(svg,encoding='utf-8')

def print_extras(folder,meta,scenes):
    """Optional A4 poster and 50 x 150 mm bookmark, both trim-size proofs."""
    if not read_json(folder/'production.json').get('print_extras'):return
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib.utils import ImageReader
    palette=meta['palette']
    for filename,size,bookmark in [('poster-A4-proof.pdf',A4,False),('bookmark-proof.pdf',(50*mm,150*mm),True)]:
        width,height=size; margin=12 if bookmark else 35
        out=canvas.Canvas(str(folder/'book'/filename),pagesize=size)
        out.setTitle(meta['title']+(' — bookmark' if bookmark else ' — poster'));out.setAuthor('Jason')
        out.setFillColor(HexColor(palette['paper']));out.rect(0,0,width,height,fill=1,stroke=0)
        out.setStrokeColor(HexColor(palette['dark']));out.rect(margin/2,margin/2,width-margin,height-margin)
        out.setFillColor(HexColor(palette['dark']));out.setFont('ChapterItalic',16 if bookmark else 33)
        out.drawString(margin,height-margin-23,'.json')
        out.setFont('Label',5 if bookmark else 9);out.drawString(margin,height-margin-40,f'CHAPTER {meta["number"]} / JASON, UNDER REVISION')
        art_height=height*(.32 if bookmark else .48)
        image=cover(Image.open(folder/scenes[0]['path']),(int((width-2*margin)*4),int(art_height*4)))
        art_bottom=height-margin-58-art_height
        out.drawImage(ImageReader(image),margin,art_bottom,width=width-2*margin,height=art_height)
        title=Paragraph(html.escape(meta['title']),ParagraphStyle('ExtraTitle',fontName='ChapterItalic',fontSize=16 if bookmark else 34,leading=18 if bookmark else 40,textColor=HexColor(palette['dark'])))
        _,th=title.wrap(width-2*margin,height);title.drawOn(out,margin,art_bottom-18-th)
        if not bookmark:
            subtitle=Paragraph(html.escape(meta['subtitle']),ParagraphStyle('ExtraSub',fontName='Chapter',fontSize=15,leading=20,textColor=HexColor(palette['dark'])))
            _,sh=subtitle.wrap(width-2*margin,height);subtitle.drawOn(out,margin,art_bottom-38-th-sh)
        out.setFont('Label',5 if bookmark else 8)
        out.drawString(margin,margin+15,('.json / CHAPTER ' if bookmark else 'JASON, UNDER REVISION / CHAPTER ')+meta['number'])
        out.drawString(margin,margin+5,'EDITORIAL PROOF / '+('50 x 150 mm' if bookmark else 'A4'))
        out.save()

def render_film(folder,meta,variant,ffmpeg):
    size=tuple(variant['size']);w,h=size
    work=ROOT/'build/media'/meta['slug']/variant['name'];work.mkdir(parents=True,exist_ok=True)
    segments=[]
    for i,segment in enumerate(variant['segments']):
        frame=card(meta,Image.open(folder/segment['scene']),segment['text'],size,number=f'{i+1:02d}',scene_fit=variant.get('scene_fit','cover'))
        # Typography stays static while the still image gently fades at scene boundaries.
        still=work/f'{i:02d}.png';frame.save(still)
        output=work/f'{i:02d}.mp4';duration=segment['end']-segment['start']
        command=[ffmpeg,'-y','-hide_banner','-loglevel','error','-loop','1','-framerate','24','-i',str(still),'-t',str(duration),'-vf',f'fade=t=in:d=0.35,fade=t=out:st={max(.4,duration-.35)}:d=0.35,format=yuv420p','-c:v','libx264','-preset','veryfast','-tune','stillimage','-crf','24','-r','24','-threads','4',str(output)]
        subprocess.run(command,check=True)
        segments.append(output)
    listing=work/'concat.txt';listing.write_text(''.join(f"file '{p.name}'\n" for p in segments),encoding='utf-8')
    out=folder/f'video/{variant["name"]}.mp4'
    subprocess.run([ffmpeg,'-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-stream_loop','-1','-i',str(folder/'audio/ambience.wav'),'-t',str(variant['duration']),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','96k','-af','afade=t=in:d=1,afade=t=out:st='+str(max(1,variant['duration']-2))+':d=2','-movflags','+faststart',str(out)],check=True)
    print(meta['slug'],variant['name'],'rendered',out.stat().st_size,flush=True)

def copy_and_notes(folder,meta,scenes,quotes):
    url=read_json(ROOT/'book.json')['public_url']+meta['canonical_path']
    captions={
        'instagram/caption.md':f'{quotes[0]}\n\n{meta["title"]} — .json / Jason, under revision.\n\nĐọc chương: {url}\n\n#jsonunderrevision #Memoir',
        'facebook/post.md':f'{quotes[2]}\n\n{quotes[3]}\n\nMột chương trong .json — Jason, under revision.\nĐọc {meta["title"]}: {url}',
        'tiktok/caption.md':f'{quotes[1]}\n\n{meta["title"]} / .json\nĐọc trọn chương: {url}\n\nFilm: ../../video/discovery-9x16.mp4\nCaptions: ../../video/discovery-9x16.srt\nAudio: original synthetic ambience; no narrator.',
        'youtube/description.md':f'# {meta["title"]} | .json — Jason, under revision\n\n{meta["subtitle"]}\n\nĐọc chương: {url}\n\nDiscovery cut: ../../video/discovery-9x16.mp4\nCompanion film: ../../video/youtube-9x16.mp4\nFormat: 1080×1920; edit preview with synthetic ambience; awaiting the author recording.\nCredits: Jason — selected prose and supplied illustration. Scene crops and layout are interpretive. No voice performance or documentary footage is claimed.'
    }
    for path,text in captions.items():(folder/'social'/path).write_text(text+'\n',encoding='utf-8')
    (folder/'docs/DESIGN_REVIEW.md').write_text(f'''# {meta['title']} — production board review

The supplied board defines the mood, composition and product categories. This build uses its cream-paper layouts, dark chapter palette, generous serif text, illustrated opener, social cards, scene details, film frames and a chapter portal with Read / Explore / Revisit.

The scene library contains {len(scenes)} documented crops of the author-selected source illustration. These are not new paintings or newly generated perspectives. The source remains untouched. The small source resolution limits close-up and print fidelity; enlargement does not create detail. See artwork/scenes/index.json for native crop sizes.

The illustrated A5 PDF contains the complete approved prose and genuine page numbers. It is an editorial proof. The board's pictured QR is not copied: the author's print QR decision remains deferred. No printer-specific bleed, CMYK conversion or PDF/X certification is claimed.

The website uses real text, playable videos, real ambient audio, functional archive controls and downloadable files. Location and reading time are not copied from the board; location remains unspecified and reading time is calculated from text. No fake store, account, narration player or completion tick is added.

These are edit cuts prepared for the author's recorded narration, as explicitly selected in this session. Current captions are timed to the on-screen text cards; timing is provisional and will change with the recording. The illustrated probability numbers on the Expected_utility board are not used as actual relationship predictions; the interactive artifact keeps unobserved outcomes unknown.
''',encoding='utf-8')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chapter');parser.add_argument('--video',action='store_true');parser.add_argument('--ffmpeg',default=shutil.which('ffmpeg'))
    args=parser.parse_args()
    if args.video and not args.ffmpeg:parser.error('--video requires ffmpeg on PATH or --ffmpeg PATH')
    for folder,meta in chapters(args.chapter):
        if not meta['publish'] and not args.chapter:
            continue
        if meta.get('release_stage','multimedia')!='multimedia':
            if args.chapter:parser.error('This chapter does not use the shared multimedia production recipe. Its reader or supplied products must be maintained separately.')
            continue
        source,scenes=crop_scenes(folder,meta)
        quotes=artwork(folder,meta,source,scenes)
        pdf(folder,meta,scenes);ambience(folder)
        variants=film_plan(folder,meta,scenes,quotes)
        copy_and_notes(folder,meta,scenes,quotes)
        supplemental_products(folder,meta,scenes)
        print_extras(folder,meta,scenes)
        if args.video:
            for variant in variants:render_film(folder,meta,variant,args.ffmpeg)
        print('Built product assets:',meta['slug'],flush=True)

if __name__=='__main__':main()
