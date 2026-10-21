# System-of-work integration

## Local studio control

The complete workspace is now indexed by `studio/studio.json`, `studio/catalog/stories.json` and per-project pointers. Read `studio/START_HERE.md` and `studio/docs/WORKSPACE.md` for current locations. The active renderer is `studio/apps/video`; the supplied starter and private boards are preserved in `studio/references/video-starter`. Old numeric video aliases are resolved through `studio/catalog/legacy-video-aliases.json`, never treated as current book slots.

The catalog discovers the actual current book registry. The supplied deck's 32-chapter statement is historical; the observed registry has 36 chapter slots plus Introduction. Only selected projects get working manifests. Cold Rice reuses its existing approved run; Fashion and To Saigon are queued audits without inferred approvals. Jira stays the external planning authority when connected; this workspace makes no claim of live Jira sync.

## Authority
- **Original prose / selected master:** `chapters/<slug>/source/` in GitHub; `chapter.json` references it.
- **Film/artwork/web recipes and exports:** `chapters/<slug>/production.json` and the existing `audio/`, `video/`, `artwork/`, `web/`, `book/`, `social/` directories.
- **Site/product availability:** `book.json`, generated inventory, public deployment evidence, chapter `docs/PRODUCT_STATUS.json`.
- **Production planning, blockers, owner and due dates:** Jira.
- **Cross-stage orchestration:** `run-manifest.json` (skill-local template, optionally versioned in `chapters/<slug>/docs/` after schema/ownership review). It references source rather than duplicating manuscript.

## Existing .json context (verified 2026-10-21, can change)
- Repo: `jasonthedataguy/json-under-revision-v2`.
- Existing docs: `docs/PRODUCTION_WORKFLOW.md`, `docs/PRODUCTION_STATUS.md`.
- Jira epics include JSON-2 editorial & rights, JSON-3 digital reader & funnel, JSON-5 films & distribution, JSON-78 social and community; inspect current boards for product/ops lanes rather than inventing an epic.
- Cold Rice: slug `com-nguoi`, v2 chapter/prologue `00`, original essay `07`. Existing portal/media recipes do not automatically prove final narrated film or retailer-ready print product.
- Specific current release dependencies: JSON-18 editorial approval, JSON-44 script/storyboard, JSON-81 repeatable weekly media kit, JSON-102 pre-traffic reader MVP, JSON-103 visibility/privacy decision, JSON-105 post-read CTA and measurement. Re-check live states every session; do not carry statuses forward from this document.

## Jira design
**Do not create 12 tasks × 36 chapters by default.** For one promoted chapter, use ONE controlling release packet/ticket (or existing week packet) and link work to canonical epic-specific issues. Populate owner, current stage, artifact links, G1/G3/G4 flags, blocker reason, dependency, due date, evidence, QA checklist, product choices, UTM campaign, post-launch results. Create separate Jira issues only for meaningful multi-day, high-risk or multi-workstream deliverables. Use existing task IDs when work is already covered; avoid duplicate tickets.

Recommended task statuses: `To Do`, `In Progress`, `In Review` if configured, `Blocked` via label/comment if configured, `Done` **only with evidence**. One issue status is not enough to indicate multi-lane production readiness: track gates separately in the manifest.

## Single-run sequence
1. Find story source, book metadata and existing Jira work. If a draft has no slug, use a temporary story ID and do not allocate a live book slot without approval.
2. Produce editorial brief and proposed improvements without mutating canonical text.
3. Receive author approval; put the approved text in source and record new hash/version.
4. Generate parallel briefs/tasks: script, reader and art; choose expected CTA; pre-score possible products.
5. Produce visuals and master video from actual personal narration; do not assume generated captions or inherited cut are release-ready.
6. Verify real site + campaign links on phone, explicit public content policy, scope, and CTA; then release authorized social pack.
7. If a paid offer is selected, separately validate commerce G4 and then launch that offer.
8. Collect observed metrics; propose one improvement and either queue next iteration or close cycle.

## Weekly solo-founder rhythm
- Editorial/approval block: one canonical story or the next unresolved source gate.
- Production block: one original 35–60s film + one 12–20s alternative cut + five-card carousel + image/essay caption; optional Sunday reframed recut.
- Distribution block: adapt assets for target channels with separate links/captions; existing plan uses repeated placements, not fictitious separate films.
- Website and commerce block: improve landing/CTA or one selected product experiment; **do not** parallel-launch many SKUs.
- Retrospective: site/UTM checks, actual versus planned, blockers and next story selection.

## Change-impact rule
When G1 text changes, invalidate and review relevant derived script, subtitles, quote cards, summaries, website render and product copy. When design changes, recheck crops, film overlays, print safe area and channel formatting. When website route/CTA changes, retest deep-links and UTMs before placing traffic. When supplier costs change, re-evaluate contribution. Record checks in the manifest.

## Publication and safety controls
- For current fast-track, website first; no social deep-link launch unless actual public URL works and story public visibility is approved.
- Hiding public routes does not make a public GitHub manuscript private. No destructive/delete/visibility changes before explicit founder policy approval.
- Do not transmit unpublished sensitive family or coworker details into public artifacts unless approved.
- Social publishing, purchase commitments, account changes and payments require distinct approval and connected tools.
- Add source version, source citation, illustration provenance, accessibility notes, actual dimensions and upload state to every media pack.

## Recommended prompt macro
"Run `json-story-to-business` for `<slug or raw draft>` in `<mode>`. Inspect repo/Jira evidence first. Use author-only facts and own-voice narration. Show G1/G2/G3/G4 status, produce currently safe assets, select up to three revenue experiments with assumptions, and report top 3 blocking next actions. Do not publish, spend, or modify public visibility without explicit approval."
