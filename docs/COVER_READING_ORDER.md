> **Historical design-change note (18 Oct 2026).** The ring-stop numbers and chapter positions below reflect an earlier interim state. The current `book.json` has 36 narrative entrances (00–35) and 38 cover selector states including Cover + Introduction. See [current BOOK_STRUCTURE](BOOK_STRUCTURE.md) and [Product Master 2026-10](PRODUCT_MASTER_2026-10.md). Do not use the old counts below to generate print/video labels.\n\n# Cover and reading update — 18 October 2026

The homepage opens on the earlier dusk-city landscape cropped from the supplied design board. The next ring stop reveals the open-book Introduction scene, followed by the earlier three-person Cold Rice Prologue (00) and Chapters 01–32. One paper ring cut from the supplied design board turns through all 35 homepage stops, carrying Jason's head and body in the foreground while the centre scene changes. The separate chapter map has 33 stops. Returning to the homepage starts on the cover. The curved quote stays upright around the rotating ring.

English navigation and chapter headings leave the original Vinglish chapter manuscripts intact. The five part names display `key | Vietnamese title` throughout the reader. The Introduction now presents the author's supplied Vietnamese synopsis and reader promise. Original titles remain in metadata and source notes. The production board is regenerated from this metadata. Raw source manuscripts and downloads are unchanged.

The supplied board and extracted landscape stay untouched. The active cover scene is the board crop; the active Cold Rice scene is the earlier family-meal illustration. The newer 3000-pixel Saigon and father-and-child scenes remain separate print-study alternates. Jason still belongs only to the rotating ring. The source board, current scenes, Introduction scene and ring variants are documented in [portal artwork](PORTAL_ARTWORK.md); separate print masters and dielines are in the [print prototype](../print/README.md). The reading pages use bundled Noto Serif regular and italic variable fonts, with the SIL OFL license included in the public build. This resolves the uneven Vietnamese diacritic spacing seen with the prior fallback font. Desktop labels are larger, long titles wrap, and the reading column has a consistent line length and paragraph rhythm.

Earlier browser validation of the 34-stop ring and layout, before Dating 102 became Chapter 19 and the artwork selection changed:

- All 34 cover stops, both wrap directions, Home/End, Enter, numbered selection, buttons, wheel, live angular dragging, and real mobile touch input passed.
- The chapter map still wraps through 32 chapters independently.
- All ten rendered manuscripts match their generated bodies, and downloads match original source bytes.
- Desktop 1440px and mobile 390px/320px layouts passed overflow checks. The screenshots were visually inspected, including Vietnamese prose and a long English chapter title.
- No browser errors or failed local HTTP requests. Noto Serif loads successfully; both faces include all Vietnamese diacritics used in the manuscripts.
- The nine source/build unit checks and generated-site integrity/link validation passed.

The browser screenshots above and the 34-stop interaction results were recorded before the design-board ring and centred scenes were added. The current artwork fits are shown in the [cover composition](qa/cover-board-composition.png), [Introduction composition](qa/introduction-board-composition.png) and [Cold Rice composition](qa/cold-rice-board-composition.png). The new frame/scene integration passed the site build and integrity checks; browser interaction and responsive visual regression remain to be rerun for this latest art change.

Earlier screenshots: [desktop cover](qa/cover-desktop.png), [mobile cover](qa/cover-mobile.png), [desktop reading typography](qa/prose-desktop.png).

Browser regression check (requires Playwright and Chromium, plus a running local preview):

```sh
python tests/browser_reader.py
```

Use `--browser` for an existing Chromium executable and `--output` for a screenshot directory. The normal Python unit test discovery does not require Playwright.
