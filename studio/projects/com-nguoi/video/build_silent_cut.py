"""Build the full author-supplied script's private reading cut; no book/library writes."""
from pathlib import Path
import sys
from itertools import combinations

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
from studio import load, save, sha
from PIL import ImageFont

PROJECT = ROOT / "studio/projects/com-nguoi"
SOURCE = PROJECT / "script/final-script-v2.md"
RUN = ROOT / "outputs/2026-10-21-com-nguoi/run-manifest.json"
ART = Path(r"E:\books\.json\outputs\json-digital-book-assets\chapters\com-nguoi\artwork")

# Clause boundaries are presentation choices only; every source word is retained.
CHUNKS = [
    ["Nếu đây là lần đầu tiên các cậu ăn cơm với tớ,", "chắc hẳn các cậu sẽ hơi ngạc nhiên", "khi thấy tớ luôn chọn cơm nguội,", "dù trên bàn vẫn có một nồi cơm mới nấu nóng hổi."],
    ["Nó không phải sở thích.", "Chẳng ai có cái sở thích kỳ quái vậy cả.", "Ăn cơm nóng rõ ràng ngon hơn chứ.", "Với tớ, nó chỉ là một thói quen,", "mà thói quen thì thường rất khó bỏ."],
    ["Cơm nguội gắn liền với thời thơ ấu của tớ."],
    ["Ngày bé, cái thời mà lò vi sóng", "hay bất cứ thứ gì dùng để hâm nóng thức ăn vẫn còn xa lạ,", "tô cơm nguội luôn xuất hiện trong những bữa ăn nhà tớ.", "Tớ để ý bố luôn là người ăn hết tô cơm ấy,", "còn phần cơm nóng thì để mẹ và tớ ăn."],
    ["Tớ không muốn bố phải ăn cơm nguội."],
    ["Thế nên cứ mỗi bữa, tớ lại giành lấy phần cơm ấy,", "bảo rằng tớ thích ăn cơm nguội hơn.", "Ban đầu chỉ đơn giản là không muốn bố", "phải ăn phần cơm còn lại từ bữa trước.", "Nhưng cứ thế, bữa này qua bữa khác,", "nó dần trở thành thói quen."],
    ["Cho đến tận bây giờ."],
    ["Thỉnh thoảng trong những bữa cơm, bố mẹ vẫn bảo:"],
    ["“Sao không ăn cơm nóng kia con,", "ăn cơm nguội đau dạ dày.”"],
    ["“Con thích ăn cơm nguội.”"],
]


def main():
    project = load(PROJECT / "project.json")
    run = load(RUN)
    digest = sha(SOURCE)
    paragraphs = [(i + 1, line) for i, line in enumerate(SOURCE.read_text(encoding="utf-8").splitlines()) if line and not line.startswith("#")]
    assert len(paragraphs) == len(CHUNKS)
    for (_, paragraph), chunks in zip(paragraphs, CHUNKS):
        assert " ".join(chunks) == paragraph, "Chunks must preserve the supplied script exactly"
    approval_path = PROJECT / "script/final-script-v2-approval.json"
    save(approval_path, {
        "approved": True, "approver": "author in this chat", "date": "2026-10-21",
        "scope": "video_script_text_only", "approved_path": str(SOURCE), "approved_sha256": digest,
        "canonical_source_sha256": project["source"]["sha256"],
        "evidence": "Author supplied the complete text with 'here is the final script' and requested generation of the first Cơm Nguội video.",
        "review_format_authorization": "give me a silent review cut",
        "book_selection_changed": False, "public_release_approved": False, "paid_release_approved": False,
        "difference_note": "The supplied video script retains the unsplit opening sentence and earlier paragraphing; prior manuscript approval remains selected in the external book."
    })
    font = ImageFont.truetype(str(Path(load(ROOT / "studio/studio.json")["book_repository"]) / "shared/fonts/Noto-Serif.ttf"), 52)
    def wrap(text):
        words = text.split()
        for count in range(1, 4):
            candidates = []
            for breaks in combinations(range(1, len(words)), count - 1):
                bounds = (0, *breaks, len(words))
                lines = [" ".join(words[a:b]) for a, b in zip(bounds, bounds[1:])]
                widths = [font.getlength(line) for line in lines]
                if max(widths) <= 878:
                    candidates.append((max(widths) - min(widths), lines))
            if candidates:
                return "\n".join(min(candidates, key=lambda c: c[0])[1])
        raise ValueError("Caption exceeds portrait reading area")
    assets = ["main-book/portal.webp", "main-book/portal.webp", "content/illustrations/01-story-detail.webp", "chapter-page/hero.webp", "content/illustrations/01-story-detail.webp", "content/illustrations/01-story-detail.webp", "chapter-page/portal.webp", "chapter-page/hero.webp", "chapter-page/hero.webp", "chapter-page/hero.webp"]
    shots, cursor = [], 0.0
    def shot(identifier, duration, relative, text="", ref=None, cues=None, kind="story", screen=""):
        nonlocal cursor
        path = ART / relative
        record = {"id": identifier, "start_s": cursor, "duration_s": duration, "vo_text": text, "source_reference": ref,
                  "asset_path": str(path), "asset_sha256": sha(path), "kind": kind, "on_screen_text": screen,
                  "visual": "Existing complete illustration; contained, slow push and dissolve. No archival claim.",
                  "subtitle_status": "silent reading text; timings estimated, not aligned to speech",
                  "motion": {"scale_from": 1.0, "scale_to": 1.025, "pan_x_px": 0, "pan_y_px": 0}}
        if cues is not None:
            record["caption_cues"] = cues
        shots.append(record)
        cursor += duration
    shot("OPEN", 3, "chapter-page/portal.webp", kind="title", screen="Cơm nguội")
    for index, ((line, paragraph), chunks, asset) in enumerate(zip(paragraphs, CHUNKS, assets), 1):
        cues, local = [], 0.0
        for chunk in chunks:
            duration = max(3.0, round((len(chunk.split()) / 3.0 + 0.65) * 2) / 2)
            if index in (5, 7, 10):
                duration = max(duration, 5.0)
            cues.append({"start_s": local, "duration_s": duration, "text": wrap(chunk)})
            local += duration
        shot(f"P{index:02}", local, asset, paragraph,
             {"text": paragraph, "line": line, "path": str(SOURCE), "source_sha256": digest}, cues)
    shot("CLOSE", 4, "chapter-page/portal.webp", kind="end", screen="Cơm nguội")
    timeline_path = PROJECT / "video/timeline.json"
    old = load(timeline_path)
    if old.get("version") == "v1":
        history = PROJECT / "video/history/timeline-excerpts-v1.json"
        if not history.exists():
            save(history, old)
    timeline = {"schema_version": "1.1", "story_slug": "com-nguoi", "version": "v2-full-silent", "display_title": "Cơm nguội",
                "source": {"path": str(SOURCE), "sha256": digest}, "canonical_narrative_source": project["source"],
                "script_reference": str(SOURCE), "script_approval_reference": str(approval_path), "status": "ready_for_review",
                "timing": "estimated_for_silent_reading; author requested a silent review cut", "visual_mode": "flat_illustration",
                "author_audio": None, "music": None,
                "cuts": {"master": {"duration_estimate_s": cursor, "full_source_reading": True, "shots": shots}}}
    save(timeline_path, timeline)
    def timestamp(seconds, separator):
        millis = round(seconds * 1000)
        return f"{millis // 3600000:02}:{millis // 60000 % 60:02}:{millis // 1000 % 60:02}{separator}{millis % 1000:03}"
    srt, vtt, count = [], ["WEBVTT", "", "NOTE Silent reading timings; no speech recording.", ""], 0
    for item in shots:
        for cue in item.get("caption_cues", []):
            count += 1
            start = item["start_s"] + cue["start_s"]
            end = start + cue["duration_s"]
            srt.extend([str(count), f"{timestamp(start, ',')} --> {timestamp(end, ',')}", cue["text"], ""])
            vtt.extend([str(count), f"{timestamp(start, '.')} --> {timestamp(end, '.')}", cue["text"], ""])
    srt_path = PROJECT / "video/com-nguoi-v2-reading-timings.srt"
    vtt_path = PROJECT / "video/com-nguoi-v2-reading-timings.vtt"
    srt_path.write_text("\n".join(srt), encoding="utf-8")
    vtt_path.write_text("\n".join(vtt), encoding="utf-8")
    run["script_facts_approved"] = True
    run["script_approval_evidence"] = {"path": str(approval_path), "sha256": sha(approval_path)}
    run["stages"]["S03_narration_script"] = "approved"
    run["stages"]["S06_audio_film"] = "in_progress"
    run["stage_evidence"]["S03_narration_script"] = {"path": str(SOURCE), "sha256": digest, "scope": "author supplied final full video script; excerpt scripts remain historical", "approval": str(approval_path)}
    run["stage_evidence"]["S06_audio_film"] = {"path": str(timeline_path), "reason": "Full silent review cut authorized; rendering in progress. Author narration and release remain separate."}
    run["approval_gates"]["script"] = {"status": "final_video_script_text_approved", "evidence": str(approval_path)}
    run["approval_scope_note"] = "Book manuscript v1 approval retained. Author supplied final full video script v2 and requested a silent review cut. This approves video text/use for internal production only; family/public scope, final quality, public and paid release remain pending."
    for blocker in run["blockers"]:
        if blocker["id"] == "SCRIPT_AND_SCOPE":
            blocker["id"] = "PUBLIC_SCOPE"
            blocker["reason"] = "Video script supplied as final; public family/visual scope remains pending."
        elif blocker["id"] == "VO":
            blocker["reason"] = "Silent review cut explicitly requested. Author recording is needed only for a future personal-narration release."
    for identifier, path, fmt in [("final-video-script-v2", SOURCE, "md"), ("full-video-timeline-v2", timeline_path, "json"), ("silent-reading-srt-v2", srt_path, "srt"), ("silent-reading-vtt-v2", vtt_path, "vtt")]:
        run["derivatives"] = [d for d in run["derivatives"] if d["id"] != identifier]
        run["derivatives"].append({"id": identifier, "path": str(path), "source_sha256": digest, "canonical_source_sha256": project["source"]["sha256"], "artifact_sha256": sha(path), "version": "v2", "format": fmt, "status": "approved" if path == SOURCE else "ready_for_review", "rights": "internal production only; public/commercial gates pending", "evidence": str(approval_path) if path == SOURCE else str(path)})
    save(RUN, run)
    print({"duration_s": cursor, "frames_30fps": round(cursor * 30), "source_words": len(" ".join(p for _, p in paragraphs).split()), "reading_cues": count, "source_sha256": digest, "narration": "none"})


if __name__ == "__main__":
    main()
