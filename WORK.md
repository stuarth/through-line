# Work

Take one coherent unit per session: a determined round, one decision, one research
or prototype ticket, or one task when execution is in scope. Carry its consequences
through the map, then stop. A continuation or compaction does not start another unit.

If the unit no longer fits safely, leave a **Resumption checkpoint** with the durable
result, commits, remaining work, review findings, and verification state. Unclaim the
ticket, reconcile the tracker, and stop so a fresh session can resume from durable
state.

## Orient

1. Load the effort's `PRINCIPLES.md` (placed per
   [PRINCIPLES-FORMAT.md](./PRINCIPLES-FORMAT.md)), the
   map's Destination, Notes, Local policies, and decision rights, the frontier, and
   the Findings, premises, and provisional verdicts that reach the selected work.
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
change the answer, create or link research and block the decision on it.

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

For a builder-owned round, resolve recommendations that still fit the decision-rights
agreement and report the overview. Escalate the rest.

When principles pull incompatibly, residual judgment remains. Remove that ticket
from the round, check the principle boundaries, and bring the surviving trade-off to
the human.

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

Take a real counterexample through [Admission](./ADMISSION.md) as a proposed boundary,
split, priority, or refutation. The human decides the doctrine change; then propagate
it through every dependent ticket.

## Finish the session

Re-chart newly sharp questions, reconcile through [Record](./SKILL.md#record), report
the frontier, and stop. A fresh session takes the next unit.

When the destination is reached, close the map. Review local policies for lessons
that deserve admission as standing principles; leave the rest with the closed map.
