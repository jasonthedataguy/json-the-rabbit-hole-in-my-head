# Asteroid digital QA

On 2026-10-19, the generated site was checked in headless Edge at 1440×900 and 390×844. The Chapter 16 leaf, chapter map, homepage Chapter 16 stop and standalone reader loaded the new art without horizontal overflow. The selected manuscript rendered nine paragraphs in each reading surface; the chapter map reported full text and the chapter marker used the updated orbit icon. The desktop cover and its reading panel both measured 833 px high. Source/build checks passed with 33 editorial chapters, 16 exact manuscripts and all local links; nine unit tests passed.

Visual evidence: [aligned portal](../../../docs/qa/asteroid-board-portal-composition.png), [desktop chapter](../../../docs/qa/asteroid-chapter-desktop.png), [mobile chapter](../../../docs/qa/asteroid-chapter-mobile.png), [desktop chapter map](../../../docs/qa/asteroid-map-desktop.png), [desktop cover stop](../../../docs/qa/asteroid-cover-desktop.png), [mobile standalone reader](../../../docs/qa/asteroid-standalone-mobile.png).

These checks cover local browser rendering. The flattened JPG still needs separated original artwork and printer specifications before a print file can be certified.
