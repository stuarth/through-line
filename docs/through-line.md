Quickstart:

```bash
npx skills add mattpocock/skills --skill=through-line
```

```bash
npx skills update through-line
```

[Source](https://github.com/mattpocock/skills/tree/main/skills/engineering/through-line)

## What it does

`through-line` takes a huge effort full of apparently separate decisions, finds the recurring commitments beneath them, and turns those commitments into standing principles in `PRINCIPLES.md`. It then uses the adopted principles to derive batches of open decisions for you to confirm, so the effort stays coherent without making every choice from scratch.

Principles are adopted only by the human and must be falsifiable: the agent can propose, challenge, and derive from them, but it cannot quietly add doctrine or stretch a principle to cover a convenient answer.

## When to reach for it

You invoke this by typing `/through-line` — the agent won't reach for it on its own.

Reach for it when an effort is too large for one session and many of its decisions seem to rhyme — you want to discover the commitments they share, reuse those commitments across the effort, and leave durable guidance behind. If the route is foggy but recurring principles are not the point, use [wayfinder](https://aihero.dev/skills-wayfinder), which clears a map one decision at a time. For an idea small enough to sharpen in one conversation, use [grill-with-docs](https://aihero.dev/skills-grill-with-docs).

## Prerequisites

The effort's map and child tickets live on the repo's issue tracker, so `through-line` needs the tracker wiring that [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills) provides. If no tracker is configured, it falls back to the local-markdown tracker. It creates `PRINCIPLES.md` lazily when the first standing principle is adopted.

## Adoption is slow; derivation is fast

A principle has leverage because one statement can decide many cases, which also makes a bad principle unusually expensive. Admission is deliberately slow: each candidate must recur across independent decisions, be atomic, survive a counterexample, and promise leverage beyond the current destination. You adopt candidates one at a time, grounded in concrete evidence and predictions.

Once adopted, derivation is fast. Frontier tickets are classified by whether a principle **determines**, **constrains**, or **does not reach** them. Only determined decisions enter a round, and each derivation must leave no material judgment hidden. You see the round together for coherence, then confirm one decision at a time.

## Standing principles, local policies

The altitude test keeps `PRINCIPLES.md` from turning into a rule dump: if violating a commitment would make the system wrong about its domain, it may be a standing principle; if it would only make this effort inconsistent, it belongs on the map as a local policy. Local policies get the same derivation power for the current route but die with the map unless later, independent evidence earns promotion.

When a principle stops predicting good answers, the skill treats that as evidence rather than friction. Rejected derivations and counterexamples trigger a boundary, split, or refutation, followed by a review of decisions previously derived from it.

## It's working if

- Every adopted principle forbids a plausible choice and cites independent evidence.
- The map names a destination, while `PRINCIPLES.md` holds only guidance that survives beyond that destination.
- A round contains only decisions fully determined by an adopted principle or local policy, and you confirm each derivation separately.
- Decisions no principle determines go through the slow way instead of forcing a vague principle to reach them.

## Where it fits

`through-line` is a huge-effort **on-ramp** to the main build flow. It is the principle-driven sibling of [wayfinder](https://aihero.dev/skills-wayfinder): both chart multi-session uncertainty, but through-line also extracts standing doctrine and uses it to settle decisions in rounds. It draws on [grilling](https://aihero.dev/skills-grilling) and [domain-modeling](https://aihero.dev/skills-domain-modeling) for decisions no principle determines, then hands a completed map to [to-spec](https://aihero.dev/skills-to-spec) unless execution was explicitly put in scope. When you're unsure which flow fits, [ask-matt](https://aihero.dev/skills-ask-matt) routes you.
