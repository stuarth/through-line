# Execution

Use this branch for repository work. The Work session implements its task directly.
Compact receipts carry progress; store them on the task ticket or in one linked
artifact. Finished means durable: a stranger could continue from the tracker,
receipts, and commits alone. A leaf still in flight, a finding unrecorded, or a
tracker unreconciled means the session has not finished.

At every scout, implementer, reviewer, or specialist dispatch, follow [receipt-only
coordination](./SKILL.md#coordination).

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
where size becomes measurable: a plan that reveals a separate human verdict,
independently releasable outcome, or authority boundary returns to the tracker as a
split before implementation. Keep separately implementable steps that compose into
one outcome as packets in this ticket's plan.

Before editing, record a compact plan on the ticket — only what the ticket does not
already settle: exact entry points and constraints, route choices the implementation
fixes, focused checks, and exclusions. For persistent data work, include the
governing schema and an isolated database check. The plan is ready when
implementation can proceed from those entry points without a new product or
architecture decision.

Use independently falsifiable authority and consumer boundaries to shape packets and
checks. Keep parts that must land together to avoid two live authorities in one
ticket and compose their candidate commits before acceptance. A packet that cannot
reach a committed candidate before a human gate sharpens the remaining plan; split
the ticket only when the resulting outcome meets the ticket rule above.

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
path: green focused evidence, a review check, or a named deferred check recorded as
a `Deferred review` when it waits for a seam. Record the base and candidate commits,
changed files, acceptance mapping, focused checks, and any remaining gap when the
candidate hands off to a reviewer or a checkpoint; a ticket closing in this session
records that evidence once, in its Resolution.

For each protected invariant touched, the acceptance mapping names its verdict,
implementing authority, persistence fence when applicable, positive test, adversarial
test, and affected transition consumers. A missing or contradictory human-owned
verdict stops before candidate freeze.

## Review and correction

An **exposure boundary** is a PR, a human approval gate, shared or production data or
effects, or map closure. Review a candidate before composition when it reaches
security-sensitive surfaces (authorization, untrusted input, secrets, crypto),
destructive behavior, a migration or command executed beyond a disposable
environment, or a human-owned class.

A candidate reaching persisted contracts or concurrency may compose on its
acceptance mapping and green adversarial checks. Defer its independent review to the
first **seam** where the integration head holds both sides: contract and first
consumer, lock and racing writers, or transition and its consumers. Record
`Deferred review: seam pending — <named invariant>` in the candidate receipt and
carry it into the resolution while that seam remains incomplete. Discharge every
deferral before the head crosses an exposure boundary, replacing it with `Deferred
review: discharged — <receipt>`. Other candidates proceed to Verify on green focused
checks with every criterion's verification path intact and record the review waiver
and reason. A candidate in both classes receives its required pre-composition review
and still records the seam deferral.

When review runs, record its exact object and claim on the ticket, then give one fresh
integrated reviewer the ticket or seam, premises, object, claim, only the references
that reach them, and [REVIEW.md](./REVIEW.md). Add a specialist only for a named risk
the reviewer cannot judge. Record the receipt and any seam deferrals it discharges.

When a receipt rejects implementation that the ticket authorizes correcting, fix
related findings together as the smallest complete correction. Return the correction
range and prior receipt for a targeted pass — to the same reviewer when resumption
answers at once, otherwise to a fresh reviewer. Judge the correction range against
the prior findings. Coverage of work the correction leaves untouched stands on the
prior receipt.
Start over only when the correction materially changes the candidate's architecture,
authority, persistence, destructive behavior, or overall shape.

Keep adjacent hardening out of the correction loop. After two material correction
cycles, revisit the unit's shape and checkpoint it for a fresh Work session unless
one bounded correction clearly closes the review.
When evidence invalidates a previously accepted result, return to
[Falsify](./WORK.md#falsify) and reopen its root before producing another candidate.

### Consequential effects

A paid or externally consequential effect proceeds only when an approved receipt
covers its exact execution state and safe execution; an earlier receipt suffices
when it already covers both. Run its launch-time preconditions immediately before
the effect, record their results on the ticket, and include them with its outputs.
Execute only with every precondition green; after a failure, rerun them all before a
later attempt, and reuse the receipt only while its object and claim remain unchanged.

After the effect, review its immutable outputs before relying on their claim. An
approved receipt validates that claim, not the candidate. Resolve a fixed-candidate
evaluation with its honest result.

## Verify and record

After review, waiver, or a recorded seam deferral, compose the candidate onto the
map's current local integration head. Use the candidate commit directly when it
descends from the recorded head; otherwise create a merge commit. Advance the ref
atomically with `git update-ref <ref> <new> <expected-old>`; when another session
wins that compare-and-swap, rebuild the composition and rerun the checks that change
invalidated.
Publishing a branch or PR remains an external promise under the map's decision
rights. When new local work follows an earlier exposure, retain its URL in history
and set the current `PR` field to `pending` before advancing the integration head.

After composition and before resolution, inspect every pending seam deferral the
candidate reaches. When the new head completes a named seam, dispatch that seam
review now and discharge its receipts; do not leave a complete seam for closure.

Run the plan's focused and integration checks on the composed state, keeping full
output outside conversation and recording only command, integrated commit, status,
duration, and useful failure excerpt. The full suite follows the map's verification
policy and defaults to once before each exposure boundary. A material reconciliation
edit returns to review or correction; afterward rerun every check it invalidated.

Resolve the ticket when its recorded evidence — candidate commit, integrated commit,
reviews run or deferred with their seam named, and verification — describes the same
final work. Advance the map's **Integration head**, propagate through the map,
reconcile the tracker, validate it, and stop after this ticket's cascade.
