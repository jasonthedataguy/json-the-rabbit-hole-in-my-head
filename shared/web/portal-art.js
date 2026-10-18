// One coordinate system for the picture, rotating frame and authoring template.
// Images are full-bleed scenes. Decorative rings belong only to the frame layer.
export const portalGeometry = Object.freeze({size:1000, centre:500, outerRadius:480, apertureRadius:310, pictureRadius:312});
export const portalPictures = Object.freeze({
  cover:{src:'assets/cover-scene-landscape.png',alt:'Jason looks through the portal toward the original dusk city and bridge landscape.',zoom:1,x:0,y:0},
  introduction:{src:'assets/introduction-scene-v2.png',alt:'An open book, a lone reader and a dusk city beside a bridge glow inside the Introduction portal.',zoom:1,x:0,y:0},
  introductionCover:{src:'assets/introduction-cover-scene-v2.png',alt:'A reader looks through an open book toward a moonlit city and bridge.',zoom:1,x:0,y:0},
  rice:{src:'assets/rice-scene-board-v2.png',alt:'A family gathers for dinner beneath a warm lamp, seen through the floral Cold Rice portal.',zoom:1,x:0,y:0},
  quant:{src:'assets/quant-scene.png',alt:'Jason studies a skyline and probability curve, contemplating his risk budget.',zoom:1,x:0,y:0},
  expectedUtility:{src:'assets/expected-utility-scene-v2.png',alt:'A laptop shows a woman’s eyes amid code, notes, coffee and branching decisions.',zoom:1,x:0,y:0},
  playToWin:{src:'assets/play-to-win-scene-v2.png',alt:'A warm lamp lights a game table with cards, poker chips, mahjong tiles and a payoff matrix.',zoom:1,x:0,y:0},
  fashion:{src:'assets/fashion-scene-v2.png',alt:'A red-and-white sneaker, hanging clothes and shoeboxes in a warm room overlooking the city.',zoom:1,x:0,y:0},
  motherRussia:{src:'assets/mother-russia-scene-v2.png',alt:'A glowing wooden cabin in snow faces a river and imagined city beneath a winter moon.',zoom:1,x:0,y:0},
  motherRussiaCover:{src:'assets/mother-russia-cover-scene-v2.png',alt:'A glowing cabin beside a snowy river faces an imagined city beneath a winter moon.',zoom:1,x:0,y:0},
  threeMeeting:{src:'assets/three-meeting-scene-v2.png',alt:'A sunset city, river and bridge seen through the Three Meeting Theory portal.',zoom:1,x:0,y:0},
  threeMeetingCover:{src:'assets/three-meeting-cover-scene-v2.png?v=2',alt:'Two people meet before a sunset bridge and skyline inside the homepage book ring.',zoom:1,x:0,y:0},
  datingAlgorithm:{src:'assets/dating-algorithm-scene-v2.png',alt:'Two people sit together at a lamplit table before a moonlit city, framed by dating profiles and signals.',zoom:1,x:0,y:0},
  datingAlgorithmCover:{src:'assets/dating-algorithm-cover-scene-v2.png',alt:'Two people share a date beneath a crescent moon inside the homepage book ring.',zoom:1,x:0,y:0},
  dating102:{src:'assets/dating-102-scene-v2.png',alt:'Two people share a notebook before a moonlit city inside the Dating 102 portal.',zoom:1,x:0,y:0},
  dating102Cover:{src:'assets/dating-102-cover-scene-v2.png',alt:'Two people lean over a shared notebook in a warm room beneath the homepage book ring.',zoom:1,x:0,y:0},
  placeholder:{src:'assets/portal-placeholder.svg',alt:'Empty picture slot for a chapter scene.',zoom:1,x:0,y:0}
});
const esc=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

export function renderPortalPicture(key,overrides={}){
  const picture={...(portalPictures[key] || portalPictures.placeholder),...overrides};
  const zoom=Math.max(1,Math.min(2,Number(picture.zoom)||1));
  const size=1000*zoom;
  // Clamp offsets so an image can never reveal an empty edge of the slot.
  const limit=(size-1000)/2;
  const x=Math.max(-limit,Math.min(limit,(Number(picture.x)||0)*10));
  const y=Math.max(-limit,Math.min(limit,(Number(picture.y)||0)*10));
  return `<svg class="fitted-portal-picture" viewBox="0 0 1000 1000" role="img" aria-label="${esc(picture.alt)}"><image href="${esc(picture.src)}" x="${500-size/2+x}" y="${500-size/2+y}" width="${size}" height="${size}" preserveAspectRatio="xMidYMid slice"/></svg>`;
}

export function renderPortalFrame(id='portal-frame',texture='assets/board-ring-cut.png'){
  // The PNG carries its own alpha mask. An SVG aperture mask would cut off
  // Jason's head where he leans into the portal opening.
  const guide=texture==='assets/board-ring-cut.png'?'<circle cx="500" cy="500" r="310" fill="none" stroke="#c5a575" stroke-width="2"/><circle cx="500" cy="500" r="480" fill="none" stroke="#c5a575" stroke-width="1.5"/>':'';
  return `<svg class="fitted-portal-frame" viewBox="0 0 1000 1000" aria-hidden="true"><image href="${esc(texture)}" x="0" y="0" width="1000" height="1000" preserveAspectRatio="xMidYMid slice"/>${guide}</svg>`;
}

export function renderFramedPortal(key,id='chapter-frame',texture='assets/board-ring-cut.png'){
  return `<div class="fitted-portal"><div class="fitted-portal-slot">${renderPortalPicture(key)}</div>${renderPortalFrame(id,texture)}</div>`;
}
