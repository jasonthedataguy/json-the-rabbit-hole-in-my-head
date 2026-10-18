import { chapters, renderIcon, renderPortal, renderPortalScene } from './chapters.js?v=15';
import { introduction, parts, chapterNotes } from './book.js?v=13';
import { renderChapterMarker, getChapterMarkerName } from './markers.js?v=11';
import { PortalRing } from './ring.js?v=10';
import { renderPortalPicture, renderPortalFrame, renderFramedPortal } from './portal-art.js?v=32';

const $ = selector => document.querySelector(selector);
const $$ = selector => [...document.querySelectorAll(selector)];
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const introInline = value => esc(value).replace(/\*([^*]+)\*/g,'<em>$1</em>');
const roman = ['','I','II','III','IV','V'];
const store = {get(key,fallback){try{return JSON.parse(localStorage.getItem(key)) ?? fallback;}catch{return fallback;}},set(key,value){try{localStorage.setItem(key,JSON.stringify(value));}catch{}}};
const library = await fetch(new URL('./content/manuscripts.json?v=11',import.meta.url)).then(response=>{
  if(!response.ok)throw new Error('Unable to load the manuscript.');return response.json();
});
const publishedById = new Map(library.chapters.filter(c=>c.editorialId!==null).map(c=>[c.editorialId,c]));
const publishedBySlug = new Map(library.chapters.map(c=>[c.slug,c]));
const chapterById = id => chapters.find(c=>c.id===id);
const partById = id => parts.find(part=>part.id===id);
const partLabel = part => `${part.key} | ${part.title}`;
const motionMedia = matchMedia('(prefers-reduced-motion: reduce)');
let reducedMotion = store.get('json-reduced-motion',motionMedia.matches);
let readingSize = store.get('json-reading-size',22);
const positions = store.get('json-book-positions',{});
let currentRoute = null, selectedMapChapter = 0, selectedCoverPage = 0, ring = null, coverRing = null, scrollTimer = null;
const drawer = $('#navigation-drawer');
if('scrollRestoration' in history)history.scrollRestoration='manual';

function parseRoute(){
  const hash=decodeURIComponent(location.hash.slice(1));
  const chapter=hash.match(/^chapter\/(\d{2})$/);
  if(chapter&&chapterById(chapter[1]))return {type:'chapter',key:hash,id:chapter[1]};
  const archive=hash.match(/^archive\/([a-z0-9-]+)$/);
  if(archive){const editorialId=publishedBySlug.get(archive[1])?.editorialId;if(editorialId!==null&&editorialId!==undefined){history.replaceState(null,'',`#chapter/${editorialId}`);return {type:'chapter',key:`chapter/${editorialId}`,id:editorialId};}}
  if(archive&&publishedBySlug.get(archive[1])?.legacyId!=null)return {type:'archive-chapter',key:hash,slug:archive[1]};
  if(['cover','introduction','contents','map','edition','archive'].includes(hash))return {type:hash,key:hash};
  return {type:'cover',key:'cover'};
}
function isCurrent(key){return currentRoute?.key===key;}
const currentAttr = key => isCurrent(key)?' aria-current="page"':'';
const dot = available => available?'<span class="available-dot" aria-label="Full text available"></span>':'';
function chapterNavIcon(chapter){return `<span class="nav-chapter-icon">${renderIcon(chapter,18)}</span>`;}
function navigationHTML(){
  const currentChapter=currentRoute?.type==='chapter'?chapterById(currentRoute.id):null;
  return `<div class="frontmatter-nav"><a class="nav-link" href="#cover"${currentAttr('cover')}><span class="nav-symbol" aria-hidden="true">▯</span><span>Book cover</span></a><a class="nav-link" href="#map"${currentAttr('map')}><span class="nav-symbol" aria-hidden="true">◌</span><span>Chapter map</span></a><a class="nav-link" href="#introduction"${currentAttr('introduction')}><span class="nav-number">i</span><span class="nav-title">Introduction</span></a><a class="nav-link" href="#contents"${currentAttr('contents')}><span class="nav-number">ii</span><span class="nav-title">Contents</span></a><a class="nav-link prologue-nav" href="#chapter/00"${currentAttr('chapter/00')}>${chapterNavIcon(chapters[0])}<span class="nav-number">00</span><span class="nav-title"><small>PROLOGUE</small>Cold Rice</span>${dot(publishedById.has('00'))}</a></div><div class="part-navigation-list">${parts.map(part=>`<details class="part-navigation"${currentChapter?.act===part.id?' open':''}><summary><span class="part-roman">${roman[part.id]}</span><span class="part-nav-title">${esc(partLabel(part))}</span></summary><div class="part-chapters">${chapters.filter(chapter=>chapter.act===part.id).map(chapter=>`<a class="chapter-nav-link" href="#chapter/${chapter.id}"${currentAttr(`chapter/${chapter.id}`)}>${chapterNavIcon(chapter)}<span class="nav-number">${chapter.id}</span><span class="nav-title">${esc(chapter.title)}</span>${dot(publishedById.has(chapter.id))}</a>`).join('')}</div></details>`).join('')}</div><div class="sidebar-secondary"><a class="nav-link" href="#archive"${currentAttr('archive')}><span class="nav-symbol" aria-hidden="true"><svg width="12" height="14" viewBox="0 0 14 16" fill="none" stroke="currentColor"><path d="M2 2h9v12H2zM4 5h5M4 8h5M4 11h3"/></svg></span><span>Published essays</span></a><a class="nav-link" href="#edition"${currentAttr('edition')}><span class="nav-symbol" aria-hidden="true">·</span><span>About this edition</span></a></div>`;
}
function renderNavigation(){$('#desktop-navigation').innerHTML=navigationHTML();$('#mobile-navigation').innerHTML=navigationHTML();}
function tocRow(chapter){return `<a class="toc-row" href="#chapter/${chapter.id}"><span class="toc-number">${chapter.id}</span><span class="toc-title">${esc(chapter.title)}${chapter.slug==='loi-xin-loi'?'<small class="toc-epilogue">Epilogue</small>':''}</span><span class="toc-leader" aria-hidden="true"></span>${dot(publishedById.has(chapter.id))}</a>`;}
function renderContents(){
  $('#book-table-of-contents').innerHTML=`<div class="toc-frontmatter"><a class="toc-row" href="#introduction"><span class="toc-number">i</span><span class="toc-title">Introduction</span><span class="toc-leader" aria-hidden="true"></span></a><p class="toc-prologue-label">PROLOGUE</p>${tocRow(chapters[0])}</div>${parts.map(part=>`<section class="toc-part"><header><p class="toc-part-number">PART ${String(part.id).padStart(2,'0')}</p><h2>${esc(partLabel(part))}</h2></header><div class="toc-chapters">${chapters.filter(chapter=>chapter.act===part.id).map(tocRow).join('')}</div></section>`).join('')}`;
}
function artHTML(chapter){
  if(chapter.id==='00')return renderFramedPortal('rice','rice-chapter','assets/rice-ring-board-v2.png');
  if(chapter.id==='01')return renderFramedPortal('quant','quant-chapter','assets/quant-ring.png');
  if(chapter.id==='02')return renderFramedPortal('expectedUtility','expected-utility-chapter','assets/expected-utility-ring-v2.png');
  if(chapter.id==='03')return renderFramedPortal('playToWin','play-to-win-chapter','assets/play-to-win-ring-v2.png');
  if(chapter.id==='04')return renderFramedPortal('fashion','fashion-chapter','assets/fashion-ring-v2.png');
  if(chapter.id==='08')return renderFramedPortal('motherRussia','mother-russia-chapter','assets/mother-russia-ring-v2.png');
  if(chapter.id==='17')return renderFramedPortal('threeMeeting','three-meeting-chapter','assets/three-meeting-ring-v2.png');
  return renderPortal(chapter);
}
function chapterArtwork(chapter){return `<figure class="chapter-illustration" aria-label="Chapter portal ${chapter.id}: ${esc(chapter.title)}"><div class="portal-scene">${artHTML(chapter)}</div><div class="portal-page-marker">${renderChapterMarker(chapter,{compact:true})}</div></figure>`;}
function pageTurn({href,title,label='',direction='next'}){
  const arrow=`<span class="leaf-arrow" aria-hidden="true">${direction==='next'?'→':'←'}</span>`;
  return `<a class="${direction==='next'?'next-leaf':'previous-leaf'}" href="${href}">${direction==='previous'?arrow:''}<span>${label?`<small>${esc(label)}</small>`:''}<strong>${esc(title)}</strong></span>${direction==='next'?arrow:''}</a>`;
}
function chapterFooter(chapter){
  const number=Number(chapter.id);
  const previous=number===0?{href:'#introduction',title:'Introduction',label:'PREVIOUS PAGE'}:{href:`#chapter/${chapters[number-1].id}`,title:chapters[number-1].title,label:number===1?'PROLOGUE':'PREVIOUS CHAPTER'};
  const next=number===chapters.length-1?{href:'#cover',title:'Book cover',label:'CLOSE THE BOOK'}:{href:`#chapter/${chapters[number+1].id}`,title:chapters[number+1].title,label:'NEXT CHAPTER'};
  return `<footer class="leaf-navigation">${pageTurn({...previous,direction:'previous'})}<span class="folio">${chapter.id}</span>${pageTurn({...next,direction:'next'})}</footer>`;
}
function sourceNotes(manuscript){
  const original=manuscript.legacyId!=null;
  const origin=original?`<p>Originally published as: <em>${esc(manuscript.originalTitle)}</em> · ${esc(manuscript.legacyId)}</p>`:'<p>New chapter in this edition.</p>';
  return `<details class="chapter-archive"><summary>Chapter sources and experiences</summary>${origin}${manuscript.experienceUrl?`<a href="${esc(manuscript.experienceUrl)}">Explore the immersive chapter</a>`:''}${manuscript.printUrl?`<a href="${esc(manuscript.printUrl)}">Original edition print proof</a>`:''}${manuscript.filmUrl?`<a href="${esc(manuscript.filmUrl)}">Watch the original film edit</a>`:''}${manuscript.archiveUrl?`<a href="${esc(manuscript.archiveUrl)}" target="_blank" rel="noopener">Read the original edition and sources <span aria-hidden="true">↗</span></a>`:''}<a href="${esc(manuscript.downloadUrl)}" download>Download the ${original?'original':'selected'} manuscript</a></details>`;
}
function renderChapter(id){
  const chapter=chapterById(id),part=partById(chapter.act),manuscript=publishedById.get(id);
  const headingLabel=id==='00'?'PROLOGUE':chapter.slug==='loi-xin-loi'?'EPILOGUE':`CHAPTER ${id}`;
  const sourceTitle=manuscript && manuscript.originalTitle.toLowerCase().replaceAll('_',' ')!==chapter.title.toLowerCase()?`<p class="chapter-source-title">Original title: ${esc(manuscript.originalTitle)}</p>`:'';
  const text=manuscript?`<div class="chapter-prose prose" lang="vi" data-chapter="${id}" data-reading-kind="full">${manuscript.bodyHtml || manuscript.html}</div>${sourceNotes(manuscript)}`:`<div class="outline-notice"><span>OUTLINE</span><p>The full text is not yet available in this edition.</p></div><div class="outline-prose prose" lang="vi" data-reading-kind="outline"><p>${esc(chapterNotes[id].summary)}</p></div><p class="outline-source">From the manuscript outline.</p>`;
  const opening=id==='17'
    ?`<header class="meeting-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="meeting-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.title)}</h1><p class="meeting-chapter-subtitle">Destiny / Timing / Reunion / Romance</p><p class="meeting-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="meeting-chapter-stage">${chapterArtwork(chapter)}<div class="meeting-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Some people return like destiny.</p><button type="button" id="meeting-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="meeting-spread-banner"><img src="assets/three-meeting-spread-v2.webp" width="1600" height="600" alt="Two people meet near a flower-lined cafe, with a bridge and city skyline beyond."><figcaption>A crowd / A glance / Another time</figcaption></figure>`
    :id==='08'
    ?`<header class="russia-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} · CHAPTER ${id}</p><p class="russia-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.title)}</h1><p class="russia-chapter-subtitle">Memory / Nostalgia / War / Dream</p><p class="russia-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="russia-chapter-stage">${chapterArtwork(chapter)}<div class="russia-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Some homelands are inherited through stories.</p><button type="button" id="russia-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="russia-cabin-banner"><img src="assets/mother-russia-cabin-v2.webp" width="240" height="150" alt="A wooden cabin glows beside the water amid snowy pines beneath a winter moon."><figcaption>Memory / Nostalgia / War / Dream</figcaption></figure>`
    :id==='00'
    ?`<header class="rice-chapter-heading"><p class="leaf-kicker">PROLOGUE · ${id}</p><p class="rice-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.title)}</h1><p class="rice-chapter-subtitle">Memory / Family / Childhood / Home</p>${sourceTitle}</header><div class="rice-chapter-stage">${chapterArtwork(chapter)}<div class="rice-chapter-note"><span>A VISUAL INTRODUCTION</span><p>A bowl of cold rice, a warm home, and the people who made ordinary nights feel like everything.</p><button type="button" id="rice-read">Read the prologue <span aria-hidden="true">↓</span></button></div></div><figure class="rice-room-banner"><img src="assets/rice-family-room-v2.webp?v=2" alt="A family shares dinner in a warm room overlooking the city."><figcaption>Memory / Family / Childhood / Home</figcaption></figure>`
    :id==='02'
    ?`<header class="utility-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} · CHAPTER ${id}</p><p class="utility-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.shortTitle)}</h1><p class="utility-chapter-subtitle">Decision / Probability / Emotion</p><p class="utility-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="utility-chapter-stage">${chapterArtwork(chapter)}<div class="utility-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Different outcomes.<br>Same uncertainty.<br>Still you.</p><button type="button" id="utility-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="utility-desk-banner"><img src="assets/expected-utility-desk-v2.webp" alt="A desk with a laptop displaying a woman's eyes, code, coffee and notes."><figcaption>Decision / Probability / Emotion</figcaption></figure>`
    :id==='03'
    ?`<header class="play-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} · CHAPTER ${id}</p><p class="play-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.title)}</h1><p class="play-chapter-subtitle">Game Theory / Decision / Relationship / Trade-off</p><p class="play-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="play-chapter-stage">${chapterArtwork(chapter)}<div class="play-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Different players.<br>Different incentives.<br>Same game.<br>Choose well.</p><button type="button" id="play-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="play-table-banner"><img src="assets/play-to-win-table-v2.webp" alt="Cards, poker chips and mahjong tiles on a lamplit game table."><figcaption>Different players. Different incentives.</figcaption></figure>`
    :id==='04'
    ?`<header class="fashion-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} · CHAPTER ${id}</p><p class="fashion-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.shortTitle)}</h1><p class="fashion-chapter-subtitle">Be Your Own Label</p><p class="fashion-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="fashion-chapter-stage">${chapterArtwork(chapter)}<div class="fashion-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Street corners, shoeboxes, hand-me-downs, and new dreams.</p><button type="button" id="fashion-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="fashion-room-banner"><img src="assets/fashion-room-v2.webp" alt="A sunset-lit room filled with a sneaker, shoeboxes, hanging clothes, photographs and plants."><figcaption>Same objects. Different worlds.</figcaption></figure>`
    :`<header class="chapter-heading"><p class="leaf-kicker">${part?`PART ${roman[part.id]}`:'.JSON / JASON, UNDER REVISION'}</p><p class="chapter-numeral">${headingLabel}</p><h1 id="chapter-heading" class="chapter-title" tabindex="-1">${esc(chapter.title)}</h1>${part?`<p class="chapter-part-title">${esc(partLabel(part))}</p>`:''}${sourceTitle}</header>${chapterArtwork(chapter)}`;
  const quantSpread=id==='01'?`<figure class="quant-reading-spread"><img src="assets/quant-reading-spread-v2.webp" width="540" height="265" alt="Jason studies charts at his desk with a dog beside him and a note about minimizing loss."><figcaption>Same objective. Same potential. Different risk budget.</figcaption></figure>`:'';
  $('#chapter-leaf').innerHTML=`${opening}${quantSpread}${id==='17'?`<div id="meeting-chapter-text">${text}</div>`:id==='08'?`<div id="russia-chapter-text">${text}</div>`:id==='00'?`<div id="rice-chapter-text">${text}</div>`:id==='02'?`<div id="utility-chapter-text">${text}</div>`:id==='03'?`<div id="play-chapter-text">${text}</div>`:id==='04'?`<div id="fashion-chapter-text">${text}</div>`:text}${chapterFooter(chapter)}`;
  if(id==='17')$('#meeting-read').addEventListener('click',()=>$('#meeting-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='08')$('#russia-read').addEventListener('click',()=>$('#russia-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='00')$('#rice-read').addEventListener('click',()=>$('#rice-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='02')$('#utility-read').addEventListener('click',()=>$('#utility-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='03')$('#play-read').addEventListener('click',()=>$('#play-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='04')$('#fashion-read').addEventListener('click',()=>$('#fashion-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  selectedMapChapter=Number(id);
}
function renderArchive(){
  $('#archive-list').innerHTML=library.chapters.filter(manuscript=>manuscript.legacyId!=null).map(manuscript=>`<a class="archive-row" href="${manuscript.editorialId!==null?`#chapter/${manuscript.editorialId}`:`#archive/${esc(manuscript.slug)}`}"><span class="archive-original-number">${esc(manuscript.legacyId)}</span><span><strong>${esc(manuscript.title)}</strong><small>${manuscript.editorialId!==null?`IN THIS BOOK · ${manuscript.editorialId==='00'?'PROLOGUE':`CHAPTER ${manuscript.editorialId}`}`:'ARCHIVED ESSAY'}</small></span><span aria-hidden="true">→</span></a>`).join('');
}
function renderArchiveChapter(slug){
  const manuscript=publishedBySlug.get(slug);
  const previous={href:'#archive',title:'Published essays',direction:'previous'};
  const next=manuscript.editorialId!==null?{href:`#chapter/${manuscript.editorialId}`,title:'Read in book order',label:manuscript.editorialId==='00'?'PROLOGUE':`CHAPTER ${manuscript.editorialId}`}:null;
  $('#chapter-leaf').innerHTML=`<header class="chapter-heading"><p class="leaf-kicker">ARCHIVE · ESSAY ${esc(manuscript.legacyId)}</p><h1 id="chapter-heading" class="chapter-title" tabindex="-1">${esc(manuscript.title)}</h1><p class="chapter-part-title">From the original publication, before the book was arranged.</p></header><div class="chapter-prose prose" lang="vi" data-reading-kind="full">${manuscript.bodyHtml || manuscript.html}</div>${sourceNotes(manuscript)}<footer class="leaf-navigation">${pageTurn(previous)}<span class="folio">Archive ${esc(manuscript.legacyId)}</span>${next?pageTurn(next):''}</footer>`;
}
function savePosition(){if(currentRoute){positions[currentRoute.key]=Math.round(window.scrollY);store.set('json-book-positions',positions);}}
function breadcrumb(route){
  if(route.type==='chapter'){const chapter=chapterById(route.id);return chapter.act?`Part ${roman[chapter.act]} / ${chapter.title}`:`Prologue / ${chapter.title}`;}
  return ({cover:'Book cover',introduction:'Front matter / Introduction',contents:'Contents',map:'Chapter map',edition:'Edition notes',archive:'Published essays','archive-chapter':'Archive / '+(publishedBySlug.get(route.slug)?.title || '')})[route.type];
}
function renderRoute(route,{initial=false}={}){
  if(!initial)savePosition();
  currentRoute=route;
  const view=route.type==='archive-chapter'?'chapter':route.type;
  $$('.book-view').forEach(element=>{element.hidden=element.id!==`${view}-view`;});
  if(route.type==='chapter')renderChapter(route.id);
  if(route.type==='archive-chapter')renderArchiveChapter(route.slug);
  if(route.type==='map')selectMapChapter(selectedMapChapter);
  if(route.type==='cover')selectCoverPage(0);
  $('#reading-breadcrumb').textContent=breadcrumb(route);
  document.title=['cover','introduction'].includes(route.type)?'.json — Jason, under revision':`${route.type==='chapter'?chapterById(route.id).title:route.type==='archive-chapter'?publishedBySlug.get(route.slug).title:breadcrumb(route)} — .json`;
  document.body.classList.toggle('viewing-map',route.type==='map');
  document.body.classList.toggle('viewing-cover',route.type==='cover');
  renderNavigation();
  if(drawer.open)drawer.close();
  requestAnimationFrame(()=>{
    window.scrollTo({top:positions[route.key] || 0,behavior:'instant'});
    const heading=$(`#${view}-view h1`);heading?.focus({preventScroll:true});
    if(route.type==='map')positionOrbit();
    if(route.type==='cover')positionCoverOrbit();
  });
  $('#reading-status').textContent=breadcrumb(route);
}
function navigate(key){
  if(drawer.open)drawer.close();
  if(key===currentRoute?.key){if(key==='cover')selectCoverPage(0);return;}
  savePosition();
  history.pushState(null,'',`#${key}`);
  renderRoute(parseRoute());
}
function applyReadingSize(){document.documentElement.style.setProperty('--reading-font',`${readingSize}px`);$('#font-down').disabled=readingSize<=18;$('#font-up').disabled=readingSize>=34;}
function applyMotion(){document.body.classList.toggle('reduced-motion',reducedMotion);$('#motion-toggle').setAttribute('aria-pressed',reducedMotion);$('#motion-label').textContent=reducedMotion?'Reduced motion on':'Reduce motion';}

// The illustrated contents remain an optional navigation page, separate from the prose.
function positionOrbit(rotation=ring?.rotation ?? -selectedMapChapter*(360/chapters.length)){
  const radius=-$('#portal-stage').getBoundingClientRect().width*.475;
  $$('.orbit-mark').forEach((element,index)=>{element.style.setProperty('--angle',`${index*(360/chapters.length)+rotation}deg`);element.style.setProperty('--orbit-radius',`${radius}px`);});
}
function selectMapChapter(index,{fromRing=false}={}){
  selectedMapChapter=((index%chapters.length)+chapters.length)%chapters.length;
  const chapter=chapters[selectedMapChapter],part=partById(chapter.act);
  $('#map-view').dataset.chapter=chapter.slug;
  const fittedRing={'00':'assets/rice-ring-board-v2.png','01':'assets/quant-ring.png','02':'assets/expected-utility-ring-v2.png','03':'assets/play-to-win-ring-v2.png','04':'assets/fashion-ring-v2.png','08':'assets/mother-russia-ring-v2.png','17':'assets/three-meeting-ring-v2.png'}[chapter.id];
  const fitted=Boolean(fittedRing);
  const pictureKey=chapter.id==='01'?'quant':chapter.id==='02'?'expectedUtility':chapter.id==='03'?'playToWin':chapter.id==='04'?'fashion':chapter.id==='08'?'motherRussia':chapter.id==='17'?'threeMeeting':'rice';
  $('#portal-art').classList.toggle('uses-fitted-picture',fitted);
  $('#portal-scene').innerHTML=fitted?renderPortalPicture(pictureKey):artHTML(chapter);
  $('#portal-rim-art').innerHTML=fitted?renderPortalFrame(`${pictureKey}-map`,fittedRing):artHTML(chapter);
  $('#portal-marker').innerHTML=renderChapterMarker(chapter);
  $('#portal-marker').setAttribute('aria-label',`Chapter marker ${chapter.id}: ${getChapterMarkerName(chapter)}`);
  $('#portal-stage').setAttribute('aria-label',`${chapter.id}. ${chapter.title}. Drag to rotate; use arrow keys to choose; Enter to read.`);
  $('#map-part').textContent=part?`PART ${roman[part.id]} · ${partLabel(part)}`:'PROLOGUE';
  $('#map-number').textContent=chapter.id;$('#map-title').textContent=['02','03','04'].includes(chapter.id)?chapter.shortTitle:chapter.title;
  $('#map-summary').textContent=chapterNotes[chapter.id].summary;
  $('#map-enter').href=`#chapter/${chapter.id}`;$('#map-enter').innerHTML=`${publishedById.has(chapter.id)?'Read chapter':'Read outline'} <span aria-hidden="true">→</span>`;
  $('#map-availability').textContent=publishedById.has(chapter.id)?'FULL TEXT':'OUTLINE';
  $$('.orbit-mark').forEach((element,i)=>{element.classList.toggle('active',i===selectedMapChapter);element.setAttribute('aria-pressed',i===selectedMapChapter);});
  $$('.map-part-button').forEach(element=>{const active=Number(element.dataset.mapPart)===chapter.act;element.classList.toggle('active',active);element.setAttribute('aria-pressed',active);});
  if(!fromRing)ring?.setChapter(selectedMapChapter);
  orientMapArtwork(ring?.rotation ?? 0,Boolean(ring?.drag?.moved));
  positionOrbit();
}
function orientMapArtwork(rotation,dragging){
  // The figures turn together while dragging, then the authored Chapter 17
  // composition faces upright again at the selected stop.
  const base=dragging?(ring?.drag?.startRotation ?? rotation):rotation;
  $('#portal-rim-art').style.transform=chapters[selectedMapChapter].id==='17'?`rotate(${-base}deg)`:'';
}
$('#orbit-marks').innerHTML=chapters.map((chapter,index)=>`<button class="orbit-mark" data-map-chapter="${index}" aria-label="${chapter.id}. ${esc(chapter.title)}" title="${chapter.id} · ${esc(chapter.title)}"><span>${chapter.id}</span></button>`).join('');
$('#map-parts').innerHTML=parts.map(part=>`<button class="map-part-button" data-map-part="${part.id}"><span>${roman[part.id]}</span><small>${esc(partLabel(part))}</small></button>`).join('');
ring=new PortalRing({stage:$('#portal-stage'),count:chapters.length,initialIndex:0,onRotate(rotation,{animate,dragging}){
  $('#portal-stage').classList.toggle('ring-instant',!animate);$('#portal-stage').dataset.ringRotation=String(rotation);
  $('#portal-rim').style.transform=`rotate(${rotation}deg)`;orientMapArtwork(rotation,dragging);positionOrbit(rotation);
},onSelect(index){selectMapChapter(index,{fromRing:true});}});
new ResizeObserver(()=>positionOrbit()).observe($('#portal-stage'));
$('#map-prev').addEventListener('click',()=>selectMapChapter(selectedMapChapter-1));
$('#map-next').addEventListener('click',()=>selectMapChapter(selectedMapChapter+1));
$('#portal-stage').addEventListener('keydown',event=>{
  if(event.target.closest('button')&&['Enter',' '].includes(event.key))return;
  const actions={ArrowRight:()=>selectMapChapter(selectedMapChapter+1),ArrowDown:()=>selectMapChapter(selectedMapChapter+1),ArrowLeft:()=>selectMapChapter(selectedMapChapter-1),ArrowUp:()=>selectMapChapter(selectedMapChapter-1),Home:()=>selectMapChapter(0),End:()=>selectMapChapter(chapters.length-1),Enter:()=>navigate(`chapter/${chapters[selectedMapChapter].id}`),' ':()=>navigate(`chapter/${chapters[selectedMapChapter].id}`)};
  if(actions[event.key]){event.preventDefault();actions[event.key]();}
});

// Front matter and chapter stops follow the same order as a physical book.
const coverPages = [
  {kind:'cover', label:'Cover', title:'.json — Jason, under revision', href:'#introduction'},
  {kind:'introduction', label:'i', title:introduction.title, href:'#introduction'},
  ...chapters.map(chapter=>({kind:'chapter', label:chapter.id, title:chapter.title, href:`#chapter/${chapter.id}`, chapter}))
];
const coverStep = 360 / coverPages.length;
let renderedCoverPage = -1;
function renderCoverReadingPage(page){
  if(renderedCoverPage===selectedCoverPage)return;
  renderedCoverPage=selectedCoverPage;
  const content=$('#cover-reading-content');
  if(page.kind==='cover'){
    content.innerHTML=`<div class="cover-reader-cover"><p class="cover-reader-kicker">THE BOOK</p><h2>.json</h2><p class="cover-reader-subtitle">Jason, under revision</p><span class="cover-reader-rule" aria-hidden="true"></span><blockquote>${introduction.epigraph.split(/(?<=answer\.)\s+/).map(line=>`<p>${esc(line)}</p>`).join('')}</blockquote><p class="cover-reader-hint">Turn the ring to see each page here.</p></div>`;
  }else if(page.kind==='introduction'){
    content.innerHTML=`<div class="cover-reader-page introduction-reader-page"><p class="cover-reader-kicker">FRONT MATTER · i</p><h2>${esc(introduction.title)}</h2><figure class="cover-reader-illustration"><img src="assets/introduction-reading-spread-v2.webp" width="420" height="280" alt="An open book frames a reader looking toward a moonlit city and bridge."><figcaption>All my selves lead here.</figcaption></figure><div class="cover-reader-prose prose" lang="vi">${introduction.sections.map(section=>`<section><h3>${esc(section.heading)}</h3>${section.paragraphs.map(paragraph=>`<p>${introInline(paragraph)}</p>`).join('')}</section>`).join('')}</div></div>`;
  }else{
    const chapter=page.chapter,part=partById(chapter.act),manuscript=publishedById.get(chapter.id);
    const numberLabel=chapter.id==='00'?'PROLOGUE':chapter.slug==='loi-xin-loi'?'EPILOGUE':`CHAPTER ${chapter.id}`;
    const body=manuscript?`<div class="cover-reader-prose prose" lang="vi">${manuscript.bodyHtml || manuscript.html}</div>${sourceNotes(manuscript)}`:`<div class="cover-reader-outline"><span>OUTLINE</span><p>${esc(chapterNotes[chapter.id].summary)}</p><small>The full manuscript is not yet available in this edition.</small></div>`;
    content.innerHTML=chapter.id==='17'
      ?`<div class="cover-reader-page meeting-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="meeting-reader-number">${chapter.id}</span><h2>${esc(chapter.title)}</h2><p class="meeting-reader-subtitle">Destiny / Timing / Reunion / Romance</p><figure class="meeting-reader-scene"><img src="assets/three-meeting-spread-v2.webp" width="1600" height="600" alt="Two people meet near a flower-lined cafe, with a bridge and city skyline beyond."><figcaption>Some people return like destiny.</figcaption></figure>${body}</div>`
      :chapter.id==='08'
      ?`<div class="cover-reader-page russia-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} · CHAPTER ${chapter.id}</p><span class="russia-reader-number">${chapter.id}</span><h2>${esc(chapter.title)}</h2><p class="russia-reader-subtitle">Memory / Nostalgia / War / Dream</p><figure class="russia-reader-scene"><img src="assets/mother-russia-cabin-v2.webp" width="240" height="150" alt="A wooden cabin glows beside the water amid snowy pines beneath a winter moon."><figcaption>Some homelands are inherited through stories.</figcaption></figure>${body}</div>`
      :chapter.id==='01'
      ?`<div class="cover-reader-page quant-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} · CHAPTER ${chapter.id}</p><h2>${esc(chapter.title)}</h2><p class="cover-reader-part">${esc(partLabel(part))}</p><figure class="cover-reader-illustration"><img src="assets/quant-reading-spread-v2.webp" width="540" height="265" alt="Jason studies charts at his desk with a dog beside him and a note about minimizing loss."><figcaption>Same objective. Same potential. Different risk budget.</figcaption></figure>${body}</div>`
      :chapter.id==='00'
      ?`<div class="cover-reader-page rice-reader-page"><p class="cover-reader-kicker">PROLOGUE · ${chapter.id}</p><span class="rice-reader-number">${chapter.id}</span><h2>${esc(chapter.title)}</h2><p class="rice-reader-subtitle">Memory / Family / Childhood / Home</p><figure class="rice-reader-scene"><img src="assets/rice-family-room-v2.webp?v=2" alt="A family shares dinner in a warm room overlooking the city."><figcaption>The same table. The same bowl. A thousand versions of home.</figcaption></figure>${body}</div>`
      :chapter.id==='02'
      ?`<div class="cover-reader-page utility-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} · CHAPTER ${chapter.id}</p><span class="utility-reader-number">${chapter.id}</span><h2>${esc(chapter.shortTitle)}</h2><p class="utility-reader-subtitle">Decision / Probability / Emotion</p><figure class="utility-reader-scene"><img src="assets/expected-utility-desk-v2.webp" alt="Code and a woman's eyes fill a laptop on a late-night desk."><figcaption>Different outcomes. Same uncertainty. Still you.</figcaption></figure>${body}</div>`
      :chapter.id==='03'
      ?`<div class="cover-reader-page play-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} · CHAPTER ${chapter.id}</p><span class="play-reader-number">${chapter.id}</span><h2>${esc(chapter.title)}</h2><p class="play-reader-subtitle">Game Theory / Decision / Relationship / Trade-off</p><figure class="play-reader-scene"><img src="assets/play-to-win-table-v2.webp" alt="A warm lamp above cards, chips and mahjong tiles on a game table."><figcaption>Different players. Different incentives. Same game.</figcaption></figure>${body}</div>`
      :chapter.id==='04'
      ?`<div class="cover-reader-page fashion-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} · CHAPTER ${chapter.id}</p><span class="fashion-reader-number">${chapter.id}</span><h2>${esc(chapter.shortTitle)}</h2><p class="fashion-reader-subtitle">Be Your Own Label</p><figure class="fashion-reader-scene"><img src="assets/fashion-room-v2.webp" alt="A sneaker and lived-in wardrobe in a room overlooking the city."><figcaption>Same objects. Different worlds.</figcaption></figure>${body}</div>`
      :`<div class="cover-reader-page"><p class="cover-reader-kicker">${esc(numberLabel)}${part?` · PART ${roman[part.id]}`:''}</p><h2>${esc(chapter.title)}</h2>${part?`<p class="cover-reader-part">${esc(partLabel(part))}</p>`:''}${body}</div>`;
  }
  content.scrollTop=0;
  $('#cover-reading-folio').textContent=page.kind==='cover'?'COVER':page.kind==='introduction'?'i':page.label;
  const link=$('#cover-reading-link');
  link.href=page.kind==='cover'?'#introduction':page.href;
  link.innerHTML=`${page.kind==='cover'?'Open the book':page.kind==='introduction'?'Read Introduction':`Read ${page.label} in the book`} <span aria-hidden="true">→</span>`;
}
function positionCoverOrbit(rotation=coverRing?.rotation ?? -selectedCoverPage*coverStep){
  const radius=-$('#cover-stage').getBoundingClientRect().width*.457;
  $$('.cover-orbit-mark').forEach((element,index)=>{element.style.setProperty('--angle',`${index*coverStep+rotation}deg`);element.style.setProperty('--orbit-radius',`${radius}px`);});
}
function selectCoverPage(index,{fromRing=false}={}){
  selectedCoverPage=((index%coverPages.length)+coverPages.length)%coverPages.length;
  const page=coverPages[selectedCoverPage];
  $('#cover-stage').dataset.page=page.kind;
  $('#cover-stage').dataset.pageIndex=String(selectedCoverPage);
  $('#cover-scene').innerHTML=page.kind==='chapter'?(page.chapter.id==='00'?renderPortalPicture('rice'):page.chapter.id==='01'?renderPortalPicture('quant'):page.chapter.id==='02'?renderPortalPicture('expectedUtility'):page.chapter.id==='03'?renderPortalPicture('playToWin'):page.chapter.id==='04'?renderPortalPicture('fashion'):page.chapter.id==='08'?renderPortalPicture('motherRussiaCover'):page.chapter.id==='17'?renderPortalPicture('threeMeetingCover'):renderPortalScene(page.chapter)):page.kind==='cover'
    ?renderPortalPicture('cover')
    :renderPortalPicture('introductionCover');
  $('#cover-marker').innerHTML=page.kind==='chapter'?renderChapterMarker(page.chapter,{compact:true}):`<span class="frontmatter-marker" aria-hidden="true">${page.kind==='cover'?'▯':'i'}</span>`;
  $('#cover-marker').hidden=page.kind==='cover';
  $('#cover-marker').setAttribute('aria-label',page.kind==='chapter'?`Chapter marker ${page.label}: ${getChapterMarkerName(page.chapter)}`:page.kind==='cover'?'Book cover':'Introduction');
  $('#cover-chapter-link').href=page.href;
  $('#cover-chapter-label').textContent=page.kind==='cover'?'Book cover':page.kind==='introduction'?'Introduction':`${page.label} · ${page.title}`;
  $('#cover-chapter-link').title=page.kind==='cover'?'Open the introduction':page.title;
  $('#cover-stage').setAttribute('aria-label',`Book ring. ${page.kind==='cover'?'Book cover':page.title}. Drag to turn, arrow keys to choose, Enter to read.`);
  $('#cover-page-position').textContent=page.kind==='cover'?'COVER':page.kind==='introduction'?'FRONT MATTER':page.label==='00'?'PROLOGUE':`CHAPTER ${page.label} / ${chapters.at(-1).id}`;
  renderCoverReadingPage(page);
  $$('.cover-orbit-mark').forEach((element,i)=>{element.classList.toggle('active',i===selectedCoverPage);element.setAttribute('aria-pressed',i===selectedCoverPage);});
  if(!fromRing)coverRing?.setChapter(selectedCoverPage);
  positionCoverOrbit();
}
$('#cover-orbit-marks').innerHTML=coverPages.map((page,index)=>`<button class="cover-orbit-mark" data-cover-page="${index}" aria-label="${esc(page.kind==='cover'?'Book cover':page.title)}" title="${esc(page.kind==='cover'?'Book cover':page.title)}"><span>${page.label}</span></button>`).join('');
$('#cover-rotor').innerHTML=renderPortalFrame('cover-frame','assets/board-cover-ring.png?v=2');
coverRing=new PortalRing({stage:$('#cover-stage'),count:coverPages.length,initialIndex:0,onRotate(rotation,{animate}){
  $('#cover-stage').classList.toggle('ring-instant',!animate);$('#cover-stage').dataset.ringRotation=String(rotation);
  $('#cover-rotor').style.transform=`rotate(${rotation}deg)`;positionCoverOrbit(rotation);
},onSelect(index){selectCoverPage(index,{fromRing:true});}});
new ResizeObserver(()=>positionCoverOrbit()).observe($('#cover-stage'));
$('#cover-prev').addEventListener('click',()=>selectCoverPage(selectedCoverPage-1));
$('#cover-next').addEventListener('click',()=>selectCoverPage(selectedCoverPage+1));
$('#cover-stage').addEventListener('keydown',event=>{
  if(event.target.closest('button')&&['Enter',' '].includes(event.key))return;
  const open=()=>navigate(coverPages[selectedCoverPage].href.slice(1));
  const actions={ArrowRight:()=>selectCoverPage(selectedCoverPage+1),ArrowDown:()=>selectCoverPage(selectedCoverPage+1),ArrowLeft:()=>selectCoverPage(selectedCoverPage-1),ArrowUp:()=>selectCoverPage(selectedCoverPage-1),Home:()=>selectCoverPage(0),End:()=>selectCoverPage(coverPages.length-1),Enter:open,' ':open};
  if(actions[event.key]){event.preventDefault();actions[event.key]();}
});

$('#motion-toggle').addEventListener('click',()=>{reducedMotion=!reducedMotion;store.set('json-reduced-motion',reducedMotion);applyMotion();});
motionMedia.addEventListener('change',event=>{reducedMotion=event.matches;applyMotion();});
for(const [selector,delta] of [['#font-down',-2],['#font-up',2]])$(selector).addEventListener('click',()=>{readingSize=Math.max(18,Math.min(34,readingSize+delta));store.set('json-reading-size',readingSize);applyReadingSize();});
$('#menu-open').addEventListener('click',()=>drawer.showModal());
$('#cover-menu-open').addEventListener('click',()=>drawer.showModal());
$('#menu-close').addEventListener('click',()=>drawer.close());
drawer.addEventListener('click',event=>{if(event.target===drawer){const rect=drawer.getBoundingClientRect();if(event.clientX>rect.right)drawer.close();}});
document.addEventListener('click',event=>{
  if(event.target.closest('.skip-link')){event.preventDefault();$('#book-content').focus();return;}
  const coverPage=event.target.closest('[data-cover-page]');if(coverPage){selectCoverPage(Number(coverPage.dataset.coverPage));return;}
  const mapChapter=event.target.closest('[data-map-chapter]');if(mapChapter){selectMapChapter(Number(mapChapter.dataset.mapChapter));return;}
  const mapPart=event.target.closest('[data-map-part]');if(mapPart){selectMapChapter(Number(chapters.find(chapter=>chapter.act===Number(mapPart.dataset.mapPart)).id));return;}
  const link=event.target.closest('a[href^="#"]');
  if(link&&!event.metaKey&&!event.ctrlKey&&!event.shiftKey&&!event.altKey){event.preventDefault();navigate(link.getAttribute('href').slice(1));}
});
window.addEventListener('popstate',()=>renderRoute(parseRoute()));
window.addEventListener('hashchange',()=>{const route=parseRoute();if(route.key!==currentRoute?.key)renderRoute(route);});
window.addEventListener('scroll',()=>{clearTimeout(scrollTimer);scrollTimer=setTimeout(savePosition,180);},{passive:true});
window.addEventListener('pagehide',savePosition);
$('#book-epigraph').innerHTML=introduction.epigraph.split(/(?<=answer\.)\s+/).map(line=>`<p>${esc(line)}</p>`).join('');
$('#introduction-text').innerHTML=introduction.sections.map((section,index)=>`<section class="intro-section${index===0?' intro-synopsis':''}"><h2>${esc(section.heading)}</h2>${section.paragraphs.map(paragraph=>`<p>${introInline(paragraph)}</p>`).join('')}</section>`).join('');
renderContents();renderArchive();applyReadingSize();applyMotion();renderRoute(parseRoute(),{initial:true});
