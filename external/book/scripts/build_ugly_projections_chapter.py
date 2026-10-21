"""Build Chapter 23's standalone reader from the selected author manuscript."""

from pathlib import Path

from manuscript import render_markdown


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "chapters/nhung-hinh-chieu-xau-xi"


def build() -> None:
    source = (CHAPTER / "source/approved.md").read_text(encoding="utf-8")
    body, heading, count = render_markdown(source)
    if heading != "Bài 26: Ugly Projections" or count != 109:
        raise ValueError(f"Unexpected manuscript structure: {heading!r}, {count}")
    page = f'''<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="theme-color" content="#112637">
  <meta name="description" content="Ugly Projections: Ugly Projections, the complete selected Chapter 23 manuscript in the .json digital book.">
  <title>Ugly Projections · Chapter 23 · .json</title>
  <link rel="icon" href="../../../assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="ugly-projections.css">
</head>
<body>
  <a class="skip" href="#essay">Skip to essay</a>
  <div class="progress" aria-hidden="true"><span id="progress-fill"></span></div>
  <header class="topbar">
    <a class="brand" href="../../../index.html#chapter/23">.json</a>
    <span>03_relationship_modelling / Chapter 23</span>
    <a href="../../../index.html#chapter/23">Back to the book <span aria-hidden="true">↗</span></a>
  </header>
  <main>
    <section class="hero" aria-labelledby="title">
      <div class="hero-copy">
        <p class="eyebrow">CHAPTER 23 / RELATIONSHIP MODELLING</p>
        <h1 id="title">Ugly Projections</h1>

        <p class="hero-lead">I kept seeing women as someone they weren't.</p>
        <a class="read-link" href="#essay">Read the chapter <span aria-hidden="true">↓</span></a>
      </div>
      <figure class="hero-art">
        <img src="assets/ugly-projections-portal-v1.png" width="1000" height="1000" alt="Jason faces a film projector and the shadow he cast on a woman, while she stands beyond the projection.">
        <figcaption>Memory / Projection / Recognition</figcaption>
      </figure>
    </section>
    <figure class="scene-spread"><img src="assets/ugly-projections-spread-v1.webp" width="1632" height="289" alt="Jason, a film projector, projected silhouette, woman, lens, paintings, empty chairs and pause symbol."><figcaption>Seeing someone as themselves</figcaption></figure>
    <div class="reading-layout" id="essay">
      <aside class="essay-nav"><p>UGLY PROJECTIONS</p><a href="../source/approved.md" download>Download manuscript ↗</a><a href="../../../index.html#chapter/23">Return to the book ↗</a></aside>
      <article class="prose" aria-label="Full author manuscript">{body}</article>
    </div>
    <footer><a href="../../../index.html#chapter/23">Return to Chapter 23 in .json <span aria-hidden="true">↗</span></a></footer>
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
