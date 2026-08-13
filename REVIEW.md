# Review

Review one fixed candidate as a read-only leaf. Do not coordinate or implement.

For an initial review, use the ticket, premises, candidate receipt, and fixed range.
For a correction, use the prior review receipt and correction range: confirm the
prior findings are resolved and judge the files the correction touches. Coverage of
everything untouched stands on the prior receipt.

For map closure, review the whole effort from its recorded base through the proposed
closure head. Prior ticket reviews are context, not inherited proof. Compare every
protected meaning to its cited human verdict and construct failures across authority,
currentness, concurrency, and consumer boundaries.

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

Return a compact receipt with the reviewed ranges, decision, material findings and
evidence, resolved prior findings, risks covered, checks run, and direct testing gaps.
For local-Markdown closure, write a dedicated receipt with the machine-readable
fields `Review range: <base>..<head>`, `Decision: <approved or rejected>`, `Checks`,
and `Findings and gaps`; the latter two may link to detail but must not be empty.
