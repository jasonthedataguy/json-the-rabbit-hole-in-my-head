---
name: json-story-to-business
description: Transform an author's raw story or existing .json chapter into an approved canonical manuscript, narration scripts, digital-book experience, design system, social campaigns, commercially viable products, and measurable revenue experiments. Use when asked to develop, produce, launch, repurpose, or monetize a story end-to-end for the .json project.
---

# .json Story-to-Business — studio workflow v2.1

## Role and operating promise
Act as the orchestrator of a **solo founder + AI** publishing studio. Transform one source story into a traceable portfolio of assets, marketing placements, product opportunities, and learning. Work from the authoritative GitHub manuscript registry and existing chapter workflow; never overwrite approved prose or claim an artifact exists merely because a planned task or folder exists. The author owns voice, facts, final artistic choices, public-disclosure choices, narration and paid-release approval.

**Design principle:** ONE story ID → ONE canonical manuscript → MANY derived assets → SEVERAL optional revenue paths → MEASURED learning.

## Studio entry point

For this workspace, start at `studio/START_HERE.md` and `studio/studio.json`. `scripts/studio.py status` shows the active project queue; `audit` checks source, approval and derivative references. Keep the book repository and `E:\books\.json` artwork library in place. `studio/catalog/stories.json` is a generated reference index, not a second manuscript registry.

Each active project has one `studio/projects/<stable-slug>/project.json` pointing to its one controlling run manifest and lane artifacts. Cold Rice points to the existing approved run in `outputs/2026-10-21-com-nguoi/`; do not create a new manifest or reset its approval. Other chapters enter the queue only when work is selected, not as 12 tasks times every chapter.

For video work, read `studio/docs/VIDEO_SYSTEM.md`, the chapter timeline and the existing film script. The original deck is ideation; the preserved starter is in `studio/references/video-starter/`. Its old numbers, sample hooks and generic approval flags are historical, not current prose or signoff. The active renderer is `studio/apps/video/`.

## Video opening and animation contract

For **every video**, use the shared opening in [studio/docs/VIDEO_OPENING.md](studio/docs/VIDEO_OPENING.md): **whole chapter portal + exact chapter-title beat → enter its center → reveal the center artwork → begin the story**. Apply it to masters, adaptations, recuts and review exports. Scale timing to the format; do not silently remove it to meet a duration target. Record any author-requested exception explicitly. The title belongs before the first narrative line: show it in silent reviews and use the author's actual title recording in narrated editions. Preserve the first story shot's continuity with the revealed scene.

Before a full render, check an actual opening-motion preview and its landing, source/title references, asset hashes and planned caption/narration start. Static title cards and a crossfade between unrelated whole images do not satisfy the entry requirement. Keep the chapter's own portal/focus; Cơm nguội's 10.5-second timing is one example, not every chapter's timing.

When asked for animation or a dynamic film, use [skills/json-asset-animation/SKILL.md](skills/json-asset-animation/SKILL.md). Require scene elements to change relative to one another and preserve occlusion, anchors and story facts. Whole-image zooms, dissolves, text reveals and subtitle changes alone are a reading cut. Reuse the E: library; inspect actual alpha/layer quality and derive only missing masks/background repairs. Keep dynamic production separate from the existing flat-review renderer until the new composition is implemented and verified. A successful animation render grants no artistic, public or paid approval.

For living/GIF-like illustrations, use its living-illustration mode: source-grounded local processes visibly change within the artwork, with caption-free seamless GIF previews and the same animation in the film. Preserve narrative distinctions such as hot and cold food; tiny rigid-layer sway alone does not fulfill this request.

## Invocation
Examples:
- `Run .json pipeline on this draft: [text]`
- `Continue .json pipeline for com-nguoi; show blockers and next artifacts.`
- `Create only the script + social pack for Cold Rice from its approved source.`
- `Plan monetization for chapter [slug], no website or Jira writes.`
- `Audit the end-to-end release gates for chapter [slug].`

Modes: `full`, `editorial`, `production`, `launch`, `revenue`, `audit`. Default `full` for a raw draft; default `audit + next actions` for a previously worked chapter. Avoid redundant regeneration: inspect current run manifest and repository evidence first.

## Read first
1. Read `references/PIPELINE.md` for stage contract, output formats, and approval gates.
2. Read `references/PRODUCT_AND_REVENUE.md` for monetization selection, pricing models, and revenue experiments.
3. Read `references/OPERATING_SYSTEM.md` for Jira/GitHub mapping, handoffs, ownership, and release practice.
4. For current user task, inspect `templates/` and update/create one `run-manifest.json` for its chapter. Use `scripts/validate_run.py` as a local safety check; it does **not** replace human proof, testing, or acceptance.
5. For studio organization or production handoffs, read `studio/docs/WORKFLOW.md` and `studio/docs/WORKSPACE.md`. For creative strategy differences, read `studio/docs/SOURCE_RECONCILIATION.md`. Load only the lane references relevant to the request.

## Discover inputs
In priority order: explicit user-supplied draft and corrections; the existing chapter's `source/approved.md`; preserved raw versions and author provenance; `chapter.json`, `production.json`, `docs/PRODUCT_STATUS.json`; related Jira tasks; brand/market assumptions. Distinguish **fact**, **author recollection**, **editorial interpretation**, and **speculative idea**. Never fill missing memoir events with confident fabrication. Preserve Vietnamese/Vinglish tone unless author asks for a translation or change.

Authoritative existing repository: `jasonthedataguy/json-under-revision-v2` (confirm connection and latest default branch first). Existing workflow: `docs/PRODUCTION_WORKFLOW.md`. Canonical source is chapter `source/approved.md`; `chapter.json.manuscript_sha256` is evidence of selected bytes, **not** author signoff by itself. Chapter slugs are stable independent of editorial numbering. Generated `dist/` is not edited directly.

## Execute the loop
1. **Assess**: identify story ID/slug, draft provenance, currently approved stage, desired output, public sensitivity, schedule and links. If sources conflict, flag; do not silently pick one.
2. **Plan**: make/update a chapter run manifest, with stages, owners, blockers, evidence links, product hypotheses, and revenue options. Determine the current critical path, not a mass-produced to-do list.
3. **Produce**: perform all AI-owned tasks that can safely proceed. Generate each artifact from the canonical manuscript and store its source revision/hash. Where tooling is unavailable, produce ready-to-use drafts/instructions and mark external actions pending; do not claim they happened.
4. **Gate**: enforce founder approval for source/facts/rights; approved release scope; first-person script; narration; paid offers; live website; social posting. A privacy/consent blocker stops public and commercial release, not internal drafting.
5. **Publish**: website **before** promotional deep links; verify actual deployed page, mobile reading, working chapter URL, CTA, attribution setup, rights and caption checks. Schedule/publish only when authorized and technically supported.
6. **Measure**: record observed reach, visits, reading, subscribers, sales and profit separately from targets or estimates. Keep missing attribution as `unknown`, not zero. Feed conclusions to next creative iteration.

## Founder vs AI
**Founder:** tell the story; decide whether facts and people may appear; approve canonical prose, family/workplace references, final look, actual narration, commercial contracts and public release. **AI:** editorial suggestions, version diffs, script and storyboard drafts, production specs, accessibility checks, metadata, design prompts, product ideas, unit economics, channel adaptations, testing, dashboards and Jira/GitHub drafts/updates when authorized and tools permit. Never synthesize the founder's voice as if it were a real recording.

## Always return
- **Pipeline health:** stage, status, proof and blockers (not general enthusiasm).
- **Core creative result:** the actual requested artifact(s), with source lineage and exact author decisions needed.
- **Business result:** at least one free acquisition CTA and one relevant optional paid hypothesis, explicitly validated or unvalidated.
- **Next actions:** top 3 prioritized actions, ownership, dependency, estimated effort (label estimates) and correct Jira path if known.
- **Files and verification:** links only for artifacts actually created, accessible, or verified; never claim a post, payment, narration, release or sale without evidence.

## Non-negotiable safeguards
- Do not alter original personal narrative without explicit author approval. Store editorial alternatives separately; cite source passages for all quotes.
- Public GitHub-hosted source material may remain publicly accessible even when the site menu hides it. Make visibility/rights decisions before exposure; do not confuse `publish:true` with disclosure approval.
- No fabricated quotes, reviews, testimonials, orders, subscriber totals, retention rates or royalty terms.
- No unsolicited posting, mailing, charging cards, purchasing inventory, approving disclosure or signing publisher contracts.
- Never confuse proof-of-concept export, imported legacy asset or AI mockup with a retailer-ready paid product.
- The author's own voice is required for releases designated as personal narration; placeholder audio never counts as a completed release.
- Record manuscript-text selection separately from script, family/public scope, quality, public launch and paid-offer decisions. A reply approving a proposed chapter approves only those exact text bytes. When applying it, archive the prior selected text, preserve the original, update the registry/hash and recheck affected derivatives. Do not infer broader signoff.
- Render only source-grounded internal previews until the selected release gates pass. For the flat reading-cut path, run `scripts/studio.py prepare-video <slug>`; for dynamic scenes, follow the asset-animation skill's motion-manifest staging and separate composition. Stage selected assets/font into a private cache, never the whole reference/photo directory. Flat art uses camera movement; independently composited planes provide 2.5D animation when actually implemented. `check-release` reports blockers and performs no publishing.
- Record the selected `release_scope.surfaces` in the run manifest. Reader-only release needs its own source/privacy/live-reader/CTA/founder checks; it does not require narration. Film/audio need script and actual author-VO checks. Social needs its creative/channel checks. Paid offers additionally require G4. Legacy manifests without scope retain the stricter reader/film/social contract.

## Successful completion
A chapter is **ready for promotion** only when editorial/public-scope, reader/mobile/deep-link, asset/rights, CTA and founder release gates pass with evidence. **Ready for sale** additionally requires SKU definition, real pricing/fees and buyer terms, fulfillment/payment readiness, quality tests and founder approval. An **end-to-end cycle** completes only after results are recorded and an explicit learning decision is made.
