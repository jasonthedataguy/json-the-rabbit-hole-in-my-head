# 12-stage execution contract

Studio workflow v2 retains S00–S11 and G0–G5. `studio/docs/WORKFLOW.md` explains daily operation; `studio/docs/VIDEO_SYSTEM.md` applies the supplied deck without replacing the approved manuscript. Project/run state is referenced through `studio/projects/<slug>/project.json`.

The stages are ordered by dependency; branches can run in parallel after the canonical gate. `Gate` means the founder (or an explicitly authorized delegate) approves the specific content and proof. Evidence is not inferred from file presence. `blocked` and `skipped` are valid outcomes, with reason and next condition.

| ID | Stage | Action | Artifact and minimum acceptance evidence | Who signs? |
|---|---|---|---|---|
| S00 | STORY INTAKE | Capture original draft, provenance, chapter slug, intent, audience, themes, factual risks, CTA hypothesis | `source/raw.*`, story brief, original retained | AI logs; founder confirms risky facts |
| S01 | EDITORIAL DIAGNOSIS | Score narrative arc, opening, tension, specificity, authenticity, emotional payoff, book-level placement; note contradictions and sensitive references | Editorial memo with cut/restructure suggestions and factual questions | Founder for changes |
| S02 | CANONICAL MANUSCRIPT | Revise collaboratively, preserve author idiom, prepare publisher-ready text, reconcile title/part/number; archive changes | `source/approved.md`, `source/revisions.log`, hash in `chapter.json` and explicit approval evidence | **Founder gate G1** |
| S03 | NARRATION SCRIPT | Convert approved chapter to 35–60s master, 12–20s cut, optional ~60s hero; indicate source line, hook, VO, duration, beat, visuals, caption and CTA | Timed script, shot list, alt hooks, pronunciation, proof of story alignment | Founder signs factual script |
| S04 | READER PRODUCT | Use full approved text in book registry; build site, deep-link; make optional interactive experience, accessible/fallback design | Git ref, preview/deployed URL, clean mobile reading, checked source bytes, working next-step CTA | Founder + technical QA |
| S05 | VISUAL IDENTITY | Story-specific motif, mood board, portals, cover art, print patterns, carousel system, verified alt text | Reusable design brief, source/provenance, exports spec, crop QA, rights | Founder visual approval |
| S06 | AUDIO / FILM | Capture author VO, retime storyboard to actual recording; assemble images, captions, safe soundtrack/ambience, exports | Actual recording provenance, 9:16 master, alternate cut, captions, QC notes | Founder preview |
| S07 | CAMPAIGN ASSETS | Generate channel-specific captions, 5-card carousel, story-image, essay excerpt, Sunday recut, replies, variants, UTMs | Social pack: platform/version, target, hook, copy, format, CTA, asset status and source references | Editorial/marketing review |
| S08 | PRODUCT STRATEGY | Translate themes into free, premium and physical product ideas, merch mockups, collector packs, licensing opportunities | Offer ladder and scoring matrix; cost/rights/fulfillment hypotheses | Founder picks experiments |
| S09 | COMMERCE READINESS | Define selected SKU, price, payment flow, support/refunds, fulfillment, taxes/fees, sample QA, rights and stock policy | Complete offer card, actual buyer terms and order/delivery test | **Founder gate G4** |
| S10 | RELEASE / DISTRIBUTION | Verify live chapter + CTA before launch, social formats and platform-specific links; publish or schedule only when authorized | Live test, post links, release log, pass/fail GO/NO-GO record | **Founder gate G3** |
| S11 | LEARNING / REUSE | Measure reads, clicks, retention where available, opt-ins, units, revenue, costs, feedback; extract new hooks/products | Results + actual vs planned + next experiment; retrospective and backlog update | Founder chooses iteration |

## Dependency design
```
S00 -> S01 -> S02[G1]
                  |----> S03 -> S06 --------> S07 ----|
                  |----> S04 --------------------------|--> S10[G3] --> S11
                  |----> S05 -> S06 / S04 / S07 -------|
                  |----> S08 -> S09[G4] -----optional commerce release
```
Reader experience and source approval are **prerequisites to traffic**; final paid checkout is **not required** for free-story acquisition. Monetization ideation (S08) may start at intake but no public offer before editorial rights and readiness. Move branches independently but do not falsely advance gate states.

## Editorial scoring rubric (0–5 each)
- Unique premise / specific lived detail
- Emotional arc and payoff
- First-300-word hook / readability
- Voice originality and restraint
- Fit within the larger .json narrative arc
- Source integrity, accuracy and privacy (a separate risk gate; high artistic score cannot override a privacy blocker)

**Output**: scorecard + rationale + what to retain + risky assumptions + author-choice options. Do not equate subjective score with quality proof.

## Source and derivative rules
- `chapters/<slug>/source/approved.md` is canonical only after signoff; preserve raw drafts and revisions, including intentional contradictions in remembered events.
- `chapter.json` stores title, slug, slot, publish flag, canonical selection and hash. Do not change numbering casually; keep original edition metadata.
- Track every derivative in the run manifest with `source_sha256`, `version`, `format`, `rights`, `status`, `evidence`.
- A script can be an **adaptation** rather than a verbatim reading; label it clearly, never present an invented first-person fact as memoir.
- Supplied art must not be claimed newly generated; generative images must be labeled as illustrations when relevant, not archival evidence.
- Any change after S02 G1 should determine affected derivatives and invalidate their clearance/QA if necessary. Rebuild and retest impacted assets.

## Video script record
Each segment needs: `segment_id`, `start_estimate_s`, `duration_estimate_s`, `vo_text`, `source_excerpt_or_adaptation`, `source_reference`, `visual`, `on_screen_text`, `subtitle_notes`, `emotion`, `rights_notes`. Durations are **estimates until the author records VO**; silent cuts use labeled reading timings. Promotional defaults are 35–60s plus a 12–20s alternative, while an explicit full-script request determines its own duration. One original film distributed on multiple platforms remains **one** creative output.

Every video includes [the shared opening](../studio/docs/VIDEO_OPENING.md): exact chapter title with its portal → enter center → reveal center artwork → story, with a tested motion preview and continuous landing. Recuts retain a compact opening unless the author explicitly chooses an exception. For dynamic scene work, route to [json-asset-animation](../skills/json-asset-animation/SKILL.md); independent asset/environment movement is required, rather than text over flattened art.

## Digital reader QA
Source bytes or approved text complete; Vietnamese characters and typography correct; screen-reader/keyboard and reduced-motion basics; mobile/small-screen text readability; reliable navigation; no broken images; accurate available/unavailable chapter claims; old routes checked; actually deployed public URL checked, not just build success. `python scripts/build_inventory.py && python scripts/build_site.py && python scripts/check_site.py && python -m unittest discover -s tests -v` are repository-prescribed local commands; generated `dist/` remains unedited/uncommitted.

## Release gates
- **G0 Intake integrity:** original captured and provenance established.
- **G1 Canonical content:** record explicit approval of exact manuscript text/version/hash. Record the approval's scope precisely: text selection does not by itself approve script, public disclosure, family representation or commercial use. Keep unresolved factual/privacy decisions visible for the relevant next gate.
- **G2 Product quality:** script/design/media/site tests evidenced for selected release surfaces.
- **G3 Public go/no-go:** authorized chapter visibility, rights, actual live URL/CTA, accessibility basics, campaign links, and approved story/post assets.
- **G4 Paid offer readiness:** only applicable to a paid offer; physical prototype quality, realistic fulfillment, terms/price/cost, payment path and rights.
- **G5 Post-release evidence:** live-post links and observed metrics, with observation dates and gaps.

**Fast-track permitted:** free reader + one narrative film + one recut + one carousel + minimum CTA, then iterate; product/merch research is optional parallel work. Do not insist on a full collector box before posting an approved reader link. Conversely, do not allow social traffic to a known broken or unapproved reader.

## Scoped release checks

`release_scope.surfaces` selects `reader`, `film`, `social`, `audio`, `digital_product` and/or `physical_product`. Reader-only release does not need film/audio production. The legacy default is reader + film + social. `scripts/validate_run.py` checks logical flag consistency; `scripts/studio.py check-release <slug>` also checks source/derivative integrity and exact approval evidence. Neither command publishes or authenticates the author's identity; a human must verify the recorded evidence and actual product QA. A content hash identifies bytes, not consent.

The deck's 45-second arc is a planning option, not a reason to truncate an approved story or rush real narration. Cold Rice's current v3 is the complete supplied video script in a 120-second silent review with the portal-center introduction. Its earlier 54s/18s excerpt plans remain historical. The book selection and video-text selection have separate evidence; public-scope and final artistic approval remain pending.
