// A continuous dial: the artwork follows pointer angle, then settles at one of 32 stops.
const STEP = 360 / 32;
const wrap = index => ((index % 32) + 32) % 32;
const shortestDelta = angle => ((angle + 540) % 360) - 180;

export class PortalRing {
  constructor({stage, initialIndex=0, onRotate, onSelect}) {
    this.stage=stage;this.index=initialIndex;this.rotation=-initialIndex*STEP;
    this.onRotate=onRotate;this.onSelect=onSelect;this.drag=null;
    this.ignoreClickUntil=0;this.lastWheelEvent=-Infinity;this.wheelCommitted=false;this.wheelDelta=0;
    stage.addEventListener('pointerdown', event=>this.start(event));
    stage.addEventListener('pointermove', event=>this.move(event));
    stage.addEventListener('pointerup', event=>this.finish(event));
    stage.addEventListener('pointercancel', event=>this.finish(event,true));
    window.addEventListener('pointerup', event=>this.finish(event));
    stage.addEventListener('dragstart', event=>event.preventDefault());
    stage.addEventListener('click',event=>{
      if(performance.now()<this.ignoreClickUntil){event.preventDefault();event.stopImmediatePropagation();}
    },true);
    stage.addEventListener('wheel',event=>this.wheel(event),{passive:false});
    this.paint(false);
  }
  paint(animate=true){this.onRotate(this.rotation,{animate,dragging:!!this.drag?.moved});}
  setChapter(index,{animate=true}={}){
    this.index=wrap(index);
    const current=-this.rotation/STEP;
    const nearest=this.index+32*Math.round((current-this.index)/32);
    this.rotation=-nearest*STEP;
    this.paint(animate);
  }
  turn(steps){this.setChapter(this.index+steps);this.onSelect(this.index);}
  pointerAngle(event,drag){return Math.atan2(event.clientY-drag.cy,event.clientX-drag.cx)*180/Math.PI;}
  start(event){
    if(this.drag || !event.isPrimary || (event.pointerType==='mouse' && event.button!==0))return;
    const box=this.stage.getBoundingClientRect(),cx=box.left+box.width/2,cy=box.top+box.height/2;
    this.drag={id:event.pointerId,x:event.clientX,y:event.clientY,cx,cy,width:box.width,startRotation:this.rotation,startIndex:this.index,moved:false,total:0,mode:Math.hypot(event.clientX-cx,event.clientY-cy)>box.width*.18?'angular':'swipe'};
    this.drag.lastAngle=this.pointerAngle(event,this.drag);
  }
  move(event){
    const drag=this.drag;if(!drag||event.pointerId!==drag.id)return;
    const dx=event.clientX-drag.x,dy=event.clientY-drag.y;
    const angle=this.pointerAngle(event,drag);
    drag.total+=shortestDelta(angle-drag.lastAngle);drag.lastAngle=angle;
    if(!drag.moved && Math.hypot(dx,dy)<5)return;
    if(!drag.moved){
      drag.moved=true;this.stage.classList.add('is-dragging');
      this.stage.setPointerCapture(event.pointerId);
    }
    if(event.cancelable)event.preventDefault();
    if(drag.mode==='angular')this.rotation=drag.startRotation+drag.total;
    else {
      const distance=Math.abs(dx)>=Math.abs(dy)?dx:dy;
      drag.swipeDistance=distance;
      this.rotation=drag.startRotation+Math.max(-STEP*1.2,Math.min(STEP*1.2,distance*STEP/(drag.width*.15)));
    }
    this.paint(false);
    const next=wrap(Math.round(-this.rotation/STEP));
    if(next!==this.index){this.index=next;this.onSelect(next);}
  }
  finish(event,cancelled=false){
    const drag=this.drag;if(!drag||event.pointerId!==drag.id)return;
    this.drag=null;this.stage.classList.remove('is-dragging');
    if(!drag.moved)return;
    this.ignoreClickUntil=performance.now()+200;
    if(this.stage.hasPointerCapture(event.pointerId))this.stage.releasePointerCapture(event.pointerId);
    let stop;
    if(cancelled)stop=drag.startIndex;
    else if(drag.mode==='swipe')stop=drag.startIndex+(Math.abs(drag.swipeDistance||0)>=24?(drag.swipeDistance<0?1:-1):0);
    else stop=wrap(Math.round(-this.rotation/STEP));
    this.setChapter(stop);this.onSelect(this.index);
  }
  wheel(event){
    if(event.ctrlKey||this.drag)return;
    event.preventDefault();
    const now=performance.now();
    if(now-this.lastWheelEvent>180){this.wheelCommitted=false;this.wheelDelta=0;}
    this.lastWheelEvent=now;
    if(this.wheelCommitted)return;
    this.wheelDelta+=(Math.abs(event.deltaY)>=Math.abs(event.deltaX)?event.deltaY:event.deltaX)*(event.deltaMode===1?16:1);
    if(Math.abs(this.wheelDelta)>=20){this.wheelCommitted=true;this.turn(this.wheelDelta>0?1:-1);}
  }
}
