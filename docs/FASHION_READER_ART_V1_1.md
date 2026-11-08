# Fashion — Digital Book illustration integration V1.1

**Date:** 2026-11-07 (Asia/Ho_Chi_Minh)  
**Owner:** JS — .json Creative Studio  
**Source:** `chapters/fashion/source/author-approved-v0.5.md` (selected V0.5; author manuscript unchanged)  
**Base commit:** `408012b18ad7fd36f5db81023b2370cbf1f86c3f`  
**Art identity:** founder-locked F00–F10 Visual Selection V1.0, private Drive library under `Studio_Production/01_Originals/book/chapters/fashion`.

## Exact reader roles

- Interactive cover, Fashion stop `mainBook` → `f00-no-foreground.png`.
- Chapter map, Fashion stop `map` → same character-free portal.
- Chapter 04 opener `opening` → `f00-with-character.webp`.
- Opening reading spread `hero` → `f00-hero.webp`.
- Stationary mirror source `centre` → `f00-centre.webp` (not a replacement for the global shared ring).
- F01–F10 use the exact `placements` order and paragraph anchor strings in `shared/web/digital-art.js`. These captions are newly authored **illustration captions**, not author manuscript or quotations. No change to source/ or chapter.json.

The character-free portal comes from the registered no-foreground layer rather than the older F00 pack's `mainBook.webp` / `map.webp`, both of which still showed the foreground character. Selected as the reader variant for this explicit request; distinct from approval of the no-character reconstruction as a native animation clean plate.

## Placement and caption index

| ID | After the paragraph containing | Caption | Web export |
|---|---|---|---|
| F01 | `Một đôi giày đôi khi không chỉ là một đôi giày.` | Một đôi giày đôi khi là hình ảnh của người mình muốn trở thành. | `f01-sneaker-dream.webp` |
| F02 | `Ba thứ ấy nghe thì có vẻ giống nhau, nhưng hình như không hoàn toàn là một.` | Mình là ai, mình muốn trở thành ai, và muốn người khác nhìn thấy ai? | `f02-triple-mirror.webp` |
| F03 | `Cứ thế, từ một sở thích, fashion đôi khi trở thành một cuộc đua` | Mỗi mùa một xu hướng mới; chiếc vạch đích của ham muốn cứ lùi xa. | `f03-trend-machine.webp` |
| F04 | `Rồi dần dần từ đống đồ mình copy của thiên hạ mới hình thành được` | Học theo người khác cũng có thể là bước đầu tìm ra style của mình. | `f04-wardrobe-classroom.webp` |
| F05 | `Một công việc có prestige, một mức thu nhập đáng mơ ước` | Đôi khi ta chọn một cuộc đời giống như chọn một bộ đồ vừa mắt người khác. | `f05-life-rulebook.webp` |
| F06 | `Chúng ta có thể dành rất nhiều thời gian và công sức để trở thành một người` | Có những kỳ vọng chưa từng được nói ra — chỉ do mình hình dung. | `f06-imagined-expectations.webp` |
| F07 | `Mình có thể dành cả đời để chứng minh mình không sống theo kỳ vọng` | Thoát khỏi một chiếc nhãn đôi khi lại là bắt đầu mang một chiếc nhãn khác. | `f07-authenticity-paradox.webp` |
| F08 | `Có khi chỉ là đổi từ một cái logo trên áo sang một thứ logo vô hình khác mà thôi.` | Logo trên áo có thể biến mất; logo trong câu chuyện về bản thân thì chưa chắc. | `f08-invisible-logo.webp` |
| F09 | `Believe me or not, cái cảm giác lục tủ đồ của bố bạn` | Một món đồ được thừa hưởng vẫn có thể trở thành của riêng mình. | `f09-dads-wardrobe.webp` |
| F10 | `Is the person I’m trying to become really the person I want to be?` | Không nhất thiết phải có câu trả lời; điều quan trọng là còn dám tự hỏi. | `f10-open-identity.webp` |

## Release and validation boundaries

- Preserve chapter 04 / original edition 02 identity.
- Only update the four requested Fashion reader surfaces and their asset mappings; other chapters use the previous generic insertion logic.
- Verify the site build and correct image decode before merging/releasing; inspect desktop and mobile cover, map, chapter view and desktop cover reading pane.
- No GitHub Pages deploy, domain change, Drive write, marketing publication, or Jira status transition is authorized by this change.
- Rights/public-distribution review of new artwork/captions remains separate. A source PR is not proof of live publication.
