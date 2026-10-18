"""Validate complete chapter products, manuscript preservation and exported links."""
import hashlib
import html
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile
from common import ROOT, artifact_hash, chapters, paragraphs, plain, read_json, safe_path
from build_site import reader_release

class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.links=[];self.ids=set();self.story=[];self.reading=False;self.para=False;self.feed(text)
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, 'Duplicate HTML id: '+attrs['id']
            self.ids.add(attrs['id'])
        for attr in ['href','src','poster','data-image','srcset']:
            if attr in attrs:self.links.append(attrs[attr])
        if tag=='article' and 'prose' in attrs.get('class','').split():self.reading=True
        if tag=='p' and self.reading:self.para=True;self.story.append('')
    def handle_endtag(self,tag):
        if tag=='article':self.reading=False
        if tag=='p':self.para=False
    def handle_data(self,data):
        if self.para:self.story[-1]+=data

def normalize(text):return ' '.join(text.split())

def validate_author_manuscript(folder,meta):
    source=meta['manuscript_source']
    original=safe_path(folder,source['path']).read_bytes()
    assert len(original)==source['bytes'],f'Author original byte count changed: {meta["slug"]}'
    assert hashlib.sha256(original).hexdigest()==source['sha256'],f'Author original changed: {meta["slug"]}'
    expected=original
    if meta['text_policy']=='verbatim-author-body':
        heading,separator,body=original.partition(b'\n')
        assert separator,'Original manuscript needs a heading and body'
        ending=b'\r\n' if heading.endswith(b'\r') else b'\n'
        expected=f'# {meta["number"]}. {meta["title"]}'.encode('utf-8')+ending+body
    assert safe_path(folder,meta['canonical_text']).read_bytes()==expected,f'Published text differs from authorized manuscript: {meta["slug"]}'
    return original

def check_site():
    site=ROOT/'site'
    pages={p.resolve():Page(p.read_text(encoding='utf-8')) for p in site.rglob('*.html')}
    for path,page in pages.items():
        for link in page.links:
            parsed=urlsplit(html.unescape(link))
            if parsed.scheme or parsed.netloc:continue
            assert not parsed.path.startswith('/'),f'Unsafe repository prefix link: {link}'
            target=(path.parent/unquote(parsed.path)).resolve() if parsed.path else path
            assert target.is_relative_to(site.resolve()),f'Link leaves output: {link}'
            if target.is_dir():target/= 'index.html'
            assert target.is_file(),f'Broken link: {path.relative_to(site)} => {link}'
            if parsed.fragment and target in pages:assert unquote(parsed.fragment) in pages[target].ids,f'Broken anchor: {link}'
    urls=set();numbers=set();count=0;reference_count=0
    expected_pages={(site/'index.html').resolve(),(site/'about/index.html').resolve()}
    for folder,meta in chapters():
        assert meta['schema_version']==1
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',meta['slug'])
        assert meta['slug']==folder.name
        assert meta['number'] not in numbers;numbers.add(meta['number'])
        for route in [meta['canonical_path'],*meta['aliases']]:
            assert route not in urls;urls.add(route)
            assert re.fullmatch(r'chapters/[a-z0-9-]+/',route)
        if meta.get('reference_manifest'):
            manifest=read_json(safe_path(folder,meta['reference_manifest']))
            imported=set()
            for item in manifest['files']:
                path=safe_path(folder,item['path'])
                assert path not in imported,f'Duplicate reference path: {path}'
                imported.add(path)
                assert path.is_file(),f'Missing supplied reference: {path}'
                data=path.read_bytes()
                assert len(data)==item['bytes'],f'Reference size changed: {path}'
                assert hashlib.sha256(data).hexdigest()==item['sha256'],f'Supplied reference changed: {path}'
                reference_count+=1
        if not meta['publish']:
            for route in [meta['canonical_path'],*meta['aliases']]:
                assert not (site/route).exists(),f'Draft chapter route was published: {route}'
            continue
        count+=1
        expected_pages.update((site/route/'index.html').resolve() for route in [meta['canonical_path'],*meta['aliases']])
        reader=reader_release(meta)
        if meta.get('text_policy') in {'verbatim-author-original','verbatim-author-body'}:
            original=validate_author_manuscript(folder,meta)
            recording_script=folder/'audio/reading-script.md'
            if recording_script.exists():assert recording_script.read_bytes()==(folder/meta['canonical_text']).read_bytes(),f'Recording script differs from approved manuscript: {meta["slug"]}'
            manuscript=original.decode('utf-8').replace('\r\n','\n')
            if meta['artifact']=='memory':
                for moment in read_json(folder/'production.json')['memory']['moments']:
                    assert moment['quote'] in manuscript,f'Memory excerpt is not in author original: {moment["title"]}'
            if (folder/'production.json').exists():
                recipe=read_json(folder/'production.json')
                if recipe.get('excerpts_verbatim'):
                    excerpts=[item['text'] for item in recipe.get('carousel',[])]
                    excerpts += [item['text'] for item in recipe.get('publish_media',{}).get('carousel',[])]
                    excerpts += [segment['text'] for film in recipe.get('films',[]) for segment in film['segments']]
                    excerpts += [item['text'] for item in recipe.get('supplemental',{}).get('cards',[]) if item.get('verbatim',True)]
                    for excerpt in excerpts:assert excerpt in manuscript,f'Product excerpt is not in author original: {excerpt}'
        expected=[normalize(plain(p)) for p in paragraphs(safe_path(folder,meta['canonical_text']))]
        actual=pages[(site/meta['canonical_path']/'index.html').resolve()].story
        assert [normalize(p) for p in actual]==expected,f'Manuscript changed: {meta["slug"]}'
        assert meta['narration']['file'] is None and meta['narration']['synthetic_voice'] is False
        if not reader:assert meta['video_mode']=='edit cuts awaiting author-recorded narration'
        for item in read_json(folder/'docs/INVENTORY.json'):
            path=safe_path(folder,item['path'])
            assert path.is_file(),path
            assert artifact_hash(path)==item['sha256_normalized_text_lf'],f'Inventory mismatch: {path}'
        for product in read_json(folder/'docs/PRODUCTS.json')['products']:
            assert product['state']!='missing',product
            assert safe_path(folder,product['path']).is_file(),product
            # Registered HTML products (for example a print guide) are deployed
            # alongside the chapter. web/index.html is its offline source page.
            if product['path'].endswith('.html') and product['path']!='web/index.html' and not product['path'].startswith('references/'):
                expected_pages.add(safe_path(site/meta['canonical_path'],product['path']))
        home=pages[(site/'index.html').resolve()]
        assert meta['canonical_path'] in home.links,f'Published chapter missing from homepage: {meta["slug"]}'
        if reader:
            page=(site/meta['canonical_path']/'index.html').read_text(encoding='utf-8')
            assert '<video' not in page and '<audio' not in page,'Reader release advertises unfinished media'
            assert not (site/meta['canonical_path']/'product-set.zip').exists()
            continue
        # Supplied cuts retain their own formats; generated cuts use the shared timeline.
        timeline=folder/'video/timeline.json'
        plans=[] if meta.get('release_stage')=='supplied' and not timeline.exists() else read_json(timeline)
        for plan in plans:
            assert plan['status']=='edit preview awaiting author narration'
            assert abs(plan['segments'][0]['start'])<.001
            for a,b in zip(plan['segments'],plan['segments'][1:]):assert abs(a['end']-b['start'])<.002
            assert abs(plan['duration']-plan['segments'][-1]['end'])<.002
            for seg in plan['segments']:
                assert seg['end']>seg['start']
                assert safe_path(folder,seg['scene']).is_file()
            assert (folder/f'video/{plan["name"]}.mp4').stat().st_size>10000
        with ZipFile(site/meta['canonical_path']/'product-set.zip') as bundle:
            assert bundle.testzip() is None
            for item in read_json(folder/'docs/INVENTORY.json'):
                data=bundle.read(f'chapters/{meta["slug"]}/{item["path"]}')
                source=(folder/item['path']).read_bytes()
                assert data==source,f'ZIP differs: {item["path"]}'
            assert 'shared/site.css' in bundle.namelist() and 'shared/site.js' in bundle.namelist()
            if meta.get('release_stage')=='supplied':
                for item in read_json(folder/meta['reference_manifest'])['files']:
                    data=bundle.read(f'chapters/{meta["slug"]}/{item["path"]}')
                    assert hashlib.sha256(data).hexdigest()==item['sha256'],f'ZIP reference changed: {item["path"]}'
    migration=read_json(ROOT/'docs/MIGRATION.json')
    for item in migration['files']:
        assert hashlib.sha256((ROOT/item['to']).read_bytes()).hexdigest()==item['sha256'],f'Archived file changed: {item["to"]}'
    assert set(pages)==expected_pages, f'Unexpected or missing public pages: {set(pages)^expected_pages}'
    print(f'PASS: {count} published chapters; {len(pages)} pages; homepage cards, links, manuscripts, inventories, available products, {reference_count} supplied references and {len(migration["files"])} archived files; draft routes excluded')

if __name__=='__main__':check_site()
