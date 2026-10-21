# Work on the .json studio from an iPad

If you are reading this on the public book repository's `ipad-workspace`
branch, start with [IPAD_WORKSPACE.md](../IPAD_WORKSPACE.md). The steps below
describe the companion private `json-studio` handoff and its media bundles.

Use the private **jasonthedataguy/json-studio** repository. The code, skills, workflow records and book working-tree source are in Git. Media, the design deck, local extraction layers, all review exports and the artwork needed by current projects are in hash-deduplicated private release bundles. The complete design/generation archive is handled by the coordinated **design workspace** chat in Google Drive; check the companion private repository for its current transfer status. The public reader on `main` is not changed by this handoff.

## Open the studio

1. Sign in to GitHub as **jasonthedataguy** in the iPad browser.
2. Open this repository, choose **Code → Codespaces → Create codespace on main**. GitHub provides a browser editor, terminal and Linux compute; this does not run Remotion directly on iPadOS. Check GitHub's displayed compute allowance/billing before starting.
3. The development-container setup installs the pinned video dependencies, restores the current-project assets and stages Cơm nguội v5. Initial setup downloads the private runtime bundles and may take several minutes. It does not download the separate historical/design archive from Google Drive.
4. Run the command below, then open forwarded port **3000**. Keep it private.
5. Use render:v5 to render the full silent review. Add -- --loop=dinner or -- --loop=child for the illustration loops.

    npm run studio:v5 --prefix studio/apps/video -- --port=3000
    npm run render:v5 --prefix studio/apps/video

The same GitHub account works independently of the account used for an AI assistant. A different GitHub login needs explicit repository access; no extra account has been invited automatically.

## Continue work

Read studio/START_HERE.md and the selected project's single run manifest. Use the existing final script, portal opening and animation skill. Artistic/public/paid gates remain pending; backing up to this private repository does not approve release.

Commit and push code/text changes in the browser editor before ending a session. Generated media and local caches remain outside normal Git history. Download a new render or upload it to an explicitly selected private asset snapshot before deleting its codespace. This initial handoff is a complete snapshot, not an automatic ongoing sync of the Windows E: drive.

The current v5 review and both GIFs are also attached directly to the private handoff release for easy download without starting a codespace.

## Restore or verify manually

    python -m pip install -r cloud/requirements.txt
    npm ci --ignore-scripts --no-audit --no-fund --prefix studio/apps/video
    python cloud/bootstrap.py --download
    python scripts/studio.py audit
    npm run typecheck --prefix studio/apps/video

cloud/bootstrap.py --archives /path/to/downloaded/bundles works with local archive copies. It verifies archive/object SHA-256 hashes and restores original bytes. Only the ignored cloud/local-paths.json maps Windows references to this checkout; it does not rewrite signed source/approval records. Package manifests state exactly which files were included. Caches, browser profiles, credentials and private keys are excluded.

The canonical external book working tree is captured under external/book, including its uncommitted manuscript edits. It is a portable source snapshot with upstream provenance, not a new public book deployment. Current-project artwork restores under external/artwork. Do not regenerate it.

For chapters/designs beyond the current runtime subset, download the canonical artwork ZIP from the private Google Drive handoff, then run:

    python cloud/restore_design_archive.py /path/to/json-digital-book-assets.zip

That restores the full 7,360-file canonical library against its original hashes. Historical variants and design-generation working scripts remain in the additional design-chat bundles linked by the provider receipt. Keeping those large archives in Drive avoids uploading the full library to GitHub a second time.

Reference: [GitHub Codespaces quickstart](https://docs.github.com/en/codespaces/quickstart), [GitHub release assets](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases), [Remotion Linux dependencies](https://www.remotion.dev/docs/miscellaneous/linux-dependencies).
