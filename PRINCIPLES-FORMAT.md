# PRINCIPLES.md Format

## Structure

```md
# {Context Name} Principles

{One or two sentence description of what these principles govern.}

**Small teams own whole verticals**:
Every feature is owned end-to-end by one team; no handoffs mid-feature.
_Holds even when_: the feature spans two services.
_Does not extend to_: platform and infra work.
_Evidence_: [Billing rewrite](…) — confirmed; [Auth migration](…) — set the infra boundary.

**Prefer boring tech**:
A new dependency must be older than the problem it solves; novelty needs a champion and an exit plan.
_Holds even when_: the shiny option is faster to adopt.
_Does not extend to_: throwaway prototypes.
_Evidence_: [Queue selection](…) — confirmed.
```

## Rules

- **A principle must forbid something.** If no conceivable decision would violate it, it is a platitude, not a principle — sharpen the statement until it bites, or leave it out.
- **Keep statements tight.** One or two sentences. The statement is the commitment; rationale lives in the evidence and ADRs it links.
- **Speak the domain's language.** Where `CONTEXT.md` defines a canonical term, the statement uses it. Domain-general principles are fine; domain-blind ones are not.
- **Stay few.** Dilution is a portfolio failure: every admitted principle spends the attention readers give the others. A rule-shaped candidate whose violation would leave the system merely inconsistent — not wrong about the domain — is a local policy for an effort's map, however good its evidence.
- **Boundaries record tested edges, not hypotheticals.** Write a _Holds even when_ or _Does not extend to_ line only when a real decision — or an invented scenario the human confirmed — actually pressed that edge. Untested boundaries are speculation wearing the format.
- **Evidence is formative only.** The trail keeps the decisions that set or tested a boundary — gist plus link, index-style. Routine confirmations stay on the tickets they resolved.
- **Group under subheadings** when natural clusters emerge. If all principles belong to one cohesive area, a flat list is fine.

## Single vs multi-context repos

`PRINCIPLES.md` shares `CONTEXT.md`'s shape and infers the structure the same way — but contexts are the shared *unit*, not a shared *trigger*: vocabulary pressure and principle pressure each justify a split independently.

- **`CONTEXT-MAP.md` exists** — multi-context: a `PRINCIPLES.md` beside each context's `CONTEXT.md`, holding the principles local to that context. Principles that span contexts live in a root `PRINCIPLES.md` — the analog of the root `docs/adr/` that holds system-wide decisions. Infer which file the current principle belongs to; if unclear, ask.
- **No `CONTEXT-MAP.md`** — one `PRINCIPLES.md` at the repo root. A principle that holds only in part of the repo stays here, scoped by its boundaries (`_Does not extend to_`) — no file split needed.
- **A cluster shares a territorial boundary** — several principles all bounded to the same part of the repo is a bounded context announcing itself: raise it with `/domain-modeling` rather than splitting `PRINCIPLES.md` unilaterally; once the context map records the context, its principles move beside its `CONTEXT.md`.
- **Create files lazily** — the first adopted principle a file would hold creates it.
