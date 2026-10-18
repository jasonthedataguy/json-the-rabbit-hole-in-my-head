# Centred portal artwork

The picture is independent of the rotating frame. Both use a 1000 × 1000 canvas centred at (500, 500). The frame PNG carries its own transparency, with radius 480 outside and radius 310 inside; its cover variant also carries Jason's head across the opening. The circular picture extends to radius 312 underneath the frame, hiding subpixel seams. The cover, Introduction, Cold Rice homepage selection, chapter reader and Cold Rice map use this shared geometry.

The cover ring comes from the user's `Jason Under Revision_ Design Asset Board.png`. The source board is copied unchanged into `references/design/`; `scripts/cut_board_ring.py` records the artwork crops and transparent annular frame. The active cover picture is again the earlier landscape-only crop of the supplied board. Jason's body and head remain together in the rotating foreground ring. The same ring stays mounted throughout all 34 homepage stops while the selected scene stays upright. The chapter map and reader use chapter-specific artwork: Cold Rice has its own cut ring, Quant uses its editorial-board ring, Fashion uses its supplied portal, and the remaining chapters use their individual procedural portal designs. The older ring remains in `shared/artwork/cover-ring.png` as a supplied reference.

The Introduction now shows the supplied concept board city and bridge scene inside its collage ring. Cold Rice again uses the earlier three-person family meal around a shared bowl. The later Saigon cover and father-and-child Cold Rice scenes remain separate alternates for the print study. The Saigon alternate depicts the [Bitexco Tower's projecting helipad](https://bitexco.com.vn/en/project/bitexco-financial-tower/) and [Ba Son Bridge's leaning pylon and cable fan](https://bandodulichtphcm.vn/en/diem-den/ba-son-bridge/). The supplied assets remain unchanged.

| Asset | Editable source |
|---|---|
| Landscape-only book-cover crop used by the site | `shared/artwork/book-cover/cover-scene-landscape.png` |
| Later Saigon cover alternate (print study) | `shared/artwork/book-cover/cover-scene-saigon-v3.png` |
| Earlier bowl-and-pedestal crop with stationary Jason removed | `shared/artwork/book-cover/cover-scene-board-clean.png` |
| Exact design-board centre crop (preserved input) | `shared/artwork/book-cover/cover-scene-board.png` |
| Active Introduction city scene | `shared/artwork/portal/introduction-scene-board.png` |
| Earlier open-book scene (alternate) | `shared/artwork/portal/introduction-scene.png` |
| Introduction leaf ring | `shared/artwork/portal/introduction-ring.png` |
| Introduction concept board (unchanged) | `references/design/Jason, Under Revision Concept Board - introduction.png` |
| Earlier generated cover interpretation (retained as an alternate) | `shared/artwork/book-cover/cover-scene-v2.png` |
| Three-person Cold Rice scene used by the site | `chapters/com-nguoi/artwork/portal/rice-scene-v2.png` |
| Cold Rice ring for the chapter map and reader | `chapters/com-nguoi/artwork/portal/rice-ring.png` |
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

The cover, Introduction and Cold Rice scene use zoom 1.00 with no offset. Placement is non-destructive SVG composition; the supplied board and approved illustrations remain unchanged. The frame rotates around the same centre without moving the scene.

The main cover follows the board's physical-book layout: navy cloth, cream `.json` title, ring as the focal point, and a figure facing a dusk city. The board's papercut ring supplies the rotating frame. Every cover stop shares the same circular aperture: the cover, Introduction and Cold Rice use raster scenes, while chapter stops after the Prologue use scene-only SVG artwork from `renderPortalScene`. The selected picture changes while the frame rotates independently.

Static composition previews of the active picture and cut ring are saved at `docs/qa/cover-board-composition.png`, `docs/qa/cover-turned-composition.png`, `docs/qa/introduction-board-composition.png`, `docs/qa/cold-rice-board-composition.png` and `docs/qa/cold-rice-map-ring-preview.png`. These show the artwork fit and are not browser screenshots of the final page.

To use the template locally, serve the repository (not `dist`) on port 4174:

```sh
python -m http.server 4174 --bind 127.0.0.1
```

Open `http://localhost:4174/docs/PORTAL_STUDIO.html`. Choose a preset or a local PNG/JPEG/WebP, adjust zoom and placement, and download the fitted SVG. The export embeds both image and frame, works independently of the repository, and excludes alignment guides. The studio is an internal authoring tool and is not copied to the public site.

## Generation record

The Cold Rice chapter ring is cut from the original supplied `chapters/com-nguoi/artwork/portal/rice-portal.png` by `scripts/cut_rice_ring.py`. Its transparent centre reveals the approved `rice-scene-v2.png` family meal; the source illustration is preserved unchanged. This 1000-pixel cut is for the digital chapter map and reader, not the print master. The homepage continues to use the constant book-cover ring at its Cold Rice stop.

The Introduction leaf pairs the board-derived city scene with the main collage ring from the author's new concept board. Its transparent cut-out lets the sunset skyline and bridge show through. `scripts/cut_intro_artboard.py` records the crop and cut; the 1672 × 941 board is preserved unchanged under `references/design/`. The cover's rotating ring remains constant at its Introduction stop, showing the same city scene in its centre. The new ring is a digital front-matter illustration and is not a print-resolution master.

The active landscape crop is derived from the unchanged design board by `scripts/cut_board_ring.py`. The active Cold Rice scene was generated with the built-in imagegen tool on 18 October 2026. The active Introduction scene is composed from the board artwork with crisp skyline and bridge layers by `scripts/compose_intro_board_scene.py`; the earlier open-book scene from `scripts/paint_intro_portal.py` remains an alternate. The later Saigon and father-and-child alternates are drawn locally by `scripts/paint_print_portals.py` at 3000 pixels, then reduced to 1000-pixel web versions. The separate [print prototype](../print/README.md) still uses those later alternates and documents its full-resolution masters, cut guides and proofs.

### Cold Rice prompt

Use case: precise-object-edit. Asset type: square scene-only illustration for the central circular window of an interactive book. Image 1 is the edit target and style reference. Redesign the composition of this warm Vietnamese family meal so the scene fits a centered circular crop. Remove the entire decorative circular paper frame, all floral borders, and the outer navy background; expand the interior scene to fill the whole square edge to edge. Keep the existing layered paper-cut texture, warm amber lamp, deep navy silhouettes, teal and terracotta palette, mother on left, child near centre, father on right, table, and blue-and-white porcelain rice bowl. The bowl is the exact horizontal centre at approximately x50%, y56%; steam rises on the same centreline towards the lamp at x50%, y23%. Arrange the three seated family silhouettes around it, fully legible within the central 80% diameter circular safe area; faces, bowl and lamp must not touch that circular boundary. Balanced front-facing composition with the dinner table centred. Background room/window fills the square corners so there is ample crop bleed. No circle outline, no ring, no decorative frame, no border, no mat, no badges, no lettering, no text, no watermark. Output one square, detailed full-bleed illustration, not a mockup or template. Preserve the quiet, intimate family-memory tone.

Input: `chapters/com-nguoi/artwork/portal/rice-portal.png`.

### Earlier cover-interpretation prompt (not used by the site)

Use case: illustration-story. Asset type: scene-only square centre picture for the book .json / Jason under revision, to be placed inside a separate circular ring by code. Image 1 is a composition/mood reference; image 2 is the material and palette reference for the separate frame which will surround this picture. Redesign and expand the central book-cover scene into a clean, detailed standalone square artwork. A single small navy human silhouette, seen from behind, stands exactly on the vertical centreline at x50%, feet at y78%, head at y58%, looking towards a layered Vietnamese city skyline at dusk. Skyline horizon at y43%. A modest path leads from foreground to the city at x50%, softly luminous coral/amber sunset at x50%,y35%. Remembered architectural silhouettes and paper landscape layers, intimate and contemplative. Hand-cut paper theatre with tactile paper grain and delicate pencil details, deep midnight navy, dusty teal, cream, muted terracotta and warm gold, matching the supplied ring. Keep all main narrative elements inside the central 75%-diameter safe circle, leave generous square bleed beyond it. Strictly ONE centered scene. No outer ring, no nested circles, no tunnel, no decorative frame, no border, no rice bowl, no typography, no letters, no labels, no watermark, no book mockup. The frame is a separate asset; this image must fill the square to every edge with illustrated scenery. One square full-bleed illustration.

Inputs: `shared/artwork/book-cover/cover_portal_circle.png` and `shared/artwork/cover-ring.png`.
