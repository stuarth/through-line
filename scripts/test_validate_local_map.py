#!/usr/bin/env python3

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from validate_local_map import validate


class ValidateLocalMapTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "issues").mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write(self, relative: str, body: str) -> None:
        (self.root / relative).write_text(body)

    def test_accepts_exact_partition_and_resolved_blockers(self) -> None:
        self.write(
            "map.md",
            """Label: through-line:map
Status: open

## Destination
Reach it.
## Notes
Human-owned.
## Local policies
## Decisions so far
- [Choose shape](issues/02-choose-shape.md) — Chose the round shape.
## Findings
- [Research source](issues/01-research-source.md) — Source exposes editions.
## Not yet specified
## Out of scope
- [Deferred service](https://example.com/deferred) — Beyond this destination.
""",
        )
        self.write(
            "issues/01-research-source.md",
            """Type: research
Status: resolved
Assignee: agent

# Research source
## Question
Which facts exist?
## Resolution
The source exposes editions.
""",
        )
        self.write(
            "issues/02-choose-shape.md",
            """Type: decision
Status: resolved
Assignee: agent
Blocked by: 01

# Choose shape
## Question
Which shape follows?
## Resolution
Use the round shape.
""",
        )

        self.assertEqual([], validate(self.root / "map.md"))

    def test_rejects_stale_blocked_state_and_open_index_entry(self) -> None:
        self.write(
            "map.md",
            """Label: through-line:map
Status: open

## Destination
Reach it.
## Notes
Human-owned.
## Local policies
## Decisions so far
- [Choose shape](issues/02-choose-shape.md) — Not actually closed.
## Findings
- [Research source](issues/01-research-source.md) — Source exposes editions.
## Not yet specified
## Out of scope
""",
        )
        self.write(
            "issues/01-research-source.md",
            """Type: research
Status: resolved
Assignee: agent

# Research source
## Question
Which facts exist?
## Resolution
The source exposes editions.
""",
        )
        self.write(
            "issues/02-choose-shape.md",
            """Type: decision
Status: blocked
Assignee: agent
Blocked by: 01

# Choose shape
## Question
Which shape follows?
""",
        )

        errors = validate(self.root / "map.md")
        self.assertTrue(any("marked blocked without an unresolved blocker" in e for e in errors))
        self.assertTrue(any("blocked ticket cannot retain Assignee" in e for e in errors))
        self.assertTrue(any("open ticket appears in a closed index" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
