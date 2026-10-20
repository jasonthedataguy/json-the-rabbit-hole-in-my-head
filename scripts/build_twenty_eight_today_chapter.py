"""Build Chapter 15's standalone reader from the selected author manuscript."""

from pathlib import Path

from manuscript import render_markdown


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "chapters/i-am-28-today"


def build() -> None:
    source = (CHAPTER / "source/approved.md").read_text(encoding="utf-8")
    body, heading, count = render_markdown(source)
    if heading != "I'm 28 today" or count != 6:
        raise ValueError(f"Unexpected manuscript structure: {heading!r}, {count}")
    page = f'''<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="theme-color" content="#112637">
  <meta name="description" content="I'm 28 today, the complete selected Chapter 15 manuscript in the .json digital book.">
  <title>I'm 28 today · Chapter 15 · .json</title>
  <link rel="icon" href="../../../assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="twenty-eight-today.css">
</head>
<body>
  <a class="skip" href="#essay">Skip to essay</a>
  <div class="progress" aria-hidden="true"><span id="progress-fill"></span></div>
  <header class="topbar">
    <a class="brand" href="../../../index.html#chapter/15">.json</a>
    <span>02_data_collection / Chapter 15</span>
    <a href="../../../index.html#chapter/15">Back to the book <span aria-hidden="true">↗</span></a>
  </header>
  <main>
    <section class="hero" aria-labelledby="title">
      <div class="hero-copy">
        <p class="eyebrow">CHAPTER 15 / DATA COLLECTION</p>
        <h1 id="title">I'm 28 today</h1>

        <p class="hero-lead">life is beautiful isn’t it</p>
        <a class="read-link" href="#essay">Read the chapter <span aria-hidden="true">↓</span></a>
      </div>
      <figure class="hero-art">
        <img src="assets/twenty-eight-today-portal-v1.png" width="1000" height="1000" alt="Jason looks through an open window while friends gather at a birthday table amid memories of work, music and travel.">
        <figcaption>Memory / Friendship / Gratitude</figcaption>
      </figure>
    </section>
    <figure class="scene-spread"><img src="assets/twenty-eight-today-spread-v1.webp" width="1632" height="289" alt="Jason, an open window, birthday cake, friends, camera, film frames, music and keepsakes."><figcaption>A life remembered in moments</figcaption></figure>
    <div class="reading-layout" id="essay">
      <aside class="essay-nav"><p>I'M 28 TODAY</p><a href="../source/approved.md" download>Download manuscript ↗</a><a href="../../../index.html#chapter/15">Return to the book ↗</a></aside>
      <article class="prose" aria-label="Full author manuscript">{body}</article>
    </div>
    <footer><a href="../../../index.html#chapter/15">Return to Chapter 15 in .json <span aria-hidden="true">↗</span></a></footer>
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
