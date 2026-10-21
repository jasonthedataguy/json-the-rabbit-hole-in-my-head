# 6 × 9 in print prototype

This package translates the design board into a physical cover and a Prologue opener. The Saigon and Cold Rice centre scenes are drawn at 3000 × 3000 px. The decorative rings are cut from the supplied design board and exported with transparent backgrounds and matching alpha masks. The original board and chapter artwork are preserved elsewhere in the repository.

## Dimensions and status

| Item | Prototype specification |
| --- | --- |
| Trim | 6 × 9 in (152.4 × 228.6 mm) |
| Bleed | 0.125 in (3.175 mm) on exposed outer edges |
| Cover spine | 12 mm placeholder; regenerate for final page count and stock |
| Raster output | 300 ppi RGB PDF/PNG proofs |
| Cover portal | 130 mm ring, 80.6 mm optional circular aperture, centred 128 mm below front trim top |
| Prologue portal | 118 mm ring, 73.2 mm optional circular aperture, centred 106 mm below page trim top |

The wrap width is **323.15 mm**, including back, placeholder spine, front, and two outer bleeds. Its height is **234.95 mm**. A single trimmed page plus bleed is **158.75 × 234.95 mm**. The exact printer spine, paper, binding, colour profile and die-cut tolerances are still open; these are prototype files, not press-approved mechanicals. The ring image is enlarged from a smaller source crop, so its effective detail should be reviewed at physical size and redrawn from original layers if the printer requires sharper fine detail.

## Files and use

| Group | Files | Use |
| --- | --- | --- |
| Flat cover | `../output/pdf/cover-wrap-flat-6x9.pdf` | Conventional cover with the portal scene printed on the front |
| Cut cover face | `../output/pdf/cover-wrap-diecut-face-6x9.pdf` | Cover face with a dark aperture area; use with cover underlay and a printer-approved cut |
| Cover underlay | `../output/pdf/cover-portal-underlay-6x9.pdf` | Scene printed on the layer immediately behind the aperture |
| Prologue face | `../output/pdf/chapter-00-diecut-face-6x9.pdf` | Cold Rice title page with the same paper-ring language and a cut aperture |
| Prologue underlay | `../output/pdf/chapter-00-underlay-6x9.pdf` | Father, child, lamp and rice-bowl scene behind the title page |
| Proofs | `proofs/*.png` | Exact 300 ppi rasters exported to the PDFs, plus a flat Prologue composition |
| Separate art | `assets/*.png` | 3000 px scenes, transparent rings and single-channel alpha masks |
| Cut paths | `cut/*.svg` | Vector trim/fold/aperture outlines; magenta is cut, cyan is trim/fold |
| Manifest | `manifest.json` | Dimensions, build status and SHA-256 hashes of generated outputs |

The die-cut cover face and underlay are alternatives to the flat cover. For a layered book, place each underlay directly behind its corresponding face at identical trim registration. Ask the printer to validate minimum paper bridges, fold clearance, aperture position, and whether the chapter opener can be cut on the chosen stock. Keep the ring artwork on the visible face; the circular cut removes only the central opening. The `portal-ring-band-guides.svg` file is an optional fabrication study for separate concentric paper layers, not a required cut on the bound book.

The Cold Rice artwork follows the chapter's intimate meal concept. The English display title is **Cold Rice** while the Vietnamese title **Cơm nguội** remains as a secondary line. The Saigon cover scene is a stylized skyline with Bitexco's helipad and Ba Son Bridge's leaning pylon and cable fan. Their placement is illustrative rather than survey accurate.

## Regenerate

From the repository root:

```sh
python scripts/paint_print_portals.py
python scripts/build_print_pack.py --spine-mm 12
python scripts/check_print_pack.py
```

Change `--spine-mm` when final page count, stock and printer spine formula are known. The website uses the corresponding 1000 px scenes copied by `scripts/build_site.py`; the print layout reads the 3000 px masters. `scripts/build_print_pack.py` writes the PDFs, proofs, cut paths and manifest deterministically. Do not place the cyan/magenta SVG guide strokes on the printed artwork.

For production, obtain the printer's cover template and ICC profile, recalculate the spine, check rich-black and colour conversion, obtain a physical-size proof, and approve the die-cut construction with the bindery. The 0.125 in bleed and page-count-dependent spine approach follow [KDP's cover preparation guidance](https://kdp.amazon.com/en_US/help/topic/G201953020); the chosen printer's specifications take precedence.
