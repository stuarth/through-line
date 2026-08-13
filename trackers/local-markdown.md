# Local Markdown wayfinding operations

Use this fallback only when the repo has no issue-tracker doc.

- **Map:** `.scratch/<effort>/map.md`, with `Label: through-line:map` and
  `Status: open|resolved`. Set `Repository execution: in-scope|out-of-scope` and
  `Tracker state: pending` explicitly. An in-scope map adds `## Execution heads` with a single
  `- Repository: <path>; Code base: <full commit hash>; Reviewed code head: <full
  commit hash or pending>; Closure state: <full commit hash or pending>; PR: <URL,
  none, or pending>; Review receipt: <local Markdown path or pending>` line per
  repository. Replace every `pending` before final validation.
- **Digest:** `.scratch/<effort>/digest.md`, per
  [Coordination](../SKILL.md#coordination); absent until a session records one.
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
- **Closure review receipt:** use a dedicated Markdown file containing `Review
  range: <base>..<head>`, `Decision: approved`, nonempty `Checks`, and nonempty
  `Findings and gaps`. Set each `Closure state` to the execution repository's current
  full commit hash, then commit the resolved tracker with `Tracker state: pending`.
  In one tracker-only attestation commit, replace `Tracker state: pending` with that
  preceding resolved-tracker commit's full hash, then rerun the validator. When the
  tracker shares an execution repository, its closure state must be the parent of
  the recorded tracker state. No other tracker content may change in the attestation
  or afterward.
  A resolved local map must be tracked in Git with a clean tracker directory; keep
  its receipt committed inside that directory.
- **Checkpoint:** use the exact `## Resumption checkpoint` heading. Repository edits
  name `Base`, `Checkpoint head` or a durable patch, `Dirty state`, checks, and next
  stage. Remove the checkpoint when the ticket resolves.
- **Commit:** when the map lives in a repository, commit tracker changes with the
  work they record.

Create child files first, then wire blockers once their numbers exist. Bare numbers
are tracker metadata only.
