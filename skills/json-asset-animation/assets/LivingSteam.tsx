import React, {useId} from 'react';

export type LivingSteamProps = {
  time: number;
  period?: number;
  width: number;
  height: number;
  color?: string;
  strength?: number;
};

// Source-space, periodic shape deformation. The bottom stays anchored to the vessel.
// No CSS animation, wall clock, random seed, image-generation service or audio.
export const LivingSteam: React.FC<LivingSteamProps> = ({
  time, period = 8, width, height, color = '#F7DFB2', strength = 1,
}) => {
  const id = useId().replace(/:/g, '');
  const phase = 2 * Math.PI * ((time % period + period) % period) / period;
  const ribbons = [0, 1, 2].map(index => {
    const offset = (index - 1) * width * .14;
    const left: [number, number][] = [];
    const right: [number, number][] = [];
    const count = 52;
    for (let step = 0; step <= count; step++) {
      const u = step / count;
      const wave = phase * (index === 1 ? 2 : 1) - u * 8.5 + index * 2.1;
      const x = width * .5 + offset * (1 - .25 * u)
        + Math.sin(wave) * width * .19 * Math.sin(u * Math.PI * .85)
        + Math.sin(phase + index) * width * .06 * u;
      const y = height * (1 - .96 * u);
      const breath = .7 + .3 * Math.sin(phase * 2 - u * 10 + index * 1.8);
      const radius = width * (.035 + index * .008)
        * Math.pow(Math.sin(Math.PI * u), .7) * breath;
      left.push([x - radius, y]);
      right.push([x + radius, y]);
    }
    const path = [...left, ...right.reverse()]
      .map(([x, y], point) => (point ? 'L' : 'M') + x.toFixed(3) + ',' + y.toFixed(3))
      .join(' ') + ' Z';
    // Multiple low-opacity wisps overlap naturally, with no solid stationary S-shape.
    const opacity = strength * (.26 + .08 * Math.sin(phase + index * 2.1));
    return <path key={index} d={path} fill={color} opacity={opacity}/>;
  });
  return <svg width={width} height={height} viewBox={'0 0 ' + width + ' ' + height}
    style={{overflow: 'visible', pointerEvents: 'none'}}>
    <defs>
      <linearGradient id={id + '-fade'} x1="0" y1="1" x2="0" y2="0" gradientUnits="objectBoundingBox">
        <stop offset="0" stopColor="white" stopOpacity=".18"/>
        <stop offset=".18" stopColor="white" stopOpacity="1"/>
        <stop offset=".68" stopColor="white" stopOpacity=".75"/>
        <stop offset="1" stopColor="white" stopOpacity="0"/>
      </linearGradient>
      <mask id={id + '-mask'}>
        <rect width={width} height={height} fill={'url(#' + id + '-fade)'}/>
      </mask>
    </defs>
    <g mask={'url(#' + id + '-mask)'}>{ribbons}</g>
  </svg>;
};
