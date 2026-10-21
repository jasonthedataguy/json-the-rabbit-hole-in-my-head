# .json Studio workspace

On the public book repository's `ipad-workspace` branch, start at [IPAD_WORKSPACE.md](IPAD_WORKSPACE.md). The separate [private asset handoff](cloud/README.md) covers browser-workspace setup, asset restoration and portable path mapping. The Windows production files and their exact author approval scopes remain authoritative.

Start at [studio/START_HERE.md](studio/START_HERE.md). This workspace now combines the publishing skill, production control, the existing book/art references, and the Remotion video app. The strategy deck remains unchanged at `json_video_design_strategy_deck.pptx`.

| Area | Current home |
|---|---|
| Studio config, catalog, project pointers, operations | `studio/` |
| Standard workflow and creative decisions | `studio/docs/` |
| Active video application | `studio/apps/video/` |
| Preserved concept boards, private references, starter docs/code | `studio/references/video-starter/` |
| Canonical manuscripts and reader source | Existing `json_under_revision_v2` repository, linked through `studio/studio.json` |
| Existing artwork | `E:\books\.json\outputs\json-digital-book-assets`, referenced without mirroring |
| Approved Cold Rice review run | `outputs/2026-10-21-com-nguoi/`; its run manifest remains the state authority |
| Shared artifact templates and control scripts | `templates/`, `scripts/` |
| Dynamic animation skill | `skills/json-asset-animation/` |

The old `json_video_studio_codex/json_video_studio` starter was relocated inside this studio. All 31 reference-image file hashes were preserved; no source artwork regenerated. Its old number-based folders and sample hooks remain historical reference material. Current projects use stable book slugs.

From this root, run `python scripts/studio.py catalog`, `python scripts/studio.py status`, or `python scripts/studio.py audit`. To prepare the full-script silent review, run `python scripts/studio.py prepare-video com-nguoi --cut master --format vertical`, then use the video app's local scripts. Exact commands and runtime requirements are in `studio/START_HERE.md`.

## Reusable publishing skill

**Purpose:** Orchestrate raw writing → source-approved literary chapter → film/audio → digital-book website → design → social distribution → product monetization → real-data learning, using the existing .json repository and Jira as production systems.

## Package contents
- `SKILL.md` — activation, agent behavior, safeguards and completion rules
- `references/PIPELINE.md` — 12 stages with gates, dependencies and accepted outputs
- `references/PRODUCT_AND_REVENUE.md` — offer ladder, revenue hypotheses, unit economics, KPIs
- `references/OPERATING_SYSTEM.md` — exact .json folder/Jira mapping and solo-founder method
- `templates/` — story brief, editorial review, film script, social pack, offer card, Jira release packet, machine-readable run manifest
- `scripts/validate_run.py` — local manifest-consistency checker (zero dependencies)
- `examples/cold-rice.example.json` — **conservative illustrative snapshot**, not an authoritative current-state report

## How to use
1. Use the discoverable `$json-story-to-business` entry for the publishing workflow and `$json-asset-animation` for independent scene animation. The discovery entry points back to this workspace; do not copy the full app or artwork library into a skill folder.
2. Say `Run .json pipeline on [raw post]`, `Continue .json pipeline for [slug]`, or `Use $json-asset-animation to animate com-nguoi from existing assets`.
3. For existing chapters, read the actual repository `chapter.json`, `source/approved.md`, workflow, product status and Jira issues; never trust old snapshots over live evidence.
4. Start with `templates/run-manifest.json` or the example, save a distinct manifest for the chapter, then update it as proofs arrive. Store in `chapters/<slug>/docs/` only after deciding integration; do not modify canonical files inadvertently.
5. Check with `python scripts/validate_run.py <run-manifest.json>` (run from this skill directory). It verifies logical flags only; the actual reviewer still checks files, live website, source approvals and vendor claims.
6. Do not publish, change public chapter visibility, commit expenses or activate paid SKUs without founder approval.

## One-sentence trigger
`Use json-story-to-business to move the [chapter/story] from its current verified state to the next approved stage, prepare its social and revenue branches, and show blockers, owner and next actions.`

## What remains unimplemented
This package is a documented **agent skill + reusable process**, not a deployed autonomous pipeline. It does not install itself into ChatGPT, schedule posts, connect payment tools, operate editing software or update Jira automatically. Those require invocation, permissions and live app/tool support.
