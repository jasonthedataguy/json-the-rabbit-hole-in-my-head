# I Was Born a Quant

V2 slot: **01**. Stable folder: `i-was-born-a-quant`.

Edit identity and state in `chapter.json`; keep author prose in `source/` and production recipes in `production.json`. See [the chapter workflow](../../docs/PRODUCTION_WORKFLOW.md) and [product status](docs/PRODUCT_STATUS.json).

The selected author manuscript is `source/approved.md`; the earlier editorial outline remains in `source/outline.md`. The supplied editorial artboard is preserved unchanged in `references/editorial-artboard.png`. Run `python scripts/cut_quant_artboard.py` from the repository root to regenerate the web portal crops in `artwork/portal/`.

The portal selects the artboard's **A · Expected Value** treatment, used in its chapter-page mockup. These crops are web assets from a 1536 × 1024 editorial board, not print-resolution masters. The reader is released; print, audio, film and social products remain separate production work.

The rectangular reading spread shows the lower main artwork with Jason, the chart, his risk-budget note and dog. `scripts/cut_intro_quant_spreads.py` regenerates it from the same preserved board. The reading page and desktop cover preview display its full frame without a forced crop.
