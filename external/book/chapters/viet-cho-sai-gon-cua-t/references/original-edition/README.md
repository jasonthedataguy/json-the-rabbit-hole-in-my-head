# 03 — Viết cho Sài Gòn của t

**State: complete multimedia proof set.** [Read Chapter 03](https://jasonthedataguy.github.io/json-under-revision/chapters/03/) or open the [book homepage](https://jasonthedataguy.github.io/json-under-revision/). The author supplied the original essay on 2026-10-16 to replace the assistant's rewrite. The published manuscript preserves that original verbatim. The full text and eight-stop memory journey now have an illustrated A5 proof, eight artwork crops, a social pack and five video edit previews.

The author designated this as Chapter 03 and selected `Saigon_Chapter_Project_Board_v01` as the reference. All 12 supplied files are preserved byte-for-byte under [references/project-board-v01](references/project-board-v01/). The original delivery contained no manuscript, A5 chapter, film or chapter website.

Open [the original project board](references/project-board-v01/PROJECT_BOARD.html) locally after cloning/downloading the repository. It includes the supplied poster concept and an editable 75-task checklist. Its browser progress stays on that device; export CSV to retain changes.

The original board says **working chapter 01**. That historical label is preserved in the reference; [chapter.json](chapter.json) is authoritative for the current **03** number and stable slug `viet-cho-sai-gon-cua-t`. Its old task statuses and publication instructions describe the source package, not current completion or a new approval requirement.

| File or folder | Purpose |
|---|---|
| [chapter.json](chapter.json) | Chapter 03 identity, palette, provenance and `publish: true` / `release_stage: multimedia` |
| [production.json](production.json) | Reproducible crops, print placements, exact excerpts, five film timelines and supplemental channel formats |
| [source/approved.md](source/approved.md) | Complete published manuscript; identical to the supplied original |
| [source/original.md](source/original.md) | Original author attachment, preserved byte-for-byte |
| [docs/MANUSCRIPT_IMPORT.json](docs/MANUSCRIPT_IMPORT.json) | Source checksum, byte count and original-text preservation record |
| [source/README.md](source/README.md) | Manuscript lineage and publication selection |
| [artwork/source/README.md](artwork/source/README.md) | Supplied illustration references and export mapping |
| [docs/DESIGN_REVIEW.md](docs/DESIGN_REVIEW.md) | Design principles and mapping into the shared chapter system |
| [docs/PRODUCT_SET.md](docs/PRODUCT_SET.md) | Actual inventory and outstanding chapter products |
| [book/chapter-A5-proof.pdf](book/chapter-A5-proof.pdf) | Six-page illustrated A5 proof containing all 20 original paragraphs |
| [artwork/exports/cover-a5.svg](artwork/exports/cover-a5.svg) | Editable cover typography with a separate supplied-art crop |
| [video/STORYBOARD.md](video/STORYBOARD.md) | Five cuts with provisional timings, plus adjacent MP4/SRT/VTT files |
| [audio/reading-script.md](audio/reading-script.md) | Complete original for author recording; per-cut scripts are alongside it |
| [social/BRIEF.md](social/BRIEF.md) | Five-card carousel, three stories, highlight, Facebook, TikTok and YouTube assets |
| [docs/BOARD_REVIEW.md](docs/BOARD_REVIEW.md) | Current findings against the supplied project board |
| [docs/REFERENCE_IMPORT.json](docs/REFERENCE_IMPORT.json) | Exact-byte import checksums for every supplied file |
| [references/project-board-v01](references/project-board-v01/) | Unmodified board, art concepts, task data, design notes and board screenshots |

The reader route is `/chapters/03/`; `/chapters/viet-cho-sai-gon-cua-t/` redirects there. The chapter appears on the homepage in chapter-number order. The published manuscript and version-history panel use the author's original essay. The superseded rewrite is retained only in the repository archive, outside the deployed chapter.

Rebuild with `python scripts/build_products.py --chapter viet-cho-sai-gon-cua-t --video --ffmpeg <path>`, then validate with `python scripts/verify_products.py --chapter viet-cho-sai-gon-cua-t --ffmpeg <path>`. Videos await the author's recording and final speech-caption timing; the PDF is an editorial proof. No generated voice. QR remains deferred; social posting stays author-managed.
