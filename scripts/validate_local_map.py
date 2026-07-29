#!/usr/bin/env python3
"""Validate a through-line map using the bundled local-Markdown convention."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

MAP_SECTIONS = [
    "Destination",
    "Notes",
    "Local policies",
    "Decisions so far",
    "Findings",
    "Not yet specified",
    "Out of scope",
]
DECISION_TYPES = {"decision"}
LEGWORK_TYPES = {"research", "prototype", "task"}
TICKET_TYPES = DECISION_TYPES | LEGWORK_TYPES
TICKET_STATUSES = {"open", "claimed", "blocked", "resolved"}


@dataclass(frozen=True)
class Ticket:
    path: Path
    number: str
    kind: str
    status: str
    assignee: str | None
    blockers: tuple[str, ...]
    text: str


def field(text: str, name: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(name)}:\s*(.+?)\s*$", text)
    return match.group(1).strip() if match else None


def numbered(path: Path) -> str | None:
    match = re.match(r"(\d+)-", path.name)
    return str(int(match.group(1))) if match else None


def parse_ticket(path: Path, errors: list[str]) -> Ticket | None:
    text = path.read_text()
    number = numbered(path)
    kind = field(text, "Type")
    status = field(text, "Status")
    assignee = field(text, "Assignee")

    if number is None:
        errors.append(f"{path}: filename must start with NN-")
    if kind not in TICKET_TYPES:
        errors.append(f"{path}: Type must be one of {sorted(TICKET_TYPES)}")
    if status not in TICKET_STATUSES:
        errors.append(f"{path}: Status must be one of {sorted(TICKET_STATUSES)}")
    if "## Question" not in text:
        errors.append(f"{path}: missing ## Question")

    blocker_value = field(text, "Blocked by")
    blockers: list[str] = []
    if blocker_value:
        for token in blocker_value.split(","):
            match = re.fullmatch(r"\s*#?0*(\d+)\s*", token)
            if match:
                blockers.append(str(int(match.group(1))))
            else:
                errors.append(f"{path}: invalid blocker {token.strip()!r}")

    if status in {"claimed", "resolved"} and not assignee:
        errors.append(f"{path}: {status} ticket must retain Assignee")
    if status in {"open", "blocked"} and assignee:
        errors.append(f"{path}: {status} ticket cannot retain Assignee")
    if status == "resolved" and not re.search(r"(?m)^## (Resolution|Answer)\s*$", text):
        errors.append(f"{path}: resolved ticket lacks ## Resolution or ## Answer")

    label = field(text, "Label")
    expected_label = f"through-line:{'decision' if kind in DECISION_TYPES else kind}"
    if label and label != expected_label:
        errors.append(f"{path}: Label should be {expected_label}")

    if number is None or kind not in TICKET_TYPES or status not in TICKET_STATUSES:
        return None

    return Ticket(
        path=path.resolve(),
        number=number,
        kind=kind,
        status=status,
        assignee=assignee,
        blockers=tuple(blockers),
        text=text,
    )


def section_spans(text: str, errors: list[str]) -> dict[str, str]:
    headings = list(re.finditer(r"(?m)^## (.+?)\s*$", text))
    names = [match.group(1) for match in headings]
    for name in MAP_SECTIONS:
        if names.count(name) != 1:
            errors.append(f"map: expected exactly one ## {name}")

    positions = [names.index(name) for name in MAP_SECTIONS if name in names]
    if len(positions) == len(MAP_SECTIONS) and positions != sorted(positions):
        errors.append("map: required sections are out of order")

    spans: dict[str, str] = {}
    for index, match in enumerate(headings):
        start = match.end()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        spans[match.group(1)] = text[start:end]
    return spans


def indexed_paths(
    map_path: Path, body: str, errors: list[str], *, allow_external: bool = False
) -> list[Path]:
    indexed: list[Path] = []
    for line in body.splitlines():
        if not re.match(r"^\s*-\s+", line):
            continue
        match = re.search(r"\[[^\]]+\]\(([^)]+)\)", line)
        if not match:
            continue
        target = match.group(1).split("#", 1)[0]
        if re.match(r"^[a-z]+://", target):
            if not allow_external:
                errors.append(f"map: index entry must link a local ticket: {target}")
            continue
        indexed.append((map_path.parent / target).resolve())
    return indexed


def duplicates(paths: list[Path]) -> set[Path]:
    return {path for path in paths if paths.count(path) > 1}


def validate(map_path: Path) -> list[str]:
    errors: list[str] = []
    map_path = map_path.resolve()
    if not map_path.is_file():
        return [f"{map_path}: map file does not exist"]

    map_text = map_path.read_text()
    if field(map_text, "Label") != "through-line:map":
        errors.append("map: Label must be through-line:map")
    map_status = field(map_text, "Status")
    if map_status not in {"open", "resolved"}:
        errors.append("map: Status must be open or resolved")

    spans = section_spans(map_text, errors)
    issues_dir = map_path.parent / "issues"
    if not issues_dir.is_dir():
        errors.append(f"{issues_dir}: issues directory does not exist")
        return errors

    tickets = [
        ticket
        for ticket in (
            parse_ticket(path, errors) for path in sorted(issues_dir.glob("*.md"))
        )
        if ticket is not None
    ]
    by_path = {ticket.path: ticket for ticket in tickets}
    by_number = {ticket.number: ticket for ticket in tickets}
    if len(by_number) != len(tickets):
        errors.append("tickets: duplicate numeric prefixes")

    for ticket in tickets:
        missing = [number for number in ticket.blockers if number not in by_number]
        for number in missing:
            errors.append(f"{ticket.path}: blocker {number} does not exist")
        unresolved = [
            number
            for number in ticket.blockers
            if number in by_number and by_number[number].status != "resolved"
        ]
        if ticket.status == "blocked" and not unresolved:
            errors.append(f"{ticket.path}: marked blocked without an unresolved blocker")
        if ticket.status != "blocked" and unresolved:
            errors.append(
                f"{ticket.path}: unresolved blockers {', '.join(unresolved)} require Status: blocked"
            )

    decisions = indexed_paths(
        map_path, spans.get("Decisions so far", ""), errors
    )
    findings = indexed_paths(map_path, spans.get("Findings", ""), errors)
    out_of_scope = indexed_paths(
        map_path, spans.get("Out of scope", ""), errors, allow_external=True
    )
    indexed = decisions + findings + out_of_scope

    for path in duplicates(indexed):
        errors.append(f"map: ticket indexed more than once: {path.name}")
    for path in indexed:
        if path not in by_path:
            errors.append(f"map: index target is not a child ticket: {path}")

    decision_set = set(decisions)
    finding_set = set(findings)
    out_set = set(out_of_scope)
    for ticket in tickets:
        if ticket.status != "resolved":
            if ticket.path in decision_set | finding_set | out_set:
                errors.append(f"map: open ticket appears in a closed index: {ticket.path.name}")
            continue

        if ticket.path in out_set:
            continue
        expected = decision_set if ticket.kind in DECISION_TYPES else finding_set
        wrong = finding_set if ticket.kind in DECISION_TYPES else decision_set
        if ticket.path not in expected:
            section = "Decisions so far" if ticket.kind in DECISION_TYPES else "Findings"
            errors.append(f"map: resolved {ticket.kind} missing from {section}: {ticket.path.name}")
        if ticket.path in wrong:
            errors.append(f"map: resolved {ticket.kind} is in the wrong index: {ticket.path.name}")

    if map_status == "resolved":
        open_tickets = [ticket.path.name for ticket in tickets if ticket.status != "resolved"]
        if open_tickets:
            errors.append(f"map: resolved with open tickets: {', '.join(open_tickets)}")

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
