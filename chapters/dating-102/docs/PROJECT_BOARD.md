# Dating 102 — The Wrong Currency

Chapter 16 / original author essay / 2026-10-17 production review.

## Narrative and design

The essay moves from a satirical dating lecture through external validation to ordinary curiosity, then the currency joke, a speculative demographic escalation and a comic sign-off. Its emotional turn is the simple question “why do you think that?”. See source/NARRATIVE_MAP.md for exact paragraph mapping.

Keep the supplied midnight-teal stage and coral highlights; cream supports long reading and sage identifies curiosity. Use six source-board crops with documented native resolution. Do not import the unrelated Paris/reunion scenes or treat the concept chart as empirical data. The original board and all 13 source files remain untouched under references/project-board-v01.

## Product set

- Reader: full ten-paragraph essay, responsive homepage card, direct chapter route and alias.
- Currency Exchange: status/curiosity perspectives across drawing, light, Thursday football and Sunday picnic; keyboard controls, reset, live status and reduced motion.
- Print: complete illustrated A5 proof with source afterword, A4 lecture poster and bookmark. Current artwork is concept resolution; printer production is pending.
- Film: 24-second teaser, 60-second discovery, 45-second feed and 120-second vertical/landscape excerpts; provisional SRT/VTT and recording scripts. Author narration pending.
- Social: five 3:4 cards, three stories, Facebook image/copy, TikTok cover/copy and YouTube thumbnail/description, with alt text. No posts uploaded.
- Archive: source hashes, immutable reference manifest, 78-task review, product inventory, actual product-board JPG/PDF and downloadable chapter ZIP.

## Editorial boundaries

All original wording stays in the essay. Source notes sit separately; dated Korea/Vietnam/UNFPA/WHO/MedlinePlus material contextualizes numerical and biological claims. The Boston story's original source remains unidentified. No narrator age, prior publication date, consent record or statistical finding is invented.

## Rebuild

From repository root, with Pillow, ReportLab and PyMuPDF installed:

1. `python scripts/build_products.py --chapter dating-102 --video --ffmpeg PATH`
2. `python chapters/dating-102/tools/build_extras.py`
3. `python scripts/build_site.py`
4. Capture current web/interactive and video QA previews, then rerun build_extras.py to include those actual screenshots in the board.
5. `python scripts/build_inventory.py --chapter dating-102` and refresh Chapter 15 inventory because its next link changes.
6. Rebuild site, run tests and check_site.py, then the authorized commit/Pages deployment.

Final measured checks live in BROWSER_QA.json and MEDIA_QA.json. Full task evidence is in CHECKLIST_REVIEW.md. Remaining recording, print and physical-device work is not marked complete.
