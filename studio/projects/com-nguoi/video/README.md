# Cơm nguội · living-illustration silent review v5

V5 reads the complete final video script supplied by the author on 21 October 2026. It preserves all 238 whitespace-separated words/syllables in 27 story-reading cues, without editing the external book manuscript. It retains the title, portal-center entry and scene reveal before the story, then brings the illustrations to life with curling vapor, moving leaves and warm light.

- Format: 1080 × 1920, 30 fps, H.264, 120 seconds. Introduction: 0–10.5 seconds; first source paragraph starts at 10.5 seconds.
- Sound: intentionally none; no narration, music, ambience or audio track.
- Visuals: existing portal, family-table and story-detail illustrations from `E:\books\.json\outputs\json-digital-book-assets\chapters\com-nguoi\artwork`. Steam changes shape and rises from the hot serving bowl/pot, while lamps, foliage and light animate independently. The child's cold bowl and family poses stay still. Original art stays unchanged.
- Text: existing licensed Noto Serif. Reading timings are not speech-aligned subtitles.
- State: internal review only. Author approval of the rendered look and pacing is pending. Public family/visual disclosure, public distribution and paid release remain separate gates.

## Files

- Active source: [final-script-v2.md](../script/final-script-v2.md).
- Text selection evidence: [final-script-v2-approval.json](../script/final-script-v2-approval.json).
- Active storyboard: [timeline.json](timeline.json).
- Reading timing files: [SRT](com-nguoi-v3-reading-timings.srt), [VTT](com-nguoi-v3-reading-timings.vtt), including the opening title beat.
- Earlier excerpt plans: [history/timeline-excerpts-v1.json](history/timeline-excerpts-v1.json). These are not the active full-story cut.
- Technical and visual checks: `review/v5-living-illustrations/verification.json`; matched vapor/no-vapor and exact-loop controls: `review/v5-living-illustrations/motion-controls/verification.json`.
- Opening/motion study: `previews/com-nguoi-v5-opening-and-living-scene-study.mp4` (18 seconds, half resolution). The complete story is the export below.
- Review delivery: [Cơm nguội v5](exports/com-nguoi-v5-living-illustrations-silent-review-1080x1920.mp4), with a hash-bound receipt alongside it. Earlier reviews and versioned timelines remain available.
- Living illustration GIFs: [dinner](../animation/v5/exports/com-nguoi-v5-dinner-living.gif), [childhood](../animation/v5/exports/com-nguoi-v5-child-living.gif). Each is an 8-second caption-free loop, not the full chapter.
- Animation assets, provenance and commands: [v5 production guide](../animation/v5/PRODUCTION.md).

## Reproduce

From the workspace root:

```powershell
.\studio.ps1 audit
& 'E:\anaconda\python.exe' -X utf8 studio/projects/com-nguoi/video/build_v5.py
npm.cmd run typecheck --prefix studio/apps/video
npm.cmd run render:v5 --prefix studio/apps/video
```

The builder derives and stages only the selected assets; it does not change approval state. `prepare-video` is the older flat-render path and intentionally refuses the selected animation timeline. Run `video/verify_v5_motion.py` and `video/verify_silent_cut.py --v5` after rendering as described in the production guide. Technical success remains separate from author approval. Make requested creative changes as a new version; preserve this reviewed export and its evidence.

## Next production decisions

1. Author: watch the full silent cut and select pacing/look changes, approximately 5–10 minutes. Dependency: rendered review file. No Jira update performed.
2. Editor/AI: apply the requested changes and render the next version, approximately 30–90 minutes depending on changes. A later narrated version additionally requires the author's own recording and retiming; the requested silent cut is complete without it.
3. Author + technical owner: select public disclosure/distribution scope and verify the reader/CTA before an exact release approval, approximately 1–2 hours excluding fixes. Existing public and paid gates stay pending.

The planned free acquisition CTA is “Đọc trọn chương”, only after its reader destination is verified and approved. An illustrated digital mini-edition remains an optional, unvalidated paid hypothesis in the existing monetization plan; no offer or payment flow is released by this video task.
