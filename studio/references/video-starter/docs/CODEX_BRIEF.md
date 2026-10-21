# Codex Implementation Brief

Build a clean, scalable video production toolkit on top of this repository. Preserve the original art board references, `.json` quiet-luxury aesthetic, and the concept of **Read → Explore → Revisit**.

## Milestones
1. **M0 inventory:** read `manifests/chapters.json`, identify missing boards and final approvals; do not hallucinate content.
2. **M1 playable prototype:** run the supplied Remotion sample; ship a preview for Cold Rice, Fashion, and To Saigon.
3. **M2 parallax master:** layer-aware scene component with independently moving depth planes, subtle animated light, textures, aspect-ratio composition and vertical safe areas.
4. **M3 editorial pipeline:** chapter specific editable `timeline.json` with intro, movement, quote, asset, voiceover path, caption slots and timing in seconds. Add validation.
5. **M4 automation:** batch render scripts for 9:16, 16:9, 1:1; cover frame generation; metadata; chapter CTA pointing to configured chapter URL only, not invented links.
6. **M5 QC:** ensure no image text unreadably small; no faces redrawn in unapproved ways; no unsupported claims; consent and music license gates; reviewer signoff.

## Technical direction
Use Remotion + React + TypeScript, plain CSS, local asset paths, ffmpeg. Avoid paid video generation until the master illustrated style is approved. Provide local preview, reproducible seeds/settings and deterministic exports.

## Acceptance criteria
- Single chapter JSON drives title, shots, audio and outputs.
- Assets mapped explicitly; paths validated before rendering.
- Graceful fallback for flattened boards (slow crop/push-in); no claim that flat art has genuine parallax.
- Motion is quiet, readable and coherent across chapters.
- Approval gates prevent publishing private/uncleared asset sets.
