"""Assemble Cold Rice review artifacts from existing source and artwork; no external writes."""
import difflib
import hashlib
import json
from pathlib import Path
from urllib.parse import urlencode, urlsplit, urlunsplit

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parents[1]
REPO = Path(r"C:\Users\Administrator\OneDrive\Desktop\.json book\json_under_revision_v2")
CHAPTER = REPO / "chapters/com-nguoi"
LIBRARY = Path(r"E:\books\.json\outputs\json-digital-book-assets")
EXPECTED_SOURCE = "d957b592dc2317aa34196dd25ab42a3fe4a7938d3aee5a1121ab173214bf76f9"
REMOTE_HEAD = "3ceecb11076ccf50a58e26d093b0dc0c97e41051"


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def write(name, value):
    (HERE / name).write_text(value, encoding="utf-8", newline="\n")


def save(name, value):
    write(name, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def link(label, path):
    return f"[{label}](<{Path(path).as_posix()}>)"


def main():
    if (HERE / "editorial-approval.json").exists():
        raise RuntimeError("Approved review package is frozen; use a new version instead of regenerating it.")
    source_path = CHAPTER / "source/approved.md"
    source_bytes = source_path.read_bytes()
    source = source_bytes.decode("utf-8")
    source_lines = source.splitlines()
    if sha(source_path) != EXPECTED_SOURCE:
        raise ValueError("Source changed; review lineage before rebuilding")
    registry = json.loads((CHAPTER / "chapter.json").read_text(encoding="utf-8"))
    if registry["manuscript_sha256"] != EXPECTED_SOURCE:
        raise ValueError("Registry/source mismatch")
    before = {str(p): sha(p) for p in (source_path, CHAPTER / "chapter.json", CHAPTER / "production.json", CHAPTER / "source/original.md")}

    # Two explicitly proposed changes; the existing selected manuscript is never edited.
    proposed = source.replace(
        "các cậu sẽ hơi ngạc nhiên khi thấy tớ luôn chọn cơm nguội",
        "các cậu sẽ hơi ngạc nhiên. Tớ luôn chọn cơm nguội", 1
    ).replace("bữa trước. Nhưng cứ thế", "bữa trước.\n\nNhưng cứ thế", 1)
    if proposed == source:
        raise ValueError("Expected editorial changes not found")
    write("chapter-proposed-v1.md", proposed)
    write("chapter-proposed-v1.diff", "".join(difflib.unified_diff(source.splitlines(True), proposed.splitlines(True), fromfile="existing-author-selected/approved.md", tofile="proposed-v1/pending-author-approval.md")))

    catalog_path = LIBRARY / "assets-manifest.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    art = next(c for c in catalog["chapters"] if c["slug"] == "com-nguoi")
    runtime = json.loads((LIBRARY / "integration/runtime-asset-map.json").read_text(encoding="utf-8"))
    runtime_art = next(c for c in runtime["chapters"] if c["slug"] == "com-nguoi")
    records, issues = [], []

    def check(record, role):
        path = LIBRARY / record["path"]
        if not path.resolve().is_relative_to(LIBRARY.resolve()):
            raise ValueError("Asset reference escapes library")
        exists = path.is_file()
        digest = sha(path) if exists else None
        matches = exists and digest == record["sha256"] and path.stat().st_size == record["bytes"]
        result = {"role": role, "path": str(path), "sha256": digest, "catalog_sha256": record["sha256"], "matches_catalog": matches, "width_catalog": record.get("width"), "height_catalog": record.get("height")}
        records.append(result)
        if not matches:
            issues.append(result)
        return path

    roles = {}
    for role, value in art["roles"].items():
        roles[role] = check(value["web"], role + "/web")
        check(value["master"], role + "/master")
        rt = runtime_art["roles"][role]
        if rt["src"] != value["web"]["path"] or rt["version"] != value["web"]["sha256"][:12]:
            issues.append({"role": role, "reason": "Runtime path/cache version mismatch"})
    for kind, items in art.get("content_assets", {}).items():
        for item in items:
            check(item, "content/" + kind)
    shared = []
    for key, rel in catalog["shared"].items():
        path = LIBRARY / rel
        shared.append({"role": key, "path": str(path), "exists": path.is_file(), "sha256": sha(path) if path.is_file() else None})
        if not path.is_file():
            issues.append({"role": key, "reason": "Missing shared reference"})
    legacy = []
    for rel in ["audio/NARRATION.md", "audio/HANDOFF.md", "audio/reading-script.md", "audio/ambience.wav", "video/timeline.json", "video/STORYBOARD.md", "video/discovery-9x16.mp4", "video/feed-3x4.mp4", "video/youtube-9x16.mp4", "book/chapter-A5-proof.pdf", "web/index.html"] + [f"social/instagram/slide-{i:02}.jpg" for i in range(1, 6)]:
        path = CHAPTER / rel
        legacy.append({"path": str(path), "exists": path.is_file(), "sha256": sha(path) if path.is_file() else None, "status": "existing reference/proof; not newly release-approved"})
    mapping = json.loads((REPO / "shared/assets.json").read_text(encoding="utf-8"))
    installed = [a for a in mapping["assets"] if "com-nguoi" in str(a)]
    save("asset-reuse.json", {"date": "2026-10-21", "chapter_slug": "com-nguoi", "library_root": str(LIBRARY), "catalog_sha256": sha(catalog_path), "assets_checked": records, "shared_references": shared, "existing_products": legacy, "local_reader_mappings": installed, "issues": issues, "assets_copied": 0, "images_generated": 0, "new_layout_exports": "v2 review adaptations only", "rights_approval": "pending", "verification_scope": "Catalog existence/bytes/SHA plus principal runtime versions; separate fresh visual review of chapter proof and new exports; not deployment or full library QA"})
    index = ["# Cold Rice — linked existing assets", "", "No source artwork copied or regenerated. New social layouts adapt these existing files.", "", "| Role | Existing file | Catalog SHA verified |", "|---|---|---|"]
    for rec in records:
        index.append(f"| {rec['role']} | {link(Path(rec['path']).name, rec['path'])} | {rec['matches_catalog']} |")
    index.extend(["", "## Existing production references", ""])
    index.extend("- " + link(Path(item["path"]).name, item["path"]) + " — proof/reference, current release not approved" for item in legacy)
    index.extend(["", "## Shared book files", ""])
    index.extend("- " + link(item["role"], item["path"]) for item in shared)
    index.extend(["", f"Checked {len(records)} catalog files and {len(shared)} shared references. Issues: {len(issues)}. Master/catalog hashes do not establish rights, final crop approval, or live-site behavior."])
    write("asset-reuse.md", "\n".join(index) + "\n")
    if issues:
        raise ValueError(f"Asset audit requires review: {len(issues)} issues")

    def quote(text, line):
        if text not in source_lines[line - 1]:
            raise ValueError(f"Quote does not match source line {line}: {text}")
        return {"text": text, "line": line, "path": str(source_path), "source_sha256": EXPECTED_SOURCE}

    bowl = LIBRARY / "chapters/com-nguoi/artwork/content/elements/03-rice-bowl-and-steam.png"
    beat_specs = [
        (5, "Nó không phải sở thích.", 5, bowl, "Bowl illustration; title supplies context", "Cơm nguội", "quiet curiosity"),
        (6, "Cơm nguội gắn liền với thời thơ ấu của tớ.", 7, roles["reader_hero"], "Whole family illustration", "", "recollection"),
        (11, "Tớ để ý bố luôn là người ăn hết tô cơm ấy, còn phần cơm nóng thì để mẹ và tớ ăn.", 9, roles["reader_hero"], "Full family table, no forced portrait crop", "", "observation"),
        (6, "Tớ không muốn bố phải ăn cơm nguội.", 11, roles["inline_illustration"], "Child and parents illustration", "", "care, understated"),
        (11, "Thế nên cứ mỗi bữa, tớ lại giành lấy phần cơm ấy, bảo rằng tớ thích ăn cơm nguội hơn.", 13, roles["inline_illustration"], "Small framing move; no staged exchange", "", "remembered choice"),
        (4, "Cho đến tận bây giờ.", 15, roles["chapter_opening"], "Return to full portal", "", "time bridge"),
        (6, "“Con thích ăn cơm nguội.”", 21, roles["reader_hero"], "Still family illustration", "", "restraint"),
        (5, "", None, roles["chapter_opening"], "Silent beat then title/CTA slate", ".json / Cơm nguội · Đọc trọn chương", "quiet invitation"),
    ]

    def segment(number, start, duration, text, line, path, visual, on_screen, emotion):
        ref = quote(text, line) if line else None
        return {"segment_id": f"B{number:02}", "start_estimate_s": start, "duration_estimate_s": duration, "vo_text": text, "source_excerpt_or_adaptation": "verbatim excerpt" if line else "marketing slate; silent, outside memoir", "source_reference": ref, "visual": visual, "asset_path": str(path), "asset_sha256": sha(path), "on_screen_text": on_screen, "subtitle_notes": "Actual VO only; at most two readable lines; retime after real recording", "emotion": emotion, "rights_notes": "Existing illustrative artwork; public/commercial rights and author visual approval pending; not archival photography", "status": "ready_for_review"}

    segments, start = [], 0
    for i, (duration, text, line, path, visual, on_screen, emotion) in enumerate(beat_specs, 1):
        segments.append(segment(i, start, duration, text, line, path, visual, on_screen, emotion))
        start += duration
    alternate, start = [], 0
    for n, index_, duration in [(1, 0, 4), (2, 3, 6), (3, 6, 4), (4, 7, 4)]:
        _, text, line, path, visual, on_screen, emotion = beat_specs[index_]
        alternate.append(segment(n, start, duration, text, line, path, visual, on_screen, emotion))
        start += duration
    save("film-script.json", {"version": "v1", "source_path": str(source_path), "source_sha256": EXPECTED_SOURCE, "status": "ready_for_review", "timing_status": "estimates until author recording", "author_vo_recorded": False, "script_facts_approved": False, "master_duration_estimate_s": 54, "alternate_duration_estimate_s": 18, "master": segments, "alternate": alternate})

    card_specs = [
        ("Nó không phải sở thích.", 5, roles["main_book"], "Minh họa cổng giấy nhiều lớp dẫn vào bàn ăn gia đình."),
        ("Cơm nguội gắn liền với thời thơ ấu của tớ.", 7, roles["reader_hero"], "Minh họa ba người bên bàn ăn dưới đèn vàng, nhìn từ phía sau."),
        ("Tớ không muốn bố phải ăn cơm nguội.", 11, roles["inline_illustration"], "Minh họa đứa trẻ và bố mẹ bên bàn ăn có tô cơm."),
        ("Cho đến tận bây giờ.", 15, roles["reader_hero"], "Minh họa gia đình quanh bàn ăn."),
        ("“Con thích ăn cơm nguội.”", 21, roles["chapter_opening"], "Minh họa Jason đứng ở ngưỡng cổng giấy, bàn ăn gia đình ở phía trong."),
    ]
    social_dir = HERE / "social"
    social_dir.mkdir(exist_ok=True)
    fonts = REPO / "shared/fonts"
    body_font = ImageFont.truetype(str(fonts / "Noto-Serif.ttf"), 58)
    # The supplied DM Sans file lacks some Vietnamese glyphs; use the existing
    # Noto Serif for every Vietnamese label as well as the quoted body text.
    label_font = ImageFont.truetype(str(fonts / "Noto-Serif.ttf"), 27)
    brand_font = ImageFont.truetype(str(fonts / "Noto-Serif-Italic.ttf"), 66)
    navy, paper = "#14313D", "#F1EBDD"

    def wrap(draw, text, font, width):
        lines, current = [], ""
        for word in text.split():
            test = (current + " " + word).strip()
            if draw.textlength(test, font=font) > width and current:
                lines.append(current)
                current = word
            else:
                current = test
        return lines + ([current] if current else [])

    def place(canvas, path, box):
        with Image.open(path) as original:
            resized = ImageOps.contain(original.convert("RGBA"), (box[2], box[3]), Image.Resampling.LANCZOS)
        x = box[0] + (box[2] - resized.width) // 2
        y = box[1] + (box[3] - resized.height) // 2
        canvas.paste(resized, (x, y), resized)

    carousel = []
    for n, (text, line, path, alt) in enumerate(card_specs, 1):
        q = quote(text, line)
        canvas = Image.new("RGB", (1080, 1440), paper)
        draw = ImageDraw.Draw(canvas)
        draw.rectangle((36, 36, 1044, 1404), outline=navy, width=2)
        draw.text((72, 56), ".json", font=brand_font, fill=navy)
        draw.text((852, 88), f"00 / {n:02}", font=label_font, fill=navy)
        place(canvas, path, (70, 180, 940, 650))
        y = 892
        for part in wrap(draw, text, body_font, 920):
            draw.text((72, y), part, font=body_font, fill=navy)
            y += 88
        if y > 1260:
            raise ValueError("Carousel text exceeds safe text region")
        if n == 5:
            draw.text((72, 1268), "Đọc trọn Cơm nguội", font=label_font, fill=navy)
        draw.text((72, 1348), "Cơm nguội / Prologue 00", font=label_font, fill=navy)
        target = social_dir / f"carousel-{n:02}.jpg"
        canvas.save(target, quality=94, subsampling=0)
        carousel.append({"id": f"carousel-{n:02}", "quote": q, "source_art_path": str(path), "source_art_sha256": sha(path), "output": str(target), "sha256": sha(target), "dimensions": [1080, 1440], "alt_text": alt + " Chữ: " + text + (" CTA: Đọc trọn Cơm nguội." if n == 5 else ""), "status": "ready_for_review"})
    contact = Image.new("RGB", (1640, 896), "#DAD4C8")
    for n in range(5):
        with Image.open(social_dir / f"carousel-{n+1:02}.jpg") as card:
            thumb = card.resize((300, 400), Image.Resampling.LANCZOS)
            contact.paste(thumb, (20 + (n % 3) * 540, 20 + (n // 3) * 440))
    contact.save(HERE / "social-contact-sheet.jpg", quality=93)

    # A wide image and a story image adapt existing art, without manufacturing new scenes.
    fb = Image.new("RGB", (1200, 630), paper)
    place(fb, roles["reader_hero"], (24, 24, 825, 550))
    draw = ImageDraw.Draw(fb)
    for y, text in [(110, "Cơm nguội"), (184, ".json"), (312, "Đọc trọn chương")]:
        draw.text((875, y), text, font=ImageFont.truetype(str(fonts / "Noto-Serif.ttf"), 28), fill=navy)
    fb.save(social_dir / "facebook-image-v1.jpg", quality=94, subsampling=0)
    story = Image.new("RGB", (1080, 1920), paper)
    place(story, roles["chapter_opening"], (60, 260, 960, 960))
    draw = ImageDraw.Draw(story)
    draw.text((72, 165), "Cơm nguội / .json", font=label_font, fill=navy)
    for i, text in enumerate(wrap(draw, card_specs[4][0], body_font, 900)):
        draw.text((72, 1260 + i * 88), text, font=body_font, fill=navy)
    draw.text((72, 1530), "Đọc trọn Cơm nguội", font=label_font, fill=navy)
    story.save(social_dir / "story-image-v1.jpg", quality=94, subsampling=0)

    book = json.loads((REPO / "book.json").read_text(encoding="utf-8"))
    base = book["public_url"]
    def campaign_url(channel, creative):
        u = urlsplit(base)
        return urlunsplit((u.scheme, u.netloc, u.path, urlencode({"utm_source": channel, "utm_medium": "organic_social", "utm_campaign": "com-nguoi-20261021", "utm_content": creative}), registry["canonical_path"].removeprefix("#")))

    captions = {
        "instagram": "Nó không phải sở thích.\n\nCơm nguội gắn liền với thời thơ ấu của tớ.\n\nCơm nguội — prologue 00 trong .json.\nĐọc trọn chương qua liên kết ở hồ sơ.\n\n#ComNguoi #json #HoiUc",
        "facebook": "Cơm nguội gắn liền với thời thơ ấu của tớ.\n\nTớ không muốn bố phải ăn cơm nguội.\n\nThế nên cứ mỗi bữa, tớ lại giành lấy phần cơm ấy, bảo rằng tớ thích ăn cơm nguội hơn.\n\nCơm nguội / .json\nĐọc trọn chương: " + campaign_url("facebook", "image-v1"),
        "tiktok": "Nó không phải sở thích.\n\nCơm nguội / .json\nĐọc trọn chương qua liên kết ở hồ sơ.\n\n#ComNguoi #json #HoiUc",
        "youtube": "Nó không phải sở thích.\n\nMột trích đoạn từ Cơm nguội, prologue 00 trong .json.\nBản đầy đủ của chương ở liên kết hồ sơ kênh.\n\n#ComNguoi #json",
        "sunday": "Cho đến tận bây giờ.\n\n“Con thích ăn cơm nguội.”\n\nCơm nguội / .json\nĐọc trọn chương qua liên kết ở hồ sơ.",
    }
    channels = []
    for channel, text in captions.items():
        creative = "carousel-v1" if channel == "instagram" else "image-v1" if channel == "facebook" else "alternate-v1" if channel == "sunday" else "master-v1"
        channels.append({"channel": channel, "creative_id": creative, "caption": text, "candidate_destination": campaign_url(channel, creative), "destination_live_verified": False, "profile_link_verified": False, "schedule": None, "published_url": None, "owner": "Jason", "status": "ready_for_review", "source_sha256": EXPECTED_SOURCE, "cta_dependency": "Use profile CTA only after actual channel link is configured and verified; all destinations need G3", "metrics": {"views": None, "clicks": None, "reads": None}})
        write(f"social/{channel}-caption.txt", text + "\n")
    save("social-pack.json", {"version": "v1", "source_sha256": EXPECTED_SOURCE, "campaign": "com-nguoi-20261021", "status": "ready_for_review", "author_approval": False, "carousel": carousel, "channels": channels, "youtube_link_policy_source": "https://support.google.com/youtube/answer/13748639?hl=en", "illustration_provenance": "Existing author asset library; AI illustration, not archival photograph", "music_rights": "no new music selected", "published": False})

    lineage = {"date": "2026-10-21", "timezone": "Asia/Bangkok", "repository": "https://github.com/jasonthedataguy/json-under-revision-v2", "remote_default_branch": "main", "remote_head_observed": REMOTE_HEAD, "local_head": (REPO / ".git/refs/heads/main").read_text().strip(), "canonical_source": str(source_path), "canonical_source_sha256": EXPECTED_SOURCE, "canonical_bytes": len(source_bytes), "registry_hash_matches": True, "historical_editorial_approval_evidence": str(CHAPTER / "source/edit-notes.md"), "new_proposal": str(HERE / "chapter-proposed-v1.md"), "new_proposal_sha256": sha(HERE / "chapter-proposed-v1.md"), "proposal_approved": False, "derivative_basis": "existing selected source; new proposal not adopted", "original_source_unchanged": True, "book_repository_files_unchanged": True}
    for path, digest in before.items():
        if sha(Path(path)) != digest:
            raise ValueError("Book repository file changed unexpectedly")
    save("source-lineage.json", lineage)

    manifest = json.loads((PACKAGE / "templates/run-manifest.json").read_text(encoding="utf-8"))
    manifest.update({"story_id": "com-nguoi", "chapter_slug": "com-nguoi", "chapter_slot": "00", "original_edition_slot": "07", "title": "Cold Rice / Cơm nguội", "run_mode": "audit + next actions", "canonical_source_path": str(source_path), "canonical_sha256": EXPECTED_SOURCE, "author_approved": False, "source_facts_approval_evidence": None, "approval_scope_note": "Historical selected text approval exists; author_approved=false refers to this run's new proposal/facts-disclosure gate, not a claim that existing text was never selected.", "historical_editorial_approval_evidence": str(CHAPTER / "source/edit-notes.md"), "proposed_manuscript_path": str(HERE / "chapter-proposed-v1.md"), "proposed_sha256": lineage["new_proposal_sha256"], "run_date": "2026-10-21", "timezone": "Asia/Bangkok", "repository_head_observed": REMOTE_HEAD, "reader_candidate_url": base + registry["canonical_path"], "jira_sync_status": "not performed; connector unavailable", "originals_unchanged": True, "approval_gates": {g: {"status": "pending", "evidence": None} for g in ["G1", "script", "G2", "G3", "G4", "G5"]}})
    for stage in manifest["stages"]:
        manifest["stages"][stage] = "ready_for_review"
    manifest["stages"].update({"S04_digital_reader": "in_progress", "S06_audio_film": "blocked", "S09_commerce": "blocked", "S10_release": "blocked", "S11_learning": "not_started"})
    files_by_stage = {"S00_intake": "story-brief.md", "S01_editorial_diagnosis": "editorial-review.md", "S02_canonical": "chapter-proposed-v1.md", "S03_narration_script": "film-script.json", "S04_digital_reader": "digital-book-design-plan.md", "S05_design": "asset-reuse.json", "S06_audio_film": "film-script.md", "S07_campaign_assets": "social-pack.json", "S08_product_strategy": "monetization-options.md", "S09_commerce": "monetization-options.md", "S10_release": "production-plan.md", "S11_learning": "production-plan.md"}
    manifest["stage_evidence"] = {stage: {"path": str(HERE / name), "sha256": sha(HERE / name), "scope": "internal artifact/status evidence; not release approval"} for stage, name in files_by_stage.items()}
    derivative_files = ["chapter-proposed-v1.md", "chapter-proposed-v1.diff", "editorial-review.md", "story-brief.md", "film-script.md", "film-script.json", "social-pack.md", "social-pack.json", "digital-book-design-plan.md", "monetization-options.md", "social-contact-sheet.jpg"] + [str(p.relative_to(HERE)) for p in social_dir.iterdir() if p.suffix in (".jpg", ".txt")]
    manifest["derivatives"] = [{"id": Path(name).stem, "path": str(HERE / name), "source_sha256": EXPECTED_SOURCE, "artifact_sha256": sha(HERE / name), "version": "v1", "format": Path(name).suffix.removeprefix("."), "rights": "public/commercial approval pending; existing illustrative artwork referenced in metadata", "status": "ready_for_review", "evidence": str(HERE / name)} for name in derivative_files]
    manifest["blockers"] = [{"id": "G1", "owner": "Jason", "reason": "Review proposed text versus retain-current choice, facts/public family scope and exact first-person script."}, {"id": "VO", "owner": "Jason then editor/AI", "reason": "Real author take, retimed film/subtitles and playback approval required."}, {"id": "LIVE", "owner": "Technical owner + Jason", "reason": "Live chapter/CTA, accessibility, rights and final G3 not yet verified/approved."}, {"id": "G4", "owner": "Jason", "reason": "Optional commerce: no selected offer or actual checkout/fulfillment/terms tests."}]
    manifest["offer_hypotheses"] = [{"id": "H1", "name": "Illustrated digital mini-edition", "validated": False}, {"id": "H2", "name": "Art print/postcard pair", "validated": False}, {"id": "H3", "name": "Collection/publisher licensing", "validated": False}]
    manifest["observed_metrics"] = {"reach": None, "visits": None, "reads": None, "onward_clicks": None, "subscribers": None, "paid_units": None, "net_sales_vnd": None, "contribution_vnd": None}
    manifest["next_actions"] = [{"priority": 1, "owner": "Jason", "action": "Review exact proposed text/script and family scope", "dependency": "review packet prepared", "effort_estimate": "20–30 minutes", "jira_path": "historical JSON-18/44; current mapping unverified"}, {"priority": 2, "owner": "Jason then editor/AI", "action": "Record real VO and retime/export/QC film", "dependency": "approved script", "effort_estimate": "20–40 minutes recording, 2–4 hours edit/QA", "jira_path": "historical JSON-44/81; current mapping unverified"}, {"priority": 3, "owner": "Technical owner + Jason", "action": "Verify deployed reader/CTA/mobile then approve exact G2/G3 package", "dependency": "selected source/final media", "effort_estimate": "1–2 hours excluding fixes", "jira_path": "historical JSON-102/103/105; current mapping unverified"}]
    manifest["notes"] = "Review package complete; production/release cycle remains open. Existing prose/art/media referenced, canonical source untouched, no film recording/public release/paid offer/Jira update claimed. All author gates pending for this run."
    save("run-manifest.json", manifest)

    readme = ["# Cold Rice — review package", "", "Prepared 21 October 2026. Original voice and selected source preserved; no source, reader, Jira or public release changed. Existing art is linked from E:; seven new social review layouts adapt it because legacy cards show Chapter 07.", "", "| Requested result | Review artifact |", "|---|---|"]
    for label, name in [("Refined chapter, pending G1", "chapter-proposed-v1.md"), ("Exact two-change comparison", "chapter-proposed-v1.diff"), ("Editorial review / voice boundaries", "editorial-review.md"), ("54s + 18s film script", "film-script.md"), ("Digital-book reuse/design update", "digital-book-design-plan.md"), ("Captions, carousel, image/essay and replies", "social-pack.md"), ("Three unvalidated monetization options", "monetization-options.md"), ("Updated local production plan", "production-plan.md"), ("Existing asset links and proof states", "asset-reuse.md"), ("Source/hash lineage", "source-lineage.json"), ("Stage/gate manifest", "run-manifest.json")]:
        readme.append(f"| {label} | {link(name, HERE / name)} |")
    readme.extend(["", "## Social review exports", ""])
    readme.extend("- " + link(p.name, p) for p in sorted(social_dir.glob("*.jpg")))
    readme.extend(["", "First decision: approve the exact proposed text or retain the selected source, review abridged script and confirm public family scope. G2/G3 need actual author narration/final media and live reader/CTA/rights QA; G4 is separate for any paid offer. Nothing is scheduled, posted, charged or narrated synthetically.", "", "The configured reader target has not been verified live. Old archive captions and Chapter 07 exports remain historical. Jira keys in the plan are unverified references; no ticket was updated. Current outputs are in this writable workspace; all existing E: artwork remains in place."])
    write("README.md", "\n".join(readme) + "\n")
    print(json.dumps({"status": "assembled_for_review", "source_sha256": EXPECTED_SOURCE, "catalog_files_verified": len(records), "shared_references": len(shared), "local_reader_mapping_count": len(installed), "social_layouts": len(list(social_dir.glob("*.jpg"))), "source_unchanged": True, "output": str(HERE)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
