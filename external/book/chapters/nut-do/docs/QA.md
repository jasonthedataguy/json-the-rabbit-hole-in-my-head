# Red Button digital QA

On 2026-10-19, the generated site was checked in headless Edge at 1440×900 and 390×844. The Chapter 06 leaf, chapter map, homepage Chapter 06 stop, and standalone reader all loaded the new artwork without horizontal overflow. The manuscript rendered 19 paragraphs in each reading surface; the chapter map reported full text. The desktop cover and its reading panel both measured 833 px high. Source/build checks passed with 33 editorial chapters, 14 exact manuscripts, and all local links; nine unit tests passed.

Visual evidence: [aligned portal](../../../docs/qa/red-button-board-portal-composition.png), [desktop chapter](../../../docs/qa/red-button-chapter-desktop.png), [mobile chapter](../../../docs/qa/red-button-chapter-mobile.png), [desktop chapter map](../../../docs/qa/red-button-map-desktop.png), [desktop cover stop](../../../docs/qa/red-button-cover-desktop.png), [mobile standalone reader](../../../docs/qa/red-button-standalone-mobile.png).

These checks cover local browser rendering. The flattened JPG still needs separated original artwork and printer specifications before a print file can be certified.
