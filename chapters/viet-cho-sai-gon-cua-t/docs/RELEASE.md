# Chapter 03 multimedia release

On 2026-10-16, the author rejected the assistant's board-derived rewrite and supplied the original essay. This correction restores all 20 original paragraphs without literary edits. `source/original.md` and `source/approved.md` preserve the attachment's exact 10,658 bytes, including its heading and CRLF line endings. The author's T/t voice, slang, dialogue, names, events and paragraph order are unchanged.

Source SHA-256: `911b174411dced9668dffd01c6860c079cc17e231c5235f5153666c6021d8b26`. The site validator enforces that hash and exact equality of the original and published manuscript. The original heading retains number 1 in the source files; the existing book registry and public route remain Chapter 03.

The generated draft and drafting notes are archived under `archive/superseded/saigon-board-derived-draft-v01/`, outside the deployed chapter. Their former reader-source URLs are removed. The version-history panel now contains the author's original, and the homepage subtitle, eight memory quotes and closing quotation use the author's own words.

- Reader URL: https://jasonthedataguy.github.io/json-under-revision/chapters/03/
- Slug alias: https://jasonthedataguy.github.io/json-under-revision/chapters/viet-cho-sai-gon-cua-t/
- Homepage: https://jasonthedataguy.github.io/json-under-revision/

The release includes the complete prose, a homepage card, responsive supplied-art crops, eight keyboard-accessible memory stops, version history and a selected-manuscript download. All memory, carousel, film and story-card excerpts occur verbatim in the selected text. Eight crops are documented in `artwork/scenes/index.json`; no new scenes or photographs were generated.

The earlier reader release now includes an illustrated six-page A5 proof, cover/poster exports, five film edits, synthetic ambience, recording scripts, provisional SRT/VTT captions, carousel and platform assets, three stories and a highlight. The existing reader design and memory journey are retained; actual media and downloads are added. Available products are included in the complete ZIP. Films await the author's recording and final speech-caption timing. The PDF is an editorial proof; printer production, QR and author-managed social posting remain separate.

## Local verification

- Repository unit tests cover scaffolding, manuscript rendering and template path containment.
- Homepage and Chapter 03 checked at 320, 390, 820 and 1440px: no horizontal overflow; images decode.
- Homepage contains four chapter cards in chapter-number order; navigation and slug redirect work.
- All 20 rendered paragraphs match the original attachment, with and without JavaScript; Markdown film-title emphasis is preserved.
- All eight journey controls work by keyboard, update their pressed state, caption and image.
- Version-history details show the original; reduced-motion behavior checked. The manuscript download matches the attachment's exact SHA-256. The rejected draft and drafting-note URLs return 404.
- Existing chapter manuscripts and interactive controls remain unchanged.
- Standalone chapter HTML loads its images, shared styles and manuscript download from the local folder.
- Browser reports no page errors. Actual 390px and 1440px screenshots are stored in `previews/`.
- Media QA checks all 20 original paragraphs in the A5 PDF and full decoding, dimensions and duration of all five films. Product excerpt checks reject text absent from the original.
- The site validator checks all ten generated pages, local links, product inventories, the 12 supplied Saigon reference files and 92 archived originals.

GitHub Actions performs the build, tests and site validation again on the published commit before deploying `site/` to Pages.
