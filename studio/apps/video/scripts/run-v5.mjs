import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';

const app=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
let propsPath=path.join(app,'manifests/com-nguoi-v5.json');
if(!fs.existsSync(propsPath)) throw new Error('Build/stage studio/projects/com-nguoi/video/build_v5.py first.');
const props=JSON.parse(fs.readFileSync(propsPath,'utf8'));
if(props.classification!=='layer_animation' || props.audio.mode!=='silent') throw new Error('V5 requires the staged animated silent review.');
const command=process.argv[2];
if(!['render','still','studio'].includes(command)) throw new Error('Choose render, still or studio.');
const extra=process.argv.slice(3);
const scene=extra.find(x=>x.startsWith('--loop='))?.split('=')[1];
const study=extra.includes('--study');
const forwarded=extra.filter(x=>x!=='--study'&&!x.startsWith('--loop='));
const cache=path.resolve(app,'../../.cache/render/com-nguoi/v5-living-illustrations');
let output=props.outputPath;
if(scene) {
  const gif=props.gif_exports.find(x=>x.scene_id===scene);
  if(!gif) throw new Error('Unknown loop scene.');
  propsPath=path.join(cache,scene+'-loop-props.json');
  fs.writeFileSync(propsPath,JSON.stringify({...props,loopScene:scene},null,2)+'\n');
  output=gif.path.replace(/\.gif$/,'.mp4');
}
if(study) output=path.resolve(app,'../../projects/com-nguoi/video/previews/com-nguoi-v5-opening-and-living-scene-study.mp4');
if(command==='still') output=output.replace(/\.mp4$/,'-cover.png');
const cli=path.join(app,'node_modules/@remotion/cli/remotion-cli.js');
const args=[command,'src/com-nguoi-v5-entry.tsx'];
if(command!=='studio') {
  fs.mkdirSync(path.dirname(output),{recursive:true});
  args.push(scene?'ComNguoiV5Loop':'ComNguoiV5',output,'--timeout=120000');
  if(command==='render') args.push('--codec=h264','--muted','--concurrency=3','--crf=18');
  if(command==='still'&&!forwarded.some(x=>x.startsWith('--frame'))) args.push('--frame='+ (scene?30:390));
  if(command==='render'&&study) args.push('--frames=0-539','--scale=0.5');
}
args.push('--public-dir='+path.join(cache,'public'),'--props='+propsPath,...forwarded);
const result=spawnSync(process.execPath,[cli,...args],{cwd:app,stdio:'inherit'});
if(result.error) throw result.error;
process.exit(result.status??1);
