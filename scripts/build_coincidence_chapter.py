"""Render Chapter 11's standalone page from the exact author-selected manuscript."""

from pathlib import Path
import html

from manuscript import render_markdown


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "chapters/nhung-su-trung-hop"
TITLE = "Coincidence - Or the arrangement of the universe"
SECTIONS = (
    ("The clocks", "Repeating digits and the patterns we remember"),
    ("The crossings", "Former colleagues, flatmates and converging paths"),
    ("The bookshop", "A conversation in Saratoga"),
    ("The question", "Chance, attention and meaning"),
)


def build() -> None:
    source = (CHAPTER / "source/approved.md").read_text(encoding="utf-8")
    body, heading, _ = render_markdown(source)
    if heading != TITLE:
        raise ValueError(f"Unexpected manuscript heading: {heading!r}")
    sections = body.split("\n<hr>\n")
    if len(sections) != len(SECTIONS):
        raise ValueError(f"Expected four manuscript movements, found {len(sections)}")

    navigation = "".join(
        f'<a href="#movement-{index}"><span>0{index}</span>{html.escape(label)}</a>'
        for index, (label, _) in enumerate(SECTIONS, 1)
    )
    prose = "".join(
        f'<section id="movement-{index}" class="movement" aria-labelledby="movement-title-{index}">'
        f'<header><span>0{index} / 04</span><h2 id="movement-title-{index}">{html.escape(label)}</h2>'
        f'<p>{html.escape(subtitle)}</p></header><div class="movement-prose">{section}</div></section>'
        for index, ((label, subtitle), section) in enumerate(zip(SECTIONS, sections), 1)
    )
    page = f'''<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="theme-color" content="#112637">
  <meta name="description" content="The complete author-selected Chapter 11 essay in the .json digital book.">
  <title>Coincidence · Chapter 11 · .json</title>
  <link rel="icon" href="../../../assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="coincidence.css">
</head>
<body>
  <a class="skip" href="#essay">Skip to essay</a>
  <div class="progress" aria-hidden="true"><span id="progress-fill"></span></div>
  <header class="topbar">
    <a class="brand" href="../../../index.html#chapter/11">.json</a>
    <span>02_data_collection / Chapter 11</span>
    <a href="../../../index.html#chapter/11">Back to the book <span aria-hidden="true">↗</span></a>
  </header>
  <main>
    <section class="hero" aria-labelledby="title">
      <div class="hero-copy">
        <p class="eyebrow">CHAPTER 11 / DATA COLLECTION</p>
        <h1 id="title">Coincidence</h1>
        <p class="subtitle">Or the arrangement of the universe</p>
        <p class="hero-lead">Maybe it's all random.<br>Maybe I'm just paying more attention.</p>
        <a class="read-link" href="#essay">Follow the paths <span aria-hidden="true">↓</span></a>
      </div>
      <figure class="hero-art">
        <img src="assets/coincidence-portal-v1.png" width="1000" height="1000" alt="Jason faces a glowing bookshop at the meeting point of golden paths, surrounded by stars, clocks and autumn streets.">
        <figcaption>Time · Paths · Chance · Attention</figcaption>
      </figure>
    </section>
    <figure class="scene-spread"><img src="assets/coincidence-spread-v1.webp" width="1600" height="1186" alt="A warm bookshop glows beneath a constellation where winding golden paths meet."><figcaption>One small bookshop. Many paths into it.</figcaption></figure>
    <div class="reading-layout" id="essay">
      <nav class="essay-nav" aria-label="Movements of Coincidence"><p>FOLLOW THE ESSAY</p>{navigation}<a href="../source/approved.md" download>Download manuscript ↗</a></nav>
      <article class="prose" aria-label="Full author manuscript">{prose}</article>
    </div>
    <footer><a href="../../../index.html#chapter/11">Return to Chapter 11 in .json <span aria-hidden="true">↗</span></a></footer>
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
