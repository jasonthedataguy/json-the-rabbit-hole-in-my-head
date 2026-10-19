"""Build Chapter 21's standalone reader from the selected author manuscript."""

from pathlib import Path

from manuscript import render_markdown


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "chapters/runaway"


def build() -> None:
    source = (CHAPTER / "source/approved.md").read_text(encoding="utf-8")
    body, heading, _ = render_markdown(source)
    if heading != "Runaway":
        raise ValueError(f"Unexpected manuscript heading: {heading!r}")
    page = f'''<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="theme-color" content="#112637">
  <meta name="description" content="Run away: the complete author-selected Chapter 21 manuscript in the .json digital book.">
  <title>Run away · Chapter 21 · .json</title>
  <link rel="icon" href="../../../assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="runaway.css">
</head>
<body>
  <a class="skip" href="#essay">Skip to essay</a>
  <div class="progress" aria-hidden="true"><span id="progress-fill"></span></div>
  <header class="topbar">
    <a class="brand" href="../../../index.html#chapter/21">.json</a>
    <span>03_relationship_modeling / Chapter 21</span>
    <a href="../../../index.html#chapter/21">Back to the book <span aria-hidden="true">↗</span></a>
  </header>
  <main>
    <section class="hero" aria-labelledby="title">
      <div class="hero-copy">
        <p class="eyebrow">CHAPTER 21 / RELATIONSHIP MODELING</p>
        <h1 id="title">Run away</h1>
        <p class="hero-lead">A chỉ muốn ở đó.</p>
        <a class="read-link" href="#essay">Read the chapter <span aria-hidden="true">↓</span></a>
      </div>
      <figure class="hero-art">
        <img src="assets/runaway-portal-v1.png" width="1000" height="1000" alt="Jason pauses at a warm doorway where a woman and dog wait inside; work, music, drawing and memories circle them.">
        <figcaption>Drawing · Music · Care · Distance</figcaption>
      </figure>
    </section>
    <figure class="scene-spread"><img src="assets/runaway-spread-v1.webp" width="1632" height="336" alt="Jason, a woman, their dog, an open doorway, a sofa, drawing tablet, headphones, music and small domestic objects from the board."><figcaption>A place to stay, or another exit</figcaption></figure>
    <div class="reading-layout" id="essay">
      <aside class="essay-nav"><p>RUN AWAY</p><a href="../source/approved.md" download>Download manuscript ↗</a><a href="../../../index.html#chapter/21">Return to the book ↗</a></aside>
      <article class="prose" aria-label="Full author manuscript">{body}</article>
    </div>
    <footer><a href="../../../index.html#chapter/21">Return to Chapter 21 in .json <span aria-hidden="true">↗</span></a></footer>
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
