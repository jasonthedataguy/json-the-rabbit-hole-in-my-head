# Canonical book-title proposal — 2026-10-30; corrected 2026-10-31

## Final founder-approved display identity

**.json — The Rabbit Hole in My Head**

- **Title component:** `.json` (leading dot included).
- **Subtitle component:** `The Rabbit Hole in My Head`.
- **Complete display title:** `.json — The Rabbit Hole in My Head`.
- **Production platform:** `.json Studio` (unchanged).
- **Working book repository:** `jasonthedataguy/json-the-rabbit-hole-in-my-head` (unchanged).

### Correction provenance

Earlier on 2026-10-30 the draft proposed `jason - the rabbit hole in my head`. A subsequent discussion briefly used `json - the rabbit hole in my head`. On 2026-10-31 the founder explicitly corrected both: **.json — The Rabbit Hole in My Head**. These old variants remain historical proposals and must not be merged into future-facing copy.

## Current draft PR scope

This PR prepares a reversible **book-title/copy-only** change, not an external release:

1. `book.json` has title `.json` and subtitle `The Rabbit Hole in My Head`, preserving the chapter list, approved manuscripts and current public URL.
2. `README.md` displays the complete corrected title.
3. `shared/web/index.html` uses `.json` and the matching title in intended web metadata/visible labels.
4. No previously approved chapter prose, artwork, original audio, native social post, past decision, automation or platform settings are changed by this PR.
5. The PR is **draft**. Do not merge/deploy until founder review and relevant checks; no public publication approval is implied.

## URL scope and later migration

The book repository and deployed Pages route are separate from the **display title**. The earlier shorter slug `jasonthedataguy/json-rabbit-hole-in-my-head` and its corresponding GitHub Pages URL were **proposed**, not verified migrated. The title correction does **not** require that rename.

Preserve current verified links and the `book.json.public_url` value. Only consider repository rename, DNS/Pages changes, link redirects, social profile links, QR codes and published CTAs via a separate explicitly approved, tested cutover. Never assume GitHub Pages URLs redirect automatically.

## Approval and evidence controls

- Do not republish or rewrite historical proof merely because a title changed.
- For any platform, verify native permissions, exact approved caption/media/settings, and publication proof separately.
- Preserve earlier draft text in Git history and preserve prior founder authorizations in Jira and asset registries.
- Group policy: [Shared Governance](https://github.com/jasonthedataguy/json-studio/blob/main/governance/SHARED_GOVERNANCE.md) and [Two-Layer AI Evidence Contract](https://github.com/jasonthedataguy/json-studio/blob/main/governance/AI_EVIDENCE_CONTRACT.md).
