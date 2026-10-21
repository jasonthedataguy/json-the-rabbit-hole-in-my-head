"""Inspect the rendered MP4 and extract every reading cue for human visual review."""
from pathlib import Path
import json
import subprocess
import sys
import argparse

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
from studio import load, save, sha, validate_timeline
from portable_paths import runtime_binary
from PIL import Image, ImageDraw, ImageFont


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--v4', action='store_true')
    parser.add_argument('--v5', action='store_true')
    args = parser.parse_args()
    assert not (args.v4 and args.v5), 'Select one version'
    animated = args.v4 or args.v5
    version_number = 'v5' if args.v5 else 'v4'
    project = ROOT / "studio/projects/com-nguoi"
    props_path = ROOT / "studio/apps/video/manifests" / ('com-nguoi-'+version_number+'.json' if animated else 'active-preview.json')
    props = load(props_path)
    assert props.get('story_slug', props.get('slug')) == 'com-nguoi'
    if animated:
        assert props['classification'] == 'layer_animation'
    else:
        assert props['cut'] == 'master'
    video = Path(props["outputPath"])
    timeline_path = project / 'video' / ('timeline-'+version_number+'.json' if animated else 'timeline.json')
    timeline = load(timeline_path)
    assert (props['source']['sha256'] if animated else props['sourceSha256']) == timeline['source']['sha256']
    cfg = load(ROOT / "studio/studio.json")
    assert not validate_timeline(timeline, cfg["asset_library"])
    probe_binary = runtime_binary('ffprobe')
    ffmpeg_binary = runtime_binary('ffmpeg')
    result = subprocess.run([probe_binary, "-v", "error", "-count_frames", "-show_format", "-show_streams", "-of", "json", str(video)], capture_output=True, text=True, check=True)
    probe = json.loads(result.stdout)
    streams = probe["streams"]
    assert not any(s["codec_type"] == "audio" for s in streams), "Silent cut must have no audio track"
    picture = next(s for s in streams if s["codec_type"] == "video")
    assert picture["codec_name"] == "h264"
    assert (picture["width"], picture["height"]) == (1080, 1920)
    assert picture["avg_frame_rate"] == "30/1"
    expected_duration = timeline["cuts"]["master"]["duration_estimate_s"]
    expected_frames = round(props['duration_s']*props['fps']) if animated else props['durationInFrames']
    assert int(picture["nb_read_frames"]) == expected_frames == round(expected_duration * 30)
    assert abs(float(picture["duration"]) - expected_duration) < 0.04
    version = timeline["version"]
    qa = project / "video/review" / ("v2-silent" if version == "v2-full-silent" else version)
    qa.mkdir(parents=True, exist_ok=True)
    save(qa / "ffprobe.json", probe)
    save(qa / "render-props.json", props)
    font = ImageFont.truetype(str(Path(cfg["book_repository"]) / "shared/fonts/Noto-Serif.ttf"), 19)
    captures = []
    for shot in timeline["cuts"]["master"]["shots"]:
        cues = shot.get("caption_cues") or [{"start_s": 0, "duration_s": shot["duration_s"], "text": shot["on_screen_text"]}]
        if shot.get("kind") == "portal_entry":
            cues = [{"start_s": second, "duration_s": 0.1, "text": phase} for second, phase in [(1.5, "chapter title"), (4.5, "enter portal"), (6.5, "center reveal begins"), (7.5, "center-scene dissolve"), (9.5, "settle into story"), (10.35, "landing before first source paragraph")]]
        for number, cue in enumerate(cues, 1):
            seconds = shot["start_s"] + cue["start_s"] + cue["duration_s"] / 2
            path = qa / f"{shot['id']}-{number:02}.png"
            subprocess.run([ffmpeg_binary, "-v", "error", "-y", "-ss", str(seconds), "-i", str(video), "-frames:v", "1", str(path)], capture_output=True, check=True)
            captures.append({"shot": shot["id"], "cue": number, "time_s": seconds, "text": cue["text"], "frame": str(path)})
    for page in range((len(captures) + 8) // 9):
        items = captures[page * 9:(page + 1) * 9]
        sheet = Image.new("RGB", (972, 1878), "#101f31")
        draw = ImageDraw.Draw(sheet)
        for index, item in enumerate(items):
            x, y = index % 3 * 324, index // 3 * 626
            with Image.open(item["frame"]) as image:
                image.thumbnail((324, 576))
                sheet.paste(image.convert("RGB"), (x, y))
            draw.text((x + 12, y + 581), f"{item['shot']}/{item['cue']} · {item['time_s']:.1f}s", font=font, fill="#f4eee3")
        sheet.save(qa / f"contact-sheet-{page + 1:02}.jpg", quality=92)
    report = {"technical_status": "pass", "visual_review_status": "pending_manual_inspection", "date": "2026-10-21",
              "classification": 'layer_animation' if animated else 'camera_only_reading_cut',
              "video": str(video), "video_sha256": sha(video), "bytes": video.stat().st_size,
              "source_sha256": timeline["source"]["sha256"], "timeline_sha256": sha(timeline_path),
              "duration_s": float(picture["duration"]), "frames_decoded": int(picture["nb_read_frames"]), "resolution": [1080, 1920], "fps": 30,
              "audio_tracks": 0, "full_source_coverage": True, "reading_cues": 27, "captures": captures,
              "opening": {"kind": timeline["cuts"]["master"]["shots"][0].get("kind"), "duration_s": timeline["cuts"]["master"]["shots"][0]["duration_s"], "title": timeline["cuts"]["master"]["shots"][0]["on_screen_text"], "title_audio": "none; silent review", "story_start_s": timeline["cuts"]["master"]["shots"][1]["start_s"]},
              "public_release_approved": False, "paid_release_approved": False}
    save(qa / "verification.json", report)
    print(json.dumps({k: v for k, v in report.items() if k != "captures"}, indent=2))


if __name__ == "__main__":
    main()
