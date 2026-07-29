# PRINCIPLES.md format

Admission, scope, and graduation rules live in [ADMISSION.md](./ADMISSION.md). This
file owns only entry and file structure.

## Entry

```md
# {Context Name} Principles

{One or two sentence description of what these principles govern.}

**Small teams own whole verticals**:
Every feature is owned end-to-end by one team; no handoffs mid-feature.
_Holds even when_: the feature spans two services.
_Does not extend to_: platform and infra work.
_Evidence_: [Billing rewrite](…) — confirmed; [Auth migration](…) — set the infra boundary.
```

- Keep the adopted statement to one or two sentences; rationale belongs in linked
  evidence and ADRs.
- Use canonical terms from `CONTEXT.md`.
- Record a boundary only after a real decision or human-confirmed scenario tests it.
- Keep formative evidence only: decisions that set or test a boundary, gist + link.
- Group entries under subheadings only when natural clusters emerge.

## File placement

`PRINCIPLES.md` follows `CONTEXT.md`'s shape, though vocabulary and principle pressure
can justify splits independently.

- With `CONTEXT-MAP.md`, put context-local principles beside that context's
  `CONTEXT.md`; put cross-context principles at the root.
- Without `CONTEXT-MAP.md`, use one root `PRINCIPLES.md` and express narrower scope
  through tested boundaries.
- When several principles share one territorial boundary, raise the emerging bounded
  context through `/domain-modeling` before splitting files.
- Create a principles file only when its first principle is adopted.
