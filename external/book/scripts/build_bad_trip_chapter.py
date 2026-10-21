"""Build Chapter 16's standalone reader from the selected author manuscript."""

from pathlib import Path

from manuscript import render_markdown


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "chapters/bad-trip"


def build() -> None:
    source = (CHAPTER / "source/approved.md").read_text(encoding="utf-8")
    body, heading, _ = render_markdown(source)
    if heading != "Badtrip":
        raise ValueError(f"Unexpected manuscript heading: {heading!r}")
    page = f'''<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="theme-color" content="#112637">
  <meta name="description" content="Bad Trip: the complete author-selected Chapter 16 manuscript in the .json digital book.">
  <title>Bad Trip · Chapter 16 · .json</title>
  <link rel="icon" href="../../../assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="bad-trip.css">
</head>
<body>
  <a class="skip" href="#essay">Skip to essay</a>
  <div class="progress" aria-hidden="true"><span id="progress-fill"></span></div>
  <header class="topbar">
    <a class="brand" href="../../../index.html#chapter/16">.json</a>
    <span>02_data_collection / Chapter 16</span>
    <a href="../../../index.html#chapter/16">Back to the book <span aria-hidden="true">↗</span></a>
  </header>
  <main>
    <section class="hero" aria-labelledby="title">
      <div class="hero-copy">
        <p class="eyebrow">CHAPTER 16 / DATA COLLECTION</p>
        <h1 id="title">Bad Trip</h1>
        <p class="hero-lead">I just wanted to be Jason.</p>
        <a class="read-link" href="#essay">Read the chapter <span aria-hidden="true">↓</span></a>
      </div>
      <figure class="hero-art">
        <img src="assets/bad-trip-portal-v1.png" width="1000" height="1000" alt="Jason faces a gilded mirror that holds another version of himself; photographs, travel and work circle them.">
        <figcaption>Identity · Memory · Work · Return</figcaption>
      </figure>
    </section>
    <figure class="scene-spread"><img src="assets/bad-trip-spread-v1.webp" width="1632" height="321" alt="A gilded mirror, two versions of Jason, old photographs, a work desk, vinyl record and travel case from the board."><figcaption>The version of himself he tried to leave behind</figcaption></figure>
    <div class="reading-layout" id="essay">
      <aside class="essay-nav"><p>BAD TRIP</p><a href="../source/approved.md" download>Download manuscript ↗</a><a href="../../../index.html#chapter/16">Return to the book ↗</a></aside>
      <article class="prose" aria-label="Full author manuscript">{body}</article>
    </div>
    <footer><a href="../../../index.html#chapter/16">Return to Chapter 16 in .json <span aria-hidden="true">↗</span></a></footer>
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
