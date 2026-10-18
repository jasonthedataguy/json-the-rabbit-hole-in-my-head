# Manuscripts from the original repository

The new reader includes all ten published canonical manuscripts from
[`jasonthedataguy/json-under-revision`](https://github.com/jasonthedataguy/json-under-revision/tree/b41b692b3e3633abea4997b6ac4513a91308f127),
pinned to commit `b41b692b3e3633abea4997b6ac4513a91308f127`.

The `approved.md` and original `chapter.json` copies in
`content/chapters/<slug>/` are byte-identical to the selected source files.
Original metadata describes the original repository's paths and numbering;
the reader manifest records the corresponding new local paths separately.
Deployed Markdown downloads in `dist/content/manuscripts/` retain those same
source bytes, including original line endings.

Regenerate these artifacts with Python 3.10 or newer and an existing checkout
of the original repository at the pinned commit:

```sh
python3 scripts/import_reference.py /path/to/json-under-revision
```

The importer reads the source checkout without modifying it, verifies the
pinned commit, all expected manuscript hashes, byte lengths, and coverage of
published chapters. It writes `dist/content/manuscripts.json` and
`docs/source-provenance.json`. It needs only the Python standard library.

The reader JSON has a `source` object with `repo`, `commit`, and `url`, plus a
`chapters` array. Each entry includes:

- `editorialId`: portal atlas ID, or `null` for the additional archive chapter.
- `legacyId`, `originalTitle`, and `originalHeading`: the original source labels.
- `html`: the complete manuscript rendered with escaped text and safe links.
- `bodyHtml`: the same rendering with only the first heading omitted, for a
  reader that already displays the original title.
- `plainText`: complete readable text, including the original first heading.
- `sourcePath`: the new local canonical Markdown copy.
- `originalSourcePath`, `originalMetadataPath`, `sourceUrl`, and `archiveUrl`:
  pointers to the selected original content and its published chapter page.
- `sha256`, `bytes`, `paragraphCount`, and `downloadUrl`: integrity information
  and the local deployed Markdown download.

The original repository's chapter numbers and the supplied portal atlas IDs
are independent. The explicit mapping in `content/reference-map.json` preserves
nine justified assignments. “Thế giới trong mơ của tôi” is the complete
manuscript behind the “Metro số 5” portal. “Dating 102” remains an additional
archive chapter with `editorialId: null`; it is not assigned to portal 16.

Validation of the imported corpus confirmed 10 manuscripts, 233 complete body
paragraphs, and 80,917 source bytes. Every rendered paragraph was compared
with its original text after removing only Markdown formatting syntax, and
all copied manuscript and metadata bytes matched the pinned originals.
