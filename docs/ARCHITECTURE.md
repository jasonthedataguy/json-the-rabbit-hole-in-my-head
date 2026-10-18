# Project architecture

V2 uses the original book’s chapter product model while retaining the portal cover, 00–32 editorial order, and continuous reader. `book.json` and each chapter’s `chapter.json` are the editable registry. Generated JavaScript no longer owns the book metadata.

```text
book.json                         identity, reading order, parts, introduction
chapters/<stable-slug>/
  chapter.json                    v2 identity, selected prose, original mapping
  production.json                 scene, print, film and social recipe
  source/                         author prose, outline, real revision history
  artwork/{source,scenes,exports,portal}/
  book/                           print proofs and instructions
  web/                            chapter-specific immersive experience
  audio/                          reading scripts, ambience, supplied narration
  video/                          edits, timeline, storyboard, SRT/VTT
  social/{instagram,facebook,tiktok,youtube}/
  docs/                           products, inventory, status, historical QA
  previews/                       real renders and product boards
  references/                     untouched supplied kits and original metadata
shared/
  web/                            editable portal HTML/CSS/JavaScript
  artwork/                        cover ring, shared badge, favicon
  fonts/                          named font files and OFL licenses
  assets.json                     source-to-public asset mapping
  design.json                     design conventions and output dimensions
  product-contract.json           deliverables and release gates
  site.css, site.js               original immersive pages’ shared runtime
templates/chapter/                reusable unpublished chapter intake
scripts/                         build, inventory, scaffold, audit, checks
tests/                           integrity, isolation and scaffold checks
docs/                            architecture, workflow, project board, migration
references/                      original toolchain and v2 intake evidence
archive/                         future superseded v2 deliverables
dist/                            ignored generated public site
.build/                          ignored staging output
```

## Editorial and source identity

The cover ring includes two front-matter stops before the chapter registry: Cover and Introduction. `PortalRing` accepts a stop count so the cover has 35 stops and the chapter map has 33. On desktop, selecting a stop also renders its full text or clearly marked outline in a separately scrollable paper page beside the ring. Mobile retains the compact cover and opens the normal reader through the page link. Returning to the cover opens on its cover artwork. English chapter display titles live in `title`/`short_title`; translated chapter metadata retains `original_title`, and original-edition metadata/manuscript bytes remain untouched. The five part labels display `key | title` using Vietnamese part titles in `book.json`.

Stable slugs survive a change of reading order. A v2 chapter number never overwrites the original number. For example, Cơm nguội is v2 `00` and original `07`; Fashion is v2 `04` and original `02`. Dating 102 is now v2 `19`, following Dating Algorithm (`18`), while its original publication number remains `16`. Former v2 chapters `19`–`31` shift to `20`–`32`. The old `#archive/dating-102` hash still opens its book chapter.

Ten original manuscripts and their complete tracked product folders were imported; the author-supplied Quant chapter brings the full-text total to eleven. All eleven map to the portal order; 22 portal slots contain the existing editorial outlines and no invented full text. `publish: false` means no manuscript/product publication, while the existing outline remains visible in the editorial map. `publish: true` requires selected prose and its recorded SHA-256. Reader availability is independent of print, narration and multimedia completion.

Fashion's current digital chapter art is derived from the author's final design board. `assets/fashion-ring-v2.png` and `assets/fashion-scene-v2.png` form the chapter map and reader portal; the scene alone appears under the unchanged homepage book ring. `assets/fashion-room-v2.webp` illustrates the reading spread. `scripts/cut_fashion_board.py` regenerates these digital crops from the unchanged board in `references/design/`. The board labels the original edition's Chapter 02; v2 Fashion remains Chapter 04. The former Paris Fashion portal remains preserved.

## Build and public paths

`build_site.py` reads local sources and works without the original checkout or a package install. It generates `book.js`, `chapter-data.js`, rendered manuscripts, manuscript downloads and the public asset manifest. The artwork renderer in `shared/web/chapters.js` consumes generated metadata and uses stable slugs to keep each scene attached to its chapter. Runtime URLs such as `#chapter/00`, `#chapter/19`, `#map`, and `assets/cover-ring.png` are used for this edition. All homepage stops share `assets/board-cover-ring.png`, including Jason's foreground figure, while the centre changes from the earlier `assets/cover-scene-landscape.png` to `assets/introduction-cover-scene-v2.png` and chapter scenes. The Introduction page uses the transparent circular `assets/introduction-portal-v2.png`; its ring and aligned scene remain separately available for editing. Prologue 00 uses `assets/rice-scene-v2.png` in the centre and its own `assets/rice-ring.png` on the chapter map and reader. Chapter 01 uses its Quant ring, Chapter 04 its Fashion portal, and the other map stops use chapter-specific procedural designs. The earlier `assets/board-ring-cut.png` and `assets/cover-ring.png` remain available. `scripts/paint_print_portals.py` preserves alternate digital scenes and 3000-pixel print masters; `scripts/build_print_pack.py` builds the separate 6×9 in print prototype.

The build stages its output before replacing the marked `dist/` directory. It refuses to clean any source directory or an unmarked output directory. `check_site.py` detects stale inputs, modified generated files, missing links, altered protected originals and absent declared products.

Existing immersive pages are available at `chapters/<slug>/web/index.html` inside the generated site. They retain their original chapter labels and external original-edition navigation. The v2 reader links to these local experiences and their print/film files. Products have been preserved and connected; their design and numbering have not been falsely relabeled as finished v2 products.

Only selected public asset groups, manuscript downloads and explicit dependencies of the immersive pages are deployed. These dependencies include six public scene SVGs, linked research/source notes and a blank study worksheet. Other source artwork, supplied references, production tooling and internal project boards stay in the repository. Public proof PDFs and media retain their actual historical status. Original offline poster/srcset path errors are repaired in generated HTML only.

## Production evidence

`docs/MIGRATION.json` records 1,412 preserved file mappings and intake hashes, including the existing v2 runtime. Protected originals and references are checked against these records; editable derivatives may evolve with documented author decisions. Two Windows checkout manuscripts differed only by CRLF/LF: their checkout bytes remain in references, while v2’s established 80,917 manuscript bytes remain the selected reader corpus.

`docs/PRODUCTS.json` is the inspected deliverable list within each chapter. `build_inventory.py` writes raw file hashes to `ASSET_INVENTORY.json`, combines product states with the contract in `PRODUCT_STATUS.json`, and produces the project-wide Markdown/HTML board. A file’s presence does not satisfy a release gate by itself.
