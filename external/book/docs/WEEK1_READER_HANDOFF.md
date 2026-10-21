# Week 1 reader handoff

Status: the post-read step was approved and published to the digital book on 21 October 2026. The October 27 campaign aims to bring social visitors into the digital book. The single primary action after a chapter is **Next chapter**. **Contents** is secondary. At the final chapter, **Browse all chapters** becomes the primary action and **Book cover** is secondary. The existing previous/next page footer remains for normal book navigation. The campaign links below remain drafts; no social posts have been published by this change.

No owned social account, updates page or contact route has been verified in the current book configuration or chapter social files. The live page therefore has no Follow action. It has no email form, preorder or deposit checkout. An updates action can be added only after its destination is supplied and verified; email collection would additionally need a working opt-in flow, consent text, storage and unsubscribe process, with a privacy/legal review before any personal information is stored.

## Proposed campaign links

Each query string precedes the `#chapter/NN` route. These are link drafts for manual placement in author-approved posts; no posts have been published by this change. The existing chapter social captions still point to the earlier edition and must be reviewed before reuse.

| Campaign | Proposed URL |
| --- | --- |
| Cold Rice · TikTok | `https://jasonthedataguy.github.io/json-the-rabbit-hole-in-my-head/?utm_source=tiktok&utm_medium=organic_social&utm_campaign=cold_rice_w01#chapter/00` |
| Fashion · Instagram | `https://jasonthedataguy.github.io/json-the-rabbit-hole-in-my-head/?utm_source=instagram&utm_medium=organic_social&utm_campaign=fashion_w01#chapter/04` |
| To My Saigon · Facebook | `https://jasonthedataguy.github.io/json-the-rabbit-hole-in-my-head/?utm_source=facebook&utm_medium=organic_social&utm_campaign=saigon_w01#chapter/14` |

The former `/json-under-revision-v2/` GitHub Pages URL returned 404 after the repository rename. Replace any previously copied campaign drafts with the URLs above before posting.

## Measurement for Week 1

This site currently has no campaign analytics, event collector, signup endpoint or consented attribution pipeline. A UTM label in a URL does not itself record a visit or conversion. This release adds none of those systems and sends no new event beacons. The reader's existing on-device reading-position and display preferences remain separate from campaign measurement.

Use a declared manual log after a post is actually published: record the platform, post URL, date, campaign URL, and the native platform's reported reach and outbound-link clicks **only if the account owner can access those figures**. Mark unavailable figures `N/A`; do not substitute likes for clicks. Website landings, chapter completions, Next chapter clicks, email signups, purchases and cross-device attribution are `N/A` under this method. Platform link clicks are intent to leave the platform, not proven website readers. No visitor-level data should be copied into the log. This gives a limited channel-side signal, not a measured site conversion rate.

Manual log template: `date | platform | post URL | campaign URL | native reach or N/A | native outbound-link clicks or N/A | site landings: N/A | Next chapter clicks: N/A`. Leave the log empty until a real author-approved post and its platform figures exist.

## Link QA and release gate

Local Chrome QA on 21 October 2026 passed for all three URLs at 1440×900 desktop and 390×844 emulated phone widths. Each opened the intended full chapter; Next chapter and Contents both worked and preserved the UTM query before the route fragment. No horizontal overflow or signup form appeared. The emulated phone tests used simulated TikTok, Instagram and Facebook user-agent tokens, so they catch obvious route problems but cannot stand in for those actual in-app browsers. Actual phone and in-app link-sticker/bio-link tests remain `N/A` until the account owner performs them in the target apps. Record redirects, blocked fragments and final URLs before approving a public post.

The deployed GitHub Pages site also passed a live Chrome check for all three proposed query URLs at both viewport sizes. Each chapter route and both post-read actions worked, with the UTM query preserved. The final chapter fallback passed as well.

Review images: [desktop post-read panel](qa/week1-post-read-desktop.png) and [emulated phone post-read panel](qa/week1-post-read-mobile-emulated.png).

The founder approved the **Next chapter → Contents** post-read step. A verified owned updates destination is needed to add Follow. Social posts, tracked conversion claims and checkout remain outside this release; the account owner should complete actual phone and in-app link checks before posting.
