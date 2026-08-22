# Execution

Execute one claimed outcome unit, then return its result to
[Advance](./ADVANCE.md) for propagation. The unit and charter bound repository work.

## Plan

Load the unit, reaching premises and principles, relevant receipts, and repository
state. Record only unsettled details: intended outcome, exact entry points,
constraints, consequential boundaries, and focused checks. Return an unresolved
product, architecture, or human-owned decision to the route.

Scale checks to maturity and consequence. For the first end-to-end result, test its
observable boundaries and highest-risk assumptions; defer broad matrices around
moving internal interfaces. Add integration, regression, recovery, and operational
evidence as the result stabilizes or approaches a consequential boundary. A **fenced
disposable** environment has isolated expendable inputs and state, effects that
cannot escape, and honest output. Shared or durable state is not disposable.

## Implement and integrate

Implement directly or send a self-contained leaf packet with
[IMPLEMENT.md](./IMPLEMENT.md). Give a leaf its exact repository, base hash, isolated
worktree, owned files, entry points, constraints, and focused checks. The coordinator
retains integration and route ownership.

Each repository has one route-named integration **Ref**, created at its recorded Base
through the tracker adapter. It is the sole integration identity. Compose a checked
leaf onto the hash currently at Ref, verify that old hash is an ancestor of the new
hash, rerun checks on the composed result, then advance Ref with compare-and-swap:

```sh
git update-ref <Ref> <new-hash> <expected-old-hash>
```

If the compare-and-swap loses, reload, recompose, and rerun checks the changed range
could invalidate. Record each integration check's command, exact hash, status,
duration, and useful failure excerpt.

## Review stable boundaries

Review the exact integrated head and relied-on claim with
[REVIEW.md](./REVIEW.md) when it establishes an architecture, provider, security, or
human-owned contract that later work will rely on. Also review the exact integrated
head set and relevant configuration before a PR or publication, shared or production
effect, paid or irreversible action, dependent human gate, or closure. Integrating
reversible local work alone does not require review.

Reuse a receipt only while its exact object, configuration, and claim remain
unchanged. `Claim supported: no` stops advancement past that boundary and returns the
finding to the owning unit.

## Consequential effects

`Claim supported: yes` is evidence, never authorization. Effects follow
[Advance's effect procedure](./ADVANCE.md#resolve).

Record terminal result, provenance, outputs, and accounting honestly. A negative
predeclared evaluation stands; do not change its object to manufacture success.

## Correct or finish

Correct related findings as the smallest complete change. Give the reviewer the
prior receipt and changed range; use the same reviewer only immediately, otherwise a
fresh one. After two failed cycles that produce no new outcome evidence, return to
Advance to rechart the unit's representation, boundary, or success basis.

On completion, return a Resolution naming integrated hashes, outcome, provenance,
checks, reviews, and effect evidence to Advance. If unfinished, commit coherent state
or store a durable patch against a verified base, then return a checkpoint with base
and Ref hashes, dirty state, completed work, evidence, blocker, and exact next step.
Keep an uncommitted worktree claimed.

## Close the route

Prepare the final map and units, then obtain a fresh closure review under
[REVIEW.md](./REVIEW.md) of their exact bytes, every Base-to-Ref range, relevant
configuration, and the destination claim. If the claim is unsupported, reopen the
unit that owns each finding or create one correction outcome when none does, and
return to Advance.

If supported, record the route-state digest, exact reviewed heads, checks, and
findings in the closure receipt, then resolve the route through the active tracker
adapter. The closure commit records route state; it does not advance an integration
Ref. Return to Advance for final validation and stop.
