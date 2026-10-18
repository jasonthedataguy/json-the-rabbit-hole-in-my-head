# Centred portal artwork

The picture is independent of the rotating frame. Both use a 1000 × 1000 canvas centred at (500, 500). The frame PNG carries its own transparency, with radius 480 outside and radius 310 inside; its cover variant also carries Jason's head across the opening. The circular picture extends to radius 312 underneath the frame, hiding subpixel seams. The cover, Introduction, Cold Rice homepage selection, chapter reader and Cold Rice map use this shared geometry.

The cover ring comes from the user's `Jason Under Revision_ Design Asset Board.png`. The source board is copied unchanged into `references/design/`; `scripts/cut_board_ring.py` records the artwork crops and transparent annular frame. The active cover picture is again the earlier landscape-only crop of the supplied board. Jason's body and head remain together in the rotating foreground ring. The same ring stays mounted throughout all 35 homepage stops while the selected scene stays upright. The chapter map and reader use chapter-specific artwork: Cold Rice has its own cut ring, Quant uses its editorial-board ring, Expected Utility, Play to Win and Fashion use their supplied portals, and the remaining chapters use their individual procedural portal designs. The older ring remains in `shared/artwork/cover-ring.png` as a supplied reference.

The Introduction now uses the latest supplied concept board's complete composition: an open book and reader before a moonlit city and bridge, encircled by memories and models. Cold Rice uses the earlier three-person family meal around a shared bowl. The later Saigon cover and father-and-child Cold Rice scenes remain separate alternates for the print study. The Saigon alternate depicts the [Bitexco Tower's projecting helipad](https://bitexco.com.vn/en/project/bitexco-financial-tower/) and [Ba Son Bridge's leaning pylon and cable fan](https://bandodulichtphcm.vn/en/diem-den/ba-son-bridge/). The supplied assets remain unchanged.

| Asset | Editable source |
|---|---|
| Landscape-only book-cover crop used by the site | `shared/artwork/book-cover/cover-scene-landscape.png` |
| Later Saigon cover alternate (print study) | `shared/artwork/book-cover/cover-scene-saigon-v3.png` |
| Earlier bowl-and-pedestal crop with stationary Jason removed | `shared/artwork/book-cover/cover-scene-board-clean.png` |
| Exact design-board centre crop (preserved input) | `shared/artwork/book-cover/cover-scene-board.png` |
| Active Introduction leaf ring and aligned scene | `shared/artwork/portal/introduction-ring-v2.png`, `shared/artwork/portal/introduction-scene-v2.png` |
| Transparent circular Introduction page composition | `shared/artwork/portal/introduction-portal-v2.png` |
| Active Introduction homepage centre crop | `shared/artwork/portal/introduction-cover-scene-v2.png` |
| Introduction rectangular reading illustration | `shared/artwork/portal/introduction-reading-spread-v2.webp` |
| Earlier Introduction city scene (alternate) | `shared/artwork/portal/introduction-scene-board.png` |
| Earlier open-book scene (alternate) | `shared/artwork/portal/introduction-scene.png` |
| Earlier Introduction leaf ring (alternate) | `shared/artwork/portal/introduction-ring.png` |
| Introduction concept boards (unchanged) | `references/design/Introduction Portal Ring Concept Board.png`, `references/design/Jason, Under Revision Concept Board - introduction.png` |
| Earlier generated cover interpretation (retained as an alternate) | `shared/artwork/book-cover/cover-scene-v2.png` |
| Cold Rice family-dinner centre used by the site | `chapters/com-nguoi/artwork/portal/rice-scene-board-v2.png` |
| Cold Rice floral lattice ring for the chapter map and reader | `chapters/com-nguoi/artwork/portal/rice-ring-board-v2.png` |
| Cold Rice wide reading illustration | `chapters/com-nguoi/artwork/portal/rice-family-room-v2.webp` |
| Quant rectangular reading illustration | `chapters/i-was-born-a-quant/artwork/portal/quant-reading-spread-v2.webp` |
| Fashion ring, upright centre and wide digital spread | `chapters/fashion/artwork/portal/fashion-ring-v2.png`, `fashion-scene-v2.png`, `fashion-room-v2.webp` |
| Earlier Fashion Paris portal (inactive reference) | `chapters/fashion/artwork/portal/fashion-portal.png` |
| Fashion final digital-book board (unchanged) | `references/design/Fashion Chapter Digital Book Board - final.png` |
| Expected Utility ring, aligned centre and desk spread | `chapters/expected-utility/artwork/portal/expected-utility-ring-v2.png`, `expected-utility-scene-v2.png`, `expected-utility-desk-v2.webp` |
| Expected Utility portal-layers board (unchanged) | `references/design/Expected Utility_ Portal Layers Board.png` |
| Play to Win ring, aligned centre and table spread | `chapters/play-to-win/artwork/portal/play-to-win-ring-v2.png`, `play-to-win-scene-v2.png`, `play-to-win-table-v2.webp` |
| Play to Win concept board (unchanged) | `references/design/model_specification - play to win dont play not to lose.png` |
| Later father-and-child Cold Rice alternate (print study) | `chapters/com-nguoi/artwork/portal/rice-scene-board-v3.png` |
| Full-resolution scene masters | `print/assets/cover-saigon-scene-3000.png`, `print/assets/cold-rice-scene-3000.png` |
| Constant homepage ring, including the foreground figure | `shared/artwork/portal/board-cover-ring.png` |
| Earlier figure-free design-board ring (retained alternate) | `shared/artwork/portal/board-ring-cut.png` |
| Design board source | `references/design/Jason Under Revision_ Design Asset Board.png` |
| Previous ring (retained) | `shared/artwork/cover-ring.png` |
| Picture placeholder | `shared/artwork/portal/placeholder.svg` |
| Reusable cutting mask and instructions | `templates/portal/` |
| Frame renderer and image placement | `shared/web/portal-art.js` |
| Interactive template / SVG exporter | `docs/PORTAL_STUDIO.html` |
| Reproducible cover and Cold Rice ring cutting, scene painting and print layout | `scripts/cut_board_ring.py`, `scripts/cut_rice_ring.py`, `scripts/paint_intro_portal.py`, `scripts/paint_print_portals.py`, `scripts/build_print_pack.py` |

The cover and Cold Rice scenes use zoom 1.00 with no offset in the SVG frame renderer. The Introduction page uses a transparent PNG composition of its matching ring and scene so only the circular portal is visible. The supplied boards and approved illustrations remain unchanged.

The main cover follows the board's physical-book layout: navy cloth, cream `.json` title, ring as the focal point, and a figure facing a dusk city. The board's papercut ring supplies the rotating frame. Every cover stop shares the same circular aperture: the cover, Introduction, Cold Rice, Quant, Expected Utility, Play to Win and Fashion use raster scenes, while the other chapters use scene-only SVG artwork from `renderPortalScene`. The selected picture changes while the frame rotates independently.

Static composition previews of the active picture and cut ring include `docs/qa/introduction-concept-leaf-composition.png`, `docs/qa/introduction-concept-cover-stop-composition.png`, and `docs/qa/cold-rice-board-portal-composition.png`. The earlier `docs/qa/cold-rice-map-ring-preview.png` remains for comparison. These show the artwork fit and are not browser screenshots of the final page.

Browser renders of the circular Introduction page at 1440px and a 500px narrow layout are saved as `docs/qa/introduction-page-desktop.png` and `docs/qa/introduction-page-500px.png`.

To use the template locally, serve the repository (not `dist`) on port 4174:

```sh
python -m http.server 4174 --bind 127.0.0.1
```

Open `http://localhost:4174/docs/PORTAL_STUDIO.html`. Choose a preset or a local PNG/JPEG/WebP, adjust zoom and placement, and download the fitted SVG. The export embeds both image and frame, works independently of the repository, and excludes alignment guides. The studio is an internal authoring tool and is not copied to the public site.

## Generation record

`scripts/cut_fashion_board.py` cuts the Fashion ring, its matching upright centre and the wide wardrobe scene from the author's final 1448 x 1086 digital-book board. The chapter map and Chapter 04 leaf use the Fashion ring. The homepage retains the common cover ring and changes only the centre scene. Both reading views use the wide illustration. The original portal and inherited products remain separate; these crops are digital assets rather than print-resolution masters. The composition proof is `docs/qa/fashion-board-portal-composition.png`.

`scripts/cut_expected_utility_board.py` cuts Expected Utility's decision-tree ring, aligned laptop-and-eyes centre and desk spread from the author's 1536 x 1024 portal-layers board. The map and Chapter 02 leaf use this ring, while the homepage retains the common cover ring and changes only the centre. The original-edition 04 on the board does not change the v2 chapter number. The crop is for digital use; its composition proof is `docs/qa/expected-utility-board-portal-composition.png`.

`scripts/cut_play_to_win_board.py` cuts Play to Win's game-table ring, matching centre and wide table scene from the author's 1448 x 1086 concept board. The map and Chapter 03 leaf use the chapter ring, while the homepage retains the common cover ring and changes only its centre. The original-edition 06 on the board does not change the v2 chapter number. These screen crops are separate from print masters; the composition proof is `docs/qa/play-to-win-board-portal-composition.png`.

The active Cold Rice portal is cut from the unchanged author board `references/design/prologue - cold rice.png` by `scripts/cut_cold_rice_board.py`. The floral lattice ring surrounds its aligned family-dinner centre on the chapter map and reader. The same centre sits under the constant book-cover ring at the homepage Cold Rice stop. The earlier `rice-portal.png`, `rice-ring.png` and `rice-scene-v2.png` remain as digital alternates. These 1000-pixel cuts are for screen display, not print masters.

The Introduction page now displays a single transparent circular composition made from its ring and aligned scene, without a rectangular artboard behind it. `scripts/cut_intro_concept_board.py` cuts both pieces from the author's latest 1672 × 941 board, exports the circular composition and focused cover-stop scene, and renders two composition proofs. The homepage's rotating book-cover ring remains constant at its Introduction stop. The supplied board is unchanged in `references/design/`, and the earlier Introduction ring and city scene remain available as alternates. These are digital front-matter illustrations, not print-resolution masters.

The active landscape crop is derived from the unchanged design board by `scripts/cut_board_ring.py`. The active Cold Rice scene was generated with the built-in imagegen tool on 18 October 2026. The previous Introduction city scene from `scripts/compose_intro_board_scene.py` and earlier open-book scene from `scripts/paint_intro_portal.py` remain alternates. The later Saigon and father-and-child alternates are drawn locally by `scripts/paint_print_portals.py` at 3000 pixels, then reduced to 1000-pixel web versions. The separate [print prototype](../print/README.md) still uses those later alternates and documents its full-resolution masters, cut guides and proofs.

### Cold Rice prompt

Use case: precise-object-edit. Asset type: square scene-only illustration for the central circular window of an interactive book. Image 1 is the edit target and style reference. Redesign the composition of this warm Vietnamese family meal so the scene fits a centered circular crop. Remove the entire decorative circular paper frame, all floral borders, and the outer navy background; expand the interior scene to fill the whole square edge to edge. Keep the existing layered paper-cut texture, warm amber lamp, deep navy silhouettes, teal and terracotta palette, mother on left, child near centre, father on right, table, and blue-and-white porcelain rice bowl. The bowl is the exact horizontal centre at approximately x50%, y56%; steam rises on the same centreline towards the lamp at x50%, y23%. Arrange the three seated family silhouettes around it, fully legible within the central 80% diameter circular safe area; faces, bowl and lamp must not touch that circular boundary. Balanced front-facing composition with the dinner table centred. Background room/window fills the square corners so there is ample crop bleed. No circle outline, no ring, no decorative frame, no border, no mat, no badges, no lettering, no text, no watermark. Output one square, detailed full-bleed illustration, not a mockup or template. Preserve the quiet, intimate family-memory tone.

Input: `chapters/com-nguoi/artwork/portal/rice-portal.png`.

### Earlier cover-interpretation prompt (not used by the site)

Use case: illustration-story. Asset type: scene-only square centre picture for the book .json / Jason under revision, to be placed inside a separate circular ring by code. Image 1 is a composition/mood reference; image 2 is the material and palette reference for the separate frame which will surround this picture. Redesign and expand the central book-cover scene into a clean, detailed standalone square artwork. A single small navy human silhouette, seen from behind, stands exactly on the vertical centreline at x50%, feet at y78%, head at y58%, looking towards a layered Vietnamese city skyline at dusk. Skyline horizon at y43%. A modest path leads from foreground to the city at x50%, softly luminous coral/amber sunset at x50%,y35%. Remembered architectural silhouettes and paper landscape layers, intimate and contemplative. Hand-cut paper theatre with tactile paper grain and delicate pencil details, deep midnight navy, dusty teal, cream, muted terracotta and warm gold, matching the supplied ring. Keep all main narrative elements inside the central 75%-diameter safe circle, leave generous square bleed beyond it. Strictly ONE centered scene. No outer ring, no nested circles, no tunnel, no decorative frame, no border, no rice bowl, no typography, no letters, no labels, no watermark, no book mockup. The frame is a separate asset; this image must fill the square to every edge with illustrated scenery. One square full-bleed illustration.

Inputs: `shared/artwork/book-cover/cover_portal_circle.png` and `shared/artwork/cover-ring.png`.
