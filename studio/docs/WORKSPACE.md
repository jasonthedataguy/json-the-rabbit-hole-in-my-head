# Workspace map and department homes

`studio/studio.json` configures all roots. Change paths there if drives change; rebuild the generated catalog and audit references. Do not migrate source manuscripts or mirror the large artwork library to make the paths look uniform.

```text
workspace/
  SKILL.md, AGENTS.md              studio instructions
  references/                    shared stage, revenue and operating contracts
  templates/                     reusable artifact/approval/measurement templates
  scripts/                       studio control and run validation
  json_video_design_strategy_deck.pptx   unchanged ideation
  outputs/2026-10-21-com-nguoi/    existing approved review run and its state
  studio/
    studio.json                  storage/authority configuration
    START_HERE.md                working entry point
    catalog/                     generated 37-story references and old aliases
    projects/<stable-slug>/       project pointers and actual new work only
      project.json               source, run state and department links
      run-manifest.json          only when no existing run already controls it
      video/timeline.json        source-grounded motion plan when produced
      video/previews/            private generated review exports, ignored
    apps/video/                  active Remotion application
    operations/                  selected queue, ownership and WIP policy
    docs/                        standard operation, creative decisions, roadmap
    references/video-starter/    preserved starter boards, private images, docs
    references/strategy-deck-extract.json  slide text and source hash
    reports/                     generated integrity/release/test evidence
    .cache/render/               selected transient render inputs, ignored
```

## Department ownership and authoritative artifacts

| Lane | Working authority | Founder decision |
|---|---|---|
| Editorial | Existing book `chapters/<slug>/source/`, registry hash; separate proposed edits and approval records | Exact prose and factual corrections |
| Digital reader | Book `shared/web/`, chapter `web/`, actual deployed evidence | Look, reading quality and public scope |
| Design | E: library chapter `assets.json`, native art and reusable components; selected crop/adaptation records | Chosen visual treatment, people/rights |
| Audio | Chapter audio handoff and actual author take with provenance | Own narration and selected take |
| Film | Project timeline, linked script, internal app previews, eventual actual export evidence | Script, visual/media preview and final release |
| Social/community | Linked social pack, channel copy, concrete adapted exports, actual upload URLs | Exact posts/surfaces and replies if authorized |
| Commerce | Selected experiment/offer card, actual prices/costs/terms/payment/delivery proof | One experiment/budget, then G4 |
| Release | One controlling run manifest, scoped approval record and actual reader/asset tests | G3 for named surfaces and versions |
| Learning | Dated observed metrics and next experiment decision; unknowns stay null | Continue, revise, scale or retire |

`project.json` links these lanes; it does not duplicate stage or gate flags. The generated catalog summarizes available sources without inferring author approval. A project receives real working files only as they are made; an empty folder is not a completed product.

## Storage and privacy

Canonical manuscript/reader repository: the existing `json_under_revision_v2` checkout configured in `studio.json`. Reusable art: `E:\books\.json\outputs\json-digital-book-assets`. Completed external book artifacts already in `E:\books\.json\outputs` stay there. This task writes only the studio workspace; a future final-export transfer requires actual filesystem access and the appropriate release decision.

Legacy reference images were moved, not regenerated: 31 image hashes are recorded in `references/migration-receipt.json`. Original starter code/docs/manifests are retained in a small code-only ZIP. The old `json_video_studio_codex` folder contains a redirect README. Never treat starter sample hooks as author text.

Render prep stages only selected explicit art and the existing Vietnamese font into an ignored private cache. It tries same-volume hardlinks before copying, records the method and verifies hashes. Never alter a staged input: a hardlink points to the existing source bytes. This staging is a render dependency, not a new asset master or another library. Private photos/boards are not automatically staged.

Heavy preview media, cache, dependencies and personal reference images are excluded from new Git tracking. This does not make a public Git repository private; public/disclosure decisions still need explicit author review.
