# .json — Jason, Under Revision · Portal edition

A separate digital reading edition of the book. Its homepage is a navy cloth book cover with a rotating paper portal and the short “I like maths because…” introduction. It links to the introduction, illustrated chapter map, printed-style contents, published archive, and edition notes. The book’s reading order begins with the title page, epigraph, and source-based introduction, followed by the Cơm nguội prologue and five narrative parts. Chapters are continuous reading pages; the illustrated portal map and physical-edition notes are separate views. The original repository remains at [jasonthedataguy/json-under-revision](https://github.com/jasonthedataguy/json-under-revision).

The optional illustrated contents map uses a circular paper rim that follows mouse or touch angle and snaps to 11.25° stops while the central scene stays upright. Center swipes, scroll gestures, arrow buttons, keyboard navigation and the chapter index provide other ways in. Every portal carries its own item-and-number paper marker. Cơm nguội uses the exact navy-and-ivory rice-bowl badge from the supplied reference image, displayed without redrawing it. Fashion uses a Jordan 1 keepsake.

## Book structure

`dist/book.js` records the introduction, five Vietnamese part titles, and 32 chapter premises from the publisher narrative review. The introduction is editorial front matter, not an invented author preface. Published chapters retain their exact prose; chapters without full text display a clearly labeled Vietnamese outline. Browser history, type sizing, saved reading positions, a printed-style table of contents, and the mobile contents drawer support reading. Promotional material is absent from the opening; physical-book notes appear only under **Về ấn bản**.

## Published writing

The reader bundles all ten published manuscripts from the original repository at commit `b41b692b3e3633abea4997b6ac4513a91308f127`. Each approved manuscript and its metadata are preserved byte-for-byte under `content/chapters/`. Deployed Markdown copies and rendered reader content are under `dist/content/`.

Nine manuscripts have evidence-based links to the new 00–31 portal order. Their original titles are retained in the reader. **Dating 102** remains an additional essay in the published archive and is not assigned to the unrelated Tiểu hành tinh portal. Original chapter numbers and the new editorial IDs are recorded separately in [source provenance](docs/source-provenance.json). Chapters without a published manuscript remain clearly labeled previews.

Original memory experiences, downloads and multimedia remain reachable through links to the original published chapter pages. This repository does not modify the original archive.

## Work on this repository

- `dist/index.html` — cover and book-page markup.
- `dist/cover.css` — cloth-cover appearance, paper ring, and short introduction.
- `dist/app.js` — navigation, readers, and the cover/chapter-map interactions.
- `dist/book.js` — book introduction, five parts, and chapter outlines.
- `content/chapters/` — preserved author-approved manuscript source files.
- `scripts/check_site.py` — manuscript and public-file validation.

Push changes to `main` to run the GitHub Pages deployment workflow.

## Run locally

No package installation or build step is required. Python is used for validation and a local HTTP server:

```sh
python scripts/check_site.py
python -m http.server 4173 --directory dist
```

Then open http://localhost:4173. JavaScript modules require an HTTP server.

## Deployment

GitHub Pages deploys the tracked `dist/` directory on pushes to `main`. The workflow verifies manuscript hashes and public assets before upload. Set the repository Pages source to **GitHub Actions**. All asset paths are relative, so the site works beneath `/json-under-revision-v2/` and on other static hosts.

No tokens, runtime credentials, or external account connections are required by the site. Fonts are served locally with their OFL licenses. Preferences and reading positions are stored only in the visitor's browser.

## Content updates

To re-import from a local checkout of the original repository:

```sh
python scripts/import_reference.py --help
```

Keep editorial IDs separate from original archive numbers. Do not replace unpublished chapters with invented essays. The supplied book and illustration boards are concepts; no stock, pricing or manufactured-cover claims are made.
