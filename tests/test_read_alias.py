"""Regression checks for Instagram-safe, first-party chapter reading links."""
import json
import unittest
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ALIAS = ROOT / "shared/web/read/com-nguoi/index.html"
CHAPTER = ROOT / "chapters/com-nguoi/chapter.json"
BUILDER = ROOT / "scripts/build_site.py"
PROJECT_URL = "https://jasonthedataguy.github.io/json-the-rabbit-hole-in-my-head/"


class ReadAliasTests(unittest.TestCase):
    def test_alias_resolves_to_the_existing_chapter(self):
        html = ALIAS.read_text(encoding="utf-8")
        chapter = json.loads(CHAPTER.read_text(encoding="utf-8"))
        self.assertEqual(chapter["canonical_path"], "#chapter/00")
        self.assertEqual(chapter["slug"], "com-nguoi")
        self.assertIn('content="0;url=../../#chapter/00"', html)
        self.assertIn('href="../../#chapter/00"', html)
        self.assertIn('destination.hash = "chapter/00"', html)
        self.assertIn("window.location.replace(destination.href)", html)

        # A bare profile URL has no hash; relative navigation adds the hash
        # only after the Instagram-safe page has loaded.
        profile_url = urljoin(PROJECT_URL, "read/com-nguoi/")
        self.assertEqual(urlsplit(profile_url).fragment, "")
        destination = urljoin(profile_url, "../../#chapter/00")
        self.assertEqual(destination, PROJECT_URL + "#chapter/00")

    def test_build_includes_the_isolated_read_tree(self):
        script = BUILDER.read_text(encoding="utf-8")
        self.assertIn("copy_public_tree(ROOT / 'shared/web/read', staging / 'read')", script)


if __name__ == "__main__":
    unittest.main()
