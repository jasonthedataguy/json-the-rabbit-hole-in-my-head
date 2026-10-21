import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Img, Sequence, continueRender, delayRender, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

export type Shot = {
  id: string;
  startFrame: number;
  durationInFrames: number;
  voText: string;
  imageSrc: string;
  nativeWidth: number;
  nativeHeight: number;
  onScreenText: string;
  kind: 'story' | 'title' | 'end' | 'portal_entry';
  portalEntry?: {focusX: number; focusY: number; maxScale: number; revealImageSrc: string};
  captionCues: {startFrame: number; durationInFrames: number; text: string}[];
  motion: {scale_from: number; scale_to: number; pan_x_px: number; pan_y_px: number};
};

const smooth = (value: number) => {
  const t = Math.max(0, Math.min(1, value));
  return t * t * (3 - 2 * t);
};

export const PortalEntry: React.FC<{shot: Shot; palette: Record<string, string>; artBox?: {x: number; y: number; width: number; height: number}}> = ({shot, palette, artBox}) => {
  const frame = useCurrentFrame();
  const {width, height, fps} = useVideoConfig();
  const entry = shot.portalEntry;
  if (!entry) throw new Error('Portal entry requires an explicit focus and reveal image.');
  const seconds = frame / fps;
  const enter = smooth((seconds - 2.6) / 5.1);
  const reveal = smooth((seconds - 6.0) / 2.5);
  const settle = smooth((seconds - 7.6) / 2.7);
  const scale = Math.exp(Math.log(entry.maxScale) * enter);
  const portalSize = Math.min(width * 0.86, height * (width > height ? 0.51 : 0.45));
  const artCenterY = artBox ? artBox.y + artBox.height / 2 : height * (0.20 + (width > height ? 0.51 : 0.45) / 2);
  const shiftX = -(entry.focusX - 0.5) * portalSize * enter;
  const shiftY = -(entry.focusY - 0.5) * portalSize * enter;
  const titleOpacity = smooth(seconds / 0.7) * (1 - smooth((seconds - 3.6) / 1.4));
  return <AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 43%, ${palette.navy} 0%, ${palette.midnight} 68%)`}}>
    <div style={{position: 'absolute', ...(artBox ? {left: artBox.x, top: artBox.y, width: artBox.width, height: artBox.height} : {left: '7%', right: '7%', top: '20%', height: width > height ? '51%' : '45%'}), display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: reveal}}>
      <Img src={staticFile(entry.revealImageSrc)} style={{width: '100%', height: '100%', objectFit: 'contain', transform: `scale(${1.65 - settle * 0.65})`}}/>
    </div>
    <Img src={staticFile(shot.imageSrc)} style={{position: 'absolute', width: portalSize, height: portalSize, left: (width - portalSize) / 2, top: artCenterY - portalSize / 2, transformOrigin: `${entry.focusX * 100}% ${entry.focusY * 100}%`, transform: `translate(${shiftX}px, ${shiftY}px) scale(${scale})`, opacity: (1 - reveal) * smooth(seconds / 0.6)}}/>
    <div style={{position: 'absolute', left: '8%', right: '8%', top: '69%', height: '15%', display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', fontSize: Math.min(width * 0.082, height * 0.082), color: palette.cream, opacity: titleOpacity}}>{shot.onScreenText}</div>
  </AbsoluteFill>;
};
export type PreviewProps = {
  title: string;
  slug: string;
  editionLabel: string;
  format: {name: string; width: number; height: number; fps: number};
  durationInFrames: number;
  shots: Shot[];
  fontSrc: string;
  renderKind: 'internal_preview';
  sourceSha256: string;
  palette: Record<string, string>;
};

const Scene: React.FC<{shot: Shot; palette: Record<string, string>}> = ({shot, palette}) => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const landscape = width > height;
  const textSize = landscape ? height * 0.044 : height / width < 1.5 ? width * 0.039 : width * 0.048;
  const progress = Math.min(1, frame / Math.max(1, shot.durationInFrames - 1));
  const scale = interpolate(progress, [0, 1], [shot.motion.scale_from, shot.motion.scale_to]);
  const opacity = interpolate(frame, [0, 18], [0, 1], {extrapolateRight: 'clamp'});
  const cue = shot.captionCues?.find(c => frame >= c.startFrame && frame < c.startFrame + c.durationInFrames);
  const text = cue?.text ?? (shot.captionCues?.length ? '' : shot.voText || shot.onScreenText);
  const cueFrame = frame - (cue?.startFrame ?? 0);
  const textOpacity = frame >= shot.durationInFrames ? 0 : interpolate(cueFrame, [0, 7], [0, 1], {extrapolateRight: 'clamp'});
  return <AbsoluteFill>
    <div style={{position: 'absolute', inset: 0, background: `radial-gradient(ellipse at 50% 43%, ${palette.navy} 0%, ${palette.midnight} 68%)`, opacity}}/>
    <div style={{position: 'absolute', left: '7%', right: '7%', top: '20%', height: landscape ? '51%' : '45%', display: 'flex', alignItems: 'center', justifyContent: 'center', opacity}}>
      <Img src={staticFile(shot.imageSrc)} style={{width: '100%', height: '100%', maxWidth: shot.nativeWidth, maxHeight: shot.nativeHeight, objectFit: 'contain', transform: `translate(${progress * shot.motion.pan_x_px}px, ${progress * shot.motion.pan_y_px}px) scale(${scale})`, transformOrigin: 'center'}}/>
    </div>
    <div style={{position: 'absolute', left: '9%', right: '9%', top: landscape ? '75%' : '69%', height: landscape ? '16%' : '15%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: palette.cream, fontSize: shot.kind === 'title' || shot.kind === 'end' ? textSize * 1.45 : textSize, lineHeight: 1.5, textAlign: 'center', opacity: textOpacity, whiteSpace: 'pre-line'}}>
      {text}
    </div>
  </AbsoluteFill>;
};

export const ChapterVideo: React.FC<PreviewProps> = (props) => {
  const [fontHandle] = useState(() => delayRender('Load existing Vietnamese font'));
  useEffect(() => {
    document.fonts.load('16px StudioSerif').then(() => continueRender(fontHandle));
  }, [fontHandle]);
  if (props.renderKind !== 'internal_preview') {
    throw new Error('This composition is an internal review renderer; release needs a separate approved handoff.');
  }
  const {width, height} = useVideoConfig();
  const frame = useCurrentFrame();
  const currentShot = props.shots.find(s => frame >= s.startFrame && frame < s.startFrame + s.durationInFrames);
  const headerOpacity = currentShot?.kind === 'story' ? 1 : 0;
  return <AbsoluteFill style={{backgroundColor: props.palette.midnight, color: props.palette.cream, fontFamily: 'StudioSerif, serif'}}>
    <style>{`@font-face { font-family: StudioSerif; src: url('${staticFile(props.fontSrc)}'); }`}</style>
    {props.shots.map((shot) => <Sequence key={shot.id} from={shot.startFrame} durationInFrames={Math.min(shot.durationInFrames + 18, props.durationInFrames - shot.startFrame)}>{shot.kind === 'portal_entry' ? <PortalEntry shot={shot} palette={props.palette}/> : <Scene shot={shot} palette={props.palette}/>}</Sequence>)}
    <div style={{position: 'absolute', left: '8%', right: '8%', top: '5%', textAlign: 'center', fontSize: Math.min(width * 0.029, height * 0.028), color: props.palette.gold, letterSpacing: '0.12em'}}>.json</div>
    <div style={{position: 'absolute', left: '8%', right: '8%', top: '9%', textAlign: 'center', fontSize: Math.min(width * 0.069, height * 0.068), opacity: headerOpacity}}>{props.title}</div>
    <div style={{position: 'absolute', left: '44%', right: '44%', top: '16.5%', height: 1, backgroundColor: props.palette.gold, opacity: 0.5 * headerOpacity}}/>
    <div style={{position: 'absolute', left: '9%', right: '9%', bottom: '9%', textAlign: 'center', fontSize: Math.min(width * 0.023, height * 0.025), color: props.palette.cream, opacity: 0.55}}>Bản dựng xem trước · Không âm thanh</div>
    <div style={{position: 'absolute', left: '35%', right: '35%', bottom: '7.2%', height: 2, backgroundColor: props.palette.navy}}><div style={{height: '100%', width: `${frame / Math.max(1, props.durationInFrames - 1) * 100}%`, backgroundColor: props.palette.gold, opacity: 0.7}}/></div>
  </AbsoluteFill>;
};
