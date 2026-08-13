# Execution

Use this branch for repository work. The Work session implements its task directly.
Compact receipts carry progress; store them on the task ticket or in one linked
artifact. Finished means durable: a stranger could continue from the tracker,
receipts, and commits alone. A leaf still in flight, a finding unrecorded, or a
tracker unreconciled means the session has not finished.

## Resume

Load the ticket and its receipts, then continue from the first unfinished or invalid
stage. Keep earlier work when its commits still exist and later edits have not changed
what it established. A checkpoint names that stage and the next plan so resumption
does not repeat orientation, implementation, or review.

A repository checkpoint is durable only when edits are committed on the task branch,
or stored as a durable patch artifact against a verified base. Record **Base**,
**Checkpoint head** or patch, **Dirty state**, completed stage, checks, and next stage.
Keep an uncommitted worktree claimed; never expose it as resumable frontier work.

## Plan

Keep the task atomic per [Map and tickets](./SKILL.md#map-and-tickets). Planning is
where size becomes measurable: a plan that reveals several independently landable
results returns to the tracker as a split — new tickets, wired dependencies, this
claim narrowed to one of them — before any implementation.

Before editing, record a compact plan on the ticket — only what the ticket does not
already settle: exact entry points and constraints, route choices the implementation
fixes, focused checks, and exclusions. For persistent data work, include the
governing schema and an isolated database check. The plan is ready when
implementation can proceed from those entry points without a new product or
architecture decision.

Split by independently falsifiable authority or consumer boundary. When several
parts must land together to avoid two live authorities, keep them as dependent
candidate commits and give their composition a separate integration check. A unit
that cannot reach a committed candidate before a human gate is evidence to split its
remaining work.

Route material to the one context that must hold it: bulk reading to read-only
scouts per [Coordination](./SKILL.md#coordination) when conclusions suffice,
discovery to the leaf that will edit the same files, failing evidence to the leaf
that owns the fix. Delegate implementation only when work is disjoint enough to run
in parallel: give each fresh leaf the ticket and its plan as a packet with
[IMPLEMENT.md](./IMPLEMENT.md). A returned gap sharpens the packet; it does not
widen the leaf's assignment.

## Candidate

Implement the plan — directly, or by landing the delegated packets' receipts — and
run the focused checks, committing only the plan's files. The candidate is ready
when every criterion and reaching premise maps to implementation and a verification
path: green focused evidence, a review check, or a named deferred check. Record the
base and candidate commits, changed files, acceptance mapping, focused checks, and
any remaining gap when the candidate hands off to a reviewer or a checkpoint; a
ticket closing in this session records that evidence once, in its Resolution.

For each protected invariant touched, the acceptance mapping names its verdict,
implementing authority, persistence fence when applicable, positive test, adversarial
test, and affected transition consumers. A missing or contradictory human-owned
verdict stops before candidate freeze.

## Review and correction

Review is required when the candidate reaches persisted contracts, migrations,
concurrency, security-sensitive surfaces (authorization, untrusted input, secrets,
crypto), destructive behavior, or a human-owned class. Otherwise proceed to Verify
on green focused checks with every criterion's verification path intact — none
resting on a review check — and record the waiver and its reason in the resolution.

When review runs, give one fresh integrated reviewer the ticket, premises, candidate
receipt, and [REVIEW.md](./REVIEW.md). Add a specialist only for a named risk the
reviewer cannot judge. Record the candidate range, decision, material findings,
checks, and gaps.

Fix related findings together as the smallest complete correction. Return the
correction range and prior receipt for a targeted pass — to the same reviewer when
resumption answers at once, otherwise to a fresh reviewer. Judge the correction range
against the prior findings. Coverage of work the correction leaves untouched stands
on the prior receipt.
Start over only when the correction materially changes the candidate's architecture,
authority, persistence, destructive behavior, or overall shape.

Keep adjacent hardening out of the correction loop. After two material correction
cycles, revisit the unit's shape and checkpoint it for a fresh Work session unless
one bounded correction clearly closes the review.
Related fixes split across tickets share `Correction of` and `Concern`; return to
[Falsify](./WORK.md#falsify) before charting a third material correction of the same
invariant.

## Verify and record

After review is clean or waived, run deferred checks and the full suite once. Keep full output
outside conversation and record only the command, candidate commit, status, duration,
and useful failure excerpt. An edit returns to correction; afterward rerun the checks
that edit invalidated and the full suite.

Resolve the ticket when its recorded evidence — candidate, review where required,
and verification — describes the same final work. Record the commits and evidence,
propagate through the map, reconcile the tracker, validate it, and stop after this
ticket's cascade.
