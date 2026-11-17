# Fashion F00 V5.0 — web review handoff (2026-11-17)

Exact approved with-observer master: SHA-256 `3998354bba9cb854291e3b25a491cf4f8cd4225ada811b16ee4cb11f4a503199`; [Drive source](https://drive.google.com/file/d/11RxyR7W1pKiMRECUEY3p_m7F4TbEyraz/view).

## Scope
Draft integration only. Chapter 04 `opening` uses source-preserving transparent F00 with boy. `map` and `mainBook` temporarily reference a **review-only observer-free reconstruction** (95.07% of RGB pixels identical to approved art, localized replacement behind foreground boy); founder approval is still needed for that derivative before merging. `hero` stays `null` and F01–F10 placements/captions stay unchanged. `centre` stays the historical source until separately selected. Book title, chapter number, prose, assets for other chapters and all historical V1.2/V4 sources are retained.

Production pack: [Drive folder](https://drive.google.com/drive/folders/18DJaQWAy_a-kuTmGspu3_BF8CPvWjZIv), [ZIP](https://drive.google.com/file/d/1vGh2xbrt-PM2mNmg19F_1ed4I0o5L5LW/view), accompanying `F00-V5-LINEAGE.json`.

## QA / release gate

- Local checks: approved-source copy matches; circular alpha corners transparent; 1254×1254; selected no-boy reconstruction inspected side-by-side at square and thumbnail sizes.
- **Still required on PR:** `python scripts/build_inventory.py`, `python scripts/build_site.py`, `python scripts/check_site.py`, `python -m unittest discover -s tests -v`, desktop (1440×900) and mobile (390×844) screenshot review.
- PR creation and passing tests do **not** mean public publication; merging to main deploys automatically and must be separately authorized after derivative review.
