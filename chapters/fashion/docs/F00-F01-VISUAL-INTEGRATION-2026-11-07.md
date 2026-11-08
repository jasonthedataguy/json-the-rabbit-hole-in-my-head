# Fashion — F00/F01 visual placement correction (2026-11-07, Asia/Ho_Chi_Minh)

## Scope and approval
Founder instruction on 2026-11-07: "yes fix it, and update on google drive and the digital book", approving the reviewed design choice: F00 only as circular chapter portal; F01 as first story illustration; F02 second. This authorizes the named digital book visual adjustment, **not** revision of prose, unrelated assets, additional media, cover edition, or social posts.

## Canon and source identity
- Book: .json — The Rabbit Hole in My Head
- Repository: `jasonthedataguy/json-the-rabbit-hole-in-my-head`
- Stable chapter slug: `fashion`; editorial number `04`; original-edition number `02`.
- Canonical source: `chapters/fashion/source/author-approved-v0.5.md`.
- Manuscript SHA-256 recorded in `chapters/fashion/chapter.json`: `9865a628ce7ab58b244caaac072a176fe0c85486c6f2c5ef436097d299ebe3d5`.
- The manuscript and chapter metadata are not changed by this visual fix.

## Artwork lineage
- F00 selected master (unchanged): Google Drive `artwork/portal-layers/masters/F00-A-selected-with-character-native.png`, SHA-256 `bc36a21737e0352575dd7dbcf75f287cdb2a39065a691cc2b6a8347908b86706`.
- Existing derived web export: `assets/digital-book/fashion/v1.1/f00-with-character.webp`, byte SHA-256 `614cb50189b5ddaa6224b10b5d12001ee9a7cc2616791ae4eebb957c68492e77`.
- F01 locked web illustration: `assets/digital-book/fashion/v1.1/f01-sneaker-dream.webp`, SHA-256 `2fab9e3a55b7accaec21102b3d3ed55c67811cf51584b073aaef4715e270d25e`.
- F02 remains the next in-text illustration; F03–F10 keep existing anchored placements and captions.
- Source artwork and prior F00 derivatives remain preserved; no images regenerated.

## Exact UI changes
1. Use approved F00-with-character for the Fashion chapter opening. Keep the existing no-foreground chapter-map export to preserve the shared book/map composition; do not use the no-character reconstruction as a newly approved chapter opening.
2. Mask only Fashion's square navy export surround using a 48.7% circle centred at 50%/50%. The artwork content is unmodified.
3. Remove the redundant F00 hero **and** legacy Fashion room banner before the chapter text in the main chapter leaf.
4. Remove the duplicate F00 hero and legacy banner in the page-turn book reader; the first in-text illustration is F01 at its exact canonical anchor, followed by F02–F10.
5. Keep all other chapters' hero behavior unchanged and bump web asset cache versions.

## Verification and release distinction
This is an approved, narrowly scoped web visual correction. Git commit/build/run proof and any live public verification must be recorded separately; a successful commit alone is not proof of a deployed/publicly verified site. No change to image rights, edition approval, or manuscript approval.
