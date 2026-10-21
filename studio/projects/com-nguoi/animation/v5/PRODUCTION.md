# Cơm nguội v5 · living illustrations

V5 keeps the exact supplied final video script, all 27 reading cues, the 10.5-second portal/title opening and the 120-second silent review format. It replaces the frozen dinner steam with continuously deforming vapor and adds vapor to the hot cooking pot in the childhood illustration. The child's cold bowl stays still. Faces, family poses and narrative facts are preserved.

The two caption-free illustration GIFs loop every 8 seconds at 960×640, 12.5 fps. Both have 100 frames, infinite-loop metadata and one fixed palette. The complete 1080×1920 film renders the same scene engine directly at 30 fps, retaining smoother motion and full color.

## Existing art and local changes

All original images remain in the E: chapter library. V4's extracted lamps/foliage are referenced in place. The only new art derivative is the dinner clean plate with the frozen paper plume removed. Its connected cream-color mask and source-sampled surface repair are recorded in `derivation-receipt.json`. This is an illustrative local repair, not archival reconstruction. The procedural steam component belongs to the reusable animation skill.

Source-pixel emitters: dinner serving bowl (1017,846); childhood hot pot (1590,697). Steam width/height and source regions are recorded in the motion manifest. All scene tracks share an 8-second period; wisps deform, rise and thin independently of the leaves and lamp. This is 2.5D environmental and procedural animation, without character articulation.

## Reproduce

From the workspace root:

```powershell
& 'E:\anaconda\python.exe' -X utf8 studio/projects/com-nguoi/video/build_v5.py
npm.cmd run typecheck --prefix studio/apps/video
npm.cmd run render:v5 --prefix studio/apps/video -- --loop=dinner
npm.cmd run render:v5 --prefix studio/apps/video -- --loop=child
npm.cmd run render:v5 --prefix studio/apps/video -- --study
npm.cmd run render:v5 --prefix studio/apps/video
```

The builder stages selected art/font only, preserves cache hardlinks using atomic derivative replacement and does not select the project version or grant approval. The runner supplies the separate v5 entry, composition, props and private public directory. Generic `prepare-video` remains the flat-render path.

Encode each rendered scene MP4 using `skills/json-asset-animation/scripts/export_loop_gif.py`, with the corresponding `--output` GIF, existing compositor `--ffmpeg`, and a separate `--report`. The script checks actual decoded frames, palette, duration and the encoded loop join. The complete chapter is the video export, not either 8-second GIF.

Run `video/verify_v5_motion.py` for matched vapor/no-vapor controls, protected cold-bowl/text regions and exact zero/eight-second poses. Run `video/verify_silent_cut.py --v5` for complete movie decoding, all source cues and opening captures. Inspect the scene loops, local clean plate, portal landing and complete cue contact sheets.

## Review

Final outputs are `video/exports/com-nguoi-v5-living-illustrations-silent-review-1080x1920.mp4` and the two GIFs in this folder's `exports/`. QA is in `video/review/v5-living-illustrations/`. Earlier versions remain available. All are internal review artifacts; author artistic, family/public disclosure, public distribution and paid-use approvals remain separate decisions in the existing controlling run.
