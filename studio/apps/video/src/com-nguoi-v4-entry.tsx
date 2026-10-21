import React from 'react';
import {Composition, getInputProps, registerRoot} from 'remotion';
import {ComNguoiV4, type V4Props} from './com-nguoi-v4';
const props=getInputProps() as unknown as V4Props;
const Root: React.FC=()=> {
  if(!props.assets || !props.timeline) throw new Error('Build and stage v4, then open this composition with its --props file.');
  return <Composition id="ComNguoiV4" component={ComNguoiV4} width={props.width} height={props.height} fps={props.fps} durationInFrames={Math.round(props.duration_s*props.fps)} defaultProps={props}/>;
};
registerRoot(Root);
