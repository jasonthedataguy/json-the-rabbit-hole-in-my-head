# .json — Jason, Under Revision · Portal edition

A separate edition of the book website, with 32 rotating chapter portals, five narrative acts and a quiet text reader. The original repository remains at [jasonthedataguy/json-under-revision](https://github.com/jasonthedataguy/json-under-revision).

The circular paper rim follows mouse or touch angle and snaps to 11.25° stops while the central scene stays upright. Center swipes, scroll gestures, arrow buttons, keyboard navigation and the chapter index provide other ways in. Every portal carries its own item-and-number paper marker. Cơm nguội uses the exact navy-and-ivory rice-bowl badge from the supplied reference image, displayed without redrawing it. Fashion uses a Jordan 1 keepsake.

## Published writing

The reader bundles all ten published manuscripts from the original repository at commit `b41b692b3e3633abea4997b6ac4513a91308f127`. Each approved manuscript and its metadata are preserved byte-for-byte under `content/chapters/`. Deployed Markdown copies and rendered reader content are under `dist/content/`.

Nine manuscripts have evidence-based links to the new 00–31 portal order. Their original titles are retained in the reader. **Dating 102** remains an additional essay in the published archive and is not assigned to the unrelated Tiểu hành tinh portal. Original chapter numbers and the new editorial IDs are recorded separately in [source provenance](docs/source-provenance.json). Chapters without a published manuscript remain clearly labeled previews.

Original memory experiences, downloads and multimedia remain reachable through links to the original published chapter pages. This repository does not modify the original archive.

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
