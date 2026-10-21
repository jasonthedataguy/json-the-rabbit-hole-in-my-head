"""Local .json studio control: references, plans, internal render staging and release checks.

No command publishes, changes source approval, sends messages or charges money.
"""
import argparse
import hashlib
import json
import math
import os
import shutil
import sys
from pathlib import Path

from validate_run import check, required_public_flags
from portable_paths import map_paths, resolve_path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "studio/studio.json"


def load(path):
    return map_paths(json.loads(resolve_path(path).read_text(encoding="utf-8")))


def sha(path):
    with resolve_path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def workspace_path(value):
    path = resolve_path(value)
    return path if path.is_absolute() else ROOT / path


def config():
    return load(CONFIG_PATH)


def slug_id(value):
    """Resolve canonical slug first; legacy numbers can never select a chapter."""
    if value.isdigit():
        raise ValueError("Use a stable slug, not a legacy chapter number")
    aliases = load(ROOT / "studio/catalog/legacy-video-aliases.json")["aliases"]
    for row in aliases:
        if value in (row["canonical_slug"], row["legacy_slug"], row["legacy_directory"]):
            return row["canonical_slug"]
    if not value or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in value):
        raise ValueError("Invalid chapter slug")
    return value


def project(value):
    slug = slug_id(value)
    path = ROOT / "studio/projects" / slug / "project.json"
    if not path.is_file():
        raise ValueError(f"No active project for {slug}; use new-project after selecting a registered story")
    return path, load(path)


def build_catalog():
    cfg = config()
    book_root = Path(cfg["book_repository"])
    art_root = Path(cfg["asset_library"])
    book_path = book_root / "book.json"
    book = load(book_path)
    art = {c["slug"]: c for c in load(art_root / "assets-manifest.json")["chapters"]}
    records = []
    for slug in ["introduction", *book["chapters"]]:
        if slug == "introduction":
            records.append({"slug": slug, "title": book["introduction"]["title"], "edition_number": "intro", "original_edition_number": None, "source": {"path": str(book_path), "selector": "introduction", "sha256": sha(book_path)}, "asset_record": str(art_root / "chapters" / slug / "assets.json"), "approval": "unknown; not inferred from registry availability", "active_project": False})
            continue
        meta_path = book_root / "chapters" / slug / "chapter.json"
        meta = load(meta_path)
        source = meta_path.parent / meta["canonical_text"]
        actual = sha(source)
        if actual != meta["manuscript_sha256"]:
            raise ValueError(f"Source/registry hash mismatch: {slug}")
        if slug not in art:
            raise ValueError(f"No existing art record: {slug}")
        project_path = ROOT / "studio/projects" / slug / "project.json"
        records.append({"slug": slug, "title": meta["title"], "edition_number": meta["number"], "original_edition_number": (meta.get("original_edition") or {}).get("number"), "source": {"path": str(source), "sha256": actual}, "registry_path": str(meta_path), "asset_record": str(art_root / "chapters" / slug / "assets.json"), "configured_route": book["public_url"] + meta["canonical_path"], "live_verified": False, "approval": "consult project run manifest; never inferred from publish:true", "active_project": project_path.is_file(), "project": str(project_path.relative_to(ROOT)) if project_path.is_file() else None})
    save(workspace_path(cfg["catalog"]), {"schema_version": "1.0", "date": "2026-10-21", "generated": True, "book_source": str(book_path), "book_sha256": sha(book_path), "counts": {"front_matter": 1, "chapter_slots": len(book["chapters"]), "total": len(records)}, "stories": records})
    return records


def validate_timeline(timeline, allowed_asset_root, *, require_opening=False):
    errors = []
    source = Path(timeline["source"]["path"])
    if not source.is_file() or sha(source) != timeline["source"]["sha256"]:
        return ["Timeline canonical source missing or stale"]
    lines = source.read_text(encoding="utf-8").splitlines()
    if timeline.get("visual_mode") == "layer_animation":
        if not timeline.get("animation_manifest") or not workspace_path(timeline["animation_manifest"]).is_file():
            errors.append("Layer animation requires an implemented, linked motion manifest")
    elif timeline.get("visual_mode") != "flat_illustration":
        errors.append("Current renderer supports flat illustration only; genuine parallax needs reviewed separated layers and an implemented composition")
    for cut, record in timeline["cuts"].items():
        if require_opening:
            opening = record["shots"][0] if record["shots"] else {}
            exception = record.get("author_opening_exception") or {}
            explicit_exception = all(exception.get(key) for key in ("requested_by", "request", "scope"))
            if not explicit_exception:
                if opening.get("kind") != "portal_entry" or not opening.get("portal_entry") or opening.get("vo_text"):
                    errors.append(f"{cut}: standard title/portal-center opening required before narrative")
                else:
                    first_story = next((shot for shot in record["shots"][1:] if shot.get("vo_text")), None)
                    if first_story and (first_story["asset_path"] != opening["portal_entry"]["reveal_asset_path"] or first_story["asset_sha256"] != opening["portal_entry"]["reveal_asset_sha256"]):
                        errors.append(f"{cut}: first story shot must continue inside the revealed center artwork")
        end = 0.0
        for shot in record["shots"]:
            if shot["duration_s"] <= 0 or not math.isclose(shot["start_s"], end, abs_tol=0.0001):
                errors.append(f"{cut}/{shot['id']}: nonpositive duration or timeline gap/overlap")
            end = shot["start_s"] + shot["duration_s"]
            path = Path(shot["asset_path"])
            if not path.resolve().is_relative_to(Path(allowed_asset_root).resolve()):
                errors.append(f"{cut}/{shot['id']}: asset is not in the selected existing art library")
            if not path.is_file() or sha(path) != shot["asset_sha256"]:
                errors.append(f"{cut}/{shot['id']}: asset missing or stale")
            entry = shot.get("portal_entry")
            if shot.get("kind") == "portal_entry" and not entry:
                errors.append(f"{cut}/{shot['id']}: portal entry configuration missing")
            if entry:
                reveal = Path(entry["reveal_asset_path"])
                if (shot.get("kind") != "portal_entry" or shot["start_s"] != 0
                        or not 1 < entry.get("max_scale", 0) <= 6
                        or not all(0 <= entry.get(k, -1) <= 1 for k in ("focus_x", "focus_y"))):
                    errors.append(f"{cut}/{shot['id']}: invalid opening portal camera")
                if not reveal.resolve().is_relative_to(Path(allowed_asset_root).resolve()):
                    errors.append(f"{cut}/{shot['id']}: reveal asset is not in the selected existing art library")
                if not reveal.is_file() or sha(reveal) != entry["reveal_asset_sha256"]:
                    errors.append(f"{cut}/{shot['id']}: reveal asset missing or stale")
                source_title = next((line.lstrip('#').strip() for line in lines if line.startswith('#')), '')
                if shot["on_screen_text"] != source_title:
                    errors.append(f"{cut}/{shot['id']}: opening title differs from supplied source")
            if shot["vo_text"]:
                ref = shot.get("source_reference") or {}
                line = ref.get("line", 0)
                if not 1 <= line <= len(lines) or shot["vo_text"] not in lines[line - 1] or ref.get("source_sha256") != timeline["source"]["sha256"]:
                    errors.append(f"{cut}/{shot['id']}: exact quote/source citation mismatch")
            if "caption_cues" in shot:
                cue_end = 0.0
                for cue in shot["caption_cues"]:
                    if cue["duration_s"] <= 0 or not math.isclose(cue["start_s"], cue_end, abs_tol=0.0001):
                        errors.append(f"{cut}/{shot['id']}: caption gap/overlap")
                    cue_end = cue["start_s"] + cue["duration_s"]
                if " ".join(c["text"] for c in shot["caption_cues"]).split() != shot["vo_text"].split():
                    errors.append(f"{cut}/{shot['id']}: caption text differs from source quote")
                if shot["caption_cues"] and not math.isclose(cue_end, shot["duration_s"], abs_tol=0.0001):
                    errors.append(f"{cut}/{shot['id']}: caption duration differs from shot")
            motion = shot.get("motion", {})
            if not 1 <= motion.get("scale_from", 1) <= 1.05 or not 1 <= motion.get("scale_to", 1) <= 1.05:
                errors.append(f"{cut}/{shot['id']}: camera move exceeds the quiet-motion preset")
        if not math.isclose(end, record["duration_estimate_s"], abs_tol=0.0001):
            errors.append(f"{cut}: duration does not equal final shot end")
        if record.get("full_source_reading"):
            expected = " ".join(line for line in lines if line.strip() and not line.startswith("#"))
            actual = " ".join(s["vo_text"] for s in record["shots"] if s["vo_text"])
            if actual.split() != expected.split():
                errors.append(f"{cut}: full reading omits, duplicates or changes source text")
    return errors


def validate_script_selection(timeline, canonical, evidence):
    """An author-supplied film variant never silently changes the book selection."""
    errors = []
    if timeline["source"]["sha256"] != canonical["sha256"]:
        if not evidence:
            return ["Video script variant requires exact author approval evidence"]
        if (evidence.get("approved") is not True
                or evidence.get("approved_sha256") != timeline["source"]["sha256"]
                or evidence.get("canonical_source_sha256") != canonical["sha256"]
                or evidence.get("scope") != "video_script_text_only"):
            errors.append("Video script approval scope or source mismatch")
    return errors


def audit_project(value):
    _, data = project(value)
    errors, warnings = [], []
    source = Path(data["source"]["path"])
    if not source.is_file() or sha(source) != data["source"]["sha256"]:
        errors.append("Project source reference is stale; review changes rather than resetting gates")
    run_path = workspace_path(data["run_manifest"])
    run = load(run_path)
    problems, notices, _ = check(run)
    errors.extend(problems)
    warnings.extend(notices)
    if run.get("canonical_sha256") != data["source"]["sha256"]:
        errors.append("Run/project source hashes disagree")
    for field in ("source_facts_approval_evidence", "manuscript_text_approval_evidence"):
        if run.get(field):
            evidence = workspace_path(run[field])
            if not evidence.is_file():
                errors.append(f"Missing {field}")
            elif load(evidence).get("approved_sha256") != run["canonical_sha256"]:
                errors.append(f"Approval does not identify current canonical bytes: {field}")
    for derivative in run.get("derivatives", []):
        path = workspace_path(derivative["path"])
        if not path.is_file() or derivative.get("artifact_sha256") and sha(path) != derivative["artifact_sha256"]:
            errors.append(f"Stale derivative: {derivative['path']}")
    if data.get("timeline"):
        timeline = load(workspace_path(data["timeline"]))
        errors.extend(validate_timeline(timeline, config()["asset_library"], require_opening=config().get("video_policy", {}).get("opening_required", False)))
        approval = None
        if run.get("script_approval_evidence"):
            pointer = run["script_approval_evidence"]
            path = workspace_path(pointer["path"])
            if not path.is_file() or sha(path) != pointer["sha256"]:
                errors.append("Script approval evidence missing or stale")
            else:
                approval = load(path)
        errors.extend(validate_script_selection(timeline, data["source"], approval))
        if timeline.get("visual_mode") == "layer_animation":
            pointer = data.get("animation_manifest") or {}
            motion_path = workspace_path(pointer.get("path", ""))
            renderer_path = workspace_path(pointer.get("render_entry", ""))
            if (not motion_path.is_file() or sha(motion_path) != pointer.get("sha256")
                    or str(motion_path) != str(workspace_path(timeline["animation_manifest"]))):
                errors.append("Active animation manifest missing, stale or different from timeline")
            elif not renderer_path.is_file() or sha(renderer_path) != pointer.get("render_entry_sha256"):
                errors.append("Implemented animation render entry missing or stale")
            else:
                import importlib.util
                module_path = ROOT / "skills/json-asset-animation/scripts/motion_assets.py"
                spec = importlib.util.spec_from_file_location("studio_motion_assets", module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                motion = load(motion_path)
                if motion["source"] != timeline["source"] or motion["timeline"] != timeline:
                    errors.append("Motion manifest and narrative timeline disagree")
                result = module.check_manifest(motion, [Path(config()["asset_library"]), ROOT / "studio/projects" / data["story_slug"] / "animation"])
                errors.extend(result["errors"])
    return {"slug": data["story_slug"], "status": "pass" if not errors else "fail", "errors": errors, "warnings": warnings, "source_sha256": data["source"]["sha256"], "run_manifest": str(run_path), "manuscript_approved": run["author_approved"], "script_approved": run["script_facts_approved"], "release_approved": run["founder_public_release_approved"], "interpretation": "pass means references/logic are consistent, not ready to release"}


def release_report(run, *, paid=False):
    errors, warnings, ready = check(run)
    surfaces, required = required_public_flags(run)
    blockers = list(errors)
    blockers += [key for key in sorted(required) if not run.get(key)]
    if run.get("public_visibility_policy") in (None, "", "undecided"):
        blockers.append("public_visibility_policy")
    # A boolean never substitutes for exact public-release evidence.
    evidence = run.get("founder_public_release_evidence")
    if not isinstance(evidence, dict) or not evidence.get("path") or not evidence.get("sha256"):
        blockers.append("exact_public_release_evidence")
    else:
        path = workspace_path(evidence["path"])
        if not path.is_file() or sha(path) != evidence["sha256"]:
            blockers.append("public_release_evidence_missing_or_stale")
        else:
            approval = load(path)
            if approval.get("approved") is not True or not approval.get("approver"):
                blockers.append("public_release_evidence_not_an_author_approval")
            if approval.get("approved_source_sha256") != run.get("canonical_sha256") or sorted(approval.get("surfaces", [])) != sorted(surfaces):
                blockers.append("public_release_evidence_scope_or_source_mismatch")
            assets = approval.get("approved_artifacts", [])
            if not assets or set(a.get("surface") for a in assets) != set(surfaces):
                blockers.append("public_release_evidence_missing_selected_artifacts")
            for asset in assets:
                target = workspace_path(asset.get("path", ""))
                if not target.is_file() or sha(target) != asset.get("sha256"):
                    blockers.append("public_release_artifact_missing_or_stale")
    if paid or any(s in surfaces for s in ("digital_product", "physical_product")):
        for key in ("selected_revenue_offer", "commerce_checkout_and_fulfillment_tested", "founder_paid_release_approved", "founder_paid_release_evidence"):
            if not run.get(key):
                blockers.append(key)
        paid_evidence = run.get("founder_paid_release_evidence")
        if isinstance(paid_evidence, dict):
            path = workspace_path(paid_evidence.get("path", ""))
            if not path.is_file() or sha(path) != paid_evidence.get("sha256"):
                blockers.append("paid_release_evidence_missing_or_stale")
            else:
                approval = load(path)
                if approval.get("approved") is not True or not approval.get("approver") or approval.get("approved_source_sha256") != run.get("canonical_sha256") or approval.get("selected_revenue_offer") != run.get("selected_revenue_offer"):
                    blockers.append("paid_approval_scope_source_or_offer_mismatch")
        elif paid_evidence:
            blockers.append("paid_release_evidence_requires_path_and_hash")
    return {"ready": ready and not blockers, "surfaces": surfaces, "blockers": sorted(set(blockers)), "warnings": warnings, "publishing_performed": False}


def stage_asset(source, destination):
    """Use a cache alias where possible; never edit or replace a source image."""
    source, destination = Path(source), Path(destination)
    if destination.exists():
        if sha(source) != sha(destination):
            raise ValueError("Existing render cache differs; do not overwrite it")
        return "existing"
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.link(source, destination)
        return "hardlink"
    except OSError:
        shutil.copy2(source, destination)
        if sha(source) != sha(destination):
            raise ValueError("Render input changed during staging")
        return "copy_for_render_cache"


def prepare_video(value, cut, format_name):
    _, data = project(value)
    audit = audit_project(value)
    if audit["errors"]:
        raise ValueError("; ".join(audit["errors"]))
    if not data.get("timeline"):
        raise ValueError("No source-grounded timeline exists for this queued project")
    timeline_path = workspace_path(data["timeline"])
    timeline = load(timeline_path)
    if timeline.get("visual_mode") != "flat_illustration":
        raise ValueError("This project uses a separate layer-animation composition; follow its video README rather than flattening it through prepare-video")
    if cut not in timeline["cuts"]:
        raise ValueError(f"Cut '{cut}' is not in the active timeline; available: {', '.join(timeline['cuts'])}")
    record = timeline["cuts"][cut]
    cfg = config()
    style = load(workspace_path(cfg["style"]))
    fmt = next(x for x in style["formats"] if x["name"] == format_name)
    renderer_hash = sha(workspace_path(cfg["video_app"]) / "src/video.tsx")
    fingerprint = hashlib.sha256((sha(timeline_path) + sha(workspace_path(cfg["style"])) + renderer_hash + cut + format_name).encode()).hexdigest()[:12]
    cache = workspace_path(cfg["cache"]) / "render" / data["story_slug"] / fingerprint
    public = cache / "public"
    shots, staged = [], {}
    dimensions = {}
    def collect_dimensions(value):
        if isinstance(value, dict):
            if all(k in value for k in ("path", "width", "height")):
                dimensions[str((Path(cfg["asset_library"]) / value["path"]).resolve())] = (value["width"], value["height"])
            for child in value.values():
                collect_dimensions(child)
        elif isinstance(value, list):
            for child in value:
                collect_dimensions(child)
    collect_dimensions(load(data["asset_record"]))
    for shot in record["shots"]:
        path = Path(shot["asset_path"])
        if sha(path) != shot["asset_sha256"]:
            raise ValueError("Selected art changed after timeline audit")
        name = shot["asset_sha256"][:20] + path.suffix.lower()
        mode = stage_asset(path, public / name)
        staged[name] = {"source": str(path), "sha256": sha(path), "mode": mode}
        native_width, native_height = dimensions[str(path.resolve())]
        cues = [{"startFrame": round(c["start_s"] * fmt["fps"]), "durationInFrames": round(c["duration_s"] * fmt["fps"]), "text": c["text"]} for c in shot.get("caption_cues", [])]
        compiled = {"id": shot["id"], "startFrame": round(shot["start_s"] * fmt["fps"]), "durationInFrames": round(shot["duration_s"] * fmt["fps"]), "voText": shot["vo_text"], "imageSrc": name, "nativeWidth": native_width, "nativeHeight": native_height, "onScreenText": shot["on_screen_text"], "motion": shot["motion"], "captionCues": cues, "kind": shot.get("kind", "story")}
        if shot.get("portal_entry"):
            entry = shot["portal_entry"]
            reveal_path = Path(entry["reveal_asset_path"])
            reveal_name = entry["reveal_asset_sha256"][:20] + reveal_path.suffix.lower()
            staged[reveal_name] = {"source": str(reveal_path), "sha256": sha(reveal_path), "mode": stage_asset(reveal_path, public / reveal_name)}
            compiled["portalEntry"] = {"focusX": entry["focus_x"], "focusY": entry["focus_y"], "maxScale": entry["max_scale"], "revealImageSrc": reveal_name}
        shots.append(compiled)
    font = Path(cfg["book_repository"]) / "shared/fonts/Noto-Serif.ttf"
    font_name = "noto-serif-" + sha(font)[:12] + ".ttf"
    staged[font_name] = {"source": str(font), "sha256": sha(font), "mode": stage_asset(font, public / font_name)}
    license_path = font.with_name("Noto-Serif-OFL.txt")
    stage_asset(license_path, public / "Noto-Serif-OFL.txt")
    props = {"title": timeline.get("display_title", data["title"]), "slug": data["story_slug"], "editionLabel": "Prologue 00" if data["edition_number"] == "00" else "Chapter " + data["edition_number"], "format": fmt, "durationInFrames": round(record["duration_estimate_s"] * fmt["fps"]), "shots": shots, "fontSrc": font_name, "renderKind": "internal_preview", "timingStatus": "estimated; silent reading cut, not speech captions", "sourceSha256": timeline["source"]["sha256"], "palette": style["palette"], "publicDir": str(public), "outputPath": str(ROOT / "studio/projects" / data["story_slug"] / "video/previews" / f"{cut}-{format_name}-{fingerprint}-REVIEW.mp4"), "cut": cut}
    props_path = cache / "props.json"
    save(props_path, props)
    save(cache / "staging.json", {"purpose": "private transient render inputs only; no mirrored library", "inputs": staged, "source_changes_allowed": False})
    save(workspace_path(cfg["video_app"]) / "manifests/active-preview.json", props)
    return {"status": "prepared_internal_preview", "props": str(props_path), "public_dir": str(public), "frames": props["durationInFrames"], "source_assets_staged": len(staged), "copied_asset_count": sum(x["mode"] == "copy_for_render_cache" for x in staged.values()), "author_narration": "not present", "release_approved": False}


def new_project(value):
    slug = slug_id(value)
    row = next((r for r in load(workspace_path(config()["catalog"]))["stories"] if r["slug"] == slug), None)
    if not row or slug == "introduction":
        raise ValueError("Choose a registered chapter; front matter/raw-story intake uses the source workflow first")
    path = ROOT / "studio/projects" / slug
    if (path / "project.json").exists():
        raise ValueError("Project already exists; refusing to duplicate or reset approval state")
    run = load(ROOT / "templates/run-manifest.json")
    run.update({"story_id": slug, "chapter_slug": slug, "chapter_slot": row["edition_number"], "title": row["title"], "canonical_source_path": row["source"]["path"], "canonical_sha256": row["source"]["sha256"], "run_mode": "audit", "release_scope": {"surfaces": ["reader", "film", "social"]}, "notes": "Intake created from source references; no prose/art/generated media/approval inferred."})
    run["stage_evidence"]["S09_commerce"] = {"reason": "Optional; no paid offer selected."}
    save(path / "run-manifest.json", run)
    save(path / "project.json", {"schema_version": "1.0", "story_slug": slug, "title": row["title"], "edition_number": row["edition_number"], "original_edition_number": row["original_edition_number"], "source": row["source"], "run_manifest": (path / "run-manifest.json").relative_to(ROOT).as_posix(), "asset_record": row["asset_record"], "timeline": None, "lanes": {"editorial": str(Path(row["source"]["path"]).parent), "design": row["asset_record"], "reader": None, "audio": None, "video": None, "social": None, "commerce": None, "release": None, "learning": None}, "state_authority": "run_manifest"})
    return {"project": str(path / "project.json"), "approval_flags": "all pending", "source_material_copied": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("catalog")
    sub.add_parser("status")
    sub.add_parser("audit")
    new = sub.add_parser("new-project")
    new.add_argument("slug")
    video = sub.add_parser("prepare-video")
    video.add_argument("slug")
    video.add_argument("--cut", default="master", choices=["master", "alternate"])
    video.add_argument("--format", default="vertical", choices=["vertical", "landscape", "square", "feed"])
    release = sub.add_parser("check-release")
    release.add_argument("slug")
    release.add_argument("--paid", action="store_true")
    args = parser.parse_args()
    if args.command == "catalog":
        rows = build_catalog()
        result = {"stories": len(rows), "copied_manuscripts_or_art": False}
    elif args.command == "new-project":
        result = new_project(args.slug)
    elif args.command == "prepare-video":
        result = prepare_video(args.slug, args.cut, args.format)
    elif args.command == "check-release":
        _, data = project(args.slug)
        result = release_report(load(workspace_path(data["run_manifest"])), paid=args.paid)
        audit = audit_project(args.slug)
        result["blockers"] += audit["errors"]
        result["ready"] = result["ready"] and not audit["errors"]
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ready"] else 2
    else:
        queue = load(ROOT / "studio/operations/pilot-queue.json")
        projects = [audit_project(x["slug"]) for x in queue["projects"]]
        result = {"status": "pass" if all(p["status"] == "pass" for p in projects) else "fail", "projects": projects}
        if args.command == "audit":
            save(ROOT / "studio/reports/workspace-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result.get("status") == "fail" else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError, StopIteration) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
