import { acts, chapters, renderPortal, renderIcon } from './chapters.js?v=3';
import { renderChapterMarker, getChapterMarkerName, renderReferenceBowlIcon } from './markers.js?v=3';
import { PortalRing } from './ring.js?v=3';

const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];
const esc = (s) => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const roman = ['','I','II','III','IV','V'];
const library = await fetch(new URL('./content/manuscripts.json',import.meta.url)).then(response=>{
 if(!response.ok)throw new Error('Published chapters could not load');return response.json();
});
const publishedById = new Map(library.chapters.filter(c=>c.editorialId!==null).map(c=>[c.editorialId,c]));
const publishedBySlug = new Map(library.chapters.map(c=>[c.slug,c]));
const storage = {get(k,fallback){try{return JSON.parse(localStorage.getItem(k)) ?? fallback;}catch{return fallback;}},set(k,v){try{localStorage.setItem(k,JSON.stringify(v));}catch{}}};
const mediaMotion = matchMedia('(prefers-reduced-motion: reduce)');
let selected = 0, ring = null, filter = 'all', readerId = null, lastFocus = null, historyScroll = window.scrollY;
let reduced = storage.get('json-reduced-motion', mediaMotion.matches);
let readingSize = storage.get('json-reading-size',24);
const readingPositions = storage.get('json-reading-positions',{});
const indexDialog = $('#index-dialog'), readerDialog = $('#reader-dialog'), bookDialog = $('#book-dialog'), archiveDialog = $('#archive-dialog');
const chapterById = (id) => chapters.find(c => c.id === id);
const actById = (id) => acts.find(a => a.id === id);
const actLabel = (c) => c.act ? `ACT ${roman[c.act]} · ${actById(c.act).key.replaceAll('_',' ').toUpperCase()}` : 'PROLOGUE · BEFORE THE FIRST VERSION';
const artHTML = (c) => c.id === '00' ? '<img class="rice-portal-image" src="assets/rice-portal.png" alt="An ivory and cobalt floral paper portal frames a childhood family dinner beneath an amber lamp.">' : c.id === '04' ? '<img src="assets/fashion-portal.png" alt="A layered paper portal into a warm bedroom: sneakers, an inherited shirt, a wardrobe, and a window over Paris.">' : renderPortal(c);
$('#portal-art').innerHTML='<div id="portal-scene" class="portal-scene"></div><div id="portal-rim" class="portal-rim" aria-hidden="true"><div id="portal-rim-art" class="portal-rim-art"></div></div><div id="portal-marker" class="portal-page-marker"></div>';


function makeNavigation(){
  $('#orbit-marks').innerHTML = chapters.map((c,i) => `<button class="orbit-mark" data-chapter="${i}" aria-label="Select chapter ${c.id}: ${esc(c.title)}" title="${c.id} · ${esc(c.title)}"><span>${c.id}</span></button>`).join('');
  $('#act-tabs').innerHTML = acts.map(a => `<button class="act-tab" data-act="${a.id}" style="--act-color:${a.color}" aria-label="Explore act ${roman[a.id]}: ${esc(a.key.replaceAll('_',' '))}"><span class="act-roman"><i class="act-dot"></i>${roman[a.id]}</span><span class="act-name">${esc(a.key)}</span></button>`).join('');
  $('#index-filters').innerHTML = `<button class="index-filter active" data-filter="all" aria-pressed="true">All chapters</button><button class="index-filter" data-filter="0" aria-pressed="false">Prologue</button>` + acts.map(a=>`<button class="index-filter" data-filter="${a.id}" aria-pressed="false">${roman[a.id]} · ${esc(a.name)}</button>`).join('');
}

function setOrbitPositions(rotation = ring?.rotation ?? -selected*11.25){
 const radius = $('#portal-stage').getBoundingClientRect().width * -.475;
 $$('.orbit-mark').forEach((el,i)=>{el.style.setProperty('--angle',`${i*11.25+rotation}deg`);el.style.setProperty('--orbit-radius',`${radius}px`);});
}

function updateRail(){
 let first = Math.max(0, Math.min(26, selected-2));
 const ids = Array.from({length:6},(_,i)=>i+first);
 $('#rail-buttons').innerHTML = ids.map(i=>`<button class="rail-button${i===selected?' active':''}" data-chapter="${i}" aria-label="Select chapter ${chapters[i].id}: ${esc(chapters[i].title)}" aria-pressed="${i===selected}">${chapters[i].id}</button>`).join('');
}

function selectChapter(index,{announce=false,fromRing=false}={}){
 selected = (index+32)%32;
 const c=chapters[selected], act=actById(c.act);
 document.documentElement.style.setProperty('--accent', act?.color || '#d8ad72');
 $('#chapter-act').textContent=actLabel(c);
 $('#chapter-number').textContent=c.id;
 const titleParts = c.id==='04' ? ['Fashion','Be Your Own Label'] : [c.shortTitle || c.title,''];
 $('#chapter-title').textContent=titleParts[0];
 $('#chapter-title').classList.toggle('long-title',titleParts[0].length>17);
 $('#chapter-subtitle').textContent=titleParts[1];
 $('#chapter-subtitle').hidden=!titleParts[1];
 $('#chapter-description').textContent=c.id==='04' ? 'A lived-in bedroom. A pair of sneakers. An old inherited shirt. The things we wear, and the selves we try on.' : c.scene;
 $('#chapter-motif').textContent=c.motif.toUpperCase();
 $('#chapter-availability').textContent=publishedById.has(c.id)?'COMPLETE CHAPTER':'CHAPTER PREVIEW';
 $('#enter-chapter').innerHTML=`${publishedById.has(c.id)?'Read chapter':'Enter preview'} <span class="arrow-ne" aria-hidden="true"></span>`;
 $('#chapter-icon').innerHTML=c.id==='00'?renderReferenceBowlIcon(38):renderIcon(c,38);
 $('#portal-scene').innerHTML=artHTML(c);
 $('#portal-rim-art').innerHTML=artHTML(c);
 $('#portal-marker').innerHTML=renderChapterMarker(c);
 $('#portal-marker').dataset.chapter=c.id;
 $('#portal-marker').setAttribute('aria-label',`Chapter ${c.id} bookmark: ${getChapterMarkerName(c)}`);
 $('#portal-stage').setAttribute('aria-label',`Chapter ${c.id}: ${c.title}. Drag around the ring to rotate, swipe the center, or use arrow keys. Enter opens the chapter.`);
 $('#portal-bottom-label').textContent=`${c.id} / 32`;
 $$('.orbit-mark').forEach((el,i)=>{el.classList.toggle('active',i===selected);el.setAttribute('aria-pressed',i===selected);});
 $$('.act-tab').forEach(el=>{let active=Number(el.dataset.act)===c.act;el.classList.toggle('active',active);el.setAttribute('aria-pressed',active);});
 if(!fromRing)ring?.setChapter(selected);
 setOrbitPositions();updateRail();
 if(announce) $('#interaction-status').textContent=`Selected chapter ${c.id}: ${c.title}`;
}

function normalize(s){return s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d').replace(/Đ/g,'D').toLowerCase();}
function renderIndex(){
 const query=normalize($('#chapter-search').value.trim());
 const matches=chapters.filter(c=>(filter==='all'||String(c.act)===filter) && normalize([c.title,c.scene,...c.objects].join(' ')).includes(query));
 $('#chapter-grid').innerHTML=matches.map(c=>`<button class="chapter-card${Number(c.id)===selected?' selected':''}" data-index-chapter="${Number(c.id)}" style="--card-color:${actById(c.act)?.color||'#d8ad72'}" aria-label="Explore chapter ${c.id}: ${esc(c.title)}"><span class="card-topline"><span>${c.id}</span>${c.id==='00'?renderReferenceBowlIcon(24):renderIcon(c,24)}</span><h3>${esc(c.title)}</h3><span>${c.act ? `ACT ${roman[c.act]} · ${esc(actById(c.act).name.toUpperCase())}`:'PROLOGUE'} <span class="card-availability">${publishedById.has(c.id)?'FULL ESSAY':'PREVIEW'}</span></span></button>`).join('');
 $('#search-empty').hidden=matches.length>0;
 $('#chapter-grid').hidden=matches.length===0;
 $('#search-count').textContent=`${matches.length} ${matches.length===1?'chapter':'chapters'}${query?' found':''}`;
}
function openIndex(){lastFocus=document.activeElement;renderIndex();indexDialog.showModal();setTimeout(()=>$('#chapter-search').focus(),0);}
function closeModal(dialog){dialog.close();if(lastFocus?.isConnected)lastFocus.focus({preventScroll:true});}

function saveReadingPosition(){if(readerId){readingPositions[readerId]=$('#reader-body').scrollTop;storage.set('json-reading-positions',readingPositions);}}
function fillReader(c,manuscript,{archive=false,key=c.id}={}){
 if(readerDialog.open)saveReadingPosition();
 readerId=key;
 $('#reader-act').textContent=archive?'PUBLISHED ARCHIVE · ADDITIONAL ESSAY':actLabel(c);
 $('#reader-number').textContent=archive?`ARCHIVE ${manuscript.legacyId}`:c.id;
 $('#reader-title').textContent=manuscript?.originalTitle || c.title;
 $('#reader-label').textContent=manuscript?'COMPLETE CHAPTER · PUBLISHED EDITION':'CHAPTER PREVIEW · DESIGN SYNOPSIS';
 $('#reader-art').hidden=archive;
 $('#reader-art').innerHTML=archive?'':`<div class="portal-scene">${artHTML(c)}</div><div class="portal-page-marker">${renderChapterMarker(c,{compact:true})}</div>`;
 $('#reader-scene').hidden=!!manuscript;
 $('#reader-scene').textContent=c.scene || '';
 $('#reader-manuscript').hidden=!manuscript;
 $('#reader-manuscript').innerHTML=manuscript?(manuscript.bodyHtml || manuscript.html):'';
 $('.memory-objects').hidden=archive;
 $('#reader-objects').innerHTML=(c.objects||[]).map(o=>`<span>${esc(o)}</span>`).join('');
 $('.manuscript-note').innerHTML=manuscript?`<a href="${esc(manuscript.archiveUrl)}" target="_blank" rel="noopener">Explore the original chapter and memory archive <span aria-hidden="true">↗</span></a>`:'This preview follows the supplied chapter design atlas. The complete essay will appear here when the approved manuscript is added.';
 $('.reading-page').style.setProperty('--reading-font',`${readingSize}px`);
 $('#reader-prev').disabled=archive||Number(c.id)===0;
 $('#reader-next').disabled=archive||Number(c.id)===31;
 $('#font-down').disabled=readingSize<=18;$('#font-up').disabled=readingSize>=34;
 if(!readerDialog.open)readerDialog.showModal();
 document.title=`${manuscript?.originalTitle||c.title} — .json`;
 requestAnimationFrame(()=>{$('#reader-body').scrollTop=readingPositions[key]||0;});
}
function displayReader(id){
 const c=chapterById(id);if(!c)return;
 selectChapter(Number(id));
 fillReader(c,publishedById.get(id));
}
function displayArchive(slug){
 const manuscript=publishedBySlug.get(slug);if(!manuscript)return;
 if(manuscript.editorialId!==null){displayReader(manuscript.editorialId);return;}
 fillReader({title:manuscript.originalTitle,id:manuscript.legacyId},manuscript,{archive:true,key:`archive/${slug}`});
}
function openPublishedArchive(){
 if(indexDialog.open)indexDialog.close();
 lastFocus=document.activeElement;
 $('#published-chapters').innerHTML=library.chapters.map(c=>`<button class="published-chapter" data-published-slug="${esc(c.slug)}"><span class="published-number">${esc(c.legacyId)}</span><span><strong>${esc(c.originalTitle)}</strong><small>COMPLETE ESSAY${c.editorialId!==null?` · PORTAL ${c.editorialId}`:' · FROM THE PUBLISHED ARCHIVE'}</small></span><span aria-hidden="true">→</span></button>`).join('');
 archiveDialog.showModal();
}
function enterArchive(slug){
 const manuscript=publishedBySlug.get(slug);if(!manuscript)return;
 if(archiveDialog.open)archiveDialog.close();
 if(manuscript.editorialId!==null){enterChapter(manuscript.editorialId);return;}
 if(!readerDialog.open){lastFocus=document.activeElement;historyScroll=window.scrollY;}
 saveReadingPosition();
 const url=new URL(location.href);url.hash=`archive/${slug}`;
 const readerDepth=history.state?.jsonReader?(history.state.readerDepth||1)+1:1;
 history.pushState({jsonReader:true,id:`archive/${slug}`,readerDepth,returnScroll:historyScroll},'',url);
 displayArchive(slug);
}
function enterChapter(id=chapters[selected].id){
 if(indexDialog.open)indexDialog.close();
 if(!readerDialog.open){lastFocus=document.activeElement;historyScroll=window.scrollY;}
 saveReadingPosition();
 const url=new URL(location.href);url.hash=`chapter/${id}`;
 const readerDepth=history.state?.jsonReader ? (history.state.readerDepth || 1)+1 : 1;
 history.pushState({jsonReader:true,id,readerDepth,returnScroll:historyScroll},'',url);
 displayReader(id);
}
function exitReader(){
 saveReadingPosition();
 if(history.state?.jsonReader){history.go(-(history.state.readerDepth || 1));}
 else{const url=new URL(location.href);url.hash='explorer';history.replaceState(null,'',url);hideReader();}
}
function hideReader(){if(readerDialog.open){saveReadingPosition();readerDialog.close();readerId=null;document.title='.json — Jason, Under Revision';requestAnimationFrame(()=>{window.scrollTo({top:historyScroll,behavior:'instant'});$('#enter-chapter').focus({preventScroll:true});});}}
function restoreLocation(){
 const match=location.hash.match(/^#chapter\/(\d{2})$/),archiveMatch=location.hash.match(/^#archive\/([a-z0-9-]+)$/);
 if(match&&chapterById(match[1])){if(!readerDialog.open||readerId!==match[1])displayReader(match[1]);}
 else if(archiveMatch&&publishedBySlug.has(archiveMatch[1])){if(!readerDialog.open||readerId!==`archive/${archiveMatch[1]}`)displayArchive(archiveMatch[1]);}
 else hideReader();
}
function applyMotion(){document.body.classList.toggle('reduced-motion',reduced);$('#motion-toggle').setAttribute('aria-pressed',reduced);$('#motion-label').textContent=reduced?'Motion reduced':'Motion on';$('#portal-stage').style.touchAction='none';}

makeNavigation();selectChapter(selected);applyMotion();
ring = new PortalRing({stage:$('#portal-stage'),initialIndex:selected,
 onRotate(rotation,{animate}){
   const stage=$('#portal-stage');
   stage.classList.toggle('ring-instant',!animate);
   stage.dataset.ringRotation=String(rotation);
   $('#portal-rim').style.transform=`rotate(${rotation}deg)`;
   setOrbitPositions(rotation);
 },
 onSelect(index){selectChapter(index,{fromRing:true,announce:true});}
});
new ResizeObserver(()=>setOrbitPositions()).observe($('#portal-stage'));
document.addEventListener('click',e=>{
 const published=e.target.closest('[data-published-slug]');if(published){enterArchive(published.dataset.publishedSlug);return;}
 const ch=e.target.closest('[data-chapter]');if(ch){selectChapter(Number(ch.dataset.chapter),{announce:true});return;}
 const act=e.target.closest('[data-act]');if(act){const first=chapters.find(c=>c.act===Number(act.dataset.act));selectChapter(Number(first.id),{announce:true});return;}
 const fil=e.target.closest('[data-filter]');if(fil){filter=fil.dataset.filter;$$('.index-filter').forEach(el=>{const active=el.dataset.filter===filter;el.classList.toggle('active',active);el.setAttribute('aria-pressed',active);});renderIndex();return;}
 const card=e.target.closest('[data-index-chapter]');if(card){selectChapter(Number(card.dataset.indexChapter),{announce:true});closeModal(indexDialog);$('#explorer').scrollIntoView({behavior:reduced?'instant':'smooth',block:'start'});$('#enter-chapter').focus({preventScroll:true});}
});
$$('.index-open').forEach(el=>el.addEventListener('click',openIndex));
 $$('.archive-open').forEach(el=>el.addEventListener('click',openPublishedArchive));
$$('.close-dialog').forEach(el=>el.addEventListener('click',()=>closeModal(el.closest('dialog'))));
$('#chapter-search').addEventListener('input',renderIndex);
$('#prev-chapter').addEventListener('click',()=>selectChapter(selected-1,{announce:true}));
$('#next-chapter').addEventListener('click',()=>selectChapter(selected+1,{announce:true}));
$('#enter-chapter').addEventListener('click',()=>enterChapter());
$('#reader-close').addEventListener('click',exitReader);$('#reader-back').addEventListener('click',exitReader);
readerDialog.addEventListener('cancel',e=>{e.preventDefault();exitReader();});
readerDialog.addEventListener('close',()=>{saveReadingPosition();});
$('#reader-prev').addEventListener('click',()=>{if(Number(readerId)>0)enterChapter(String(Number(readerId)-1).padStart(2,'0'));});
$('#reader-next').addEventListener('click',()=>{if(Number(readerId)<31)enterChapter(String(Number(readerId)+1).padStart(2,'0'));});
for(const [selector,diff] of [['#font-down',-2],['#font-up',2]]) $(selector).addEventListener('click',()=>{readingSize=Math.max(18,Math.min(34,readingSize+diff));storage.set('json-reading-size',readingSize);$('.reading-page').style.setProperty('--reading-font',`${readingSize}px`);$('#font-down').disabled=readingSize<=18;$('#font-up').disabled=readingSize>=34;});
$('#motion-toggle').addEventListener('click',()=>{reduced=!reduced;storage.set('json-reduced-motion',reduced);applyMotion();});
mediaMotion.addEventListener('change',e=>{reduced=e.matches;applyMotion();});
$('#open-book-detail').addEventListener('click',()=>{lastFocus=document.activeElement;bookDialog.showModal();});
$('#start-prologue').addEventListener('click',()=>{selectChapter(0);enterChapter('00');});
for(const d of [indexDialog,bookDialog,archiveDialog])d.addEventListener('click',e=>{if(e.target===d){const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)closeModal(d);}});
window.addEventListener('popstate',restoreLocation);window.addEventListener('hashchange',restoreLocation);
window.addEventListener('pagehide',saveReadingPosition);
const stage=$('#portal-stage');
stage.addEventListener('keydown',e=>{if(e.target.closest('button')&&['Enter',' '].includes(e.key))return;const actions={ArrowRight:()=>selectChapter(selected+1),ArrowDown:()=>selectChapter(selected+1),ArrowLeft:()=>selectChapter(selected-1),ArrowUp:()=>selectChapter(selected-1),Home:()=>selectChapter(0),End:()=>selectChapter(31),Enter:()=>enterChapter(),' ':()=>enterChapter()};if(actions[e.key]){e.preventDefault();actions[e.key]();}});
restoreLocation();
