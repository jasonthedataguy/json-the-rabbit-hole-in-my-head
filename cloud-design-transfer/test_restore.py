import hashlib
import tempfile
import unittest
import zipfile
import json
import os
from pathlib import Path

from restore import restore, safe_target, join_library


class RestoreTests(unittest.TestCase):
    @unittest.skipUnless(os.name == 'nt', 'Windows extended path handling')
    def test_windows_deep_historical_names_can_be_written(self):
        with tempfile.TemporaryDirectory() as directory:
            target = safe_target(Path(directory), '/'.join(['deep-folder-' * 6] * 3) + '/source.png')
            target.parent.mkdir(parents=True)
            target.write_bytes(b'original')
            self.assertEqual(target.read_bytes(), b'original')
            target.unlink()
            parent = target.parent
            for _ in range(3):
                parent.rmdir()
                parent = parent.parent

    def test_binary_parts_recreate_the_exact_original_zip(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = b'byte-exact original archive file'
            checksum = lambda b: hashlib.sha256(b).hexdigest()
            parts = []
            for i, data in enumerate((content[:7], content[7:])):
                name = 'library.zip.part' + str(i)
                (root / name).write_bytes(data)
                parts.append({'name': name, 'bytes': len(data), 'sha256': checksum(data)})
            (root / 'canonical-zip-parts.json').write_text(json.dumps(
                {'name': 'library.zip', 'sha256': checksum(content), 'parts': parts}))
            join_library(root)
            self.assertEqual((root / 'library.zip').read_bytes(), content)
            join_library(root)

    def test_reuses_archive_and_preserves_every_exact_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archives = root / 'archives'
            archives.mkdir()
            bundle = archives / 'library.zip'
            content = b'exact original pixel or text bytes'
            with zipfile.ZipFile(bundle, 'w') as z:
                z.writestr('chapter/master.png', content)
            checksum = lambda b: hashlib.sha256(b).hexdigest()
            rows = [{'path': 'output/a.png', 'sha256': checksum(content), 'archive': bundle.name, 'member': 'chapter/master.png'},
                    {'path': 'output/b.png', 'sha256': checksum(content), 'archive': bundle.name, 'member': 'chapter/master.png'},
                    {'path': 'output/library.zip', 'sha256': checksum(bundle.read_bytes()), 'archive': bundle.name, 'member': None}]
            manifest = {'archives': [{'name': bundle.name, 'sha256': checksum(bundle.read_bytes())}], 'files': rows}
            result = restore(manifest, archives, root / 'restored')
            self.assertEqual(result['restored_files'], 3)
            self.assertEqual((root / 'restored/output/a.png').read_bytes(), content)
            self.assertEqual((root / 'restored/output/library.zip').read_bytes(), bundle.read_bytes())
            self.assertEqual(restore(manifest, archives, root / 'restored')['existing_verified_files'], 3)
            (root / 'restored/output/a.png').write_bytes(b'user changed this')
            with self.assertRaises(ValueError):
                restore(manifest, archives, root / 'restored')
            with self.assertRaises(ValueError):
                safe_target(root, '../outside')


if __name__ == '__main__':
    unittest.main()
