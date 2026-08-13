# Work

Take one coherent unit per session: a determined round, one decision, one prototype
ticket, or one task when execution is in scope. Research is the exception: a
dispatched `/research` subagent resolves it in parallel without consuming the unit.
Carry the unit's consequences through the map, then stop. Its resolution or
checkpoint is a **terminal receipt**: later messages may clarify it or resume the same
unfinished claim, but the next frontier always gets a fresh Work session. A
continuation or compaction does not widen the unit.

If the unit no longer fits safely, leave a **Resumption checkpoint** with the durable
result, commits, remaining work, review findings, and verification state. Unclaim the
ticket, reconcile the tracker, and stop so a fresh session can resume from durable
state.

## Orient

1. Load the effort's `PRINCIPLES.md` (placed per
   [PRINCIPLES-FORMAT.md](./PRINCIPLES-FORMAT.md)), the
   map's Destination, Notes, Local policies, and decision rights, the orientation
   digest when present, only its reference notes that reach the selected work, the
   frontier, and the Findings, premises, and provisional verdicts that reach the
   selected work.
   The map's closure indexes serve Propagate.
2. Reconcile completed work through [Record](./SKILL.md#record).
3. Classify frontier decisions by reach and ownership.

Reach:

- **Determines** — the recommendation follows without material judgment.
- **Constrains** — some choices are ruled out, but judgment remains.
- **Does not reach** — the premise has no meaningful bearing.

A provisional verdict constrains but does not determine. Ownership follows the
map's decision-rights agreement.

A decision needs enough facts to support its recommendation. If a missing fact could
change the answer, create or link a research ticket, block the decision on it, and
dispatch its `/research` subagent.

## Round

A round contains determined decisions of one ownership class. Prefer about five
different scenarios; a new principle's first validation round holds at most three.
Claim only that round.

Record each derivation with:

- decision right;
- principle or premise;
- scenario;
- implications;
- residual judgment; and
- recommendation.

For a human-owned round, show the ticket names and recommendations together and ask
for one exception review. Only explicit approval of those recommendations is a
verdict. Keep the full derivations in their tickets and expand them when useful.

The ticket is the audit trail; the prompt is the decision interface. A human who has
not opened the ticket must be able to decide from the prompt. For each residual
judgment, use ordinary domain language to give the choice, recommendation, one
separating example, the recommendation's main downside, and the fact or exception
that would change it. Link the ticket as optional depth.

Before asking, privately test the options against reaching premises and consider a
narrower scope, staged adoption, a suggestion-versus-authority hybrid, and doing
nothing. Classify each clause as determined or residual, then surface only residual
clauses and the minimum rationale needed to decide. Present independently rejectable
residual clauses as separate recommendations, even when they share one ticket.

Batch adjacent human decisions that share one mental model when later alternatives
can be stated contingently without new evidence. Keep them separate when an earlier
verdict changes the later evidence or option set.

For a builder-owned round, resolve recommendations that still fit the decision-rights
agreement and report the overview. Escalate the rest.

When principles pull incompatibly, residual judgment remains. Remove that ticket
from the round, check the principle boundaries, and bring the surviving trade-off to
the human.

If the human asks for plain language or an example, repair the affected capsule before
accepting its verdict and apply that correction to later prompts. Re-present the full
capsule only when the clarification exposes material ambiguity; answer a narrow
clarification narrowly.

## Rejection

A rejected recommendation means some link in its derivation is wrong: the premise,
boundary, inference, ownership, or principle. Correct or reclassify that link and
present the recommendation again. Do not stretch doctrine to preserve a round.

## Propagate

After every new fact, verdict, or resolution, update every decision it reaches before
asking the human another question.

1. Record the new result in its ticket and map index. Keep non-final premises in
   **Provisional verdict** and final ones in **Resolution**; move replaced premises
   to **Verdict history**.
2. When a premise changes, trace its dependents. Remove conclusions it no longer
   supports and reopen closures whose rationale no longer holds.
3. Reclassify the affected map: resolve determined builder-owned work, collect
   determined human-owned decisions for the next round, narrow constrained questions,
   close moot or out-of-scope work, and audit contradicted principles.
4. Respect active claims. Coordinate instead of rewriting work owned by another
   session.
5. Reconcile the tracker and report what reopened, resolved, narrowed, and still
   needs human judgment.

Propagation is complete when the tracker reflects the new premise and the next human
question, if any, contains only residual judgment.

## Individual judgment

When nothing is determined, first look for rhyme among frontier decisions. A recurring
commitment may deserve [Admission](./ADMISSION.md) before more one-off judgment.

Otherwise take one ticket. Present its residual judgment, recommendation, and only
the evidence or trade-off that could change the verdict. Use `/grilling` and
`/domain-modeling` for genuine human judgment. Resolve builder-owned choices only
while they remain clearly inside the decision-rights agreement.

## Task

For repository work, follow [EXECUTION.md](./EXECUTION.md). Return here after it
records a resolution or checkpoint.

## Falsify

Principles are strong priors, not laws. When code, decisions, or new evidence
contradicts one—or recurring exceptions show it has stopped predicting useful
answers—pause derivation and audit it.

Each correction ticket records `Correction of: <root ticket>; Concern: <stable
invariant>`; later corrections for that invariant keep the same root and concern.
Before charting its third material correction, pause execution and audit the chain as
one builder-owned architecture or principle-candidate ticket: test whether the rule,
representation, authority boundary, or review frame is wrong. Resume only after the
audit propagates. Any doctrine change still requires human Admission.

Take a real counterexample through [Admission](./ADMISSION.md) as a proposed boundary,
split, priority, or refutation. The human decides the doctrine change; then propagate
it through every dependent ticket.

## Finish the session

Re-chart newly sharp questions, reconcile through [Record](./SKILL.md#record), report
the frontier, and stop. A fresh session takes the next unit.

New work required by the unchanged destination is discovery, not a scope amendment:
record its added units and risk, then chart it under the existing decision rights.
Ask the human to amend scope only when the proposed work changes the destination,
protected meaning, external promise, or reversal budget. Otherwise keep a genuine
follow-up out of scope and close with a truthful bounded exception.

When the destination is reached, close the map. Review local policies for lessons
that deserve admission as standing principles; leave the rest with the closed map.
For repository execution, the claimable **Final map closure** task completes
[Review](./REVIEW.md), verifies every recorded execution repository is still at its
reviewed clean head, then follows [Record](./SKILL.md#record)'s closure gate. A
rejected review blocks that task on its correction tickets instead of closing the
map.
