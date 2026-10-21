# Living illustrations and GIF loops

Use this mode when the author wants the illustration itself to feel alive. A moving camera or a small rotation of an unchanged picture does not establish that result. Choose a visible process in the existing scene: vapor curls, rises and thins; water ripples; flame changes shape; light moves across a surface. These are examples, not additions to every story.

Ground each effect in the selected artwork and text. Record the emitting object, source-pixel anchor, affected region, occlusion and intentionally still areas. In Cơm nguội, the existing dinner serving bowl has a painted plume; the childhood scene has a hot cooking pot. The child's cold bowl gets no steam. Preserve the family poses and facial expressions.

Remove or isolate baked effects before animating them. Otherwise the frozen plume remains beneath the moving one. Save only the necessary local clean plate or alpha extraction, with its original path/hash, mask and repair operation. Inspect repairs in the phase of lowest effect opacity; steam must not conceal a bad repair.

The reusable [LivingSteam.tsx](../assets/LivingSteam.tsx) builds continuously deforming, tapered vapor ribbons. It is deterministic and periodic in scene time. Place it in the same source coordinate space as the emitting object and the scene camera so its base remains attached. Its shape changes internally; moving an unchanged smoke sticker is insufficient. Choose color, width, opacity and height to match the artwork and the final display scale.

For a loop, give every track and effect a shared period or integer divisor of that period. Keep the camera and captions out of the illustration GIF. Compare the exact zero/end pose and the last encoded frame → first encoded frame; omit a duplicated endpoint frame to avoid a pause. Use a fixed GIF palette to reduce flicker, and verify duration, loop metadata and decoded frame changes. The film can render the same scene directly at its higher frame rate rather than embedding a palette-limited GIF.

Deliver a caption-free GIF for each requested illustration and the complete film when requested. A GIF preview is not a complete chapter video and does not need the film's portal intro. A complete film retains the shared opening. Keep motion readable at the real delivery size; render an actual local preview before the full export.

Use `scripts/export_loop_gif.py <local-loop.mp4> --output <scene.gif> --ffmpeg <existing-ffmpeg> --duration 8 --fps 12.5 --report <qa.json>` when these cadence/duration choices suit the scene. It uses the sibling ffprobe executable, native-frame decoding, a fixed palette and GIF duration/loop/seam checks. It works with the studio's restricted FFmpeg build, without installing a second media runtime.

Record matched controls that disable only the new local effect while keeping source frame, camera and text identical. Test the emitting region and a protected still region separately. This establishes where pixels change; visual inspection establishes whether the change looks alive. Report true 2.5D/procedural effects accurately, without implying character or 3D animation. Artistic approval and public/paid release gates remain separate.
