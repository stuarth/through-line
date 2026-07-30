Quickstart:

```bash
npx skills add mattpocock/skills --skill=through-line
```

```bash
npx skills update through-line
```

[Source](https://github.com/mattpocock/skills/tree/main/skills/engineering/through-line)

## What it does

`through-line` takes a huge effort full of apparently separate decisions, finds the recurring commitments beneath them, and turns those commitments into standing principles in `PRINCIPLES.md`. It then propagates every human verdict through the remaining map under decision rights you agree once for the effort, so each answer resolves or narrows as many later questions as it can.

Principles are adopted only by the human and must be falsifiable: the agent can propose, challenge, and derive from them, but it cannot quietly add doctrine or stretch a principle to cover a convenient answer. An adopted principle is a strong prior, not an inviolable law — derivation defers to it by default, and evidence strong enough to contradict it triggers a re-examination rather than a forced derivation.

The map keeps resolved **Findings** separate from decisions, so a decision can proceed
only when its material facts are already established or made explicit as assumptions.
Each ticket holds one independently confirmable choice.

## When to reach for it

You invoke this by typing `/through-line` — the agent won't reach for it on its own.

Reach for it when an effort is too large for one session and many of its decisions seem to rhyme — you want to discover the commitments they share, reuse those commitments across the effort, and leave durable guidance behind. If the route is foggy but recurring principles are not the point, use [wayfinder](https://aihero.dev/skills-wayfinder), which clears a map one decision at a time. For an idea small enough to sharpen in one conversation, use [grill-with-docs](https://aihero.dev/skills-grill-with-docs).

## Prerequisites

The effort's map and child tickets live on the repo's issue tracker, so `through-line` needs the tracker wiring that [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills) provides. If no tracker is configured, it falls back to a bundled local-markdown tracker and validator. It creates `PRINCIPLES.md` lazily when the first standing principle is adopted.

## Decision rights

Decision rights let you choose where the builder can keep moving and where it must stop for you. You can retain every substantive decision, or delegate obvious, cheaply reversible choices within agreed guardrails. Ordinary delegated choices stay below the ticket threshold; ambiguity, meaningful commitment, or a broken guardrail brings a decision back to you.

The direction of the effort is never delegated. You own the destination and scope, adopt every principle and local policy, and validate each new principle before it can guide builder-owned decisions. Through-line delegates routine judgment, not doctrine.

## Adoption is slow; propagation is fast

A principle has leverage because one statement can decide many cases, which also makes a bad principle unusually expensive. Admission is deliberately slow: each candidate must recur across independent decisions, be atomic, be interpretable by an uninvolved reader familiar with the domain, survive a counterexample, and promise leverage beyond the current destination. The principle itself carries its full meaning in plain domain language; its evidence and example support that meaning.

Once adopted, propagation is fast. After each verdict, the agent checks every remaining decision: determined choices resolve, constrained questions shrink to their residual judgment, and moot choices close. Human-owned consequences that already follow receive one exception review; builder-owned consequences resolve inside the agreed guardrails. The next individual question contains only the product or domain judgment the existing answers could not settle.

## Standing principles, local policies

The altitude test keeps `PRINCIPLES.md` from turning into a rule dump: if violating a commitment would make the system wrong about its domain, it may be a standing principle; if it would only make this effort inconsistent, it belongs on the map as a local policy. Local policies get the same derivation power for the current route but die with the map unless later, independent evidence earns promotion.

When a principle stops predicting good answers, the skill treats that as evidence rather than friction. Repeated rejected derivations, or a single application that meets strong enough contradicting evidence, trigger a boundary, split, or refutation, followed by a review of decisions previously derived from it. Re-examination is still adoption: the human confirms any change to the principle.

## It's working if

- Every adopted principle lets a reader identify from the statement alone one choice it requires and one it forbids, and cites independent evidence.
- The map's decision rights classify every known choice and, where choices are builder-owned, state a concrete reversal budget and escalation conditions.
- Every human-owned decision ticket puts one residual judgment in its Question and keeps derived implications and builder discretion outside it.
- Every material factual premise is already in the map's Findings or explicit in the decision's Scenario.
- The map names a destination, while `PRINCIPLES.md` holds only guidance that survives beyond that destination.
- A round contains one ownership class and only decisions fully determined by an adopted principle, local policy, or recorded premise.
- Every human verdict produces a propagation delta: what resolved, what narrowed, and what still needs human judgment.
- Decisions no principle determines receive individual judgment under their decision right instead of forcing a vague principle to reach them.
- The map's closed-ticket indexes and tracker frontier agree with the tickets' real state.

## Where it fits

`through-line` is a huge-effort **on-ramp** to the main build flow. It is the principle-driven sibling of [wayfinder](https://aihero.dev/skills-wayfinder): both chart multi-session uncertainty, but through-line also extracts standing doctrine and uses it to settle decisions in rounds. It draws on [grilling](https://aihero.dev/skills-grilling) and [domain-modeling](https://aihero.dev/skills-domain-modeling) for decisions no principle determines, then hands a completed map to [to-spec](https://aihero.dev/skills-to-spec) unless execution was explicitly put in scope. When you're unsure which flow fits, [ask-matt](https://aihero.dev/skills-ask-matt) routes you.
