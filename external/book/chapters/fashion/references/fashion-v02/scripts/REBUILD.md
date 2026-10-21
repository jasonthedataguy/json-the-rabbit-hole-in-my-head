# Rebuilding the Fashion v0.2 production kit

**No remote services or private data are required.** The five supplied poster source images remain under `assets/master/` and the manuscript under `content/`.

Run in this extracted folder (Python 3.10+, Pillow, reportlab, PyMuPDF, FFmpeg):

```bash
python -m pip install -r scripts/requirements.txt
python scripts/build_assets.py
python scripts/build_media_and_docs.py
python scripts/validate.py
```

`build_assets.py` produces A5 PDF, WebP scene assets, and social/vertical storyboard images. `build_media_and_docs.py` makes the two ambient animatics, contact sheets and 64-task board. It overwrites derived drafts, **not** the five original selected images. For the exact saved v0.2, the ready files are already included: running the scripts is optional.

For website preview open `website/index.html` after extracting with the `website/assets` folder. Embedded manuscript data in the script is intentionally part of the PRIVATE review pack; do not copy it into a public website without author publication approval.

Commercial rights for visible logos, posters, people or music are not guaranteed by having a generated concept image. Content sign-off, rights clearance, voiceover, printer PDF/X, and live deployment remain separate stages.
