"""Switch the editable Cold Rice immersive page to its v2 digital art.

This only changes the experience wrapper; the story and archive prose stay intact.
"""
from pathlib import Path

PAGE = Path(__file__).resolve().parents[1] / 'chapters/com-nguoi/web/index.html'


def main():
    page = PAGE.read_text(encoding='utf-8')
    changes = [
        ('<meta name="theme-color" content="#102a2c">', '<meta name="theme-color" content="#102331">'),
        ('<title>Cơm nguội — .json</title>', '<title>Cold Rice — .json</title>'),
        ('href="https://jasonthedataguy.github.io/json-under-revision/chapters/07/"', 'href="https://jasonthedataguy.github.io/json-under-revision-v2/chapters/com-nguoi/web/"'),
        ('<meta property="og:title" content="Cơm nguội — .json">', '<meta property="og:title" content="Cold Rice — .json">'),
        ('content="https://jasonthedataguy.github.io/json-under-revision/chapters/07/artwork/exports/hero.jpg"', 'content="https://jasonthedataguy.github.io/json-under-revision-v2/chapters/com-nguoi/web/assets/rice-portal-board-v2.png"'),
        ('<style>:root{--dark:#102a2c;--paper:#f3ead5;--accent:#d39b72;--ink:#182a2a}</style>', '<link rel="stylesheet" href="cold-rice-v2.css">'),
        ('<a class="brand" href="https://jasonthedataguy.github.io/json-under-revision/">', '<a class="brand" href="../../../index.html#chapter/00">'),
        ('href="https://jasonthedataguy.github.io/json-under-revision/#chapters">Chapters</a>', 'href="../../../index.html#contents">Chapters</a>'),
        ('href="https://jasonthedataguy.github.io/json-under-revision/about/">About</a>', 'href="../../../index.html#edition">About</a>'),
        ('<picture><source media="(max-width:700px)" srcset="../artwork/exports/hero-mobile.jpg"><img src="../artwork/exports/hero.jpg" alt="Minh họa chương Cơm nguội" width="1600" height="960" fetchpriority="high"></picture>', '<picture><img src="assets/rice-portal-board-v2.png" alt="A floral paper portal frames a Vietnamese family dinner beneath a warm hanging lamp." width="1000" height="1000" fetchpriority="high"></picture>'),
        ('<div class="eyebrow">CHAPTER 07 / .json</div><h1 id="chapter-title">Cơm nguội</h1>', '<div class="eyebrow">PROLOGUE 00 / ORIGINAL ESSAY 07</div><h1 id="chapter-title">Cold Rice</h1>'),
        ('<div class="eyebrow">THE STORY / 07</div>', '<div class="eyebrow">THE STORY / PROLOGUE 00</div>'),
        ('<a href="https://jasonthedataguy.github.io/json-under-revision/">← Tất cả các chương</a><a href="https://jasonthedataguy.github.io/json-under-revision/chapters/08/">Dating Algorithm →</a>', '<a href="../../../index.html#chapter/00">Digital book / Prologue 00</a><a href="../../../index.html#chapter/01">Chapter 01: I Was Born a Quant →</a>'),
    ]
    for old, new in changes:
        if old not in page:
            if new in page:
                continue
            raise ValueError(f'Missing expected Cold Rice wrapper text: {old[:90]}')
        page = page.replace(old, new, 1)
    PAGE.write_text(page, encoding='utf-8', newline='')


if __name__ == '__main__':
    main()
