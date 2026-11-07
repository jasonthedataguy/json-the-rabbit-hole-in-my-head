"""Fashion V1.1 private reader integration: source anchors and locked asset integrity."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "chapters/fashion"
EXPORTS = CHAPTER / "artwork/exports/reader-v1_1"
RUNTIME = ROOT / "shared/web/digital-art.js"
ASSET_MANIFEST = ROOT / "shared/assets.json"
SOURCE = CHAPTER / "source/author-approved-v0.5.md"


def fashion_runtime():
    text = RUNTIME.read_text(encoding="utf-8")
    marker = '  "fashion": '
    assert text.count(marker) == 1, "Fashion entry must be unique"
    start = text.index(marker) + len(marker)
    end = text.index('\n  "flow":', start)
    return json.loads(text[start:end].strip().rstrip(','))


class FashionReaderArtTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.art = fashion_runtime()
        cls.manifest = json.loads(ASSET_MANIFEST.read_text(encoding="utf-8"))
        cls.manuscript = SOURCE.read_text(encoding="utf-8")
        cls.exports = {asset["public_path"]: asset for asset in cls.manifest["assets"]
                       if asset["public_path"].startswith("assets/digital-book/fashion/v1.1/")}

    def test_portal_roles_have_correct_foreground(self):
        art = self.art
        self.assertEqual(art["mainBook"], art["map"])
        self.assertIn("f00-no-foreground.png", art["mainBook"])
        self.assertIn("f00-with-character.webp", art["opening"])
        self.assertIn("f00-hero.webp", art["hero"])
        self.assertIn("f00-centre.webp", art["centre"])
        self.assertNotEqual(art["mainBook"], art["opening"])

    def test_exactly_ten_unique_captioned_manuscript_anchors(self):
        places = self.art["placements"]
        self.assertEqual([x["id"] for x in places], [f"F{i:02}" for i in range(1, 11)])
        positions = []
        for place in places:
            with self.subTest(id=place["id"]):
                self.assertTrue(place["caption"].strip())
                self.assertTrue(place["alt"].strip())
                self.assertTrue(place["anchor"].strip())
                self.assertEqual(self.manuscript.count(place["anchor"]), 1)
                positions.append(self.manuscript.index(place["anchor"]))
                self.assertIn(place["src"].split("?")[0], self.exports)
        self.assertEqual(positions, sorted(positions), "Illustrations must follow manuscript order")

    def test_fourteen_locked_web_assets_are_retrievable_and_exact(self):
        self.assertEqual(len(self.exports), 14)
        self.assertEqual(len({a["public_path"] for a in self.exports.values()}), 14)
        for url, asset in self.exports.items():
            with self.subTest(path=url):
                source = ROOT / asset["source"]
                self.assertTrue(source.is_file(), str(source))
                self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),
                                 asset["sha256_at_intake"])
                raw = source.read_bytes()[:16]
                if source.suffix == ".webp":
                    self.assertEqual(raw[:4], b"RIFF")
                    self.assertEqual(raw[8:12], b"WEBP")
                else:
                    self.assertEqual(raw[:8], b"\x89PNG\r\n\x1a\n")

    def test_fashion_has_dedicated_reader_layout_and_cache_keys(self):
        app = (ROOT / "shared/web/app.js").read_text(encoding="utf-8")
        index = (ROOT / "shared/web/index.html").read_text(encoding="utf-8")
        style = (ROOT / "shared/web/style.css").read_text(encoding="utf-8")
        self.assertIn("if(slug==='fashion'&&Array.isArray(art.placements))", app)
        self.assertIn("Missing Fashion art anchor", app)
        self.assertIn("digital-book-fashion-scene", app)
        self.assertIn("digital-book-fashion-scene", style)
        self.assertIn("app.js?v=82", index)
        self.assertIn("style.css?v=62", index)
        self.assertIn("./digital-art.js?v=4", app)


if __name__ == "__main__":
    unittest.main()
