from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import studio
from validate_run import check, required_public_flags


class StudioTests(unittest.TestCase):
    def setUp(self):
        cache = studio.ROOT / "studio/.cache/tests"
        cache.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=cache)
        self.root = Path(self.temp.name)
        def cleanup():
            if not self.root.resolve().is_relative_to(cache.resolve()):
                raise ValueError("Refusing test cleanup outside workspace cache")
            self.temp.cleanup()
        self.addCleanup(cleanup)
        self.source = self.root / "approved.md"
        self.source.write_text("# Cơm nguội\n\nNó không phải sở thích.\n", encoding="utf-8")
        self.art = self.root / "art"
        self.art.mkdir()
        self.image = self.art / "existing.webp"
        self.image.write_bytes(b"existing illustrative asset fixture")
        self.timeline = {"source": {"path": str(self.source), "sha256": studio.sha(self.source)}, "visual_mode": "flat_illustration", "cuts": {"master": {"duration_estimate_s": 5, "shots": [{"id": "B01", "start_s": 0, "duration_s": 5, "vo_text": "Nó không phải sở thích.", "source_reference": {"text": "Nó không phải sở thích.", "line": 3, "source_sha256": studio.sha(self.source)}, "asset_path": str(self.image), "asset_sha256": studio.sha(self.image), "motion": {"scale_from": 1, "scale_to": 1.03}}]}}}

    def reader_run(self):
        run = studio.load(studio.ROOT / "templates/run-manifest.json")
        run.update({"author_approved": True, "canonical_source_path": str(self.source), "canonical_sha256": studio.sha(self.source), "source_facts_approval_evidence": "fixture text approval", "founder_public_release_approved": True, "privacy_rights_approved": True, "reader_verified_live": True, "reader_live_url": "https://example.invalid/verified-fixture", "website_cta_verified": True, "public_visibility_policy": "explicit fixture", "release_scope": {"surfaces": ["reader"]}})
        return run

    def add_public_evidence(self, run):
        p = self.root / "public-approval.json"
        studio.save(p, {"approved": True, "approver": "test author", "approved_source_sha256": run["canonical_sha256"], "surfaces": ["reader"], "approved_artifacts": [{"surface": "reader", "path": str(self.source), "sha256": studio.sha(self.source)}]})
        run["founder_public_release_evidence"] = {"path": str(p), "sha256": studio.sha(p)}
        return p

    def test_canonical_and_legacy_ids_do_not_confuse_edition_numbers(self):
        self.assertEqual(studio.slug_id("07-cold-rice"), "com-nguoi")
        self.assertEqual(studio.slug_id("cold-rice"), "com-nguoi")
        self.assertEqual(studio.slug_id("18-to-saigon"), "viet-cho-sai-gon-cua-t")
        with self.assertRaises(ValueError):
            studio.slug_id("07")

    def test_valid_exact_quote_timeline(self):
        self.assertEqual(studio.validate_timeline(self.timeline, self.art), [])

    def test_source_revision_invalidates_old_timeline(self):
        self.source.write_text("Changed source", encoding="utf-8")
        self.assertIn("stale", studio.validate_timeline(self.timeline, self.art)[0])

    def test_full_reading_rejects_omitted_source(self):
        self.source.write_text("# Title\n\nNó không phải sở thích.\n\nAnother paragraph.\n", encoding="utf-8")
        self.timeline["source"]["sha256"] = studio.sha(self.source)
        cut = self.timeline["cuts"]["master"]
        cut["full_source_reading"] = True
        cut["shots"][0]["source_reference"]["source_sha256"] = studio.sha(self.source)
        self.assertTrue(any("omits" in e for e in studio.validate_timeline(self.timeline, self.art)))

    def test_caption_text_and_timing_are_checked(self):
        shot = self.timeline["cuts"]["master"]["shots"][0]
        shot["caption_cues"] = [{"start_s": 0, "duration_s": 5, "text": "Nó không phải\nsở thích."}]
        self.assertEqual(studio.validate_timeline(self.timeline, self.art), [])
        shot["caption_cues"][0]["text"] = "Different text"
        self.assertTrue(any("caption text" in e for e in studio.validate_timeline(self.timeline, self.art)))
        shot["caption_cues"][0].update({"text": shot["vo_text"], "duration_s": 4})
        self.assertTrue(any("caption duration" in e for e in studio.validate_timeline(self.timeline, self.art)))

    def test_video_variant_needs_exact_scope_and_both_sources(self):
        canonical = {"sha256": "book-sha"}
        self.assertTrue(studio.validate_script_selection(self.timeline, canonical, None))
        evidence = {"approved": True, "scope": "video_script_text_only", "approved_sha256": self.timeline["source"]["sha256"], "canonical_source_sha256": "book-sha"}
        self.assertEqual(studio.validate_script_selection(self.timeline, canonical, evidence), [])
        evidence["canonical_source_sha256"] = "another-book-revision"
        self.assertTrue(studio.validate_script_selection(self.timeline, canonical, evidence))

    def test_unwritten_first_person_claim_is_rejected(self):
        self.timeline["cuts"]["master"]["shots"][0]["vo_text"] = "Invented memory."
        self.assertTrue(any("quote" in e for e in studio.validate_timeline(self.timeline, self.art)))

    def test_overlap_or_gap_is_rejected(self):
        shot = self.timeline["cuts"]["master"]["shots"][0]
        shot["start_s"] = 1
        self.assertTrue(any("gap/overlap" in e for e in studio.validate_timeline(self.timeline, self.art)))

    def test_asset_drift_is_rejected(self):
        self.image.write_bytes(b"changed art")
        self.assertTrue(any("asset missing or stale" in e for e in studio.validate_timeline(self.timeline, self.art)))

    def test_private_photo_outside_selected_library_is_rejected(self):
        photo = self.root / "private-photo.jpg"
        photo.write_bytes(b"private")
        shot = self.timeline["cuts"]["master"]["shots"][0]
        shot.update({"asset_path": str(photo), "asset_sha256": studio.sha(photo)})
        self.assertTrue(any("not in" in e for e in studio.validate_timeline(self.timeline, self.art)))

    def test_flat_board_cannot_claim_real_parallax(self):
        self.timeline["visual_mode"] = "parallax"
        self.assertTrue(any("parallax" in e for e in studio.validate_timeline(self.timeline, self.art)))

    def test_layer_animation_needs_a_real_motion_manifest(self):
        self.timeline["visual_mode"] = "layer_animation"
        self.assertTrue(any("motion manifest" in e for e in studio.validate_timeline(self.timeline, self.art)))

    def portal_opening(self):
        shot = self.timeline["cuts"]["master"]["shots"][0]
        shot.update({"kind": "portal_entry", "on_screen_text": "Cơm nguội", "portal_entry": {"focus_x": 0.5, "focus_y": 0.565, "max_scale": 5.5, "reveal_asset_path": str(self.image), "reveal_asset_sha256": studio.sha(self.image)}})
        return shot

    def test_explicit_opening_camera_can_enter_the_center(self):
        self.portal_opening()
        self.assertEqual(studio.validate_timeline(self.timeline, self.art), [])

    def test_studio_policy_rejects_an_opening_omitted_from_any_cut(self):
        errors = studio.validate_timeline(self.timeline, self.art, require_opening=True)
        self.assertTrue(any("opening required" in e for e in errors))

    def test_an_opening_exception_needs_an_explicit_scoped_request(self):
        cut = self.timeline["cuts"]["master"]
        cut["author_opening_exception"] = {"request": "Skip intro"}
        self.assertTrue(studio.validate_timeline(self.timeline, self.art, require_opening=True))
        cut["author_opening_exception"].update({"requested_by": "author", "scope": "this diagnostic cut only"})
        self.assertEqual(studio.validate_timeline(self.timeline, self.art, require_opening=True), [])

    def test_opening_landing_must_match_the_first_story_art(self):
        import copy
        opening = self.portal_opening()
        story = copy.deepcopy(opening)
        opening.update({"vo_text": "", "source_reference": None, "duration_s": 1})
        story.update({"id": "STORY", "start_s": 1, "kind": "story"})
        del story["portal_entry"]
        cut = self.timeline["cuts"]["master"]
        cut.update({"shots": [opening, story], "duration_estimate_s": 6})
        self.assertEqual(studio.validate_timeline(self.timeline, self.art, require_opening=True), [])
        alternate = self.art / "other.webp"
        alternate.write_bytes(b"other art")
        story.update({"asset_path": str(alternate), "asset_sha256": studio.sha(alternate)})
        self.assertTrue(any("continue inside" in e for e in studio.validate_timeline(self.timeline, self.art, require_opening=True)))

    def test_portal_reveal_cannot_bypass_asset_or_title_checks(self):
        shot = self.portal_opening()
        shot["on_screen_text"] = "An invented title"
        shot["portal_entry"]["reveal_asset_sha256"] = "stale"
        errors = studio.validate_timeline(self.timeline, self.art)
        self.assertTrue(any("opening title" in e for e in errors))
        self.assertTrue(any("reveal asset missing or stale" in e for e in errors))

    def test_portal_entry_is_restricted_to_an_explicit_opening(self):
        shot = self.portal_opening()
        shot["kind"] = "story"
        self.assertTrue(any("opening portal camera" in e for e in studio.validate_timeline(self.timeline, self.art)))

    def test_reader_only_scope_does_not_require_film_narration(self):
        run = self.reader_run()
        errors, _, logical_ready = check(run)
        self.assertEqual(errors, [])
        self.assertTrue(logical_ready)
        self.assertNotIn("narration_recorded_by_author", required_public_flags(run)[1])

    def test_legacy_scope_retains_film_requirements(self):
        run = self.reader_run()
        del run["release_scope"]
        self.assertFalse(check(run)[2])
        self.assertIn("narration_recorded_by_author", required_public_flags(run)[1])

    def test_boolean_flags_do_not_replace_exact_release_approval(self):
        run = self.reader_run()
        report = studio.release_report(run)
        self.assertFalse(report["ready"])
        self.assertIn("exact_public_release_evidence", report["blockers"])

    def test_exact_reader_approval_is_scoped_and_hash_bound(self):
        run = self.reader_run()
        self.add_public_evidence(run)
        self.assertTrue(studio.release_report(run)["ready"])
        run["release_scope"]["surfaces"].append("film")
        self.assertFalse(studio.release_report(run)["ready"])

    def test_changed_approved_artifact_invalidates_release(self):
        run = self.reader_run()
        self.add_public_evidence(run)
        self.source.write_text("changed after approval", encoding="utf-8")
        self.assertIn("public_release_artifact_missing_or_stale", studio.release_report(run)["blockers"])

    def test_template_or_unapproved_record_cannot_clear_release(self):
        run = self.reader_run()
        p = self.add_public_evidence(run)
        record = studio.load(p)
        record["approved"] = False
        studio.save(p, record)
        run["founder_public_release_evidence"]["sha256"] = studio.sha(p)
        self.assertFalse(studio.release_report(run)["ready"])

    def test_paid_gate_is_independent_of_free_reader_approval(self):
        run = self.reader_run()
        self.add_public_evidence(run)
        report = studio.release_report(run, paid=True)
        self.assertFalse(report["ready"])
        self.assertIn("commerce_checkout_and_fulfillment_tested", report["blockers"])

    def test_staging_preserves_source_and_does_not_replace_cache(self):
        destination = self.root / "cache" / self.image.name
        original = studio.sha(self.image)
        studio.stage_asset(self.image, destination)
        self.assertEqual(studio.sha(destination), original)
        self.assertEqual(studio.sha(self.image), original)
        self.assertEqual(studio.stage_asset(self.image, destination), "existing")
        other = self.root / "other.webp"
        other.write_bytes(b"different bytes")
        with self.assertRaises(ValueError):
            studio.stage_asset(other, destination)

    def test_existing_approved_project_is_not_reinitialized(self):
        with self.assertRaises(ValueError):
            studio.new_project("com-nguoi")


if __name__ == "__main__":
    unittest.main()
