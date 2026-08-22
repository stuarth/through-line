# Principles guide

Principles are standing doctrine: human-adopted commitments that resolve choices
across routes. A charter premise applies only to one route. ADRs remain repository
records for hard-to-reverse choices, not another Through-line state.

## Admit

Propose a principle only when it:

- recurs across independent decisions or materially different scenarios;
- is precise enough to require one plausible choice and forbid another;
- survives a concrete counterexample or states the boundary it revealed; and
- will shape more than the answer already in front of the route.

Present the candidate, the evidence it distills, one application, its scope, and what
it predicts elsewhere. The human adopts, amends, or rejects it. Without explicit
adoption, retain the underlying decision as a charter premise only when the human has
accepted it for that route.

## Record

Keep the adopted statement short and leave rationale in linked evidence:

```markdown
**<Name>**: <one or two sentences that guide a required and forbidden choice>
_Scope_: <where it applies>
_Does not extend to_: <tested boundary>
_Evidence_: <decisions or scenarios that formed or tested it>
```

Use the repository's existing principles location. Create `PRINCIPLES.md` only after
the first adoption. Split files only when existing domain boundaries make the scope
clearer; do not create a Through-line-specific placement taxonomy.

## Challenge

When a real fact, decision, or result contradicts a principle, stop applying it to
the affected case. Present the counterexample and ask whether it is an exception, a
narrower boundary, a split, a replacement, or insufficient evidence. The human
decides. Record any adopted change, then propagate it through every dependent unit.

Repeated implementation failure without counterevidence does not falsify a principle;
rechart the unit under [Advance](./ADVANCE.md) instead.
