import { chapters, renderIcon, renderPortal, renderPortalScene } from './chapters.js?v=36';
import { introduction, parts, chapterNotes } from './book.js?v=28';
import { renderChapterMarker, getChapterMarkerName } from './markers.js?v=31';
import { PortalRing } from './ring.js?v=10';
import { renderPortalPicture, renderPortalFrame, renderFramedPortal } from './portal-art.js?v=59';

const $ = selector => document.querySelector(selector);
const $$ = selector => [...document.querySelectorAll(selector)];
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const introInline = value => esc(value).replace(/\*([^*]+)\*/g,'<em>$1</em>');
const roman = ['','I','II','III','IV','V'];
const store = {get(key,fallback){try{return JSON.parse(localStorage.getItem(key)) ?? fallback;}catch{return fallback;}},set(key,value){try{localStorage.setItem(key,JSON.stringify(value));}catch{}}};
const library = await fetch(new URL('./content/manuscripts.json?v=30',import.meta.url)).then(response=>{
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
  if(chapter.id==='02')return renderFramedPortal('expectedUtility','expected-utility-chapter','assets/expected-utility-ring-v3.png');
  if(chapter.id==='03')return renderFramedPortal('playToWin','play-to-win-chapter','assets/play-to-win-ring-v2.png');
  if(chapter.id==='04')return renderFramedPortal('fashion','fashion-chapter','assets/fashion-ring-v2.png');
  if(chapter.id==='05')return renderFramedPortal('flow','flow-chapter','assets/flow-ring-v2.png');
  if(chapter.id==='06')return renderFramedPortal('redButton','red-button-chapter','assets/red-button-ring-v1.png');
  if(chapter.id==='07')return renderFramedPortal('oldFriend','old-friend-chapter','assets/old-friend-ring-v1.png');
  if(chapter.id==='10')return renderFramedPortal('dreamDiary','dream-diary-chapter','assets/dream-diary-ring-v1.png');
  if(chapter.id==='13')return renderFramedPortal('myBrothers','my-brothers-chapter','assets/my-brothers-ring-v1.png');
  if(chapter.id==='15')return renderFramedPortal('twentyEightToday','twenty-eight-today-chapter','assets/twenty-eight-today-ring-v1.png');
  if(chapter.id==='23')return renderFramedPortal('uglyProjections','ugly-projections-chapter','assets/ugly-projections-ring-v1.png');
  if(chapter.id==='34')return renderFramedPortal('afterLeaving','after-leaving-chapter','assets/after-leaving-ring-v1.png');
  if(chapter.id==='32')return renderFramedPortal('commandRespect','command-respect-chapter','assets/command-respect-ring-v1.png');
  if(chapter.id==='30')return renderFramedPortal('negativeSum','negative-sum-chapter','assets/negative-sum-ring-v1.png');
  if(chapter.id==='29')return renderFramedPortal('moralStory','moral-story-chapter','assets/moral-story-ring-v1.png');
  if(chapter.id==='28')return renderFramedPortal('goodBoy','good-boy-chapter','assets/good-boy-ring-v1.png');
  if(chapter.id==='27')return renderFramedPortal('recordKeeping','record-keeping-chapter','assets/record-keeping-ring-v1.png');
  if(chapter.id==='26')return renderFramedPortal('betterBrighter','better-brighter-chapter','assets/better-brighter-ring-v1.png');
  if(chapter.id==='25')return renderFramedPortal('payoffMatrix','payoff-matrix-chapter','assets/payoff-matrix-ring-v1.png');
  if(chapter.id==='24')return renderFramedPortal('officeBattlefield','office-chapter','assets/office-battlefield-ring-v1.png');
  if(chapter.id==='16')return renderFramedPortal('badTrip','bad-trip-chapter','assets/bad-trip-ring-v1.png');
  if(chapter.id==='17')return renderFramedPortal('asteroid','asteroid-chapter','assets/asteroid-ring-v1.png');
  if(chapter.id==='22')return renderFramedPortal('runaway','runaway-chapter','assets/runaway-ring-v1.png');
  if(chapter.id==='08')return renderFramedPortal('motherRussia','mother-russia-chapter','assets/mother-russia-ring-v2.png');
  if(chapter.id==='09')return renderFramedPortal('dreamWorld','dream-world-chapter','assets/dream-world-ring-v2.png');
  if(chapter.id==='11')return renderFramedPortal('coincidence','coincidence-chapter','assets/coincidence-ring-v1.png');
  if(chapter.id==='14')return renderFramedPortal('saigon','saigon-chapter','assets/saigon-ring-v1.png');
  if(chapter.id==='18')return renderFramedPortal('threeMeeting','three-meeting-chapter','assets/three-meeting-ring-v2.png?v=4');
  if(chapter.id==='19')return renderFramedPortal('datingAlgorithm','dating-algorithm-chapter','assets/dating-algorithm-ring-v2.png');
  if(chapter.id==='20')return renderFramedPortal('dating102','dating-102-chapter','assets/dating-102-ring-v2.png');
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
  const opening=id==='10'
    ?`<header class="dream-diary-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="dream-diary-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">Dream Diary</h1><p class="dream-diary-chapter-subtitle">The Things We Never Saved</p><p class="dream-diary-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="dream-diary-chapter-stage">${chapterArtwork(chapter)}<div class="dream-diary-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Nhưng rồi đoàn tàu tới.<br>Và tôi tỉnh dậy.</p><button type="button" id="dream-diary-read">Read the chapter <span aria-hidden="true">&#8595;</span></button></div></div><figure class="dream-diary-spread-banner"><img src="assets/dream-diary-spread-v1.webp" width="1632" height="309" alt="An open dream diary, yellow metro train, two people holding hands, pencil, sketches, a window and childhood objects."><figcaption>Dream / Memory / Letting Go</figcaption></figure>`
    :id==='13'
    ?`<header class="my-brothers-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="my-brothers-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">My brothers</h1><p class="my-brothers-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="my-brothers-chapter-stage">${chapterArtwork(chapter)}<div class="my-brothers-chapter-note"><span>A VISUAL INTRODUCTION</span><p>where I belong</p><button type="button" id="my-brothers-read">Read the chapter <span aria-hidden="true">&#8595;</span></button></div></div><figure class="my-brothers-spread-banner"><img src="assets/my-brothers-spread-v1.webp" width="1632" height="289" alt="Four former teammates, a glowing universe model, books, drinks, physics diagrams and a globe."><figcaption>Friendship / Curiosity / Belonging</figcaption></figure>`
    :id==='15'
    ?`<header class="twenty-eight-today-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="twenty-eight-today-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">I'm 28 today</h1><p class="twenty-eight-today-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="twenty-eight-today-chapter-stage">${chapterArtwork(chapter)}<div class="twenty-eight-today-chapter-note"><span>A VISUAL INTRODUCTION</span><p>life is beautiful<br>isn’t it</p><button type="button" id="twenty-eight-today-read">Read the chapter <span aria-hidden="true">&#8595;</span></button></div></div><figure class="twenty-eight-today-spread-banner"><img src="assets/twenty-eight-today-spread-v1.webp" width="1632" height="289" alt="Jason, an open window, birthday cake, friends, camera, film frames, music and keepsakes."><figcaption>Memory / Friendship / Gratitude</figcaption></figure>`
    :id==='23'
    ?`<header class="ugly-projections-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="ugly-projections-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">Ugly Projections</h1><p class="ugly-projections-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="ugly-projections-chapter-stage">${chapterArtwork(chapter)}<div class="ugly-projections-chapter-note"><span>A VISUAL INTRODUCTION</span><p>I kept seeing women<br>as someone they weren't.</p><button type="button" id="ugly-projections-read">Read the chapter <span aria-hidden="true">&#8595;</span></button></div></div><figure class="ugly-projections-spread-banner"><img src="assets/ugly-projections-spread-v1.webp" width="1632" height="289" alt="Jason, a film projector, shadow screen, woman, lens, paintings, empty chairs and pause symbol."><figcaption>Memory / Projection / Recognition</figcaption></figure>`
    :id==='34'
    ?`<header class="after-leaving-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="after-leaving-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">Office Battlefield</h1><p class="after-leaving-chapter-subtitle">Things You Only See After Leaving</p><p class="after-leaving-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="after-leaving-chapter-stage">${chapterArtwork(chapter)}<div class="after-leaving-chapter-note"><span>A VISUAL INTRODUCTION</span><p>I matter here.<br>I belong here.</p><button type="button" id="after-leaving-read">Read the chapter <span aria-hidden="true">&#8595;</span></button></div></div><figure class="after-leaving-spread-banner"><img src="assets/after-leaving-spread-v1.webp" width="1632" height="289" alt="Jason, a roadtrip whiteboard, phone, umbrella, mountains, farewell gifts and office keepsakes."><figcaption>Memory / Care / Belonging</figcaption></figure>`
    :id==='32'
    ?`<header class="command-respect-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="command-respect-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">Office Battlefield</h1><p class="command-respect-chapter-subtitle">Command Respect</p><p class="command-respect-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="command-respect-chapter-stage">${chapterArtwork(chapter)}<div class="command-respect-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Those were<br>my choices.</p><button type="button" id="command-respect-read">Read the chapter <span aria-hidden="true">&#8595;</span></button></div></div><figure class="command-respect-spread-banner"><img src="assets/command-respect-spread-v1.webp" width="1632" height="289" alt="Jason, an arched childhood mirror, a small boy, boxing gloves, a work ticket and a note from David."><figcaption>Fear / Respect / Choice</figcaption></figure>`
    :id==='30'
    ?`<header class="negative-sum-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="negative-sum-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">Office Battlefield</h1><p class="negative-sum-chapter-subtitle">Negative-Sum Game</p><p class="negative-sum-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="negative-sum-chapter-stage">${chapterArtwork(chapter)}<div class="negative-sum-chapter-note"><span>A VISUAL INTRODUCTION</span><p>I mistook that anger<br>for strategy.</p><button type="button" id="negative-sum-read">Read the chapter <span aria-hidden="true">&#8595;</span></button></div></div><figure class="negative-sum-spread-banner"><img src="assets/negative-sum-spread-v1.webp" width="1632" height="289" alt="Jason, two chess pieces, a cost ledger, office chair, mugs and records."><figcaption>Time / Trust / Friendship</figcaption></figure>`
    :id==='29'
    ?`<header class="moral-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="moral-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">Office Battlefield</h1><p class="moral-chapter-subtitle">The Moral Story Schools Don't Teach You</p><p class="moral-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="moral-chapter-stage">${chapterArtwork(chapter)}<div class="moral-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Implementation?<br>Not so much.</p><button type="button" id="moral-read">Read the chapter <span aria-hidden="true">&#8595;</span></button></div></div><figure class="moral-spread-banner"><img src="assets/moral-story-spread-v1.webp" width="1632" height="289" alt="Jason, an open book on context and impact, a versioned draft, mirror, compass and office documents."><figcaption>Context / Audience / Timing / Impact</figcaption></figure>`
    :id==='28'
    ?`<header class="good-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="good-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">Office Battlefield</h1><p class="good-chapter-subtitle">Good Boy</p><p class="good-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="good-chapter-stage">${chapterArtwork(chapter)}<div class="good-chapter-note"><span>A VISUAL INTRODUCTION</span><p>You're a nice guy,<br>don't be mean.</p><button type="button" id="good-read">Read the chapter <span aria-hidden="true">&#8595;</span></button></div></div><figure class="good-spread-banner"><img src="assets/good-boy-spread-v1.webp" width="1632" height="289" alt="Jason, a rubber stamp, an apology letter, phone, clock and office conversation objects."><figcaption>Apology / Validation / Escalation / Pause</figcaption></figure>`
    :id==='27'
    ?`<header class="record-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="record-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">Office Battlefield</h1><p class="record-chapter-subtitle">Masterclass in Record Keeping</p><p class="record-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="record-chapter-stage">${chapterArtwork(chapter)}<div class="record-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Version history.<br>Timestamp. Event log.<br>Provenance. Evidence.</p><button type="button" id="record-read">Read the chapter <span aria-hidden="true">&#8595;</span></button></div></div><figure class="record-spread-banner"><img src="assets/record-keeping-spread-v1.webp" width="1632" height="289" alt="Jason, an AI assistant, an open record log, magnifying glass, files, clock and locked envelope."><figcaption>History / Timestamp / Provenance / Evidence</figcaption></figure>`
    :id==='26'
    ?`<header class="better-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="better-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">Office Battlefield</h1><p class="better-chapter-subtitle">Better and Brighter Than Ever</p><p class="better-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="better-chapter-stage">${chapterArtwork(chapter)}<div class="better-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Better and brighter than ever.</p><button type="button" id="better-read">Read the chapter <span aria-hidden="true">&#8595;</span></button></div></div><figure class="better-spread-banner"><img src="assets/better-brighter-spread-v1.webp" width="1632" height="289" alt="Jason, an eye-shaped doorway, two jerseys, a gift, two mugs, an empty chair and office objects."><figcaption>Trust / Friendship / Sight / Distance</figcaption></figure>`
    :id==='25'
    ?`<header class="payoff-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="payoff-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">Office Battlefield</h1><p class="payoff-chapter-subtitle">The Payoff Matrix</p><p class="payoff-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="payoff-chapter-stage">${chapterArtwork(chapter)}<div class="payoff-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Game over. Checkmate.</p><button type="button" id="payoff-read">Read the chapter <span aria-hidden="true">&#8595;</span></button></div></div><figure class="payoff-spread-banner"><img src="assets/payoff-matrix-spread-v1.webp" width="1632" height="289" alt="Jason, an AI agent, scorecards, a payoff grid, chess pieces, a phone and office objects."><figcaption>Score / Strategy / Certainty / Doubt</figcaption></figure>`
    :id==='24'
    ?`<header class="office-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="office-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">Office Battlefield</h1><p class="office-chapter-subtitle">The 23-Word Nuclear Warhead</p><p class="office-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="office-chapter-stage">${chapterArtwork(chapter)}<div class="office-chapter-note"><span>A VISUAL INTRODUCTION</span><p>All in one Slack message.</p><button type="button" id="office-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="office-spread-banner"><img src="assets/office-battlefield-spread-v1.webp" width="1632" height="327" alt="Jason, an AI agent, paper message, chess pieces, task ticket, laptop and office objects from the board."><figcaption>Message / Work / Strategy / Perception</figcaption></figure>`
    :id==='16'
    ?`<header class="bad-trip-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="bad-trip-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.title)}</h1><p class="bad-trip-chapter-subtitle">Identity / Memory / Work / Return</p><p class="bad-trip-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="bad-trip-chapter-stage">${chapterArtwork(chapter)}<div class="bad-trip-chapter-note"><span>A VISUAL INTRODUCTION</span><p>I just wanted to be Jason.</p><button type="button" id="bad-trip-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="bad-trip-spread-banner"><img src="assets/bad-trip-spread-v1.webp" width="1632" height="321" alt="A mirror, old photographs, vinyl record, work desk, suitcase and two versions of Jason."><figcaption>Identity / Memory / Work / Return</figcaption></figure>`
    :id==='22'
    ?`<header class="runaway-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="runaway-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.title)}</h1><p class="runaway-chapter-subtitle">Drawing / Music / Care / Distance</p><p class="runaway-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="runaway-chapter-stage">${chapterArtwork(chapter)}<div class="runaway-chapter-note"><span>A VISUAL INTRODUCTION</span><p>A chỉ muốn ở đó.</p><button type="button" id="runaway-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="runaway-spread-banner"><img src="assets/runaway-spread-v1.webp" width="1632" height="336" alt="Jason, a woman, Gấu, an open doorway, a sofa, a drawing tablet, headphones and music."><figcaption>Drawing / Music / Care / Distance</figcaption></figure>`
    :id==='17'
    ?`<header class="asteroid-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="asteroid-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.title)}</h1><p class="asteroid-chapter-subtitle">Orbit / Work / Connection / Distance</p><p class="asteroid-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="asteroid-chapter-stage">${chapterArtwork(chapter)}<div class="asteroid-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Đừng bao giờ dừng lại em nhé!</p><button type="button" id="asteroid-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="asteroid-spread-banner"><img src="assets/asteroid-spread-v1.webp" width="1638" height="342" alt="A woman on a small planet, an orbit, coworkers, a cafe table, a bench, a house, suitcase and sunset."><figcaption>Orbit / Work / Connection / Distance</figcaption></figure>`
    :id==='07'
    ?`<header class="old-friend-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="old-friend-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.title)}</h1><p class="old-friend-chapter-subtitle">Childhood / Friendship / Memory / Distance</p><p class="old-friend-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="old-friend-chapter-stage">${chapterArtwork(chapter)}<div class="old-friend-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Và tớ vẫn nhớ gói chíp chíp ngày hôm ấy.</p><button type="button" id="old-friend-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="old-friend-spread-banner"><img src="assets/old-friend-spread-v1.webp" width="1638" height="342" alt="Two childhood friends, a packet of candy, a game console, school papers, an apology and a gate."><figcaption>Childhood / Friendship / Memory / Distance</figcaption></figure>`
    :id==='06'
    ?`<header class="red-button-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="red-button-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.title)}</h1><p class="red-button-chapter-subtitle">Call / Deadline / Family / Memory</p><p class="red-button-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="red-button-chapter-stage">${chapterArtwork(chapter)}<div class="red-button-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Tôi chỉ biết mình vẫn nhớ.</p><button type="button" id="red-button-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="red-button-spread-banner"><img src="assets/red-button-spread-v1.webp" width="1638" height="342" alt="A phone, dog, airport, parents, childhood study desk, paperwork and clock from the Red Button artwork."><figcaption>Call / Deadline / Family / Memory</figcaption></figure>`
    :id==='20'
    ?`<header class="dating-102-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="dating-102-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.title)}</h1><p class="dating-102-chapter-subtitle">Curiosity / Intimacy / Signaling / Compatibility</p><p class="dating-102-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="dating-102-chapter-stage">${chapterArtwork(chapter)}<div class="dating-102-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Better questions lead to deeper people, and a better you.</p><button type="button" id="dating-102-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="dating-102-spread-banner"><img src="assets/dating-102-spread-v2.webp" width="1600" height="764" alt="Two people lean over a shared notebook in a warm room overlooking the night city."><figcaption>Curiosity / Intimacy / Signaling / Compatibility</figcaption></figure>`
    :id==='19'
    ?`<header class="dating-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="dating-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.title)}</h1><p class="dating-chapter-subtitle">Matching / Signaling / Compatibility / Strategy</p><p class="dating-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="dating-chapter-stage">${chapterArtwork(chapter)}<div class="dating-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Some matches are math.<br>Some are timing.<br>The rare ones are both.</p><button type="button" id="dating-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="dating-spread-banner"><img src="assets/dating-algorithm-spread-v2.webp" width="1600" height="600" alt="A date table, profile card, chat, compatibility graph, coffee, invitation and moonlit city from the chapter artwork."><figcaption>Matching / Signaling / Compatibility / Strategy</figcaption></figure>`
    :id==='11'
    ?`<header class="coincidence-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="coincidence-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.title)}</h1><p class="coincidence-chapter-subtitle">Time / Paths / Chance / Attention</p><p class="coincidence-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="coincidence-chapter-stage">${chapterArtwork(chapter)}<div class="coincidence-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Maybe it's all random.<br>Maybe I'm just paying more attention.</p><button type="button" id="coincidence-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="coincidence-spread-banner"><img src="assets/coincidence-spread-v1.webp" width="1600" height="1186" alt="Golden paths converge on a lamplit bookshop beneath stars, with autumn trees and a clock nearby."><figcaption>Time / Paths / Chance / Attention</figcaption></figure>`
    :id==='14'
    ?`<header class="saigon-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="saigon-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.title)}</h1><p class="saigon-chapter-subtitle">Arrival / Belonging / Friendship / Home</p><p class="saigon-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="saigon-chapter-stage">${chapterArtwork(chapter)}<div class="saigon-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Sài Gòn cho t nhiều thứ quá, chẳng biết nói gì hơn ngoài cảm ơn.</p><button type="button" id="saigon-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="saigon-spread-banner"><img src="assets/saigon-spread-v1.webp" width="1600" height="1132" alt="Two people and a small dog look toward Ba Son Bridge and the Saigon skyline at sunset."><figcaption>One city. Many versions of belonging.</figcaption></figure>`
    :id==='18'
    ?`<header class="meeting-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="meeting-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.title)}</h1><p class="meeting-chapter-subtitle">Destiny / Timing / Reunion / Romance</p><p class="meeting-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="meeting-chapter-stage">${chapterArtwork(chapter)}<div class="meeting-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Some people return like destiny.</p><button type="button" id="meeting-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="meeting-spread-banner"><img src="assets/three-meeting-spread-v2.webp" width="1600" height="600" alt="Two people meet near a flower-lined cafe, with a bridge and city skyline beyond."><figcaption>A crowd / A glance / Another time</figcaption></figure>`
    :id==='09'
    ?`<header class="dream-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} / CHAPTER ${id}</p><p class="dream-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.title)}</h1><p class="dream-chapter-subtitle">Memory / Journey / Imagination / Home</p><p class="dream-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="dream-chapter-stage">${chapterArtwork(chapter)}<div class="dream-chapter-note"><span>A VISUAL INTRODUCTION</span><p>A train to Bastille.<br>A conversation overheard.<br>A family dinner imagined.</p><button type="button" id="dream-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="dream-spread-banner"><img src="assets/dream-world-spread-v2.webp" width="1600" height="520" alt="Jason with two suitcases, a Metro train, two children, and a warmly lit family dinner seen through a window."><figcaption>Observed / Imagined / Remembered</figcaption></figure>`
    :id==='08'
    ?`<header class="russia-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} · CHAPTER ${id}</p><p class="russia-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.title)}</h1><p class="russia-chapter-subtitle">Memory / Nostalgia / War / Dream</p><p class="russia-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="russia-chapter-stage">${chapterArtwork(chapter)}<div class="russia-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Some homelands are inherited through stories.</p><button type="button" id="russia-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="russia-cabin-banner"><img src="assets/mother-russia-cabin-v2.webp" width="240" height="150" alt="A wooden cabin glows beside the water amid snowy pines beneath a winter moon."><figcaption>Memory / Nostalgia / War / Dream</figcaption></figure>`
    :id==='00'
    ?`<header class="rice-chapter-heading"><p class="leaf-kicker">PROLOGUE · ${id}</p><p class="rice-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.title)}</h1><p class="rice-chapter-subtitle">Memory / Family / Childhood / Home</p>${sourceTitle}</header><div class="rice-chapter-stage">${chapterArtwork(chapter)}<div class="rice-chapter-note"><span>A VISUAL INTRODUCTION</span><p>A bowl of cold rice, a warm home, and the people who made ordinary nights feel like everything.</p><button type="button" id="rice-read">Read the prologue <span aria-hidden="true">↓</span></button></div></div><figure class="rice-room-banner"><img src="assets/rice-family-room-v2.webp?v=2" alt="A family shares dinner in a warm room overlooking the city."><figcaption>Memory / Family / Childhood / Home</figcaption></figure>`
    :id==='02'
    ?`<header class="utility-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} · CHAPTER ${id}</p><p class="utility-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.shortTitle)}</h1><p class="utility-chapter-subtitle">Decision / Probability / Emotion</p><p class="utility-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="utility-chapter-stage">${chapterArtwork(chapter)}<div class="utility-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Different outcomes.<br>Same uncertainty.<br>Still you.</p><button type="button" id="utility-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="utility-spread-banner"><img src="assets/expected-utility-gaze-v3.webp" alt="A woman's eyes framed by choices, a heart, scales, code, a letter and branching paths."><figcaption>Decision / Probability / Emotion</figcaption></figure>`
    :id==='03'
    ?`<header class="play-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} · CHAPTER ${id}</p><p class="play-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.title)}</h1><p class="play-chapter-subtitle">Game Theory / Decision / Relationship / Trade-off</p><p class="play-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="play-chapter-stage">${chapterArtwork(chapter)}<div class="play-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Different players.<br>Different incentives.<br>Same game.<br>Choose well.</p><button type="button" id="play-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="play-table-banner"><img src="assets/play-to-win-table-v2.webp" alt="Cards, poker chips and mahjong tiles on a lamplit game table."><figcaption>Different players. Different incentives.</figcaption></figure>`
    :id==='04'
    ?`<header class="fashion-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} · CHAPTER ${id}</p><p class="fashion-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">${esc(chapter.shortTitle)}</h1><p class="fashion-chapter-subtitle">Be Your Own Label</p><p class="fashion-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="fashion-chapter-stage">${chapterArtwork(chapter)}<div class="fashion-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Street corners, shoeboxes, hand-me-downs, and new dreams.</p><button type="button" id="fashion-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="fashion-room-banner"><img src="assets/fashion-room-v2.webp" alt="A sunset-lit room filled with a sneaker, shoeboxes, hanging clothes, photographs and plants."><figcaption>Same objects. Different worlds.</figcaption></figure>`
    :id==='05'
    ?`<header class="flow-chapter-heading"><p class="leaf-kicker">PART ${roman[part.id]} · CHAPTER ${id}</p><p class="flow-chapter-numeral">${id}</p><h1 id="chapter-heading" tabindex="-1">FLOW</h1><p class="flow-chapter-subtitle">The Secret of Wealth</p><p class="flow-chapter-part">${esc(partLabel(part))}</p>${sourceTitle}</header><div class="flow-chapter-stage">${chapterArtwork(chapter)}<div class="flow-chapter-note"><span>A VISUAL INTRODUCTION</span><p>Money is like water.<br>Wealth is the reservoir.<br>Cash flow is the river.</p><button type="button" id="flow-read">Read the chapter <span aria-hidden="true">↓</span></button></div></div><figure class="flow-spread-banner"><img src="assets/flow-spread-v2.webp" width="1600" height="480" alt="Jason, coins, a reservoir, waterwheel, homes, a seedling and a bridge from the Flow illustration."><figcaption>Income / Assets / Consumption / Cash flow</figcaption></figure>`
    :`<header class="chapter-heading"><p class="leaf-kicker">${part?`PART ${roman[part.id]}`:'.JSON / JASON, UNDER REVISION'}</p><p class="chapter-numeral">${headingLabel}</p><h1 id="chapter-heading" class="chapter-title" tabindex="-1">${esc(chapter.title)}</h1>${part?`<p class="chapter-part-title">${esc(partLabel(part))}</p>`:''}${sourceTitle}</header>${chapterArtwork(chapter)}`;
  const quantSpread=id==='01'?`<figure class="quant-reading-spread"><img src="assets/quant-reading-spread-v2.webp" width="540" height="265" alt="Jason studies charts at his desk with a dog beside him and a note about minimizing loss."><figcaption>Same objective. Same potential. Different risk budget.</figcaption></figure>`:'';
  $('#chapter-leaf').innerHTML=`${opening}${quantSpread}${id==='10'?`<div id="dream-diary-chapter-text">${text}</div>`:id==='13'?`<div id="my-brothers-chapter-text">${text}</div>`:id==='15'?`<div id="twenty-eight-today-chapter-text">${text}</div>`:id==='23'?`<div id="ugly-projections-chapter-text">${text}</div>`:id==='34'?`<div id="after-leaving-chapter-text">${text}</div>`:id==='32'?`<div id="command-respect-chapter-text">${text}</div>`:id==='30'?`<div id="negative-sum-chapter-text">${text}</div>`:id==='29'?`<div id="moral-chapter-text">${text}</div>`:id==='28'?`<div id="good-chapter-text">${text}</div>`:id==='27'?`<div id="record-chapter-text">${text}</div>`:id==='26'?`<div id="better-chapter-text">${text}</div>`:id==='25'?`<div id="payoff-chapter-text">${text}</div>`:id==='24'?`<div id="office-chapter-text">${text}</div>`:id==='16'?`<div id="bad-trip-chapter-text">${text}</div>`:id==='22'?`<div id="runaway-chapter-text">${text}</div>`:id==='17'?`<div id="asteroid-chapter-text">${text}</div>`:id==='07'?`<div id="old-friend-chapter-text">${text}</div>`:id==='06'?`<div id="red-button-chapter-text">${text}</div>`:id==='11'?`<div id="coincidence-chapter-text">${text}</div>`:id==='14'?`<div id="saigon-chapter-text">${text}</div>`:id==='20'?`<div id="dating-102-chapter-text">${text}</div>`:id==='19'?`<div id="dating-chapter-text">${text}</div>`:id==='18'?`<div id="meeting-chapter-text">${text}</div>`:id==='09'?`<div id="dream-chapter-text">${text}</div>`:id==='08'?`<div id="russia-chapter-text">${text}</div>`:id==='00'?`<div id="rice-chapter-text">${text}</div>`:id==='02'?`<div id="utility-chapter-text">${text}</div>`:id==='03'?`<div id="play-chapter-text">${text}</div>`:id==='04'?`<div id="fashion-chapter-text">${text}</div>`:id==='05'?`<div id="flow-chapter-text">${text}</div>`:text}${chapterFooter(chapter)}`;
  if(id==='10')$('#dream-diary-read').addEventListener('click',()=>$('#dream-diary-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='13')$('#my-brothers-read').addEventListener('click',()=>$('#my-brothers-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='15')$('#twenty-eight-today-read').addEventListener('click',()=>$('#twenty-eight-today-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='23')$('#ugly-projections-read').addEventListener('click',()=>$('#ugly-projections-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='34')$('#after-leaving-read').addEventListener('click',()=>$('#after-leaving-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='32')$('#command-respect-read').addEventListener('click',()=>$('#command-respect-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='30')$('#negative-sum-read').addEventListener('click',()=>$('#negative-sum-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='29')$('#moral-read').addEventListener('click',()=>$('#moral-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='28')$('#good-read').addEventListener('click',()=>$('#good-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='27')$('#record-read').addEventListener('click',()=>$('#record-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='26')$('#better-read').addEventListener('click',()=>$('#better-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='25')$('#payoff-read').addEventListener('click',()=>$('#payoff-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='24')$('#office-read').addEventListener('click',()=>$('#office-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='16')$('#bad-trip-read').addEventListener('click',()=>$('#bad-trip-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='22')$('#runaway-read').addEventListener('click',()=>$('#runaway-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='17')$('#asteroid-read').addEventListener('click',()=>$('#asteroid-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='07')$('#old-friend-read').addEventListener('click',()=>$('#old-friend-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='06')$('#red-button-read').addEventListener('click',()=>$('#red-button-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='11')$('#coincidence-read').addEventListener('click',()=>$('#coincidence-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='14')$('#saigon-read').addEventListener('click',()=>$('#saigon-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='20')$('#dating-102-read').addEventListener('click',()=>$('#dating-102-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='19')$('#dating-read').addEventListener('click',()=>$('#dating-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='18')$('#meeting-read').addEventListener('click',()=>$('#meeting-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='09')$('#dream-read').addEventListener('click',()=>$('#dream-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='08')$('#russia-read').addEventListener('click',()=>$('#russia-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='00')$('#rice-read').addEventListener('click',()=>$('#rice-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='02')$('#utility-read').addEventListener('click',()=>$('#utility-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='03')$('#play-read').addEventListener('click',()=>$('#play-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='04')$('#fashion-read').addEventListener('click',()=>$('#fashion-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
  if(id==='05')$('#flow-read').addEventListener('click',()=>$('#flow-chapter-text').scrollIntoView({behavior:reducedMotion?'instant':'smooth'}));
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
  const fittedRing={'00':'assets/rice-ring-board-v2.png','01':'assets/quant-ring.png','02':'assets/expected-utility-ring-v3.png','03':'assets/play-to-win-ring-v2.png','04':'assets/fashion-ring-v2.png','05':'assets/flow-ring-v2.png','06':'assets/red-button-ring-v1.png','07':'assets/old-friend-ring-v1.png','08':'assets/mother-russia-ring-v2.png','09':'assets/dream-world-ring-v2.png','11':'assets/coincidence-ring-v1.png','14':'assets/saigon-ring-v1.png','16':'assets/bad-trip-ring-v1.png','24':'assets/office-battlefield-ring-v1.png','25':'assets/payoff-matrix-ring-v1.png','26':'assets/better-brighter-ring-v1.png','27':'assets/record-keeping-ring-v1.png','28':'assets/good-boy-ring-v1.png','29':'assets/moral-story-ring-v1.png','30':'assets/negative-sum-ring-v1.png','32':'assets/command-respect-ring-v1.png','10':'assets/dream-diary-ring-v1.png','13':'assets/my-brothers-ring-v1.png','15':'assets/twenty-eight-today-ring-v1.png','23':'assets/ugly-projections-ring-v1.png','34':'assets/after-leaving-ring-v1.png','17':'assets/asteroid-ring-v1.png','22':'assets/runaway-ring-v1.png','18':'assets/three-meeting-ring-v2.png?v=4','19':'assets/dating-algorithm-ring-v2.png','20':'assets/dating-102-ring-v2.png'}[chapter.id];
  const fitted=Boolean(fittedRing);
  const pictureKey=chapter.id==='01'?'quant':chapter.id==='02'?'expectedUtility':chapter.id==='03'?'playToWin':chapter.id==='04'?'fashion':chapter.id==='05'?'flow':chapter.id==='06'?'redButton':chapter.id==='07'?'oldFriend':chapter.id==='08'?'motherRussia':chapter.id==='09'?'dreamWorld':chapter.id==='11'?'coincidence':chapter.id==='14'?'saigon':chapter.id==='16'?'badTrip':chapter.id==='24'?'officeBattlefield':chapter.id==='25'?'payoffMatrix':chapter.id==='26'?'betterBrighter':chapter.id==='27'?'recordKeeping':chapter.id==='28'?'goodBoy':chapter.id==='10'?'dreamDiary':chapter.id==='13'?'myBrothers':chapter.id==='15'?'twentyEightToday':chapter.id==='23'?'uglyProjections':chapter.id==='34'?'afterLeaving':chapter.id==='32'?'commandRespect':chapter.id==='30'?'negativeSum':chapter.id==='29'?'moralStory':chapter.id==='17'?'asteroid':chapter.id==='22'?'runaway':chapter.id==='18'?'threeMeeting':chapter.id==='19'?'datingAlgorithm':chapter.id==='20'?'dating102':'rice';
  $('#portal-art').classList.toggle('uses-fitted-picture',fitted);
  $('#portal-scene').innerHTML=fitted?renderPortalPicture(pictureKey):artHTML(chapter);
  $('#portal-rim-art').innerHTML=fitted?renderPortalFrame(`${pictureKey}-map`,fittedRing):artHTML(chapter);
  $('#portal-marker').innerHTML=renderChapterMarker(chapter);
  $('#portal-marker').setAttribute('aria-label',`Chapter marker ${chapter.id}: ${getChapterMarkerName(chapter)}`);
  $('#portal-stage').setAttribute('aria-label',`${chapter.id}. ${chapter.title}. Drag to rotate; use arrow keys to choose; Enter to read.`);
  $('#map-part').textContent=part?`PART ${roman[part.id]} · ${partLabel(part)}`:'PROLOGUE';
  $('#map-number').textContent=chapter.id;$('#map-title').textContent=['02','03','04','10','24','25','26','27','28','29','30','32','34'].includes(chapter.id)?chapter.shortTitle:chapter.title;
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
  // These supplied collages turn while dragging, then face upright at their
  // selected stops so the centre artwork joins the paper layers again.
  const base=dragging?(ring?.drag?.startRotation ?? rotation):rotation;
  $('#portal-rim-art').style.transform=['06','07','11','14','16','17','18','19','20','22','24','25','26','27','28'].includes(chapters[selectedMapChapter].id)?`rotate(${-base}deg)`:'';
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
  ...chapters.map(chapter=>({kind:'chapter', label:chapter.id, title:chapter.id==='10'?chapter.shortTitle:chapter.title, href:`#chapter/${chapter.id}`, chapter}))
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
    content.innerHTML=chapter.id==='10'
      ?`<div class="cover-reader-page dream-diary-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="dream-diary-reader-number">${chapter.id}</span><h2>Dream Diary</h2><p class="dream-diary-reader-subtitle">The Things We Never Saved</p><figure class="dream-diary-reader-scene"><img src="assets/dream-diary-spread-v1.webp" width="1632" height="309" alt="An open diary, metro train, two people holding hands, sketches and remembered rooms."><figcaption>Nhưng rồi đoàn tàu tới. Và tôi tỉnh dậy.</figcaption></figure>${body}</div>`
     :chapter.id==='13'
      ?`<div class="cover-reader-page my-brothers-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="my-brothers-reader-number">${chapter.id}</span><h2>My brothers</h2><figure class="my-brothers-reader-scene"><img src="assets/my-brothers-spread-v1.webp" width="1632" height="289" alt="Four former teammates, a glowing universe model, books, drinks, physics diagrams and a globe."><figcaption>where I belong</figcaption></figure>${body}</div>`
     :chapter.id==='15'
      ?`<div class="cover-reader-page twenty-eight-today-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="twenty-eight-today-reader-number">${chapter.id}</span><h2>I'm 28 today</h2><figure class="twenty-eight-today-reader-scene"><img src="assets/twenty-eight-today-spread-v1.webp" width="1632" height="289" alt="Jason, an open window, birthday cake, friends, camera, film frames, music and keepsakes."><figcaption>life is beautiful isn’t it</figcaption></figure>${body}</div>`
    :chapter.id==='23'
      ?`<div class="cover-reader-page ugly-projections-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="ugly-projections-reader-number">${chapter.id}</span><h2>Ugly Projections</h2><figure class="ugly-projections-reader-scene"><img src="assets/ugly-projections-spread-v1.webp" width="1632" height="289" alt="Jason, a film projector, projected silhouette, woman, lens, paintings and empty chairs."><figcaption>I kept seeing women as someone they weren't.</figcaption></figure>${body}</div>`
    :chapter.id==='34'
      ?`<div class="cover-reader-page after-leaving-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="after-leaving-reader-number">${chapter.id}</span><h2>Office Battlefield</h2><p class="after-leaving-reader-subtitle">Things You Only See After Leaving</p><figure class="after-leaving-reader-scene"><img src="assets/after-leaving-spread-v1.webp" width="1632" height="289" alt="Jason, an office whiteboard, phone, umbrella, mountains and farewell keepsakes."><figcaption>I matter here. I belong here.</figcaption></figure>${body}</div>`
    :chapter.id==='32'
      ?`<div class="cover-reader-page command-respect-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="command-respect-reader-number">${chapter.id}</span><h2>Office Battlefield</h2><p class="command-respect-reader-subtitle">Command Respect</p><figure class="command-respect-reader-scene"><img src="assets/command-respect-spread-v1.webp" width="1632" height="289" alt="Jason, a childhood mirror, office objects, boxing gloves, a work ticket, phone and a note from David."><figcaption>Those were my choices.</figcaption></figure>${body}</div>`
    :chapter.id==='30'
      ?`<div class="cover-reader-page negative-sum-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="negative-sum-reader-number">${chapter.id}</span><h2>Office Battlefield</h2><p class="negative-sum-reader-subtitle">Negative-Sum Game</p><figure class="negative-sum-reader-scene"><img src="assets/negative-sum-spread-v1.webp" width="1632" height="289" alt="Jason, opposing chess pieces, a cost ledger, chair, mugs and office records."><figcaption>I mistook that anger for strategy.</figcaption></figure>${body}</div>`
    :chapter.id==='29'
      ?`<div class="cover-reader-page moral-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="moral-reader-number">${chapter.id}</span><h2>Office Battlefield</h2><p class="moral-reader-subtitle">The Moral Story Schools Don't Teach You</p><figure class="moral-reader-scene"><img src="assets/moral-story-spread-v1.webp" width="1632" height="289" alt="Jason, a moral-model book, draft, mirror, compass and office records."><figcaption>Implementation? Not so much.</figcaption></figure>${body}</div>`
      :chapter.id==='28'
      ?`<div class="cover-reader-page good-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="good-reader-number">${chapter.id}</span><h2>Office Battlefield</h2><p class="good-reader-subtitle">Good Boy</p><figure class="good-reader-scene"><img src="assets/good-boy-spread-v1.webp" width="1632" height="289" alt="Jason, a Good Boy stamp, an apology letter, phone, clock and conversation objects."><figcaption>You're a nice guy, don't be mean.</figcaption></figure>${body}</div>`
      :chapter.id==='27'
      ?`<div class="cover-reader-page record-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="record-reader-number">${chapter.id}</span><h2>Office Battlefield</h2><p class="record-reader-subtitle">Masterclass in Record Keeping</p><figure class="record-reader-scene"><img src="assets/record-keeping-spread-v1.webp" width="1632" height="289" alt="Jason, an AI assistant, an open record log, files, a clock and magnifying glass."><figcaption>Version history. Timestamp. Event log. Provenance. Evidence.</figcaption></figure>${body}</div>`
      :chapter.id==='26'
      ?`<div class="cover-reader-page better-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="better-reader-number">${chapter.id}</span><h2>Office Battlefield</h2><p class="better-reader-subtitle">Better and Brighter Than Ever</p><figure class="better-reader-scene"><img src="assets/better-brighter-spread-v1.webp" width="1632" height="289" alt="Jason walks toward an eye-shaped doorway between two jerseys, with gifts, mugs, desks and an empty chair nearby."><figcaption>Better and brighter than ever.</figcaption></figure>${body}</div>`
      :chapter.id==='25'
      ?`<div class="cover-reader-page payoff-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="payoff-reader-number">${chapter.id}</span><h2>Office Battlefield</h2><p class="payoff-reader-subtitle">The Payoff Matrix</p><figure class="payoff-reader-scene"><img src="assets/payoff-matrix-spread-v1.webp" width="1632" height="289" alt="Jason, an AI agent, scorecards, payoff grid, chess pieces and a phone."><figcaption>Game over. Checkmate.</figcaption></figure>${body}</div>`
      :chapter.id==='24'
      ?`<div class="cover-reader-page office-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="office-reader-number">${chapter.id}</span><h2>Office Battlefield</h2><p class="office-reader-subtitle">The 23-Word Nuclear Warhead</p><figure class="office-reader-scene"><img src="assets/office-battlefield-spread-v1.webp" width="1632" height="327" alt="Jason, a paper message, chess pieces, an AI agent and office objects."><figcaption>All in one Slack message.</figcaption></figure>${body}</div>`
      :chapter.id==='16'
      ?`<div class="cover-reader-page bad-trip-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="bad-trip-reader-number">${chapter.id}</span><h2>${esc(chapter.title)}</h2><p class="bad-trip-reader-subtitle">Identity / Memory / Work / Return</p><figure class="bad-trip-reader-scene"><img src="assets/bad-trip-spread-v1.webp" width="1632" height="321" alt="A mirror, two versions of Jason, old photographs, work desk and suitcase."><figcaption>I just wanted to be Jason.</figcaption></figure>${body}</div>`
      :chapter.id==='22'
      ?`<div class="cover-reader-page runaway-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="runaway-reader-number">${chapter.id}</span><h2>${esc(chapter.title)}</h2><p class="runaway-reader-subtitle">Drawing / Music / Care / Distance</p><figure class="runaway-reader-scene"><img src="assets/runaway-spread-v1.webp" width="1632" height="336" alt="Jason, a woman, Gấu, an open doorway, sofa, drawing tablet, headphones and music."><figcaption>A chỉ muốn ở đó.</figcaption></figure>${body}</div>`
      :chapter.id==='17'
      ?`<div class="cover-reader-page asteroid-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="asteroid-reader-number">${chapter.id}</span><h2>${esc(chapter.title)}</h2><p class="asteroid-reader-subtitle">Orbit / Work / Connection / Distance</p><figure class="asteroid-reader-scene"><img src="assets/asteroid-spread-v1.webp" width="1638" height="342" alt="A woman on a small planet, an orbit, coworkers, a cafe table, a bench, a house, suitcase and sunset."><figcaption>Đừng bao giờ dừng lại em nhé!</figcaption></figure>${body}</div>`
      :chapter.id==='07'
      ?`<div class="cover-reader-page old-friend-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="old-friend-reader-number">${chapter.id}</span><h2>${esc(chapter.title)}</h2><p class="old-friend-reader-subtitle">Childhood / Friendship / Memory / Distance</p><figure class="old-friend-reader-scene"><img src="assets/old-friend-spread-v1.webp" width="1638" height="342" alt="Two childhood friends, a packet of candy, a game console, school papers, an apology and a gate."><figcaption>Và tớ vẫn nhớ gói chíp chíp ngày hôm ấy.</figcaption></figure>${body}</div>`
      :chapter.id==='06'
      ?`<div class="cover-reader-page red-button-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="red-button-reader-number">${chapter.id}</span><h2>${esc(chapter.title)}</h2><p class="red-button-reader-subtitle">Call / Deadline / Family / Memory</p><figure class="red-button-reader-scene"><img src="assets/red-button-spread-v1.webp" width="1638" height="342" alt="A phone, dog, airport, parents, childhood study desk, paperwork and clock."><figcaption>Tôi chỉ biết mình vẫn nhớ.</figcaption></figure>${body}</div>`
      :chapter.id==='20'
      ?`<div class="cover-reader-page dating-102-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="dating-102-reader-number">${chapter.id}</span><h2>${esc(chapter.title)}</h2><p class="dating-102-reader-subtitle">Curiosity / Intimacy / Signaling / Compatibility</p><figure class="dating-102-reader-scene"><img src="assets/dating-102-spread-v2.webp" width="1600" height="764" alt="Two people share a notebook in a warm room facing a night skyline."><figcaption>Better questions lead to deeper people.</figcaption></figure>${body}</div>`
      :chapter.id==='19'
      ?`<div class="cover-reader-page dating-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="dating-reader-number">${chapter.id}</span><h2>${esc(chapter.title)}</h2><p class="dating-reader-subtitle">Matching / Signaling / Compatibility / Strategy</p><figure class="dating-reader-scene"><img src="assets/dating-algorithm-spread-v2.webp" width="1600" height="600" alt="A date table, profile, messages, a compatibility graph and a moonlit city."><figcaption>Some matches are math. Some are timing.</figcaption></figure>${body}</div>`
      :chapter.id==='18'
      ?`<div class="cover-reader-page meeting-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="meeting-reader-number">${chapter.id}</span><h2>${esc(chapter.title)}</h2><p class="meeting-reader-subtitle">Destiny / Timing / Reunion / Romance</p><figure class="meeting-reader-scene"><img src="assets/three-meeting-spread-v2.webp" width="1600" height="600" alt="Two people meet near a flower-lined cafe, with a bridge and city skyline beyond."><figcaption>Some people return like destiny.</figcaption></figure>${body}</div>`
      :chapter.id==='11'
      ?`<div class="cover-reader-page coincidence-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="coincidence-reader-number">${chapter.id}</span><h2>${esc(chapter.title)}</h2><p class="coincidence-reader-subtitle">Time / Paths / Chance / Attention</p><figure class="coincidence-reader-scene"><img src="assets/coincidence-spread-v1.webp" width="1600" height="1186" alt="Golden paths converge on a lamplit bookshop beneath a starry sky."><figcaption>Maybe it's all random. Maybe I'm just paying more attention.</figcaption></figure>${body}</div>`
      :chapter.id==='14'
      ?`<div class="cover-reader-page saigon-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} · CHAPTER ${chapter.id}</p><span class="saigon-reader-number">${chapter.id}</span><h2>${esc(chapter.title)}</h2><p class="saigon-reader-subtitle">Arrival / Belonging / Friendship / Home</p><figure class="saigon-reader-scene"><img src="assets/saigon-spread-v1.webp" width="1600" height="1132" alt="A couple and small dog look over Ba Son Bridge and the Saigon skyline at sunset."><figcaption>One city. Many versions of belonging.</figcaption></figure>${body}</div>`
      :chapter.id==='09'
      ?`<div class="cover-reader-page dream-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} / CHAPTER ${chapter.id}</p><span class="dream-reader-number">${chapter.id}</span><h2>${esc(chapter.title)}</h2><p class="dream-reader-subtitle">Memory / Journey / Imagination / Home</p><figure class="dream-reader-scene"><img src="assets/dream-world-spread-v2.webp" width="1600" height="520" alt="Jason with two suitcases, a Metro train, two children, and a warm family dinner seen through a window."><figcaption>Observed / Imagined / Remembered</figcaption></figure>${body}</div>`
      :chapter.id==='08'
      ?`<div class="cover-reader-page russia-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} · CHAPTER ${chapter.id}</p><span class="russia-reader-number">${chapter.id}</span><h2>${esc(chapter.title)}</h2><p class="russia-reader-subtitle">Memory / Nostalgia / War / Dream</p><figure class="russia-reader-scene"><img src="assets/mother-russia-cabin-v2.webp" width="240" height="150" alt="A wooden cabin glows beside the water amid snowy pines beneath a winter moon."><figcaption>Some homelands are inherited through stories.</figcaption></figure>${body}</div>`
      :chapter.id==='01'
      ?`<div class="cover-reader-page quant-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} · CHAPTER ${chapter.id}</p><h2>${esc(chapter.title)}</h2><p class="cover-reader-part">${esc(partLabel(part))}</p><figure class="cover-reader-illustration"><img src="assets/quant-reading-spread-v2.webp" width="540" height="265" alt="Jason studies charts at his desk with a dog beside him and a note about minimizing loss."><figcaption>Same objective. Same potential. Different risk budget.</figcaption></figure>${body}</div>`
      :chapter.id==='00'
      ?`<div class="cover-reader-page rice-reader-page"><p class="cover-reader-kicker">PROLOGUE · ${chapter.id}</p><span class="rice-reader-number">${chapter.id}</span><h2>${esc(chapter.title)}</h2><p class="rice-reader-subtitle">Memory / Family / Childhood / Home</p><figure class="rice-reader-scene"><img src="assets/rice-family-room-v2.webp?v=2" alt="A family shares dinner in a warm room overlooking the city."><figcaption>The same table. The same bowl. A thousand versions of home.</figcaption></figure>${body}</div>`
      :chapter.id==='02'
      ?`<div class="cover-reader-page utility-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} · CHAPTER ${chapter.id}</p><span class="utility-reader-number">${chapter.id}</span><h2>${esc(chapter.shortTitle)}</h2><p class="utility-reader-subtitle">Decision / Probability / Emotion</p><figure class="utility-reader-scene"><img src="assets/expected-utility-gaze-v3.webp" alt="A woman's eyes framed by choices, a heart, scales, code, a letter and branching paths."><figcaption>Different outcomes. Same uncertainty. Still you.</figcaption></figure>${body}</div>`
      :chapter.id==='03'
      ?`<div class="cover-reader-page play-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} · CHAPTER ${chapter.id}</p><span class="play-reader-number">${chapter.id}</span><h2>${esc(chapter.title)}</h2><p class="play-reader-subtitle">Game Theory / Decision / Relationship / Trade-off</p><figure class="play-reader-scene"><img src="assets/play-to-win-table-v2.webp" alt="A warm lamp above cards, chips and mahjong tiles on a game table."><figcaption>Different players. Different incentives. Same game.</figcaption></figure>${body}</div>`
      :chapter.id==='04'
      ?`<div class="cover-reader-page fashion-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} · CHAPTER ${chapter.id}</p><span class="fashion-reader-number">${chapter.id}</span><h2>${esc(chapter.shortTitle)}</h2><p class="fashion-reader-subtitle">Be Your Own Label</p><figure class="fashion-reader-scene"><img src="assets/fashion-room-v2.webp" alt="A sneaker and lived-in wardrobe in a room overlooking the city."><figcaption>Same objects. Different worlds.</figcaption></figure>${body}</div>`
      :chapter.id==='05'
      ?`<div class="cover-reader-page flow-reader-page"><p class="cover-reader-kicker">PART ${roman[part.id]} · CHAPTER ${chapter.id}</p><span class="flow-reader-number">${chapter.id}</span><h2>FLOW</h2><p class="flow-reader-subtitle">The Secret of Wealth</p><figure class="flow-reader-scene"><img src="assets/flow-spread-v2.webp" width="1600" height="480" alt="Jason, coins, reservoir, waterwheel, houses, trees and bridge from the Flow illustration."><figcaption>Money is like water. Cash flow is the river.</figcaption></figure>${body}</div>`
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
  $('#cover-scene').innerHTML=page.kind==='chapter'?(page.chapter.id==='00'?renderPortalPicture('rice'):page.chapter.id==='01'?renderPortalPicture('quant'):page.chapter.id==='02'?renderPortalPicture('expectedUtilityCover'):page.chapter.id==='03'?renderPortalPicture('playToWin'):page.chapter.id==='04'?renderPortalPicture('fashion'):page.chapter.id==='05'?renderPortalPicture('flowCover'):page.chapter.id==='06'?renderPortalPicture('redButtonCover'):page.chapter.id==='07'?renderPortalPicture('oldFriendCover'):page.chapter.id==='08'?renderPortalPicture('motherRussiaCover'):page.chapter.id==='09'?renderPortalPicture('dreamWorldCover'):page.chapter.id==='11'?renderPortalPicture('coincidenceCover'):page.chapter.id==='14'?renderPortalPicture('saigonCover'):page.chapter.id==='16'?renderPortalPicture('badTripCover'):page.chapter.id==='24'?renderPortalPicture('officeBattlefieldCover'):page.chapter.id==='25'?renderPortalPicture('payoffMatrixCover'):page.chapter.id==='26'?renderPortalPicture('betterBrighterCover'):page.chapter.id==='27'?renderPortalPicture('recordKeepingCover'):page.chapter.id==='28'?renderPortalPicture('goodBoyCover'):page.chapter.id==='10'?renderPortalPicture('dreamDiaryCover'):page.chapter.id==='13'?renderPortalPicture('myBrothersCover'):page.chapter.id==='15'?renderPortalPicture('twentyEightTodayCover'):page.chapter.id==='23'?renderPortalPicture('uglyProjectionsCover'):page.chapter.id==='34'?renderPortalPicture('afterLeavingCover'):page.chapter.id==='32'?renderPortalPicture('commandRespectCover'):page.chapter.id==='30'?renderPortalPicture('negativeSumCover'):page.chapter.id==='29'?renderPortalPicture('moralStoryCover'):page.chapter.id==='17'?renderPortalPicture('asteroidCover'):page.chapter.id==='22'?renderPortalPicture('runawayCover'):page.chapter.id==='18'?renderPortalPicture('threeMeetingCover'):page.chapter.id==='19'?renderPortalPicture('datingAlgorithmCover'):page.chapter.id==='20'?renderPortalPicture('dating102Cover'):renderPortalScene(page.chapter)):page.kind==='cover'
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
