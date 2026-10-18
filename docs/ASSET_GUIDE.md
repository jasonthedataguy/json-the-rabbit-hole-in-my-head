# Asset ownership and editing

| Asset | Editable home | Public build |
|---|---|---|
| Cover layout, quote arcs, navigation, reader | `shared/web/` | Root HTML/CSS/JS in `dist/` |
| Book parts and introduction | `book.json` | Generated `book.js` |
| Chapter titles, summaries, portal scene metadata | `chapters/<slug>/chapter.json` | Generated `chapter-data.js` |
| Portal SVG drawing code | `shared/web/chapters.js` | `chapters.js` |
| Paper ring and bowl badge | `shared/artwork/` | Existing `assets/` URLs through `shared/assets.json` |
| Cơm nguội / Expected Utility / Fashion portal images | Their chapter’s `artwork/portal/` | Existing portal image URLs |
| Fonts and license texts | `shared/fonts/` | Local `assets/` files, mapped by manifest |
| Physical-edition concept image | `references/design/` | Only the explicitly mapped concept image |
| Selected manuscript | `chapters/<slug>/source/approved.md` | Rendered content plus byte-identical Markdown download |
| Product artwork, print, audio, film and social | Their chapter’s named product directories | Whitelisted finished exports for published chapters |
| Source art, original toolchain and supplied boards | `artwork/source/` and `references/` | Not deployed except source SVGs explicitly used by an immersive page |

Add a shared public asset to `shared/assets.json` with an explicit source and public path. `sha256_at_intake` records provenance; the build manifest records the current bytes. Do not use a generated `dist/` file as a source.

Keep product filenames descriptive and retain original supplied names in references. Put replaced v2 products under `archive/` with their provenance. `docs/ASSET_INVENTORY.json` is generated from actual chapter files; `docs/PRODUCTS.json` is the curated declaration of product purpose and inspected state.

Source artwork and references are distinct from public exports. Public build inputs are recorded in `dist/build-manifest.json`, so a source edit requires a rebuild and an output edit is detected by validation.
