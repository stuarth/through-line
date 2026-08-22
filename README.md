# through-line

`through-line` carries a large effort across many agent sessions without losing its
direction. It keeps the route durable: the destination, open choices, settled
results, and their downstream consequences.

The product is built around decisions and outcomes rather than a task backlog. A
chartered route advances one meaningful unit at a time and derives its next frontier
from recorded state, so it still makes sense to a fresh worker.

## Install and invoke

Install from the skills registry:

```bash
npx skills@latest add stuarth/through-line
```

Update with `npx skills update through-line`. To follow the repository directly,
clone it and symlink the skill directory:

```bash
git clone https://github.com/stuarth/through-line ~/dev/through-line
ln -s ~/dev/through-line ~/.claude/skills/through-line
```

Invoke it explicitly as `/through-line` in Claude Code or `$through-line` in
Codex. Automatic invocation is disabled; see
[agents/openai.yaml](./agents/openai.yaml). When an issue tracker is configured,
the route can live there. Otherwise, the bundled [local Markdown
tracker](./trackers/local-markdown.md) and
[validator](./scripts/validate_local_map.py) provide a self-contained option.

## How it works

**The charter fixes the route.** It names the destination, the boundaries of the
effort, the first end-to-end result worth reaching, the premises currently being
relied on, and who may decide what. This is the boundary for autonomous progress:
discoveries inside it can extend the map, while a proposed change to the charter
comes back to the human.

**Decision rights keep direction human-owned.** The human retains control of the
destination, protected meanings, external promises, and consequential or
irreversible effects. The builder can make ordinary reversible choices that follow
the charter and settled decisions. A route can reserve additional choices for the
human when the work needs tighter control.

**A unit records either a decision or an outcome.** Each unit carries the question
or result, the premises and acceptance evidence that matter, and its eventual
resolution with provenance. The route has at most one claimed builder unit. Human
choices remain independent units even when several ready questions share one concise
prompt. Finishing or checkpointing builder work leaves a durable handoff before a
fresh session takes another unit.

**Every resolution propagates.** When a premise, decision, or result changes,
Through-line revisits every resolved dependent and records whether it still stands
or reopens. Open work is then recomputed rather than manually curated. The visible
frontier is simply the work that is open, unblocked, and unclaimed; only items that
need human judgment form the human frontier.

**Principles are optional leverage.** If a commitment recurs, rules out a plausible
choice, and survives counterexamples, the agent may propose it as a standing
principle. It becomes active only when the human adopts it. Principles help future
units inherit hard-won judgment, but a route does not need them, and contradictory
evidence can put one back in question.

**Repository execution is optional.** A route may stop at durable decisions and
outcomes, or include implementation. When code is in scope, each repository moves
through one integration ref so composition is observable. Review covers the exact
integrated ref at stable architecture or provider boundaries and before an external
effect, publication, dependent human gate, or completion. It reports whether the
stated claim is supported; it does not grant authority for an effect.

**Unattended mode uses fresh workers.** A supervisor sends one explicit unit packet
to a fresh worker with no conversation history, waits for its terminal result, and
then derives the next unit or route transition. The loop continues serially until the
route reaches a human frontier, needs a charter change, completes, or reaches its
first-result effort trigger without path evidence. Fresh workers make recorded state,
not conversational memory, prove that the route is resumable.

## Repo layout

This repository is the skill. [SKILL.md](./SKILL.md) introduces the model and
routes into the focused guides:

- [CHART.md](./CHART.md) — turn an idea into a chartered route
- [ADVANCE.md](./ADVANCE.md) — resolve a unit or complete a route transition
- [SUPERVISE.md](./SUPERVISE.md) — continue through units unattended
- [EXECUTION.md](./EXECUTION.md) and [IMPLEMENT.md](./IMPLEMENT.md) — plan,
  integrate, and verify repository work
- [REVIEW.md](./REVIEW.md) — test a claim against one immutable object
- [PRINCIPLES-GUIDE.md](./PRINCIPLES-GUIDE.md) — propose, adopt, and challenge
  standing principles

The tracker adapter defines storage; the skill defines the product model. That
separation lets Through-line stay useful across hosts without coupling the route to
another mandatory skill.
