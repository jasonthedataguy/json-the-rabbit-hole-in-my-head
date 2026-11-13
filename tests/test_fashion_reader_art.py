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
        self.assertIn("v1.2/f00-without-character-transparent.webp", art["mainBook"])
        self.assertIn("v1.2/f00-with-character-transparent.webp", art["opening"])
        self.assertIsNone(art["hero"], "F00 must not repeat as a hero illustration")
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
                path = place["src"].split("?")[0]
                if place["id"] == "F01":
                    self.assertEqual(path, "assets/digital-book/fashion/v1.3/f01-sneaker-dream.webp")
                    self.assertEqual(len([a for a in self.manifest["assets"] if a["public_path"] == path]), 1)
                else:
                    self.assertIn(path, self.exports)
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

    def test_f01_author_selected_replacement_is_exact_and_separate(self):
        f01 = self.art["placements"][0]
        self.assertEqual(f01["id"], "F01")
        asset_url = "assets/digital-book/fashion/v1.3/f01-sneaker-dream.webp"
        self.assertEqual(f01["src"], asset_url + "?v=5a80feba402a")
        self.assertIn("bộ sưu tập sneakers", f01["alt"])
        matches = [a for a in self.manifest["assets"] if a["public_path"] == asset_url]
        self.assertEqual(len(matches), 1)
        asset = matches[0]
        self.assertEqual(asset["source"], "chapters/fashion/artwork/exports/reader-v1_3/f01-sneaker-dream.webp")
        self.assertEqual(asset["sha256_at_intake"], "5a80feba402ab1f8e0bf470846d3d4f2108b5e8627b594869d1d67412297d613")
        data = (ROOT / asset["source"]).read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), "5a80feba402ab1f8e0bf470846d3d4f2108b5e8627b594869d1d67412297d613")
        self.assertEqual(data[:4], b"RIFF")
        self.assertEqual(data[8:12], b"WEBP")

    def test_fashion_has_dedicated_reader_layout_and_cache_keys(self):
        app = (ROOT / "shared/web/app.js").read_text(encoding="utf-8")
        index = (ROOT / "shared/web/index.html").read_text(encoding="utf-8")
        style = (ROOT / "shared/web/style.css").read_text(encoding="utf-8")
        self.assertIn("if(slug==='fashion'&&Array.isArray(art.placements))", app)
        self.assertIn("Missing Fashion art anchor", app)
        self.assertIn("digital-book-fashion-scene", app)
        self.assertIn("digital-book-fashion-scene", style)
        self.assertIn("if(chapter.slug==='fashion')", app)
        self.assertIn("if(slug==='fashion')", app)
        self.assertNotIn("clip-path:circle(48.7% at 50% 50%)", style)
        self.assertIn("app.js?v=85", index)
        self.assertIn("style.css?v=64", index)
        self.assertIn("./digital-art.js?v=7", app)


    def test_transparent_f00_pair_is_registered_and_binary_exact(self):
        pair = {
            "f00-with-character-transparent.webp": "f245c3795ae8bcd4332749d0f8b17ddd4ea1ecd29fbe7fd7520cac5acd114fe3",
            "f00-without-character-transparent.webp": "95ff1c00d71a6836e7ff4f4ba96b666cb444a9401135e919e9008a733ee1aa86",
        }
        for name, expected_hash in pair.items():
            with self.subTest(name=name):
                public = "assets/digital-book/fashion/v1.2/" + name
                matches = [a for a in self.manifest["assets"] if a["public_path"] == public]
                self.assertEqual(len(matches), 1)
                asset = matches[0]
                file_bytes = (ROOT / asset["source"]).read_bytes()
                self.assertEqual(hashlib.sha256(file_bytes).hexdigest(), expected_hash)
                self.assertEqual(asset["sha256_at_intake"], expected_hash)
                self.assertEqual(file_bytes[:4], b"RIFF")
                self.assertEqual(file_bytes[8:12], b"WEBP")
                self.assertEqual(file_bytes[12:16], b"VP8X")
                self.assertIn(b"ALPH", file_bytes[:64], "Portal exports must retain transparency")


if __name__ == "__main__":
    unittest.main()
