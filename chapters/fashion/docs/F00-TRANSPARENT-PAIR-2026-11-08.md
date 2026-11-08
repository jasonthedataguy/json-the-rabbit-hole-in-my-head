# Fashion F00 transparent portal pair · 2026-11-08

## Decision / scope
Founder explicitly requested both character and non-character F00 portals **without the square navy background**, with no changes to the chapter's established design, and authorized updating Google Drive and digital book. This is approval for this narrowly scoped web visual update, **not** a new book/print edition or unrelated public content.

## Art identity and fidelity
- Author-selected base A: `F00-A-selected-with-character-native.png`, original SHA-256 `bc36a21737e0352575dd7dbcf75f287cdb2a39065a691cc2b6a8347908b86706`.
- Original B no-foreground reconstruction retained as historical review source. B differs from A only around the foreground boy/steps; other pixels are identical (97.18% of the overall original canvas).
- Both outputs retain the RGB data of their respective source images inside the portal; the only newly authored field is per-pixel transparency for the exterior navy backdrop. This is deliberate fidelity preservation, not a generative redraw that might change the illustration.
- Background separation: common foreground mask, contoured to the portal's *actual outer ring*, anti-aliased and saved with alpha. No CSS circle crop is used after release. No original masters overwritten.

## Active WebP exports (1254 × 1254, RGBA)
| Role | Asset | SHA-256 |
| --- | --- | --- |
| Chapter opening, with character | `assets/digital-book/fashion/v1.2/f00-with-character-transparent.webp` | `f245c3795ae8bcd4332749d0f8b17ddd4ea1ecd29fbe7fd7520cac5acd114fe3` |
| Interactive cover Fashion stop and chapter map, no foreground character | `assets/digital-book/fashion/v1.2/f00-without-character-transparent.webp` | `95ff1c00d71a6836e7ff4f4ba96b666cb444a9401135e919e9008a733ee1aa86` |

## Drive masters
Source-preserving PNG masters and WebP screen derivatives stored under:
`.json - Private Artwork Library/Studio_Production/01_Originals/book/chapters/fashion/artwork/portal-layers/masters` and `.../web`. Older masters and exports are preserved.

## Digital-book integration
- `shared/web/digital-art.js`: `fashion.mainBook` and `fashion.map` → no-character; `fashion.opening` → with-character.
- `fashion.hero` remains null: do not duplicate F00 before the prose. Keep exact F01–F10 manuscript-anchored placements unchanged.
- `shared/web/style.css`: remove obsolete F00 clip-path. The real source files carry clean transparency.
- HTML/module cache keys bumped. The separate preserved original-edition Fashion experience is not reauthored.
- Manuscript: `chapters/fashion/source/author-approved-v0.5.md` unchanged, recorded SHA-256 `9865a628ce7ab58b244caaac072a176fe0c85486c6f2c5ef436097d299ebe3d5`.

## Verification states
Code integration requires passing tests, inventory, build, local link checks, then an actual GitHub Pages successful deployment. Public visual verification is separate; no claim of user-browser visual validation without observed evidence.
