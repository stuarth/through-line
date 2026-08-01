# Review

Review one fixed candidate as a read-only leaf. Do not coordinate or implement.

For an initial review, use the ticket, premises, candidate receipt, and fixed range.
For a correction, use the prior review receipt and correction range; revisit its
findings and touched files while preserving unaffected coverage.

Report only material findings: acceptance failures or evidenced correctness,
security, or data-integrity failures. Leave optional hardening, adjacent cleanup, and
broader completeness ideas outside this ticket. Run only the checks named for review.

If one named risk needs expertise you do not have, return that risk for one specialist
instead of delegating the review.

Return a compact receipt with the reviewed ranges, decision, material findings and
evidence, resolved prior findings, risks covered, checks run, and direct testing gaps.
