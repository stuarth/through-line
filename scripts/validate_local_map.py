#!/usr/bin/env python3
"""Check structural cross-file state in a through-line local-Markdown map."""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

INDEX_SECTIONS = ("Decisions so far", "Findings", "Out of scope")
LEGWORK_TYPES = {"research", "prototype", "task"}
TICKET_TYPES = {"decision"} | LEGWORK_TYPES
TICKET_STATUSES = {"open", "claimed", "blocked", "resolved"}
DIGEST_MAX_LINES = 120
DIGEST_MAX_WORDS = 1_000


@dataclass(frozen=True)
class Ticket:
    path: Path
    number: str | None
    kind: str | None
    status: str | None
    blockers: tuple[str, ...]
    assignee: str | None
    resolutions: int
    checkpoints: int
    provisionals: int
    legacy_actives: int
    reopened: int
    convergence_verdicts: int
    falsify_audits: int
    affected_dependents: int
    dependent_dispositions: int
    deferred_reviews: tuple[str, ...]
    repository: str | None
    candidate_commit: str | None
    integrated_commit: str | None


FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
COMMENT_OPEN = re.compile(r"^ {0,3}<!--")


def scannable_text(text: str) -> str:
    lines: list[str] = []
    fence: tuple[str, int] | None = None
    in_comment = False
    for line in text.splitlines():
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        match = FENCE.match(line)
        if fence is not None:
            if (
                match
                and match.group(1)[0] == fence[0]
                and len(match.group(1)) >= fence[1]
                and not match.group(2).strip()
            ):
                fence = None
            continue
        if match and (match.group(1)[0] == "~" or "`" not in match.group(2)):
            fence = (match.group(1)[0], len(match.group(1)))
            continue
        if COMMENT_OPEN.match(line):
            if "-->" not in line.split("<!--", 1)[1]:
                in_comment = True
            continue
        lines.append(line)
    return "\n".join(lines)


def section_bodies(text: str, name: str) -> str:
    bodies: list[str] = []
    for match in re.finditer(rf"(?m)^## {re.escape(name)}\s*$", text):
        start = match.end()
        next_heading = re.search(r"(?m)^## ", text[start:])
        end = start + next_heading.start() if next_heading else len(text)
        bodies.append(text[start:end])
    return "\n".join(bodies)


def fields(text: str, name: str) -> tuple[str, ...]:
    return tuple(
        match.group(1).strip()
        for match in re.finditer(
            rf"(?m)^{re.escape(name)}:[ \t]*(.+?)[ \t]*$", text
        )
    )


def field(text: str, name: str) -> str | None:
    values = fields(text, name)
    return values[0] if values else None


def ticket_number(path: Path) -> str | None:
    match = re.match(r"(\d+)-", path.name)
    return str(int(match.group(1))) if match else None


def blockers(text: str, path: Path, errors: list[str]) -> tuple[str, ...]:
    value = field(text, "Blocked by")
    if not value:
        return ()

    numbers: list[str] = []
    for token in value.split(","):
        match = re.fullmatch(r"\s*#?0*(\d+)\s*", token)
        if match:
            numbers.append(str(int(match.group(1))))
        else:
            errors.append(f"{path}: cannot resolve blocker {token.strip()!r}")
    return tuple(numbers)


def count_field(text: str, name: str, path: Path, errors: list[str]) -> int:
    value = field(text, name)
    if value is None:
        return 0
    if re.fullmatch(r"[1-9]\d*", value):
        return int(value)
    errors.append(f"{path}: {name} must be a positive integer")
    return 0


def section(text: str, name: str, errors: list[str]) -> str:
    matches = list(re.finditer(rf"(?m)^## {re.escape(name)}\s*$", text))
    if len(matches) != 1:
        errors.append(f"map: cannot compare state without exactly one ## {name}")
        return ""

    start = matches[0].end()
    next_heading = re.search(r"(?m)^## ", text[start:])
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end]


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )


def git_root(path: Path) -> Path | None:
    result = git(path, "rev-parse", "--show-toplevel")
    return Path(result.stdout.strip()).resolve() if result.returncode == 0 else None


def git_common_dir(repo: Path) -> Path | None:
    result = git(repo, "rev-parse", "--git-common-dir")
    if result.returncode:
        return None
    common_dir = Path(result.stdout.strip())
    if not common_dir.is_absolute():
        common_dir = repo / common_dir
    return common_dir.resolve()


def recorded_repository(map_path: Path, value: str | None) -> Path | None:
    if value is None:
        return None
    supplied = Path(value).expanduser()
    if not supplied.is_absolute():
        supplied = map_path.parent / supplied
    return git_root(supplied) if supplied.is_dir() else None


def full_commit(repo: Path, value: str) -> bool:
    object_format = git(repo, "rev-parse", "--show-object-format")
    expected_length = 64 if object_format.stdout.strip() == "sha256" else 40
    return (
        bool(re.fullmatch(rf"[0-9a-fA-F]{{{expected_length}}}", value))
        and not git(repo, "cat-file", "-e", f"{value}^{{commit}}").returncode
    )


def commit_is_ancestor(repo: Path, earlier: str, later: str) -> bool:
    return (
        full_commit(repo, earlier)
        and full_commit(repo, later)
        and not git(repo, "merge-base", "--is-ancestor", earlier, later).returncode
    )


def commit_paths(repo: Path, commit: str) -> list[str]:
    result = git(
        repo,
        "diff-tree",
        "--root",
        "-m",
        "--no-commit-id",
        "--name-only",
        "-r",
        commit,
    )
    return [line for line in result.stdout.splitlines() if line]


def validate_execution_heads(
    map_path: Path,
    map_text: str,
    map_status: str | None,
    errors: list[str],
    warnings: list[str],
    pending_deferred_reviews: tuple[tuple[Path | None, str | None], ...],
) -> list[tuple[Path, str]]:
    matches = list(re.finditer(r"(?m)^## Execution heads\s*$", map_text))
    if len(matches) != 1:
        errors.append(
            "map: in-scope repository execution requires exactly one ## Execution heads"
        )
        return []

    start = matches[0].end()
    next_heading = re.search(r"(?m)^## ", map_text[start:])
    end = start + next_heading.start() if next_heading else len(map_text)
    head_lines = [
        line
        for line in map_text[start:end].splitlines()
        if line.lstrip().startswith("-")
    ]
    if not head_lines:
        errors.append("map: in-scope repository execution has no execution head")
        return []

    pattern = re.compile(
        r"^\s*-\s+Repository:\s*(?P<repo>.+?);\s*"
        r"Code base:\s*(?P<base>[^;]+);\s*"
        r"(?:Integration head:\s*(?P<integration>[^;]+);\s*)?"
        r"Reviewed code head:\s*(?P<head>[^;]+);\s*"
        r"Closure state:\s*(?P<closure>[^;]+);\s*"
        r"PR:\s*(?P<pr>[^;]+);\s*"
        r"Review receipt:\s*(?P<receipt>.+?)\s*$"
    )

    tracker_repo = git_root(map_path.parent)
    tracker_identity = git_common_dir(tracker_repo) if tracker_repo else None

    def outside_tracker(repo: Path, changed: list[str]) -> list[str]:
        if tracker_repo is None or git_common_dir(repo) != tracker_identity:
            return changed
        try:
            tracker_dir = map_path.parent.relative_to(tracker_repo)
        except ValueError:
            return changed
        if tracker_dir == Path("."):
            return changed
        return [
            changed_path
            for changed_path in changed
            if Path(changed_path) != tracker_dir
            and tracker_dir not in Path(changed_path).parents
        ]

    seen_repositories: set[Path] = set()
    integration_heads: list[tuple[Path, str]] = []
    for line in head_lines:
        match = pattern.match(line)
        if not match:
            errors.append(f"map: malformed execution head: {line.strip()}")
            continue

        values = {
            name: value.strip() if value is not None else None
            for name, value in match.groupdict().items()
        }
        assert values["repo"] is not None
        assert values["base"] is not None
        assert values["head"] is not None
        assert values["closure"] is not None
        assert values["pr"] is not None
        assert values["receipt"] is not None
        repo = Path(values["repo"]).expanduser()
        if not repo.is_absolute():
            repo = map_path.parent / repo
        supplied_repo = repo.resolve()
        repo = git_root(supplied_repo) if supplied_repo.is_dir() else None
        if repo is None:
            errors.append(
                f"map: execution repository is not a Git repository: {supplied_repo}"
            )
            continue
        repository_identity = git_common_dir(repo) or repo
        if repository_identity in seen_repositories:
            errors.append(f"map: duplicate execution repository: {repo}")
            continue
        seen_repositories.add(repository_identity)

        base = values["base"]
        base_is_exact = full_commit(repo, base)
        if not base_is_exact:
            errors.append(
                f"map: Code base is not a commit named by its full hash in {repo}: "
                f"{base}"
            )

        head = values["head"]
        integration_value = values["integration"]
        if integration_value is None:
            integration = head if head != "pending" else base
            warnings.append(
                f"map: execution head for {repo} uses legacy format without "
                "Integration head"
            )
        else:
            integration = integration_value

        integration_is_exact = full_commit(repo, integration)
        if not integration_is_exact:
            errors.append(
                "map: Integration head is not a commit named by its full hash "
                f"in {repo}: {integration}"
            )
        if (
            base_is_exact
            and integration_is_exact
            and git(repo, "merge-base", "--is-ancestor", base, integration).returncode
        ):
            errors.append(
                f"map: Code base {base} is not an ancestor of integration head "
                f"{integration}"
            )
        pending_seam_reaches_head = any(
            (
                deferred_repository is None
                or git_common_dir(deferred_repository) == repository_identity
            )
            and (commit is None or commit_is_ancestor(repo, commit, integration))
            for deferred_repository, commit in pending_deferred_reviews
        )

        head_is_exact = False
        if head == "pending":
            if map_status == "resolved":
                errors.append("map: resolved execution head is still pending")
        else:
            head_is_exact = full_commit(repo, head)
            if not head_is_exact:
                errors.append(
                    "map: Reviewed code head is not a commit named by its full hash "
                    f"in {repo}: {head}"
                )
        if (
            base_is_exact
            and head_is_exact
            and git(repo, "merge-base", "--is-ancestor", base, head).returncode != 0
        ):
            errors.append(
                f"map: Code base {base} is not an ancestor of reviewed head {head}"
            )
        if (
            head_is_exact
            and integration_is_exact
            and git(repo, "merge-base", "--is-ancestor", head, integration).returncode
        ):
            errors.append(
                f"map: reviewed head {head} is not an ancestor of integration head "
                f"{integration}"
            )
        if map_status == "resolved" and head_is_exact and integration_is_exact:
            if head != integration:
                errors.append(
                    "map: resolved Integration head must equal Reviewed code head: "
                    f"{integration} != {head}"
                )

        closure = values["closure"]
        closure_is_exact = False
        if closure == "pending":
            if map_status == "resolved":
                errors.append("map: resolved execution closure state is still pending")
        else:
            closure_is_exact = full_commit(repo, closure)
            if not closure_is_exact:
                errors.append(
                    "map: Closure state is not a commit named by its full hash "
                    f"in {repo}: {closure}"
                )
        if integration_is_exact and closure_is_exact:
            if git(
                repo, "merge-base", "--is-ancestor", integration, closure
            ).returncode:
                errors.append(
                    f"map: integration head {integration} is not an ancestor of "
                    f"closure state {closure}"
                )
            elif head_is_exact:
                touched = git(
                    repo,
                    "log",
                    "-m",
                    "--format=",
                    "--name-only",
                    f"{head}..{closure}",
                )
                drift = outside_tracker(
                    repo, [line for line in touched.stdout.splitlines() if line]
                )
                if drift:
                    errors.append(
                        "map: closure state changed files outside the tracker after "
                        f"review: {', '.join(drift[:5])}"
                    )
        tracker_state = field(map_text, "Tracker state")
        if (
            map_status == "resolved"
            and tracker_identity is not None
            and git_common_dir(repo) == tracker_identity
            and tracker_state
            and full_commit(repo, tracker_state)
        ):
            parent = git(repo, "rev-parse", f"{tracker_state}^").stdout.strip()
            if closure != parent:
                errors.append(
                    "map: Closure state for the tracker repository must be the "
                    f"parent of Tracker state: expected {parent}"
                )
            drift = outside_tracker(repo, commit_paths(repo, tracker_state))
            if drift:
                errors.append(
                    "map: Tracker state commit changed files outside the tracker: "
                    f"{', '.join(drift[:5])}"
                )

        pr = values["pr"]
        pr_is_url = bool(re.match(r"^https?://", pr))
        if pr == "pending" and map_status == "resolved":
            errors.append("map: resolved execution PR is still pending")
        elif pr not in {"none", "pending"} and not pr_is_url:
            errors.append(f"map: PR must be a URL, `none`, or `pending`: {pr}")
        elif pr_is_url:
            if not head_is_exact or not integration_is_exact or head != integration:
                errors.append(
                    "map: PR exposure requires Integration head to equal Reviewed "
                    f"code head in {repo}"
                )
            if pending_seam_reaches_head:
                errors.append("map: PR exposure has a pending seam review")

        receipt = values["receipt"]
        if receipt == "pending":
            if map_status == "resolved":
                errors.append("map: resolved execution review receipt is still pending")
            if pr_is_url:
                errors.append(
                    "map: PR exposure requires an approved review receipt"
                )
        elif re.match(r"^https?://", receipt):
            errors.append("map: local Markdown requires a local review receipt")
        else:
            receipt_path = Path(receipt.split("#", 1)[0]).expanduser()
            if not receipt_path.is_absolute():
                receipt_path = map_path.parent / receipt_path
            receipt_path = receipt_path.resolve()
            try:
                receipt_path.relative_to(map_path.parent)
                receipt_is_local = True
            except ValueError:
                receipt_is_local = False
            if not receipt_is_local:
                errors.append(
                    f"map: review receipt must be inside the map tracker: {receipt_path}"
                )
            elif not receipt_path.is_file():
                errors.append(f"map: review receipt does not exist: {receipt_path}")
            else:
                tracker_root = git_root(map_path.parent)
                if map_status == "resolved" and (
                    tracker_root is None
                    or git(
                        tracker_root,
                        "ls-files",
                        "--error-unmatch",
                        "--",
                        str(receipt_path.relative_to(tracker_root)),
                    ).returncode
                ):
                    errors.append(
                        f"map: resolved review receipt is not committed: {receipt_path}"
                    )
                receipt_text = scannable_text(receipt_path.read_text())
                expected_range = f"{base}..{head}"
                if field(receipt_text, "Review range") != expected_range:
                    errors.append(
                        f"map: review receipt range must be {expected_range}: "
                        f"{receipt_path}"
                    )
                if not field(receipt_text, "Claim"):
                    errors.append(f"map: review receipt lacks Claim: {receipt_path}")
                decision = field(receipt_text, "Decision")
                if pr_is_url and decision != "approved":
                    errors.append(
                        "map: PR exposure requires an approved review receipt"
                    )
                elif map_status == "resolved" and decision != "approved":
                    errors.append(
                        f"map: review receipt Decision must be `approved`: "
                        f"{receipt_path}"
                    )
                elif map_status != "resolved" and decision not in {
                    "approved",
                    "rejected",
                }:
                    errors.append(
                        "map: open review receipt Decision must be `approved` or "
                        f"`rejected`: {receipt_path}"
                    )
                if not field(receipt_text, "Checks"):
                    errors.append(f"map: review receipt lacks Checks: {receipt_path}")
                if not field(receipt_text, "Findings and gaps"):
                    errors.append(
                        f"map: review receipt lacks Findings and gaps: {receipt_path}"
                    )

        integration_heads.append((repo, integration))

    return integration_heads


def index_paths(
    map_path: Path,
    body: str,
    name: str,
    errors: list[str],
) -> list[Path]:
    paths: list[Path] = []
    for line in body.splitlines():
        if not re.match(r"^\s*-\s+", line):
            continue
        match = re.search(r"\[[^\]]+\]\(([^)]+)\)", line)
        if not match:
            continue
        target = match.group(1).split("#", 1)[0]
        if re.match(r"^[a-z]+://", target):
            if name != "Out of scope":
                errors.append(f"map: {name} entry is not a child ticket: {target}")
            continue
        paths.append((map_path.parent / target).resolve())
    return paths


def validate(map_path: Path, warnings: list[str] | None = None) -> list[str]:
    errors: list[str] = []
    warnings = warnings if warnings is not None else []
    map_path = map_path.resolve()
    if not map_path.is_file():
        return [f"{map_path}: map file does not exist"]

    issues_dir = map_path.parent / "issues"
    if not issues_dir.is_dir():
        return [f"{issues_dir}: issues directory does not exist"]

    tickets: list[Ticket] = []
    for path in sorted(issues_dir.glob("*.md")):
        text = scannable_text(path.read_text())
        resolution_text = section_bodies(text, "Resolution")
        tickets.append(
            Ticket(
                path=path.resolve(),
                number=ticket_number(path),
                kind=field(text, "Type"),
                status=field(text, "Status"),
                blockers=blockers(text, path, errors),
                assignee=field(text, "Assignee"),
                resolutions=len(re.findall(r"(?m)^## Resolution\s*$", text)),
                checkpoints=len(
                    re.findall(r"(?m)^## Resumption checkpoint(?:\s+.*)?$", text)
                ),
                provisionals=len(re.findall(r"(?m)^## Provisional verdict\s*$", text)),
                legacy_actives=len(
                    re.findall(
                        r"(?m)^State: active\s*$",
                        section_bodies(text, "Verdict history"),
                    )
                ),
                reopened=count_field(text, "Reopened", path, errors),
                convergence_verdicts=len(
                    re.findall(r"(?m)^## Convergence verdict\s*$", text)
                ),
                falsify_audits=len(
                    re.findall(r"(?m)^## Falsify audit\s*$", text)
                ),
                affected_dependents=len(
                    re.findall(r"(?m)^## Affected resolved dependents\s*$", text)
                ),
                dependent_dispositions=len(
                    re.findall(r"(?m)^## Dependent disposition\s*$", text)
                ),
                deferred_reviews=fields(resolution_text, "Deferred review"),
                repository=field(text, "Repository"),
                candidate_commit=field(resolution_text, "Candidate commit"),
                integrated_commit=field(resolution_text, "Integrated commit"),
            )
        )

    for ticket in tickets:
        if ticket.kind not in TICKET_TYPES:
            errors.append(f"{ticket.path}: unknown Type {ticket.kind!r}")
        if ticket.status not in TICKET_STATUSES:
            errors.append(f"{ticket.path}: unknown Status {ticket.status!r}")
        if ticket.status in {"claimed", "resolved"} and not ticket.assignee:
            errors.append(f"{ticket.path}: Status {ticket.status} requires an Assignee")
        if ticket.status in {"open", "blocked"} and ticket.assignee:
            errors.append(
                f"{ticket.path}: Status {ticket.status} must not carry an Assignee"
            )
        if ticket.provisionals > 1:
            errors.append(f"{ticket.path}: more than one ## Provisional verdict")
        if ticket.checkpoints > 1:
            errors.append(f"{ticket.path}: more than one ## Resumption checkpoint")
        if ticket.status != "resolved" and ticket.resolutions:
            errors.append(f"{ticket.path}: unresolved with a ## Resolution")
        if ticket.legacy_actives:
            errors.append(
                f"{ticket.path}: legacy `State: active` marker requires migration "
                "to ## Provisional verdict"
            )
        if ticket.reopened:
            if ticket.convergence_verdicts != 1:
                errors.append(
                    f"{ticket.path}: reopened ticket requires exactly one "
                    "## Convergence verdict"
                )
        elif ticket.convergence_verdicts:
            errors.append(
                f"{ticket.path}: ## Convergence verdict requires Reopened"
            )
        for heading, count in (
            ("Falsify audit", ticket.falsify_audits),
            ("Affected resolved dependents", ticket.affected_dependents),
            ("Dependent disposition", ticket.dependent_dispositions),
        ):
            if count > 1:
                errors.append(f"{ticket.path}: more than one ## {heading}")
        if bool(ticket.candidate_commit) != bool(ticket.integrated_commit):
            errors.append(
                f"{ticket.path}: Candidate commit and Integrated commit must "
                "appear together"
            )
        for deferred_review in ticket.deferred_reviews:
            if not re.fullmatch(
                r"(?:seam pending|discharged) — .+", deferred_review
            ):
                errors.append(f"{ticket.path}: malformed Deferred review state")
        if (
            any(
                review.startswith("seam pending — ")
                for review in ticket.deferred_reviews
            )
            and not ticket.integrated_commit
        ):
            errors.append(
                f"{ticket.path}: pending seam review requires Integrated commit"
            )
        if ticket.status == "resolved":
            if ticket.resolutions != 1:
                errors.append(
                    f"{ticket.path}: resolved without exactly one ## Resolution"
                )
            if ticket.checkpoints:
                errors.append(
                    f"{ticket.path}: resolved with a ## Resumption checkpoint"
                )
            if ticket.provisionals:
                errors.append(f"{ticket.path}: resolved with a ## Provisional verdict")

    by_path = {ticket.path: ticket for ticket in tickets}
    by_number: dict[str, Ticket] = {}
    for ticket in tickets:
        if ticket.number is None:
            continue
        if ticket.number in by_number:
            errors.append(f"tickets: blocker number {ticket.number} is ambiguous")
        by_number[ticket.number] = ticket

    for ticket in tickets:
        missing = [number for number in ticket.blockers if number not in by_number]
        for number in missing:
            errors.append(f"{ticket.path}: blocker {number} does not exist")
        unresolved = [
            number
            for number in ticket.blockers
            if number in by_number and by_number[number].status != "resolved"
        ]
        if unresolved and ticket.status != "blocked":
            errors.append(
                f"{ticket.path}: unresolved blockers {', '.join(unresolved)} "
                "require Status: blocked"
            )
        if not unresolved and ticket.status == "blocked":
            errors.append(f"{ticket.path}: blocked without an unresolved blocker")

    def visit(number: str, active: tuple[str, ...], visited: set[str]) -> None:
        if number in active:
            cycle = active[active.index(number) :] + (number,)
            errors.append(f"tickets: dependency cycle {' -> '.join(cycle)}")
            return
        if number in visited or number not in by_number:
            return
        for blocker in by_number[number].blockers:
            visit(blocker, active + (number,), visited)
        visited.add(number)

    visited: set[str] = set()
    for number in by_number:
        visit(number, (), visited)

    map_text = scannable_text(map_path.read_text())
    indexes = {
        name: index_paths(map_path, section(map_text, name, errors), name, errors)
        for name in INDEX_SECTIONS
    }
    all_indexed = [path for paths in indexes.values() for path in paths]
    for path in set(all_indexed):
        if all_indexed.count(path) > 1:
            errors.append(f"map: ticket indexed more than once: {path.name}")
        if path not in by_path:
            errors.append(f"map: index target is not a child ticket: {path}")

    decisions = set(indexes["Decisions so far"])
    findings = set(indexes["Findings"])
    out_of_scope = set(indexes["Out of scope"])
    closed_indexes = decisions | findings | out_of_scope

    for ticket in tickets:
        if ticket.status != "resolved":
            if ticket.path in closed_indexes:
                errors.append(f"map: unresolved ticket is indexed: {ticket.path.name}")
            continue
        if ticket.path in out_of_scope:
            continue

        if ticket.kind == "decision":
            expected, wrong, name = decisions, findings, "Decisions so far"
        elif ticket.kind in LEGWORK_TYPES:
            expected, wrong, name = findings, decisions, "Findings"
        else:
            errors.append(
                f"{ticket.path}: cannot place resolved Type {ticket.kind!r} in an index"
            )
            continue

        if ticket.path in wrong:
            errors.append(f"map: {ticket.path.name} belongs in {name}")
        elif ticket.path not in expected:
            errors.append(
                f"map: resolved ticket missing from {name}: {ticket.path.name}"
            )

    map_status = field(map_text, "Status")
    if map_status not in {"open", "resolved"}:
        errors.append(f"map: unknown Status {map_status!r}")

    repository_execution = field(map_text, "Repository execution")
    integration_heads: list[tuple[Path, str]] = []
    ticket_repositories: dict[Path, Path] = {}
    for ticket in tickets:
        repository = recorded_repository(map_path, ticket.repository)
        if ticket.repository and repository is None:
            errors.append(
                f"{ticket.path}: Repository is not a Git repository: "
                f"{ticket.repository}"
            )
        elif repository is not None:
            ticket_repositories[ticket.path] = repository
    pending_deferred_reviews = tuple(
        (ticket_repositories.get(ticket.path), ticket.integrated_commit)
        for ticket in tickets
        for deferred_review in ticket.deferred_reviews
        if deferred_review.startswith("seam pending — ")
    )
    if repository_execution not in {"in-scope", "out-of-scope"}:
        errors.append("map: Repository execution must be `in-scope` or `out-of-scope`")
    elif repository_execution == "in-scope":
        integration_heads = validate_execution_heads(
            map_path,
            map_text,
            map_status,
            errors,
            warnings,
            pending_deferred_reviews,
        )

    for ticket in tickets:
        candidate = ticket.candidate_commit
        integrated = ticket.integrated_commit
        if not integrated:
            continue
        ticket_repository = ticket_repositories.get(ticket.path)
        if len(integration_heads) > 1 and ticket_repository is None:
            errors.append(
                f"{ticket.path}: repository task requires Repository when the map "
                "spans multiple execution repositories"
            )
        repositories = [
            repository
            for repository, integration in integration_heads
            if (
                ticket_repository is None
                or git_common_dir(repository) == git_common_dir(ticket_repository)
            )
            and commit_is_ancestor(repository, integrated, integration)
        ]
        if not repositories:
            errors.append(
                f"{ticket.path}: Integrated commit is not contained in an "
                f"Integration head: {integrated}"
            )
        elif candidate and not any(
            commit_is_ancestor(repository, candidate, integrated)
            for repository in repositories
        ):
            errors.append(
                f"{ticket.path}: Candidate commit is not an ancestor of "
                f"Integrated commit in its execution repository: "
                f"{candidate} -> {integrated}"
            )

    if map_status == "resolved":
        unresolved = [
            ticket.path.name for ticket in tickets if ticket.status != "resolved"
        ]
        if unresolved:
            errors.append(
                f"map: resolved with unresolved tickets: {', '.join(unresolved)}"
            )
        if pending_deferred_reviews:
            errors.append("map: resolved with a pending seam review")

    if map_status == "resolved" and repository_execution == "in-scope":
        tracker_root = git_root(map_path.parent)
        if tracker_root is None:
            errors.append("map: resolved local tracker is not in a Git repository")
        else:
            tracker_dir = map_path.parent.relative_to(tracker_root)
            tracker_arg = "." if tracker_dir == Path(".") else str(tracker_dir)
            map_relative = map_path.relative_to(tracker_root)
            tracker_state = field(map_text, "Tracker state")
            if not tracker_state or not full_commit(tracker_root, tracker_state):
                errors.append(
                    "map: resolved Tracker state must be a full commit hash in the "
                    "tracker repository"
                )
            else:
                if git(
                    tracker_root,
                    "merge-base",
                    "--is-ancestor",
                    tracker_state,
                    "HEAD",
                ).returncode:
                    errors.append(
                        "map: Tracker state is not an ancestor of the current tracker "
                        "HEAD"
                    )
                recorded_map = git(
                    tracker_root, "show", f"{tracker_state}:{map_relative.as_posix()}"
                )
                expected_recorded_map = re.sub(
                    rf"(?m)^Tracker state:[ \t]*{re.escape(tracker_state)}[ \t]*$",
                    "Tracker state: pending",
                    map_path.read_text(),
                    count=1,
                )
                if (
                    recorded_map.returncode
                    or recorded_map.stdout != expected_recorded_map
                ):
                    errors.append(
                        "map: current map differs from its immutable tracker state "
                        "beyond the Tracker state attestation"
                    )
                attestation_commits = git(
                    tracker_root,
                    "log",
                    "--format=%H",
                    "--reverse",
                    f"{tracker_state}..HEAD",
                    "--",
                    str(map_relative),
                ).stdout.splitlines()
                if len(attestation_commits) != 1:
                    errors.append(
                        "map: resolved tracker requires exactly one map attestation "
                        "commit after Tracker state"
                    )
                else:
                    attestation = attestation_commits[0]
                    parent = git(
                        tracker_root, "rev-parse", f"{attestation}^"
                    ).stdout.strip()
                    if parent != tracker_state:
                        errors.append(
                            "map: tracker attestation must immediately follow "
                            "Tracker state"
                        )
                    if set(commit_paths(tracker_root, attestation)) != {
                        str(map_relative)
                    }:
                        errors.append(
                            "map: tracker attestation commit must change only the map"
                        )
                changed_tracker = git(
                    tracker_root,
                    "log",
                    "-m",
                    "--format=",
                    "--name-only",
                    f"{tracker_state}..HEAD",
                    "--",
                    tracker_arg,
                ).stdout.splitlines()
                unexpected_tracker = [
                    changed
                    for changed in changed_tracker
                    if changed and Path(changed) != map_relative
                ]
                if unexpected_tracker:
                    errors.append(
                        "map: tracker changed after its immutable state: "
                        f"{', '.join(unexpected_tracker[:5])}"
                    )
            if git(
                tracker_root, "ls-files", "--error-unmatch", "--", str(map_relative)
            ).returncode:
                errors.append("map: resolved map is not committed")
            tracker_status = git(
                tracker_root,
                "status",
                "--porcelain",
                "--untracked-files=all",
                "--",
                tracker_arg,
            ).stdout.splitlines()
            if tracker_status:
                errors.append(
                    "map: resolved tracker has uncommitted state: "
                    f"{', '.join(line.strip() for line in tracker_status[:5])}"
                )
    digest_path = map_path.parent / "digest.md"
    if digest_path.is_file():
        digest_text = digest_path.read_text()
        digest_lines = len(digest_text.splitlines())
        digest_words = len(digest_text.split())
        if digest_lines > DIGEST_MAX_LINES:
            errors.append(
                f"{digest_path}: digest has {digest_lines} lines; "
                f"maximum is {DIGEST_MAX_LINES}"
            )
        if digest_words > DIGEST_MAX_WORDS:
            errors.append(
                f"{digest_path}: digest has {digest_words} words; "
                f"maximum is {DIGEST_MAX_WORDS}"
            )

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_local_map.py PATH/TO/map.md", file=sys.stderr)
        return 2

    warnings: list[str] = []
    errors = validate(Path(sys.argv[1]), warnings)
    for warning in warnings:
        print(f"WARN: {warning}", file=sys.stderr)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK (tracker structure only): {Path(sys.argv[1])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
