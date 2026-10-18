"""Build Flow's standalone essay from its exact approved manuscript."""

from pathlib import Path
import re

from manuscript import render_markdown


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "chapters/flow"


def build() -> None:
    source = (CHAPTER / "source/approved.md").read_text(encoding="utf-8")
    body, heading, _ = render_markdown(source)
    if heading != "FLOW - the secret of wealth":
        raise ValueError(f"Unexpected Flow manuscript heading: {heading!r}")

    sections = []

    def mark_heading(match: re.Match[str]) -> str:
        section_id = f"section-{len(sections)+1}"
        sections.append((section_id, match.group(1)))
        return f'<h3 id="{section_id}">{match.group(1)}</h3>'

    body = re.sub(r"<h3>(.*?)</h3>", mark_heading, body)
    navigation = "".join(
        f'<a href="#{section_id}">{title}</a>' for section_id, title in sections
    )
    page = f'''<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="theme-color" content="#102735">
  <title>FLOW — The Secret of Wealth · .json</title>
  <meta name="description" content="Jason follows the river from income and assets to consumption and behavior in the full Flow essay.">
  <link rel="stylesheet" href="flow.css">
</head>
<body>
  <a class="skip" href="#essay">Skip to essay</a>
  <div class="progress" aria-hidden="true"><span id="progress-fill"></span></div>
  <header class="topbar">
    <a class="brand" href="../../../index.html#chapter/05">.json</a>
    <span>01_model_specification / Chapter 05</span>
    <a href="../../../index.html#chapter/05">Back to the book <span aria-hidden="true">↗</span></a>
  </header>
  <main>
    <section class="hero" aria-labelledby="title">
      <div class="hero-copy">
        <p class="eyebrow">CHAPTER 05 / MODEL SPECIFICATION</p>
        <h1 id="title">FLOW</h1>
        <p class="subtitle">The Secret of Wealth</p>
        <p class="hero-lead">Money is like water.<br>Wealth is the reservoir.<br>Cash flow is the river.</p>
        <a class="read-link" href="#essay">Follow the river <span aria-hidden="true">↓</span></a>
      </div>
      <figure class="hero-art">
        <img src="../artwork/portal/flow-portal-v2.png" width="1000" height="1000" alt="Jason stands before nested landscape rings and a winding river of money, with reservoir, waterwheel, houses and trees.">
        <figcaption>The river continues beyond the frame.</figcaption>
      </figure>
    </section>
    <figure class="object-strip"><img src="../artwork/portal/flow-spread-v2.webp" width="1600" height="480" alt="Jason, coins, reservoir, waterwheel, homes, seedling, trees, bridge and a cracked riverbank."><figcaption>Income · Assets · Consumption · Behavior</figcaption></figure>
    <div class="reading-layout" id="essay">
      <nav class="essay-nav" aria-label="Sections of Flow"><p>IN THIS CHAPTER</p>{navigation}<a href="../source/approved.md" download>Download original manuscript ↗</a></nav>
      <article class="prose" aria-label="Full author manuscript">{body}</article>
    </div>
    <footer><a href="../../../index.html#chapter/05">Return to Chapter 05 in .json <span aria-hidden="true">↗</span></a></footer>
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
