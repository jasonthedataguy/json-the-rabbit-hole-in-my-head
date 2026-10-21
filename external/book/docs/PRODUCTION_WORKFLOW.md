# Full immersive chapter workflow

The complete story is the primary product. Read / Explore / Revisit adds optional ways to spend time with it. The production contract is [shared/product-contract.json](../shared/product-contract.json), and current evidence is on the [project board](PROJECT_BOARD.html).

| Stage | Work and location | Exit evidence |
|---|---|---|
| Intake | Preserve manuscript and supplied boards in `source/` and `references/` | Source provenance and real author selection |
| Editorial | Select `source/approved.md`, retain earlier prose, record changes | Correct `canonical_text` and `manuscript_sha256`; no invented paragraphs |
| Artwork | Keep masters, scene crops and portal art in `artwork/` | Provenance, crop coordinates, alt text and appropriate source resolution |
| Read | Reader uses the whole selected manuscript | Exact source/download bytes; complete rendered prose |
| Explore | Build the chapter’s source-grounded interactive memory or model in `web/` | Mouse, touch, keyboard and reduced-motion checks; sound never autoplays |
| Revisit | Offer original prose, history, actual print/media downloads | Existing files, valid paths and clear edition labels |
| Print | A5 illustrated proof; optional A4 poster, bookmark and booklet in `book/` | Rendered page QA; proof versus printer-approved production distinguished |
| Audio | Script and ambience in `audio/`; author recording when supplied | Real recording provenance, timing and final mix status |
| Film | Scene/time recipe, cuts and captions in `video/` | Playable files, real dimensions, source-verbatim excerpts, narration retiming |
| Social | Channel artwork, captions, alt text and download packs in `social/` | Correct dimensions and exact excerpts; upload state recorded separately |
| Release | Update `docs/PRODUCTS.json`, screenshots and actual board in `previews/` | Inventory, build checks, visual QA and all applicable release gates |

For the 32 existing slots, work in their existing chapter folders. Use `number` only for the v2 editorial slot, and keep original metadata under `references/original-edition/`. Do not rename an inherited PDF or edit its number merely to make it look like a v2 release. Create a new derivative after reviewing its contents, and record the superseded version.

New additional essays can start with:

```sh
python scripts/new_chapter.py --slug another-essay --title "Another essay" --archive
```

The scaffold remains unpublished and contains no fake manuscript. The cover currently has 33 editorial chapter stops, plus Cover and Introduction. They are all allocated; a new chapter requires a deliberate reading-order change.

After an authorized manuscript selection, calculate the raw SHA-256 and put it in `chapter.json` as `manuscript_sha256`. Record the reason in `source/revisions.log`; changing a hash is a record of a selection, not an approval process itself.

```sh
python -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('chapters/SLUG/source/approved.md').read_bytes()).hexdigest())"
python scripts/build_inventory.py
python scripts/build_site.py
python scripts/check_site.py
python -m unittest discover -s tests -v
python -m http.server 4173 --directory dist --bind 127.0.0.1
```

The current build generates the website, local product collection, inventories and board. It does not rerender inherited PDFs, regenerate artwork or retime films. Original production recipes remain in each chapter; the original renderer/toolchain is preserved under `references/original-edition/toolchain/` for adaptation, not presented as a v2-ready command. Narration, high-resolution print masters, physical print tests and updated v2 product exports remain explicit work items.

Before a v2 product release, review every inherited chapter number, title, caption, embedded URL, attribution and QR decision. Existing author decisions remain: supplied artwork/crops, cuts prepared for author-recorded narration, no synthetic author voice, deferred QR, and author-managed social uploads. Record actual evidence in the chapter’s product list; do not mark every lane complete because a folder exists.
