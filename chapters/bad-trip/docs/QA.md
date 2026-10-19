# Bad Trip digital QA

On 2026-10-19 the built digital book was checked in headless Chrome at 1440×900 and 390×844. Chapter 16, its map stop, homepage cover stop and standalone reader load the aligned mirror artwork without horizontal overflow. The selected manuscript renders 228 paragraphs and two section breaks. The chapter map reports full text and uses the mirror icon. On desktop, the cover and reading panel both measure 833 px high.

Shifted direct routes were checked: Chapter 15 I Am 28 Today, 16 Bad Trip, 17 Asteroid, 18 Three Meeting Theory, 19 Dating Algorithm, 20 Dating 102, 22 Run away and 33 An Apology. The site validator reports 34 chapter slots, 18 exact selected manuscripts, protected originals and working local links; nine unit tests passed.

Visual evidence: [aligned portal](../../../docs/qa/bad-trip-board-portal-composition.png), [desktop chapter](../../../docs/qa/bad-trip-chapter-desktop.png), [mobile chapter](../../../docs/qa/bad-trip-chapter-mobile.png), [desktop chapter map](../../../docs/qa/bad-trip-map-desktop.png), [desktop homepage stop](../../../docs/qa/bad-trip-cover-desktop.png), [mobile homepage stop](../../../docs/qa/bad-trip-cover-mobile.png), [mobile standalone reader](../../../docs/qa/bad-trip-standalone-mobile.png).

The supplied flattened board supports these digital crops. It does not provide separated original layers for certified print production.
