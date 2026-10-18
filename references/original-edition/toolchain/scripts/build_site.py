"""Build the chapter registry into a static archive. Python standard library only."""
import argparse
import html
import math
import re
import shutil
import stat
from pathlib import Path
from string import Template
from zipfile import ZIP_DEFLATED, ZipFile
from common import ROOT, chapters, inline, paragraphs, plain, read_json, safe_path

def reader_release(meta):
    stage=meta.get('release_stage','multimedia')
    if stage not in {'reader','multimedia','supplied'}:raise ValueError('Unknown chapter release stage: '+stage)
    return stage=='reader'

def render_chapter(folder,meta,config,next_meta):
    reader=reader_release(meta)
    supplied=meta.get('release_stage')=='supplied'
    name='chapter-reader.html' if reader else 'chapter.html'
    template_path=safe_path(folder,meta['web_template']) if meta.get('web_template') else ROOT/'shared'/name
    template=Template(template_path.read_text(encoding='utf-8'))
    prose=paragraphs(safe_path(folder,meta['canonical_text']))
    illustrations={}
    for illustration in meta.get('reading_illustrations',[]):
        index=illustration['after_paragraph']
        if not isinstance(index,int) or not 0<=index<len(prose):
            raise ValueError('Reading illustration must follow an existing paragraph')
        tag=f'<img class="chapter-art" src="{html.escape(illustration["src"])}" alt="{html.escape(illustration["alt"])}" width="{int(illustration["width"])}" height="{int(illustration["height"])}" loading="lazy">'
        illustrations.setdefault(index,[]).append(tag)
    history=meta.get('history_text','source/original.md')
    values={
      **meta['palette'],'title':html.escape(meta['title']),'subtitle':html.escape(meta['subtitle']),
      'number':meta['number'],'url':config['public_url']+meta['canonical_path'],
      'hero_alt':html.escape(meta.get('hero_alt',f'Minh họa chương {meta["title"]}')),
      'minutes':str(max(1,math.ceil(sum(len(plain(p).split()) for p in prose)/220))),
      'tags':''.join(f'<span class="tag">{html.escape(tag)}</span>' for tag in meta['theme']),
      'story':''.join(f'<p>{inline(p)}</p>'+''.join(illustrations.get(index,[])) for index,p in enumerate(prose)),
      'closing_quote':inline(prose[-1]),
      'artifact':'' if supplied else artifact(folder,meta),
      'film_note':'Những khoảnh khắc từ chương được đặt cạnh nhau, cùng chữ trên màn hình và âm thanh nền.',
      'original':''.join(f'<p>{inline(p)}</p>' for p in paragraphs(safe_path(folder,history))),
      'history_label':html.escape(meta.get('history_label','original.md — bản gốc')),
      'revisions':html.escape((folder/'source/revisions.log').read_text(encoding='utf-8')),
      'revision_note':html.escape(meta.get('revision_note','Bản đang đọc là bản tác giả đã chọn. Bản gốc được giữ lại để những thay đổi không biến mất.')),
      'gallery':'',
      'next_url':'../../'+next_meta['canonical_path'],'next_title':html.escape(next_meta['title']),
    }
    if not reader and not supplied:
        alts=read_json(folder/'social/instagram/alt-text.json')
        values['gallery']=''.join(f'<a href="social/instagram/slide-{i:02d}.jpg" download><img src="social/instagram/slide-{i:02d}.jpg" alt="{html.escape(alts[i-1]["alt"])}" width="1080" height="1440" loading="lazy"></a>' for i in range(1,6))
    return template.substitute(values),values

def remove_readonly(function,path,error):
    if not isinstance(error[1],PermissionError):raise error[1]
    Path(path).chmod(stat.S_IREAD|stat.S_IWRITE|stat.S_IEXEC);function(path)

def redirect(path,url,canonical=None):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url={html.escape(url)}"><title>.json — chapter archive</title>'+ (f'<link rel="canonical" href="{canonical}">' if canonical else '')+f'</head><body><a href="{html.escape(url)}">Mở chương →</a></body></html>',encoding='utf-8')

def artifact(folder,meta):
    template=(ROOT/'shared'/f'{meta["artifact"]}.html').read_text(encoding='utf-8')
    if meta['artifact']=='memory':
        memory=read_json(folder/'production.json')['memory']
        first=memory['moments'][0]
        values={k:html.escape(v) for k,v in {**first,**{k:memory[k] for k in ['heading','intro']}}.items()}
        values['buttons']=''.join(f'<button type="button" data-memory="{i}" data-image="{html.escape(m["image"])}" data-alt="{html.escape(m["alt"])}" data-quote="{html.escape(m["quote"])}" aria-pressed="{str(i==0).lower()}">{html.escape(m["title"])}</button>' for i,m in enumerate(memory['moments']))
        return Template(template).substitute(values)
    return template

def build_site():
    config=read_json(ROOT/'book.json');site=ROOT/'site'
    if site.resolve()!=ROOT.resolve()/'site':raise ValueError('Refusing to clean site outside repository')
    if site.exists():shutil.rmtree(site,onerror=remove_readonly)
    (site/'assets').mkdir(parents=True)
    for name in ['site.css','site.js']:shutil.copy2(ROOT/'shared'/name,site/'assets'/name)
    published=[(f,m) for f,m in chapters() if m['publish']]
    if not published:raise ValueError('No published chapters in book.json')
    cards=[]
    for index,(folder,meta) in enumerate(published):
        chapter=site/meta['canonical_path'];chapter.mkdir(parents=True)
        for name in ['artwork','book','audio','video','social','docs','previews','source']:
            if (folder/name).is_dir():shutil.copytree(folder/name,chapter/name)
        if (folder/'web/assets').is_dir():shutil.copytree(folder/'web/assets',chapter/'assets')
        shutil.copy2(folder/'chapter.json',chapter/'chapter.json')
        next_meta=published[(index+1)%len(published)][1]
        page,values=render_chapter(folder,meta,config,next_meta)
        (chapter/'index.html').write_text(page,encoding='utf-8')
        # A chapter's source preview works from both the repo and the downloadable ZIP.
        offline=re.sub(r'href="../../(?!assets/)',f'href="{config["public_url"]}',page)
        offline=offline.replace('../../assets/','../../../shared/')
        for directory in ['artwork','audio','video','book','social','source','previews','docs']:
            offline=re.sub(r'((?:href|src|srcset|data-image)=")'+directory+'/',r'\1../'+directory+'/',offline)
        offline=offline.replace('href="product-set.zip"',f'href="{values["url"]}product-set.zip"')
        (folder/'web').mkdir(exist_ok=True)
        (folder/'web/index.html').write_text(offline,encoding='utf-8')
        if not reader_release(meta):
            with ZipFile(chapter/'product-set.zip','w',ZIP_DEFLATED) as bundle:
                for source in sorted(folder.rglob('*')):
                    if source.is_file():bundle.write(source,source.relative_to(ROOT))
                for name in ['site.css','site.js']:bundle.write(ROOT/'shared'/name,'shared/'+name)
        for alias in meta['aliases']:redirect(site/alias/'index.html','../'+meta['number']+'/',values['url'])
        cards.append(f'<a class="chapter-card" href="{meta["canonical_path"]}"><img src="{meta["canonical_path"]}artwork/exports/hero.jpg" alt="{values["hero_alt"]}" width="1600" height="960"><div class="copy"><span class="eyebrow">CHAPTER {meta["number"]}</span><h2>{values["title"]}</h2><p>{values["subtitle"]}</p><span class="eyebrow">READ / EXPLORE / REVISIT →</span></div></a>')
    (site/'index.html').write_text('''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content=".json — Jason, under revision. Những câu chuyện và những gì còn lại."><title>.json — Jason, under revision</title><link rel="stylesheet" href="assets/site.css"></head><body><header class="bar"><a class="brand" href="./">.json<small>JASON, UNDER REVISION</small></a><nav aria-label="Điều hướng"><a href="#chapters">Chapters</a><a href="about/">About</a></nav></header><main class="home"><div class="eyebrow">A BOOK WITH A VERSION HISTORY</div><h1>.json</h1><p class="home-intro">Một cuốn sách với lịch sử phiên bản.<br>Những câu chuyện, những ký ức, và những điều chưa thể biết.</p><div class="chapter-grid" id="chapters">'''+''.join(cards)+'''</div><p class="quiet">Câu chuyện nằm trọn trong từng chương. Phần còn lại là lời mời nhìn gần hơn.</p></main><footer class="footer"><span>© Jason / .json — Jason, under revision</span><a href="about/">Về cuốn sách →</a></footer></body></html>''',encoding='utf-8')
    (site/'about').mkdir()
    (site/'about/index.html').write_text('''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>About — .json</title><link rel="stylesheet" href="../assets/site.css"></head><body><header class="bar"><a class="brand" href="../">.json<small>JASON, UNDER REVISION</small></a></header><main class="about"><div class="eyebrow">ABOUT THE BOOK</div><h1>Jason, under revision.</h1><p>.json là một cuốn hồi ký theo từng chương: những ký ức, những cách lý giải, và những điều có thể thay đổi khi nhìn lại.</p><p>Mỗi chương có một câu chuyện trọn vẹn. Kho lưu trữ đi cùng giữ lại hình ảnh, âm thanh, bản gốc và dấu vết chỉnh sửa — để bạn có thể đọc, khám phá, rồi quay lại.</p><p>Minh họa là diễn giải. Âm thanh nền được tổng hợp cho không gian đọc. Những bản dựng video hiện tại đang chờ giọng đọc của tác giả.</p><p><a href="../#chapters">Đọc các chương →</a></p></main></body></html>''',encoding='utf-8')
    # Preserve the prior release's public media URLs, including its complete delivery ZIP.
    previous=site/'chapters/04/files';previous.mkdir()
    source=ROOT/'archive/deliveries/expected-utility-v02'
    shutil.copytree(source/'web/assets',site/'chapters/04/assets')
    for name in ['assets','book','video','social']:shutil.copytree(source/name,previous/name)
    with ZipFile(previous/'Expected_utility.zip','w',ZIP_DEFLATED) as bundle:
        for path in sorted(source.rglob('*')):
            if path.is_file():bundle.write(path,Path('Expected_utility')/path.relative_to(source))
    previous=site/'chapters/07/files';previous.mkdir()
    (site/'chapters/07/assets').mkdir()
    for name in ['two_bowls.svg','room_tone.wav']:
        shutil.copy2(ROOT/'archive/legacy-v01/digital/assets'/name,site/'chapters/07/assets'/name)
    for name in ['book/07_com_nguoi_A5_PROOF.pdf','video/com_nguoi_animatic_v01.mp4']:
        shutil.copy2(ROOT/'archive/legacy-v01'/name,previous/Path(name).name)
    (site/'.nojekyll').touch()
    print('Built',len(published),'chapters, shared archive and preserved release URLs.')

if __name__=='__main__':build_site()
