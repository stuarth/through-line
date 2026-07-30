# Work

Run at most one decision round per session. Completed legwork may be harvested first.

## Orient

1. Load `PRINCIPLES.md`, the map, its **Findings**, decision rights, and the tracker
   frontier.
2. Reconcile completed legwork and tracker state through [Record](./SKILL.md#record).
3. Classify every frontier decision by principle reach and ownership.

Principle reach:

- **Determines** — the recommendation follows with no material judgment.
- **Constrains** — the principle rules answers out but leaves material judgment.
- **Does not reach** — it has no real bearing.

Ownership:

- **Human-owned** — reserved by the map's decision rights.
- **Builder-owned** — every delegation guardrail holds.

A decision is resolvable only when every material factual premise appears in
**Findings** or is stated as an explicit assumption in its Scenario. This includes
decisions committing to an output or delivery. If an unresolved fact could change the
recommendation, create or link its research ticket, wire it as a blocker, and leave
the decision off the frontier.

## Round

A round contains only **determined** tickets of one ownership class. Compatibility is
not derivation. Prefer about five materially different scenarios; a new principle's
validation pass comes first and holds at most three. Claim only the round's tickets.

Write each derivation as:

- **Decision right**
- **Principle** — name it; mark local policies as local
- **Scenario**
- **Implications**
- **Residual judgment** — `none`; otherwise remove it from the round
- **Recommendation**

For a human-owned round, first present every ticket name and one-line recommendation
side by side. Surface incoherence or conflicting pull in that overview. Then present
one full derivation per turn and wait for its verdict; there is no round-level
confirmation.

For a builder-owned round, complete every derivation, re-check decision-rights
guardrails, resolve the items that still qualify, and report their overview. Leave
escalated items open.

When adopted principles determine one ticket incompatibly, residual judgment exists:
remove it from the round, audit both boundaries, and put any surviving trade-off to
the human.

## Rejection

A material amendment rejects the presented derivation. Diagnose the broken link
before proceeding:

- wrong principle → re-derive under the right one;
- outside its boundary → propose the boundary through Admission;
- bad derivation → correct and re-present;
- constrained, not determined → unclaim it, then use individual judgment;
- principle itself wrong → falsify it.

A wording clarification that preserves the recommendation is confirmation. A later
material amendment to a builder-owned answer reopens the ticket and makes its
replacement human-owned.

## Individual judgment

When nothing is determined, first look for rhyme: a frontier cluster or recent judged
decisions leaning together. Name that candidate, then read
[ADMISSION.md](./ADMISSION.md) and take it through the gate before another round.

Without such a cluster, decide one ticket. For human-owned choices use `/grilling`
and `/domain-modeling`; for builder-owned choices compare credible alternatives and
resolve only while every guardrail holds. Individual judgment funds derivation; do
not stretch a principle to avoid it.

## Falsify

A principle is a strong prior, not a law: the deference it earns from its evidence
yields to stronger contradicting evidence. Watch every application for contradicting
code, past decisions, or new resolutions; evidence strong enough to contradict the
statement outright warrants an immediate audit, before any further derivation. Audit
also on request, and whenever slower signs accumulate: two derivations rejected or
materially amended, recurring exceptions, a shifted destination, boundary text
outgrowing the statement, or cited resolutions that keep needing material residual
judgment.

A surviving counterexample yields a human-adopted boundary, split, or refutation
through [ADMISSION.md](./ADMISSION.md). Trace the evidence trail to every derived
ticket and present a review round; the human chooses what to revisit.

## Finish the session

1. Record resolved tickets and principle changes through
   [Record](./SKILL.md#record).
2. Re-chart: create then wire newly sharp tickets, graduate fog, and close mis-scoped
   tickets into **Out of scope**; then take the re-charted tracker through
   [Record](./SKILL.md#record) again.

When the destination is reached, close the map with a local-policy sweep: record each
policy's determined derivations, scenario spread, and pre-effort evidence; look for
the higher-altitude candidate the group implies; propose any graduation through
[ADMISSION.md](./ADMISSION.md). The rest remain minable on the closed map.
