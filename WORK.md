# Work

Run exactly one of the following per session: one round; one individual decision
ticket when nothing is determined; one research or prototype ticket; or, when
execution is in scope, one task ticket. Then propagate its verdicts and resolutions
to convergence. Exception reviews and builder resolutions raised by propagation
belong to that session's cascade; completed legwork may be harvested first.
Finishing one listed round or ticket and its cascade is a stop condition: an
automatic continuation or resumed turn is still the same session. When earlier
conversation history has been summarized or lost before that round or ticket
resolves, set one `## Resumption checkpoint` section on every claimed ticket with
durable work and its commits, work remaining, and current verification state,
sufficient for a fresh session to resume from the tracker alone. Unclaim, reconcile
through [Record](./SKILL.md#record), report the frontier, and stop.

## Orient

1. Load `PRINCIPLES.md`, the map, its **Findings**, decision rights, the tracker
   frontier, and only `State: active` entries from **Verdict history** in every
   unresolved decision.
2. Reconcile completed legwork and tracker state through [Record](./SKILL.md#record).
3. Classify every frontier decision by the reach of adopted principles, local
   policies, and recorded premises, and by ownership.

Reach:

- **Determines** — the recommendation follows with no material judgment.
- **Constrains** — the principle or premise rules answers out but leaves material
  judgment.
- **Does not reach** — it has no real bearing.

Treat a non-final premise as constraining only; never use it to determine or moot a
decision.

Ownership:

- **Human-owned** — reserved by the map's decision rights.
- **Builder-owned** — every decision-rights guardrail holds.

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
- **Principle or premise** — name it; mark local policies as local
- **Scenario**
- **Implications**
- **Residual judgment** — `none`; otherwise remove it from the round
- **Recommendation**

For a human-owned round, first present every ticket name and one-line recommendation
side by side. Surface incoherence or conflicting pull in that overview, then ask for
one **exception review** of the listed recommendations. Resolve the round only from
an explicit verdict on that overview. Silence, an automatic continuation, a generic
"continue" or "next ticket", and earlier approval of a plan or graph carry no verdict.
Confirmation resolves only those recommendations as presented; a challenged ticket
leaves the round and follows Rejection. Keep full derivations in the tickets, and
expand one in conversation when the human asks or must understand an incoherence.

A new principle's validation pass presents its full derivations. Its exception review
still covers at most three tickets.

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
material amendment to a final premise follows Propagate's replacement-premise sweep.
When the amended answer was builder-owned, its replacement becomes human-owned.

## Propagate

After every human verdict or resolved individual decision, after every resolved
research, prototype, or task ticket, and after each round's resolutions, propagate the
new premise or Finding through every remaining unresolved decision ticket before
presenting another human question:

1. Record the session's smallest durable result:
   - A research, prototype, or task ticket goes in **Resolution** and its **Findings**
     gist.
   - When replacing a final premise, first move the old **Resolution** under
     **Verdict history** as `State: superseded`.
   - A non-final premise goes under **Verdict history** as `State: active`; first
     mark any earlier active entry `State: superseded`. When it replaces a final
     premise, clear the stale map entry, then reopen the deciding ticket through the
     claim protocol below.
   - A final premise goes in **Resolution** and its **Decisions so far** gist.
   When the verdict changes doctrine, its adopted principle or local-policy entry is
   the durable premise. A decision may become a downstream premise without becoming
   doctrine; take recurring rhyme through [Admission](./ADMISSION.md) before
   proposing a principle or local policy.
2. Whenever an earlier recorded premise becomes `State: superseded`, run the
   **replacement-premise sweep**. Trace every decision that names the old premise in
   its derivation,
   **Derived implications**, **Resolution**, or map gist, including transitively
   through decisions that became downstream premises. Through the claim protocol
   below, re-check whether an adopted principle, local policy, surviving active
   premise, or surviving recorded final premise still supports each implication or
   ruled-out choice. Restore to each dependent's **Question** every choice ruled out
   only by the old premise, and clear each implication derived from it,
   re-attributing any that still holds. Include every dependent in reclassification.
   For each closed dependent, also move its **Resolution** under **Verdict history**
   as `State: superseded`, clear that **Resolution**, remove its stale map entry, and
   clear its retained assignee before reopening it.
3. Reclassify reach and ownership using the new premise:
   - resolve determined builder-owned decisions inside their guardrails, naming the
     determining principle, local policy, or recorded final premise in
     **Resolution**;
   - collect determined human-owned decisions for the cascade's next Round;
   - rewrite a constrained ticket's **Question** to name only its residual
     judgment, and move the ruled-out choices into **Derived implications** with
     the determining principle or premise;
   - close moot decisions under **Decisions so far**, using the mooting premise as
     the gist, and close scope departures under **Out of scope**; and
   - audit a contradicted principle through [Falsify](#falsify).
4. Apply ticket mutations through the [claim protocol](./SKILL.md#map-and-tickets).
   When a ticket claimed by another session would change, leave it read-only, surface
   the ownership conflict, and coordinate with its assignee before either session
   resolves it. Unclaim every unresolved ticket initially claimed for this session
   unless the cascade is explicitly continuing it. Unclaim every still-open ticket
   claimed for propagation unless this session is retaining it for the cascade's next
   Round. Keep a ticket blocked whenever a missing fact could change the
   recommendation.
5. Record every changed ticket, dependency, map index, and principle evidence trail,
   then report the propagation delta:
   - **Reopened**
   - **Resolved**
   - **Narrowed**
   - **Still needs human judgment**

Propagation is complete when every unresolved decision has been checked, tracker state
records every resulting change, and the next human question—if any—states one
residual judgment.

## Individual judgment

When nothing is determined, first look for rhyme: a frontier cluster or recent judged
decisions leaning together. Name that candidate, then read
[ADMISSION.md](./ADMISSION.md) and take it through the gate before another round.

Without such a cluster, decide one ticket. Before asking a human-owned question,
write its one-sentence residual judgment and move its derived implications and
builder discretion out of the Question. Present the recommendation and only the
evidence or trade-off that can change the verdict; use examples when the distinction
remains ambiguous. If no residual judgment remains, reclassify the ticket as
determined and collect it for the cascade's next Round. Use `/grilling` and
`/domain-modeling` for genuine human judgment; for builder-owned choices compare
credible alternatives and resolve only while every guardrail holds. Individual
judgment funds derivation; do not stretch a principle to avoid it.

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
3. Report the frontier and stop. A fresh session resumes from the tracker and takes
   the next round or ticket.

When the destination is reached, close the map with a local-policy sweep: record each
policy's determined derivations, scenario spread, and pre-effort evidence; look for
the higher-altitude candidate the group implies; propose any graduation through
[ADMISSION.md](./ADMISSION.md). The rest remain minable on the closed map.
