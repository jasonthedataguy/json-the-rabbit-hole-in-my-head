# Project architecture

V2 uses the original book’s chapter product model while retaining the portal cover, 00–31 editorial order, continuous reader, and separate archive essay. `book.json` and each chapter’s `chapter.json` are the editable registry. Generated JavaScript no longer owns the book metadata.

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

Stable slugs survive a change of reading order. A v2 chapter number never overwrites the original number. For example, Cơm nguội is v2 `00` and original `07`; Fashion is v2 `04` and original `02`. Dating 102 has no portal number and remains in `archive_chapters`.

Ten existing manuscripts and their complete tracked product folders were imported. Nine map to the portal order; 23 portal slots contain the existing editorial outlines and no invented full text. `publish: false` means no manuscript/product publication, while the existing outline remains visible in the editorial map. `publish: true` requires selected prose and its recorded SHA-256. Reader availability is independent of print, narration and multimedia completion.

## Build and public paths

`build_site.py` reads local sources and works without the original checkout or a package install. It generates `book.js`, `chapter-data.js`, rendered manuscripts, manuscript downloads and the public asset manifest. The artwork renderer in `shared/web/chapters.js` consumes generated metadata. Runtime URLs such as `#chapter/00`, `#map`, `#archive/dating-102`, and `assets/cover-ring.png` remain stable.

The build stages its output before replacing the marked `dist/` directory. It refuses to clean any source directory or an unmarked output directory. `check_site.py` detects stale inputs, modified generated files, missing links, altered protected originals and absent declared products.

Existing immersive pages are available at `chapters/<slug>/web/index.html` inside the generated site. They retain their original chapter labels and external original-edition navigation. The v2 reader links to these local experiences and their print/film files. Products have been preserved and connected; their design and numbering have not been falsely relabeled as finished v2 products.

Only selected public asset groups, manuscript downloads and explicit dependencies of the immersive pages are deployed. These dependencies include six public scene SVGs, linked research/source notes and a blank study worksheet. Other source artwork, supplied references, production tooling and internal project boards stay in the repository. Public proof PDFs and media retain their actual historical status. Original offline poster/srcset path errors are repaired in generated HTML only.

## Production evidence

`docs/MIGRATION.json` records 1,412 preserved file mappings and intake hashes, including the existing v2 runtime. Protected originals and references are checked against these records; editable derivatives may evolve with documented author decisions. Two Windows checkout manuscripts differed only by CRLF/LF: their checkout bytes remain in references, while v2’s established 80,917 manuscript bytes remain the selected reader corpus.

`docs/PRODUCTS.json` is the inspected deliverable list within each chapter. `build_inventory.py` writes raw file hashes to `ASSET_INVENTORY.json`, combines product states with the contract in `PRODUCT_STATUS.json`, and produces the project-wide Markdown/HTML board. A file’s presence does not satisfy a release gate by itself.
