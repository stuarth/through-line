from __future__ import annotations

import hashlib
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import scripts.validate_local_map as validator
from scripts.validate_local_map import validate


def unit(
    *,
    status: str = "resolved",
    owner: str = "builder",
    claimed_by: str | None = None,
    blocked_by: str | None = None,
    body_heading: str = "Outcome",
    resolution: str | None = None,
    extra: str = "",
) -> str:
    claim = f"Claimed by: {claimed_by}\n" if claimed_by else ""
    blockers = f"Blocked by: {blocked_by}\n" if blocked_by else ""
    if resolution is None and status == "resolved":
        resolution = (
            "\n## Resolution\n"
            "Provenance: focused implementation and review\n"
            "Evidence: the observable result passed its focused check\n"
        )
    return (
        f"Status: {status}\nOwner: {owner}\n{claim}{blockers}"
        f"\n## {body_heading}\nReach one observable result.\n"
        f"{extra}{resolution or ''}"
    )


class ValidatorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tempdir.name)
        self.tracker = self.workspace / "tracker"
        self.route = self.tracker / ".scratch" / "route"
        (self.route / "issues").mkdir(parents=True)
        self.init_repo(self.tracker)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def init_repo(self, path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)
        self.git(path, "init")
        self.git(path, "config", "user.email", "test@example.com")
        self.git(path, "config", "user.name", "Test")

    def git(self, repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            capture_output=True,
            text=True,
        )

    def write_unit(self, number: int, text: str, slug: str = "unit") -> Path:
        path = self.route / "issues" / f"{number:02d}-{slug}.md"
        path.write_text(text)
        return path

    def write_map(
        self,
        *,
        status: str = "resolved",
        execution: str = "out-of-scope",
        deferred: str = "none",
        repository_lines: str = "",
        closure_receipt: str = "pending",
    ) -> Path:
        execution_header = ""
        repositories = ""
        if execution == "in-scope":
            execution_header = (
                "First result: one end-to-end result\n"
                "Effort expectation: 2 active days\n"
                f"Closure receipt: {closure_receipt}\n"
            )
            repositories = f"\n## Repositories\n{repository_lines}\n"
        path = self.route / "map.md"
        path.write_text(
            "Schema: through-line/v2\n"
            f"Status: {status}\n"
            f"Repository execution: {execution}\n"
            f"{execution_header}"
            "\n## Destination\nShip the smallest credible result.\n"
            "\n## Decision rights\nHuman owns consequential tradeoffs.\n"
            "\n## Premises\nnone\n"
            f"\n## Deferred\n{deferred}\n"
            "\n## Out of scope\nnone\n"
            f"{repositories}"
        )
        return path

    def make_execution_repo(self, name: str = "app") -> tuple[Path, str, str, str]:
        repo = self.workspace / name
        self.init_repo(repo)
        (repo / "app.txt").write_text("base\n")
        self.git(repo, "add", "app.txt")
        self.git(repo, "commit", "-m", "base")
        base = self.git(repo, "rev-parse", "HEAD").stdout.strip()
        self.git(repo, "checkout", "-b", "integration/route")
        (repo / "app.txt").write_text("result\n")
        self.git(repo, "commit", "-am", "result")
        ref = "refs/heads/integration/route"
        head = self.git(repo, "rev-parse", ref).stdout.strip()
        return repo, base, ref, head

    @staticmethod
    def repository_line(
        repo: Path,
        base: str,
        ref: str,
        *,
        review: str = "pending",
        pr: str = "pending",
    ) -> str:
        return (
            f"- Repository: {repo}; Base: {base}; Ref: {ref}; "
            f"Review: {review}; PR: {pr}"
        )

    def write_receipt(
        self,
        records: list[tuple[Path, str]],
        *,
        route_id: str = "route",
        route_state: str | None = None,
        claim: str = (
            "The delivered import preserves identities and exposes one verified "
            "end-to-end result."
        ),
        supported: str = "yes",
        findings: str = "none",
        include_clean: bool = True,
    ) -> Path:
        reviewed = "\n".join(
            f"- Repository: {repo}; Reviewed head: {head}"
            for repo, head in records
        )
        clean = "\n".join(
            f"- Clean worktree: {repo} @ {head}" for repo, head in records
        )
        checks = clean if include_clean else "- Focused tests: passed"
        route_state = route_state or f"sha256:{self.route_digest()}"
        path = self.route / "closure.md"
        path.write_text(
            f"Route id: {route_id}\n"
            f"Route state: {route_state}\n"
            f"Claim: {claim}\n"
            f"Claim supported: {supported}\n"
            f"\n## Reviewed repositories\n{reviewed}\n"
            f"\n## Checks\n{checks}\n"
            f"\n## Findings\n{findings}\n"
        )
        return path

    def route_digest(self) -> str:
        digest = hashlib.sha256()
        paths = [self.route / "map.md", *sorted((self.route / "issues").glob("*.md"))]
        for path in sorted(paths, key=lambda item: item.relative_to(self.route).as_posix()):
            digest.update(path.relative_to(self.route).as_posix().encode())
            digest.update(b"\0")
            digest.update(path.read_bytes())
            digest.update(b"\0")
        return digest.hexdigest()

    def commit_closure(self, *, outside: bool = False) -> None:
        if outside:
            (self.tracker / "outside.txt").write_text("not tracker state\n")
            self.git(self.tracker, "add", "outside.txt")
        self.git(self.tracker, "add", ".scratch/route")
        self.git(self.tracker, "commit", "-m", "close route")

    def amend_closure(self) -> None:
        self.git(self.tracker, "add", ".scratch/route")
        self.git(self.tracker, "commit", "--amend", "--no-edit")

    def close_cross_repo(
        self, *, pr: str = "none"
    ) -> tuple[Path, Path, str, str, str, Path]:
        repo, base, ref, head = self.make_execution_repo()
        self.write_unit(1, unit())
        map_path = self.write_map(
            execution="in-scope",
            repository_lines=self.repository_line(
                repo, base, ref, review=f"{head} @ closure.md", pr=pr
            ),
            closure_receipt="closure.md",
        )
        receipt = self.write_receipt([(repo, head)])
        self.commit_closure()
        return map_path, repo, base, ref, head, receipt

    def assert_error(self, map_path: Path, fragment: str) -> None:
        errors = validate(map_path)
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_valid_decision_route(self) -> None:
        self.write_unit(1, unit())
        map_path = self.write_map()
        self.commit_closure()
        self.assertEqual(validate(map_path), [])

    def test_resolved_route_requires_a_terminal_outcome_unit(self) -> None:
        self.write_unit(1, unit(body_heading="Question"))
        map_path = self.write_map()
        self.commit_closure()
        self.assert_error(map_path, "requires at least one Outcome unit")

    def test_resolved_decision_route_requires_head_bytes_and_a_clean_route(self) -> None:
        unit_path = self.write_unit(1, unit())
        map_path = self.write_map()
        errors = validate(map_path)
        self.assertTrue(any("not tracked at tracker HEAD" in error for error in errors))
        self.assertTrue(any("uncommitted state" in error for error in errors))

        self.commit_closure()
        unit_path.write_text(unit() + "\nChanged after closure.\n")
        errors = validate(map_path)
        self.assertTrue(any("bytes do not match tracker HEAD" in error for error in errors))
        self.assertTrue(any("uncommitted state" in error for error in errors))

    def test_open_route_derives_claimed_blocked_and_frontier(self) -> None:
        self.write_unit(1, unit(status="open", claimed_by="worker-a"), "claimed")
        self.write_unit(2, unit(status="open", blocked_by="03"), "blocked")
        self.write_unit(3, unit(status="open"), "frontier")
        state: dict[str, list[str]] = {}
        errors = validate(self.write_map(status="open"), derived=state)
        self.assertEqual(errors, [])
        self.assertEqual(state["claimed"], ["01-claimed.md"])
        self.assertEqual(state["blocked"], ["02-blocked.md"])
        self.assertEqual(state["frontier"], ["03-frontier.md"])

    def test_decision_route_cannot_linger_open_after_closure(self) -> None:
        self.write_unit(1, unit())
        self.assert_error(self.write_map(status="open"), "satisfies closure")

    def test_map_requires_v2_schema_and_charter_sections(self) -> None:
        self.write_unit(1, unit(status="open"))
        path = self.write_map(status="open")
        path.write_text(
            path.read_text()
            .replace("through-line/v2", "through-line/v1")
            .replace("## Premises", "## Old premises")
        )
        errors = validate(path)
        self.assertTrue(any("Schema must" in error for error in errors))
        self.assertTrue(any("## Premises" in error for error in errors))

    def test_unit_requires_exactly_one_question_or_outcome(self) -> None:
        self.write_unit(
            1,
            unit(status="open", extra="\n## Question\nA second discriminator.\n"),
        )
        self.assert_error(self.write_map(status="open"), "exactly one")

    def test_reserved_field_names_in_unit_prose_are_not_state(self) -> None:
        self.write_unit(
            1,
            unit(
                status="open",
                extra="\nStatus: visible to the user\nOwner: selected account\n",
            ),
        )
        self.assertEqual(validate(self.write_map(status="open")), [])

    def test_resolution_requires_provenance_and_evidence(self) -> None:
        self.write_unit(1, unit(resolution="\n## Resolution\nDone.\n"))
        errors = validate(self.write_map())
        self.assertTrue(any("Provenance" in error for error in errors))
        self.assertTrue(any("Evidence" in error for error in errors))

    def test_resolution_and_checkpoint_follow_status(self) -> None:
        self.write_unit(
            1,
            unit(status="open", resolution="\n## Resolution\nProvenance: x\nEvidence: y\n"),
            "open",
        )
        self.write_unit(
            2,
            unit(extra="\n## Resumption checkpoint\nContinue tomorrow.\n"),
            "resolved",
        )
        errors = validate(self.write_map(status="open", deferred="later"))
        self.assertTrue(any("open unit cannot" in error for error in errors))
        self.assertTrue(any("checkpointed" in error for error in errors))

    def test_route_allows_at_most_one_claim(self) -> None:
        self.write_unit(1, unit(status="open", claimed_by="a"))
        self.write_unit(2, unit(status="open", claimed_by="b"))
        self.assert_error(self.write_map(status="open"), "at most one")

    def test_only_builder_owned_units_may_be_claimed(self) -> None:
        self.write_unit(1, unit(status="open", owner="human", claimed_by="worker-a"))
        self.assert_error(
            self.write_map(status="open"),
            "Claimed by is allowed only for Owner builder",
        )

    def test_claimed_unit_cannot_have_unresolved_blocker(self) -> None:
        self.write_unit(1, unit(status="open"))
        self.write_unit(2, unit(status="open", claimed_by="a", blocked_by="01"))
        self.assert_error(self.write_map(status="open"), "unresolved blockers")

    def test_resolved_unit_cannot_have_unresolved_blocker(self) -> None:
        self.write_unit(1, unit(status="open"))
        self.write_unit(2, unit(blocked_by="01"))
        self.assert_error(
            self.write_map(status="open", deferred="later"),
            "resolved unit has unresolved blockers",
        )

    def test_missing_blocker_and_dependency_cycle_are_rejected(self) -> None:
        self.write_unit(1, unit(status="open", blocked_by="02"))
        self.write_unit(2, unit(status="open", blocked_by="01, 99"))
        errors = validate(self.write_map(status="open"))
        self.assertTrue(any("blocker 99" in error for error in errors))
        self.assertTrue(any("dependency cycle" in error for error in errors))

    def test_legacy_state_and_history_files_are_rejected(self) -> None:
        self.write_unit(1, "Type: task\n" + unit(status="open"))
        history = self.route / "history"
        history.mkdir()
        (history / "old.md").write_text("superseded\n")
        errors = validate(self.write_map(status="open"))
        self.assertTrue(any("legacy or non-v2" in error for error in errors))
        self.assertTrue(any("does not use history" in error for error in errors))

    def test_supplied_map_symlink_is_rejected_before_resolution(self) -> None:
        target = self.workspace / "external-map.md"
        target.write_text("external\n")
        map_path = self.route / "map.md"
        map_path.symlink_to(target)
        self.assert_error(map_path, "map must not be a symlink")

    def test_supplied_route_symlink_is_rejected_before_resolution(self) -> None:
        target = self.workspace / "external-route"
        (target / "issues").mkdir(parents=True)
        (target / "map.md").write_text("external\n")
        route_link = self.tracker / ".scratch" / "linked-route"
        route_link.symlink_to(target)
        self.assert_error(route_link / "map.md", "route directory must not be a symlink")

    def test_supplied_issues_symlink_is_rejected_before_resolution(self) -> None:
        (self.route / "issues").rmdir()
        external = self.workspace / "external-issues"
        external.mkdir()
        (self.route / "issues").symlink_to(external)
        map_path = self.write_map(status="open")
        self.assert_error(map_path, "issues directory must not be a symlink")

    def test_digest_budget_and_route_state_shadowing(self) -> None:
        self.write_unit(1, unit())
        (self.route / "digest.md").write_text(
            "Status: open\n## Destination\ncopy\n" + "word " * 1_001
        )
        errors = validate(self.write_map())
        self.assertTrue(any("1000 words" in error for error in errors))
        self.assertTrue(any("shadows route state" in error for error in errors))

    def test_digest_rejects_execution_and_checkpoint_state(self) -> None:
        self.write_unit(1, unit())
        (self.route / "digest.md").write_text(
            "Base: abcdef\nRef: refs/heads/integration/route\n"
            "## Resumption checkpoint\nContinue here.\n"
        )
        self.assert_error(self.write_map(), "shadows route state")

    def test_valid_open_execution_route(self) -> None:
        repo, base, ref, _ = self.make_execution_repo()
        self.write_unit(1, unit(status="open"))
        path = self.write_map(
            status="open",
            execution="in-scope",
            repository_lines=self.repository_line(repo, base, ref),
        )
        self.assertEqual(validate(path), [])

    def test_open_execution_route_keeps_closure_receipt_pending(self) -> None:
        repo, base, ref, head = self.make_execution_repo()
        self.write_unit(1, unit(status="open"))
        path = self.write_map(
            status="open",
            execution="in-scope",
            repository_lines=self.repository_line(repo, base, ref),
            closure_receipt="closure.md",
        )
        self.write_receipt([(repo, head)])
        self.assert_error(path, "keep Closure receipt pending")

    def test_stale_review_is_derived_warning_not_error(self) -> None:
        repo, base, ref, reviewed = self.make_execution_repo()
        (repo / "app.txt").write_text("new head\n")
        self.git(repo, "commit", "-am", "advance ref")
        (self.route / "review.md").write_text("review evidence\n")
        self.write_unit(1, unit(status="open"))
        path = self.write_map(
            status="open",
            execution="in-scope",
            repository_lines=self.repository_line(
                repo, base, ref, review=f"{reviewed} @ review.md"
            ),
        )
        warnings: list[str] = []
        self.assertEqual(validate(path, warnings), [])
        self.assertTrue(any("Review is stale" in warning for warning in warnings))

    def test_open_review_requires_an_existing_local_reference_or_http_url(self) -> None:
        repo, base, ref, head = self.make_execution_repo()
        self.write_unit(1, unit(status="open"))
        path = self.write_map(
            status="open",
            execution="in-scope",
            repository_lines=self.repository_line(
                repo, base, ref, review=f"{head} @ missing-review.md"
            ),
        )
        self.assert_error(path, "local Review reference does not exist")

        path.write_text(
            path.read_text().replace(
                "missing-review.md", "https://example.com/reviews/route"
            )
        )
        self.assertEqual(validate(path), [])

    def test_execution_ref_must_use_exact_route_namespace(self) -> None:
        repo, base, _, head = self.make_execution_repo()
        self.write_unit(1, unit(status="open"))
        path = self.write_map(
            status="open",
            execution="in-scope",
            repository_lines=self.repository_line(repo, base, head),
        )
        self.assert_error(path, "Ref must be exactly refs/heads/integration/route")

    def test_execution_requires_result_expectation_and_repository(self) -> None:
        self.write_unit(1, unit(status="open"))
        path = self.write_map(status="open", execution="in-scope")
        path.write_text(
            path.read_text()
            .replace("First result: one end-to-end result\n", "")
            .replace(
                "Effort expectation: 2 active days\n",
                "",
            )
        )
        errors = validate(path)
        self.assertTrue(any("requires First result" in error for error in errors))
        self.assertTrue(any("requires Effort expectation" in error for error in errors))
        self.assertTrue(any("at least one repository" in error for error in errors))

    def test_valid_cross_repository_closure(self) -> None:
        map_path, *_ = self.close_cross_repo()
        self.assertEqual(validate(map_path), [])

    def test_closure_rejects_proxy_claim(self) -> None:
        map_path, repo, _, _, head, receipt = self.close_cross_repo()
        receipt.write_text(receipt.read_text().replace(
            "The delivered import preserves identities and exposes one verified end-to-end result.",
            "The work is fully complete and all required changes are done.",
        ))
        self.amend_closure()
        self.assert_error(map_path, "concrete and nonproxy")

    def test_closure_accepts_a_short_concrete_claim(self) -> None:
        map_path, _, _, _, _, receipt = self.close_cross_repo()
        receipt.write_text(receipt.read_text().replace(
            "The delivered import preserves identities and exposes one verified end-to-end result.",
            "Imports preserve IDs and audit history.",
        ))
        self.amend_closure()
        self.assertEqual(validate(map_path), [])

    def test_closure_requires_supported_claim(self) -> None:
        map_path, _, _, _, _, receipt = self.close_cross_repo()
        receipt.write_text(receipt.read_text().replace("Claim supported: yes", "Claim supported: no"))
        self.amend_closure()
        self.assert_error(map_path, "Claim supported: yes")

    def test_supported_claim_requires_findings_to_normalize_to_none(self) -> None:
        map_path, _, _, _, _, receipt = self.close_cross_repo()
        receipt.write_text(
            receipt.read_text().replace(
                "## Findings\nnone", "## Findings\n- Identity loss remains"
            )
        )
        self.amend_closure()
        self.assert_error(map_path, "Claim supported yes requires Findings none")

    def test_closure_receipt_requires_matching_route_state(self) -> None:
        repo, base, ref, head = self.make_execution_repo()
        self.write_unit(1, unit())
        map_path = self.write_map(
            execution="in-scope",
            repository_lines=self.repository_line(
                repo, base, ref, review=f"{head} @ closure.md", pr="none"
            ),
            closure_receipt="closure.md",
        )
        self.write_receipt([(repo, head)], route_state=f"sha256:{'0' * 64}")
        self.commit_closure()
        self.assert_error(map_path, "Route state does not match")

    def test_closure_receipt_requires_route_state_field(self) -> None:
        map_path, _, _, _, _, receipt = self.close_cross_repo()
        receipt.write_text(
            "\n".join(
                line
                for line in receipt.read_text().splitlines()
                if not line.startswith("Route state:")
            )
            + "\n"
        )
        self.amend_closure()
        self.assert_error(map_path, "missing or empty Route state field")

    def test_resolved_route_requires_current_repository_review(self) -> None:
        map_path, _, _, _, head, _ = self.close_cross_repo()
        map_path.write_text(
            map_path.read_text().replace(
                f"Review: {head} @ closure.md", "Review: pending"
            )
        )
        self.amend_closure()
        self.assert_error(map_path, "requires current Review")

    def test_resolved_review_reference_must_equal_closure_receipt(self) -> None:
        repo, base, ref, head = self.make_execution_repo()
        self.write_unit(1, unit())
        (self.route / "other-review.md").write_text("older review\n")
        map_path = self.write_map(
            execution="in-scope",
            repository_lines=self.repository_line(
                repo, base, ref, review=f"{head} @ other-review.md", pr="none"
            ),
            closure_receipt="closure.md",
        )
        self.write_receipt([(repo, head)])
        self.commit_closure()
        self.assert_error(map_path, "Review reference must equal Closure receipt")

    def test_resolved_route_cannot_leave_pr_pending(self) -> None:
        map_path, *_ = self.close_cross_repo(pr="pending")
        self.assert_error(map_path, "requires PR to be `none` or HTTP(S)")

    def test_closure_requires_clean_observation(self) -> None:
        map_path, _, _, _, _, receipt = self.close_cross_repo()
        receipt.write_text(receipt.read_text().replace("Clean worktree:", "Checked worktree:"))
        self.amend_closure()
        self.assert_error(map_path, "Clean worktree observation")

    def test_closure_rejects_duplicate_clean_observation(self) -> None:
        map_path, _, _, _, _, receipt = self.close_cross_repo()
        clean_line = next(
            line for line in receipt.read_text().splitlines() if "Clean worktree:" in line
        )
        receipt.write_text(receipt.read_text().replace(clean_line, f"{clean_line}\n{clean_line}"))
        self.amend_closure()
        self.assert_error(map_path, "duplicate Clean worktree observation")

    def test_closure_head_must_equal_current_ref(self) -> None:
        map_path, repo, _, _, _, _ = self.close_cross_repo()
        (repo / "app.txt").write_text("advanced\n")
        self.git(repo, "commit", "-am", "advance after review")
        self.assert_error(map_path, "does not equal current Ref head")

    def test_closure_requires_clean_execution_worktree(self) -> None:
        map_path, repo, *_ = self.close_cross_repo()
        (repo / "dirty.txt").write_text("dirty\n")
        self.assert_error(map_path, "execution worktree is not clean")

    def test_closure_git_evidence_commands_fail_closed(self) -> None:
        map_path, *_ = self.close_cross_repo()
        real_git = validator.git

        for command in ("status", "log", "diff-tree"):
            with self.subTest(command=command):
                def fail_selected(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
                    if args and args[0] == command:
                        return subprocess.CompletedProcess(
                            ["git", *args], 2, stdout="", stderr="forced failure"
                        )
                    return real_git(repo, *args)

                with patch("scripts.validate_local_map.git", side_effect=fail_selected):
                    errors = validate(map_path)
                self.assertTrue(
                    any("Git" in error and "failed" in error for error in errors),
                    errors,
                )

    def test_closure_commit_must_touch_only_route_files(self) -> None:
        repo, base, ref, head = self.make_execution_repo()
        self.write_unit(1, unit())
        map_path = self.write_map(
            execution="in-scope",
            repository_lines=self.repository_line(
                repo, base, ref, review=f"{head} @ closure.md", pr="none"
            ),
            closure_receipt="closure.md",
        )
        self.write_receipt([(repo, head)])
        self.commit_closure(outside=True)
        self.assert_error(map_path, "touch only route files")

    def test_closure_rejects_unit_state_symlinked_outside_tracker(self) -> None:
        repo, base, ref, head = self.make_execution_repo()
        external_unit = self.workspace / "external-unit.md"
        external_unit.write_text(unit())
        (self.route / "issues" / "01-unit.md").symlink_to(external_unit)
        map_path = self.write_map(
            execution="in-scope",
            repository_lines=self.repository_line(
                repo, base, ref, review=f"{head} @ closure.md", pr="none"
            ),
            closure_receipt="closure.md",
        )
        self.write_receipt([(repo, head)])
        self.commit_closure()
        self.assert_error(map_path, "units must not be symlinks")

    def test_map_and_receipt_must_share_closure_commit(self) -> None:
        map_path, _, _, _, _, receipt = self.close_cross_repo()
        receipt.write_text(receipt.read_text() + "\nAdditional evidence.\n")
        self.git(self.tracker, "add", ".scratch/route/closure.md")
        self.git(self.tracker, "commit", "-m", "change receipt later")
        self.assert_error(map_path, "same commit")

    def test_route_cannot_change_after_closure(self) -> None:
        map_path, *_ = self.close_cross_repo()
        references = self.route / "references"
        references.mkdir()
        (references / "later.md").write_text("late state\n")
        self.git(self.tracker, "add", ".scratch/route/references/later.md")
        self.git(self.tracker, "commit", "-m", "change closed route")
        self.assert_error(map_path, "changed after its closure")

    def close_shared_repo(self, *, tracker_on_integration: bool = False) -> Path:
        (self.tracker / "app.txt").write_text("base\n")
        self.git(self.tracker, "add", "app.txt")
        self.git(self.tracker, "commit", "-m", "base")
        base = self.git(self.tracker, "rev-parse", "HEAD").stdout.strip()
        self.git(self.tracker, "checkout", "-b", "integration/route")
        (self.tracker / "app.txt").write_text("result\n")
        self.git(self.tracker, "commit", "-am", "result")
        ref = "refs/heads/integration/route"
        head = self.git(self.tracker, "rev-parse", ref).stdout.strip()
        if not tracker_on_integration:
            self.git(self.tracker, "checkout", "-b", "tracker/route", base)
        self.write_unit(1, unit())
        map_path = self.write_map(
            execution="in-scope",
            repository_lines=self.repository_line(
                self.tracker,
                base,
                ref,
                review=f"{head} @ closure.md",
                pr="none",
            ),
            closure_receipt="closure.md",
        )
        self.write_receipt([(self.tracker, head)])
        self.commit_closure()
        return map_path

    def test_shared_repository_tracker_closure_may_be_a_sibling_branch(self) -> None:
        self.assertEqual(validate(self.close_shared_repo()), [])

    def test_shared_repository_closure_rejects_checked_out_integration_ref(self) -> None:
        self.assert_error(
            self.close_shared_repo(tracker_on_integration=True),
            "non-integration branch",
        )

    def test_receipt_repositories_must_match_map(self) -> None:
        map_path, _, _, _, _, receipt = self.close_cross_repo()
        other, _, _, other_head = self.make_execution_repo("other")
        text = receipt.read_text()
        reviewed_start = text.index("## Reviewed repositories")
        checks_start = text.index("## Checks")
        text = (
            text[:reviewed_start]
            + f"## Reviewed repositories\n- Repository: {other}; Reviewed head: {other_head}\n\n"
            + text[checks_start:]
        )
        receipt.write_text(text)
        self.amend_closure()
        self.assert_error(map_path, "exactly match the map")

    def test_validator_is_executable_as_a_cli(self) -> None:
        self.write_unit(1, unit(status="open", body_heading="Question"))
        map_path = self.write_map(status="open")
        script = Path(__file__).with_name("validate_local_map.py")
        self.assertTrue(os.access(script, os.X_OK))
        result = subprocess.run(
            [str(script), str(map_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("OK:", result.stdout)

    def test_cli_prints_route_state_digest(self) -> None:
        self.write_unit(1, unit(status="open", body_heading="Question"))
        map_path = self.write_map(status="open")
        script = Path(__file__).with_name("validate_local_map.py")
        result = subprocess.run(
            [str(script), "--digest", str(map_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.strip(),
            f"sha256:{validator.route_state_digest(self.route)}",
        )


if __name__ == "__main__":
    unittest.main()
