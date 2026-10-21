# Dynamic film production

The studio's `studio/docs/VIDEO_OPENING.md` is the shared opening authority. Do not fork another intro convention here. Use the existing Remotion app and pinned runtime at `studio/apps/video`. `prepare-video` currently compiles the flat reading-cut timeline, not this motion manifest: keep their formats and render paths separate until explicitly integrated.

The asset utility needs Python 3.11+ and Pillow; use the existing bundled studio Python where available. The scene component needs the existing Remotion/React/TypeScript app and its installed browser runtime. No external generation provider, API key or new paid service is required for this local layer-animation path.

## Manifest used by the bundled component

Use JSON with:

- `schema_version`: `1.0`; `story_slug`; `classification`: `layer_animation`.
- `source`: exact script `path` and `sha256`; `asset_roots`: existing selected art root and, if needed, one project-derived-assets root.
- `width`, `height`, `fps`, `duration_s`, `background`.
- `opening`: `title` matching the script heading, `portal_asset`, `reveal_asset`, `focus_x/y` between 0 and 1, `title_hold_s`, `entry_end_s`, `story_start_s`. Times satisfy `0 < title_hold_s < entry_end_s < story_start_s < duration_s`. Per-chapter timing is intentional; the original Cơm nguội 10.5-second intro is not fixed for every film.
- `assets`: unique `id`, `path`, `sha256`, `role` (`portal`, `base`, `cutout`, `plane`), optional `provenance` for project extraction. An opaque image may be a base/plane; a declared cutout must have real transparent pixels.
- `layers`: unique `id`, `asset_id` for an image, or `kind: glow|steam` for a procedural environment effect; `x/y/width/height` in canvas pixels; `z`; `pivot_x/y` normalized (defaults 0.5); `color` for effects; `base` values and `tracks`.
- `tracks`: keys `x`, `y`, `rotation`, `scale`, `opacity`, each with increasing keyframes `{t, value}` in **seconds from the story start**, optional `ease: linear|smooth`. The component clamps outside the track. Rotation is degrees. Image bounds must be planned for the animated range, not merely the first pose.
- `audio`: `mode: silent` or `author_recording` with a real recording path/provenance. The reference component is silent-only; implement and verify audio integration before claiming a narrated output.
- `status: internal_review`, `author_quality_approved: false`, `public_release_approved: false`, `paid_release_approved: false` for draft manifests. These fields describe scope; they are not a substitute for run-manifest approval evidence.

`motion_assets.py check` verifies source/title and assets, alpha assumptions, layer references, sane keyframes, visible independent non-text motion after the intro, and the silent reference-component boundary. It does not prove story fidelity, attractive motion, reliable masks, consent or artistic quality. Human/agent visual inspection remains necessary. Record scene-by-scene citations and checks in the shot list.

## Scene component and render procedure

Copy `assets/AssetScene.tsx` and its sibling `assets/LivingSteam.tsx` into separate modules under the existing app's `src/`. Stage the manifest into a private cache with `motion_assets.py stage`. Its `render-props.json` replaces image paths with safe public filenames and records the source manifest hash. Build an explicitly named composition using `AssetScene`, the manifest's dimensions/fps and `round(duration_s*fps)` frames. Keep the selected chapter's current `root.tsx`, `active-preview.json`, timeline and last review intact while testing a new scene.

Use the bundled Noto Serif font in the public cache and `fontSrc` prop if title glyphs require it. The component has independent image transforms, correct transform-origin pivots, keyed procedural light/steam and a common portal/title entry. It provides no facial/character rig, clean-plate extraction, optical-flow generation, audio mixing or automatic speech alignment. Extend the implementation for a selected supported shot rather than claiming these features exist.

Render a short scene study with the standard opening first. Decode the result and compare more than still endpoints: look for body/prop drift, alpha halos, duplicate objects, depth reversals, sliding contact shadows, aliased thin edges, brightness pumping and inter-frame discontinuity. Do not label a collection of still screenshots as a watched real-time playback review. Keep the animation useful without subtitle changes; captions support the narrative rather than supplying all visual motion.

The existing app supports standard vertical/landscape/square/feed dimensions. Validate each chosen crop and title/subtitle safe area independently; do not stretch a vertical scene into landscape. First use a modest review render; export requested masters only after the scene motion works. No frame-rate or duration alone guarantees platform eligibility.

For final handoff, keep one controlling run; register manifest/component revision, script/asset hashes, output stream/frame/duration verification, motion preview, full cut, captions/audio provenance and author decisions. Publication and paid release remain separate gates. Reader/CTA verification precedes traffic as described by the parent publishing workflow.
