import html
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def chapters(selected=None):
    registry=read_json(ROOT/'book.json')
    for slug in registry['chapters']:
        if selected and slug!=selected:
            continue
        folder=ROOT/'chapters'/slug
        yield folder, read_json(folder/'chapter.json')

def paragraphs(path):
    return Path(path).read_text(encoding='utf-8').strip().split('\n\n')[1:]

def plain(text):
    return re.sub(r'[`*]','',text)

def inline(text):
    text=html.escape(text)
    text=re.sub(r'`([^`]+)`',r'<code>\1</code>',text)
    return re.sub(r'\*([^*]+)\*',r'<em>\1</em>',text)

def safe_path(base, relative):
    result=(base/relative).resolve()
    if not result.is_relative_to(base.resolve()):
        raise ValueError(f'Path leaves chapter: {relative}')
    return result

def artifact_hash(path):
    data=path.read_bytes()
    if path.suffix.lower() in {'.md','.html','.json','.srt','.vtt','.log','.css','.js','.txt','.svg'}:
        data=data.replace(b'\r\n',b'\n')
    return hashlib.sha256(data).hexdigest()
