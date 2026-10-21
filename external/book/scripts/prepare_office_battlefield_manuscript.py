"""Lay out the author's supplied Office Battlefield text for the reader.

The source attachment is retained byte-for-byte in source/original.md. Each
nonempty source line is an author paragraph; this adds blank lines between
them and marks the first line as a heading. No words are edited.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "chapters/the-23-word-nuclear-warhead/source/original.md"
SELECTED = ROOT / "chapters/the-23-word-nuclear-warhead/source/approved.md"


def prepare() -> None:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    if lines[0] != "01. The 23-Word Nuclear Warhead":
        raise ValueError("Unexpected author manuscript heading")
    if not any("All in one Slack message." in line for line in lines):
        raise ValueError("The supplied ending is missing")
    paragraphs = [line for line in lines if line.strip()]
    SELECTED.write_text("# " + paragraphs[0] + "\n\n" + "\n\n".join(paragraphs[1:]) + "\n", encoding="utf-8")


if __name__ == "__main__":
    prepare()
