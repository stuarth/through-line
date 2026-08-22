# Review

Review one immutable **object** against one explicit **claim** as a read-only leaf.
Its receipt stands until the object or claim changes. A fresh reviewer receives only
the review packet, never the implementer's or supervisor's conversation. Do not
coordinate or implement.

The claim is the assertion the caller will rely on. It must cover the applicable
acceptance criteria, not a proxy such as `checks passed` or `artifacts exist`.
Approval alone authorizes nothing: a gate passes only when both the receipt's object
and claim match the object and claim that gate requires.

Load the map's orientation digest only when the review spans tickets or repositories;
otherwise load only references that reach the object.

For an initial review, use the ticket, premises, object, and claim. For a correction
under the same claim, use the prior receipt and changed object range: confirm the
prior findings are resolved and judge what changed. Coverage of everything untouched
stands on the prior receipt. A changed or distinct downstream claim requires a fresh
review of the whole object; it may cite the earlier receipt.

For a seam review, the object is the composed range holding both sides and the claim
is the named invariant across them. Trace that complete path instead of treating
either candidate in isolation. Include the deferred-review receipts the seam reaches.

When the claim authorizes a paid or externally consequential effect, the object is
the exact state that will execute. Review its head and configuration, budgets and
stop conditions, recovery behavior, and executable launch-time preconditions for
time-sensitive facts.

When the object is run evidence, review its claim against the ticket's acceptance
criteria and the receipt that authorized execution. Verify the provenance, terminal
accounting, safety claims, and independently checkable basis the stated claim relies
on; do not demand guarantees that belong only to a later exposure boundary.

For map closure, review the whole effort from its recorded base through the proposed
closure head. Prior ticket reviews are context, not inherited proof. Compare every
protected meaning to its cited human verdict and construct failures across authority,
currentness, concurrency, and consumer boundaries. Before deciding, verify each
execution repository has a clean worktree and its current HEAD is the proposed
closure state; record that observation in Checks.

Report only material findings: acceptance failures or evidenced correctness,
security, or data-integrity failures. Leave optional hardening, adjacent cleanup, and
broader completeness ideas outside this ticket. Run only the checks named for review.

For persisted authorities, probe alternate writers, temporal bounds, exact
provenance, replacement and equal recapture, reassignment, both concurrency race
directions, transition-to-consumer coverage, and scope or visibility isolation where
they apply. Deterministic replay proves reproducibility, not semantic correctness;
each semantic claim needs an independently failing counterexample.

If one named risk needs expertise you do not have, return that risk for one specialist
instead of delegating the review.

Use receipt-only coordination: send one terminal receipt; communicate earlier only
for a blocker or durable checkpoint that needs coordination.

Return a compact receipt with:

- `Object`: an identity that fixes the reviewed bytes and execution configuration,
  such as full commit hashes, an immutable version, or content digests;
- `Claim`: the exact assertion reviewed;
- `Decision`: `approved` or `rejected`;
- `Checks`;
- `Findings and gaps`, with each finding's open or resolved state and resolution
  evidence; and
- `Prior receipt` when correcting an earlier review. Cite other receipts in `Checks`.

A seam receipt also names every deferral it discharges.

`Decision` judges whether the object supports the claim, so valid evidence that a
candidate failed may be approved. For local-Markdown closure, also follow its
[closure review receipt
format](./trackers/local-markdown.md#local-markdown-wayfinding-operations).
