# .json Video app

This is the active internal-review renderer within the [full studio](../../START_HERE.md). Read that entry point for current commands. The original starter's boards/photos/docs/manifests and code snapshot moved intact to `../../references/video-starter`; they are historical references, not current approval state.

The Cơm nguội v5 film is 120 seconds: title/portal-center entry and scene reveal, then 27 source-checked story-reading cues. Curling vapor rises and fades from the hot serving bowl/pot; foliage, lamps and lighting animate independently. Two caption-free GIFs use the same scene engine. It is a silent 2.5D/procedural review; author look/pacing and release approval remain pending.

Use the [v5 production guide](../../projects/com-nguoi/animation/v5/PRODUCTION.md) to build/stage inputs, then run `npm run typecheck` and `npm run render:v5`, `npm run studio:v5` or `npm run still:v5` in this app. Add `-- --loop=dinner` or `-- --loop=child` to render the artwork loops. The dedicated runner supplies the animation entry, composition, props and private asset directory. Preserve existing reviewed exports when making a new creative version. V4 commands remain available for its preserved version.

For flat reading cuts, `python scripts/studio.py prepare-video <chapter> --cut master --format vertical` selects the exact source, timeline and format before the generic `studio`, `still` or `render` scripts. That path intentionally rejects layer-animation timelines. Pinned dependencies and the existing lockfile remain authoritative.

Source-grounded timeline preparation is required before rendering. The app never reads the preserved starter sample hooks or private reference-photo folders. Original starter instructions are archived in the reference area and are not the current runbook.
