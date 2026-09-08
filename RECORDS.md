# Keep a small, usable body of judgment

## Location and authority

Prefer the workspace's established policy, principles, and decision locations. Use
`principles/index.md` only as a default when an adopted commitment first needs a home.
Do not migrate existing documents or create empty scaffolding automatically. The
workspace owns its records; the installed skill contains only the practice.

A filesystem workspace might grow into:

```text
principles/index.md                 # applicability and discovery pointers
principles/recorded-events.md       # a bounded commitment and its reasoning
docs/decisions/event-corrections.md  # originating decision, in its existing home
```

An existing document service works too when the host can read and update it. Keep one
authoritative location for each commitment. Do not copy a shared principle into every
repository, startup file, or index. Respect source access and audience: a public
repository is not a suitable destination for private customer transcripts.

## The discovery index

Keep the entry index short enough to read routinely; aim for a screen or two, roughly
400 words. This is an attention budget, not a reason to omit an important constraint.
Use two sections: **Always consult**, for the few truly workspace-wide commitments,
and **By concern**, for pointers with applicability descriptions. Read the canonical
always-consult records during orientation; pointers alone do not convey their rules.

An entry should explain when it matters:

> Recorded events and corrections: consult when changing how observations are edited,
> imported, reconciled, displayed, summarized, or exported.

Link that description to the authoritative record. Index descriptions are discovery
hints, not a second statement of the commitment. Include cross-cutting applicability,
not just code paths. When the index becomes hard to scan, split it along established
domain concerns and keep the parent as a router. Do not invent a taxonomy in advance
or hide universal commitments behind an optional subtree.

## The record

Keep the operative commitment short. Put only decision-useful rationale and examples
beside it; link longer evidence. One focused record may contain closely related
commitments when they share a real scope. Use stable paths or the workspace's existing
identifiers rather than a new mandatory numbering system.

Suggested shape, not a migration requirement:

```markdown
# Preserve accepted observations
Status: adopted
Authority: <human decision, date, durable source or faithful decision note>

## Commitment
<the choice this requires or rules out>

## Why this choice
<the plausible alternative, tradeoff, and important premise>

## Applies when
<domain meanings and applicable cases>

## Boundary
<a contrasting case where the commitment does not decide the answer>

## Evidence
<originating decision, relevant examples, and checks; links where available>
```

For new records, use `proposed`, `adopted`, or `retired` status. Proposed records never
appear as active commitments; store them only when preserving the candidate itself
is useful or requested, with the unresolved adoption question visible. Do not build
a speculative candidate backlog. Working explanations and observations remain in
ordinary work notes, with evidence and uncertainty, outside the active canon.

Authority must reflect a real decision. When a chat has no durable URL, write a faithful
minimal decision note identifying the human, context, and actual verdict; say that
no durable transcript link is available. Never fabricate a link, quote, date, or
approval. In a proposed diff, distinguish the proposed record from completed adoption.

## Write with the work's permission

During an authorized workspace editing task, explicit adoption for future workspace
work includes recording the commitment in the visible diff. Update the record,
necessary decision evidence, and affected discovery pointers together. For
discussion-only or read-only work, present a proposed edit. Filesystem access alone
is not write authorization. Merely invoking this skill authorizes no persistence,
startup-file edits, commits, or external writes. Follow the existing workspace workflow
for review and publication; this skill adds no separate approval ceremony.

Re-read before editing and preserve concurrent changes. If another worker changed
meaning, reconcile it; do not overwrite their verdict or merge contradictory policy
by prose cleanup. Inspect the diff and links after the change. Do not claim the
record is durable until the write succeeds; distinguish local edits from publication.

## Revise and inspect consequences

Prefer amendment or consolidation to accumulating overlapping principles. Preserve
the previous version and its rationale in native history or a linked decision before
replacing it. Record local exceptions as bounded decisions. Retirement removes a
commitment from active discovery but preserves its historical source; low retrieval
frequency alone is not a reason to retire a rare, consequential constraint.

For an adopted change, inspect explicit references and likely semantic consumers in
the affected scope: implementation, tests, reports, guidance, and existing commitments.
Report confirmed changes, inspected consumers that still stand, and areas not checked.
Apply only authorized consequences. Link residual decisions or follow-on work in the
workspace's normal place; no new task graph or universal backlink ledger is required.
Do not imply every dependency was found or rewrite the rationale of historical choices.

Maintain the collection when real work reveals duplication, stale premises, missing
boundaries, or weak discovery pointers. Empty outcomes are normal: most tasks should
not add a record.
