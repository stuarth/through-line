# Local Markdown wayfinding operations

Use this fallback only when the repo has no issue-tracker doc.

- **Map:** `.scratch/<effort>/map.md`, with `Label: through-line:map` and
  `Status: open|resolved`.
- **Child:** `.scratch/<effort>/issues/NN-<slug>.md`, with `Type:
  decision|research|prototype|task`, `Status: open|claimed|blocked|resolved`, and the
  question under `## Question`. Further sections—`## Derived implications`,
  `## Builder discretion`, `## Provisional verdict`, `## Verdict history`,
  `## Resolution`, `## Resumption checkpoint`—carry the meanings
  [Map and tickets](../SKILL.md#map-and-tickets) defines.
- **Claim:** add `Assignee: <dev>` and set `Status: claimed` before work. Work that
  lands in a repository also adds `Repository: <repo>` when the map spans more than
  one, and `Branch: <branch>` once it exists.
- **Unclaim:** remove `Assignee` and set `Status: blocked` when an unresolved blocker
  exists, otherwise `Status: open`.
- **Blocking:** add `Blocked by: NN, NN`. Use `blocked` only while at least one named
  blocker is unresolved.
- **Frontier:** open, unblocked, unclaimed child files, ordered by number.
- **Resolve:** append `## Resolution`, set `Status: resolved`, retain the assignee,
  then update the map through [Record](../SKILL.md#record).
- **Commit:** when the map lives in a repository, commit tracker changes with the
  work they record.

Create child files first, then wire blockers once their numbers exist. Take the next
number from a fresh listing of the issues directory — concurrent sessions also mint
numbers — and never reuse one. Bare numbers are tracker metadata only.
