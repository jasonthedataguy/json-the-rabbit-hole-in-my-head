# Chapter 09 — The Borrowed Reel

The source package used 06. The author selected 09 to preserve the existing chapter routes. Keep original source labels as historical provenance; new public art, print, media and metadata use 09.

The design follows the supplied Paris dusk palette and three narrative layers: observation, imagination and afterimage. The complete nineteen-paragraph essay is static HTML and remains readable without JavaScript. The interactive film changes layer and color grade without inventing an outcome or implying the dinner was witnessed.

Products: eight supplied scene derivatives, full illustrated A5 proof, A4 poster/bookmark, five verbatim carousel cards, platform art/copy, five video edit formats, SRT/VTT visual timings, full and excerpt recording scripts, responsive reader, archive, actual product board and complete ZIP. All 76 original kit files remain checksum-preserved references. See PRODUCT_SET.md and the 72-task audit for exact delivery states.

Rebuild from the repository root with Pillow, ReportLab, PyMuPDF and ffmpeg available:

1. `python chapters/the-gioi-trong-mo-cua-toi/tools/prepare_artwork.py`
2. `python scripts/build_supplied_media.py --chapter the-gioi-trong-mo-cua-toi --ffmpeg PATH`
3. `python chapters/the-gioi-trong-mo-cua-toi/tools/build_extras.py`
4. `python scripts/build_site.py`
5. Capture web/media QA previews; rerun build_extras.py to place those actual previews on the board.
6. Refresh Chapter 09 inventory and Chapter 08 inventory because its next link now leads to 09; rebuild and validate the site.

The artwork helper crops embedded board labels from the new derivatives. Crop coordinates, native dimensions and original hashes are recorded in artwork/scenes/index.json. Source artwork and all references remain untouched. The current A5 proof contains four pages with the complete original body.

Author narration, speech-synced captions, high-resolution layered art and printer-specific/physical production remain pending. QR is deferred; social posting remains author-managed.
