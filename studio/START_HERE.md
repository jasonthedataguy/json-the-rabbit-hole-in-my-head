# .json Studio

The book is the narrative authority. The studio coordinates editorial, reader design, artwork, author audio, film, social, optional commerce, release and learning from that source. Existing assets remain where they already live.

## Start a work session

1. Run `.\studio.ps1 status` from the workspace root. Cold Rice is active; Fashion and To Saigon are queued. Read the selected project's `project.json`, then its linked run manifest.
2. Read [the standard workflow](docs/WORKFLOW.md) and the relevant lane references. Read [the video system](docs/VIDEO_SYSTEM.md) for motion work. [Source reconciliation](docs/SOURCE_RECONCILIATION.md) records how the 12-slide deck and starter were adopted.
3. Produce the next actual artifact, update its version/source/hash and seek author approval only for the concrete decision at the next gate. Existing approval records remain in force for their exact scope.

Every video and recut follows [the opening standard](docs/VIDEO_OPENING.md): chapter title/portal, enter the center, reveal the scene, then story. The studio audit enforces this before flat-render preparation; explicitly requested exceptions are scoped in the cut record.

Use `$json-story-to-business` for the publishing workflow and `$json-asset-animation` for dynamic scene animation. The selected [Cơm nguội v5](projects/com-nguoi/video/README.md) is the complete silent living-illustration review: curling vapor, independent environmental motion and two caption-free GIF loops. Its [production guide](projects/com-nguoi/animation/v5/PRODUCTION.md) uses `render:v5`, `studio:v5` and `still:v5`. The [animation skill](../skills/json-asset-animation/SKILL.md) now includes [living-illustration guidance](../skills/json-asset-animation/references/LIVING_ILLUSTRATIONS.md), a reusable vapor component and a tested GIF exporter. The earlier [technical motion proof](reports/skill-validation/asset-animation/dynamic-motion-proof.mp4) remains a separate demonstration. Generic `prepare-video` applies to flat reading cuts and intentionally refuses the selected v5 animation timeline.

## Local commands

On this Windows workspace, `.\studio.ps1` selects the configured bundled Python and avoids the nonfunctional Windows Store `python` alias. It defaults to `status`; you can override the executable with `JSON_STUDIO_PYTHON`. For example:

```powershell
.\studio.ps1 audit
npm.cmd run render:v5 --prefix studio/apps/video
```

Direct Python equivalents:

```powershell
python scripts/studio.py catalog
python scripts/studio.py status
python scripts/studio.py audit
python scripts/studio.py check-release com-nguoi
python -m unittest discover -s tests -v
```

Use your configured Python 3.11+ executable if `python` is a Windows app alias. The control scripts use only the standard library. Catalog/audit read external source files and write local indexes/reports; they do not edit the book or artwork. `check-release` exits 2 when a release is blocked, which is expected for current projects.

For flat cuts, after preparing an internal preview with the selected chapter's `prepare-video` command:

```powershell
cd studio/apps/video
npm ci --ignore-scripts --no-audit --no-fund
npm run typecheck
npm run studio
npm run still
npm run render
```

The app uses Node/npm, pinned dependencies and its lockfile. Remotion may need its local browser runtime on first render. `npm run studio` starts a local interactive process; stop it when finished. The current full Cold Rice cut is marked **Bản dựng xem trước · Không âm thanh** and uses the author's supplied final video script. Its 27 cues are reading timings. Public/paid release remains separately gated. `prepare-video` selects a chapter/cut/format; there is no silent fallback to the first chapter.

Supported review formats: vertical 1080×1920, landscape 1920×1080, square 1080×1080, feed 1080×1440 at 30fps. Real voice recording determines final timing and captions. The flat-art renderer does not implement true parallax or final audio mixing.

## Workspace and authority

- [Workspace map](docs/WORKSPACE.md): current paths, storage and department responsibilities.
- [Pilot roadmap](docs/ROADMAP.md): completed foundation and actual remaining production work.
- [Setup verification](reports/SETUP_REPORT.md): actual checks, private render evidence and remaining gates.
- [Studio configuration](studio.json), [story catalog](catalog/stories.json), [pilot queue](operations/pilot-queue.json).
- [Cold Rice project](projects/com-nguoi/project.json): manuscript v1 and final video script approved; v4 rendered-look review, public family scope and release pending. Its existing run manifest remains authoritative.
- [Fashion project](projects/fashion/project.json) and [To Saigon project](projects/viet-cho-sai-gon-cua-t/project.json): references captured; no new creative approvals inferred.

No public posting, deployment, voice synthesis, outreach, payments, inventory purchase or recurring automation is part of this setup. Free chapter reading can release independently of optional commerce after its own gates pass.
