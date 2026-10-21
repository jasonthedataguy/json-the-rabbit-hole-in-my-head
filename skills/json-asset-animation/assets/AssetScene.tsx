import React, {useEffect, useState} from 'react';
import {LivingSteam} from './LivingSteam';
import {AbsoluteFill, Img, continueRender, delayRender, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

type Key = {t: number; value: number; ease?: 'smooth' | 'linear'};
type Prop = 'x' | 'y' | 'rotation' | 'scale' | 'opacity';
type Layer = {id: string; kind?: 'image' | 'glow' | 'steam'; asset_id?: string; x: number; y: number; width: number; height: number; z: number; pivot_x?: number; pivot_y?: number; color?: string; base?: Partial<Record<Prop, number>>; tracks?: Partial<Record<Prop, Key[]>>};
export type MotionManifest = {
  width: number; height: number; fps: number; duration_s: number; background: string;
  opening: {title: string; portal_asset: string; reveal_asset: string; focus_x: number; focus_y: number; title_hold_s: number; entry_end_s: number; story_start_s: number};
  assets: {id: string; imageSrc: string}[];
  layers: Layer[]; fontSrc?: string; audio: {mode: 'silent'};
};

const smooth = (value: number) => {const t = Math.max(0, Math.min(1, value)); return t * t * (3 - 2 * t);};
export const valueAt = (keys: Key[] | undefined, time: number, fallback: number): number => {
  if (!keys?.length) return fallback;
  if (time <= keys[0].t) return keys[0].value;
  for (let i = 1; i < keys.length; i++) {
    if (time <= keys[i].t) {
      const a = keys[i - 1], b = keys[i];
      const t = (time - a.t) / (b.t - a.t);
      return a.value + (b.value - a.value) * (b.ease === 'linear' ? t : smooth(t));
    }
  }
  return keys[keys.length - 1].value;
};

const AnimatedLayer: React.FC<{layer: Layer; time: number; assets: Map<string, string>}> = ({layer, time, assets}) => {
  const read = (prop: Prop, fallback: number) => valueAt(layer.tracks?.[prop], time, layer.base?.[prop] ?? fallback);
  const kind = layer.kind ?? 'image';
  const common: React.CSSProperties = {position: 'absolute', left: read('x', layer.x), top: read('y', layer.y), width: layer.width, height: layer.height, zIndex: layer.z, opacity: read('opacity', 1), transformOrigin: `${(layer.pivot_x ?? .5) * 100}% ${(layer.pivot_y ?? .5) * 100}%`, transform: `rotate(${read('rotation', 0)}deg) scale(${read('scale', 1)})`};
  if (kind === 'glow') return <div style={{...common, borderRadius: '50%', background: `radial-gradient(ellipse, ${layer.color ?? '#efb55b'} 0%, transparent 70%)`, mixBlendMode: 'screen'}}/>;
  if (kind === 'steam') return <div style={common}><LivingSteam time={time} width={layer.width} height={layer.height} color={layer.color}/></div>;
  const image = assets.get(layer.asset_id ?? '');
  if (!image) throw new Error('Unstaged image layer: ' + layer.id);
  return <Img src={staticFile(image)} style={{...common, objectFit: 'contain'}}/>;
};

export const AssetScene: React.FC<MotionManifest> = (props) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const [fontHandle] = useState(() => delayRender('Load animation title font'));
  useEffect(() => {document.fonts.load('16px MotionSerif').then(() => continueRender(fontHandle));}, [fontHandle]);
  if (props.audio.mode !== 'silent') throw new Error('Implement and verify real author audio before narrated rendering.');
  const time = frame / fps, opening = props.opening;
  const assets = new Map(props.assets.map(asset => [asset.id, asset.imageSrc]));
  const portal = assets.get(opening.portal_asset), reveal = assets.get(opening.reveal_asset);
  if (!portal || !reveal) throw new Error('Missing opening art');
  const entry = smooth((time - opening.title_hold_s) / (opening.entry_end_s - opening.title_hold_s));
  const dissolveStart = opening.title_hold_s + (opening.entry_end_s - opening.title_hold_s) * .72;
  const revealOpacity = smooth((time - dissolveStart) / (opening.story_start_s - dissolveStart));
  const storyOpacity = smooth((time - opening.story_start_s) / .55);
  const size = Math.min(width * .88, height * .56);
  const imageLeft = (width - size) / 2, imageTop = height * .43 - size / 2;
  const shiftX = -(opening.focus_x - .5) * size * entry;
  const shiftY = -(opening.focus_y - .5) * size * entry;
  const titleOpacity = smooth(time / .4) * (1 - smooth((time - opening.title_hold_s) / Math.max(.3, (opening.entry_end_s - opening.title_hold_s) * .5)));
  return <AbsoluteFill style={{backgroundColor: props.background, overflow: 'hidden', color: '#F4EEE3', fontFamily: 'MotionSerif, serif'}}>
    {props.fontSrc ? <style>{`@font-face {font-family: MotionSerif; src: url('${staticFile(props.fontSrc)}');}`}</style> : null}
    <AbsoluteFill style={{opacity: 1 - storyOpacity}}>
      <Img src={staticFile(reveal)} style={{position: 'absolute', width: '100%', height: '100%', objectFit: 'contain', opacity: revealOpacity}}/>
      <Img src={staticFile(portal)} style={{position: 'absolute', left: imageLeft, top: imageTop, width: size, height: size, transformOrigin: `${opening.focus_x * 100}% ${opening.focus_y * 100}%`, transform: `translate(${shiftX}px, ${shiftY}px) scale(${Math.exp(Math.log(5.2) * entry)})`, opacity: 1 - revealOpacity}}/>
      <div style={{position: 'absolute', left: '8%', right: '8%', top: '76%', textAlign: 'center', fontSize: Math.min(width * .075, height * .075), opacity: titleOpacity}}>{opening.title}</div>
    </AbsoluteFill>
    <AbsoluteFill style={{opacity: storyOpacity}}>{[...props.layers].sort((a,b) => a.z - b.z).map(layer => <AnimatedLayer key={layer.id} layer={layer} time={Math.max(0,time-opening.story_start_s)} assets={assets}/>)}</AbsoluteFill>
    <div style={{position: 'absolute', left: '8%', top: '5%', fontSize: Math.min(width * .025, height * .03), color: '#DFA569'}}>.json</div>
    <div style={{position: 'absolute', left: '8%', right: '8%', bottom: '5%', fontSize: Math.min(width * .022, height * .027), color: '#F4EEE3', opacity: .65, textAlign: 'center'}}>THỬ CHUYỂN ĐỘNG · KHÔNG ÂM THANH · CHƯA DUYỆT</div>
  </AbsoluteFill>;
};
