"""Inspect selected art; validate independent motion; stage private render inputs."""
import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import sys
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'scripts'))
from portable_paths import map_paths, resolve_path


def sha(path):
    with resolve_path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def load(path):
    return map_paths(json.loads(resolve_path(path).read_text(encoding='utf-8')))


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def inspect(path):
    path = Path(path).resolve()
    with Image.open(path) as im:
        alpha = im.getchannel('A') if 'A' in im.getbands() else None
        histogram = alpha.histogram() if alpha else None
        return {'path': str(path), 'sha256': sha(path), 'width': im.width, 'height': im.height,
                'mode': im.mode, 'alpha_extrema': list(alpha.getextrema()) if alpha else None,
                'visible_bbox': list(alpha.getbbox()) if alpha and alpha.getbbox() else None,
                'transparent_fraction': histogram[0] / (im.width * im.height) if histogram else 0,
                'warning': 'Inspect actual edges, internal holes, sharpness and baked objects; alpha is not proof of a clean layer.' if alpha else 'Opaque plane/base; not a separated object cutout.'}


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def check_manifest(data, allowed_roots):
    errors, warnings = [], []
    def fail(message):
        errors.append(message)
    source = Path(data['source']['path'])
    if not source.is_file() or sha(source) != data['source']['sha256']:
        return {'status': 'fail', 'errors': ['Script source missing or stale'], 'warnings': []}
    title = next((line.lstrip('#').strip() for line in source.read_text(encoding='utf-8').splitlines() if line.startswith('#')), '')
    if data.get('classification') != 'layer_animation':
        fail('This checker accepts layer_animation, not a camera-only reading cut')
    if any(not finite(data.get(k)) or data[k] <= 0 for k in ('width', 'height', 'fps', 'duration_s')):
        return {'status': 'fail', 'errors': ['Canvas, fps and duration must be positive finite numbers'], 'warnings': []}
    opening = data['opening']
    if opening.get('title') != title:
        fail('Opening title must match the selected source heading')
    times = [opening.get(k) for k in ('title_hold_s', 'entry_end_s', 'story_start_s')]
    if not all(finite(t) for t in times) or not (0 < times[0] < times[1] < times[2] < data['duration_s']):
        return {'status': 'fail', 'errors': errors + ['Opening must hold title, enter center, reveal scene, then start story'], 'warnings': warnings}
    if any(not finite(opening.get(k)) or not 0 <= opening[k] <= 1 for k in ('focus_x', 'focus_y')):
        fail('Opening focus must lie inside the artwork')
    assets = {}
    for asset in data['assets']:
        identifier, path = asset['id'], Path(asset['path']).resolve()
        if identifier in assets:
            fail('Duplicate asset id: ' + identifier)
        assets[identifier] = asset
        if not any(path.is_relative_to(Path(root).resolve()) for root in allowed_roots):
            fail('Asset outside trusted library/project derivative roots: ' + identifier)
            continue
        if not path.is_file() or sha(path) != asset['sha256']:
            fail('Asset missing or stale: ' + identifier)
            continue
        info = inspect(path)
        if len(allowed_roots) > 1 and path.is_relative_to(Path(allowed_roots[1]).resolve()):
            provenance = asset.get('provenance') or {}
            parent = Path(provenance.get('source_path', ''))
            if (not provenance.get('operation') or not parent.is_file()
                    or not parent.resolve().is_relative_to(Path(allowed_roots[0]).resolve())
                    or sha(parent) != provenance.get('source_sha256')):
                fail('Project derivative requires original library source/hash and operation: ' + identifier)
        if asset.get('role') == 'cutout' and (info['alpha_extrema'] is None or info['transparent_fraction'] == 0):
            fail('Declared cutout has no transparent pixels: ' + identifier)
        if asset.get('role') == 'cutout':
            warnings.append(identifier + ': actual matte quality needs visual review')
    for key in ('portal_asset', 'reveal_asset'):
        if opening.get(key) not in assets:
            fail('Opening references missing asset: ' + key)
    signatures, moving, identifiers = set(), [], set()
    story_duration = data['duration_s'] - opening['story_start_s']
    for layer in data['layers']:
        identifier = layer['id']
        if identifier in identifiers:
            fail('Duplicate layer id: ' + identifier)
        identifiers.add(identifier)
        kind = layer.get('kind', 'image')
        if kind == 'image' and layer.get('asset_id') not in assets:
            fail('Layer references missing asset: ' + identifier)
        if kind not in ('image', 'glow', 'steam'):
            fail('Unsupported scene layer kind: ' + identifier)
        if any(not finite(layer.get(k)) for k in ('x', 'y', 'width', 'height', 'z')) or layer.get('width', 0) <= 0 or layer.get('height', 0) <= 0:
            fail('Invalid layer placement: ' + identifier)
        if any(not finite(layer.get(k, .5)) or not 0 <= layer.get(k, .5) <= 1 for k in ('pivot_x', 'pivot_y')):
            fail('Invalid layer pivot: ' + identifier)
        signature = []
        for prop, keys in layer.get('tracks', {}).items():
            if prop not in ('x', 'y', 'rotation', 'scale', 'opacity') or not keys:
                fail('Unsupported/empty animation track: ' + identifier + '/' + prop)
                continue
            if any(not finite(k.get('t')) or not finite(k.get('value')) for k in keys):
                fail('Nonfinite keyframe: ' + identifier)
                continue
            if any(not 0 <= k['t'] <= story_duration or k.get('ease', 'smooth') not in ('linear', 'smooth') for k in keys) or any(b['t'] <= a['t'] for a, b in zip(keys, keys[1:])):
                fail('Keyframes must increase within story time: ' + identifier)
            if prop == 'opacity' and any(not 0 <= k['value'] <= 1 for k in keys):
                fail('Opacity out of range: ' + identifier)
            if prop == 'scale' and any(not 0 < k['value'] <= 8 for k in keys):
                fail('Scale out of range: ' + identifier)
            values = [k['value'] for k in keys]
            opacity_keys = layer.get('tracks', {}).get('opacity', [])
            visible_opacity = any(k.get('value', 0) > 0 for k in opacity_keys) if opacity_keys else layer.get('base', {}).get('opacity', 1) > 0
            if len(set(values)) > 1 and visible_opacity:
                # Ignore initial offsets: two images in identical lockstep are not independent motion.
                signature.append((prop, tuple((k['t'], round(k['value'] - values[0], 6)) for k in keys)))
        if signature:
            positions = {key: [k['value'] for k in layer.get('tracks', {}).get(key, [])] or [layer.get('base', {}).get(key, layer[key])] for key in ('x', 'y')}
            if (max(positions['x']) + layer['width'] <= 0 or min(positions['x']) >= data['width']
                    or max(positions['y']) + layer['height'] <= 0 or min(positions['y']) >= data['height']):
                warnings.append(identifier + ': moving layer is outside the canvas and cannot count as visible animation')
            else:
                moving.append(identifier)
                signatures.add(tuple(sorted(signature)))
    if len(moving) < 2 or len(signatures) < 2:
        fail('Dynamic scene needs at least two independently moving visible elements; shared camera/text/lockstep movement is insufficient')
    if data.get('audio', {}).get('mode') != 'silent':
        fail('Reference scene component supports silent review only; author audio needs an implemented verified audio handoff')
    if any(data.get(k) is not False for k in ('author_quality_approved', 'public_release_approved', 'paid_release_approved')):
        fail('Draft motion manifests cannot grant author quality/public/paid approval')
    return {'status': 'fail' if errors else 'pass', 'errors': errors, 'warnings': warnings, 'moving_layers': moving, 'independent_signatures': len(signatures), 'interpretation': 'Technical preflight, not artistic quality, consent or release approval'}


def stage_file(source, target):
    source, target = Path(source), Path(target)
    if target.exists():
        if sha(source) != sha(target):
            raise ValueError('Existing cache differs; refuse overwrite: ' + str(target))
        return 'existing'
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.link(source, target)
        mode = 'hardlink'
    except OSError:
        shutil.copy2(source, target)
        mode = 'private_render_copy'
    if sha(source) != sha(target):
        raise ValueError('Input changed during staging')
    return mode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    audit = sub.add_parser('inspect')
    audit.add_argument('inputs', nargs='+')
    audit.add_argument('--output', required=True)
    for command in ('check', 'stage'):
        item = sub.add_parser(command)
        item.add_argument('manifest')
        item.add_argument('--studio', default=str(Path(__file__).resolve().parents[3]))
        if command == 'stage':
            item.add_argument('--output', required=True)
    args = parser.parse_args()
    if args.command == 'inspect':
        paths = []
        for value in args.inputs:
            path = Path(value)
            paths.extend(sorted(p for p in path.iterdir() if p.suffix.lower() in ('.png', '.webp', '.jpg', '.jpeg')) if path.is_dir() else [path])
        if len(paths) > 64:
            raise ValueError('Select at most 64 explicit images; do not mirror the book library')
        result = {'assets': [inspect(p) for p in dict.fromkeys(paths)], 'source_files_modified': False}
        save(args.output, result)
        print(json.dumps({'inspected': len(result['assets']), 'report': args.output}))
        return 0
    data = load(args.manifest)
    root = Path(args.studio).resolve()
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', data['story_slug']):
        raise ValueError('Use a stable chapter slug')
    cfg = load(root / 'studio/studio.json')
    roots = [Path(cfg['asset_library']), root / 'studio/projects' / data['story_slug'] / 'animation']
    result = check_manifest(data, roots)
    if result['errors'] or args.command == 'check':
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result['errors'] else 0
    output = Path(args.output).resolve()
    if any(output == p or output.is_relative_to(p) for p in roots):
        raise ValueError('Stage in a separate private cache, not the artwork/derived-assets source directory')
    props = copy.deepcopy(data)
    inputs = []
    for asset in props['assets']:
        path = Path(asset['path'])
        filename = asset['sha256'][:20] + path.suffix.lower()
        mode = stage_file(path, output / 'public' / filename)
        asset['imageSrc'] = filename
        inputs.append({'source': str(path), 'sha256': asset['sha256'], 'mode': mode})
    font = Path(cfg['book_repository']) / 'shared/fonts/Noto-Serif.ttf'
    font_name = 'noto-serif-' + sha(font)[:12] + '.ttf'
    stage_file(font, output / 'public' / font_name)
    stage_file(font.with_name('Noto-Serif-OFL.txt'), output / 'public/Noto-Serif-OFL.txt')
    props['fontSrc'] = font_name
    save(output / 'render-props.json', props)
    save(output / 'staging.json', {'manifest': str(Path(args.manifest).resolve()), 'manifest_sha256': sha(args.manifest), 'inputs': inputs, 'source_changes_allowed': False, 'public_dir': str(output / 'public')})
    print(json.dumps({'status': 'staged_internal_animation', 'props': str(output / 'render-props.json'), 'public_dir': str(output / 'public'), 'release_approved': False}, indent=2))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('ERROR: ' + str(exc))
        raise SystemExit(1)
