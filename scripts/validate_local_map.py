#!/usr/bin/env python3
"""Check cross-file state in a through-line local-Markdown map."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

INDEX_SECTIONS = ("Decisions so far", "Findings", "Out of scope")
LEGWORK_TYPES = {"research", "prototype", "task"}
TICKET_TYPES = {"decision"} | LEGWORK_TYPES
TICKET_STATUSES = {"open", "claimed", "blocked", "resolved"}


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


FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


def strip_fences(text: str) -> str:
    lines: list[str] = []
    fence: tuple[str, int] | None = None
    for line in text.splitlines():
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
        lines.append(line)
    return "\n".join(lines)


def field(text: str, name: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(name)}:\s*(.+?)\s*$", text)
    return match.group(1).strip() if match else None


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


def section(text: str, name: str, errors: list[str]) -> str:
    matches = list(re.finditer(rf"(?m)^## {re.escape(name)}\s*$", text))
    if len(matches) != 1:
        errors.append(f"map: cannot compare state without exactly one ## {name}")
        return ""

    start = matches[0].end()
    next_heading = re.search(r"(?m)^## ", text[start:])
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end]


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


def validate(map_path: Path) -> list[str]:
    errors: list[str] = []
    map_path = map_path.resolve()
    if not map_path.is_file():
        return [f"{map_path}: map file does not exist"]

    issues_dir = map_path.parent / "issues"
    if not issues_dir.is_dir():
        return [f"{issues_dir}: issues directory does not exist"]

    tickets: list[Ticket] = []
    for path in sorted(issues_dir.glob("*.md")):
        text = strip_fences(path.read_text())
        tickets.append(
            Ticket(
                path=path.resolve(),
                number=ticket_number(path),
                kind=field(text, "Type"),
                status=field(text, "Status"),
                blockers=blockers(text, path, errors),
                assignee=field(text, "Assignee"),
                resolutions=len(re.findall(r"(?m)^## Resolution\s*$", text)),
                checkpoints=len(re.findall(r"(?m)^## Resumption checkpoint\s*$", text)),
                provisionals=len(re.findall(r"(?m)^## Provisional verdict\s*$", text)),
                legacy_actives=len(re.findall(r"(?m)^State: active\s*$", text)),
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
            errors.append(f"{ticket.path}: Status {ticket.status} must not carry an Assignee")
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
        if ticket.status == "resolved":
            if ticket.resolutions != 1:
                errors.append(f"{ticket.path}: resolved without exactly one ## Resolution")
            if ticket.checkpoints:
                errors.append(f"{ticket.path}: resolved with a ## Resumption checkpoint")
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

    map_text = strip_fences(map_path.read_text())
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
            errors.append(f"map: resolved ticket missing from {name}: {ticket.path.name}")

    map_status = field(map_text, "Status")
    if map_status not in {"open", "resolved"}:
        errors.append(f"map: unknown Status {map_status!r}")
    if map_status == "resolved":
        unresolved = [ticket.path.name for ticket in tickets if ticket.status != "resolved"]
        if unresolved:
            errors.append(f"map: resolved with unresolved tickets: {', '.join(unresolved)}")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_local_map.py PATH/TO/map.md", file=sys.stderr)
        return 2

    errors = validate(Path(sys.argv[1]))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {Path(sys.argv[1])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
