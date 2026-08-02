---
name: through-line
description: Drive a huge effort by distilling recurring commitments into PRINCIPLES.md, propagating each human verdict through the remaining map, and surfacing only residual judgment under agreed decision rights.
disable-model-invocation: true
---

A huge effort hides a **through-line**: recurring commitments beneath its many
decisions. Name the destination, distill those commitments into human-adopted
principles, and use them to resolve what no longer needs fresh judgment. After each
new fact or verdict, propagate its consequences through the map before asking the
human another question.

Produce decisions, not deliverables, unless the map's **Notes** puts execution in
scope.

## Invocation

- Loose idea: follow [CHART.md](./CHART.md).
- Existing map: follow [WORK.md](./WORK.md).
- Existing map with **advance unattended**: follow [SUPERVISE.md](./SUPERVISE.md).

## Decision rights

Each map records a simple working agreement. The human owns destination, scope,
doctrine, domain meaning, priorities, external promises, and irreversible effects.
The builder owns reversible route and implementation choices that clearly follow
adopted principles and settled premises within the agreed reversal budget. The map
may reserve more choices for the human.

When alignment is unclear or a choice changes protected meaning, surface it rather
than stretching the agreement.

## Map and tickets

The map is one issue labelled `through-line:map`; its tickets are child issues. Read
the repo's issue-tracker guidance. If none exists, use
[local Markdown](./trackers/local-markdown.md).

Load the map once per session as the low-resolution view. Query open child tickets
for detail instead of copying them into it.

```markdown
## Destination

<one or two lines fixing scope>

## Notes

<!-- Domain, useful skills, execution scope, and decision-rights agreement. -->

## Local policies

<!-- Adopted route-scoped rules, in PRINCIPLES.md entry format. -->

## Decisions so far

<!-- One gist (two lines max) + link per closed in-scope decision ticket. -->

## Findings

<!-- One gist (two lines max) + link per closed research, prototype, or task ticket. -->

## Not yet specified

<!-- In-scope fog not yet sharp enough to ticket. -->

## Out of scope

<!-- Work consciously ruled beyond the destination. -->
```

Ticket types:

- **decision** — one human- or builder-owned choice;
- **research** — one material fact, resolved through `/research`;
- **prototype** — one cheap artifact to react to;
- **task** — one reviewable unit of execution or manual legwork.

A ticket is atomic when its answer or result can be accepted as a whole. Split an
independently decidable, landable, or verifiable part: a task whose acceptance
criteria contain several independently landable or verifiable results is several
tickets wired by dependencies. When work exposes a separate human judgment, create
that decision ticket and block the original work on it.

For a human-owned decision, keep only the residual judgment in **Question**. Put
settled consequences in **Derived implications** and small aligned choices in
**Builder discretion**.

An unresolved ticket may carry one **Provisional verdict**. **Resolution** is its
final premise; replaced premises move to **Verdict history**, which is context rather
than authority.

Ticket every sharp human question. Ticket builder choices only when they block the
map, test a principle, or deserve a durable record. Leave unshaped uncertainty in
**Not yet specified** and work beyond the destination in **Out of scope**.

Claim a ticket before work. Respect another session's claim. Repository work also
records its repository and branch. Use native dependencies so the **frontier** is
the open, unblocked, unclaimed work. Link large artifacts instead of pasting them
into tickets.

## Record

Recording is done when the tracker agrees with reality:

- status, assignee, dependencies, and claims are current;
- each resolution records its outcome, provenance, and repository commit or PR when
  applicable;
- checkpoints exist only on unfinished work;
- **Decisions so far**, **Findings**, and **Out of scope** index the right closures;
- principle evidence links to the decisions that set or tested it; and
- the available tracker validator passes.

For local Markdown, run the bundled
[state validator](./scripts/validate_local_map.py).

## Principles

`PRINCIPLES.md` is standing doctrine, not effort state. Follow
[PRINCIPLES-FORMAT.md](./PRINCIPLES-FORMAT.md).

- Nothing enters or changes doctrine without [Admission](./ADMISSION.md) and human
  adoption.
- A useful principle forbids a plausible choice.
- A principle is an earned prior, not a law; contradictory evidence goes through
  [Falsify](./WORK.md#falsify).

An ADR records one hard-to-reverse decision and its trade-off. A principle distills
several decisions. Cross-cite them.

## Coordination

The tracker, map, principles, and linked artifacts—not conversation—carry state
between sessions. The Work session owns claims, human questions, propagation, and
tracker reconciliation. Give research and prototype agents only their selected
ticket, reaching premises, references, and checks. Delegate bulk reading to
disposable read-only scouts, each with a bounded brief of named questions; carry
back conclusions and exact references, never file dumps.

Repository work follows [EXECUTION.md](./EXECUTION.md). Its plan, candidate,
review, and verification receipts let a fresh session resume without reloading map
history or conversation.
