"""Build Chapter 07's standalone reader from the selected author manuscript."""

from pathlib import Path

from manuscript import render_markdown


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "chapters/mot-nguoi-ban-cu"


def build() -> None:
    source = (CHAPTER / "source/approved.md").read_text(encoding="utf-8")
    body, heading, _ = render_markdown(source)
    if heading != "An Old Friend":
        raise ValueError(f"Unexpected manuscript heading: {heading!r}")
    page = f'''<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="theme-color" content="#112637">
  <meta name="description" content="An Old Friend: the complete author-selected Chapter 07 manuscript in the .json digital book.">
  <title>An Old Friend · Chapter 07 · .json</title>
  <link rel="icon" href="../../../assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="old-friend.css">
</head>
<body>
  <a class="skip" href="#essay">Skip to essay</a>
  <div class="progress" aria-hidden="true"><span id="progress-fill"></span></div>
  <header class="topbar">
    <a class="brand" href="../../../index.html#chapter/07">.json</a>
    <span>02_data_collection / Chapter 07</span>
    <a href="../../../index.html#chapter/07">Back to the book <span aria-hidden="true">↗</span></a>
  </header>
  <main>
    <section class="hero" aria-labelledby="title">
      <div class="hero-copy">
        <p class="eyebrow">CHAPTER 07 / DATA COLLECTION</p>
        <h1 id="title">An Old Friend</h1>
        <p class="hero-lead">Và tớ vẫn nhớ gói chíp chíp ngày hôm ấy.</p>
        <a class="read-link" href="#essay">Read the chapter <span aria-hidden="true">↓</span></a>
      </div>
      <figure class="hero-art">
        <img src="assets/old-friend-portal-v1.png" width="1000" height="1000" alt="Two childhood friends share a small packet of candy on a bench, surrounded by games, school papers and paths that diverge.">
        <figcaption>Childhood · Friendship · Memory · Distance</figcaption>
      </figure>
    </section>
    <figure class="scene-spread"><img src="assets/old-friend-spread-v1.webp" width="1638" height="342" alt="Childhood friends, a packet of candy, a game console, school papers, an apology and a gate from the chapter artwork."><figcaption>What stays from a childhood friendship</figcaption></figure>
    <div class="reading-layout" id="essay">
      <aside class="essay-nav"><p>AN OLD FRIEND</p><a href="../source/approved.md" download>Download manuscript ↗</a><a href="../../../index.html#chapter/07">Return to the book ↗</a></aside>
      <article class="prose" aria-label="Full author manuscript">{body}</article>
    </div>
    <footer><a href="../../../index.html#chapter/07">Return to Chapter 07 in .json <span aria-hidden="true">↗</span></a></footer>
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
