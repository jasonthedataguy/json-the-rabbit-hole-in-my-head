import React from 'react';
import {Composition} from 'remotion';
import {ChapterVideo, type PreviewProps} from './video';
import active from '../manifests/active-preview.json';

const props = active as PreviewProps;
export const RemotionRoot: React.FC = () => (
  <Composition
    id="ChapterVideo"
    component={ChapterVideo}
    width={props.format.width}
    height={props.format.height}
    fps={props.format.fps}
    durationInFrames={props.durationInFrames}
    defaultProps={props}
    calculateMetadata={({props: input}) => ({
      width: input.format.width,
      height: input.format.height,
      fps: input.format.fps,
      durationInFrames: input.durationInFrames,
    })}
  />
);
