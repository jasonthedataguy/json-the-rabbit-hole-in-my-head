"""One-time, local studio setup. Existing book/art sources stay in place."""
import hashlib
import json
import shutil
import zipfile
import xml.etree.ElementTree as ET
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STUDIO = ROOT / "studio"
BOOK = Path(r"C:\Users\Administrator\OneDrive\Desktop\.json book\json_under_revision_v2")
ART = Path(r"E:\books\.json\outputs\json-digital-book-assets")
LEGACY = ROOT / "json_video_studio_codex/json_video_studio"
VIDEO = STUDIO / "apps/video"


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"Refusing to replace existing studio record: {path}")
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def move(source, target):
    for path in (source, target):
        if not path.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError(f"Move outside workspace: {path}")
    if target.exists():
        raise FileExistsError(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(target))


def main():
    if (STUDIO / "studio.json").exists():
        raise RuntimeError("Studio already initialized; use scripts/studio.py for ongoing work")
    legacy_manifest = json.loads((LEGACY / "manifests/chapters.json").read_text(encoding="utf-8"))
    original_assets = {p.relative_to(ROOT).as_posix(): sha(p) for p in LEGACY.rglob("*") if p.is_file() and p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")}
    book = json.loads((BOOK / "book.json").read_text(encoding="utf-8"))
    art = json.loads((ART / "assets-manifest.json").read_text(encoding="utf-8"))
    # Preserve original text/code as a small reference archive, without copying art.
    archive = STUDIO / "references/video-starter/original-code-v0.1.zip"
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, "x", zipfile.ZIP_DEFLATED) as z:
        for p in LEGACY.rglob("*"):
            if p.is_file() and p.suffix.lower() in (".md", ".json", ".ts", ".tsx"):
                z.write(p, p.relative_to(LEGACY).as_posix())
    move(LEGACY, VIDEO)
    relocation = [{"from": "json_video_studio_codex/json_video_studio", "to": "studio/apps/video"}]
    for name in ("chapters", "assets", "public", "docs"):
        move(VIDEO / name, STUDIO / "references/video-starter" / name)
        relocation.append({"from": "studio/apps/video/" + name, "to": "studio/references/video-starter/" + name})
    move(VIDEO / "manifests/chapters.json", STUDIO / "references/video-starter/concepts.legacy.json")
    relocation.append({"from": "studio/apps/video/manifests/chapters.json", "to": "studio/references/video-starter/concepts.legacy.json"})

    config = {
        "schema_version": "1.0", "name": ".json Studio", "timezone": "Asia/Bangkok",
        "workspace_root": "..", "book_repository": str(BOOK), "asset_library": str(ART),
        "video_app": "studio/apps/video", "strategy_deck": "json_video_design_strategy_deck.pptx",
        "legacy_video_reference_root": "studio/references/video-starter",
        "style": "studio/apps/video/manifests/style.json", "projects": "studio/projects",
        "catalog": "studio/catalog/stories.json", "cache": "studio/.cache", "reports": "studio/reports",
        "run_manifest_schema": "templates/run-manifest.json", "default_visibility": "private",
        "pilot_order": ["com-nguoi", "fashion", "viet-cho-sai-gon-cua-t"],
        "release_policy": "Exact author approval by scope/version; this workspace contains no publisher or payment action",
    }
    save(STUDIO / "studio.json", config)
    aliases = {"quant": "i-was-born-a-quant", "russia": "for-mother-russia", "cold-rice": "com-nguoi", "little-planet": "tieu-hanh-tinh", "three-meetings": "three-meeting-theory", "to-saigon": "viet-cho-sai-gon-cua-t"}
    alias_rows = []
    for row in legacy_manifest:
        slug = aliases.get(row["slug"], row["slug"])
        identity = {"legacy_working_id": row["id"], "legacy_slug": row["slug"], "legacy_directory": f'{row["id"]}-{row["slug"]}', "canonical_slug": slug, "legacy_hook_status": "unapproved ideation; never automatically used as memoir"}
        if row["board"]:
            identity["board_reference"] = "studio/references/video-starter/" + row["board"]
        else:
            identity["board_reference"] = None
            identity["missing_legacy_board_is_not_missing_current_art"] = True
        alias_rows.append(identity)
    save(STUDIO / "catalog/legacy-video-aliases.json", {"schema_version": "1.0", "aliases": alias_rows})

    pilot_rows = []
    for slug in config["pilot_order"]:
        directory = STUDIO / "projects" / slug
        meta = json.loads((BOOK / "chapters" / slug / "chapter.json").read_text(encoding="utf-8"))
        source = BOOK / "chapters" / slug / meta["canonical_text"]
        run_path = ROOT / "outputs/2026-10-21-com-nguoi/run-manifest.json" if slug == "com-nguoi" else directory / "run-manifest.json"
        if slug != "com-nguoi":
            run = json.loads((ROOT / "templates/run-manifest.json").read_text(encoding="utf-8"))
            run.update({"story_id": slug, "chapter_slug": slug, "chapter_slot": meta["number"], "title": meta["title"], "run_mode": "audit", "canonical_source_path": str(source), "canonical_sha256": sha(source), "release_scope": {"surfaces": ["reader", "film", "social"]}, "notes": "Pilot queue only. Selected source exists in registry; no author approval inferred. No new prose/script/media produced."})
            run["stages"]["S00_intake"] = "in_progress"
            run["stage_evidence"]["S09_commerce"] = {"reason": "No paid experiment selected; optional lane deferred."}
            save(run_path, run)
        project = {"schema_version": "1.0", "story_slug": slug, "title": meta["title"], "edition_number": meta["number"], "original_edition_number": meta.get("original_edition", {}).get("number"), "source": {"path": str(source), "sha256": sha(source)}, "run_manifest": run_path.relative_to(ROOT).as_posix(), "asset_record": str(ART / "chapters" / slug / "assets.json"), "timeline": f"studio/projects/{slug}/video/timeline.json" if slug == "com-nguoi" else None, "lanes": {"editorial": str(BOOK / "chapters" / slug / "source"), "reader": str(BOOK / "chapters" / slug / "web"), "design": str(ART / "chapters" / slug / "assets.json"), "audio": str(BOOK / "chapters" / slug / "audio"), "video": f"studio/projects/{slug}/video", "social": str(ROOT / "outputs/2026-10-21-com-nguoi/social-pack.json") if slug == "com-nguoi" else None, "commerce": str(ROOT / "outputs/2026-10-21-com-nguoi/monetization-options.md") if slug == "com-nguoi" else None, "release": None, "learning": None}, "state_authority": "run_manifest; project.json contains pointers, not a second set of gate flags"}
        save(directory / "project.json", project)
        pilot_rows.append({"slug": slug, "project": (directory / "project.json").relative_to(ROOT).as_posix(), "role": "active" if slug == "com-nguoi" else "queued", "owner": "Jason + AI", "next_dependency": "script/visual/public-scope approval" if slug == "com-nguoi" else "source/approval/rights audit before adaptation"})
    save(STUDIO / "operations/pilot-queue.json", {"date": "2026-10-21", "wip_limit": 1, "projects": pilot_rows, "dates": "unscheduled; sequence is dependency-based"})

    film = json.loads((ROOT / "outputs/2026-10-21-com-nguoi/film-script.json").read_text(encoding="utf-8"))
    timeline = {"schema_version": "1.0", "story_slug": "com-nguoi", "version": "v1", "title": "Cold Rice / Cơm nguội", "source": {"path": film["source_path"], "sha256": film["source_sha256"]}, "script_reference": "outputs/2026-10-21-com-nguoi/film-script.json", "status": "ready_for_review", "timing": "estimates_until_author_recording", "visual_mode": "flat_illustration", "author_audio": None, "music": None, "cuts": {}}
    for key in ("master", "alternate"):
        timeline["cuts"][key] = {"duration_estimate_s": sum(x["duration_estimate_s"] for x in film[key]), "shots": [{"id": x["segment_id"], "start_s": x["start_estimate_s"], "duration_s": x["duration_estimate_s"], "vo_text": x["vo_text"], "source_reference": x["source_reference"], "asset_path": x["asset_path"], "asset_sha256": x["asset_sha256"], "visual": x["visual"], "on_screen_text": x["on_screen_text"], "subtitle_status": "storyboard_text_only; speech_captions_pending", "motion": {"scale_from": 1, "scale_to": 1.03, "pan_x_px": 0, "pan_y_px": 0}} for x in film[key]]}
    save(STUDIO / "projects/com-nguoi/video/timeline.json", timeline)

    deck = ROOT / config["strategy_deck"]
    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    with zipfile.ZipFile(deck) as z:
        names = sorted([n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+.xml", n)], key=lambda n: int(re.search(r"slide(\d+)", n).group(1)))
        slides = [{"slide": int(re.search(r"slide(\d+)", name).group(1)), "text": [t.text or "" for t in ET.fromstring(z.read(name)).findall(".//a:t", ns)]} for name in names]
    save(STUDIO / "references/strategy-deck-extract.json", {"source": str(deck), "sha256": sha(deck), "slide_count": len(slides), "slides": slides, "scope": "User-provided ideation; not manuscript, approval, release proof or measured business results"})
    after_assets = {}
    for p in (STUDIO / "references/video-starter").rglob("*"):
        if p.is_file() and p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
            after_assets[p.relative_to(ROOT).as_posix()] = sha(p)
    if sorted(original_assets.values()) != sorted(after_assets.values()):
        raise ValueError("Reference artwork preservation check failed")
    save(STUDIO / "references/migration-receipt.json", {"date": "2026-10-21", "moves": relocation, "original_reference_images": len(original_assets), "preserved_reference_images": len(after_assets), "image_hashes_preserved": True, "original_images": original_assets, "current_images": after_assets, "canonical_manuscripts_moved": False, "external_asset_library_copied": False, "starter_code_archive": str(archive), "legacy_personal_references_visibility": "private; never automatically staged"})
    print(json.dumps({"studio": str(STUDIO), "pilot_projects": len(pilot_rows), "reference_images_preserved": len(after_assets), "external_source_files_modified": False, "deck_slides_read": len(slides)}))


if __name__ == "__main__":
    main()
