"""Restore the full canonical Drive artwork ZIP against the studio file hashes."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import zipfile

ROOT=Path(__file__).resolve().parents[1]


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('zip',type=Path)
    args=parser.parse_args()
    manifest=json.loads((ROOT/'cloud/handoff-manifest.json').read_text(encoding='utf-8'))
    expected=[row for row in manifest['files'] if row['root']=='artwork']
    with zipfile.ZipFile(args.zip) as archive:
        index={}
        for member in archive.infolist():
            name=member.filename.replace('\\','/')
            parts=PurePosixPath(name).parts
            if name.startswith('/') or '..' in parts:
                raise ValueError('Unsafe member path in the design archive.')
            if 'json-digital-book-assets/' in name:
                name=name.split('json-digital-book-assets/',1)[1]
            index[name]=member
        for row in expected:
            relative=row['path'].removeprefix('external/artwork/')
            target=(ROOT/row['path']).resolve()
            if not target.is_relative_to(ROOT/'external/artwork'):
                raise ValueError('Artwork target escapes the checkout.')
            if target.is_file():
                if sha(target)!=row['sha256']:
                    raise ValueError('Existing artwork changed; preserve it before restoring: '+relative)
                continue
            if relative not in index:
                raise ValueError('Expected original file missing from archive: '+relative)
            target.parent.mkdir(parents=True,exist_ok=True)
            temporary=target.with_name(target.name+'.restoring')
            with archive.open(index[relative]) as source,temporary.open('wb') as output:
                shutil.copyfileobj(source,output,1024*1024)
            if sha(temporary)!=row['sha256']:
                raise ValueError('Original artwork hash differs: '+relative)
            temporary.replace(target)
    print('Full canonical artwork restored and verified: '+str(len(expected))+' original files.')


if __name__=='__main__':
    main()
