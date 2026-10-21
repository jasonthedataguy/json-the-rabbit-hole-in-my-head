"""Cut complete reading-page rectangles from the supplied Introduction and Quant boards.

These crops accompany their circular portals in the digital book. They are
screen-resolution excerpts, not separately editable print illustrations.
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CROPS = (
    (
        ROOT / 'references/design/Introduction Portal Ring Concept Board.png',
        (1672, 941),
        (165, 268, 585, 548),
        ROOT / 'shared/artwork/portal/introduction-reading-spread-v2.webp',
    ),
    (
        ROOT / 'chapters/i-was-born-a-quant/references/editorial-artboard.png',
        (1536, 1024),
        (0, 345, 540, 610),
        ROOT / 'chapters/i-was-born-a-quant/artwork/portal/quant-reading-spread-v2.webp',
    ),
)


def cut():
    for source, dimensions, box, output in CROPS:
        board = Image.open(source).convert('RGB')
        if board.size != dimensions:
            raise ValueError(f'Unexpected artboard size for {source}: {board.size}')
        output.parent.mkdir(parents=True, exist_ok=True)
        board.crop(box).save(output, 'WEBP', quality=96, method=6)


if __name__ == '__main__':
    cut()
