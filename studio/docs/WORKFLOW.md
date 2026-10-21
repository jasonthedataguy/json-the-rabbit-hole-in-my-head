# Standard studio workflow v2.1

The stage contract remains [S00–S11 in PIPELINE.md](../../references/PIPELINE.md). This document makes it usable across the full studio, with a single chapter identity and scoped evidence.

## Intake and selection

Resolve the stable book slug through the current registry/catalog. Keep v2 number, original edition number and legacy video ID separate. Inspect existing prose, art, media, current run and author decisions before creating work. Select one controlling run manifest; `project.json` points to it. Do not create another run just because a department starts work.

For a registered chapter without an active project, refresh the catalog, then run `python scripts/studio.py new-project <stable-slug>`. It creates pointers and unapproved intake state, not prose, artwork or a live chapter slot. A new raw story uses editorial intake first and does not silently allocate a book number.

## Editorial and approvals

Preserve original words, Vietnamese/Vinglish, remembered uncertainty and provenance. Keep proposed edits separate and give an exact comparison. Text approval identifies exact bytes/hash. Apply only that decision: preserve the prior selection, update source/registry/history and review affected derivatives. Public family scope and script remain independent decisions. Cold Rice v1 is already approved and selected; do not ask for the same text approval again or erase it with the starter's old `approved:false`.

## Production branches

After selecting the source, prepare script/reader/design/social planning from it. Internal provisional work may proceed with clearly pending gates. Film uses a cited script and project timeline. Every video follows [the shared opening](VIDEO_OPENING.md), including recuts: exact title with the portal, entry into its center, center-art reveal, then the story. Preserve explicit author exceptions. Render and inspect the opening motion and first-line handoff before exporting the full film.

Cold Rice's active v3 uses the complete supplied video script in a 120-second silent review with a 10.5-second introduction; earlier versions remain in history. A silent review does not require a recording. Record real author VO before a future narrated version and retime its speech captions. When animation is requested, use [json-asset-animation](../../skills/json-asset-animation/SKILL.md) to inspect reusable layers, design independent object/environment motion, verify a representative moving scene, then build the film. Do not deliver another whole-image reading cut as the requested dynamic animation.

Reader work uses the complete selected text, existing book source UI/routes, responsive art, accessible controls and correct onward CTA. Reuse installed assets after checking current mappings. Existing boards, print PDFs, edit previews and legacy social files retain honest proof/edition labels.

Social is one core film plus alternate/carousel/image/essay placements, not one fictitious new film per channel. Use verified destination/CTA behavior per channel. Website and reader checks precede promotional traffic.

Commerce stays a separate optional branch: at most three relevant hypotheses, one initial experiment, real demand/cost/rights/fulfillment evidence, and separate G4. The free acquisition CTA can be **Đọc trọn chương**, followed by a truthful next chapter. Paid candidates remain unvalidated until tested.

## Shared gate language

| Decision | Evidence and scope |
|---|---|
| G0 intake | Identified source, provenance, stable identity and sensitive questions |
| G1 text | Exact manuscript version/hash and direct author approval; preserve separate fact/disclosure questions |
| Script | Exact first-person wording, source references and shortened adaptations |
| G2 quality | Chosen art, actual media/narration/captions, reader and selected-surface QA |
| G3 public release | Named surfaces, exact artifact hashes/versions, actual live reader/CTA, rights/public scope and author GO |
| G4 paid release | Selected offer/price/terms/cost/rights, checkout/delivery/sample tests and author commercial GO |
| G5 learning | Actual dated post/product links, observed outcomes and next decision |

`release_scope.surfaces` selects the needed lanes. Reader-only launch does not wait for narration. An image-only social release needs its own creative/public/reader checks, without falsely declaring a narrated film complete. Film/audio require script and actual author VO. Paid surfaces require G4 as well. Legacy runs without scope keep the stricter reader/film/social behavior.

## Verification and handoff

Run studio audit before render prep and before release review. Audit checks local source/hash/citation consistency. `prepare-video` produces only explicit, watermarked silent reviews. `check-release` returns blockers, requires exact public-release evidence and has no publishing side effect. These checks help coordination; they cannot authenticate human consent or substitute for watching/reading the actual release.

Use one existing Jira controlling/week packet when connected, linked to real editorial/reader/media/community issues. Update current owners/blockers/evidence; never assume historical issue IDs are current. No live Jira connection, publisher, scheduler, payment integration or automation was installed by this standardization.

After release, distinguish targets from observed reach, clicks, measured reading, onward visits, opt-ins and sales/contribution. Missing attribution stays `unknown`/null. Review what the result changes about the next creative or commercial experiment.
