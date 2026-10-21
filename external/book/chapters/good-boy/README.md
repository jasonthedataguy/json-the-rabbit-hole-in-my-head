# Office Battlefield - Good Boy

V2 slot: **28**. Stable folder: `good-boy`.

Edit identity and state in `chapter.json`; keep author prose in `source/` and production recipes in `production.json`. See [the chapter workflow](../../docs/PRODUCTION_WORKFLOW.md) and [product status](docs/PRODUCT_STATUS.json).

The final author manuscript is selected in `source/approved.md`, with the quoted messages and original Vinglish intact. The earlier outline remains in `source/outline.md`.

The supplied board is preserved in `references/design/`. Run `python scripts/cut_good_boy_board.py` from the repository root to rebuild the aligned digital ring, centre and rectangular illustration; run `python scripts/build_good_boy_chapter.py` for the standalone reader. The same assets appear in the chapter leaf, map and homepage preview. See [asset provenance](docs/ASSET_SOURCE.md) and [visual QA](docs/QA.md).
