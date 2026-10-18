# Working on the portal edition

- Read `README.md`, `docs/ARCHITECTURE.md` and the relevant chapter metadata before editing.
- Edit portal UI in `shared/web/`, book content in `book.json`, and chapter identity/content in `chapters/<slug>/`. `dist/` and `.build/` are generated; never use them as the only copy of a change.
- Keep stable slugs, v2 editorial numbers and original edition numbers separate. Dating 102 is Chapter 19 in this edition, with its original edition number retained as source history. Do not turn an editorial outline into invented author prose.
- Preserve source manuscripts and supplied references. Apply author-requested manuscript changes to the selected source and record the selection/hash; retain the original and real history.
- A declared product must exist. Keep proofs, edit previews, pending narration and final outputs distinct. File presence alone does not complete a release gate.
- Preserve the changing centre artwork, stationary curved quote, keyboard/touch ring controls, reduced motion and stable hash routes when changing the UI.
- After changes, run relevant unit checks, `python scripts/build_inventory.py`, `python scripts/build_site.py`, and `python scripts/check_site.py`. Inspect desktop/mobile renders for layout changes. Media regeneration needs its own visual/playback checks.
- The original toolchain in `references/` is historical input, not the active v2 build. Do not run it as though its paths and chapter numbers already match this edition.
