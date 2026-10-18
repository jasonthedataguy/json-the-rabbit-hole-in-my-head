#!/usr/bin/env python3
"""Import approved manuscripts from the pinned original repository.

Usage: python3 scripts/import_reference.py /path/to/json-under-revision
Only the Python standard library is required. The source checkout is read-only.
"""

from __future__ import annotations

import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import quote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "content/reference-map.json"
PUBLIC_ARCHIVE = "https://jasonthedataguy.github.io/json-under-revision/"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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
        if heading:
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

    def result(self) -> str:
        return re.sub(r"\n{3,}", "\n\n", "".join(self.parts)).strip()


def import_reference(source_root: Path) -> dict:
    mapping = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    commit = mapping["sourceCommit"]
    current_commit = subprocess.check_output(
        ["git", "-C", str(source_root), "rev-parse", "HEAD"], text=True
    ).strip()
    if current_commit != commit:
        raise ValueError(f"Source must be checked out at {commit}; found {current_commit}")
    source = {
        "repo": mapping["sourceRepo"],
        "commit": commit,
        "url": mapping["sourceRepo"] + "/tree/" + commit,
    }
    entries = []
    provenance = []
    seen_editorial_ids: set[str] = set()
    for item in mapping["chapters"]:
        slug = item["slug"]
        metadata_path = Path("chapters") / slug / "chapter.json"
        metadata_bytes = (source_root / metadata_path).read_bytes()
        metadata = json.loads(metadata_bytes)
        if not metadata.get("publish"):
            raise ValueError(f"Cannot import unpublished chapter {slug}")
        manuscript_path = metadata_path.parent / metadata["canonical_text"]
        if manuscript_path.as_posix() != item["manuscriptPath"]:
            raise ValueError(f"Canonical path changed for {slug}")
        manuscript = (source_root / manuscript_path).read_bytes()
        digest = sha256(manuscript)
        if digest != item["manuscriptSha256"] or len(manuscript) != item["manuscriptBytes"]:
            raise ValueError(f"Canonical manuscript bytes changed for {slug}")
        editorial_id = item["portalId"]
        if editorial_id is not None:
            if editorial_id in seen_editorial_ids:
                raise ValueError(f"Duplicate portal assignment {editorial_id}")
            seen_editorial_ids.add(editorial_id)
        markdown = manuscript.decode("utf-8")
        body, original_heading, paragraph_count = render_markdown(markdown)
        full_html = (f"<h2>{inline(original_heading)}</h2>\n" if original_heading else "") + body
        plain_text = PlainText()
        plain_text.feed(full_html)
        local_dir = ROOT / "content/chapters" / slug
        local_dir.mkdir(parents=True, exist_ok=True)
        (local_dir / "approved.md").write_bytes(manuscript)
        (local_dir / "chapter.json").write_bytes(metadata_bytes)
        public_path = Path("content/manuscripts") / (slug + ".md")
        download_path = ROOT / "dist" / public_path
        download_path.parent.mkdir(parents=True, exist_ok=True)
        download_path.write_bytes(manuscript)
        entry = {
            "slug": slug,
            "editorialId": editorial_id,
            "legacyId": metadata["number"],
            "originalTitle": metadata["title"],
            "title": metadata["title"],
            "originalHeading": original_heading,
            "language": metadata.get("language", "vi"),
            "subtitle": metadata.get("subtitle", ""),
            "html": full_html,
            "bodyHtml": body,
            "plainText": plain_text.result(),
            "paragraphCount": paragraph_count,
            "sourcePath": (local_dir / "approved.md").relative_to(ROOT).as_posix(),
            "originalSourcePath": manuscript_path.as_posix(),
            "originalMetadataPath": metadata_path.as_posix(),
            "sha256": digest,
            "bytes": len(manuscript),
            "archiveUrl": PUBLIC_ARCHIVE + metadata["canonical_path"],
            "downloadUrl": public_path.as_posix(),
            "sourceUrl": mapping["sourceRepo"] + "/blob/" + commit + "/" + quote(manuscript_path.as_posix()),
        }
        entries.append(entry)
        provenance.append({
            key: entry[key]
            for key in ("slug", "editorialId", "legacyId", "originalTitle", "originalHeading", "sourcePath", "originalSourcePath", "sha256", "bytes", "archiveUrl")
        } | {
            "localPath": (local_dir / "approved.md").relative_to(ROOT).as_posix(),
            "metadataSourcePath": metadata_path.as_posix(),
            "metadataSha256": sha256(metadata_bytes),
            "matchEvidence": item["matchEvidence"],
        })
        if (local_dir / "approved.md").read_bytes() != manuscript:
            raise ValueError(f"Local manuscript copy failed verification for {slug}")
        if download_path.read_bytes() != manuscript:
            raise ValueError(f"Published download failed verification for {slug}")
    published_slugs = {
        path.parent.name
        for path in (source_root / "chapters").glob("*/chapter.json")
        if json.loads(path.read_text(encoding="utf-8")).get("publish")
    }
    imported_slugs = {item["slug"] for item in entries}
    if published_slugs != imported_slugs:
        raise ValueError(f"Published chapter coverage mismatch: {published_slugs ^ imported_slugs}")
    result = {"source": source, "chapters": entries}
    write_json(ROOT / "dist/content/manuscripts.json", result)
    write_json(ROOT / "docs/source-provenance.json", {
        "source": source,
        "policy": "Approved canonical manuscripts and chapter metadata copied byte-for-byte; all ten published canonical texts are included. Editorial portal IDs follow the supplied atlas mapping, independently of the source repository's chapter numbers. Dating 102 is an additional archive chapter without an atlas assignment. Full html and plainText retain the first Markdown heading; bodyHtml omits only this heading because the reader displays originalTitle above it. Raw downloads retain all source bytes unchanged.",
        "publishedManuscripts": len(entries),
        "assignedPortalManuscripts": len(seen_editorial_ids),
        "additionalArchiveManuscripts": len(entries) - len(seen_editorial_ids),
        "manuscriptBytes": sum(item["bytes"] for item in entries),
        "chapters": provenance,
    })
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Original repository checkout at the pinned source commit")
    args = parser.parse_args()
    result = import_reference(args.source.resolve())
    entries = result["chapters"]
    print(json.dumps({
        "chapters": len(entries),
        "assigned": sum(item["editorialId"] is not None for item in entries),
        "archiveOnly": [item["slug"] for item in entries if item["editorialId"] is None],
        "paragraphs": sum(item["paragraphCount"] for item in entries),
        "bytes": sum(item["bytes"] for item in entries),
        "sourceCommit": result["source"]["commit"],
        "byteVerification": "passed",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
