# .json — Jason, under revision

The portal edition and its immersive chapter production workspace. On desktop, the homepage presents the rotating cover ring beside a paper reading page that loads the selected Introduction or chapter text. The mobile cover keeps its compact layout. The ring retains its changing centre artwork and curved maths/literature quote. The reading order contains 33 editorial slots. Dating 102 is Chapter 19, immediately after Dating Algorithm; its original essay number remains in the source notes.

The Introduction leaf shows the author's latest concept board as a transparent circular portal: its collage ring frames the open book, reader, dusk city and bridge, followed by the six-step story progression and a full rectangular reading illustration. The homepage keeps the shared cover ring as it turns to a centre scene cut from that same board. Chapter 01, I Was Born a Quant, also carries a complete desk-scene spread before its manuscript.

The homepage starts on the earlier dusk-city landscape from the supplied design board, with Jason carried by its rotating paper ring. The Introduction uses the new board-derived city portal; Cold Rice now shows the author's floral-lattice family-dinner board. Its 35 ring stops follow **Cover → Introduction → Prologue (00) → Chapters 01–32**. The optional chapter map has 33 chapter stops. The paper ring surrounds a separate, upright picture. Navigation and chapter headings use English; the five part names display each English key alongside its Vietnamese title. The original Vinglish manuscripts remain unchanged. The Introduction uses the author's new Vietnamese synopsis and reader promise. Reading pages bundle Noto Serif for full Vietnamese typography. [Portal artwork and the replaceable picture template](docs/PORTAL_ARTWORK.md) explain how to fit another scene. The [6×9 in print prototype](print/README.md) preserves the newer art as a separate printable study, with underlays, cut guides and proofs.

Start with the [production board](docs/PROJECT_BOARD.html), [chapter status](docs/PRODUCTION_STATUS.md), [architecture](docs/ARCHITECTURE.md), [asset guide](docs/ASSET_GUIDE.md), and [full production workflow](docs/PRODUCTION_WORKFLOW.md).

```text
book.json             reading order, parts, introduction and shared conventions
chapters/<slug>/      manuscript, artwork, web, book, audio, video, social, QA
shared/               editable portal site, fonts, shared artwork, product contract
templates/chapter/    reusable unpublished intake structure
scripts/              build, inventory, validation, scaffolding and reference audit
tests/                source integrity and build safety checks
docs/                 project board, workflow, provenance and migration records
references/           original toolchain and design inputs
archive/              superseded v2 deliverables
dist/                 generated website; do not edit or commit
```

Each chapter has `chapter.json`, `production.json`, `source/`, `artwork/{source,scenes,exports,portal}/`, `book/`, `web/`, `audio/`, `video/`, four social channel folders, `docs/`, `previews/`, and `references/`. Stable slugs identify chapters independently of editorial numbers.

## Work here

Edit the website in `shared/web/`. Edit book-level content in `book.json` and chapter identity/summary in `chapters/<slug>/chapter.json`. Keep author-selected prose in the chapter’s `source/`. All 33 slots have a folder; 19 currently contain editorial outlines, not full author manuscripts.

Ten original chapters have their complete tracked asset kits locally: 1,412 preserved file mappings, about 444 MB including existing portal assets and production references. The selected reader retains all 80,917 original manuscript bytes plus the author-supplied Quant, Flow, Red Button and Coincidence chapters. All fourteen full manuscripts now have portal slots. [Migration evidence](docs/MIGRATION.json) and [source provenance](docs/source-provenance.json) record their identities.

The reader links to local immersive experiences and inherited print/film files. Their original numbering and proof states remain explicit. Existing assets are available for adaptation; narration, printer-specific work and v2 media/design review are not automatically complete.

## Build and preview

Python 3.11+; no package installation is required for the site or inventories.

```sh
python scripts/build_inventory.py
python scripts/build_site.py
python scripts/check_site.py
python -m unittest discover -s tests -v
python -m http.server 4173 --directory dist --bind 127.0.0.1
```

Open [localhost:4173](http://localhost:4173). Rebuild after changing sources. To view the internal board in a browser, serve the repository on a separate local port and visit `/docs/PROJECT_BOARD.html`; only `dist/` is intended for public deployment.

`build_site.py` generates the portal modules, manuscript library, public assets and local chapter collections. `build_inventory.py` generates the per-chapter file inventory, product status and cross-chapter board. The current tooling preserves existing media; it does not claim to regenerate inherited print or video products. Their recipes and original renderer remain available for deliberate v2 adaptation.

## Additional essays

```sh
python scripts/new_chapter.py --slug another-essay --title "Another essay" --archive
```

To work on one of the remaining 19 outline chapters, edit its existing folder. [The workflow](docs/PRODUCTION_WORKFLOW.md) explains manuscript selection, Read / Explore / Revisit, print, narration, films, social packs and release evidence.

## Cold Rice digital design

Cold Rice uses the supplied prologue board's floral lattice portal on the map, prologue leaf and immersive page. The homepage uses the same family dinner scene inside the constant book-cover ring, while the desktop reading preview shows the warm family room. The board's “03” is an illustrative mock-page label: this edition keeps **Prologue 00**, with original essay **07** preserved. See [Cold Rice adaptation notes](chapters/com-nguoi/docs/DESIGN_ADAPTATION.md).

## Fashion digital design

Fashion uses the final supplied digital-book board's wardrobe and sneaker portal on the chapter map and Chapter 04 leaf. The homepage keeps the common book-cover ring and shows the Fashion scene in its centre. Both reading views use the board's wide wardrobe illustration. The board's “02” is its original-edition number; the current book keeps Fashion at Chapter 04. See [the Fashion adaptation notes](chapters/fashion/docs/DESIGN_ADAPTATION.md).

## Expected Utility digital design

Expected Utility uses the revised supplied board's choice-path ring, stationary gaze and wide reading scene on its Chapter 02 map and reading views. The homepage keeps the shared cover ring and swaps in a face-only centre. The board labels original-edition Chapter 04; the v2 chapter remains 02. See [the Expected Utility adaptation notes](chapters/expected-utility/docs/DESIGN_ADAPTATION.md).

## Play to Win digital design

Play to Win uses the supplied game-table concept board's cards, mahjong, chips and payoff matrix across its Chapter 03 map and reading views. The homepage keeps the shared cover ring and swaps in the aligned table scene. The board labels original-edition Chapter 06; the v2 chapter remains 03 and uses the full author-approved English title. See [the Play to Win adaptation notes](chapters/play-to-win/docs/DESIGN_ADAPTATION.md).

## For Mother Russia digital design

For Mother Russia now uses the supplied winter-memory board's photographic portal ring, snowy city-and-cabin centre and rectangular cabin vignette in the chapter map, Chapter 08 reading leaf and desktop book preview. The homepage retains the common cover ring and shows the new centre at this stop. Its separate immersive page adopts the same art while keeping the original essay and Memory Graph. The board's Chapter 03 is a concept label; v2 remains Chapter 08, and original-edition 05 remains historical metadata. See [the design adaptation notes](chapters/for-mother-russia/docs/DESIGN_ADAPTATION.md).

## Three Meeting Theory digital design

Three Meeting Theory uses the supplied romance-and-city board's complete circular collage and rectangular couple/cafe vignette on the chapter map, Chapter 17 reading leaf and desktop book preview. The whole illustrated circle turns together, keeping the original bridge and river free of reconstructed background. The homepage keeps its common cover ring and shows both people in the centre at this stop. Its separate immersive page uses the same art and retains the original essay and Third Intersection explorer. The board's Chapter 15 is an original-edition label; v2 remains Chapter 17. See [the design adaptation notes](chapters/three-meeting-theory/docs/DESIGN_ADAPTATION.md).

## To My Saigon digital design

To My Saigon uses the supplied Saigon board's work-and-home ring and the still view of the couple, dog, Ba Son Bridge and skyline on the map and Chapter 14 leaf. The homepage keeps its shared cover ring and shows a city-only crop at this stop. The desktop preview and standalone chapter use the full couple-and-river reading illustration; the standalone memory selector has eight matching board crops. The English display title and Chapter 14 label leave the 20-paragraph original Vinglish essay unchanged. See [the design adaptation notes](chapters/viet-cho-sai-gon-cua-t/docs/DESIGN_ADAPTATION.md).

## Deployment



GitHub Actions tests, inventories, builds and validates before deploying `dist/` on pushes to `main`. Pull requests run checks without deployment. Source assets and chapter products are versioned; generated site output is ignored. Existing hash routes and root asset URLs are preserved, and all local paths work beneath `/json-under-revision-v2/`.

No release or social upload is performed by the local build. The [original edition](https://github.com/jasonthedataguy/json-under-revision) remains unchanged at its own repository and URLs.
