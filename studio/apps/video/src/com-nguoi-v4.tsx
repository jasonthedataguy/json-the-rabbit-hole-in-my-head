import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Img, Sequence, continueRender, delayRender, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {PortalEntry, type Shot} from './video';

type Key = {t: number; value: number};
type Layer = {id: string; scene_id: string; asset_id?: string; kind?: string; x: number; y: number; width: number; height: number; z: number; pivot_x?: number; pivot_y?: number; color?: string; tracks: Record<string, Key[]>};
type StoryShot = {id: string; kind: string; start_s: number; duration_s: number; scene_id: string; vo_text: string; on_screen_text: string; caption_cues?: {start_s: number; duration_s: number; text: string}[]; portal_entry?: {focus_x: number; focus_y: number; max_scale: number}};
export type V4Props = {width: number; height: number; fps: number; duration_s: number; fontSrc: string; classification: string; audio: {mode: string}; assets: {id: string; imageSrc: string}[]; layers: Layer[]; scene_art_box: {x: number; y: number; width: number; height: number}; timeline: {cuts: {master: {shots: StoryShot[]}}}; proofStatic?: boolean};
const palette = {midnight: '#101F31', navy: '#1C3247', cream: '#F4EEE3', gold: '#DFA569'};
const smooth = (v: number) => {const t=Math.max(0,Math.min(1,v)); return t*t*(3-2*t);};
const read = (keys: Key[]|undefined, time: number, fallback: number) => {
  if(!keys?.length) return fallback;
  if(time <= keys[0].t) return keys[0].value;
  for(let i=1;i<keys.length;i++) if(time<=keys[i].t) {const a=keys[i-1],b=keys[i]; return a.value+(b.value-a.value)*smooth((time-a.t)/(b.t-a.t));}
  return keys[keys.length-1].value;
};

const MovingScene: React.FC<{props: V4Props; shot: StoryShot; assets: Map<string,string>}> = ({props,shot,assets}) => {
  const frame=useCurrentFrame();
  const {fps,height}=useVideoConfig();
  const seconds=frame/fps;
  const storyTime=Math.max(0,shot.start_s+seconds-10.5);
  const box=props.scene_art_box;
  const opacity=smooth(seconds/.6);
  const camera=1+.024*(.5-.5*Math.cos(storyTime/17));
  const cue=shot.caption_cues?.find(c=>seconds>=c.start_s && seconds<c.start_s+c.duration_s);
  const layers=props.layers.filter(l=>l.scene_id===shot.scene_id).sort((a,b)=>a.z-b.z);
  return <AbsoluteFill>
    <AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 40%, ${palette.navy} 0%, ${palette.midnight} 70%)`,opacity}}/>
    <AbsoluteFill style={{opacity, clipPath:`inset(${box.y}px ${props.width-box.x-box.width}px ${height-box.y-box.height}px ${box.x}px)`}}>
      <AbsoluteFill style={{transform:`translate(${Math.sin(storyTime/15)*3}px,${Math.sin(storyTime/22)*2}px) scale(${camera})`,transformOrigin:`${props.width/2}px ${box.y+box.height/2}px`}}>
        {layers.map(layer=>{
          const time=props.proofStatic ? 0 : storyTime;
          const rotation=read(layer.tracks.rotation,time,0);
          const alpha=layer.kind==='glow' && props.proofStatic ? 0 : read(layer.tracks.opacity,time,1);
          const style: React.CSSProperties={position:'absolute',left:layer.x,top:layer.y,width:layer.width,height:layer.height,zIndex:layer.z,opacity:alpha,transform:`rotate(${rotation}deg)`,transformOrigin:`${(layer.pivot_x??.5)*100}% ${(layer.pivot_y??.5)*100}%`};
          if(layer.kind==='glow') return <div key={layer.id} style={{...style,borderRadius:'50%',background:`radial-gradient(ellipse, ${layer.color} 0%, transparent 70%)`,mixBlendMode:'screen'}}/>;
          const src=assets.get(layer.asset_id??'');
          if(!src) throw new Error('Unstaged v4 layer '+layer.id);
          return <Img key={layer.id} src={staticFile(src)} style={style}/>;
        })}
      </AbsoluteFill>
    </AbsoluteFill>
    <div style={{position:'absolute',left:'9%',right:'9%',top:'68%',height:'16%',display:'flex',alignItems:'center',justifyContent:'center',textAlign:'center',fontSize:52,lineHeight:1.5,whiteSpace:'pre-line',opacity:seconds<shot.duration_s && cue ? smooth((seconds-cue.start_s)/.2) : 0}}>{cue?.text??''}</div>
  </AbsoluteFill>;
};

export const ComNguoiV4: React.FC<V4Props> = (props) => {
  const frame=useCurrentFrame();
  const {fps}=useVideoConfig();
  const [handle]=useState(()=>delayRender('Load Vietnamese v4 title and captions'));
  useEffect(()=>{document.fonts.load('16px V4Serif').then(()=>continueRender(handle));},[handle]);
  if(props.audio.mode!=='silent' || props.classification!=='layer_animation') throw new Error('V4 is a silent layer-animation review.');
  const shots=props.timeline.cuts.master.shots;
  const assets=new Map(props.assets.map(a=>[a.id,a.imageSrc]));
  const current=shots.find(s=>frame>=Math.round(s.start_s*fps)&&frame<Math.round((s.start_s+s.duration_s)*fps));
  return <AbsoluteFill style={{backgroundColor:palette.midnight,color:palette.cream,fontFamily:'V4Serif,serif'}}>
    <style>{`@font-face{font-family:V4Serif;src:url('${staticFile(props.fontSrc)}');}`}</style>
    {shots.map(shot=>{
      const start=Math.round(shot.start_s*fps), duration=Math.min(Math.round(shot.duration_s*fps)+18,Math.round(props.duration_s*fps)-start);
      return <Sequence key={shot.id} from={start} durationInFrames={duration}>
        {shot.kind==='portal_entry' ? <PortalEntry artBox={props.scene_art_box} palette={palette} shot={{id:shot.id,startFrame:0,durationInFrames:Math.round(shot.duration_s*fps),voText:'',imageSrc:assets.get('portal')!,nativeWidth:1600,nativeHeight:1600,onScreenText:'Cơm nguội',kind:'portal_entry',captionCues:[],motion:{scale_from:1,scale_to:1,pan_x_px:0,pan_y_px:0},portalEntry:{focusX:.5,focusY:.565,maxScale:5.5,revealImageSrc:assets.get('hero-original')!}} as Shot}/> : shot.kind==='end' ? <AbsoluteFill style={{background:palette.midnight,opacity:smooth((frame-start)/18)}}><Img src={staticFile(assets.get('portal')!)} style={{position:'absolute',width:864,height:864,left:108,top:308,objectFit:'contain'}}/><div style={{position:'absolute',top:'72%',left:'8%',right:'8%',textAlign:'center',fontSize:76}}>Cơm nguội</div></AbsoluteFill> : <MovingScene props={props} shot={shot} assets={assets}/>}
      </Sequence>;
    })}
    <div style={{position:'absolute',top:'5%',left:'8%',right:'8%',textAlign:'center',fontSize:31,color:palette.gold,letterSpacing:'.12em'}}>.json</div>
    {current?.kind==='story' ? <><div style={{position:'absolute',top:'9%',left:'8%',right:'8%',textAlign:'center',fontSize:74}}>Cơm nguội</div><div style={{position:'absolute',top:'16.5%',left:'44%',right:'44%',height:1,backgroundColor:palette.gold,opacity:.5}}/></> : null}
    <div style={{position:'absolute',bottom:'9%',left:'8%',right:'8%',textAlign:'center',fontSize:24,color:palette.cream,opacity:.55}}>V4 · Bản dựng xem trước · Không âm thanh</div>
    <div style={{position:'absolute',left:'35%',right:'35%',bottom:'7.2%',height:2,backgroundColor:palette.navy}}><div style={{height:'100%',width:`${frame/3599*100}%`,backgroundColor:palette.gold,opacity:.7}}/></div>
  </AbsoluteFill>;
};
