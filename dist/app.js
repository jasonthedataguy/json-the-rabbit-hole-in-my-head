import { chapters, renderPortal } from './chapters.js?v=4';
import { introduction, parts, chapterNotes } from './book.js?v=4';
import { renderChapterMarker, renderReferenceBowlIcon, getChapterMarkerName } from './markers.js?v=4';
import { PortalRing } from './ring.js?v=4';

const $ = selector => document.querySelector(selector);
const $$ = selector => [...document.querySelectorAll(selector)];
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const roman = ['','I','II','III','IV','V'];
const store = {get(key,fallback){try{return JSON.parse(localStorage.getItem(key)) ?? fallback;}catch{return fallback;}},set(key,value){try{localStorage.setItem(key,JSON.stringify(value));}catch{}}};
const library = await fetch(new URL('./content/manuscripts.json',import.meta.url)).then(response=>{
  if(!response.ok)throw new Error('Không thể tải bản thảo.');return response.json();
});
const publishedById = new Map(library.chapters.filter(c=>c.editorialId!==null).map(c=>[c.editorialId,c]));
const publishedBySlug = new Map(library.chapters.map(c=>[c.slug,c]));
const chapterById = id => chapters.find(c=>c.id===id);
const partById = id => parts.find(part=>part.id===id);
const motionMedia = matchMedia('(prefers-reduced-motion: reduce)');
let reducedMotion = store.get('json-reduced-motion',motionMedia.matches);
let readingSize = store.get('json-reading-size',24);
const positions = store.get('json-book-positions',{});
let currentRoute = null, selectedMapChapter = 0, ring = null, scrollTimer = null;
const drawer = $('#navigation-drawer');
if('scrollRestoration' in history)history.scrollRestoration='manual';

function parseRoute(){
  const hash=decodeURIComponent(location.hash.slice(1));
  const chapter=hash.match(/^chapter\/(\d{2})$/);
  if(chapter&&chapterById(chapter[1]))return {type:'chapter',key:hash,id:chapter[1]};
  const archive=hash.match(/^archive\/([a-z0-9-]+)$/);
  if(archive&&publishedBySlug.has(archive[1]))return {type:'archive-chapter',key:hash,slug:archive[1]};
  if(['contents','map','edition','archive'].includes(hash))return {type:hash,key:hash};
  return {type:'introduction',key:'introduction'};
}
function isCurrent(key){return currentRoute?.key===key;}
const currentAttr = key => isCurrent(key)?' aria-current="page"':'';
const dot = available => available?'<span class="available-dot" aria-label="Có toàn văn"></span>':'';
function navigationHTML(){
  const currentChapter=currentRoute?.type==='chapter'?chapterById(currentRoute.id):null;
  return `<div class="frontmatter-nav"><a class="nav-link" href="#introduction"${currentAttr('introduction')}><span class="nav-number">i</span><span class="nav-title">Dẫn nhập</span></a><a class="nav-link" href="#contents"${currentAttr('contents')}><span class="nav-number">ii</span><span class="nav-title">Mục lục</span></a><a class="nav-link prologue-nav" href="#chapter/00"${currentAttr('chapter/00')}><span class="nav-number">00</span><span class="nav-title"><small>MỞ ĐẦU</small>Cơm nguội</span>${renderReferenceBowlIcon(24)}</a></div><div class="part-navigation-list">${parts.map(part=>`<details class="part-navigation"${currentChapter?.act===part.id?' open':''}><summary><span class="part-roman">${roman[part.id]}</span><span class="part-nav-title">${esc(part.title)}</span></summary><div class="part-chapters">${chapters.filter(chapter=>chapter.act===part.id).map(chapter=>`<a class="chapter-nav-link" href="#chapter/${chapter.id}"${currentAttr(`chapter/${chapter.id}`)}><span class="nav-number">${chapter.id}</span><span class="nav-title">${esc(chapter.title)}</span>${dot(publishedById.has(chapter.id))}</a>`).join('')}</div></details>`).join('')}</div><div class="sidebar-secondary"><a class="nav-link" href="#map"${currentAttr('map')}><span class="nav-symbol" aria-hidden="true">◌</span><span>Bản đồ chương</span></a><a class="nav-link" href="#archive"${currentAttr('archive')}><span class="nav-symbol" aria-hidden="true"><svg width="12" height="14" viewBox="0 0 14 16" fill="none" stroke="currentColor"><path d="M2 2h9v12H2zM4 5h5M4 8h5M4 11h3"/></svg></span><span>Những bản đã công bố</span></a><a class="nav-link" href="#edition"${currentAttr('edition')}><span class="nav-symbol" aria-hidden="true">·</span><span>Về ấn bản</span></a></div>`;
}
function renderNavigation(){$('#desktop-navigation').innerHTML=navigationHTML();$('#mobile-navigation').innerHTML=navigationHTML();}
function tocRow(chapter){return `<a class="toc-row" href="#chapter/${chapter.id}"><span class="toc-number">${chapter.id}</span><span class="toc-title">${esc(chapter.title)}${chapter.id==='31'?'<small class="toc-epilogue">Lời kết</small>':''}</span><span class="toc-leader" aria-hidden="true"></span>${dot(publishedById.has(chapter.id))}</a>`;}
function renderContents(){
  $('#book-table-of-contents').innerHTML=`<div class="toc-frontmatter"><a class="toc-row" href="#introduction"><span class="toc-number">i</span><span class="toc-title">Dẫn nhập</span><span class="toc-leader" aria-hidden="true"></span></a><p class="toc-prologue-label">MỞ ĐẦU</p>${tocRow(chapters[0])}</div>${parts.map(part=>`<section class="toc-part"><header><p class="toc-part-number">PHẦN ${String(part.id).padStart(2,'0')}</p><h2>${esc(part.title)}</h2><p class="toc-part-key">${esc(part.key)}</p></header><div class="toc-chapters">${chapters.filter(chapter=>chapter.act===part.id).map(tocRow).join('')}</div></section>`).join('')}`;
}
function artHTML(chapter){
  if(chapter.id==='00')return '<img class="rice-portal-image" src="assets/rice-portal.png" alt="Một bữa cơm gia đình dưới ánh đèn vàng, nhìn qua vòng giấy có hoa văn xanh trên nền ngà.">';
  if(chapter.id==='04')return '<img src="assets/fashion-portal.png" alt="Căn phòng, chiếc áo cũ, những đôi giày và cửa sổ Paris nằm trong các lớp giấy nhiều màu.">';
  return renderPortal(chapter);
}
function chapterArtwork(chapter){return `<figure class="chapter-illustration" aria-label="Cửa sổ chương ${chapter.id}: ${esc(chapter.title)}"><div class="portal-scene">${artHTML(chapter)}</div><div class="portal-page-marker">${renderChapterMarker(chapter,{compact:true})}</div></figure>`;}
function pageTurn({href,title,label='',direction='next'}){
  const arrow=`<span class="leaf-arrow" aria-hidden="true">${direction==='next'?'→':'←'}</span>`;
  return `<a class="${direction==='next'?'next-leaf':'previous-leaf'}" href="${href}">${direction==='previous'?arrow:''}<span>${label?`<small>${esc(label)}</small>`:''}<strong>${esc(title)}</strong></span>${direction==='next'?arrow:''}</a>`;
}
function chapterFooter(chapter){
  const number=Number(chapter.id);
  const previous=number===0?{href:'#introduction',title:'Dẫn nhập',label:'TRANG TRƯỚC'}:{href:`#chapter/${chapters[number-1].id}`,title:chapters[number-1].title,label:number===1?'MỞ ĐẦU':'CHƯƠNG TRƯỚC'};
  const next=number===31?{href:'#introduction',title:'Trở về trang đầu',label:'KHÉP LẠI'}:{href:`#chapter/${chapters[number+1].id}`,title:chapters[number+1].title,label:'CHƯƠNG TIẾP'};
  return `<footer class="leaf-navigation">${pageTurn({...previous,direction:'previous'})}<span class="folio">${chapter.id}</span>${pageTurn({...next,direction:'next'})}</footer>`;
}
function sourceNotes(manuscript){return `<details class="chapter-archive"><summary>Bản lưu của chương</summary><p>Bản đã công bố: <em>${esc(manuscript.originalTitle)}</em> · ${esc(manuscript.legacyId)}</p><a href="${esc(manuscript.archiveUrl)}" target="_blank" rel="noopener">Đọc bản công bố và xem tư liệu <span aria-hidden="true">↗</span></a><a href="${esc(manuscript.downloadUrl)}" download>Tải bản chữ gốc</a></details>`;}
function renderChapter(id){
  const chapter=chapterById(id),part=partById(chapter.act),manuscript=publishedById.get(id);
  const headingLabel=id==='00'?'MỞ ĐẦU':id==='31'?'LỜI KẾT':`CHƯƠNG ${id}`;
  const sourceTitle=manuscript && manuscript.originalTitle.toLowerCase().replaceAll('_',' ')!==chapter.title.toLowerCase()?`<p class="chapter-source-title">Bản công bố: ${esc(manuscript.originalTitle)}</p>`:'';
  const text=manuscript?`<div class="chapter-prose prose" data-reading-kind="full">${manuscript.bodyHtml || manuscript.html}</div>${sourceNotes(manuscript)}`:`<div class="outline-notice"><span>ĐỀ CƯƠNG</span><p>Toàn văn chương này chưa có trong ấn bản số.</p></div><div class="outline-prose prose" data-reading-kind="outline"><p>${esc(chapterNotes[id].summary)}</p></div><p class="outline-source">Theo đề cương cấu trúc bản thảo.</p>`;
  $('#chapter-leaf').innerHTML=`<header class="chapter-heading"><p class="leaf-kicker">${part?`PHẦN ${roman[part.id]} · ${esc(part.key)}`:'.JSON / JASON, UNDER REVISION'}</p><p class="chapter-numeral">${headingLabel}</p><h1 id="chapter-heading" class="chapter-title" tabindex="-1">${esc(chapter.title)}</h1>${part?`<p class="chapter-part-title">${esc(part.title)}</p>`:''}${sourceTitle}</header>${chapterArtwork(chapter)}${text}${chapterFooter(chapter)}`;
  selectedMapChapter=Number(id);
}
function renderArchive(){
  $('#archive-list').innerHTML=library.chapters.map(manuscript=>`<a class="archive-row" href="#archive/${esc(manuscript.slug)}"><span class="archive-original-number">${esc(manuscript.legacyId)}</span><span><strong>${esc(manuscript.originalTitle)}</strong><small>${manuscript.editorialId!==null?`TRONG CUỐN SÁCH · ${manuscript.editorialId==='00'?'MỞ ĐẦU':`CHƯƠNG ${manuscript.editorialId}`}`:'BÀI VIẾT TRONG BẢN LƯU'}</small></span><span aria-hidden="true">→</span></a>`).join('');
}
function renderArchiveChapter(slug){
  const manuscript=publishedBySlug.get(slug);
  $('#chapter-leaf').innerHTML=`<header class="chapter-heading"><p class="leaf-kicker">BẢN LƯU · BÀI ${esc(manuscript.legacyId)}</p><h1 id="chapter-heading" class="chapter-title" tabindex="-1">${esc(manuscript.originalTitle)}</h1><p class="chapter-part-title">Theo lần công bố trước khi sắp xếp thành cuốn sách.</p></header><div class="chapter-prose prose" data-reading-kind="full">${manuscript.bodyHtml || manuscript.html}</div>${sourceNotes(manuscript)}<footer class="leaf-navigation">${pageTurn({href:'#archive',title:'Những bản đã công bố',direction:'previous'})}<span class="folio">Bản lưu ${esc(manuscript.legacyId)}</span>${manuscript.editorialId!==null?pageTurn({href:`#chapter/${manuscript.editorialId}`,title:'Vị trí trong cuốn sách',label:manuscript.editorialId==='00'?'MỞ ĐẦU':`CHƯƠNG ${manuscript.editorialId}`}):''}</footer>`;
}
function savePosition(){if(currentRoute){positions[currentRoute.key]=Math.round(window.scrollY);store.set('json-book-positions',positions);}}
function breadcrumb(route){
  if(route.type==='chapter'){const chapter=chapterById(route.id);return chapter.act?`Phần ${roman[chapter.act]} / ${chapter.title}`:`Mở đầu / ${chapter.title}`;}
  return ({introduction:'Phần mở đầu / Dẫn nhập',contents:'Mục lục',map:'Bản đồ chương',edition:'Ghi chú ấn bản',archive:'Những bản đã công bố','archive-chapter':'Bản lưu / '+(publishedBySlug.get(route.slug)?.originalTitle || '')})[route.type];
}
function renderRoute(route,{initial=false}={}){
  if(!initial)savePosition();
  currentRoute=route;
  const view=route.type==='archive-chapter'?'chapter':route.type;
  $$('.book-view').forEach(element=>{element.hidden=element.id!==`${view}-view`;});
  if(route.type==='chapter')renderChapter(route.id);
  if(route.type==='archive-chapter')renderArchiveChapter(route.slug);
  if(route.type==='map')selectMapChapter(selectedMapChapter);
  $('#reading-breadcrumb').textContent=breadcrumb(route);
  document.title=route.type==='introduction'?'.json — Jason, under revision':`${route.type==='chapter'?chapterById(route.id).title:route.type==='archive-chapter'?publishedBySlug.get(route.slug).originalTitle:breadcrumb(route)} — .json`;
  document.body.classList.toggle('viewing-map',route.type==='map');
  renderNavigation();
  if(drawer.open)drawer.close();
  requestAnimationFrame(()=>{
    window.scrollTo({top:positions[route.key] || 0,behavior:'instant'});
    const heading=$(`#${view}-view h1`);heading?.focus({preventScroll:true});
    if(route.type==='map')positionOrbit();
  });
  $('#reading-status').textContent=breadcrumb(route);
}
function navigate(key){
  if(drawer.open)drawer.close();
  if(key===currentRoute?.key)return;
  savePosition();
  history.pushState(null,'',`#${key}`);
  renderRoute(parseRoute());
}
function applyReadingSize(){document.documentElement.style.setProperty('--reading-font',`${readingSize}px`);$('#font-down').disabled=readingSize<=18;$('#font-up').disabled=readingSize>=34;}
function applyMotion(){document.body.classList.toggle('reduced-motion',reducedMotion);$('#motion-toggle').setAttribute('aria-pressed',reducedMotion);$('#motion-label').textContent=reducedMotion?'Đang giảm chuyển động':'Giảm chuyển động';}

// The illustrated contents remain an optional navigation page, separate from the prose.
function positionOrbit(rotation=ring?.rotation ?? -selectedMapChapter*11.25){
  const radius=-$('#portal-stage').getBoundingClientRect().width*.475;
  $$('.orbit-mark').forEach((element,index)=>{element.style.setProperty('--angle',`${index*11.25+rotation}deg`);element.style.setProperty('--orbit-radius',`${radius}px`);});
}
function selectMapChapter(index,{fromRing=false}={}){
  selectedMapChapter=((index%32)+32)%32;
  const chapter=chapters[selectedMapChapter],part=partById(chapter.act);
  $('#portal-scene').innerHTML=artHTML(chapter);$('#portal-rim-art').innerHTML=artHTML(chapter);
  $('#portal-marker').innerHTML=renderChapterMarker(chapter);
  $('#portal-marker').setAttribute('aria-label',`Dấu chương ${chapter.id}: ${getChapterMarkerName(chapter)}`);
  $('#portal-stage').setAttribute('aria-label',`${chapter.id}. ${chapter.title}. Kéo vòng để xoay; dùng phím mũi tên để chọn; Enter để đọc.`);
  $('#map-part').textContent=part?`PHẦN ${roman[part.id]} · ${part.title}`:'MỞ ĐẦU';
  $('#map-number').textContent=chapter.id;$('#map-title').textContent=chapter.title;
  $('#map-summary').textContent=chapterNotes[chapter.id].summary;
  $('#map-enter').href=`#chapter/${chapter.id}`;$('#map-enter').innerHTML=`${publishedById.has(chapter.id)?'Đọc chương':'Đọc đề cương'} <span aria-hidden="true">→</span>`;
  $('#map-availability').textContent=publishedById.has(chapter.id)?'TOÀN VĂN':'ĐỀ CƯƠNG';
  $$('.orbit-mark').forEach((element,i)=>{element.classList.toggle('active',i===selectedMapChapter);element.setAttribute('aria-pressed',i===selectedMapChapter);});
  $$('.map-part-button').forEach(element=>{const active=Number(element.dataset.mapPart)===chapter.act;element.classList.toggle('active',active);element.setAttribute('aria-pressed',active);});
  if(!fromRing)ring?.setChapter(selectedMapChapter);
  positionOrbit();
}
$('#orbit-marks').innerHTML=chapters.map((chapter,index)=>`<button class="orbit-mark" data-map-chapter="${index}" aria-label="${chapter.id}. ${esc(chapter.title)}" title="${chapter.id} · ${esc(chapter.title)}"><span>${chapter.id}</span></button>`).join('');
$('#map-parts').innerHTML=parts.map(part=>`<button class="map-part-button" data-map-part="${part.id}"><span>${roman[part.id]}</span><small>${esc(part.title)}</small></button>`).join('');
ring=new PortalRing({stage:$('#portal-stage'),initialIndex:0,onRotate(rotation,{animate}){
  $('#portal-stage').classList.toggle('ring-instant',!animate);$('#portal-stage').dataset.ringRotation=String(rotation);
  $('#portal-rim').style.transform=`rotate(${rotation}deg)`;positionOrbit(rotation);
},onSelect(index){selectMapChapter(index,{fromRing:true});}});
new ResizeObserver(()=>positionOrbit()).observe($('#portal-stage'));
$('#map-prev').addEventListener('click',()=>selectMapChapter(selectedMapChapter-1));
$('#map-next').addEventListener('click',()=>selectMapChapter(selectedMapChapter+1));
$('#portal-stage').addEventListener('keydown',event=>{
  if(event.target.closest('button')&&['Enter',' '].includes(event.key))return;
  const actions={ArrowRight:()=>selectMapChapter(selectedMapChapter+1),ArrowDown:()=>selectMapChapter(selectedMapChapter+1),ArrowLeft:()=>selectMapChapter(selectedMapChapter-1),ArrowUp:()=>selectMapChapter(selectedMapChapter-1),Home:()=>selectMapChapter(0),End:()=>selectMapChapter(31),Enter:()=>navigate(`chapter/${chapters[selectedMapChapter].id}`),' ':()=>navigate(`chapter/${chapters[selectedMapChapter].id}`)};
  if(actions[event.key]){event.preventDefault();actions[event.key]();}
});
$('#motion-toggle').addEventListener('click',()=>{reducedMotion=!reducedMotion;store.set('json-reduced-motion',reducedMotion);applyMotion();});
motionMedia.addEventListener('change',event=>{reducedMotion=event.matches;applyMotion();});
for(const [selector,delta] of [['#font-down',-2],['#font-up',2]])$(selector).addEventListener('click',()=>{readingSize=Math.max(18,Math.min(34,readingSize+delta));store.set('json-reading-size',readingSize);applyReadingSize();});
$('#menu-open').addEventListener('click',()=>drawer.showModal());
$('#menu-close').addEventListener('click',()=>drawer.close());
drawer.addEventListener('click',event=>{if(event.target===drawer){const rect=drawer.getBoundingClientRect();if(event.clientX>rect.right)drawer.close();}});
document.addEventListener('click',event=>{
  if(event.target.closest('.skip-link')){event.preventDefault();$('#book-content').focus();return;}
  const mapChapter=event.target.closest('[data-map-chapter]');if(mapChapter){selectMapChapter(Number(mapChapter.dataset.mapChapter));return;}
  const mapPart=event.target.closest('[data-map-part]');if(mapPart){selectMapChapter(Number(chapters.find(chapter=>chapter.act===Number(mapPart.dataset.mapPart)).id));return;}
  const link=event.target.closest('a[href^="#"]');
  if(link&&!event.metaKey&&!event.ctrlKey&&!event.shiftKey&&!event.altKey){event.preventDefault();navigate(link.getAttribute('href').slice(1));}
});
window.addEventListener('popstate',()=>renderRoute(parseRoute()));
window.addEventListener('hashchange',()=>{const route=parseRoute();if(route.key!==currentRoute?.key)renderRoute(route);});
window.addEventListener('scroll',()=>{clearTimeout(scrollTimer);scrollTimer=setTimeout(savePosition,180);},{passive:true});
window.addEventListener('pagehide',savePosition);
$('#book-epigraph').textContent=introduction.epigraph;
$('#introduction-text').innerHTML=introduction.paragraphs.map(paragraph=>`<p>${esc(paragraph)}</p>`).join('');
renderContents();renderArchive();applyReadingSize();applyMotion();renderRoute(parseRoute(),{initial:true});
