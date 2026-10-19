# Office Battlefield - Masterclass in Record Keeping

V2 slot: **27**. Stable folder: `masterclass-in-record-keeping`.

Edit identity and state in `chapter.json`; keep author prose in `source/` and production recipes in `production.json`. See [the chapter workflow](../../docs/PRODUCTION_WORKFLOW.md) and [product status](docs/PRODUCT_STATUS.json).

The exact author attachment is preserved in `source/original.txt`. `source/approved.md` changes only the heading markup and paragraph spacing so the 70 paragraphs render in the digital reader. The earlier outline remains in `source/outline.md`.

The supplied board is preserved in `references/design/`. Run `python scripts/cut_record_keeping_board.py` from the repository root to rebuild the aligned digital ring, centre and rectangular illustration; run `python scripts/build_record_keeping_chapter.py` for the standalone reader. The same assets appear in the chapter leaf, map and homepage preview. See [asset provenance](docs/ASSET_SOURCE.md) and [visual QA](docs/QA.md).
