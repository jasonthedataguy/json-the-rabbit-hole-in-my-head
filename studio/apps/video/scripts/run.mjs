import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';

const app = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const propsPath = path.join(app, 'manifests', 'active-preview.json');
if (!fs.existsSync(propsPath)) throw new Error('Run python scripts/studio.py prepare-video <stable-slug> from the workspace first.');
const props = JSON.parse(fs.readFileSync(propsPath, 'utf8'));
if (props.renderKind !== 'internal_preview') throw new Error('Only internal review previews are supported.');
const command = process.argv[2];
if (!['studio', 'render', 'still'].includes(command)) throw new Error('Choose studio, render or still.');
const pkgPath = path.join(app, 'node_modules', '@remotion', 'cli', 'package.json');
if (!fs.existsSync(pkgPath)) throw new Error('Install the pinned video-app dependencies first: npm ci');
const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
const bin = typeof pkg.bin === 'string' ? pkg.bin : pkg.bin.remotion;
const cli = path.join(path.dirname(pkgPath), bin);
const args = [command, 'src/index.ts'];
const extra = process.argv.slice(3);
if (command !== 'studio') {
  const output = command === 'still' ? props.outputPath.replace(/\.mp4$/, '-cover.png') : props.outputPath;
  fs.mkdirSync(path.dirname(output), {recursive: true});
  args.push('ChapterVideo', output);
  if (command === 'render') args.push('--codec=h264');
  else if (!extra.some((arg) => arg.startsWith('--frame'))) args.push('--frame=45');
}
args.push(`--public-dir=${props.publicDir}`, `--props=${propsPath}`, ...extra);
const result = spawnSync(process.execPath, [cli, ...args], {cwd: app, stdio: 'inherit'});
if (result.error) throw result.error;
process.exit(result.status ?? 1);
