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

Produce decisions, not deliverables, unless the map sets `Repository execution:
in-scope`.

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

The map is one issue labelled `through-line:map`; its tickets are child issues.
Resolve the tracker through the `### Issue tracker` block in the repo's
`CLAUDE.md`/`AGENTS.md` and follow its "Wayfinding operations" section. Without that
pointer, use [local Markdown](./trackers/local-markdown.md).

Load the map once per session as the low-resolution view. Query open child tickets
for detail instead of copying them into it.

```markdown
Label: through-line:map
Status: open
Repository execution: out-of-scope

## Destination

<one or two lines fixing scope>

<!-- With `Repository execution: in-scope`, add:
Tracker state: pending

## Execution heads

- Repository: <path>; Code base: <full commit hash>; Reviewed code head: <full commit hash or pending>; Closure state: <full commit hash or pending>; PR: <URL, none, or pending>; Review receipt: <durable reference or pending>
-->

## Notes

<!-- Domain, useful skills, and decision-rights agreement. -->

## Local policies

<!-- Adopted route-scoped rules, in PRINCIPLES.md entry format. -->

## Decisions so far

<!-- One gist + link per closed in-scope decision ticket. -->

## Findings

<!-- One gist + link per closed research, prototype, or task ticket. -->

## Not yet specified

<!-- In-scope fog not yet sharp enough to ticket. -->

## Out of scope

<!-- Work consciously ruled beyond the destination. -->
```

Ticket types:

- **decision** — one human- or builder-owned choice;
- **research** — one material fact, resolved in parallel by a `/research` subagent
  dispatched when the ticket is created; findings live on a throwaway
  `research/<name>` branch the resolution points to;
- **prototype** — one cheap artifact to react to, built with `/prototype` and kept
  as runnable evidence on a throwaway `prototype/<name>` branch the resolution
  points to;
- **task** — one reviewable unit of execution or manual legwork, authored with its
  acceptance criteria.

A ticket is atomic when its answer or result can be accepted as a whole. Split an
independently decidable, landable, or verifiable part: a task whose acceptance
criteria name several results, each acceptable as a whole on its own, is several
tickets wired by dependencies. When work exposes a separate human judgment, create
that decision ticket and block the original work on it.

For a human-owned decision, keep only the residual judgment in **Question**. Put
settled consequences in **Derived implications** and small aligned choices in
**Builder discretion**.

Keep tickets as state, not transcripts. A decision ticket carries its question,
decisive evidence, alternatives, verdict, and implications; move a durable full
contract to its ADR or domain documentation. A resolved task keeps one final receipt,
not a chronological copy of candidate, review, and test chatter.

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
- each decision, research, or prototype resolution records its outcome and
  provenance; each task resolution records its outcome and repository commit or PR;
- checkpoints exist only on unfinished work;
- **Decisions so far**, **Findings**, and **Out of scope** index the right closures,
  each gist at most two lines;
- the digest carries what this session paid to discover and a sibling would
  otherwise pay again;
- principle evidence links to the decisions that set or tested it; and
- the available tracker validator passes.

For repository execution, close only after a fresh whole-effort review covers the
exact code range and the tracker records its PR, review receipt, and immutable closure
state. A later in-scope correction reopens the affected ticket or creates a correction
ticket. For local Markdown, follow its [closure
protocol](./trackers/local-markdown.md#local-markdown-wayfinding-operations), then run
the bundled [state validator](./scripts/validate_local_map.py). Validator success
establishes tracker structure only; it is not implementation or decision evidence.

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
disposable read-only scouts, each with a brief of named questions and the named
places to look; carry back conclusions and exact references, never file dumps.

Sessions in one effort walk the same ground. An **orientation digest** beside the
map caches expensive discovery for siblings: code entry points already located and
environment facts. Orient loads it as earned priors to verify before relying on.
Keep it under 1,000 words and 120 lines. Retain only discoveries a sibling would
otherwise repay; prune doctrine, closures, and receipts carried elsewhere.

Repository work follows [EXECUTION.md](./EXECUTION.md). Its plan, the receipts
recorded at handoffs and checkpoints, and each resolution's evidence let a fresh
session resume without reloading map history or conversation.
