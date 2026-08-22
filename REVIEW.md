# Review

Review one immutable **object** against one explicit **claim** as a fresh, read-only
leaf. Fix bytes and configuration with full hashes, immutable versions, or digests.
The claim states the relied-on outcome; `checks passed` and `artifacts exist` are
proxies. A receipt stands only while object and claim are unchanged.

Judge evidence relative to the claim and present consequences. Trace relevant authority,
persistence, concurrency, and consumer boundaries; seek a counterexample that would
falsify a semantic claim. Reproduction alone does not prove meaning. Do not require
later-boundary guarantees.

For an integrated-range review, inspect the full range at the named integration
`Ref`, including current consumers. Verify Base matches its first committed route
value. Identify the object by base, exact head, and necessary configuration, not
isolated leaf commits.

For a consequential effect, review the exact state and configuration that would
execute, including limits, stops, recovery, and executable launch preconditions. The
verdict does not authorize the effect.

For run evidence, verify provenance, terminal accounting, safety assertions, and an
independently checkable basis. Honest failure evidence can support a failure claim.

For closure, review the exact proposed map and unit bytes plus every recorded
Base-to-Ref range. Identify the route state by the tracker's deterministic digest.
An earlier receipt applies only when its exact object, configuration, and closure
claim are unchanged. Verify each Ref resolves to its reviewed hash and each repository
worktree is clean, then follow the tracker's closure-receipt format.

Report only evidenced, material failures of the claim in required behavior,
correctness, security, or data integrity. Exclude optional hardening and adjacent
cleanup.

Return one compact receipt:

- `Object`: exact identity, including configuration when relevant;
- `Claim`: the assertion reviewed;
- `Claim supported`: `yes` or `no`;
- `Checks`: evidence examined or run, with exact object identities; and
- `Findings`: material findings, or `none`.

For a correction under the same claim, cite the prior receipt and judge the changed
range against its findings. A changed claim needs whole-object review.
