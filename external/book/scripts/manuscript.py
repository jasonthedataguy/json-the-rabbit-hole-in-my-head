#!/usr/bin/env python3
"""Render the existing manuscript Markdown subset without changing source bytes."""

from __future__ import annotations

import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urlsplit


def safe_url(value: str) -> str | None:
    """Only links with ordinary browser-safe protocols can reach the reader."""
    if any(ord(c) < 32 for c in value):
        return None
    parsed = urlsplit(value)
    if parsed.scheme.lower() not in ("", "https", "http", "mailto"):
        return None
    if value.startswith("//"):
        return None
    return html.escape(value, quote=True)


INLINE = re.compile(
    r"(?P<code>`(?P<code_text>[^`]+)`)|"
    r"(?P<link>\[(?P<link_text>[^\]\n]+)\]\((?P<link_url>[^\s)]+)\))|"
    r"(?P<strong>\*\*(?P<strong_text>.+?)\*\*)|"
    r"(?P<strong_under>(?<!\w)__(?P<strong_under_text>.+?)__(?!\w))|"
    r"(?P<em>\*(?P<em_text>[^*\n]+)\*)|"
    r"(?P<em_under>(?<!\w)_(?P<em_under_text>[^_\n]+)_(?!\w))"
)


def inline(text: str) -> str:
    """Render the small Markdown subset used by the canonical manuscripts.

    Raw HTML is always escaped. Link labels may contain emphasis; generated
    attributes are escaped separately. Underscores within words stay literal.
    """
    output: list[str] = []
    position = 0
    for match in INLINE.finditer(text):
        output.append(html.escape(text[position:match.start()]))
        kind = next(
            name for name in ("code", "link", "strong", "strong_under", "em", "em_under")
            if match.group(name) is not None
        )
        if kind == "code":
            output.append("<code>" + html.escape(match.group("code_text")) + "</code>")
        elif kind == "link":
            href = safe_url(match.group("link_url"))
            label = inline(match.group("link_text"))
            output.append(f'<a href="{href}">{label}</a>' if href else label)
        else:
            tag = "strong" if kind.startswith("strong") else "em"
            output.append(f"<{tag}>{inline(match.group(kind + '_text'))}</{tag}>")
        position = match.end()
    output.append(html.escape(text[position:]))
    return "".join(output)


def markdown_table(block: str) -> str | None:
    """Render a simple pipe table while keeping every cell inert."""
    lines = block.splitlines()
    if len(lines) < 3 or not all(line.strip().startswith("|") for line in lines):
        return None

    def cells(line: str) -> list[str]:
        return [cell.strip() for cell in line.strip().strip("|").split("|")]

    headers = cells(lines[0])
    divider = cells(lines[1])
    if len(headers) < 2 or len(divider) != len(headers):
        return None
    if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in divider):
        return None
    rows = [cells(line) for line in lines[2:]]
    if not rows or any(len(row) != len(headers) for row in rows):
        return None

    head = "".join(f"<th scope=\"col\">{inline(cell)}</th>" for cell in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{inline(cell)}</td>" for cell in row) + "</tr>"
        for row in rows
    )
    return (
        '<div class="prose-table-scroll" role="region" aria-label="Manuscript table" tabindex="0">'
        f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"
    )


def render_markdown(markdown: str) -> tuple[str, str | None, int]:
    """Return body HTML, the unchanged first heading, and paragraph count.

    The first heading is displayed by the reader's chapter header instead;
    its exact source label remains in originalHeading and in the raw download.
    All subsequent manuscript blocks are retained.
    """
    lines = markdown.splitlines()
    first_heading = None
    for index, line in enumerate(lines):
        if line.strip():
            if re.match(r"^#{1,6}\s+", line):
                first_heading = re.sub(r"^#{1,6}\s+", "", line)
                del lines[index]
            break
    blocks = re.split(r"\n\s*\n", "\n".join(lines).strip())
    output: list[str] = []
    paragraph_count = 0
    for block in blocks:
        if not block.strip():
            continue
        heading = re.fullmatch(r"(#{1,6})\s+(.+)", block)
        table = markdown_table(block)
        if table:
            output.append(table)
            paragraph_count += 1
        elif heading:
            level = min(6, len(heading.group(1)) + 1)
            output.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
        elif re.fullmatch(r"\s*(?:\*\s*){3,}|\s*(?:-\s*){3,}|\s*(?:_\s*){3,}", block):
            output.append("<hr>")
        elif all(line.startswith("> ") for line in block.splitlines()):
            text = "\n".join(line[2:] for line in block.splitlines())
            output.append(f"<blockquote><p>{inline(text)}</p></blockquote>")
            paragraph_count += 1
        else:
            output.append(f"<p>{inline(block)}</p>")
            paragraph_count += 1
    return "\n".join(output), first_heading, paragraph_count


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class PlainText(HTMLParser):
    """Extract readable text from the safe rendered manuscript, including title."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"p", "blockquote", "h1", "h2", "h3", "h4", "h5", "h6"}:
            self.parts.append("\n\n")
        elif tag in {"th", "td"}:
            self.parts.append("\t")
        elif tag == "tr":
            self.parts.append("\n")

    def result(self) -> str:
        return re.sub(r"\n{3,}", "\n\n", "".join(self.parts)).strip()
