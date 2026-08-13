# through-line

A skill for driving efforts too large for one agent session — where the
bottleneck isn't code generation, it's **decisions**: the agent re-asks
questions you already answered, forgets verdicts after compaction, or quietly
decides things that were yours to decide.

`through-line` makes decisions the unit of work. A huge effort hides recurring
commitments beneath its many choices; the skill distills those into standing
principles you adopt, then propagates every verdict through a map of atomic
decision tickets, so each answer resolves or narrows as many later questions as
it can. You only ever see the residual judgment your previous answers couldn't
settle.

## Install

```bash
npx skills@latest add stuarth/through-line
```

Later, `npx skills update through-line` picks up new versions. Or, to track the
repo directly, clone and symlink — a `git pull` then keeps the installed skill
current:

```bash
git clone https://github.com/stuarth/through-line ~/dev/through-line
ln -s ~/dev/through-line ~/.claude/skills/through-line
```

Invoke with `/through-line` — the agent won't reach for it on its own. It works
under Claude Code and Codex (see [agents/openai.yaml](./agents/openai.yaml)).

Maps and tickets live on the repo's issue tracker when one is wired up;
otherwise the skill falls back to the bundled local-markdown tracker and its
validator (see [trackers/](./trackers/) and [scripts/](./scripts/)).
When updating a legacy local map, add `Repository execution: out-of-scope` for a
decision-only effort; use `in-scope` and add execution heads when its destination
includes repository deliverables.

## How it works

**You adopt principles; the agent proposes them.** Recurring commitments are
distilled into `PRINCIPLES.md`. Admission is deliberately slow — a candidate
must recur across independent decisions, be atomic and falsifiable, and survive
a counterexample — because one bad principle mis-decides many cases. Once
adopted, a principle is a strong prior, not a law: evidence strong enough to
contradict it triggers re-examination, and re-examination is still yours to
confirm.

**Every verdict propagates.** After each answer, the agent sweeps the remaining
map: decisions the answer determines resolve, constrained questions shrink to
their residual judgment, moot ones close. Replacing an earlier premise reopens
and rechecks its dependents before the replacement propagates.

**Decision rights are explicit.** Once per effort you agree on what the builder
may decide (cheaply reversible route choices, within a stated reversal budget)
and what always comes back to you: destination, scope, doctrine, domain
meaning, external promises, irreversible effects. Direction is never delegated.

**One round or ticket per Work session, hard stop.** The tracker, map, and
principles — not the conversation — are the shared state. A session takes one
round or ticket, records the outcome with provenance (the quoted human verdict,
or the principle that determined it), reports the frontier, and stops. Its receipt
retires that worker; automatic continuations and resumed turns may only finish the
same unresolved claim. Research tickets are the exception: `/research` subagents
burn them down in parallel, leaving findings on throwaway branches the tickets point
to.

**Advance unattended to a real frontier.** Invoke with an existing map and say
**advance unattended**: the supervisor remains active, runs a fresh no-history Work
session per ticket, and continues through builder-owned decisions and legwork until
the map closes or genuinely needs human judgment or an external unblock. It waits on
worker completion instead of polling. An expired wait is re-armed without reloading
or narrating unchanged state; it does not end supervision. A host without a
completion-aware wait cannot offer this mode.

## It's working if

- Every adopted principle lets a reader name, from the statement alone, one
  choice it requires and one it forbids.
- Every human-owned ticket asks exactly one residual judgment.
- Every human verdict produces a propagation delta: what resolved, what
  narrowed, what still needs you.
- Every closed decision preserves why it closed — quoted verdict, linked
  artifact, or the determining principle.
- Each Work session ends after one round or ticket and its cascade, with the
  next frontier recorded for a fresh session.
- A repository-execution map closes only at the exact code head covered by a fresh
  whole-effort review and records an immutable tracker-only closure boundary. Later
  repository work does not rewrite that boundary; in-scope corrections reopen the
  same canonical map while its prior closure remains immutable in Git history.

## Repo layout

This repo **is** the skill — [SKILL.md](./SKILL.md) at the root, with its phase
runbooks alongside:

- [CHART.md](./CHART.md) — turn a loose idea into a map
- [WORK.md](./WORK.md) — advance an existing map, one round or ticket per session
- [SUPERVISE.md](./SUPERVISE.md) — opt-in unattended advancement
- [ADMISSION.md](./ADMISSION.md), [REVIEW.md](./REVIEW.md),
  [IMPLEMENT.md](./IMPLEMENT.md), [EXECUTION.md](./EXECUTION.md) — supporting
  stages
- [PRINCIPLES-FORMAT.md](./PRINCIPLES-FORMAT.md) — the shape of adopted doctrine

## Where it fits

`through-line` began inside a fork of
[mattpocock/skills](https://github.com/mattpocock/skills) and grew until it was
the fork's entire purpose; this repo carries that full history. It builds on
that ecosystem rather than forking it: it is the principle-driven sibling of
[wayfinder](https://aihero.dev/skills-wayfinder) (multi-session maps without
standing doctrine), draws on [grilling](https://aihero.dev/skills-grilling) and
[domain-modeling](https://aihero.dev/skills-domain-modeling) for decisions no
principle determines, and hands a completed map to
[to-spec](https://aihero.dev/skills-to-spec) unless execution was put in scope.
Install mattpocock/skills separately for those — `claude plugins install
mattpocock-skills` under Claude Code, or its `skills.sh` for other harnesses;
without its tracker wiring, through-line uses the bundled local-markdown tracker.
