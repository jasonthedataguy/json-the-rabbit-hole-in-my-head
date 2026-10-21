import React from 'react';
import {Composition, getInputProps, registerRoot} from 'remotion';
import {ComNguoiV5, ComNguoiV5Loop, type V5Props} from './com-nguoi-v5';
const props=getInputProps() as unknown as V5Props;
const Root: React.FC=()=> {
  if(!props.assets || !props.timeline) throw new Error('Build/stage v5 and supply its --props file.');
  return <>
    <Composition id="ComNguoiV5" component={ComNguoiV5} width={props.width} height={props.height} fps={props.fps} durationInFrames={Math.round(props.duration_s*props.fps)} defaultProps={props}/>
    <Composition id="ComNguoiV5Loop" component={ComNguoiV5Loop} width={960} height={640} fps={25} durationInFrames={200} defaultProps={props}/>
  </>;
};
registerRoot(Root);
