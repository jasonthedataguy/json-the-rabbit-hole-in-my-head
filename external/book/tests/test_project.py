import hashlib
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import build_site
from common import ROOT, PRODUCT_DIRS, read_json, safe_path, validate_project, write_json
from import_reference import original_bytes
from manuscript import render_markdown
from new_chapter import create_chapter

class ProjectTests(unittest.TestCase):
    def test_checked_out_project_structure(self):
        validate_project(ROOT)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / 'templates', self.root / 'templates')
        write_json(self.root / 'book.json', {'chapters': ['story'], 'archive_chapters': [], 'asset_manifest': 'shared/assets.json'})
        write_json(self.root / 'shared/assets.json', {'assets': []})
        self.folder = self.root / 'chapters/story'
        for directory in PRODUCT_DIRS:
            (self.folder / directory).mkdir(parents=True, exist_ok=True)
        self.raw = '# Story\r\n\r\nCơm nguội.\r\n'.encode('utf-8')
        (self.folder / 'source/approved.md').write_bytes(self.raw)
        self.meta = {'slug': 'story', 'number': '00', 'publish': True, 'canonical_text': 'source/approved.md', 'manuscript_sha256': hashlib.sha256(self.raw).hexdigest()}
        write_json(self.folder / 'chapter.json', self.meta)
        write_json(self.folder / 'docs/PRODUCTS.json', {'products': [{'product': 'Selected prose', 'state': 'ready', 'path': 'source/approved.md'}]})

    def test_byte_preserved_manuscript(self):
        validate_project(self.root)
        self.assertEqual((self.folder / 'source/approved.md').read_bytes(), self.raw)

    def test_changed_manuscript_rejected(self):
        (self.folder / 'source/approved.md').write_bytes(self.raw + b'Changed')
        with self.assertRaisesRegex(ValueError, 'hash changed'):
            validate_project(self.root)

    def test_missing_product_rejected(self):
        write_json(self.folder / 'docs/PRODUCTS.json', {'products': [{'path': 'video/missing.mp4'}]})
        with self.assertRaisesRegex(ValueError, 'missing file'):
            validate_project(self.root)

    def test_duplicate_registry_rejected(self):
        registry = read_json(self.root / 'book.json'); registry['chapters'].append('story')
        write_json(self.root / 'book.json', registry)
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            validate_project(self.root)

    def test_paths_cannot_escape(self):
        for path in ('../outside', '/outside', 'C:/outside', 'source/../../outside', '..\\outside'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                safe_path(self.root, path)

    def test_archive_scaffold_is_unpublished_and_cannot_overwrite(self):
        folder = create_chapter(self.root, 'additional-essay', 'Additional essay', archive=True)
        meta = read_json(folder / 'chapter.json')
        self.assertFalse(meta['publish'])
        self.assertIsNone(meta['number'])
        self.assertIsNone(meta['canonical_text'])
        self.assertTrue(all((folder / p).is_dir() for p in PRODUCT_DIRS))
        validate_project(self.root)
        with self.assertRaisesRegex(ValueError, 'already exists'):
            create_chapter(self.root, 'additional-essay', 'Overwrite', archive=True)

    def test_cleanup_refuses_sources_and_unmarked_output(self):
        with patch.object(build_site, 'ROOT', self.root):
            with self.assertRaises(ValueError):
                build_site.generated_directory(self.folder)
            output = self.root / 'dist'; output.mkdir()
            marker = output / 'important.txt'; marker.write_text('keep', encoding='utf-8')
            with self.assertRaises(ValueError):
                build_site.generated_directory(output)
            self.assertEqual(marker.read_text(), 'keep')

    def test_archive_import_reconstructs_only_verified_line_endings(self):
        source = self.folder / 'source/approved.md'
        expected = hashlib.sha256(self.raw.replace(b'\r\n', b'\n')).hexdigest()
        self.assertEqual(original_bytes(source, expected), self.raw.replace(b'\r\n', b'\n'))
        with self.assertRaises(ValueError):
            original_bytes(source, '0' * 64)

    def test_manuscript_html_is_inert(self):
        body, heading, count = render_markdown('# Story\n\n<script>alert(1)</script>\n\n[bad](javascript:alert)')
        self.assertEqual(heading, 'Story')
        self.assertEqual(count, 2)
        self.assertNotIn('<script', body)
        self.assertNotIn('href="javascript:', body)

    def test_payoff_table_is_readable_and_escaped(self):
        source = (
            '# Matrix\n\n'
            '| Move | Payoff |\n'
            '| --- | --- |\n'
            '| Pokes | −20 |\n'
            '| <script> | +10 |\n\n'
            'Game over.'
        )
        body, heading, count = render_markdown(source)
        self.assertEqual((heading, count), ('Matrix', 2))
        self.assertIn('<th scope="col">Move</th>', body)
        self.assertIn('<td>−20</td>', body)
        self.assertIn('&lt;script&gt;', body)
        self.assertNotIn('<script>', body)
        self.assertIn('<p>Game over.</p>', body)

if __name__ == '__main__':
    unittest.main()
