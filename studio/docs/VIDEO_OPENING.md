# Opening standard for every .json video

Author instruction, 21 October 2026: standardize the opening of every video.

**Chapter portal + title → move into the center → reveal center artwork → story.**

Use the chapter's exact selected title and its own existing portal. Let the title read before the first narrative sentence. A silent review has a title reading beat; a narrated release uses the author's actual chapter-title take. Do not generate a personal voice or invent an introductory memoir paragraph.

Choose timing for the selected format and real narration. Even short recuts retain a legible compact opening; do not cut it automatically because of a default 18/45/60-second target. An explicit author request may select an exception. Record that instruction, version and scope in the timeline. Diagnostic frame ranges must identify themselves as partial tests rather than complete videos.

## Per-video record

Record the title/source reference, portal path/hash, normalized focus coordinates, center/reveal asset path/hash, title hold, entry/reveal times, story start and narrator state. The handoff lands inside the revealed scene; the first paragraph does not jump back to a whole exterior portal. For shared-cover openings, retain its established fixed-Jason / moving-ring-and-Gấu behavior when those layers exist. A chapter-specific portal follows its own composition.

If the center exists only in a flattened illustration, use the existing sharp matching hero where possible. Otherwise derive a sourced crop/mask and check its usable resolution. Report a missing usable center rather than quietly substituting unrelated art. Flat camera entry remains a camera move; independent planes must exist before claiming layered animation.

## Opening review before the full export

Render a motion preview covering the title hold, approach, center reveal and the first narrative line. Inspect it as a sequence, including the landing frame and first story frame. Check focus, title diacritics, legible hold, no prolonged soft enlargement, masks/edges, matching composition, continuous timing and no premature narrative/captions. Preserve its file and settings with the project's one controlling run.

This preview is internal production work. Obtain author approval of the selected look and final cut for its quality gate; retain separate public/disclosure and paid-release gates. Existing approval applies only to its exact scope. Do not stop internal drafting or technical previews merely because public gates are pending.

## Existing implementation and example

The current `portal_entry` shot supports a flat-art camera move and matching hero reveal, with explicit focus and hashed assets. The opening camera has a bounded maximum 6× enlargement; ordinary flat story pushes remain within 1.05×. This bound belongs to the existing renderer and is not a substitute for judging pixel quality.

Cơm nguội v3 is the first implementation: title hold, entry beginning at 2.6 seconds, sharp family-table reveal, then story at 10.5 seconds. Its complete 120-second silent cut and previous versions remain in `studio/projects/com-nguoi/video/`. This opening is implemented; independently animated story scenes are a separate capability described in the asset-animation skill.
