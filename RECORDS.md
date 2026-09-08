# Keep a small, usable body of judgment

## Location and authority

Prefer the workspace's established policy, principles, and decision locations. Use
`principles/index.md` only as a default when an adopted commitment first needs a home.
Create records as decisions need them, keeping existing documents in their established
locations.

A filesystem workspace might grow into:

```text
principles/index.md                 # applicability and discovery pointers
principles/recorded-events.md       # a bounded commitment and its reasoning
docs/decisions/event-corrections.md  # originating decision, in its existing home
```

An existing document service works too when the host can read and update it. Keep one
authoritative location for each commitment and link to it from other locations. Keep
source evidence within its intended audience.

## The discovery index

Keep the entry index short enough to read routinely; aim for a screen or two, roughly
400 words, with room for all workspace-wide commitments.
Use two sections: **Always consult**, for the few truly workspace-wide commitments,
and **By concern**, for pointers with applicability descriptions. Read the canonical
always-consult records during orientation; pointers alone do not convey their rules.

An entry should explain when it matters:

> Recorded events and corrections: consult when changing how observations are edited,
> imported, reconciled, displayed, summarized, or exported.

Link that description to the authoritative record. Index descriptions are discovery
hints, not a second statement of the commitment. Include cross-cutting applicability,
not just code paths. When the index becomes hard to scan, split it along established
domain concerns. Keep workspace-wide commitments accessible from the entry index.

## The record

Keep the operative commitment short. Put only decision-useful rationale and examples
beside it; link longer evidence. One focused record may contain closely related
commitments when they share a real scope. Use stable paths or the workspace's existing
identifiers rather than a new mandatory numbering system.

For a new record:

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

For new records, use `proposed`, `adopted`, or `retired` status. Only adopted principles
act as standing commitments. Preserve a proposal when the candidate has future value
or the user requests it, and include the open adoption question. Keep working
explanations and observations in ordinary work notes with their evidence.

Identify the human decision that establishes authority. Link to it when a durable
source exists; otherwise write a brief decision note with the person, context, and
verdict. Keep proposed wording distinct from an adopted commitment.

## Update records

During an authorized workspace editing task, explicit adoption for future workspace
work includes recording the commitment in the visible diff. Update the record,
necessary decision evidence, and affected discovery pointers together. For
discussion-only or read-only work, present a proposed edit. Follow the workspace's
existing authorization, review, and publication workflow.

Re-read before editing and preserve concurrent changes. Resolve conflicting decisions
with the people responsible. After writing, inspect the diff and links, and report
whether the record is saved locally or published.

## Revise and inspect consequences

Prefer amendment or consolidation to accumulating overlapping principles. Preserve
the previous version and its rationale in native history or a linked decision before
replacing it. Record local exceptions as bounded decisions. Retirement removes a
commitment from active discovery but preserves its historical source; low retrieval
frequency alone is not a reason to retire a rare, consequential constraint.

For an adopted change, inspect explicit references and likely semantic consumers in
the affected scope: implementation, tests, reports, guidance, and existing commitments.
Report confirmed changes, inspected consumers that still stand, and areas not checked.
Apply authorized consequences and link remaining decisions or work in the workspace's
normal place. Preserve the rationale of historical choices.

Maintain the collection when real work reveals duplication, stale premises, missing
boundaries, or weak discovery pointers. Write a record only when the work changes
judgment worth preserving.
