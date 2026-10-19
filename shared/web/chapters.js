import { chapters, acts } from './chapter-data.js?v=17';
export { chapters, acts };

const iconPaths = {
  bowl:'M3 10h18c-1 7-5 10-9 10S4 17 3 10ZM5 6c2-3 3 2 5-1m4 0c2-3 3 2 5-1',
  chart:'M4 3v17h17M7 15l4-6 4 3 5-7M7 5h1m9 13h1',
  laptop:'M5 4h14v12H5zM2 20h20l-3-4H5zM8 8l-2 2 2 2m8-4 2 2-2 2',
  scales:'M12 2v19M5 6h14M4 21h16M5 6 2 14h6L5 6Zm14 0-3 8h6l-3-8Z',
  tile:'M6 2h12v20H6zM10 7h4m-4 5h4m-4 5h4',
  sneaker:'M3 14l4-7 5 5 5 1 4 3v4H3zM3 17h18M10 11l-2 2m5-1-2 2',
  key:'M10 9a4 4 0 1 1-8 0 4 4 0 0 1 8 0ZM10 9h12m-4 0v4m-4-4v3',
  phone:'M5 3c-5 10 4 19 14 17l2-4-5-3-3 3-5-5 2-3-3-5z',
  toy:'M5 10h13v9H5zM9 6h5v4m-8 9v3m10-3v3M18 12h4m-1-2v4M7 13h1m5 0h1',
  candy:'M5 3h14v18H5zM5 8c4 2 10 2 14 0M9 12a2 2 0 1 0 0 4 2 2 0 0 0 0-4Zm6 1a2 2 0 1 0 0 4 2 2 0 0 0 0-4Z',
  pine:'M12 2L5 11h4l-6 7h7v4h4v-4h7l-6-7h4z',
  metro:'M5 3h14v15H5zM8 6h8v6H8zM8 16h1m6 0h1M5 22l3-4m8 0 3 4',
  notebook:'M3 4c4-2 6-2 9 0 3-2 5-2 9 0v16c-4-2-6-2-9 0-3-2-5-2-9 0zM12 4v16M6 8h3m6 0h3',
  clock:'M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0ZM12 6v6l4 2M12 3v1m0 16v1M3 12h1m16 0h1',
  star:'M12 2l3 6 7 1-5 5 1 8-6-4-6 4 1-8-5-5 7-1z',
  van:'M3 6h14l4 6v7H3zM4 10h12V7M17 11h3M5 19a2 2 0 1 0 4 0m6 0a2 2 0 1 0 4 0',
  bridge:'M2 19h20M6 19V4m12 15V4M2 15l4-9 6 8 6-8 4 9M3 15v4m6-8v8m6-8v8m6-4v4',
  cake:'M3 11h18v10H3zM3 14c3 5 4-3 7 0s4-3 7 0 3 2 4 0M7 11V7m5 4V6m5 5V7M7 4v1m5-3v1m5 1v1',
  asteroid:'M17 3l-9 7M21 7l-8 8M11 13l-5 7M21 2l-7 7M14 14a5 5 0 1 1-10 0 5 5 0 0 1 10 0ZM7 13h1',
  paths:'M3 21 17 3M10 21 5 3M21 21 13 3M9 12h2m5 0h2',
  microphone:'M9 4a3 3 0 0 1 6 0v9a3 3 0 0 1-6 0zM5 11v2a7 7 0 0 0 14 0v-2M12 20v3m-4 0h8',
  heart:'M12 21 3.5 12.5C-1 8 5 1 12 7c7-6 13 1 8.5 5.5Z',
  envelope:'M2 5h20v15H2zM2 5l10 8L22 5M2 20l7-9m13 9-7-9',
  bed:'M3 8v14M21 8v14M3 18h18V9H3M6 9V6h6v3M3 14h18',
  mirror:'M6 2h12v16H6zM9 6l5 5m-3-6 4 4M12 18v4m-5 0h10',
  message:'M3 3h18v13H9l-6 6zM7 7h10m-10 4h6',
  jersey:'M8 3l-6 5 4 5 2-2v11h8V11l2 2 4-5-6-5c-1 4-7 4-8 0Z',
  search:'M16 10a6 6 0 1 1-12 0 6 6 0 0 1 12 0ZM15 15l7 7M7 7h4m-4 4h4',
  dialogue:'M2 3h13v9H7l-5 4zM18 8h4v14l-5-4H9v-3',
  counters:'M2 9h20M6 12v9m12-9v9M3 17l3 4 3-4m6 0 3 4 3-4M9 4h6',
  eye:'M2 12c5-9 15-9 20 0-5 9-15 9-20 0ZM16 12a4 4 0 1 1-8 0 4 4 0 0 1 8 0ZM12 10v4',
  door:'M5 22V2h14v20M9 3l7 3v16M12 13h1M3 22h18',
  dog:'M6 10 3 6l-1 9 5 2 1 5m9 0 1-6 4-5-4-5-4 3-5-2M10 11h1m6 0h1M9 17h8',
  mountain:'M2 21 9 7l4 7 3-11 6 18zM6 13l3 2 3-2m2-3 2 2 2-2',
  crescent:'M19 3a10 10 0 1 0 2 16C8 22 3 8 19 3Z',
};

const esc = value => String(value).replace(/[&<>"']/g, x => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));
export function renderIcon(chapterOrKey, size = 24) {
  const key = typeof chapterOrKey === 'string' ? chapterOrKey : chapterOrKey.iconKey;
  return `<svg viewBox="0 0 24 24" width="${Number(size)||24}" height="${Number(size)||24}" fill="none" stroke="currentColor" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="${iconPaths[key] || iconPaths.bowl}"/></svg>`;
}

const palettes = {
  0:['#dfb775','#af6d49','#d4b99b','#778b88','#c7ad79','#253e49'],
  1:['#dea786','#ad584a','#e6c9a0','#738b8c','#d0a16d','#294652'],
  2:['#c7a15c','#587f80','#d1b886','#b5674f','#d9c7a4','#243f4b'],
  3:['#ca9996','#7e536c','#d2ae9e','#a55c58','#dcbd99','#31364d'],
  4:['#ae604e','#3b5361','#c88a65','#997d68','#dcc2a2','#253641'],
  5:['#a4b59d','#547e7d','#d2bf9d','#9d8d75','#c6c6a9','#2b4851'],
};

const circle = (x,y,r,fill,stroke='none',sw=1) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/>`;
const rect = (x,y,w,h,fill,rx=0,stroke='none',sw=1) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/>`;
const path = (d,fill='none',stroke='none',sw=1) => `<path d="${d}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round"/>`;
const line = (x1,y1,x2,y2,stroke,sw=1) => `<path d="M${x1} ${y1}L${x2} ${y2}" fill="none" stroke="${stroke}" stroke-width="${sw}" stroke-linecap="round"/>`;
const txt = (x,y,text,size=12,fill='#e9d3ac',extra='') => `<text x="${x}" y="${y}" fill="${fill}" font-family="Georgia,serif" font-size="${size}" ${extra}>${esc(text)}</text>`;
function person(x,y,scale=1,color='#17303c',pose='stand') {
  return `<g transform="translate(${x} ${y}) scale(${scale})">${circle(0,0,9,color)}${path(pose==='sit'?'M-8 11Q0 5 9 12L12 39 32 40 32 48 3 49-6 25-12 40-19 38Z':'M-8 11Q0 7 8 11L13 40 6 42 6 68-2 68-5 43-8 69-15 68-10 39-17 35Z',color)}${pose==='sit'?'':line(10,15,19,39,color,6)}</g>`;
}
function bowl(x,y,scale=1) {
  return `<g transform="translate(${x} ${y}) scale(${scale})">${path('M-40 0Q-36 38 0 39Q36 38 40 0Z','#d9bc89','#243b45',2)}<ellipse cx="0" cy="0" rx="40" ry="10" fill="#f3dec0" stroke="#243b45" stroke-width="2"/><ellipse cx="0" cy="0" rx="30" ry="5" fill="#d8cfb1"/>${line(-14,40,14,40,'#243b45',3)}${path('M-9 -17q-6-8 0-15M8 -13q7-10 0-18','none','#e2bd84',2)}</g>`;
}
function table(x=207,y=363,w=186) {
  return `${rect(x,y,w,13,'#ad7952',2,'#213c46',2)}${path(`M${x+14} ${y+13}l-5 87h9l8-87M${x+w-15} ${y+13}l7 87h-9l-10-87`,'#7a533e','#203944',2)}`;
}
function windowFrame(x=218,y=179,w=164,h=134,warm=false) {
  return `${rect(x-7,y-7,w+14,h+14,'#bc9973',2,'#152e3a',3)}${rect(x,y,w,h,warm?'#deb679':'#6c8991',1)}${path(`M${x+w/2} ${y}v${h}M${x} ${y+h*.6}h${w}`,'none','#203d49',5)}`;
}
function book(x,y,w,h,fill,rot=0) {
  return `<g transform="rotate(${rot} ${x+w/2} ${y+h/2})">${rect(x,y,w,h,fill,2,'#263d46',2)}${line(x+4,y+2,x+4,y+h-2,'#ecd3a5',1)}${line(x+8,y+7,x+w-4,y+7,'#243e48',1)}</g>`;
}
function envelope(x,y,w=95,h=62,fill='#e4d1ad') {
  return `${rect(x,y,w,h,fill,2,'#35414a',2)}${path(`M${x} ${y}l${w/2} ${h*.58}L${x+w} ${y}M${x} ${y+h}l${w*.35}-${h*.58}M${x+w} ${y+h}l-${w*.35}-${h*.58}`,'none','#976f61',1.5)}`;
}
function pine(x,y,s=1,fill='#193b43') {
  return `<g transform="translate(${x} ${y}) scale(${s})">${rect(-3,0,6,90,'#796b52')}${path('M0-80-35-18h18l-29 46h30l-37 45H53L16 28h30L17-18h18Z',fill,'#18333d',2)}</g>`;
}
function skyline(y=302,fill='#1b3b49') {
  return path(`M116 ${y+40}v-35h18v-12h13v28h15v-60h10v-8h8v8h10v45h18v-30h20v-18h8v-8h6v8h9v48h21v-70h6v-28h3v28h7v70h19v-42h24v12h18v-65h11v-14h6v14h10v57h18v-25h17v18h16v-37h18v50h21v-15h12v64Z`,fill);
}
function room(floor='#8a745d') {
  return `${rect(120,125,360,330,'#39515a')}${path('M120 342 300 300 480 342V480H120Z',floor)}${line(120,342,300,300,'#263f47',2)}${line(480,342,300,300,'#263f47',2)}${[155,207,263,329,390,451].map(x=>line(300,300,x,480,'#aa8e6d',1)).join('')}`;
}
function sceneFor(chapter,p) {
  const dark='#193541', ink='#243e48', cream='#e9d2a9', coral=p[1], ochre=p[0];
  const dots=Array.from({length:22},(_,i)=>circle(154+(i*47)%296,161+(i*29)%144,i%3===0?1.6:1,cream)).join('');
  switch(chapter.slug) {
    case 'com-nguoi': return `${rect(120,130,360,350,'#294550')}${windowFrame(232,164,135,140,true)}${path('M163 394Q300 332 442 394L442 480H163Z','#a17d58')}${table(171,365,260)}${bowl(301,358,.88)}${line(217,345,268,336,'#c89c6d',3)}${path('M236 206q19-40 47-8M319 228q13-30 36-8','none','#eed4a7',2)}`;
    case 'i-was-born-a-quant': return `${room('#8a7a66')}${windowFrame(248,155,151,163)}${path('M250 234l27-20 25 7 22-41 30 13 20-23 23 8','none',cream,2)}${[190,220,250,280].map(y=>line(145,y,450,y,'#54717a',1)).join('')}${[178,210,242,274,306,338,370,402].map(x=>line(x,145,x,325,'#54717a',1)).join('')}${person(278,308,1.13)}${rect(160,290,48,100,'#263b46',1,'#a78d71',3)}${circle(198,342,3,ochre)}${path('M348 348a38 38 0 0 1 76 0','none',ochre,4)}${line(386,348,408,321,cream,3)}${rect(350,347,72,4,cream)}`;
    case 'expected-utility': return `${room('#89705d')}${windowFrame(195,156,212,140)}${path('M229 196q22-24 43 0-23 18-43 0M326 196q22-24 43 0-23 18-43 0','none','#c6a08e',2)}${circle(251,194,4,coral)}${circle(348,194,4,coral)}${table(175,365,255)}${rect(250,292,105,69,'#182e3b',4,'#aa9d83',3)}${path('M241 366h125l-12-12h-102Z','#d1b994',ink,2)}${[307,319,331,343].map((y,i)=>line(262,y,325-i*9,y,i%2?ochre:'#8fa6a2',2)).join('')}${path('M206 361v-80l27-17','none',cream,5)}${path('M212 272l34-14 13 31-47 6Z',ochre,ink,2)}${path('M226 293l-48 70h102Z','#eac995').replace('fill="','opacity=".12" fill="')}${person(364,303,.9,ink,'sit')}`;
    case 'play-to-win': return `${room('#6c6658')}${table(190,327,220)}${path('M190 327 235 285h133l42 42Z','#6d8c7c',ink,3)}${person(168,286,1.15,ink,'sit')}${person(415,286,1.15,ink,'sit')}${rect(278,377,49,48,'#a78d65',3,ink,3)}${line(281,425,281,456,ink,5)}${line(324,425,324,456,ink,5)}${[0,1,2,3,4,5].map(i=>`${rect(237+i*17,299,13,20,cream,2,ink,1)}${circle(243+i*17,307,2,coral)}`).join('')}${[0,1,2].map(i=>circle(315+i*14,335,7,ochre,ink,1)).join('')}`;
    case 'fashion': return `${room('#b18865')}${rect(338,170,93,192,'#a06c53',2,ink,3)}${line(384,176,384,351,cream,1)}${path('M355 211l16-13 26 0 18 13-13 18-7-5v62h-35v-62l-7 5Z','#d4b78a',ink,2)}${rect(156,337,130,54,'#c3aa8c',4,ink,3)}${rect(156,384,130,32,'#d4bc9b',2,ink,2)}${path('M176 340l21-32 25 23 39 9 11 17h-96Z',coral,ink,3)}${line(177,352,269,352,cream,3)}${[0,1,2].map(i=>line(204+i*9,326,199+i*9,336,cream,2)).join('')}${rect(190,186,91,101,'#263e49',3,ochre,4)}${path('M219 215l13-11 20 0 14 11-10 16-7-4v38h-26v-38l-7 4Z','#8b9d92')}${person(305,316,.88)}`;
    case 'flow': return `${room('#a58e6a')}${windowFrame(245,157,132,124,true)}${table(182,348,245)}${path('M227 348l19-35 107 5 27 30Z',cream,ink,2)}${path('M258 342v-22h35v22m8 0v-21h36v22m-88-10h102','none','#7b8b7c',1.8)}${person(171,300,.92,ink,'sit')}${person(418,300,.92,ink,'sit')}${circle(332,362,7,ochre,ink,1)}${line(338,362,361,362,ink,3)}${line(353,362,353,370,ink,3)}${path('M164 414q58-37 115 0t137 0','none','#9db6a3',6)}${path('M390 401l22 13-20 12','none','#9db6a3',3)}`;
    case 'nut-do': return `${room('#7b715b')}${windowFrame(217,159,165,130)}${table(175,364,255)}${book(218,334,76,28,cream,-7)}${line(306,344,353,351,ochre,4)}${rect(354,329,42,27,'#b99e7a',6,ink,2)}${path('M360 331q15-13 29 0','none',ink,7)}${circle(300,226,38,'#8e493c')}${circle(300,226,29,'#c7614f')}${path('M280 231q20-17 40 0l-5 9-7-7h-16l-7 7Z','#e6bd98')}${path('M277 279l-17 17m56-18 22 17','none',coral,1.5)}${rect(279,391,56,45,'#25414a',4,ochre,3)}${line(285,436,280,466,ink,4)}${line(329,436,334,466,ink,4)}`;
    case 'mot-nguoi-ban-cu': return `${room('#b29b77')}${windowFrame(185,155,228,115,true)}${[0,1,2,3].map(i=>line(155,335+i*31,449,335+i*31,'#c4ad86',1)).join('')}${rect(191,326,38,12,'#9d6b50',2,ink,2)}${line(199,338,193,380,ink,4)}${line(221,338,227,380,ink,4)}${rect(376,326,38,12,'#9d6b50',2,ink,2)}${line(383,338,377,380,ink,4)}${line(407,338,413,380,ink,4)}${rect(283,378,34,27,coral,4,ink,2)}${rect(289,363,22,17,ochre,3,ink,2)}${circle(295,370,2,ink)}${circle(305,370,2,ink)}${line(281,389,272,386,ink,3)}${line(316,388,325,384,ink,3)}${circle(290,407,5,ink)}${circle(311,407,5,ink)}${path('M304 367v-12m-5 4h10','none',cream,2)}`;
    case 'for-mother-russia': return `${rect(120,125,360,360,'#244652')}${dots}${path('M118 375q85-41 172-3t192-5v120H118Z','#d1d8c7')}${path('M267 480q81-62 65-115l-10-28h-18q44 67-84 143Z','#9fb8af')}${pine(173,283,.95)}${pine(425,304,1.1)}${pine(219,245,.58,'#315e60')}${pine(382,244,.59,'#315e60')}${rect(258,277,99,75,'#a46e4f',3,ink,3)}${path('M243 280l64-54 65 54Z','#d8d9c8',ink,3)}${rect(281,293,33,34,'#f3ce7c',1,ink,3)}${line(298,294,298,326,ink,2)}${rect(329,302,18,50,'#533e36',0,ink,2)}${path('M317 230q-12-28 3-38t1-32','none','#adbbb2',4)}`;
    case 'the-gioi-trong-mo-cua-toi': return `${rect(120,125,360,360,'#7c9b9d')}${path('M121 182q178-61 358 0v271H121Z','#cabf9a',ink,5)}${rect(199,196,202,127,'#254c5a',14,ink,5)}${path('M203 285h195M217 265h13v-26h9v-15h8v41h15v-36h20v36h17v-58h6v58h16v-28h16v28h21v-39h12v39h28','none','#b9a27c',3)}${rect(143,331,90,19,coral,5,ink,3)}${rect(367,331,90,19,coral,5,ink,3)}${rect(139,349,94,46,'#536f75',4,ink,3)}${rect(367,349,94,46,'#536f75',4,ink,3)}${person(206,297,.7,ink,'sit')}${person(394,297,.7,ink,'sit')}${rect(270,159,61,28,ochre,5,ink,2)}${txt(300,180,'5',23,ink,'text-anchor="middle"')}${line(249,182,249,425,ink,5)}${line(352,182,352,425,ink,5)}${path('M228 477l29-65h88l32 65Z','#a7997c')}${txt(300,444,'BASTILLE',10,ink,'text-anchor="middle" letter-spacing="3"')}`;
    case 'nhung-thu-khong-duoc-luu-lai': return `${rect(120,125,360,360,'#284856')}${path('M120 319q98-20 179-3t181-19v190H120Z','#afaa8c')}${path('M151 409l143-41 153 37-143 53Z','#40565b')}${path('M190 360q52-21 109 3v73q-54-22-109-2Z',cream,ink,2)}${path('M299 363q53-30 110-12v74q-51-17-110 11Z','#d7c29a',ink,2)}${[0,1,2,3].map(i=>path(`M207 ${378+i*12}q36-7 76 3`,'none','#a89b7e',1.4)).join('')}${[0,1,2,3].map(i=>path(`M315 ${376+i*12}q29-13 72-10`,'none','#a89b7e',1.4)).join('')}${path('M364 352q38-43 80-37m-81 53q44-20 90-10m-68 21q41-2 71 8','none','#d7c29a',2)}${book(166,292,53,54,'#dfcfad',-13)}${rect(174,301,37,34,'#718e87',1)}${line(351,446,408,423,coral,4)}${path('M219 253q39-22 67-7t61-13 47 4','none','#b7bba1',1.5)}`;
    case 'nhung-su-trung-hop': return `${room('#987e5e')}${[256,322,388].map(y=>`${rect(152,y,296,9,'#ad8a60',2,ink,2)}${Array.from({length:13},(_,i)=>book(160+i*21,y-48-(i%3)*5,15,47+(i%3)*5,p[(i+1)%5],(i%5===0)?-8:0)).join('')}`).join('')}${circle(300,187,43,cream,ink,5)}${circle(300,187,36,'#d8c49f',ink,1)}${txt(300,192,'11:11',16,ink,'text-anchor="middle"')}${path('M199 470q35-32 100-57m104 57q-39-33-104-57','none','#d6b482',3)}${person(299,352,.81)}`;
    case 'vo-mong': return `${rect(120,125,360,360,'#24434f')}${dots}${path('M124 406V309l171-82 180 85v174H124Z','#8a705a',ink,3)}${path('M123 313l172-100 182 100-11 17-171-91-161 90Z','#b49974',ink,3)}${rect(269,293,62,76,ochre,1,ink,4)}${line(300,294,300,367,ink,3)}${line(270,330,330,330,ink,3)}${path('M228 243l8-24 14 20 23 1-17 14 4 23-21-12-21 11 6-23-17-15Z','#d1b776',ink,2)}${line(239,239,239,204,'#c6aa7b',1)}${rect(227,391,54,43,'#a45547',2,ink,2)}${line(252,391,252,434,ochre,5)}${path('M251 392q-29-28-25-11t25 11q28-31 26-13t-26 13','none',ochre,3)}${path('M120 450q120-43 240-9t120 14v40H120Z','#ab9476')}`;
    case 'nhung-nguoi-anh-em': return `${rect(120,125,360,360,'#203d49')}${dots}${path('M120 344q131-47 360 0v150H120Z','#516567')}${path('M189 490l65-173h79l87 173Z','#b39a75')}${line(303,341,309,373,cream,4)}${line(314,400,321,445,cream,4)}${rect(182,252,136,63,'#b78761',10,ink,3)}${path('M202 252v-18h66l39 33h-106Z','#97ada2',ink,3)}${line(251,238,251,276,ink,3)}${circle(209,315,14,ink)}${circle(290,315,14,ink)}${table(218,381,185)}${person(202,328,.8,ink,'sit')}${person(414,330,.8,ink,'sit')}${person(300,321,.75,ink,'sit')}${[254,304,354].map(x=>`${rect(x,364,17,17,cream,3,ink,1.5)}${path(`M${x+17} 369q11-4 11 5t-11 4`,'none',cream,3)}`).join('')}`;
    case 'viet-cho-sai-gon-cua-t': return `${rect(120,125,360,360,'#ca9167')}${circle(364,237,53,'#e8bc7c')}${skyline(305,'#72594d')}${path('M120 352q126-20 360 0v125H120Z','#4c7679')}${[0,1,2,3,4].map(i=>line(135+i*18,373+i*19,450-i*22,373+i*19,'#b8a783',1.5)).join('')}${path('M113 334Q298 273 486 311','none','#e2bd89',9)}${path('M281 312V205l17-40 18 129M283 211l-132 111m144-142 105 124','none',ink,3)}${path('M120 427q160-45 360-6v70H120Z',ink)}${rect(205,386,51,66,'#b48b63',4,'#142e3b',3)}${rect(265,402,41,54,coral,4,'#142e3b',3)}${path('M219 387v-10h21v10m35 15v-9h18v9','none',ochre,3)}${person(336,380,.82)}`;
    case 'i-am-28-today': return `${rect(120,125,360,360,'#203745')}${[[-20,186,196],[13,330,176],[-8,153,307],[10,365,285]].map(([r,x,y],i)=>`<g transform="rotate(${r} ${x+30} ${y+25})">${rect(x,y,70,60,'#d3b992',3,ink,3)}${rect(x+6,y+6,58,40,p[(i+2)%5],1)}${path(`M${x+13} ${y+39}l15-18 12 12 13-23 14 29Z`,ink)}${circle(x+47,y+17,6,ochre)}</g>`).join('')}${table(207,399,191)}${rect(239,346,119,51,coral,7,ink,3)}${path('M239 355q13 25 24 0 12 25 24 0 12 25 24 0 12 25 24 0 12 25 23 0','none',cream,8)}${path('M262 344v-17m24 17v-24m24 24v-24m24 24v-17','none',cream,4)}${[262,286,310,334].map(x=>path(`M${x} 321q-8-10 0-17 8 8 0 17`,ochre)).join('')}${txt(299,305,'28',40,ochre,'text-anchor="middle"')}${rect(348,420,42,28,'#a48c71',3,ink,2)}${circle(370,434,9,ink)}${rect(354,414,14,7,coral,1)}`;
    case 'tieu-hanh-tinh': return `${rect(120,125,360,360,'#303448')}${dots}${path('M123 422q139-85 359-11v74H123Z','#675c6c')}${path('M152 430q120-108 281-217','none','#bd918e',1.5)}${path('M310 210l66-65m-49 78 72-58m-67 80 99-64','none','#bd918e',3)}${path('M276 224l26-28 30 9 12 33-23 26-32-8Z','#d3aa8f',ink,3)}${circle(304,232,11,'#a37173')}${circle(324,220,5,'#e4c09b')}${envelope(218,337,144,84)}${path('M245 365q25 4 47-5m-47 17q36 5 70-6','none','#af8d7c',2)}${path('M174 318q21-14 33-4m163-8 30-18','none',cream,1.5)}`;
    case 'three-meeting-theory': return `${rect(120,125,360,360,'#394454')}${skyline(295,'#635465')}${path('M120 370 300 285 480 370v115H120Z','#8b7c78')}${path('M130 465q124-75 170-180M280 485q72-97 20-200M469 454q-172-57-169-169','none','#d3b49c',4)}${path('M300 354V181q0-14 17-14h23','none',ink,7)}${path('M323 170h31l-6 14h-19Z',cream,ink,3)}${path('M338 185l-63 171h126Z','#e9c89b').replace('fill="','opacity=".1" fill="')}${person(220,350,.65)}${person(354,365,.68)}${person(294,288,.45)}${circle(300,410,7,coral)}${circle(270,397,6,coral)}${circle(328,397,6,coral)}`;
    case 'dating-algorithm': return `${rect(120,125,360,360,'#333446')}${path('M149 137h36v225h-36ZM415 137h36v225h-36Z','#8d5361')}${rect(204,182,193,132,'#bfa992',4,ink,3)}${path('M229 278l33-36 27 14 33-46 42 9','none',coral,4)}${[0,1,2].map(i=>`${rect(231+i*47,215+(i%2)*10,29,40,'#dfc0a6',3,ink,1)}${circle(245+i*47,227+(i%2)*10,6,'#aa7d77')}${path(`M${236+i*47} ${248+(i%2)*10}q9-15 18 0`,coral)}`).join('')}${path('M134 374q164-40 332 0l-21 49H154Z','#a76162',ink,3)}${person(303,293,.83)}${path('M332 330v49m-6-49h12','none',cream,3)}${Array.from({length:8},(_,i)=>`${rect(169+i*31,425,24,35,'#584554',8,ink,2)}${line(174+i*31,460,171+i*31,477,ink,3)}`).join('')}${txt(300,201,'A THOUGHT EXPERIMENT',7,ink,'text-anchor="middle" letter-spacing="1.2"')}`;
    case 'to-mary-jane': return `${room('#a18b76')}${rect(344,156,78,210,'#d8b69b',0,ink,5)}${path('M347 160l58 16v192l-58-4Z','#ae8f81',ink,3)}${circle(395,275,3,cream)}${path('M348 366l-84 114h194l-39-114Z','#d9b99b').replace('fill="','opacity=".45" fill="')}${table(175,353,177)}${envelope(219,316,92,59)}${path('M198 355l12-69m-5 40-14-15m15 4 15-17','none','#a2a183',3)}${path('M209 288q-20-19-12-27 8-9 14 6 12-11 17-1 5 10-19 22Z','#ae7372',ink,1)}${path('M150 414q45-15 64 1','none',coral,2)}`;
    case 'runaway': return `${room('#ae8a72')}${windowFrame(171,169,136,118,true)}${rect(194,340,228,94,'#80646b',6,ink,4)}${rect(183,330,246,62,'#d3b4a3',8,ink,3)}${path('M190 353q42 31 74 1t67 12 94-3v58H190Z','#b88883',ink,2)}${rect(200,320,68,32,'#e4cdb4',8,ink,2)}${rect(309,352,59,42,'#253d49',4,'#cfb69a',3)}${path('M316 378l14-12 11 9 17-16','none','#b5c7b1',2)}${table(365,294,64)}${rect(381,267,18,27,'#a8b3ab',2,ink,1.5)}${line(383,278,397,278,cream,1)}${path('M348 206l15-12 21 0 16 12-11 15-7-4v48h-25v-48l-7 4Z','#b5b5a0',ink,2)}`;
    case 'nhung-hinh-chieu-xau-xi': return `${room('#938478')}${path('M215 157h143l-9 179H224Z','#b49786',ink,4)}${path('M226 169h120l-8 154H234Z','#6e7e85',ink,2)}${path('M249 184l65 91-44 15 54 26M262 178l51 41 17-10','none','#d1b6a4',3)}${path('M345 199l113 88-68 25 64 131-114-73 30-65-35-44Z','#273845').replace('fill="','opacity=".55" fill="')}${rect(227,369,65,20,'#bc9a82',4,ink,3)}${path('M233 367v-47h52v47M235 390l-8 59m58-59 8 59','none',ink,5)}${circle(184,264,24,'#a59f91',ink,3)}${path('M169 247l31 33','none',cream,2)}`;
    case 'the-23-word-nuclear-warhead': return `${room('#8e7464')}${table(182,363,250)}${rect(246,302,100,59,'#1c3441',3,'#ba9a79',3)}${rect(235,358,124,7,'#b5a087',2)}${path('M194 175h216v104H304l-57 40 12-40h-65Z','#b16b56',ink,4)}${[210,237,265,293,321,349,377].map((x,i)=>line(x,199,x+12+(i%3)*2,199,cream,3)).join('')}${[210,245,280,315,350].map(x=>line(x,218,x+23,218,cream,3)).join('')}${line(210,237,292,237,cream,3)}${circle(386,339,9,ochre,ink,2)}${path('M380 348l-7 13h26l-7-13Z',ochre,ink,2)}${rect(201,335,30,21,'#d6b897',2,ink,1)}${path('M386 291l-12 16m25-12-2 14','none',coral,2)}`;
    case 'better-and-brighter-than-ever': return `${room('#8e7965')}${rect(188,163,225,10,'#e3d2b5',4,ink,3)}${path('M151 218h299','none',ink,5)}${[222,366].map((x,i)=>`${path(`M${x} 219q-9-8 0-13 8-4 8-11`,'none',ochre,2)}${path(`M${x-26} 242l19-16h25l20 16-15 24-9-8v82h-40v-82l-9 8Z`,i?'#b66d56':'#b6b69c',ink,3)}${txt(x+1,295,i?'08':'23',26,ink,'text-anchor="middle"')}${line(x-14,249,x+18,249,cream,2)}`).join('')}${path('M292 218q-8-6 0-13 8-5 8-12','none',ochre,2)}${rect(385,303,18,26,cream,1,ink,1)}${line(384,301,381,284,ochre,1.5)}${path('M167 407q105-34 274 0','none','#ae8b6c',2)}`;
    case 'masterclass-in-record-keeping': return `${room('#8c7969')}${rect(170,170,263,187,'#675a52',4,ink,4)}${Array.from({length:9},(_,i)=>{const x=185+(i%3)*79,y=185+Math.floor(i/3)*51;return `${rect(x,y,62,42,i%3===0?'#d6bf9e':'#bdac90',1,ink,1)}${line(x+7,y+10,x+50,y+10,'#776d60',1)}${line(x+7,y+18,x+43,y+18,'#776d60',1)}${line(x+7,y+26,x+49,y+26,'#776d60',1)}${circle(x+31,y-2,2,coral)}`;}).join('')}${path('M209 208 288 260l80-20-73 67-77-21','none',coral,1.4)}${table(180,396,243)}${book(211,363,78,18,cream,-5)}${book(206,380,89,13,'#c7ac88')}${circle(362,338,33,'#b8c3b0',ink,7)}${circle(362,338,26,'#c9c7ae',ink,1)}${path('M385 363l36 39','none',ink,12)}${line(347,330,376,330,'#6c786f',2)}${line(347,340,369,340,'#6c786f',2)}${line(347,350,373,350,'#6c786f',2)}`;
    case 'good-boy': return `${rect(120,125,360,360,'#273e49')}${path('M120 433q185-57 360-6v58H120Z','#736b62')}${rect(226,167,148,275,'#162c38',18,'#a08d77',5)}${rect(237,189,126,224,'#d5c5a8',5)}${rect(276,177,48,4,'#baac91',2)}${path('M251 230h84v41h-58l-16 14 3-14h-13Z','#839b92',ink,2)}${path('M266 301h83v42h-13l3 14-18-14h-55Z','#bb8f79',ink,2)}${circle(294,386,13,'#a86451')}${path('M285 388q9-9 18 0','none',cream,3)}${line(272,427,326,427,'#a3927d',3)}`;
    case 'negative-sum-game': return `${room('#786c62')}${path('M142 280h132m50 0h134','none',cream,3)}${path('M282 272l10 15 13-15 12 15','none',cream,2)}${[204,397].map((x,i)=>`${circle(x,330+i*33,26,i?coral:ochre,ink,3)}${txt(x,338+i*33,i?'−2':'−1',22,ink,'text-anchor="middle"')}${path(`M${x} 304v-46m-8 34 8 12 8-12`,'none',cream,2)}`).join('')}${rect(269,332,62,13,'#9c8a73',3,ink,2)}${line(275,345,270,408,ink,4)}${line(324,345,330,408,ink,4)}${path('M182 426l119-35 121 33-118 40Z','#c2a889',ink,3)}${Array.from({length:4},(_,row)=>Array.from({length:4},(_,col)=>((row+col)%2===0)?path(`M${225+col*23-row*11} ${414+row*10}l23-7 11 10-23 7Z`,'#6b635b'):'').join('')).join('')}`;
    case 'sharingan': return `${rect(120,125,360,360,'#32545a')}${path('M120 386q157-87 360-10v110H120Z','#72867a')}${path('M260 486q98-88 54-155l-16-9q45 81-101 164Z','#c4b99b')}${path('M143 482l28-177-7-176h45l-5 165 28 188ZM380 482l16-188-13-165h47l-5 166 34 187Z','#6f7764',ink,3)}${path('M179 310q-16-66 4-125m14 247q-18-60-5-98m220 75q16-80-4-186','none','#a5a28a',2)}${path('M393 270q23-27 42 0-23 27-42 0Z','#b9b897',ink,2)}${circle(415,270,8,ink)}${Array.from({length:6},(_,i)=>`<ellipse cx="${264+i*5}" cy="${453-i*17}" rx="3" ry="6" fill="#68756a" transform="rotate(28 ${264+i*5} ${453-i*17})"/>`).join('')}${path('M241 195q42-31 84-4-25 20-55 16Z','#aab597',ink,1)}${path('M247 199l65-5','none',ink,1)}`;
    case 'command-respect': return `${room('#a28d72')}${rect(268,152,96,231,'#b3ad8d',0,ink,4)}${rect(278,162,77,210,'#263f47',0)}${path('M282 165l111 311h-180l65-104Z','#1c333f').replace('fill="','opacity=".65" fill="')}${table(174,362,252)}${bowl(292,355,.68)}${path('M356 242l11-19h43l14 19-8 10h-51Z','#a2ab92',ink,2)}${path('M360 244q28 14 60 0','none',ink,3)}${circle(388,236,5,ochre)}${line(198,340,251,329,ochre,3)}${rect(180,288,39,68,'#46615e',2,ink,3)}`;
    case 'lone-wolf': return `${rect(120,125,360,360,'#41636b')}${circle(363,210,43,'#c7c7aa')}${path('M120 352q82-63 185-18t175-1v147H120Z','#8b9c86')}${path('M117 415q165-29 363 19v61H117Z','#a5ad92')}${path('M180 337h233v17H180Zm16 34h200v12H196Z','#b79d78',ink,3)}${path('M197 354v78m199-78v78','none',ink,7)}${person(269,304,.86,ink,'sit')}${path('M324 367l5-20 15 9 13-11 7 17 17 8-4 21h-11l-4-10h-17l-2 12h-10l-5-18Z','#e5dfc3',ink,2)}${circle(349,361,2,ink)}${path('M378 374q15-16 12-26','none','#e5dfc3',5)}${path('M250 428l61-12 30-22 16 17 27-13 10 31-32 23-76-7-47 13Z','#4c655e').replace('fill="','opacity=".5" fill="')}${line(296,338,333,357,ochre,2)}${path('M136 355l29-38 24 38m210-24 25-39 29 39','none','#5b7c72',3)}`;
    case 'co-nhung-thu-chi-khi-minh-roi-di-roi-moi-nhin-thay': return `${room('#a19b7f')}${rect(176,167,251,164,'#d0cfaf',4,ink,4)}${path('M192 284l37-51 27 29 39-67 41 63 27-34 49 65','none','#577973',3)}${path('M250 314q29-39 63-47t44-36','none','#b77d64',3)}${path('M315 269l9-9-12 2','none','#b77d64',2)}${txt(300,191,'PATAGONIA',9,ink,'text-anchor="middle" letter-spacing="2"')}${table(188,378,242)}${rect(356,341,17,36,'#58736a',3,ink,2)}${rect(360,331,9,12,'#a6aa8c',1,ink,1)}${path('M212 450v-100q-4-13-15 0m-21-1q35-50 70 0Z','#b79d75',ink,2)}${path('M204 349v-32m-16 28 16-28 17 28','none',ink,2)}${rect(285,401,59,40,'#5f7870',3,ink,3)}${path('M290 439l-7 37m54-37 7 37','none',ink,4)}`;
    case 'loi-xin-loi': return `${room('#b0a58a')}${rect(322,157,101,142,'#c7cfb4',1,ink,4)}${path('M325 159l-40 20v137l40-18ZM420 158l39 22v134l-39-17Z','#8aa397',ink,3)}${path('M329 262q46-21 88-8','none','#7f9a91',2)}${table(175,369,220)}${rect(222,307,117,72,'#e4d9b8',2,ink,1.5)}${line(238,329,318,329,'#a69d80',1)}${line(238,340,310,340,'#a69d80',1)}${line(238,351,290,351,'#a69d80',1)}${rect(167,260,100,8,'#b9ab88',2,ink,2)}${path('M191 260v-41m17 41v-41','none','#627d73',4)}${path('M191 219v-9m17 9v-9','none','#cbd1b5',6)}${path('M382 348q20-21 36-2','none','#afad8b',2)}${path('M409 327q-7-9 1-14','none',ink,2)}`;
    case 'dating-102': return `${room('#9a7c72')}${windowFrame(170,163,258,144,true)}${path('M191 292q105-22 218 0','none','#e1ba9b',2)}${table(179,372,243)}${rect(263,323,78,52,'#263e49',6,cream,2)}${rect(271,330,62,37,'#dec9ab',3)}${path('M281 350q13-22 24 0t22-5','none',coral,3)}${circle(296,341,3,'#779c91')}${person(212,309,.87,ink,'sit')}${person(397,309,.87,ink,'sit')}${path('M159 191l47-12 17 49-47 12ZM398 185l38 8-10 46-38-8Z','#c3a584',ink,2)}${path('M173 204h27m-21 9h19m199-13h23m-25 10h17','none','#77675e',2)}${path('M300 284c-15-18-34-1 0 24 34-25 15-42 0-24Z',coral,ink,2)}`;
    default:return '';
  }
}

function ringPath(cx,cy,r,seed,irregular=0) {
  const n=96, pts=[];
  for(let i=0;i<n;i++) {
    const a=i/n*Math.PI*2;
    const rr=r+(Math.sin(a*5+seed)*.65+Math.sin(a*11+seed*1.7)*.35)*irregular;
    pts.push([cx+Math.cos(a)*rr,cy+Math.sin(a)*rr]);
  }
  return `M${pts.map(([x,y])=>`${x.toFixed(2)},${y.toFixed(2)}`).join('L')}Z`;
}

let portalRenderCount = 0;

/** Scene-only illustration for the shared paper ring on the book cover. */
export function renderPortalScene(chapter) {
  if (typeof chapter === 'string') chapter = chapters.find(c => c.id === chapter) || chapters[0];
  const palette = palettes[chapter.act] || palettes[0];
  const uid = `portal-scene-${chapter.id}-${++portalRenderCount}`;
  return `<svg class="portal-scene-art" viewBox="120 120 360 360" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="${uid}-title ${uid}-desc"><title id="${uid}-title">${esc(chapter.id)} · ${esc(chapter.title)}</title><desc id="${uid}-desc">${esc(chapter.scene)}</desc><rect x="120" y="120" width="360" height="360" fill="#193541"/>${sceneFor(chapter, palette)}</svg>`;
}

/** Self-contained paper-cut illustration. Safe to inject as a trusted local template. */
export function renderPortal(chapter) {
  if(typeof chapter==='string') chapter=chapters.find(c=>c.id===chapter)||chapters[0];
  const p=palettes[chapter.act]||palettes[0], seed=Number(chapter.id), uid=`portal-${chapter.id}-${++portalRenderCount}`;
  const irregular=chapter.act===1?0.6:chapter.act===2?3.2:chapter.act===4?2.4:1.5;
  let rings='';
  const radii=[250,235,221,208,195,183];
  radii.forEach((r,i)=>{
    const eccentric=chapter.act===2?3:chapter.act===3?4.8:chapter.act===4?5.7:2;
    const ox=Math.sin(seed*.7+i*1.8)*eccentric,oy=Math.cos(seed*.5+i*1.7)*eccentric;
    const outer=ringPath(300+ox,300+oy,r,seed+i,irregular), inner=ringPath(300+ox*.7,300+oy*.7,r-13,seed+i+1,irregular);
    const fill=p[i%5];
    rings+=`<path d="${outer}${inner}" fill="${fill}" fill-rule="evenodd" stroke="#172f39" stroke-width="1.2" filter="url(#${uid}-shadow)"/>`;
    rings+=`<circle cx="${300+ox}" cy="${300+oy}" r="${r-3}" fill="none" stroke="#f5dfb4" opacity=".25" stroke-width="1" ${chapter.act===5?'stroke-dasharray="800 500" transform="rotate(30 300 300)"':''}/>`;
    for(let j=0;j<7;j++) {
      const a=(j/7*Math.PI*2)+(i*.38)+(seed*.14);
      const x=300+Math.cos(a)*(r-7), y=300+Math.sin(a)*(r-7);
      if(chapter.slug==='loi-xin-loi'&&a%6.28>4.7)continue;
      rings+=`<g transform="translate(${x.toFixed(2)} ${y.toFixed(2)}) rotate(${a*180/Math.PI+90})">${path('M-4-4h8v9h-8Z',i%2?'#e9d6ac':'#344f57','#263c45',.5)}${line(-2,-1,2,-1,i%2?'#526667':'#c9b58d',.7)}${line(-2,2,1,2,i%2?'#526667':'#c9b58d',.7)}</g>`;
    }
  });
  // Fine cut edges are deliberately uneven. The final chapter leaves an unfinished arc.
  const crescentMask=chapter.slug==='loi-xin-loi'?`<path d="M300 300L502 105A280 280 0 0 1 553 430Z" fill="#071b27"/>`:'';
  const title=`${chapter.id} · ${chapter.title}`;
  return `<svg class="portal-illustration" viewBox="0 0 600 600" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="${uid}-title ${uid}-desc"><title id="${uid}-title">${esc(title)}</title><desc id="${uid}-desc">${esc(chapter.scene)} A layered paper illustration for this chapter.</desc><defs><radialGradient id="${uid}-glow"><stop stop-color="#6c7d7b"/><stop offset="1" stop-color="#152e3a"/></radialGradient><filter id="${uid}-shadow" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="5" stdDeviation="3" flood-color="#0c202a" flood-opacity=".55"/></filter><filter id="${uid}-grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".61" numOctaves="3" stitchTiles="stitch" seed="${seed+3}"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="linear" slope=".11"/></feComponentTransfer><feBlend in="SourceGraphic" mode="multiply"/></filter><clipPath id="${uid}-scene"><circle cx="300" cy="300" r="174"/></clipPath><clipPath id="${uid}-rim"><circle cx="300" cy="300" r="254"/></clipPath></defs><circle cx="300" cy="306" r="255" fill="#051621" opacity=".6"/><circle cx="300" cy="300" r="253" fill="#d0b086" stroke="#c9aa7e" stroke-width="2"/><circle cx="300" cy="300" r="246" fill="url(#${uid}-glow)"/><g clip-path="url(#${uid}-scene)">${sceneFor(chapter,p)}</g>${rings}<circle cx="300" cy="300" r="174" stroke="#102d38" stroke-width="4"/><circle cx="300" cy="300" r="177" stroke="#ecd4a7" stroke-opacity=".4" stroke-width="1"/><g clip-path="url(#${uid}-rim)" opacity=".36" pointer-events="none"><circle cx="300" cy="300" r="253" fill="transparent" filter="url(#${uid}-grain)"/></g>${crescentMask}</svg>`;
}
