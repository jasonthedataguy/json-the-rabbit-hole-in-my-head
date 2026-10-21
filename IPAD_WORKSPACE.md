# iPad source workspace

This `ipad-workspace` branch is the source and production-control snapshot inside
`jasonthedataguy/json-the-rabbit-hole-in-my-head`. It is separate from `main`,
which deploys the public reader. The book working-tree text, including local
edits that were not on `main`, is under `external/book/` in this snapshot.

Sign in to GitHub as `jasonthedataguy` on the iPad, select this branch, and
open the browser editor to work on code and text. Commit and push changes to
this branch; they will not change the live reader until they are deliberately
reviewed and applied to `main`.

Large media and source artwork are not ordinary Git files here. The current
studio runtime bundles and review exports belong to the account's private
[`json-studio` handoff](https://github.com/jasonthedataguy/json-studio), whose
`cloud/README.md` explains the Codespaces workflow and hash-checked restore.
The complete historical design library has a separate private Drive transfer;
check the companion private studio handoff for its actual upload status before
relying on it. These backups are snapshots, not automatic sync from the Windows
drives.

The private studio repository is the easiest route for running the video app
from a Codespace. This public branch is useful for reviewing and editing the
source alongside the book, without adding gigabytes of media to the reader repo.
