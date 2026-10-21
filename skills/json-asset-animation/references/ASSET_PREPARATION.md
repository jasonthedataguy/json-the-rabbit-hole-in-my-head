# Inspect and prepare existing art

Start from the selected chapter's `assets.json` and its role paths. Inspect explicit files with `motion_assets.py inspect <image...> --output <report.json>`. It reads images and emits metadata only. A directory input is limited to 64 selected image files; do not use the whole book library as a render public directory.

Check the images themselves after the report. An alpha minimum of zero is necessary for a cutout but not sufficient: some PNGs have a transparent margin around a mostly rectangular flattened scene. Preserve clean native silhouettes, perspective, relative scale and anchors. Existing Cơm nguội assets include usable RGBA elements; the three decorative panel JPEG/RGB-style PNGs are opaque planes, not clean object masks. The rice-bowl/steam crop is visibly soft; do not enlarge it into a full-screen hero.

For missing layers, derive the smallest necessary mask/crop from an existing source, in the project's animation version folder. Record source path/hash, crop bounds in source pixels, canvas dimensions, matte/feather, intended pivot, base-image alignment and any background repair. Keep source files immutable. A repair that creates unseen narrative details needs a deliberate creative decision; do not describe it as recovered original art.

Match each moving foreground object with its background. If a lamp is already in the flat hero, moving a duplicate cutout creates two lamps. Either remove/mask the baked lamp on a derived plate, construct a separate paper-stage scene from compatible cutouts, or select another scene. Do not cut and float whole faces/body parts or rig a family action without source and author intent.

Animate only material that can tolerate the motion: hanging objects pivot at their attachment, plants at their roots, shadows stay attached to contact surfaces, light spill belongs behind/over its subject deliberately. Maintain occlusion order. A shared whole-image transform gives no independent depth.

Reuse licensed fonts and source art by path/hash. The staging utility copies or aliases only explicit approved library inputs to a private cache and verifies bytes. New extraction derivatives belong under the declared project derivative root with provenance. Never edit a staged hardlink.
