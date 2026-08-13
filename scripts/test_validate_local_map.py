from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.validate_local_map import validate

MAP = """\
Label: through-line:map
Status: {status}
Repository execution: {repository_execution}
Tracker state: {tracker_state}

# Test map

## Destination

Test the validator.

{execution_heads}

## Notes

None.

## Local policies

None.

## Decisions so far

{decisions}

## Findings

{findings}

## Not yet specified

None.

## Out of scope

None.
"""


def ticket(
    *,
    kind: str = "decision",
    status: str = "resolved",
    blocker: str | None = None,
    checkpoint: str = "",
) -> str:
    assignee = "Assignee: Agent\n" if status in {"claimed", "resolved"} else ""
    blocked_by = f"Blocked by: {blocker}\n" if blocker else ""
    resolution = "\n## Resolution\n\nDone.\n" if status == "resolved" else ""
    return (
        f"Type: {kind}\nLabel: through-line:{kind}\nStatus: {status}\n"
        f"{assignee}{blocked_by}\n# Ticket\n\n## Question\n\nQuestion.\n"
        f"{checkpoint}{resolution}"
    )


class ValidatorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        (self.root / "issues").mkdir()
        self.run_git(self.root, "init")
        self.run_git(self.root, "config", "user.email", "test@example.com")
        self.run_git(self.root, "config", "user.name", "Test")
        self.exec_tempdir = tempfile.TemporaryDirectory()
        self.exec_root = Path(self.exec_tempdir.name)

    def tearDown(self) -> None:
        self.exec_tempdir.cleanup()
        self.tempdir.cleanup()

    def write_map(
        self,
        *,
        status: str = "resolved",
        decisions: str = "- [Ticket](issues/01-ticket.md) — done.",
        findings: str = "None.",
        execution_heads: str = "",
        repository_execution: str = "out-of-scope",
        tracker_state: str = "pending",
    ) -> Path:
        map_path = self.root / "map.md"
        map_path.write_text(
            MAP.format(
                status=status,
                decisions=decisions,
                findings=findings,
                execution_heads=execution_heads,
                repository_execution=repository_execution,
                tracker_state=tracker_state,
            )
        )
        if status == "resolved" and repository_execution == "in-scope":
            self.run_git(self.root, "add", ".")
            self.run_git(self.root, "commit", "-m", "tracker state")
            tracker_state = self.run_git(self.root, "rev-parse", "HEAD").stdout.strip()
            map_path.write_text(
                map_path.read_text().replace(
                    "Tracker state: pending", f"Tracker state: {tracker_state}"
                )
            )
            self.run_git(self.root, "commit", "-am", "attest tracker state")
        return map_path

    def test_valid_map(self) -> None:
        (self.root / "issues/01-ticket.md").write_text(ticket())
        self.assertEqual(validate(self.write_map()), [])

    def test_resolved_ticket_rejects_dated_checkpoint_heading(self) -> None:
        (self.root / "issues/01-ticket.md").write_text(
            ticket(checkpoint="\n## Resumption checkpoint (2026-08-12)\n\nPaused.\n")
        )
        errors = validate(self.write_map())
        self.assertTrue(
            any("resolved with a ## Resumption checkpoint" in e for e in errors)
        )

    def test_dependency_cycle(self) -> None:
        (self.root / "issues/01-ticket.md").write_text(
            ticket(status="blocked", blocker="02")
        )
        (self.root / "issues/02-ticket.md").write_text(
            ticket(status="blocked", blocker="01")
        )
        errors = validate(self.write_map(status="open", decisions="None."))
        self.assertTrue(any("dependency cycle" in e for e in errors))

    def test_manual_task_does_not_imply_repository_execution(self) -> None:
        (self.root / "issues/01-ticket.md").write_text(ticket(kind="task"))
        errors = validate(
            self.write_map(
                decisions="None.",
                findings="- [Ticket](issues/01-ticket.md) — done.",
            )
        )
        self.assertEqual(errors, [])

    def test_in_scope_execution_map_requires_execution_head_while_open(self) -> None:
        (self.root / "issues/01-ticket.md").write_text(ticket(status="open"))
        errors = validate(
            self.write_map(
                status="open",
                decisions="None.",
                repository_execution="in-scope",
            )
        )
        self.assertTrue(any("exactly one ## Execution heads" in e for e in errors))

    def test_resolved_execution_map_requires_execution_head(self) -> None:
        (self.root / "issues/01-ticket.md").write_text(ticket(kind="task"))
        errors = validate(
            self.write_map(
                decisions="None.",
                findings="- [Ticket](issues/01-ticket.md) — done.",
                repository_execution="in-scope",
            )
        )
        self.assertTrue(any("exactly one ## Execution heads" in e for e in errors))

    def test_valid_execution_head(self) -> None:
        repo, base, head = self.make_repo()
        self.write_review(base, head)

        (self.root / "issues/01-ticket.md").write_text(ticket(kind="task"))
        errors = validate(
            self.write_map(
                decisions="None.",
                findings="- [Ticket](issues/01-ticket.md) — done.",
                execution_heads=(
                    "## Execution heads\n\n"
                    f"- Repository: {repo}; Code base: {base}; "
                    f"Reviewed code head: {head}; Closure state: {head}; PR: none; "
                    "Review receipt: review.md"
                ),
                repository_execution="in-scope",
            )
        )
        self.assertEqual(errors, [])

    def test_open_execution_head_allows_pending_review(self) -> None:
        repo, base, _ = self.make_repo()

        (self.root / "issues/01-ticket.md").write_text(ticket(status="open"))
        errors = validate(
            self.write_map(
                status="open",
                decisions="None.",
                execution_heads=(
                    "## Execution heads\n\n"
                    f"- Repository: {repo}; Code base: {base}; "
                    "Reviewed code head: pending; Closure state: pending; PR: pending; "
                    "Review receipt: pending"
                ),
                repository_execution="in-scope",
            )
        )
        self.assertEqual(errors, [])

    def test_resolved_execution_head_rejects_pending_review(self) -> None:
        repo, base, _ = self.make_repo()
        (self.root / "issues/01-ticket.md").write_text(ticket(kind="task"))
        errors = validate(
            self.write_map(
                decisions="None.",
                findings="- [Ticket](issues/01-ticket.md) — done.",
                execution_heads=(
                    "## Execution heads\n\n"
                    f"- Repository: {repo}; Code base: {base}; "
                    "Reviewed code head: pending; Closure state: pending; PR: none; "
                    "Review receipt: pending"
                ),
                repository_execution="in-scope",
            )
        )
        self.assertTrue(
            any("resolved execution head is still pending" in e for e in errors)
        )
        self.assertTrue(any("review receipt is still pending" in e for e in errors))

    def test_execution_head_must_name_real_commit(self) -> None:
        repo, base, head = self.make_repo()
        self.write_review(base, "deadbeef")
        (self.root / "issues/01-ticket.md").write_text(ticket(kind="task"))
        errors = validate(
            self.write_map(
                decisions="None.",
                findings="- [Ticket](issues/01-ticket.md) — done.",
                execution_heads=(
                    "## Execution heads\n\n"
                    f"- Repository: {repo}; Code base: {base}; "
                    f"Reviewed code head: deadbeef; Closure state: {head}; PR: none; "
                    "Review receipt: review.md"
                ),
                repository_execution="in-scope",
            )
        )
        self.assertTrue(any("Reviewed code head is not a commit" in e for e in errors))

    def test_execution_head_rejects_abbreviated_commit(self) -> None:
        repo, base, head = self.make_repo()
        self.write_review(base, head[:8])
        (self.root / "issues/01-ticket.md").write_text(ticket(kind="task"))
        errors = validate(
            self.write_map(
                decisions="None.",
                findings="- [Ticket](issues/01-ticket.md) — done.",
                execution_heads=(
                    "## Execution heads\n\n"
                    f"- Repository: {repo}; Code base: {base}; "
                    f"Reviewed code head: {head[:8]}; Closure state: {head}; PR: none; "
                    "Review receipt: review.md"
                ),
                repository_execution="in-scope",
            )
        )
        self.assertTrue(any("full hash" in e for e in errors))

    def test_execution_review_receipt_must_exist(self) -> None:
        repo, base, head = self.make_repo()
        (self.root / "issues/01-ticket.md").write_text(ticket(kind="task"))
        errors = validate(
            self.write_map(
                decisions="None.",
                findings="- [Ticket](issues/01-ticket.md) — done.",
                execution_heads=(
                    "## Execution heads\n\n"
                    f"- Repository: {repo}; Code base: {base}; "
                    f"Reviewed code head: {head}; Closure state: {head}; PR: none; "
                    "Review receipt: missing.md"
                ),
                repository_execution="in-scope",
            )
        )
        self.assertTrue(any("review receipt does not exist" in e for e in errors))

    def test_execution_review_receipt_must_match_range_and_schema(self) -> None:
        repo, base, head = self.make_repo()
        (self.root / "review.md").write_text("Decision: approved\n")
        (self.root / "issues/01-ticket.md").write_text(ticket(kind="task"))
        errors = validate(
            self.write_map(
                decisions="None.",
                findings="- [Ticket](issues/01-ticket.md) — done.",
                execution_heads=(
                    "## Execution heads\n\n"
                    f"- Repository: {repo}; Code base: {base}; "
                    f"Reviewed code head: {head}; Closure state: {head}; PR: none; "
                    "Review receipt: review.md"
                ),
                repository_execution="in-scope",
            )
        )
        self.assertTrue(any("review receipt range" in e for e in errors))
        self.assertTrue(any("lacks Checks" in e for e in errors))
        self.assertTrue(any("lacks Findings and gaps" in e for e in errors))

    def test_resolved_tracker_must_be_clean(self) -> None:
        repo, base, head = self.make_repo()
        self.write_review(base, head)
        (self.root / "issues/01-ticket.md").write_text(ticket(kind="task"))
        map_path = self.write_map(
            decisions="None.",
            findings="- [Ticket](issues/01-ticket.md) — done.",
            execution_heads=(
                "## Execution heads\n\n"
                f"- Repository: {repo}; Code base: {base}; "
                f"Reviewed code head: {head}; Closure state: {head}; PR: none; "
                "Review receipt: review.md"
            ),
            repository_execution="in-scope",
        )
        map_path.write_text(map_path.read_text() + "\nUncommitted.\n")
        errors = validate(map_path)
        self.assertTrue(any("uncommitted state" in e for e in errors))

    def test_resolved_tracker_rejects_later_clean_rewrite(self) -> None:
        repo, base, head = self.make_repo()
        self.write_review(base, head)
        ticket_path = self.root / "issues/01-ticket.md"
        ticket_path.write_text(ticket(kind="task"))
        map_path = self.write_map(
            decisions="None.",
            findings="- [Ticket](issues/01-ticket.md) — done.",
            execution_heads=(
                "## Execution heads\n\n"
                f"- Repository: {repo}; Code base: {base}; "
                f"Reviewed code head: {head}; Closure state: {head}; PR: none; "
                "Review receipt: review.md"
            ),
            repository_execution="in-scope",
        )
        ticket_path.write_text(ticket(kind="task") + "\nRewritten after closure.\n")
        self.run_git(self.root, "commit", "-am", "rewrite closed tracker")
        errors = validate(map_path)
        self.assertTrue(
            any("tracker changed after its immutable state" in e for e in errors)
        )

    def test_resolved_tracker_rejects_change_then_revert(self) -> None:
        repo, base, head = self.make_repo()
        self.write_review(base, head)
        ticket_path = self.root / "issues/01-ticket.md"
        original = ticket(kind="task")
        ticket_path.write_text(original)
        map_path = self.write_map(
            decisions="None.",
            findings="- [Ticket](issues/01-ticket.md) — done.",
            execution_heads=(
                "## Execution heads\n\n"
                f"- Repository: {repo}; Code base: {base}; "
                f"Reviewed code head: {head}; Closure state: {head}; PR: none; "
                "Review receipt: review.md"
            ),
            repository_execution="in-scope",
        )
        ticket_path.write_text(original + "\nTemporary rewrite.\n")
        self.run_git(self.root, "commit", "-am", "rewrite closed tracker")
        ticket_path.write_text(original)
        self.run_git(self.root, "commit", "-am", "revert tracker rewrite")
        errors = validate(map_path)
        self.assertTrue(
            any("tracker changed after its immutable state" in e for e in errors)
        )

    def test_resolved_decision_map_does_not_require_git_attestation(self) -> None:
        root = self.exec_root / "decision-map"
        (root / "issues").mkdir(parents=True)
        (root / "issues/01-ticket.md").write_text(ticket())
        map_path = root / "map.md"
        map_path.write_text(
            MAP.format(
                status="resolved",
                repository_execution="out-of-scope",
                tracker_state="pending",
                execution_heads="",
                decisions="- [Ticket](issues/01-ticket.md) — done.",
                findings="None.",
            )
        )
        self.assertEqual(validate(map_path), [])

    def test_resolved_review_receipt_must_be_committed(self) -> None:
        repo, base, head = self.make_repo()
        (self.root / ".gitignore").write_text("review.md\n")
        self.write_review(base, head)
        (self.root / "issues/01-ticket.md").write_text(ticket(kind="task"))
        errors = validate(
            self.write_map(
                decisions="None.",
                findings="- [Ticket](issues/01-ticket.md) — done.",
                execution_heads=(
                    "## Execution heads\n\n"
                    f"- Repository: {repo}; Code base: {base}; "
                    f"Reviewed code head: {head}; Closure state: {head}; PR: none; "
                    "Review receipt: review.md"
                ),
                repository_execution="in-scope",
            )
        )
        self.assertTrue(any("review receipt is not committed" in e for e in errors))

    def test_duplicate_execution_repository_is_rejected(self) -> None:
        repo, base, head = self.make_repo()
        self.write_review(base, head)
        (self.root / "issues/01-ticket.md").write_text(ticket(kind="task"))
        entry = (
            f"- Repository: {repo}; Code base: {base}; "
            f"Reviewed code head: {head}; Closure state: {head}; PR: none; "
            "Review receipt: review.md"
        )
        errors = validate(
            self.write_map(
                decisions="None.",
                findings="- [Ticket](issues/01-ticket.md) — done.",
                execution_heads=f"## Execution heads\n\n{entry}\n{entry}",
                repository_execution="in-scope",
            )
        )
        self.assertTrue(any("duplicate execution repository" in e for e in errors))

    def test_sha256_repository_requires_64_character_hashes(self) -> None:
        repo, base, head = self.make_repo(object_format="sha256")
        self.write_review(base[:40], head[:40])
        (self.root / "issues/01-ticket.md").write_text(ticket(kind="task"))
        errors = validate(
            self.write_map(
                decisions="None.",
                findings="- [Ticket](issues/01-ticket.md) — done.",
                execution_heads=(
                    "## Execution heads\n\n"
                    f"- Repository: {repo}; Code base: {base[:40]}; "
                    f"Reviewed code head: {head[:40]}; Closure state: {head}; PR: none; "
                    "Review receipt: review.md"
                ),
                repository_execution="in-scope",
            )
        )
        self.assertTrue(any("full hash" in e for e in errors))

    def test_tracker_only_closure_boundary_remains_historically_valid(self) -> None:
        repo, base, head = self.make_repo()
        tracker = repo / ".scratch/test"
        (tracker / "issues").mkdir(parents=True)
        (tracker / "issues/01-ticket.md").write_text(ticket(kind="task"))
        (tracker / "review.md").write_text(self.review(base, head))
        map_path = tracker / "map.md"
        map_path.write_text(
            MAP.format(
                status="resolved",
                repository_execution="in-scope",
                tracker_state="pending",
                execution_heads=(
                    "## Execution heads\n\n"
                    f"- Repository: {repo}; Code base: {base}; "
                    f"Reviewed code head: {head}; Closure state: {head}; PR: none; "
                    "Review receipt: review.md"
                ),
                decisions="None.",
                findings="- [Ticket](issues/01-ticket.md) — done.",
            )
        )
        self.run_git(repo, "add", ".scratch/test")
        self.run_git(repo, "commit", "-m", "prepare tracker closure")
        tracker_state = self.run_git(repo, "rev-parse", "HEAD").stdout.strip()
        map_path.write_text(
            map_path.read_text().replace(
                "Tracker state: pending", f"Tracker state: {tracker_state}"
            )
        )
        self.run_git(repo, "commit", "-am", "attest tracker closure")
        self.assertEqual(validate(map_path), [])

        (repo / "file.txt").write_text("post-review code\n")
        self.run_git(repo, "commit", "-am", "change code after review")
        self.assertEqual(validate(map_path), [])

    def test_tracker_state_commit_rejects_unreviewed_code(self) -> None:
        repo, base, head = self.make_repo()
        tracker = repo / ".scratch/test"
        (tracker / "issues").mkdir(parents=True)
        (tracker / "issues/01-ticket.md").write_text(ticket(kind="task"))
        (tracker / "review.md").write_text(self.review(base, head))
        map_path = tracker / "map.md"
        map_path.write_text(
            MAP.format(
                status="resolved",
                repository_execution="in-scope",
                tracker_state="pending",
                execution_heads=(
                    "## Execution heads\n\n"
                    f"- Repository: {repo}; Code base: {base}; "
                    f"Reviewed code head: {head}; Closure state: {head}; PR: none; "
                    "Review receipt: review.md"
                ),
                decisions="None.",
                findings="- [Ticket](issues/01-ticket.md) — done.",
            )
        )
        self.run_git(repo, "add", ".scratch/test")
        (repo / "file.txt").write_text("unreviewed closure code\n")
        self.run_git(repo, "commit", "-am", "prepare tracker with code")
        tracker_state = self.run_git(repo, "rev-parse", "HEAD").stdout.strip()
        map_path.write_text(
            map_path.read_text().replace(
                "Tracker state: pending", f"Tracker state: {tracker_state}"
            )
        )
        self.run_git(repo, "commit", "-am", "attest tracker closure")
        errors = validate(map_path)
        self.assertTrue(any("Tracker state commit changed files" in e for e in errors))

    def test_tracker_attestation_rejects_unreviewed_code(self) -> None:
        repo, base, head = self.make_repo()
        tracker = repo / ".scratch/test"
        (tracker / "issues").mkdir(parents=True)
        (tracker / "issues/01-ticket.md").write_text(ticket(kind="task"))
        (tracker / "review.md").write_text(self.review(base, head))
        map_path = tracker / "map.md"
        map_path.write_text(
            MAP.format(
                status="resolved",
                repository_execution="in-scope",
                tracker_state="pending",
                execution_heads=(
                    "## Execution heads\n\n"
                    f"- Repository: {repo}; Code base: {base}; "
                    f"Reviewed code head: {head}; Closure state: {head}; PR: none; "
                    "Review receipt: review.md"
                ),
                decisions="None.",
                findings="- [Ticket](issues/01-ticket.md) — done.",
            )
        )
        self.run_git(repo, "add", ".scratch/test")
        self.run_git(repo, "commit", "-m", "prepare tracker closure")
        tracker_state = self.run_git(repo, "rev-parse", "HEAD").stdout.strip()
        map_path.write_text(
            map_path.read_text().replace(
                "Tracker state: pending", f"Tracker state: {tracker_state}"
            )
        )
        (repo / "file.txt").write_text("unreviewed attestation code\n")
        self.run_git(repo, "commit", "-am", "attest tracker with code")
        errors = validate(map_path)
        self.assertTrue(any("attestation commit must change only" in e for e in errors))

    def test_closure_boundary_rejects_post_review_code(self) -> None:
        repo, base, head = self.make_repo()
        self.write_review(base, head)
        (repo / "file.txt").write_text("unreviewed code\n")
        self.run_git(repo, "commit", "-am", "change code before closure")
        closure = self.run_git(repo, "rev-parse", "HEAD").stdout.strip()
        (self.root / "issues/01-ticket.md").write_text(ticket(kind="task"))
        errors = validate(
            self.write_map(
                decisions="None.",
                findings="- [Ticket](issues/01-ticket.md) — done.",
                execution_heads=(
                    "## Execution heads\n\n"
                    f"- Repository: {repo}; Code base: {base}; "
                    f"Reviewed code head: {head}; Closure state: {closure}; PR: none; "
                    "Review receipt: review.md"
                ),
                repository_execution="in-scope",
            )
        )
        self.assertTrue(any("closure state changed files" in e for e in errors))

    def test_closure_boundary_rejects_code_changed_then_reverted(self) -> None:
        repo, base, head = self.make_repo()
        self.write_review(base, head)
        (repo / "file.txt").write_text("temporary unreviewed code\n")
        self.run_git(repo, "commit", "-am", "temporary code")
        (repo / "file.txt").write_text("head\n")
        self.run_git(repo, "commit", "-am", "revert temporary code")
        closure = self.run_git(repo, "rev-parse", "HEAD").stdout.strip()
        (self.root / "issues/01-ticket.md").write_text(ticket(kind="task"))
        errors = validate(
            self.write_map(
                decisions="None.",
                findings="- [Ticket](issues/01-ticket.md) — done.",
                execution_heads=(
                    "## Execution heads\n\n"
                    f"- Repository: {repo}; Code base: {base}; "
                    f"Reviewed code head: {head}; Closure state: {closure}; PR: none; "
                    "Review receipt: review.md"
                ),
                repository_execution="in-scope",
            )
        )
        self.assertTrue(any("closure state changed files" in e for e in errors))

    def test_shared_repo_closure_must_precede_tracker_state(self) -> None:
        repo, base, head = self.make_repo()
        tracker = repo / ".scratch/test"
        (tracker / "issues").mkdir(parents=True)
        (tracker / "issues/01-ticket.md").write_text(ticket(kind="task"))
        (tracker / "review.md").write_text(self.review(base, head))
        map_path = tracker / "map.md"
        map_path.write_text(
            MAP.format(
                status="resolved",
                repository_execution="in-scope",
                tracker_state="pending",
                execution_heads=(
                    "## Execution heads\n\n"
                    f"- Repository: {repo}; Code base: {base}; "
                    f"Reviewed code head: {head}; Closure state: {base}; PR: none; "
                    "Review receipt: review.md"
                ),
                decisions="None.",
                findings="- [Ticket](issues/01-ticket.md) — done.",
            )
        )
        self.run_git(repo, "add", ".scratch/test")
        self.run_git(repo, "commit", "-m", "prepare tracker closure")
        tracker_state = self.run_git(repo, "rev-parse", "HEAD").stdout.strip()
        map_path.write_text(
            map_path.read_text().replace(
                "Tracker state: pending", f"Tracker state: {tracker_state}"
            )
        )
        self.run_git(repo, "commit", "-am", "attest tracker closure")
        errors = validate(map_path)
        self.assertTrue(any("parent of Tracker state" in e for e in errors))

    def test_repository_subdirectory_is_deduplicated_to_git_root(self) -> None:
        repo, base, head = self.make_repo()
        subdir = repo / "subdir"
        subdir.mkdir()
        self.write_review(base, head)
        (self.root / "issues/01-ticket.md").write_text(ticket(kind="task"))
        first = (
            f"- Repository: {repo}; Code base: {base}; Reviewed code head: {head}; "
            f"Closure state: {head}; PR: none; Review receipt: review.md"
        )
        second = first.replace(f"Repository: {repo}", f"Repository: {subdir}")
        errors = validate(
            self.write_map(
                decisions="None.",
                findings="- [Ticket](issues/01-ticket.md) — done.",
                execution_heads=f"## Execution heads\n\n{first}\n{second}",
                repository_execution="in-scope",
            )
        )
        self.assertTrue(any("duplicate execution repository" in e for e in errors))

    def test_digest_budget(self) -> None:
        (self.root / "issues/01-ticket.md").write_text(ticket())
        (self.root / "digest.md").write_text("word " * 1_001)
        errors = validate(self.write_map())
        self.assertTrue(any("maximum is 1000" in e for e in errors))

    def test_fenced_digest_content_counts_toward_budget(self) -> None:
        (self.root / "issues/01-ticket.md").write_text(ticket())
        (self.root / "digest.md").write_text("```\n" + "word " * 1_001 + "\n```\n")
        errors = validate(self.write_map())
        self.assertTrue(any("maximum is 1000" in e for e in errors))

    def run_git(self, repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            text=True,
            check=True,
        )

    def make_repo(self, object_format: str = "sha1") -> tuple[Path, str, str]:
        repo = self.exec_root / "repo"
        repo.mkdir()
        self.run_git(repo, "init", f"--object-format={object_format}")
        self.run_git(repo, "config", "user.email", "test@example.com")
        self.run_git(repo, "config", "user.name", "Test")
        (repo / "file.txt").write_text("base\n")
        self.run_git(repo, "add", "file.txt")
        self.run_git(repo, "commit", "-m", "base")
        base = self.run_git(repo, "rev-parse", "HEAD").stdout.strip()
        (repo / "file.txt").write_text("head\n")
        self.run_git(repo, "commit", "-am", "head")
        head = self.run_git(repo, "rev-parse", "HEAD").stdout.strip()
        return repo, base, head

    def write_review(self, base: str, head: str) -> None:
        (self.root / "review.md").write_text(self.review(base, head))

    @staticmethod
    def review(base: str, head: str) -> str:
        return (
            f"Review range: {base}..{head}\n"
            "Decision: approved\n"
            "Checks: focused tests passed\n"
            "Findings and gaps: none\n"
        )


if __name__ == "__main__":
    unittest.main()
