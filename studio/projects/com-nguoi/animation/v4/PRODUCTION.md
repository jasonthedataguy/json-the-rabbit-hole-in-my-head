# Cơm nguội v4 · animated silent review

V4 preserves the complete author-supplied script and 120-second reading timeline. The chapter-title/portal-center introduction lasts 10.5 seconds, followed by the story. No voice, music or ambience is used.

## What moves

Two existing illustrations are split into aligned environmental layers: a hanging lamp pivots at its ceiling attachment; foreground foliage and the plant crown move around separate roots; local warm lighting varies independently. The family figures retain their source poses. This is restrained 2.5D environmental animation, not facial/body animation or recovered archival footage. Existing hot-rice steam remains illustration context; no animated steam is added to the narrator's cold bowl.

The source-derived clean plates use nearest existing surface colors only behind the extracted environmental masks. They are local animation repairs, not newly discovered source details. The unmodified E: images remain authoritative; masks, crop bounds, pivots and source hashes are in `motion-manifest.json` and `derivation-receipt.json`.

The earlier low-resolution cutouts with background residue are not used. There are no floating demonstration cards. The portal reveals the sharp family illustration and lands in the same composition as the first story frame. All 27 story-reading cues are retained. Their timing matches the existing v3 SRT/VTT; those files remain the timing reference.

## Reproduce

From the studio root, use the existing Anaconda Python for SciPy-based layer derivation:

```powershell
& 'E:\anaconda\python.exe' -X utf8 studio/projects/com-nguoi/video/build_v4.py
npm.cmd run typecheck --prefix studio/apps/video
```

The builder stages selected assets/font into `studio/.cache/render/com-nguoi/v4-layer-animation` and writes the separate app props. It does not select v4 in the project or change book approval. To render, run the pinned Remotion CLI in `studio/apps/video` with entry `src/com-nguoi-v4-entry.tsx`, composition `ComNguoiV4`, the cache `public` directory and `manifests/com-nguoi-v4.json` props. Use H.264 and `--muted`; the standard master is 1080×1920, 30fps, 3600 frames.

The app now wraps those exact arguments: `npm.cmd run render:v4 --prefix studio/apps/video`. Add `-- --study` for the opening/motion preview. `studio:v4` opens the selected animation composition and `still:v4 -- --frame=390` exports a review still. These commands are separate from the older flat reading-cut commands.

The existing `prepare-video` command is the flat reading-cut path and intentionally refuses a selected layer-animation timeline. It must not flatten v4.

## Checks and decisions

`video/verify_v4_motion.py` renders matched moving/static controls of the dinner and child scenes. Text and camera remain identical; separate lamp/foliage changes are measured. `video/verify_silent_cut.py --v4` decodes and counts the full movie, checks streams/duration and captures every reading cue and the opening phases. Technical checks do not approve the final look, family/public scope, public distribution or paid use. Review those exact decisions through the existing controlling run; do not create another run manifest.

The opening/motion study, controls and final QA are under `video/review/v4-layer-animation/`. Earlier film versions remain available. A revision after review should receive a new version rather than overwrite this export and its evidence.
