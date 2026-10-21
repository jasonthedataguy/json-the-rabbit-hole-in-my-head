"""Record exact author text approval and optionally integrate it into the local book."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = Path(r"C:\Users\Administrator\OneDrive\Desktop\.json book\json_under_revision_v2")
CHAPTER = REPO / "chapters/com-nguoi"
OLD = "d957b592dc2317aa34196dd25ab42a3fe4a7938d3aee5a1121ab173214bf76f9"
NEW = "b4319bf9abb463148f590c773c14f12732e3524a612936fd2edddcaebecdfd3a"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def save(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def replace(name, pairs):
    path = ROOT / name
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8", newline="\n")


def prepare():
    proposal = ROOT / "chapter-proposed-v1.md"
    if sha(proposal) != NEW:
        raise ValueError("Proposal differs from exact version approved by author")
    approval = {
        "date": "2026-10-21", "timezone": "Asia/Bangkok", "chapter_slug": "com-nguoi",
        "approver": "Author, via direct reply in this Codex chat", "response_verbatim": "Approve proposed v1",
        "question_scope": "Editorial text selection only; choice explicitly excluded posting and paid release",
        "approved_artifact_path": str(proposal), "approved_sha256": NEW,
        "previous_source_sha256": OLD,
        "approved_changes": ["Split opening sentence", "Paragraph break before Nhưng cứ thế"],
        "ending_unchanged": True, "script_approved": False, "family_public_scope_approved": False,
        "public_release_approved": False, "paid_release_approved": False,
    }
    save("editorial-approval.json", approval)
    manifest = load("run-manifest.json")
    manifest["manuscript_text_approved"] = True
    manifest["manuscript_text_approval_evidence"] = str(ROOT / "editorial-approval.json")
    manifest["canonical_integration_status"] = "pending_local_application"
    save("run-manifest.json", manifest)
    print("Exact manuscript-text approval recorded; application prepared.", flush=True)


def apply():
    approval = load("editorial-approval.json")
    proposal = ROOT / "chapter-proposed-v1.md"
    if approval["approved_sha256"] != NEW or sha(proposal) != NEW:
        raise ValueError("Approved bytes changed")
    canonical = CHAPTER / "source/approved.md"
    registry = CHAPTER / "chapter.json"
    revisions = CHAPTER / "source/revisions.log"
    original = CHAPTER / "source/original.md"
    original_hash = sha(original)
    source_bytes, registry_bytes, revision_bytes = canonical.read_bytes(), registry.read_bytes(), revisions.read_bytes()
    current = hashlib.sha256(source_bytes).hexdigest()
    if current not in (OLD, NEW):
        raise ValueError("Canonical text changed independently; refusing to overwrite")
    if json.loads(registry_bytes)["manuscript_sha256"] not in (OLD, NEW):
        raise ValueError("Registry changed independently; refusing to overwrite")
    archive = CHAPTER / "source/history/approved-d957b592dc2317aa.md"
    archive.parent.mkdir(exist_ok=True)
    if current == OLD:
        if archive.exists():
            if sha(archive) != OLD:
                raise ValueError("Existing historical selection conflicts")
        else:
            with archive.open("xb") as stream:
                stream.write(source_bytes)
    elif not archive.exists() or sha(archive) != OLD:
        raise ValueError("Previously selected text archive missing")
    # Compare bytes again immediately before each write. Preserve unrelated metadata.
    if canonical.read_bytes() != source_bytes or registry.read_bytes() != registry_bytes or revisions.read_bytes() != revision_bytes:
        raise ValueError("Concurrent chapter edit detected")
    canonical.write_bytes(proposal.read_bytes())
    if json.loads(registry_bytes)["manuscript_sha256"] == OLD:
        if registry_bytes.count(OLD.encode()) != 1:
            raise ValueError("Unexpected hash occurrences in registry")
        registry.write_bytes(registry_bytes.replace(OLD.encode(), NEW.encode()))
    marker = b"2026-10-21 | Author approved proposed v1 in Codex"
    if marker not in revision_bytes:
        newline = b"\r\n" if b"\r\n" in revision_bytes else b"\n"
        entry = ("2026-10-21 | Author approved proposed v1 in Codex: opening sentence split and paragraph break; ending unchanged. Selected SHA256 " + NEW + "; previous selection archived at source/history/approved-d957b592dc2317aa.md. Script, family disclosure and release approvals remain separate.").encode("utf-8")
        revisions.write_bytes(revision_bytes + (b"" if revision_bytes.endswith(b"\n") else newline) + entry + newline)
    assert sha(canonical) == NEW and sha(archive) == OLD and sha(original) == original_hash
    receipt = {"date": "2026-10-21", "status": "applied_locally", "canonical_path": str(canonical), "canonical_sha256": NEW, "previous_selection_archive": str(archive), "previous_sha256": OLD, "original_manuscript_unchanged": True, "registry_sha256": sha(registry), "revision_log_path": str(revisions), "git_commit_created": False, "pushed": False, "deployed": False}
    save("canonical-selection-receipt.json", receipt)
    print("Approved text selected locally; previous selection archived. No commit or push.", flush=True)

    # Citation rebasing only: no image, caption wording or narration regeneration.
    lines = canonical.read_text(encoding="utf-8").splitlines()
    def rebase(ref):
        matches = [i for i, line in enumerate(lines, 1) if ref["text"] in line]
        if len(matches) != 1:
            raise ValueError("Source quote needs manual review")
        ref.update({"line": matches[0], "path": str(canonical), "source_sha256": NEW})
    script = load("film-script.json")
    script["source_sha256"] = NEW
    script["source_rebase_note"] = "All quoted words remain exact in author-approved v1; source line numbers/hash refreshed. Script approval still pending."
    for beat in script["master"] + script["alternate"]:
        if beat["source_reference"]:
            rebase(beat["source_reference"])
    save("film-script.json", script)
    social = load("social-pack.json")
    social["source_sha256"] = NEW
    social["manuscript_text_approval_evidence"] = str(ROOT / "editorial-approval.json")
    social["source_rebase_note"] = "Exact quoted words unchanged; original art/layouts retained; social approval still pending."
    for card in social["carousel"]:
        rebase(card["quote"])
    for channel in social["channels"]:
        channel["source_sha256"] = NEW
    save("social-pack.json", social)
    for name in ("film-script.md", "social-pack.md"):
        replace(name, [(OLD, NEW), ("Line 15", "Line 17"), ("Line 21", "Line 23"), ("line 15", "line 17"), ("line 21", "line 23")])
    replace("digital-book-design-plan.md", [("lines 9/11/15", "lines 9/11/17")])
    replace("editorial-review.md", [("Input: [selected manuscript]", "Historical review input: [selected manuscript]"), ("The local `main` HEAD matches the remote default-branch HEAD observed during this run:", "At the first inspection, local HEAD matched the remote HEAD then observed:"), ("This establishes input lineage, not approval of this run's new edit or release.", "The checkout subsequently advanced during other work; its changing HEAD is not source approval. The reviewed input is pinned by the source hash above."), ("New G1 remains pending.", "The author approved proposed v1 in this chat on 21 October 2026; public family scope remains pending."), ("No canonical file was changed here.", "The approved v1 has now been selected locally, with the previous selection archived and original manuscript preserved. Script and release decisions remain separate.")])
    replace("production-plan.md", [("Local plan/manifest updated; live Jira, canonical source, chapter production.json and deployed website unchanged.", "Author approved proposed v1 and its exact bytes are now selected locally; prior selection/original preserved. No live Jira, production recipe, commit, push or deployment change."), ("The optional new revision is separate.", "Proposed v1 is now the author-approved local manuscript selection."), ("new text/script/privacy/visual decisions", "script/privacy/visual decisions"), ("| S02 Canonical | Ready for review | Full two-change proposal + diff; G1 pending for new version |", "| S02 Canonical | Approved text | Author approved exact v1 hash; source/registry/history updated locally; public scope separate |"), ("Choose proposed edit or existing text, and approve the abridged excerpts/visual representation.", "Text v1 is approved. Review the abridged script, public family scope and visual representation."), ("| G1 | Exact proposed bytes/hash or explicit retain-current decision; facts/disclosure scope | Pending for this run; historical text selection recorded separately |", "| G1 text selection | Exact approved manuscript/hash and author response | Approved proposed v1; public family/disclosure scope remains pending |")])
    replace("README.md", [("Original voice and selected source preserved; no source, reader, Jira or public release changed.", "Proposed v1 approved by the author and selected in the local book source; prior selected text and original manuscript preserved. No commit, push, deployment or Jira update."), ("Refined chapter, pending G1", "Author-approved manuscript v1"), ("First decision: approve the exact proposed text or retain the selected source, review abridged script and confirm public family scope.", "Text decision recorded: author approved proposed v1. Next: review abridged script and confirm public family scope.")])
    with (ROOT / "README.md").open("a", encoding="utf-8") as stream:
        stream.write("\nApproval evidence: [editorial-approval.json](<" + (ROOT / "editorial-approval.json").as_posix() + ">). Local source application: [canonical-selection-receipt.json](<" + (ROOT / "canonical-selection-receipt.json").as_posix() + ">).\n")
    lineage = load("source-lineage.json")
    lineage.update({"previous_canonical_sha256": OLD, "canonical_source_sha256": NEW, "canonical_bytes": canonical.stat().st_size, "proposal_approved": True, "approval_evidence": str(ROOT / "editorial-approval.json"), "canonical_selection_receipt": str(ROOT / "canonical-selection-receipt.json"), "previous_selection_archive": str(archive), "derivative_basis": "author-approved v1; exact quotations rebased, no creative/image regeneration", "book_repository_files_unchanged": False, "local_head_at_selection": (REPO / ".git/refs/heads/main").read_text().strip(), "head_equality_note": "Earlier recorded local/remote HEAD observations are historical; this selection is pinned to approved manuscript SHA, not global checkout equality."})
    save("source-lineage.json", lineage)
    manifest = load("run-manifest.json")
    manifest.update({"canonical_sha256": NEW, "author_approved": True, "source_facts_approval_evidence": str(ROOT / "editorial-approval.json"), "approval_scope_note": "Author approved manuscript text v1 only. Script, family/public disclosure, quality and paid/public release remain pending.", "canonical_integration_status": "applied_locally", "canonical_selection_receipt": str(ROOT / "canonical-selection-receipt.json"), "notes": "Manuscript v1 approved/selected locally; exact quotes rebased without regenerating art. Script/privacy/quality/release gates remain pending; no push or release."})
    manifest["stages"]["S02_canonical"] = "approved"
    manifest["approval_gates"]["G1"] = {"status": "manuscript_text_approved", "evidence": str(ROOT / "editorial-approval.json"), "public_family_scope": "pending"}
    for blocker in manifest["blockers"]:
        if blocker["id"] == "G1":
            blocker.update({"id": "SCRIPT_AND_SCOPE", "reason": "Manuscript v1 approved; first-person script and public family/visual scope still require separate author decisions."})
    manifest["next_actions"][0]["action"] = "Review exact film script and confirm public family/visual scope; manuscript v1 already approved"
    for item in manifest["derivatives"]:
        path = Path(item["path"])
        item["artifact_sha256"] = sha(path)
        if path.suffix != ".diff" and path.name not in ("editorial-review.md", "story-brief.md"):
            item["source_sha256"] = NEW
            item["source_rebase_status"] = "unchanged quotes verified; no approval inherited"
        if path == proposal:
            item["status"] = "approved"
            item["evidence"] = str(ROOT / "editorial-approval.json")
    for evidence in manifest["stage_evidence"].values():
        evidence["sha256"] = sha(Path(evidence["path"]))
    manifest["stage_evidence"]["S02_canonical"]["approval_evidence"] = str(ROOT / "editorial-approval.json")
    save("run-manifest.json", manifest)

    # Prescribed local checks: no deploy command is invoked.
    results = []
    for args in [["scripts/build_inventory.py"], ["scripts/build_site.py"], ["scripts/check_site.py"], ["-m", "unittest", "discover", "-s", "tests", "-v"]]:
        print("Running local check: " + " ".join(args), flush=True)
        run = subprocess.run([sys.executable, "-X", "utf8", *args], cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace")
        log = ROOT / ("approval-check-" + str(len(results) + 1) + ".log")
        log.write_text(run.stdout + run.stderr, encoding="utf-8")
        results.append({"command": args, "exit_code": run.returncode, "log": str(log)})
        print("Exit " + str(run.returncode) + ": " + (run.stdout + run.stderr)[-1200:], flush=True)
        if run.returncode:
            break
    save("approval-verification.json", {"date": "2026-10-21", "source_sha256": sha(canonical), "approved_sha256": NEW, "archive_sha256": sha(archive), "original_unchanged": sha(original) == original_hash, "source_quote_rebase": "all exact quotations verified", "art_regenerated": False, "local_checks": results, "status": "pass" if len(results) == 4 and all(x["exit_code"] == 0 for x in results) else "review_required", "public_release_approved": False, "paid_release_approved": False, "script_approved": False})
    print("Approval application and local verification recorded.", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply-to-book", action="store_true")
    options = parser.parse_args()
    if options.apply_to_book:
        apply()
    else:
        prepare()
