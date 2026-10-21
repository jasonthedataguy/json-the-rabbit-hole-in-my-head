import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';

const app=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const propsPath=path.join(app,'manifests/com-nguoi-v4.json');
if(!fs.existsSync(propsPath)) throw new Error('Build/stage Cơm nguội v4 first: studio/projects/com-nguoi/video/build_v4.py');
const props=JSON.parse(fs.readFileSync(propsPath,'utf8'));
if(props.classification!=='layer_animation' || props.audio.mode!=='silent') throw new Error('This runner exports only the selected animated silent review.');
const command=process.argv[2];
if(!['render','still','studio'].includes(command)) throw new Error('Choose render, still or studio.');
const extra=process.argv.slice(3);
const study=extra.includes('--study');
const forwarded=extra.filter(x=>x!=='--study');
const publicDir=path.resolve(app,'../../.cache/render/com-nguoi/v4-layer-animation/public');
let output=props.outputPath;
if(study) output=path.resolve(app,'../../projects/com-nguoi/video/previews/com-nguoi-v4-opening-and-motion-study.mp4');
if(command==='still') output=output.replace(/\.mp4$/,'-cover.png');
const cli=path.join(app,'node_modules/@remotion/cli/remotion-cli.js');
const args=[command,'src/com-nguoi-v4-entry.tsx'];
if(command!=='studio') {
  fs.mkdirSync(path.dirname(output),{recursive:true});
  args.push('ComNguoiV4',output,'--timeout=120000');
  if(command==='render') args.push('--codec=h264','--muted','--concurrency=3','--crf=18');
  if(command==='still'&&!forwarded.some(x=>x.startsWith('--frame'))) args.push('--frame=390');
  if(command==='render'&&study) args.push('--frames=0-539','--scale=0.5');
}
args.push('--public-dir='+publicDir,'--props='+propsPath,...forwarded);
const result=spawnSync(process.execPath,[cli,...args],{cwd:app,stdio:'inherit'});
if(result.error) throw result.error;
process.exit(result.status??1);
