"""Apply the author's opening correction without altering script or v2 review files."""
from pathlib import Path
import sys
import copy

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
from studio import load, save, sha


def main():
    project = ROOT / "studio/projects/com-nguoi"
    timeline_path = project / "video/timeline.json"
    current = load(timeline_path)
    history = project / "video/history/timeline-full-silent-v2.json"
    if current["version"] == "v2-full-silent":
        if not history.exists():
            save(history, current)
        original = current
    else:
        original = load(history)
    timeline = copy.deepcopy(original)
    timeline["version"] = "v3-portal-entry"
    timeline["creative_revision"] = {
        "request": "you miss the introduction part, i need the transition to go into the center art with the narrative of the chapter title then it comes to the story",
        "date": "2026-10-21", "scope": "internal silent opening revision; public release unapproved",
        "sequence": "Hold chapter title; camera enters the portal's family-table center; dissolve to sharp existing center-scene art; settle into story before its first paragraph.",
        "title_narration": "Cơm nguội is the title reading beat; intentionally text-only in the authorized silent review format. No new narrative or synthetic speech."
    }
    record = timeline["cuts"]["master"]
    opening = record["shots"][0]
    difference = 10.5 - opening["duration_s"]
    hero = Path(record["shots"][4]["asset_path"])
    assert hero.name == "hero.webp"
    opening.update({"kind": "portal_entry", "duration_s": 10.5,
                    "visual": "Title hold, focused camera entry into center artwork, sharp family-table reveal, then first source paragraph.",
                    "portal_entry": {"focus_x": 0.5, "focus_y": 0.565, "max_scale": 5.5, "reveal_asset_path": str(hero), "reveal_asset_sha256": sha(hero)}})
    for shot in record["shots"][1:]:
        shot["start_s"] += difference
        if shot["id"] in ("P01", "P02"):
            shot["asset_path"] = str(hero)
            shot["asset_sha256"] = sha(hero)
            shot["visual"] = "Continue inside the family-table scene revealed by the opening; no return to the exterior portal."
    record["duration_estimate_s"] += difference
    save(timeline_path, timeline)
    def stamp(seconds, separator):
        value = round(seconds * 1000)
        return f"{value // 3600000:02}:{value // 60000 % 60:02}:{value // 1000 % 60:02}{separator}{value % 1000:03}"
    srt, vtt, number = [], ["WEBVTT", "", "NOTE Silent reading cut, including the chapter-title introduction.", ""], 0
    for shot in record["shots"]:
        cues = shot.get("caption_cues", [])
        if shot["id"] == "OPEN":
            cues = [{"start_s": 0.7, "duration_s": 4.0, "text": shot["on_screen_text"]}]
        for cue in cues:
            number += 1
            start = shot["start_s"] + cue["start_s"]
            end = start + cue["duration_s"]
            for target, separator in ((srt, ','), (vtt, '.')):
                target.extend([str(number), f"{stamp(start, separator)} --> {stamp(end, separator)}", cue["text"], ""])
    srt_path = project / "video/com-nguoi-v3-reading-timings.srt"
    vtt_path = project / "video/com-nguoi-v3-reading-timings.vtt"
    srt_path.write_text("\n".join(srt), encoding="utf-8")
    vtt_path.write_text("\n".join(vtt), encoding="utf-8")
    run_path = ROOT / "outputs/2026-10-21-com-nguoi/run-manifest.json"
    run = load(run_path)
    # The previous timeline moves to history so its prior derivative hash remains meaningful.
    for derivative in run["derivatives"]:
        if derivative["id"] == "full-video-timeline-v2":
            derivative["path"] = str(history)
            derivative["artifact_sha256"] = sha(history)
            derivative["status"] = "historical_review"
    for identifier, path, fmt in [("full-video-timeline-v3", timeline_path, "json"), ("silent-reading-srt-v3", srt_path, "srt"), ("silent-reading-vtt-v3", vtt_path, "vtt")]:
        run["derivatives"] = [item for item in run["derivatives"] if item["id"] != identifier]
        run["derivatives"].append({"id": identifier, "path": str(path), "artifact_sha256": sha(path), "source_sha256": timeline["source"]["sha256"], "canonical_source_sha256": run["canonical_sha256"], "version": "v3-portal-entry", "format": fmt, "status": "ready_for_review", "rights": "internal review only; public/paid approval pending", "evidence": str(timeline_path)})
    run["stages"]["S06_audio_film"] = "in_progress"
    run["stage_evidence"]["S06_audio_film"] = {"path": str(timeline_path), "reason": "Author requested missing portal-entry introduction. V3 rendering; full script and prior review retained."}
    run["notes"] = "Author correction: add chapter-title introduction, enter portal center and reveal the story. V3 silent cut in production; v2 retained. Script and book selections unchanged; release remains unapproved."
    save(run_path, run)
    print({"version": timeline["version"], "duration_s": record["duration_estimate_s"], "story_starts_s": record["shots"][1]["start_s"], "script_unchanged": True})


if __name__ == "__main__":
    main()
