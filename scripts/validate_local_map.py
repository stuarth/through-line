#!/usr/bin/env python3
"""Validate a through-line/v2 local Markdown route."""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


MAP_SECTIONS = ("Destination", "Decision rights", "Premises", "Deferred", "Out of scope")
DIGEST_FIELDS = (
    "Schema", "Status", "Repository execution", "First result", "Effort expectation",
    "Closure receipt", "Repository", "Base", "Ref", "Review", "PR", "Owner",
    "Claimed by", "Blocked by", "Provenance", "Evidence", "Route id", "Claim",
    "Route state", "Claim supported", "Reviewed head",
)
DIGEST_SECTIONS = MAP_SECTIONS + (
    "Repositories", "Question", "Outcome", "Acceptance", "Reaching premises",
    "Resumption checkpoint", "Resolution", "Reviewed repositories", "Checks",
    "Findings", "Decisions so far",
)
DIGEST_MAX_LINES = 120
DIGEST_MAX_WORDS = 1_000
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
REPO_LINE = re.compile(
    r"^\s*-\s+Repository:\s*(.+?);\s*Base:\s*(.+?);\s*Ref:\s*(.+?);\s*"
    r"Review:\s*(.+?);\s*PR:\s*(.+?)\s*$"
)
REVIEW = re.compile(r"^([0-9a-fA-F]{40}|[0-9a-fA-F]{64}) @ (.+)$")
RECEIPT_REPO = re.compile(
    r"^\s*-\s+Repository:\s*(.+?);\s*Reviewed head:\s*"
    r"([0-9a-fA-F]{40}|[0-9a-fA-F]{64})\s*$"
)
CLEAN = re.compile(
    r"^\s*-\s+Clean worktree:\s*(.+?)\s+@\s+"
    r"([0-9a-fA-F]{40}|[0-9a-fA-F]{64})\s*$"
)
LEGACY = re.compile(
    r"(?m)^(?:Type|Label|Assignee|Tracker state|Code base|Integration head|"
    r"Reviewed code head|Closure state|Review receipt|Deferred review|Reopened|"
    r"Convergence|Attestation|History|Candidate commit|Integrated commit|Branch):|"
    r"^## (?:Execution heads|Decisions so far|Findings|Not yet specified|"
    r"Convergence verdict|Falsify audit|Verdict history)$"
)


@dataclass(frozen=True)
class Unit:
    path: Path
    number: str | None
    status: str | None
    claim: str | None
    blockers: tuple[str, ...]
    outcome: bool


@dataclass(frozen=True)
class Repository:
    label: str
    root: Path
    identity: Path
    ref_head: str
    review_head: str | None
    review_reference: str | None
    pr: str


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )


def git_bytes(repo: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        timeout=10,
        check=False,
    )


def git_root(path: Path) -> Path | None:
    if not path.is_dir():
        return None
    result = git(path, "rev-parse", "--show-toplevel")
    return Path(result.stdout.strip()).resolve() if result.returncode == 0 else None


def git_identity(repo: Path) -> Path | None:
    result = git(repo, "rev-parse", "--git-common-dir")
    if result.returncode:
        return None
    common = Path(result.stdout.strip())
    return (common if common.is_absolute() else repo / common).resolve()


def resolve_commit(repo: Path, value: str, *, require_full: bool = False) -> str | None:
    object_format = git(repo, "rev-parse", "--show-object-format")
    if object_format.returncode:
        return None
    length = 64 if object_format.stdout.strip() == "sha256" else 40
    if require_full and not re.fullmatch(rf"[0-9a-fA-F]{{{length}}}", value):
        return None
    result = git(repo, "rev-parse", "--verify", f"{value}^{{commit}}")
    head = result.stdout.strip()
    return head if result.returncode == 0 and len(head) == length else None


def visible(text: str) -> str:
    """Ignore fenced examples and HTML comments when reading state."""
    kept: list[str] = []
    fence: tuple[str, int] | None = None
    comment = False
    for line in text.splitlines():
        if comment:
            comment = "-->" not in line
            continue
        mark = FENCE.match(line)
        if fence:
            if mark and mark.group(1)[0] == fence[0] and len(mark.group(1)) >= fence[1] and not mark.group(2).strip():
                fence = None
            continue
        if mark and (mark.group(1)[0] == "~" or "`" not in mark.group(2)):
            fence = (mark.group(1)[0], len(mark.group(1)))
            continue
        if line.lstrip().startswith("<!--"):
            comment = "-->" not in line
            continue
        kept.append(line)
    return "\n".join(kept)


def values(text: str, name: str) -> tuple[str, ...]:
    return tuple(
        match.group(1).strip()
        for match in re.finditer(rf"(?m)^{re.escape(name)}:[ \t]*(.*?)[ \t]*$", text)
    )


def preamble(text: str) -> str:
    heading = re.search(r"(?m)^## ", text)
    return text[: heading.start()] if heading else text


def one_value(
    text: str, name: str, source: str, errors: list[str], *, required: bool = False
) -> str | None:
    found = values(text, name)
    if len(found) > 1:
        errors.append(f"{source}: more than one {name} field")
    if not found or not found[0]:
        if required or found:
            errors.append(f"{source}: missing or empty {name} field")
        return None
    return found[0]


def section_bodies(text: str, name: str) -> tuple[str, ...]:
    matches = list(re.finditer(rf"(?m)^## {re.escape(name)}[ \t]*$", text))
    bodies: list[str] = []
    for match in matches:
        next_heading = re.search(r"(?m)^## ", text[match.end() :])
        end = match.end() + next_heading.start() if next_heading else len(text)
        bodies.append(text[match.end() : end])
    return tuple(bodies)


def one_section(text: str, name: str, source: str, errors: list[str]) -> str:
    found = section_bodies(text, name)
    if len(found) != 1:
        errors.append(f"{source}: requires exactly one ## {name}")
    return found[0] if found else ""


def empty(body: str) -> bool:
    return not body.strip() or bool(re.fullmatch(r"(?is)\s*(?:-\s*)?none\.?\s*", body))


def path_for(route: Path, supplied: str) -> Path:
    path = Path(supplied).expanduser()
    return path if path.is_absolute() else route / path


def authoritative_paths(route: Path) -> tuple[Path, ...]:
    return (route / "map.md", *sorted((route / "issues").glob("*.md")))


def route_state_digest(route: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(authoritative_paths(route), key=lambda item: item.relative_to(route).as_posix()):
        relative = path.relative_to(route).as_posix().encode()
        digest.update(relative)
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def blocker_numbers(value: str | None, path: Path, errors: list[str]) -> tuple[str, ...]:
    if value is None:
        return ()
    numbers: list[str] = []
    for token in value.split(","):
        match = re.fullmatch(r"\s*#?0*(\d+)\s*", token)
        if not match or int(match.group(1)) == 0:
            errors.append(f"{path}: malformed blocker {token.strip()!r}")
        else:
            numbers.append(str(int(match.group(1))))
    return tuple(numbers)


def read_units(route: Path, errors: list[str]) -> tuple[Unit, ...]:
    issues = route / "issues"
    if issues.is_symlink():
        errors.append(f"{issues}: issues directory must not be a symlink")
        return ()
    if not issues.is_dir():
        errors.append(f"{issues}: issues directory does not exist")
        return ()
    paths = sorted(issues.glob("*.md"))
    if not paths:
        errors.append(f"{issues}: route requires at least one unit")
    units: list[Unit] = []
    for path in paths:
        if path.is_symlink():
            errors.append(f"{path}: route units must not be symlinks")
            continue
        canonical = path.resolve()
        if route != canonical and route not in canonical.parents:
            errors.append(f"{path}: canonical unit must stay inside the route")
            continue
        text = visible(path.read_text())
        unit_fields = preamble(text)
        if LEGACY.search(text) or values(unit_fields, "Claim"):
            errors.append(f"{path}: contains legacy or non-v2 state")
        status = one_value(unit_fields, "Status", str(path), errors, required=True)
        owner = one_value(unit_fields, "Owner", str(path), errors, required=True)
        claim = one_value(unit_fields, "Claimed by", str(path), errors)
        blockers = blocker_numbers(
            one_value(unit_fields, "Blocked by", str(path), errors), path, errors
        )
        if status not in {"open", "resolved"}:
            errors.append(f"{path}: Status must be `open` or `resolved`")
        if owner not in {"human", "builder"}:
            errors.append(f"{path}: Owner must be `human` or `builder`")
        if claim and claim.lower() in {"none", "pending"}:
            errors.append(f"{path}: Claimed by must identify a claimant")
        if claim and owner != "builder":
            errors.append(f"{path}: Claimed by is allowed only for Owner builder")
        question = section_bodies(text, "Question")
        outcome = section_bodies(text, "Outcome")
        if len(question) + len(outcome) != 1:
            errors.append(f"{path}: requires exactly one of ## Question or ## Outcome")
        elif empty((question or outcome)[0]):
            errors.append(f"{path}: Question or Outcome must not be empty")
        resolutions = section_bodies(text, "Resolution")
        checkpoints = section_bodies(text, "Resumption checkpoint")
        for name in ("Acceptance", "Reaching premises", "Resumption checkpoint"):
            optional = section_bodies(text, name)
            if len(optional) > 1:
                errors.append(f"{path}: more than one optional ## {name}")
            elif optional and empty(optional[0]):
                errors.append(f"{path}: optional ## {name} must not be empty")
        if status == "resolved":
            if len(resolutions) != 1:
                errors.append(f"{path}: resolved unit requires exactly one ## Resolution")
            if claim or checkpoints:
                errors.append(f"{path}: resolved unit cannot be claimed or checkpointed")
        elif resolutions:
            errors.append(f"{path}: open unit cannot have ## Resolution")
        if resolutions:
            for name in ("Provenance", "Evidence"):
                value = one_value(resolutions[0], name, str(path), errors, required=True)
                if value and value.lower() in {"none", "pending"}:
                    errors.append(f"{path}: Resolution {name} must be substantive")
        number_match = re.match(r"(\d+)-.+\.md$", path.name)
        number = str(int(number_match.group(1))) if number_match and int(number_match.group(1)) else None
        if number is None:
            errors.append(f"{path}: unit filename needs a positive numeric prefix")
        units.append(
            Unit(
                canonical,
                number,
                status,
                claim,
                blockers,
                len(outcome) == 1 and not question and not empty(outcome[0]),
            )
        )
    history = route / "history"
    if history.exists() and any(item.is_file() for item in history.rglob("*")):
        errors.append(f"{history}: through-line/v2 does not use history files")
    return tuple(units)


def validate_dependencies(
    units: tuple[Unit, ...], errors: list[str], derived: dict[str, list[str]]
) -> None:
    by_number: dict[str, Unit] = {}
    for unit in units:
        if unit.number in by_number:
            errors.append(f"units: number {unit.number} is ambiguous")
        elif unit.number:
            by_number[unit.number] = unit
    if sum(bool(unit.claim) for unit in units) > 1:
        errors.append("route: at most one unit may carry Claimed by")
    for unit in units:
        missing = [number for number in unit.blockers if number not in by_number]
        for number in missing:
            errors.append(f"{unit.path}: blocker {number} does not exist")
        unresolved = [
            number
            for number in unit.blockers
            if number not in by_number or by_number[number].status != "resolved"
        ]
        if unit.status == "resolved" and unresolved:
            errors.append(f"{unit.path}: resolved unit has unresolved blockers")
        if unit.status != "open":
            continue
        if unit.claim:
            derived["claimed"].append(unit.path.name)
            if unresolved:
                errors.append(f"{unit.path}: claimed unit has unresolved blockers")
        elif unresolved:
            derived["blocked"].append(unit.path.name)
        else:
            derived["frontier"].append(unit.path.name)

    def visit(number: str, active: tuple[str, ...], done: set[str]) -> None:
        if number in active:
            errors.append(f"units: dependency cycle {' -> '.join(active + (number,))}")
            return
        if number in done or number not in by_number:
            return
        for blocker in by_number[number].blockers:
            visit(blocker, active + (number,), done)
        done.add(number)

    done: set[str] = set()
    for number in by_number:
        visit(number, (), done)


def read_repositories(
    map_path: Path, body: str, warnings: list[str], errors: list[str]
) -> tuple[Repository, ...]:
    repositories: list[Repository] = []
    identities: set[Path] = set()
    for line in (line for line in body.splitlines() if line.strip()):
        match = REPO_LINE.fullmatch(line)
        if not match:
            errors.append(f"map: malformed repository line: {line.strip()!r}")
            continue
        label, base, ref, review, pr = (part.strip() for part in match.groups())
        root = git_root(path_for(map_path.parent, label))
        if root is None:
            errors.append(f"map: Repository is not a Git worktree: {label}")
            continue
        identity = git_identity(root)
        if identity is None:
            errors.append(f"map: could not identify execution repository: {label}")
            continue
        if identity in identities:
            errors.append(f"map: duplicate execution repository: {label}")
            continue
        identities.add(identity)
        base_head = resolve_commit(root, base, require_full=True)
        expected_ref = f"refs/heads/integration/{map_path.parent.name}"
        if ref != expected_ref:
            errors.append(f"map: Ref must be exactly {expected_ref}: {ref}")
        ref_head = resolve_commit(root, ref)
        if base_head is None:
            errors.append(f"map: Base must be an existing full commit: {base}")
        if ref_head is None:
            errors.append(f"map: Ref does not resolve to a commit: {ref}")
            continue
        if base_head:
            ancestry = git(root, "merge-base", "--is-ancestor", base_head, ref_head)
            if ancestry.returncode == 1:
                errors.append(f"map: Base is not an ancestor of Ref: {label}")
            elif ancestry.returncode:
                errors.append(f"map: Git Base ancestry check failed for {label}")
        reviewed = None
        review_reference = None
        if review != "pending":
            reviewed = REVIEW.fullmatch(review)
            if not reviewed or not resolve_commit(root, reviewed.group(1), require_full=True):
                errors.append("map: Review must be `pending` or `<full commit> @ <reference>`")
            elif reviewed.group(2).lower() in {"none", "pending"}:
                errors.append("map: Review requires a durable reference")
            else:
                review_reference = reviewed.group(2)
                if not re.fullmatch(r"https?://\S+", review_reference) and not path_for(
                    map_path.parent, review_reference
                ).exists():
                    errors.append(f"map: local Review reference does not exist: {review_reference}")
                if reviewed.group(1).lower() != ref_head.lower():
                    warnings.append(f"map: Review is stale for {label}")
        if pr not in {"pending", "none"} and not re.fullmatch(r"https?://\S+", pr):
            errors.append(f"map: invalid PR value for {label}")
        review_head = reviewed.group(1) if review != "pending" and reviewed else None
        repositories.append(
            Repository(
                label,
                root,
                identity,
                ref_head,
                review_head,
                review_reference,
                pr,
            )
        )
    if not repositories:
        errors.append("map: ## Repositories requires at least one repository line")
    return tuple(repositories)


def concrete_claim(claim: str) -> bool:
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'-]*", claim)
    normalized = " ".join(words).lower()
    proxy_words = {
        "all", "and", "approved", "are", "artifacts", "been", "change",
        "changes", "checks", "complete", "completed", "done", "every", "exist",
        "finished", "fully", "good", "has", "have", "implementation", "is",
        "map", "now", "pass", "passed", "project", "ready", "request",
        "requested", "required", "requirements", "route", "successful",
        "successfully", "task", "tests", "the", "valid", "was", "were", "work",
    }
    proxy = re.fullmatch(
        r"(?:all )?(?:the )?(?:route|map|work|implementation|changes?) "
        r"(?:is|are) (?:complete|done|ready|approved|valid|good)",
        normalized,
    ) or re.fullmatch(r"(?:all )?(?:checks|tests) (?:pass|passed)", normalized)
    return bool(words) and proxy is None and not set(normalized.split()) <= proxy_words


def read_receipt(
    map_path: Path,
    value: str,
    repositories: tuple[Repository, ...],
    errors: list[str],
) -> tuple[Path, dict[Path, str]] | None:
    supplied = Path(value)
    candidate = map_path.parent / supplied
    if candidate.is_symlink():
        errors.append("map: Closure receipt must not be a symlink")
        return None
    path = candidate.resolve()
    if supplied.is_absolute() or map_path.parent not in path.parents:
        errors.append("map: Closure receipt must stay inside the route directory")
        return None
    if not path.is_file():
        errors.append(f"map: Closure receipt does not exist: {path}")
        return None
    text = visible(path.read_text())
    receipt_fields = preamble(text)
    if any(
        values(receipt_fields, name)
        for name in ("Review range", "Decision", "Findings and gaps")
    ):
        errors.append(f"{path}: contains a legacy review receipt field")
    route_id = one_value(receipt_fields, "Route id", str(path), errors, required=True)
    route_state = one_value(
        receipt_fields, "Route state", str(path), errors, required=True
    )
    claim = one_value(receipt_fields, "Claim", str(path), errors, required=True)
    supported = one_value(
        receipt_fields, "Claim supported", str(path), errors, required=True
    )
    if route_id != map_path.parent.name:
        errors.append(f"{path}: Route id does not match the route directory")
    expected_state = f"sha256:{route_state_digest(map_path.parent)}"
    if route_state and route_state != expected_state:
        errors.append(f"{path}: Route state does not match authoritative route bytes")
    if claim and not concrete_claim(claim):
        errors.append(f"{path}: Claim must be concrete and nonproxy")
    if supported not in {"yes", "no"}:
        errors.append(f"{path}: Claim supported must be `yes` or `no`")
    reviewed_body = one_section(text, "Reviewed repositories", str(path), errors)
    checks = one_section(text, "Checks", str(path), errors)
    findings = one_section(text, "Findings", str(path), errors)
    if not checks.strip() or not findings.strip():
        errors.append(f"{path}: Checks and Findings must be nonempty")
    if supported == "yes" and not empty(findings):
        errors.append(f"{path}: Claim supported yes requires Findings none")

    reviewed: dict[Path, str] = {}
    for line in (line for line in reviewed_body.splitlines() if line.strip()):
        match = RECEIPT_REPO.fullmatch(line)
        root = git_root(path_for(map_path.parent, match.group(1).strip())) if match else None
        if not match or root is None:
            errors.append(f"{path}: malformed reviewed repository line: {line!r}")
            continue
        identity = git_identity(root)
        head = match.group(2)
        if identity is None:
            errors.append(f"{path}: could not identify reviewed repository")
            continue
        if identity in reviewed or not resolve_commit(root, head, require_full=True):
            errors.append(f"{path}: duplicate repository or invalid Reviewed head")
        reviewed[identity] = head

    clean: dict[Path, str] = {}
    for line in checks.splitlines():
        if "Clean worktree:" not in line:
            continue
        match = CLEAN.fullmatch(line)
        root = git_root(path_for(map_path.parent, match.group(1).strip())) if match else None
        if not match or root is None:
            errors.append(f"{path}: malformed Clean worktree observation")
            continue
        identity = git_identity(root)
        if identity is None:
            errors.append(f"{path}: could not identify Clean worktree repository")
            continue
        if identity in clean:
            errors.append(f"{path}: duplicate Clean worktree observation")
        clean[identity] = match.group(2)
    expected = {repository.identity for repository in repositories}
    if set(reviewed) != expected:
        errors.append(f"{path}: reviewed repositories must exactly match the map")
    if set(clean) != expected or any(clean[key].lower() != reviewed.get(key, "").lower() for key in clean):
        errors.append(f"{path}: require one matching Clean worktree observation per repo")
    if supported != "yes":
        errors.append("map: closure receipt must say Claim supported: yes")
    return path, reviewed


def evidence(
    repo: Path, errors: list[str], description: str, *args: str
) -> str | None:
    result = git(repo, *args)
    if result.returncode:
        errors.append(f"map: Git {description} failed")
        return None
    return result.stdout


def validate_closure(
    map_path: Path,
    repositories: tuple[Repository, ...],
    receipt: tuple[Path, dict[Path, str]] | None,
    errors: list[str],
) -> None:
    tracker = git_root(map_path.parent)
    if tracker is None:
        errors.append("map: resolved route is not in Git")
        return
    route = map_path.parent.relative_to(tracker)
    map_rel = map_path.relative_to(tracker).as_posix()
    status = evidence(
        tracker,
        errors,
        "resolved route status",
        "status",
        "--porcelain",
        "--untracked-files=all",
        "--",
        route.as_posix(),
    )
    if status is not None and status.strip():
        errors.append("map: resolved tracker route has uncommitted state")
    history = evidence(
        tracker,
        errors,
        "resolved map history",
        "log",
        "-1",
        "--format=%H",
        "--",
        map_rel,
    )
    map_commit = history.strip() if history is not None else ""
    if history is not None and not map_commit:
        errors.append("map: resolved map is not committed at tracker HEAD")
    for path in authoritative_paths(map_path.parent):
        relative = path.relative_to(tracker).as_posix()
        recorded = git_bytes(tracker, "show", f"HEAD:{relative}")
        if recorded.returncode:
            errors.append(
                f"{path}: authoritative route file is not tracked at tracker HEAD"
            )
        elif recorded.stdout != path.read_bytes():
            errors.append(
                f"{path}: authoritative route bytes do not match tracker HEAD"
            )
    if map_commit:
        ancestry = git(tracker, "merge-base", "--is-ancestor", map_commit, "HEAD")
        if ancestry.returncode == 1:
            errors.append("map: closure commit is not an ancestor of tracker HEAD")
        elif ancestry.returncode:
            errors.append("map: Git closure ancestry check failed")
        else:
            later = evidence(
                tracker, errors, "post-closure route history", "log", "--format=%H",
                f"{map_commit}..HEAD", "--", route.as_posix(),
            )
            if later is not None and later.strip():
                errors.append("map: route changed after its closure commit")
    if repositories:
        branch = evidence(tracker, errors, "tracker branch check", "symbolic-ref", "-q", "HEAD")
        if branch is not None and branch.strip().startswith("refs/heads/integration/"):
            errors.append("map: tracker closure must be committed on a non-integration branch")
    reviewed = receipt[1] if receipt else {}
    if receipt and map_commit:
        receipt_rel = receipt[0].relative_to(tracker).as_posix()
        receipt_history = evidence(
            tracker, errors, "closure receipt history", "log", "-1", "--format=%H",
            "--", receipt_rel,
        )
        if receipt_history is not None and map_commit != receipt_history.strip():
            errors.append("map: resolved map and closure receipt must be in the same commit")
        elif receipt_history is not None:
            changed_text = evidence(
                tracker, errors, "closure diff-tree", "diff-tree", "--root", "-m",
                "--no-commit-id", "--name-only", "-r", map_commit,
            )
            changed = set(changed_text.splitlines()) if changed_text is not None else set()
            if changed_text is not None and (
                not {map_rel, receipt_rel} <= changed
                or any(not Path(path).is_relative_to(route) for path in changed)
            ):
                errors.append("map: closure commit must contain map and receipt and touch only route files")
    for repository in repositories:
        head = reviewed.get(repository.identity)
        if head and head.lower() != repository.ref_head.lower():
            errors.append(f"map: Reviewed head does not equal current Ref head for {repository.label}")
        status = evidence(
            repository.root, errors, f"execution worktree status for {repository.label}",
            "status", "--porcelain", "--untracked-files=all",
        )
        if status is not None and status.strip():
            errors.append(f"map: execution worktree is not clean: {repository.label}")


def validate_digest(route: Path, errors: list[str]) -> None:
    path = route / "digest.md"
    if not path.is_file():
        return
    if path.is_symlink():
        errors.append(f"{path}: digest must not be a symlink")
        return
    text = path.read_text()
    if len(text.splitlines()) > DIGEST_MAX_LINES:
        errors.append(f"{path}: digest exceeds 120 lines")
    if len(text.split()) > DIGEST_MAX_WORDS:
        errors.append(f"{path}: digest exceeds 1000 words")
    state = visible(text)
    state_names = "|".join(re.escape(name) for name in DIGEST_FIELDS)
    section_names = "|".join(re.escape(name) for name in DIGEST_SECTIONS)
    state_pattern = rf"(?m)^(?:{state_names}):|^## (?:{section_names})$"
    if re.search(state_pattern, state):
        errors.append(f"{path}: digest shadows route state")
    if re.search(r"(?:^|[(/])issues/[^)\s]+\.md", state):
        errors.append(f"{path}: digest must not index route units")


def validate(
    map_path: Path,
    warnings: list[str] | None = None,
    derived: dict[str, list[str]] | None = None,
) -> list[str]:
    errors: list[str] = []
    local_warnings: list[str] = []
    state = {"claimed": [], "blocked": [], "frontier": []}
    supplied_map = map_path.expanduser()
    supplied_route = supplied_map.parent
    if supplied_map.is_symlink():
        errors.append(f"{supplied_map}: map must not be a symlink")
    if supplied_route.is_symlink():
        errors.append(f"{supplied_route}: route directory must not be a symlink")
    if (supplied_route / "issues").is_symlink():
        errors.append(
            f"{supplied_route / 'issues'}: issues directory must not be a symlink"
        )
    if errors:
        return errors
    map_path = supplied_map.resolve()
    if not map_path.is_file():
        return [f"{map_path}: map file does not exist"]
    if map_path.name != "map.md" or map_path.parent.parent.name != ".scratch":
        errors.append("map: local route must be at .scratch/<route>/map.md")
    text = visible(map_path.read_text())
    map_fields = preamble(text)
    if LEGACY.search(text):
        errors.append("map: contains legacy through-line state")
    schema = one_value(map_fields, "Schema", "map", errors, required=True)
    status = one_value(map_fields, "Status", "map", errors, required=True)
    execution = one_value(
        map_fields, "Repository execution", "map", errors, required=True
    )
    if schema != "through-line/v2":
        errors.append("map: Schema must be `through-line/v2`")
    if status not in {"open", "resolved"}:
        errors.append("map: Status must be `open` or `resolved`")
    if execution not in {"in-scope", "out-of-scope"}:
        errors.append("map: Repository execution must be `in-scope` or `out-of-scope`")
    bodies = {name: one_section(text, name, "map", errors) for name in MAP_SECTIONS}
    if empty(bodies["Destination"]) or empty(bodies["Decision rights"]):
        errors.append("map: Destination and Decision rights must be nonempty")

    units = read_units(map_path.parent, errors)
    validate_dependencies(units, errors, state)
    all_resolved = bool(units) and all(unit.status == "resolved" for unit in units)
    closure_ready = all_resolved and empty(bodies["Deferred"])
    if status == "resolved" and not any(unit.outcome for unit in units):
        errors.append("map: resolved route requires at least one Outcome unit")
    closure_value = one_value(map_fields, "Closure receipt", "map", errors)
    repositories: tuple[Repository, ...] = ()
    receipt = None
    if execution == "out-of-scope":
        for name in ("First result", "Effort expectation", "Closure receipt"):
            if values(map_fields, name):
                errors.append(f"map: {name} is execution-only")
        if section_bodies(text, "Repositories"):
            errors.append("map: ## Repositories is execution-only")
        if status == "resolved" and not closure_ready:
            errors.append("map: resolved route requires all units resolved and Deferred empty")
        if status == "open" and closure_ready:
            errors.append("map: decision-only route satisfies closure but Status is open")
    elif execution == "in-scope":
        for name in ("First result", "Effort expectation", "Closure receipt"):
            value = one_value(map_fields, name, "map", errors)
            if value is None:
                errors.append(f"map: in-scope execution requires {name}")
            elif name != "Closure receipt" and value.lower() in {"none", "pending"}:
                errors.append(f"map: {name} must be concrete")
        repo_body = one_section(text, "Repositories", "map", errors)
        repositories = read_repositories(map_path, repo_body, local_warnings, errors)
        if status == "resolved":
            for repository in repositories:
                if (
                    repository.review_head is None
                    or repository.review_head.lower() != repository.ref_head.lower()
                ):
                    errors.append(
                        f"map: resolved route requires current Review for "
                        f"{repository.label}"
                    )
                if repository.review_reference != closure_value:
                    errors.append(
                        f"map: resolved Review reference must equal Closure receipt "
                        f"for {repository.label}"
                    )
                if repository.pr == "pending":
                    errors.append(
                        f"map: resolved route requires PR to be `none` or HTTP(S) "
                        f"for {repository.label}"
                    )
        if status == "open" and closure_value and closure_value != "pending":
            errors.append("map: open execution route must keep Closure receipt pending")
        elif closure_value and closure_value != "pending":
            receipt = read_receipt(map_path, closure_value, repositories, errors)
        if status == "resolved":
            if not closure_ready:
                errors.append("map: resolved route requires all units resolved and Deferred empty")
            if not closure_value or closure_value == "pending":
                errors.append("map: resolved execution route requires a closure receipt")
    if status == "resolved":
        validate_closure(map_path, repositories, receipt, errors)

    validate_digest(map_path.parent, errors)
    if warnings is not None:
        warnings.extend(local_warnings)
    if derived is not None:
        derived.update(state)
    return errors


def main() -> int:
    if len(sys.argv) == 3 and sys.argv[1] == "--digest":
        supplied = Path(sys.argv[2]).expanduser()
        if (
            supplied.is_symlink()
            or supplied.parent.is_symlink()
            or (supplied.parent / "issues").is_symlink()
            or not supplied.is_file()
        ):
            print("ERROR: digest requires a regular in-route map", file=sys.stderr)
            return 1
        print(f"sha256:{route_state_digest(supplied.resolve().parent)}")
        return 0
    if len(sys.argv) != 2:
        print(
            "usage: validate_local_map.py [--digest] PATH/TO/map.md",
            file=sys.stderr,
        )
        return 2
    warnings: list[str] = []
    state: dict[str, list[str]] = {}
    errors = validate(Path(sys.argv[1]), warnings, state)
    for warning in warnings:
        print(f"WARN: {warning}", file=sys.stderr)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        f"OK: {sys.argv[1]} (claimed={len(state['claimed'])}, "
        f"blocked={len(state['blocked'])}, frontier={len(state['frontier'])})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
