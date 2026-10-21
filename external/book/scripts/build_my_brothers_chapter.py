"""Build Chapter 13's standalone reader from the selected author manuscript."""

from pathlib import Path

from manuscript import render_markdown


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "chapters/nhung-nguoi-anh-em"


def build() -> None:
    source = (CHAPTER / "source/approved.md").read_text(encoding="utf-8")
    body, heading, count = render_markdown(source)
    if heading != "My brothers" or count != 6:
        raise ValueError(f"Unexpected manuscript structure: {heading!r}, {count}")
    page = f'''<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="theme-color" content="#112637">
  <meta name="description" content="My brothers, the complete selected Chapter 13 manuscript in the .json digital book.">
  <title>My brothers · Chapter 13 · .json</title>
  <link rel="icon" href="../../../assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="my-brothers.css">
</head>
<body>
  <a class="skip" href="#essay">Skip to essay</a>
  <div class="progress" aria-hidden="true"><span id="progress-fill"></span></div>
  <header class="topbar">
    <a class="brand" href="../../../index.html#chapter/13">.json</a>
    <span>02_data_collection / Chapter 13</span>
    <a href="../../../index.html#chapter/13">Back to the book <span aria-hidden="true">↗</span></a>
  </header>
  <main>
    <section class="hero" aria-labelledby="title">
      <div class="hero-copy">
        <p class="eyebrow">CHAPTER 13 / DATA COLLECTION</p>
        <h1 id="title">My brothers</h1>

        <p class="hero-lead">where I belong</p>
        <a class="read-link" href="#essay">Read the chapter <span aria-hidden="true">↓</span></a>
      </div>
      <figure class="hero-art">
        <img src="assets/my-brothers-portal-v1.png" width="1000" height="1000" alt="Four former teammates gather around a glowing universe model at a table, surrounded by books and diagrams.">
        <figcaption>Friendship / Curiosity / Belonging</figcaption>
      </figure>
    </section>
    <figure class="scene-spread"><img src="assets/my-brothers-spread-v1.webp" width="1632" height="289" alt="Jason and his former teammates, an illuminated universe model, books, physics diagrams, a globe and shared drinks."><figcaption>Questions among friends</figcaption></figure>
    <div class="reading-layout" id="essay">
      <aside class="essay-nav"><p>MY BROTHERS</p><a href="../source/approved.md" download>Download manuscript ↗</a><a href="../../../index.html#chapter/13">Return to the book ↗</a></aside>
      <article class="prose" aria-label="Full author manuscript">{body}</article>
    </div>
    <footer><a href="../../../index.html#chapter/13">Return to Chapter 13 in .json <span aria-hidden="true">↗</span></a></footer>
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
