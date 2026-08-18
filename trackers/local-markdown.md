# Local Markdown wayfinding operations

Use this fallback only when the repo has no issue-tracker doc.

- **Map:** `.scratch/<effort>/map.md`, with `Label: through-line:map`,
  `Status: open|resolved`, and `Repository execution: in-scope|out-of-scope`. Set
  execution in scope when the destination includes repository deliverables. An
  in-scope map also adds `Tracker state: pending` and `## Execution heads` with a
  single `- Repository: <path>; Code base: <full commit hash>; Integration head:
  <full commit hash>; Reviewed code head: <full commit hash or pending>; Closure
  state: <full commit hash or pending>; PR: <URL, none, or pending>; Review receipt:
  <local Markdown path or pending>` line per repository. Use a local
  `integration/<effort>` branch as the canonical head and advance it only through
  [Execution](../EXECUTION.md). A PR URL means the current integration head is
  exposed. Replace every closure `pending` before final validation. For a
  cross-repository effort, Notes carries the exact `Tracker authority: Repository:
  <path>; Ref: <branch>; Map: <repository-relative path>` line. Each secondary
  repository stores that same line at `.scratch/<effort>/tracker-pointer.md`; never
  mirror the map.
- **Digest:** `.scratch/<effort>/digest.md`, per
  [Coordination](../SKILL.md#coordination); absent until a session records one. It is
  the bounded orientation index, not the store for all effort knowledge.
- **Reference:** `.scratch/<effort>/references/<topic>.md`, linked from the digest
  and relevant tickets when a reusable discovery needs more depth. Keep one note per
  topic and load it only for work it reaches.
- **History:** `.scratch/<effort>/history/NN-<slug>.md`, created only when a ticket
  has superseded material worth retaining and linked from that ticket. History is
  context, not authority.
- **Child:** `.scratch/<effort>/issues/NN-<slug>.md`, with `Type:
  decision|research|prototype|task`, `Status: open|claimed|blocked|resolved`, and the
  question under `## Question`. Further sections—`## Derived implications`,
  `## Builder discretion`, `## Provisional verdict`, `## Resolution`, `## Resumption
  checkpoint`—carry the meanings
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
  then update the map through [Record](../SKILL.md#record). Repository resolutions
  record `Candidate commit` and `Integrated commit`; deferred seam reviews follow
  [Execution](../EXECUTION.md#review-and-correction).
- **Reopen:** while the map is open, move the old Resolution to the ticket's history
  artifact and leave one linked `History: <path>` pointer; remove it from the map's
  closure index, remove its assignee, set `Status: open` or `blocked`, increment
  `Reopened: <count>`, and add one current `## Convergence verdict`. List resolved
  consumers under `## Affected resolved dependents`; at re-resolution replace that
  list with `## Dependent disposition`, marking each `stands` or `reopens`. A second
  reopening also records one current `## Falsify audit`; later qualifying reopenings
  replace it and archive the superseded audit.
- **Closure review receipt:** use a dedicated Markdown file containing `Review
  range: <base>..<head>`, a nonempty `Claim` covering the Destination and protected
  meanings, `Decision: approved|rejected`, nonempty `Checks`, and nonempty `Findings
  and gaps`. A rejected receipt keeps the map open and reopens affected roots, or one
  integrated outcome when no root owns the defect. After approval, set each `Closure
  state` to the execution repository's current full commit hash after verifying its
  worktree is clean. Immediately before committing the resolved tracker, verify each
  repository still has that clean HEAD. Then commit the resolved tracker with
  `Tracker state: pending`.
  In one tracker-only attestation commit, replace `Tracker state: pending` with that
  preceding resolved-tracker commit's full hash, then rerun the validator. When the
  tracker shares an execution repository, its closure state must be the parent of
  the recorded tracker state. Both commits change tracker files only, and the
  attestation changes only the map. The recorded tracker-state commit remains
  unchanged afterward.
  A resolved local map must be tracked in Git with a clean tracker directory; keep
  its receipt committed inside that directory.
- **Post-closure correction:** reopen the same canonical map, create a correction
  ticket with `Correction of: <root ticket>; Concern: <stable invariant>`, reset the
  current `Closure state` and `PR` to `pending`, and retain the prior PR and closure
  through history and its recorded tracker-state commit. Re-close through the same
  protocol with a new **Final map closure** task and tracker state.
- **Checkpoint:** use the exact `## Resumption checkpoint` heading. Repository edits
  follow [Execution](../EXECUTION.md)'s durable checkpoint schema. Remove the
  checkpoint when the ticket resolves.
- **Commit:** make claim, human-verdict, checkpoint, resolution, and map-closure state
  durable immediately; batch tracker edits between those transitions.

Create child files first, then wire blockers once their numbers exist. Bare numbers
are tracker metadata only.
