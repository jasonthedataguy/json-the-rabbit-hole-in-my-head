import { renderIcon } from './chapters.js?v=34';

// The chapter's keepsake is printed on a paper tab seated in the portal's rim.
// Keep this SVG in normal document flow; its owner decides where the tab sits.
const ink = '#153746';
const esc = value => String(value ?? '').replace(/[&<>"']/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[character]));
const markerNames = {
  bowl: 'a cobalt porcelain bowl of rice',
  chart: 'a probability chart',
  laptop: 'a late-night laptop',
  scales: 'a balance scale for choices of heart and mind',
  tile: 'a mahjong tile',
  sneaker: 'a red, black and ivory Jordan 1 high-top sneaker',
  key: 'an apartment key',
  phone: 'a telephone receiver',
  toy: 'a childhood wind-up toy',
  candy: 'the packet of chíp chíp shared in childhood',
  pine: 'a snow-covered pine',
  metro: 'a Paris metro carriage',
  notebook: 'an open memory notebook',
  clock: 'a repeating clock',
  star: 'a childhood paper star',
  van: 'a road-trip van',
  bridge: 'Ba Son Bridge',
  cake: 'a birthday cake',
  asteroid: 'a luminous little planet on its own orbit',
  paths: 'three crossing paths',
  microphone: 'a stage microphone',
  heart: 'a small heart beside an iPad sketch',
  envelope: 'a sealed goodbye letter',
  bed: 'a familiar bed',
  mirror: 'a framed mirror',
  message: 'a message on paper',
  matrix: 'a scored payoff matrix',
  jersey: 'a football jersey',
  stamp: 'an apology stamped GOOD BOY',
  book: 'an open moral-model book',
  search: 'a record-keeper’s magnifying glass',
  dialogue: 'two quiet speech bubbles',
  counters: 'two falling counters',
  chess: 'a chessboard with opposing pieces',
  eye: 'an eye reflected in a leaf',
  vision: 'a bright eye and open path',
  arch: 'an arched childhood mirror',
  door: 'a doorway home',
  dog: 'Gấu, a little white dog',
  projector: 'a film projector and shadow screen',
  whiteboard: 'a mountain-roadtrip whiteboard',
  mountain: 'the mountains of Patagonia',
  crescent: 'an unfinished crescent',
};

export function getChapterMarkerName(chapter) {
  return markerNames[chapter?.iconKey] || 'a chapter keepsake';
}

function jordanHighTop() {
  return `<g class="marker-jordan-one" stroke-linejoin="round" stroke-linecap="round">
    <ellipse cx="51" cy="76" rx="34" ry="3" fill="#9d754c" opacity=".16"/>
    <path d="M19 66L22 40L25 21L43 19L49 32L48 44L58 54L75 58Q84 59 87 66L86 72H17Z" fill="#f0e1c3" stroke="#172f3a" stroke-width="1.7"/>
    <path d="M25 21L43 19L47 28L24 31Z" fill="#b44738" stroke="#172f3a" stroke-width="1.2"/>
    <path d="M27 25L40 23L43 27L26 29Z" fill="#24323a"/>
    <path d="M24 32L45 29L49 36L47 46L39 51L22 48Z" fill="#af4034" stroke="#172f3a" stroke-width="1.1"/>
    <path d="M22 47L35 46L40 52L39 63L20 64Z" fill="#b34636" stroke="#172f3a" stroke-width="1.1"/>
    <path d="M41 32L47 34L47 44L58 54L51 59L38 46Z" fill="#26333b" stroke="#172f3a" stroke-width="1.1"/>
    <path d="M39 51L48 46L60 55L72 58L68 64H41Z" fill="#f5e9d1" stroke="#172f3a" stroke-width="1"/>
    <path d="M69 57L78 59Q85 61 87 67L83 69L66 66L65 62Z" fill="#b64a39" stroke="#172f3a" stroke-width="1.1"/>
    <path d="M26 56Q32 60 37 56L61 48L46 59Q37 66 29 62Q24 61 26 56Z" fill="#172f3a"/>
    <path d="M18 66Q47 69 87 66L86 73Q47 77 17 72Z" fill="#f1dfb9" stroke="#172f3a" stroke-width="1.4"/>
    <path d="M18 73Q49 77 86 73L85 76Q47 80 18 76Z" fill="#9c392e" stroke="#172f3a" stroke-width=".8"/>
    <path d="M23 69L32 70M36 70L49 71M53 71L65 70M69 70L82 69" fill="none" stroke="#bd9a66" stroke-width=".75"/>
    <path d="M42 36L47 35M42 40L48 39M44 44L50 43M48 48L54 47M52 52L58 51" fill="none" stroke="#e7d8b8" stroke-width="1.8"/>
    <g fill="#d8b988"><circle cx="40" cy="36" r=".9"/><circle cx="40.5" cy="40.5" r=".9"/><circle cx="43" cy="44.8" r=".9"/><circle cx="47" cy="49" r=".9"/></g>
    <path d="M28 37L32 35L38 37M28 39L32 37L37 39M30 41L33 39L36 40" fill="none" stroke="#e6cda2" stroke-width=".8"/>
    <g fill="#3b3935"><circle cx="72" cy="62" r=".55"/><circle cx="76" cy="63" r=".55"/><circle cx="80" cy="64" r=".55"/></g>
    <path d="M25 32L23 43M22 51L21 60M70 59L67 64" fill="none" stroke="#e0a17a" stroke-width=".7"/>
  </g>`;
}

function keepsakeStamp(chapter) {
  const base = renderIcon(chapter, 24)
    .replace('<svg ', '<svg x="26" y="28" ')
    .replace('width="24" height="24"', 'width="48" height="48"');
  return `<g class="marker-keepsake-stamp" color="${ink}">
    <circle cx="50" cy="52" r="29" fill="#e7cfa2" stroke="#aa8350" stroke-width=".7"/>
    <circle cx="50" cy="52" r="26" fill="#f0dfbb" stroke="#af8854" stroke-width=".55" stroke-dasharray="1 3"/>
    ${base}
  </g>`;
}

let markerRenderCount = 0;

/** Return one accessible, self-contained illustrated paper chapter tab. */
export function renderChapterMarker(chapter, { compact = false } = {}) {
  const chapterNumber = chapter?.id ?? '';
  const markerName = getChapterMarkerName(chapter);
  const uid = `chapter-marker-${String(chapterNumber).replace(/[^a-zA-Z0-9_-]/g, '')}-${++markerRenderCount}`;
  if (chapter?.iconKey === 'bowl') {
    // Display the original supplied artwork without redrawing or changing its pixels.
    // Its medallion is centered at (478, 852); the 128px viewport retains the
    // ivory rim, navy disk, rice mound, and exact cobalt floral bowl decoration.
    return `<svg class="chapter-marker-svg${compact ? ' is-compact' : ''}" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="${uid}-title ${uid}-desc" data-marker-icon="bowl">
      <title id="${uid}-title">${esc(chapterNumber)} · ${esc(chapter?.shortTitle || chapter?.title || 'Chapter')} — ${esc(markerName)}</title>
      <desc id="${uid}-desc">The original illustrated rice-bowl medallion from the supplied Cơm nguội cover, with its ivory circular rim, navy background, and cobalt floral porcelain bowl. Chapter ${esc(chapterNumber)}.</desc>
      <defs><clipPath id="${uid}-reference-clip"><circle cx="50" cy="52" r="46"/></clipPath></defs>
      <g clip-path="url(#${uid}-reference-clip)">
        <svg x="4" y="6" width="92" height="92" viewBox="414 788 128 128" aria-hidden="true">
          <image href="./assets/bowl-reference.jpg" x="0" y="0" width="960" height="1280"/>
        </svg>
      </g>
      <text x="50" y="112" text-anchor="middle" fill="#f5e6c4" font-family="Georgia, 'Times New Roman', serif" font-size="12" letter-spacing="1">${esc(chapterNumber)}</text>
    </svg>`;
  }
  const illustration = chapter?.iconKey === 'sneaker' ? jordanHighTop() : keepsakeStamp(chapter || {});
  const fibers = compact ? '' : Array.from({ length: 26 }, (_, index) => {
    const x = 14 + index * 19 % 73;
    const y = 13 + index * 29 % 79;
    return `<path d="M${x} ${y}l${index % 2 ? 1.5 : 2.2} ${index % 3 ? '.3' : '-.4'}" stroke="#866037" stroke-width=".35" opacity=".22"/>`;
  }).join('');
  return `<svg class="chapter-marker-svg${compact ? ' is-compact' : ''}" viewBox="0 0 100 116" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="${uid}-title ${uid}-desc" data-marker-icon="${esc(chapter?.iconKey || 'bowl')}">
    <title id="${uid}-title">${esc(chapterNumber)} · ${esc(chapter?.shortTitle || chapter?.title || 'Chapter')} — ${esc(markerName)}</title>
    <desc id="${uid}-desc">A textured paper chapter tab with ${esc(markerName)} above the engraved chapter number ${esc(chapterNumber)}.</desc>
    <defs>
      <linearGradient id="${uid}-paper" x1="0" y1="0" x2=".8" y2="1"><stop stop-color="#fff0cb"/><stop offset=".52" stop-color="#e9cfa0"/><stop offset="1" stop-color="#cba76c"/></linearGradient>
      <linearGradient id="${uid}-edge" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#bd955c"/><stop offset="1" stop-color="#725538"/></linearGradient>
    </defs>
    <path d="M20 8H80V25C90 33 95 45 95 59C95 83 76 104 50 113C24 104 5 83 5 59C5 45 10 33 20 25Z" fill="url(#${uid}-edge)" stroke="#102c39" stroke-width="1.5"/>
    <path d="M20 5H80V22C90 30 95 42 95 56C95 80 76 101 50 110C24 101 5 80 5 56C5 42 10 30 20 22Z" fill="url(#${uid}-paper)" stroke="${ink}" stroke-width="1.4"/>
    <path d="M24 9H76V25C87 33 91 44 91 56C91 78 74 97 50 106C26 97 9 78 9 56C9 44 13 33 24 25Z" fill="none" stroke="#fff2ce" stroke-width="1" opacity=".8"/>
    <path d="M29 12H71" fill="none" stroke="#9c7948" stroke-width=".7"/>
    ${fibers}
    ${illustration}
    <path d="M35 83H65" fill="none" stroke="#aa8350" stroke-width=".65"/>
    <text x="50" y="99" text-anchor="middle" fill="#fff2d1" font-family="Georgia, 'Times New Roman', serif" font-size="18" letter-spacing="1">${esc(chapterNumber)}</text>
    <text x="50" y="98.2" text-anchor="middle" fill="${ink}" font-family="Georgia, 'Times New Roman', serif" font-size="18" letter-spacing="1">${esc(chapterNumber)}</text>
  </svg>`;
}

/** The same unmodified source medallion, also used in chapter detail and index. */
export function renderReferenceBowlIcon(size=38) {
  const uid=`reference-bowl-${++markerRenderCount}`;
  return `<svg class="reference-bowl-icon" width="${Number(size)||38}" height="${Number(size)||38}" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="${uid}-title"><title id="${uid}-title">The original Cơm nguội rice-bowl badge</title><defs><clipPath id="${uid}-clip"><circle cx="50" cy="50" r="49"/></clipPath></defs><g clip-path="url(#${uid}-clip)"><svg width="100" height="100" viewBox="414 788 128 128" aria-hidden="true"><image href="./assets/bowl-reference.jpg" width="960" height="1280"/></svg></g></svg>`;
}
