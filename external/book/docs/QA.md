# Structure migration verification — 18 October 2026

The local v2 migration passed the following checks. These results cover the repository migration and website integration, not a new certification of inherited print/media products.

Current reader order has 33 editorial slots (`00`–`32`), 11 full manuscripts and 22 outlines. Dating 102 is Chapter 19 after Dating Algorithm. The table below records the earlier migration audit before this chapter-order update; current build and link validation are reported by `scripts/check_site.py`.

| Check | Result |
|---|---|
| Chapter registry | 32 editorial slots, 23 outline-only slots, 10 published manuscripts including one archive-only essay |
| Original import | 1,377 original-repository files audited against the pinned checkout; no changed imported derivatives |
| Migration record | 1,412 preserved input mappings including portal assets and manuscript snapshots |
| Manuscript integrity | All 80,917 selected source bytes preserved; downloads match sources |
| Product structure | 33 chapter folders and 214 declared existing deliverables |
| Public build | 811 generated files, about 282 MB; active inputs and outputs recorded by SHA-256 |
| Source and local-link validation | Passed; original offline poster/srcset mistakes repaired only in generated output |
| Unit checks | 9 passed: manuscript integrity, missing products, duplicate registry, path isolation, non-destructive scaffold, generated-output cleanup, line-ending audit and inert Markdown rendering |
| Cover controls | All 32 scenes, both wraparound directions, live angular drag, wheel, numbered selection, keyboard, touch swipe and reduced motion passed |
| Reader and immersive pages | All 10 readers match DOM-normalized source rendering; all 10 local experiences load; print/film HTTP checks pass |
| Interactive sample | Cơm nguội memory selector changes the image and pressed state |
| Browser errors / failed local HTTP requests | None observed in the integration audit |
| Layout | Cover inspected at 1440px and 390px; 320px overflow and ring controls checked |
| Original repository | Working tree remains unchanged |

Screenshots: [desktop cover](qa/cover-desktop.png), [mobile cover](qa/cover-mobile.png).

Standard checks:

```sh
python -m unittest discover -s tests -v
python scripts/build_inventory.py
python scripts/build_site.py
python scripts/check_site.py
```

Additional local browser checks used the installed Playwright/Chromium environment and actual pointer, keyboard and touch input. External network requests were blocked during the chapter integration audit. Human screen-reader review, physical-device testing, retimed author narration, physical print tests and v2 adaptation of inherited product labels remain listed production work. Changes have not been pushed or deployed.
