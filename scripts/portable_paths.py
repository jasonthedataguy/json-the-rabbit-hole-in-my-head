"""Resolve a cloud checkout's external snapshots without rewriting signed JSON bytes."""
import json
from functools import lru_cache
from pathlib import Path, PurePosixPath
import shutil

ROOT = Path(__file__).resolve().parents[1]


@lru_cache(maxsize=8)
def mappings(root):
    root = Path(root).resolve()
    config = root/'cloud/local-paths.json'
    if not config.is_file():
        return ()
    rows = json.loads(config.read_text(encoding='utf-8'))['mappings']
    result = []
    for row in rows:
        target = (root/row['relative']).resolve()
        if not target.is_relative_to(root):
            raise ValueError('Portable snapshot target escapes this checkout.')
        result.append((row['original'].replace('\\','/').rstrip('/'),target))
    return tuple(sorted(result,key=lambda row:len(row[0]),reverse=True))


def resolve_path(value, root=None):
    root = Path(root or ROOT).resolve()
    native = Path(value)
    if native.is_absolute() and native.resolve().is_relative_to(root):
        return native.resolve()
    text = str(value)
    normalized = text.replace('\\','/')
    for prefix,target in mappings(str(root)):
        if normalized.casefold()==prefix.casefold():
            return target
        if normalized.casefold().startswith(prefix.casefold()+'/'):
            suffix = PurePosixPath(normalized[len(prefix)+1:])
            if '..' in suffix.parts:
                raise ValueError('Portable source path traverses outside its snapshot.')
            return target.joinpath(*suffix.parts)
    return Path(value)


def map_paths(value, root=None):
    if isinstance(value,dict):
        return {key:map_paths(item,root) for key,item in value.items()}
    if isinstance(value,list):
        return [map_paths(item,root) for item in value]
    if isinstance(value,str):
        normalized=value.replace('\\','/').casefold()
        active=mappings(str(Path(root or ROOT).resolve()))
        if any(normalized==prefix.casefold() or normalized.startswith(prefix.casefold()+'/')
               for prefix,_ in active):
            return str(resolve_path(value,root))
        return value
    return value


def runtime_binary(name):
    found = shutil.which(name)
    if found:
        return found
    bundled = ROOT/'studio/apps/video/node_modules/@remotion/compositor-win32-x64-msvc'/(name+'.exe')
    if bundled.is_file():
        return str(bundled)
    raise FileNotFoundError('Install '+name+' in the development environment.')
