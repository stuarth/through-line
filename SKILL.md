---
name: through-line
description: Drive a huge effort by distilling recurring commitments into PRINCIPLES.md, propagating each human verdict through the remaining map, and surfacing only residual judgment under agreed decision rights.
disable-model-invocation: true
---

A huge effort hides a **through-line**: recurring commitments beneath its many
decisions. Name the **destination**, distill those commitments into human-adopted,
falsifiable principles, then let **derivation** resolve the decisions they determine
under agreed **decision rights**. Individual judgment handles the genuinely novel
questions and funds the next distillation. After every human verdict and decision
round, propagate their consequences through the remaining map before asking another
question.

Produce decisions, not deliverables, unless the map's **Notes** puts execution in
scope.

## Invocation

- Invoked with a loose idea: read [CHART.md](./CHART.md) and follow it.
- Invoked with an existing map: read [WORK.md](./WORK.md) and follow it.

## Decision rights

Each map records one working agreement classifying decisions as:

- **Human-owned** — put every decision to the human; use legwork to establish facts.
- **Builder-owned within guardrails** — resolve without stopping only while the
  choice is clearly preferable under established facts and at least one adopted
  principle, local policy, or recorded final premise; is reversible within the map's
  concrete budget; is contained to its scope; and creates no new external interface,
  domain commitment, or irreversible data effect.

The human always owns the decision rights themselves; destination and scope;
adoption, revision, boundary, priority, or refutation of a principle or local policy;
and a new principle's validation pass.

Re-check every builder-owned resolution against every guardrail at the moment of
resolution. A failed guardrail makes it human-owned.

## Map and tickets

The map is one issue labelled `through-line:map`; its tickets are child issues. Read
the repo's issue-tracker doc and follow its **Wayfinding operations**. If none was
provided, read [trackers/local-markdown.md](./trackers/local-markdown.md) before
creating or claiming anything.

Refer to maps, tickets, and principles by name in prose. The map is the effort's
low-resolution view, loaded once per session; query open child tickets rather than
listing them on the map.

```markdown
## Destination

<one or two lines fixing scope>

## Notes

<!-- Description only: domain, skills, execution scope, and the adopted
decision-rights agreement. A rule that determines ticket answers is a local policy
and enters through Admission. -->

## Local policies

<!-- Adopted route-scoped rules, in PRINCIPLES.md entry format. -->

## Decisions so far

<!-- Exactly one gist + link per closed in-scope decision ticket. -->

## Findings

<!-- Exactly one gist + link per closed in-scope research, prototype, or task ticket. -->

## Not yet specified

<!-- In-scope fog not yet sharp enough to ticket. -->

## Out of scope

<!-- Closed tickets and work consciously ruled beyond the destination. -->
```

Each ticket contains one question and carries `through-line:<type>`:

- **decision** — a choice, human- or builder-owned;
- **research** — a material fact to establish, resolved through `/research`;
- **prototype** — a cheap artifact to react to; build AFK, react HITL;
- **task** — manual legwork such as provisioning or a data move.

A human-owned decision ticket is atomic when its **Question** asks for one verdict
the human must confirm or reject as a whole. A builder-owned decision ticket is
atomic when it names one choice the builder can resolve as a whole inside the
guardrails. Split either ticket when a partial resolution is possible.

For a human-owned ticket, put only its residual judgment in **Question**. Put
principle-derived consequences in **Derived implications** and below-threshold
choices in **Builder discretion**; the human verdict covers only the Question.

Record a non-final verdict or superseded resolution under **Verdict history**. Mark
each entry `State: active|finalized|superseded`. Before any ticket resolves or
closes, mark each active entry `State: finalized` when its **Resolution** carries it
forward and `State: superseded` otherwise. Only an active entry may constrain
another decision.

Ticket every sharp human-owned question. Ticket a builder-owned choice only when it
blocks another mapped decision, tests a principle, or needs a durable record;
ordinary below-threshold choices remain builder discretion.

Sharp enough to state means **ticket**, even when blocked. Otherwise it remains fog;
do not pre-slice fog. Work beyond the destination goes to **Out of scope**. Close a
mis-scoped ticket with its gist and reason there, never in the route indexes.

Claim a ticket by assigning it before any work. Use the tracker's native dependencies
so the **frontier** is the open, unblocked, unclaimed set. Link assets from tickets
rather than pasting them into the body.

## Record

Recording is done when the tracker agrees with reality:

- every claimed or resolved ticket has an assignee, and open or blocked tickets do
  not;
- every resolved ticket is closed with its resolution;
- **Decisions so far** indexes exactly the closed in-scope decision tickets;
- **Findings** indexes exactly the closed in-scope research, prototype, and task
  tickets;
- **Out of scope** holds every scoped-out closure and none of the route indexes do;
- no open ticket appears in a closed-ticket index, and blocker/status state renders
  the real frontier.

Record principle boundaries and revisions inline in `PRINCIPLES.md`; add tickets that
set or tested a boundary to the evidence trail. For local Markdown, run the bundled
[state validator](./scripts/validate_local_map.py) to compare blockers, indexes, and
child status; otherwise run the tracker validator when provided. The checklist always
applies, and recording is not done until every available validator passes.

## Principles

`PRINCIPLES.md` is standing doctrine, not effort state. Entry format and file
placement follow [PRINCIPLES-FORMAT.md](./PRINCIPLES-FORMAT.md).

- **Adopted only.** Nothing enters or changes `PRINCIPLES.md` or **Local policies**
  except through [ADMISSION.md](./ADMISSION.md) and the human's explicit adoption.
- **Falsifiable only.** A principle must forbid a plausible decision; otherwise
  sharpen it or leave it out.
- **Priors, not laws.** An adopted principle is a strong prior earned by its
  evidence, not an inviolable rule: derive under it by default, and take evidence
  strong enough to contradict it through [Falsify](./WORK.md#falsify).

An ADR records one hard-to-reverse decision and its trade-off; a principle distills
several decisions. Cross-cite them.

Expect concurrent sessions. The tracker, map, and principles—not the conversation—are
the shared state.
