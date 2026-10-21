"""Upload a resumable, verified complete-design fallback to the owner's private repo."""
import hashlib
import http.client
import json
import os
from pathlib import Path
import subprocess
import time
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '.design-handoff'
REPOSITORY = 'jasonthedataguy/json-studio'
TAG = 'json-design-archive-2026-10-21'


def digest(path):
    with Path(path).open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def credentials():
    result = subprocess.run(['git', 'credential', 'fill'],
                            input='protocol=https\nhost=github.com\n\n', text=True,
                            capture_output=True, check=True,
                            env=dict(os.environ, GIT_TERMINAL_PROMPT='0', GCM_INTERACTIVE='never'))
    fields = dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)
    if not fields.get('password'):
        raise RuntimeError('Existing GitHub authentication unavailable.')
    return fields['password']


def api(token, route, body=None):
    request = urllib.request.Request('https://api.github.com' + route,
        data=json.dumps(body).encode() if body is not None else None,
        headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json',
                 'X-GitHub-Api-Version': '2022-11-28', 'Content-Type': 'application/json',
                 'User-Agent': 'json-private-design-backup'})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def partitions(source, checksum, size=1024**3):
    parts = []
    with source.open('rb') as stream:
        offset = 0
        while offset < source.stat().st_size:
            weight = min(size, source.stat().st_size - offset)
            sha = hashlib.sha256()
            remaining = weight
            while remaining:
                block = stream.read(min(4 * 1024**2, remaining))
                if not block:
                    raise ValueError('Library ZIP changed during partitioning.')
                sha.update(block)
                remaining -= len(block)
            parts.append({'name': source.name + '.part' + str(len(parts) + 1).zfill(3),
                          'bytes': weight, 'sha256': sha.hexdigest(), 'offset': offset})
            offset += weight
    return {'name': source.name, 'bytes': source.stat().st_size, 'sha256': checksum,
            'parts': parts, 'note': 'Concatenate parts in order to recreate the exact original ZIP.'}


def upload(token, release, source, item):
    start = time.monotonic()
    address = urllib.parse.urlsplit(release['upload_url'].split('{')[0])
    if address.hostname != 'uploads.github.com':
        raise ValueError('Unexpected upload host.')
    connection = http.client.HTTPSConnection(address.hostname, timeout=300)
    connection.putrequest('POST', address.path + '?name=' + urllib.parse.quote(item['name']))
    for name, value in {'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json',
                        'User-Agent': 'json-private-design-backup', 'Content-Type': 'application/octet-stream',
                        'Content-Length': str(item['bytes'])}.items():
        connection.putheader(name, value)
    connection.endheaders()
    sha = hashlib.sha256()
    sent = 0
    next_report = time.monotonic() + 45
    with source.open('rb') as stream:
        stream.seek(item.get('offset', 0))
        while sent < item['bytes']:
            block = stream.read(min(4 * 1024**2, item['bytes'] - sent))
            if not block:
                raise ValueError('Local upload source changed.')
            connection.send(block)
            sha.update(block)
            sent += len(block)
            if time.monotonic() >= next_report:
                print(item['name'] + ': ' + str(round(sent / item['bytes'] * 100)) + '% sent', flush=True)
                next_report = time.monotonic() + 45
    response = connection.getresponse()
    body = response.read()
    connection.close()
    if response.status != 201:
        raise RuntimeError('GitHub upload returned HTTP ' + str(response.status) + ' for ' + item['name'])
    record = json.loads(body)
    if sha.hexdigest() != item['sha256'] or record.get('digest') != 'sha256:' + item['sha256']:
        raise ValueError('Local/remote upload digest mismatch: ' + item['name'])
    if record['size'] != item['bytes'] or record['state'] != 'uploaded':
        raise ValueError('Remote upload incomplete: ' + item['name'])
    elapsed = time.monotonic() - start
    print(item['name'] + ': verified ' + str(round(sent / 1024**2 / elapsed, 2)) + ' MiB/s', flush=True)
    return {key: record[key] for key in ('name', 'id', 'size', 'digest', 'browser_download_url', 'state')}


def main():
    token = credentials()
    account = api(token, '/user')
    repo = api(token, '/repos/' + REPOSITORY)
    if account['login'].lower() != 'jasonthedataguy' or not repo['private']:
        raise RuntimeError('Expected authenticated owner and private repository; no upload performed.')
    manifest = json.loads((OUT / 'artwork-manifest.json').read_text(encoding='utf-8'))
    baseline = Path('E:/books/.json/outputs/json-digital-book-assets.zip')
    expected = manifest['archives'][0]['sha256']
    if digest(baseline) != expected:
        raise ValueError('Current library ZIP no longer matches the prepared archive.')
    part_index = partitions(baseline, expected)
    parts_path = OUT / 'uploads/canonical-zip-parts.json'
    parts_path.write_text(json.dumps(part_index, indent=2) + '\n', encoding='utf-8')
    releases = api(token, '/repos/' + REPOSITORY + '/releases?per_page=100')
    release = next((r for r in releases if r['tag_name'] == TAG), None)
    if release is None:
        release = api(token, '/repos/' + REPOSITORY + '/releases', {
            'tag_name': TAG, 'target_commitish': repo['default_branch'], 'draft': True,
            'name': 'Complete private design archive — 2026-10-21',
            'body': 'Private backup of all artwork, original boards and generation sources. '
                    'Download all assets and run restore-artwork.py as described in READ-ME-FIRST.md. '
                    'The large current-library ZIP is split into exact binary parts, automatically joined by the restore helper. '
                    'This is a private backup snapshot; no public or paid book release is approved.'})
    existing = {r['name']: r for r in api(token, '/repos/' + REPOSITORY + '/releases/' + str(release['id']) + '/assets?per_page=100')}
    entries = [(baseline, item) for item in part_index['parts']]
    # Small recovery files first; never upload another full copy of the large ZIP.
    local_files = sorted((OUT / 'uploads').iterdir(), key=lambda p: (p.suffix == '.zip', p.name))
    for path in local_files:
        if not path.is_file() or path.name == baseline.name:
            continue
        entries.append((path, {'name': path.name, 'bytes': path.stat().st_size, 'sha256': digest(path)}))
    receipt = {'repository': REPOSITORY, 'release_url': release['html_url'], 'release_id': release['id'],
               'status': 'uploading', 'visibility': 'private', 'assets': []}
    receipt_path = OUT / 'github-design-receipt.json'
    for source, item in entries:
        remote = existing.get(item['name'])
        if remote:
            if remote.get('digest') != 'sha256:' + item['sha256'] or remote['size'] != item['bytes']:
                raise ValueError('An existing remote asset differs; preserve/review it: ' + item['name'])
            record = {key: remote[key] for key in ('name', 'id', 'size', 'digest', 'browser_download_url', 'state')}
            print(item['name'] + ': existing remote hash verified', flush=True)
        else:
            record = upload(token, release, source, item)
        receipt['assets'].append(record)
        receipt_path.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    # A private repository stays private; this makes the finished backup visible to its owner.
    request = urllib.request.Request('https://api.github.com/repos/' + REPOSITORY + '/releases/' + str(release['id']),
        data=json.dumps({'draft': False}).encode(), method='PATCH',
        headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json',
                 'Accept': 'application/vnd.github+json', 'User-Agent': 'json-private-design-backup'})
    with urllib.request.urlopen(request, timeout=60) as response:
        finished = json.load(response)
    receipt.update(status='complete', release_url=finished['html_url'],
                   verified_assets=len(receipt['assets']), total_bytes=sum(a['size'] for a in receipt['assets']))
    receipt_path.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in receipt.items() if k != 'assets'}, indent=2), flush=True)


if __name__ == '__main__':
    main()
