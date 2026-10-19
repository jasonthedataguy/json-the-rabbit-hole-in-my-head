"""Build Chapter 27's standalone reader from the selected author manuscript."""

from pathlib import Path

from manuscript import render_markdown


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "chapters/masterclass-in-record-keeping"


def build() -> None:
    source = (CHAPTER / "source/approved.md").read_text(encoding="utf-8")
    body, heading, count = render_markdown(source)
    if heading != "04. Masterclass in Record Keeping" or count != 70:
        raise ValueError(f"Unexpected manuscript structure: {heading!r}, {count}")
    page = f'''<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="theme-color" content="#112637">
  <meta name="description" content="Office Battlefield: Masterclass in Record Keeping, the complete selected Chapter 27 manuscript in the .json digital book.">
  <title>Office Battlefield · Chapter 27 · .json</title>
  <link rel="icon" href="../../../assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="record-keeping.css">
</head>
<body>
  <a class="skip" href="#essay">Skip to essay</a>
  <div class="progress" aria-hidden="true"><span id="progress-fill"></span></div>
  <header class="topbar">
    <a class="brand" href="../../../index.html#chapter/27">.json</a>
    <span>04_model_failure / Chapter 27</span>
    <a href="../../../index.html#chapter/27">Back to the book <span aria-hidden="true">↗</span></a>
  </header>
  <main>
    <section class="hero" aria-labelledby="title">
      <div class="hero-copy">
        <p class="eyebrow">CHAPTER 27 / MODEL FAILURE</p>
        <h1 id="title">Office Battlefield</h1>
        <p class="subtitle">Masterclass in Record Keeping</p>
        <p class="hero-lead">Version history. Timestamp. Event log. Provenance. Evidence.</p>
        <a class="read-link" href="#essay">Read the chapter <span aria-hidden="true">↓</span></a>
      </div>
      <figure class="hero-art">
        <img src="assets/record-keeping-portal-v1.png" width="1000" height="1000" alt="Jason faces an opened record log and magnifying glass amid office files, timestamps and tickets.">
        <figcaption>History · Timestamp · Provenance · Evidence</figcaption>
      </figure>
    </section>
    <figure class="scene-spread"><img src="assets/record-keeping-spread-v1.webp" width="1632" height="289" alt="Jason, a small AI assistant, an opened record log, a magnifying glass, a file cabinet and office objects."><figcaption>The evidence trail</figcaption></figure>
    <div class="reading-layout" id="essay">
      <aside class="essay-nav"><p>OFFICE BATTLEFIELD</p><a href="../source/approved.md" download>Download manuscript ↗</a><a href="../../../index.html#chapter/27">Return to the book ↗</a></aside>
      <article class="prose" aria-label="Full author manuscript">{body}</article>
    </div>
    <footer><a href="../../../index.html#chapter/27">Return to Chapter 27 in .json <span aria-hidden="true">↗</span></a></footer>
  </main>
  <script>
    const fill=document.getElementById('progress-fill');
    function updateProgress(){{const max=document.documentElement.scrollHeight-innerHeight;fill.style.width=`${{max>0?Math.max(0,Math.min(100,scrollY/max*100)):0}}%`;}}
    addEventListener('scroll',updateProgress,{{passive:true}});addEventListener('resize',updateProgress);updateProgress();
  </script>
</body>
</html>
'''
    (CHAPTER / "web/index.html").write_text(page, encoding="utf-8")


if __name__ == "__main__":
    build()
