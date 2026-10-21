"""Use the existing Git credential helper for this owner's private studio handoff."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import urllib.error
import urllib.request
import urllib.parse
import hashlib
import time
import http.client
import socket

OWNER = 'jasonthedataguy'
NAME = 'json-studio'
ROOT = Path(__file__).resolve().parents[1]


class BufferedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.blocksize=1024*1024

    def connect(self):
        super().connect()
        try:
            self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,4*1024*1024)
        except OSError:
            pass  # Buffer tuning is optional; normal verified TLS remains in use.


class BufferedHTTPSHandler(urllib.request.HTTPSHandler):
    def https_open(self,request):
        options={'context':self._context}
        if hasattr(self,'_check_hostname'):
            options['check_hostname']=self._check_hostname
        return self.do_open(BufferedHTTPSConnection,request,**options)


def enable_fast_uploads():
    urllib.request.install_opener(urllib.request.build_opener(BufferedHTTPSHandler()))


class UploadProgress:
    def __init__(self,stream,name):
        self.stream=stream
        self.name=name
        self.started=time.monotonic()
        self.total=0
        self.next_report=32*1024*1024

    def read(self,size=-1):
        chunk=self.stream.read(size)
        self.total+=len(chunk)
        if self.total>=self.next_report:
            elapsed=max(time.monotonic()-self.started,.001)
            print(self.name+': '+str(round(self.total/1024/1024))+' MiB sent, '+
                  str(round(self.total/1024/1024/elapsed,2))+' MiB/s',flush=True)
            self.next_report+=32*1024*1024
        return chunk


def github_token():
    supplied=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if supplied:
        return supplied
    environment = dict(os.environ, GIT_TERMINAL_PROMPT='0', GCM_INTERACTIVE='never')
    result = subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',
                            capture_output=True,text=True,env=environment)
    if result.returncode:
        raise RuntimeError('Existing GitHub authentication is unavailable; sign in through Git Credential Manager.')
    values = dict(line.split('=',1) for line in result.stdout.splitlines() if '=' in line)
    token = values.get('password')
    if not token:
        raise RuntimeError('Git credential helper did not return usable authentication.')
    return token


def api(token, route, data=None):
    url = 'https://api.github.com'+route
    payload = json.dumps(data).encode() if data is not None else None
    request = urllib.request.Request(url,data=payload,headers={
        'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json',
        'X-GitHub-Api-Version':'2022-11-28','Content-Type':'application/json',
        'User-Agent':'json-studio-private-handoff',
    })
    with urllib.request.urlopen(request,timeout=60) as response:
        return json.load(response)


def private_repository(token):
    try:
        repository=api(token,'/repos/'+OWNER+'/'+NAME)
    except urllib.error.HTTPError as error:
        if error.code!=404:
            raise
        repository=api(token,'/user/repos',{'name':NAME,'private':True,'auto_init':False,
                                          'description':'Private .json publishing studio, living artwork and portable iPad/Codespaces workspace.'})
    if not repository['private'] or repository['owner']['login'].lower()!=OWNER:
        raise RuntimeError('Refuse upload: destination is not the requested owner’s private studio repository.')
    return repository


def publish(token,account):
    out=ROOT/'.handoff'
    checkout=out/'repository'
    manifest_path=checkout/'cloud/handoff-manifest.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    verification=json.loads((out/'verification.json').read_text(encoding='utf-8'))
    checksum=lambda path:hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if verification['status']!='pass' or verification['manifest_sha256']!=checksum(manifest_path):
        raise RuntimeError('Complete the relocated-checkout audit before uploading.')
    repository=private_repository(token)
    env=dict(os.environ,GIT_TERMINAL_PROMPT='0',GCM_INTERACTIVE='never')
    def git(*args,check=True):
        result=subprocess.run(['git','-C',str(checkout),*args],capture_output=True,text=True,env=env)
        if check and result.returncode:
            raise RuntimeError('Git operation failed: '+result.stderr[-1800:])
        return result
    if not (checkout/'.git').exists():
        git('init','-b','main')
        git('config','user.name',account.get('name') or OWNER)
        git('config','user.email',str(account['id'])+'+'+OWNER+'@users.noreply.github.com')
        git('config','core.autocrlf','false')
        git('remote','add','origin',repository['clone_url'])
    if git('remote','get-url','origin').stdout.strip()!=repository['clone_url']:
        raise RuntimeError('Handoff Git remote differs from the selected private repository.')
    wanted=[row['path'] for row in manifest['files'] if row['storage']=='git']+['cloud/handoff-manifest.json']
    pathspec=out/'git-pathspec'
    pathspec.write_bytes(('\0'.join(wanted)+'\0').encode('utf-8'))
    git('add','--force','--pathspec-from-file='+str(pathspec),'--pathspec-file-nul')
    tracked=git('ls-files','-z').stdout.split('\0')
    if set(filter(None,tracked))!=set(wanted):
        raise RuntimeError('Git staging differs from the reviewed code-only package.')
    if git('diff','--cached','--quiet',check=False).returncode:
        git('commit','-m','Add private studio, complete v5 handoff and portable asset restore')
    git('push','--set-upstream','origin','main')
    commit=git('rev-parse','HEAD').stdout.strip()
    print('Private code pushed: '+repository['html_url']+' @ '+commit,flush=True)
    tag=manifest['asset_release_tag']
    route='/repos/'+OWNER+'/'+NAME+'/releases'
    try:
        release=api(token,route+'/tags/'+tag)
    except urllib.error.HTTPError as error:
        if error.code!=404:
            raise
        release=api(token,route,{'tag_name':tag,'target_commitish':commit,'name':'Private studio working snapshot — Cơm nguội v5',
                                'draft':False,'prerelease':True,
                                'body':'Private cross-device production handoff, not a public chapter release. Complete artwork and media are in hash-deduplicated bundles; restore through cloud/bootstrap.py. Artistic/public/paid approval remains pending. Current v5 MP4 and GIFs are attached separately for review.'})
    attachments=[(out/manifest.get('local_bundle_directory','assets')/a['name'],a['sha256']) for a in manifest['archives']]
    attachments.append((manifest_path,checksum(manifest_path)))
    project=ROOT/'studio/projects/com-nguoi'
    attachments.extend((p,checksum(p)) for p in [
        project/'video/exports/com-nguoi-v5-living-illustrations-silent-review-1080x1920.mp4',
        project/'animation/v5/exports/com-nguoi-v5-dinner-living.gif',
        project/'animation/v5/exports/com-nguoi-v5-child-living.gif'])
    assets={item['name']:item for item in api(token,route+'/'+str(release['id'])+'/assets?per_page=100')}
    results=[]
    for path,expected in attachments:
        asset=assets.get(path.name)
        if asset is None:
            upload=release['upload_url'].split('{',1)[0]+'?name='+urllib.parse.quote(path.name)
            if urllib.parse.urlparse(upload).hostname!='uploads.github.com':
                raise RuntimeError('Unexpected upload host.')
            print('Uploading '+path.name+' ('+str(path.stat().st_size)+' bytes)',flush=True)
            with path.open('rb') as stream:
                request=urllib.request.Request(upload,data=UploadProgress(stream,path.name),method='POST',headers={
                    'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json',
                    'Content-Type':'application/octet-stream','Content-Length':str(path.stat().st_size),
                    'User-Agent':'json-studio-private-handoff'})
                with urllib.request.urlopen(request,timeout=3600) as response:
                    asset=json.load(response)
        if asset['size']!=path.stat().st_size or asset.get('state')!='uploaded':
            raise RuntimeError('Remote asset size/state did not verify: '+path.name)
        remote_digest=asset.get('digest')
        if remote_digest and remote_digest!='sha256:'+expected:
            raise RuntimeError('Remote digest differs: '+path.name)
        results.append({'name':path.name,'bytes':asset['size'],'sha256':expected,'remote_digest':remote_digest,
                        'url':asset['browser_download_url'],'verified':True})
        print('Verified '+path.name,flush=True)
    # Verify the destination is still private and branch identity is the pushed commit.
    remote=api(token,'/repos/'+OWNER+'/'+NAME)
    branch=api(token,'/repos/'+OWNER+'/'+NAME+'/branches/main')
    assert remote['private'] and branch['commit']['sha']==commit
    receipt={'status':'uploaded_verified','repository':remote['html_url'],'private':True,'commit':commit,
             'release':release['html_url'],'assets':results,'summary':manifest['summary'],
             'codespaces_url':'https://github.com/codespaces/new?repo='+str(remote['id']),
             'public_book_changed':False,'public_story_release_approved':False}
    (out/'upload-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,ensure_ascii=False,indent=2))


def main():
    enable_fast_uploads()
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['inspect','publish'])
    args=parser.parse_args()
    token=github_token()
    account=api(token,'/user')
    if account['login'].lower()!=OWNER:
        raise RuntimeError('Authenticated owner differs from the requested jasonthedataguy account.')
    if args.command=='publish':
        publish(token,account)
        return
    repos=[]
    for page in range(1,5):
        items=api(token,'/user/repos?affiliation=owner&per_page=100&page='+str(page))
        repos.extend({'name':item['full_name'],'private':item['private'],'url':item['html_url']}
                     for item in items if any(term in item['name'].lower() for term in ('json','studio','book')))
        if len(items)<100:
            break
    print(json.dumps({'authenticated_account':account['login'],'relevant_repositories':repos},indent=2))


if __name__=='__main__':
    try:
        main()
    except urllib.error.HTTPError as error:
        raise SystemExit('GitHub API request failed with HTTP '+str(error.code)+'. No credentials were printed.')
    except Exception as error:
        raise SystemExit(str(error))
