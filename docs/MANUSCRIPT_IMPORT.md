# Manuscript and product provenance

The original edition is pinned to `b41b692b3e3633abea4997b6ac4513a91308f127`. Ten selected manuscripts, their original prose/history and tracked product kits are held locally under `chapters/<slug>/`. The ten selected manuscripts remain 80,917 bytes in total.

`chapter.json` now describes v2. The original `chapter.json` is preserved at `references/original-edition/chapter.json` inside that chapter, and the pinned selected manuscript is preserved beside it as `approved.md`. Original product labels, metadata and source numbers stay distinct from editorial slots 00–31.

The original mapping is [references/original-edition/manuscript-map.json](../references/original-edition/manuscript-map.json). Nine manuscripts map to portals. Dating 102 remains an additional archive essay; it is not assigned to Tiểu hành tinh. All source-based previews retain their existing outlines.

Two original Windows checkout files used CRLF while v2’s pinned manuscripts used LF. The checkout bytes were preserved as `approved-checkout.md` in the relevant chapter references, and the existing v2 selected bytes remain canonical. No prose was rewritten.

Build the deployed manuscript library from local sources:

```sh
python scripts/build_site.py
python scripts/check_site.py
```

Audit the complete imported original product files against the pinned checkout:

```sh
python scripts/import_reference.py /path/to/json-under-revision --check
```

`--restore-missing` restores missing recorded original files only and never overwrites an existing v2 derivative. The audit tolerates checkout line-ending differences only when a candidate reconstructs the exact recorded intake SHA-256. Moving to another source commit is a new intake and requires a new provenance record.

The old v2 importer is preserved in `references/portal-v2/`; it is not the active workflow. Generated `dist/content/manuscripts.json` records current source paths, original identities, safe rendered HTML, manuscript hashes and local experience/download URLs. `docs/source-provenance.json` is refreshed by the build.
