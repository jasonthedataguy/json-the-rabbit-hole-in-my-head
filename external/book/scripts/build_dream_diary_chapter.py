"""Build Chapter 10's standalone reader from the selected author manuscript."""

from pathlib import Path

from manuscript import render_markdown


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "chapters/nhung-thu-khong-duoc-luu-lai"


def build() -> None:
    source = (CHAPTER / "source/approved.md").read_text(encoding="utf-8")
    body, heading, count = render_markdown(source)
    if heading != "Những thứ không được lưu lại" or count != 135:
        raise ValueError(f"Unexpected manuscript structure: {heading!r}, {count}")
    page = f'''<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="theme-color" content="#112637">
  <meta name="description" content="Dream Diary, the complete selected Chapter 10 manuscript in the .json digital book.">
  <title>Dream Diary · Chapter 10 · .json</title>
  <link rel="icon" href="../../../assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="dream-diary.css">
</head>
<body>
  <a class="skip" href="#essay">Skip to essay</a>
  <div class="progress" aria-hidden="true"><span id="progress-fill"></span></div>
  <header class="topbar">
    <a class="brand" href="../../../index.html#chapter/10">.json</a>
    <span>02_data_collection / Chapter 10</span>
    <a href="../../../index.html#chapter/10">Back to the book <span aria-hidden="true">↗</span></a>
  </header>
  <main>
    <section class="hero" aria-labelledby="title">
      <div class="hero-copy">
        <p class="eyebrow">CHAPTER 10 / DATA COLLECTION</p>
        <h1 id="title">Dream Diary</h1>
        <p class="subtitle">The Things We Never Saved</p>

        <p class="hero-lead">Nhưng rồi đoàn tàu tới. Và tôi tỉnh dậy.</p>
        <a class="read-link" href="#essay">Read the chapter <span aria-hidden="true">↓</span></a>
      </div>
      <figure class="hero-art">
        <img src="assets/dream-diary-portal-v1.png" width="1000" height="1000" alt="Two people hold hands beside an approaching yellow metro train, with an open dream diary in the foreground.">
        <figcaption>Dream / Memory / Letting Go</figcaption>
      </figure>
    </section>
    <figure class="scene-spread"><img src="assets/dream-diary-spread-v1.webp" width="1632" height="289" alt="An open diary, metro train, two people holding hands, pencil, sketches, childhood objects and nighttime windows."><figcaption>Things we never saved</figcaption></figure>
    <div class="reading-layout" id="essay">
      <aside class="essay-nav"><p>DREAM DIARY</p><a href="../source/approved.md" download>Download manuscript ↗</a><a href="../../../index.html#chapter/10">Return to the book ↗</a></aside>
      <article class="prose" aria-label="Full author manuscript">{body}</article>
    </div>
    <footer><a href="../../../index.html#chapter/10">Return to Chapter 10 in .json <span aria-hidden="true">↗</span></a></footer>
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
