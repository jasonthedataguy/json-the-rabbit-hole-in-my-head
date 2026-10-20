# Digital-book artwork library

On 20 October 2026, the screen exports from the author-supplied
`json-digital-book-assets.zip` were installed in the portal reader. The source
archive was read from:

```text
C:\Users\Administrator\Documents\Codex\2026-10-19\can\outputs\json-digital-book-assets.zip
```

The installation matches assets by stable chapter slug, not the concept
boards' chapter labels. It covers the Introduction and all 36 editorial
chapter slots without changing book order, chapter numbers, or manuscripts.

For each of the 37 sets, the website uses the pack's independent web exports:

| Role in the pack | Website placement |
| --- | --- |
| `main_book` | Portal on the cover's paper reading preview |
| `chapter_map` | Full portal on the chapter map |
| `chapter_opening` | Circular portal on the chapter-opening leaf |
| `reader_hero` | Rectangular opening illustration in both reading views |
| `inline_illustration` | Supporting illustration in the prose |
| `centre-scene.webp` | Upright, stationary picture inside the rotating cover ring |

The shared observer-free ring is the rotating cover layer. The Apology also
has two additional inline illustrations. This makes 225 installed screen
assets. Their source-to-public mappings and intake hashes are in
`shared/assets.json`; `shared/web/digital-art.js` is the runtime placement
map. The original pack manifest, quality report, and runtime asset map are
preserved in `references/digital-book-asset-pack/`. The native masters and
other reusable cutouts remain in the original ZIP; the website uses the
compressed web exports to avoid deploying the entire archive.

To reinstall or update from that archive:

```sh
python scripts/import_digital_art_pack.py --archive "C:\path\to\json-digital-book-assets.zip"
python scripts/build_inventory.py
python scripts/build_site.py
python scripts/check_site.py
python -m unittest discover -s tests -v
```

The importer verifies the pack's supplied SHA-256 hashes and that its slug
set exactly matches this edition. The web build copies the mapped files to
`dist/assets/digital-book/`. The ZIP's later full manuscript for The Apology
was outside this asset-only update; the existing editorial outline remains
until the manuscript is selected through the separate source workflow.

Visual QA covered the Introduction, all 36 chapter routes, 36 map stops, and
37 cover art stops at 1440×900 and 390×844. Representative images were also
decoded and visually checked for missing art, clipping, and page overflow.
