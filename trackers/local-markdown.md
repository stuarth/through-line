# Local Markdown adapter

Use this adapter only when the repository has no issue-tracker instructions. A route
lives at `.scratch/<route>/`: `map.md` is the charter,
`issues/NN-<slug>.md` are units, and optional reusable discoveries live under
`references/`.

## Map

```markdown
Schema: through-line/v2
Status: open
Repository execution: out-of-scope

## Destination
<observable destination>
## Decision rights
<human/builder boundary>
## Premises
none
## Deferred
none
## Out of scope
none
```

Use `open|resolved` for Status and `in-scope|out-of-scope` for Repository execution.
Each nonempty Deferred entry names the outcome, `human|builder` owner, and evidence
that would activate it. An in-scope map also has:

```markdown
First result: <smallest end-to-end result>
Effort expectation: <active effort in the human's unit, e.g. 2 active days>
Closure receipt: pending

## Repositories
- Repository: <path>; Base: <full commit>; Ref: refs/heads/integration/<route>; Review: pending; PR: pending
```

Base is immutable after the route's first commit. Create each Ref at Base. After
review, record `Review: <full reviewed commit> @
<durable receipt reference>`. Retain a stale value until a new review replaces it so
the current Ref makes staleness visible. A local reference must exist; HTTP(S) URLs
are also valid. PR is `pending`, `none`, or an HTTP(S) URL; resolve `pending` before
closing the route.

## Units

Use exactly one of Question or Outcome. Acceptance, Reaching premises, and Resumption
checkpoint are optional.

```markdown
Status: open
Owner: human
Blocked by: 01, 02

## Question
<decision to reach>
## Acceptance
<observable acceptance>
## Reaching premises
<premises used to reach this unit>
```

Use `Owner: human|builder`. Only a builder unit may add `Claimed by:
<host-addressable worker/session>`. A resolved unit removes Claimed by and checkpoint,
sets `Status: resolved`, and adds exactly one Resolution:

```markdown
## Resolution
Provenance: <human verdict, review, experiment, or implementation source>
Evidence: <durable result or reference>
```

Claimed, blocked, and frontier are derived: Claimed by means claimed; an open unit
with any unresolved `Blocked by` unit is blocked; every other unclaimed open unit is
frontier. Keep at most one Claimed by field across the route.

Before reopening, commit the current Resolution. Then set Status open, remove that
Resolution, update Reaching premises with the new evidence, and let Git preserve the
old verdict. A dependent that stands records the new premise in its current
Resolution. Commit claim, verdict, checkpoint, resolution, reopen, and map transitions
promptly.

## Closure

Every route ends in a resolved Outcome unit that evidences the Destination. A
decision-only route closes by setting the map resolved and committing a clean route.
An execution route additionally records this receipt at the path in Closure receipt:

```markdown
Route id: <route>
Route state: sha256:<digest of final map and units>
Claim: <concrete destination claim including protected meanings, not “work complete”>
Claim supported: yes

## Reviewed repositories
- Repository: <path>; Reviewed head: <full commit>
## Checks
- Clean worktree: <path> @ <same full commit>
## Findings
none
```

Compute Route state with `scripts/validate_local_map.py --digest <map.md>`; the receipt
is excluded. Each reviewed head must equal its current Ref, and the map's Review for
that repository must name the same head and closure receipt.

Commit the resolved map and receipt together in one commit touching only this route.
Use the tracker branch, not an integration Ref; switch or create one first if an
integration Ref is checked out. The tracker commit neither advances nor needs to
descend from an integration Ref.
Every authoritative file must be tracked with matching bytes, the route and execution
worktrees must be clean, and later route edits require a new route. Validate after
the commit.

## Orientation

`digest.md` is an optional index of discovery entry points and environment facts. It
must not copy map or unit state, index units, exceed 1,000 words, or exceed 120 lines.
