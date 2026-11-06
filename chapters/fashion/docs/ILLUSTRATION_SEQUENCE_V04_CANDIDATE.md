# Fashion — Be Your Own Label: five-scene illustration sequence (candidate)

- **Date:** 2026-11-06 (Asia/Ho_Chi_Minh)
- **Accountable project:** JP (.json Publishing & IP)
- **Chapter:** 04 / `fashion`
- **Manuscript:** author-approved Hybrid V0.4, SHA-256 `dd81d8c35b7ff542c36cdb0be3f26a6685406b11e30cb8a88d8ccf83697abb47`
- **Decision status:** Founder requested new Fashion digital-book illustrations and supplied four visual references. Five-scene arrangement below is an editorial candidate. The fifth source-derived montage has **not** been individually approved; release/technical/public verification is pending.
- **Public release:** **Not yet changed by this candidate document.** This file alone must not trigger a reader artwork change.

## Sequence and manuscript anchors

| Sequence | Artwork | Manuscript anchor (place figure immediately after) | Editorial function |
| --- | --- | --- | --- |
| 01 | **Culture and aspiration** — proposed collage of reference #4 (the mirror/hip-hop scene), without new memoir events | `Hoặc ít nhất, this is who I want to be.` | Childhood influences, hip-hop, the aspirational self |
| 02 | **The desire loop** — supplied reference #3 (sneaker choices, coin jar, trend economics) | `Cứ thế, từ một sở thích, fashion đôi khi trở thành một cuộc đua` | Consumer desire and the repeated trend cycle |
| 03 | **The mirror and the rulebook** — supplied reference #4 (trying identities before a mirror) | `Mà là mình có thực sự thích những gì mình đang mặc hay không.` | Borrowed identity, imitation and fashion rules |
| 04 | **Own label** — supplied reference #2 (quiet confidence inside the wardrobe rings) | `Hãy để chúng làm nền cho bạn.` | Personal expression without prescribed rules |
| 05 | **What remains** — supplied reference #1 (holding a worn jacket, old sneakers and keepsakes) | `Believe me or not, cái cảm giác lục tủ đồ của bố bạn` | Memories, wear marks and value beyond resale |

## Source provenance (exact user-supplied JPEG bytes)

| Reference in user message | SHA-256 | Scene |
| --- | --- | --- |
| #1, worn garment | `1ca7060e2454399a2729bac6c369fa845967c78aa18dcd9715d4585b037f287c` | 05 |
| #2, standing figure | `81d3456671d5527e3a332269d80e3787525107a912cee89c355abecb55e69fb4` | 04 + wide hero |
| #3, sneaker economics | `8d0067b66619b64dc36fbacbb609fcfd5aea689f77015d94f1ebe0449a979e0c` | 02 |
| #4, mirror | `a0ef702b2884be334ed58bcf6977a2e2f0f2d4c5a50eee4a998b8cb1123e9156` | 01 derived + 03 |

Source identity: founder-supplied images in JP project chat, 2026-11-06. Creator and commercial reuse rights have **not** been independently verified. Screen-only editorial selection; no assumption of print/film/social licenses.

## Implementation and safeguards

The prepared local package `fashion-v04-five-illustrations-package.zip` contains the four source JPEGs, five screen-optimized WebP illustrations, one wide hero and a scoped, dry-run-first integration script. It is a **conversation attachment**, not yet a committed repository asset. This draft branch intentionally does not refer to missing public files.

The integration script is designed to update only Fashion's `hero`, `inline` and `extras` reading images in `shared/web/digital-art.js`, insert figures after exact V0.4 paragraphs, register new assets, provide accessible captions and alt text, and bust the reader cache. Existing source manuscript, original illustrations and other chapters are preserved.

**Portal navigation art (`mainBook`, `map`, `opening`, `centre`) stays unchanged** in this proposal. Prior child-facing portal direction conflicts with the teenager in all four supplied images. A separately reviewed child-facing portal is needed before replacing navigation art.

## Release gates

1. Upload the binary assets from the prepared package to the review branch; run the scoped integration script.
2. Validate source SHA, build inventory, site build, check_site, unit tests, mobile layout, exact anchors, image alt text and browser cache.
3. Founder reviews the five-scene sequence and separate portal decision; rights scope confirmed.
4. Merge approved code/assets and verify the **actual** Chapter 04 public URL. Record Git revision, asset hashes and public evidence before marking release approved or publicly verified.

**No new Jira issue.** Existing accountable editorial work: JP-1; reader delivery: JP-2. Other derivative owners are unaffected.
