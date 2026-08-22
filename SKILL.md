---
name: through-line
description: Drive a large, multi-session effort by preserving decision rights, propagating human verdicts, and advancing only the work those verdicts authorize.
disable-model-invocation: true
---

# Through-line

Use Through-line when work spans sessions and later work must inherit durable
decisions or outcomes. Use an ordinary plan when the work fits one session or needs
no durable propagation.

## Model

A **route** is the durable authority for one effort. Its **charter** fixes the
destination, decision rights, execution scope, and charter-level premises. Its
**units** are unresolved questions or acceptable outcomes connected by dependencies.
The **frontier** is derived: open, unblocked work that no other session owns.

An **adopted principle** is a recurring, human-approved commitment that can settle
later choices. A charter premise applies only to this route. Follow
[PRINCIPLES-GUIDE.md](./PRINCIPLES-GUIDE.md) when proposing or challenging a
principle.

Each **unit** is a durability boundary. A decision unit contains `## Question`; an
outcome unit contains `## Outcome`. Builder work has one current claimed unit; ready
human units may share a prompt but never state. A unit exists only when it blocks the
route, crosses an authority or consequential boundary, tests a principle, or changes
its observable result. Research, prototyping, manual work, implementation, and review
are methods inside a unit, not additional unit types. Helpers contribute evidence
without creating a second mutable work lane.

## Invariants

- The human owns the charter: destination, scope, doctrine, protected domain meaning,
  priorities, external promises, and irreversible effects. The builder owns clearly
  aligned, reversible route and implementation choices within the agreed budget.
- Only explicit human adoption creates or changes a principle. Every resolved unit
  records the verdict, principle, fact, or artifact that makes it stand.
- Durable route state, not conversation, is authoritative. Mark at most one builder
  unit `Claimed by` across the route. Persist its host-addressable worker or session
  identifier before work. Resume live ownership; recover or release stale ownership
  before selecting more work.
- After every fact, verdict, or result, update every unit it reaches before asking the
  human another question. Apply builder-owned consequences and surface only residual
  human judgment.
- For repository execution, maintain one named integration ref per repository. A
  review states whether an exact object supports an exact claim; it never grants
  permission to publish, spend, delete, deploy, or mutate shared state.
- A helper receives only the current unit, reaching evidence, useful references, and
  checks. Wait on its completion instead of polling. It returns one result at
  completion, or earlier only for a blocker or durable checkpoint.
- Writing route state through its configured tracker is standing authority. Every
  other shared, external, paid, destructive, or irreversible effect requires human
  authorization for the exact action, target, scope, and limits.

## Routing

- No route yet: follow [CHART.md](./CHART.md).
- Resolved route: treat it as immutable; start a new route that references it for
  later correction or follow-on work.
- Open route with **advance unattended**: follow [SUPERVISE.md](./SUPERVISE.md).
- Other open route: follow [ADVANCE.md](./ADVANCE.md).

Resolve the tracker through the repository's `### Issue tracker` guidance. Without a
configured tracker, use [local Markdown](./trackers/local-markdown.md). The tracker
adapter owns storage syntax; the model above owns meaning.
