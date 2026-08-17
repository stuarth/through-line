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

- Repository: <path>; Code base: <full commit hash>; Integration head: <full commit hash>; Reviewed code head: <full commit hash or pending>; Closure state: <full commit hash or pending>; PR: <URL, none, or pending>; Review receipt: <durable reference or pending>
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

<!-- In-scope fog and sharp work consciously deferred from the confirmed route. -->

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
- **task** — one execution or manual outcome acceptable as a whole, authored with
  its acceptance criteria.

A ticket is one decision or one outcome acceptable as a whole. Split only for a
separate human verdict, an outcome releasable on its own across an [exposure
boundary](./EXECUTION.md#review-and-correction), or a distinct authority boundary.
Separately implementable steps are plan packets inside one ticket and compose
together. When work exposes a separate human judgment, create that decision ticket
and block the original work on it.

For a human-owned decision, keep only the residual judgment in **Question**. Put
settled consequences in **Derived implications** and small aligned choices in
**Builder discretion**.

Keep ticket bodies as current state, not transcripts. An unresolved ticket retains
its current question, live alternatives and premises, applicable acceptance
criteria, one **Provisional verdict**, derived implications, and direct pointers to
the current candidate and each authoritative review receipt when they exist. A
resolved ticket retains its accepted question or criteria, final **Resolution**, and
the evidence pointers needed for later closure review. Move only superseded analysis,
replaced verdicts and receipts, and chronological chatter to one linked history
artifact; leave one line pointing to it. History is context, not authority. The
active body must support the next action and a later audit without loading history.
Put a durable full contract in its ADR or domain documentation.

Ticket every sharp human question. Ticket builder choices only when they block the
map, test a principle, or deserve a durable record. Leave unshaped uncertainty in
**Not yet specified** and work beyond the destination in **Out of scope**.

When an accepted result proves wrong while the map is open, reopen its ticket. Move
the old **Resolution** to the ticket's linked history artifact, leave a one-line
pointer, increment `Reopened: <count>`, record the defect and current **Convergence
verdict**, and list the resolved dependents that consumed the old result.
Re-resolution gives every listed dependent one disposition: **stands** or
**reopens**. Integrated behavior with no single root becomes one new outcome ticket.
A closed map still reopens through a correction ticket against its immutable closure
state.

Claim a ticket before work. Respect another session's claim. Repository work also
records its repository and branch. Use native dependencies so the **frontier** is
the open, unblocked, unclaimed work. Link large artifacts instead of pasting them
into tickets.

## Record

Recording is done when the tracker agrees with reality:

- status, assignee, dependencies, and claims are current;
- each decision, research, or prototype resolution records its outcome and
  provenance; each repository task resolution records its candidate and integrated
  commits, plus its PR when one exists;
- checkpoints exist only on unfinished work;
- **Decisions so far**, **Findings**, and **Out of scope** index the right closures,
  each gist at most two lines;
- the digest carries what this session paid to discover and a sibling would
  otherwise pay again;
- principle evidence links to the decisions that set or tested it; and
- the available tracker validator passes.

For repository execution, close only after a fresh whole-effort review covers the
exact code range and the tracker records its PR, review receipt, and immutable closure
state. Later in-scope work reopens the same canonical map and adds a correction
ticket; the recorded closure commit remains its immutable historical boundary. For
local Markdown, follow its [closure
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

Use **receipt-only coordination** at every dispatch depth:

- give the agent one selected unit with its reaching premises, references, and
  completion checks;
- require one terminal receipt, with earlier communication only for a blocker or
  durable checkpoint that needs coordination;
- when that receipt is the next critical-path input, keep the coordinator active
  with the host's completion-aware wait at its maximum timeout; and
- treat an expired wait or unrelated mailbox wake as no state change: re-arm the
  wait without reloading durable state, inspecting the agent tree, or reporting
  unchanged progress. Reload durable state after the terminal receipt.

The tracker, map, principles, and linked artifacts—not conversation—carry state
between sessions. The Work session owns claims, human questions, propagation, and
tracker reconciliation. Give research and prototype agents only their selected
ticket, reaching premises, references, and checks. Delegate bulk reading to
disposable read-only scouts, each with a brief of named questions and the named
places to look; carry back conclusions and exact references, never file dumps.

Sessions in one effort walk the same ground. An **orientation digest** beside the
map is the bounded index of expensive discovery: code entry points already located,
environment facts, and links to topic reference notes when an entry needs depth.
Orient loads the index as earned priors to verify before relying on, then loads only
references that reach the selected work. Keep the index under 1,000 words and 120
lines. Retain only discoveries a sibling would otherwise repay; prune doctrine,
closures, and receipts carried elsewhere. Keep one reference note per topic rather
than multiplying context-specific digests.

Repository work follows [EXECUTION.md](./EXECUTION.md). Its plan, the receipts
recorded at handoffs and checkpoints, and each resolution's evidence let a fresh
session resume without reloading map history or conversation.
