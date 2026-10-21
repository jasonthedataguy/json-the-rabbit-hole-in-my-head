# Cold Rice — digital-book design update

Concrete reuse proposal; no site source or deployment changed. Preserve `com-nguoi`, prologue 00 and original 07 in history.

The reader's `docs/DIGITAL_ASSET_PACK.md` records installation of this artwork library on 20 October, and current source asset mappings exist. The external library's older README describes its own non-deploying behavior; do not interpret that as proof the separate reader is still unintegrated. Check selected mappings/rendering, without another bulk import.

## Reading sequence

| Surface | Existing E: asset | Treatment |
|---|---|---|
| Main-book stop | `chapters/com-nguoi/artwork/main-book/portal.webp` | Full portal without foreground observer; no extra ring over it |
| Map | `chapters/com-nguoi/artwork/chapter-map/portal.webp` | Independent map file; UI labels remain separate |
| Opening | `chapters/com-nguoi/artwork/chapter-page/portal.webp` | Keep Jason at threshold; display metadata Cold Rice / 00 |
| Hero | `chapters/com-nguoi/artwork/chapter-page/hero.webp` | Full family-table composition after title, before prose |
| Body | `chapters/com-nguoi/artwork/content/illustrations/01-story-detail.webp` | Proposed after source line 9, before `Tớ không muốn bố phải ăn cơm nguội.`; leave ending uninterrupted |

Resolve these under `E:\books\.json\outputs\json-digital-book-assets`; the linked asset index contains exact paths/hashes. Keep complete 3:2 illustrations responsive at natural proportions, using available 960px alternatives. No new chapter artwork is required.

Keep the established **Read / Explore / Revisit** structure. Read presents full approved text without interaction. Explore reuses `production.json.memory`'s **Bố → Tớ → Bây giờ** and exact source quotes at lines 9/11/17, with buttons, visible focus and a linear fallback. Revisit links actual source/history and existing A5 proof, labeled an editorial proof until its edition references are reviewed. Do not create a new interaction to fill a lane.

Use existing licensed Noto Serif for Vietnamese prose and labels. The supplied DM Sans file showed missing Vietnamese glyphs during new social export review; those exports use Noto Serif throughout. Keep DM Sans for controls only with verified Vietnamese coverage/fallback. Proposed reader review targets: 18–20px mobile body, line height near 1.65, larger-screen line length around 65 characters; retain established tokens where already effective. Keep selectable text, accents, deliberate paragraph breaks, keyboard/touch controls, meaningful focus, no autoplay sound and reduced-motion/static fallback.

Alt text after inspecting existing placement proof: hero `Minh họa ba người ngồi bên bàn ăn dưới ánh đèn vàng, nhìn từ phía sau.`; inline `Minh họa một đứa trẻ cùng bố mẹ bên bàn ăn có tô cơm và nồi cơm.` These are illustrations, not photographs. Decorative patterns use empty alt. Do not infer which illustrated portion is cold from steam.

End with **Đọc chương tiếp theo**, resolved from actual registry, plus contents. Social acquisition CTA is **Đọc trọn Cơm nguội**. No new newsletter or paid checkout until real consent/delivery is approved and implemented.

Shared cover keeps the exact title **.json - the rabbit hole in my head** and `shared/main-book/master-ring/book-copy.json`. Jason stays fixed; center upright; ring/Gấu move. Preserve Cold Rice's own observer choices rather than applying shared-cover rules to every chapter asset.

## Target and QA

Registry target: `https://jasonthedataguy.github.io/json-the-rabbit-hole-in-my-head/#chapter/00`. This is a configured target, not a live-verified URL. Old captions use the original `/json-under-revision/chapters/07/` archive; replace campaign links without destroying history.

G2 needs complete rendered text against approved bytes, mobile/desktop inspection, image loading, keyboard/touch/screen-reader review, reduced motion, alt text and onward/source links. G3 adds actual deployed route/CTA and campaign attribution tests. Put UTMs before the fragment. No live verification or source changes are claimed.

If integration changes are authorized later, follow book AGENTS.md, edit source UI/registry only, preserve revisions, run prescribed inventory/build/integrity/unit checks and inspect actual layouts. Generated `dist/` stays unedited. Existing physical cover and print files remain proofs requiring printer/physical tests.
