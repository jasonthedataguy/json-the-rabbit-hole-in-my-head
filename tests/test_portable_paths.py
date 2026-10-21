import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from portable_paths import map_paths, resolve_path


class PortablePathTests(unittest.TestCase):
    def setUp(self):
        self.cache=Path(__file__).resolve().parents[1]/'studio/.cache/portable-tests'
        self.cache.mkdir(parents=True,exist_ok=True)

    def test_external_paths_move_but_source_hash_and_release_decisions_do_not(self):
        with tempfile.TemporaryDirectory(dir=self.cache) as directory:
            root=Path(directory).resolve()
            (root/'cloud').mkdir()
            (root/'cloud/local-paths.json').write_text(json.dumps({'mappings':[
                {'original':r'E:\studio','relative':'.'},
                {'original':r'E:\books\.json\outputs\art','relative':'external/artwork'},
                {'original':str(root.parent),'relative':'.'}]}))
            source={'path':r'E:\books\.json\outputs\art\chapter\hero.webp','sha256':'a'*64,
                    'public_release_approved':False,'note':'Keep the words unchanged'}
            mapped=map_paths(source,root)
            self.assertEqual(map_paths('https://example.invalid/chapter',root),'https://example.invalid/chapter')
            self.assertEqual(mapped['path'],str(root/'external/artwork/chapter/hero.webp'))
            self.assertEqual(mapped['sha256'],source['sha256'])
            self.assertEqual(resolve_path(mapped['path'],root),root/'external/artwork/chapter/hero.webp')
            self.assertEqual(resolve_path(root/'already-local.txt',root),root/'already-local.txt')
            self.assertIs(mapped['public_release_approved'],False)
            self.assertEqual(mapped['note'],source['note'])
            self.assertEqual(source['path'],r'E:\books\.json\outputs\art\chapter\hero.webp')
            with self.assertRaises(ValueError):
                resolve_path(r'E:\studio\..\outside.txt',root)

    def test_no_portable_config_leaves_current_production_paths_unchanged(self):
        with tempfile.TemporaryDirectory(dir=self.cache) as directory:
            original={'path':r'E:\books\art\hero.webp','url':'https://example.invalid/chapter'}
            self.assertEqual(map_paths(original,Path(directory)),original)
