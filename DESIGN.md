# V2 design rationale

## The product

Work together without starting over in judgment. Through-line v2 helps a human and
an agent develop, apply, and revise a small body of consequential commitments during
everyday work. Discovery is proactive. Interruption is selective. Recorded principles
have visible consequences for the work and remain open to challenge.

This is a fresh start. V1's routes, charters, unit ownership, supervisors, integration
refs, tracker adapters, and closure receipts are outside the product. Other workflows
can coordinate execution. V2 does not require a substantial project or even a codebase.

## Three influences, kept distinct

[Peter Naur, Programming as Theory Building](https://pages.cs.wisc.edu/~remzi/Naur.pdf)
locates important programming knowledge in the ability to relate software to the
world, justify its construction, and respond intelligently to new demands. He does
not claim that rules or documentation can fully contain that understanding. Our design
uses bounded commitments, reasons, and contrasting cases to support reconstruction
of relevant judgment. It does not claim to serialize the programmer's theory.

[Sean Goedecke's commentary](https://www.seangoedecke.com/in-defense-of-not-understanding-your-codebase/)
defends useful work through partial understanding and reconstruction. Our design
therefore makes local sufficiency a stopping condition. Comprehensive understanding
and complete documentation are not prerequisites for acting.

The author's Inferal manifesto, discussed during v2's design, proposes directly
editable operational rules with governed consequences. Through-line borrows the demand
that commitments visibly affect work, but an agent still interprets its prose. These
principles are not directly executable rules. The essay is not reproduced in this
repository, and this design makes no claims about a deployed Inferal product.

The synthesis is a design proposal, not a claim that these sources agree: preserve
judgment that would otherwise be lost, reconstruct what the present choice needs,
and keep incomplete understanding usable and correctable.

## Deliberate choices

- **Progressive discovery by applicability.** A small entry point routes to scoped
  records and then evidence. Cross-cutting concerns need semantic discovery, not just
  directory-based lookup. The index never substitutes for the authoritative record.
- **A counterfactual admission bar.** Each principle must change a plausible future
  choice. Generic advice and task-specific observations do not earn permanent attention.
- **Human adoption with no ritual.** Discussion can form new judgment. Explicit
  adoption establishes authority; inference, silence, and one-off task acceptance do not.
- **Visible application and bounded impact discovery.** Cite concrete consequences,
  test relevant claims, and inspect consumers when a commitment changes. Do not promise
  exhaustive propagation across an unknown system.

## What this draft does not prove

Metadata and instructions make automatic use possible. They do not guarantee host
invocation, retrieval recall, or good judgment. The evaluation suite specifies intended
behavior for fresh sessions, including restraint and counterexamples. It separates
structural checks, author review, and live agent results.

Key questions for review: does the entry description activate on ordinary work, does
applicability-based discovery find cross-cutting concerns without reading everything,
and does discussion improve consequential choices without turning into bureaucracy?

## Transition

This draft replaces the skill at the repository root. V1 remains available through
Git history; it is not loaded alongside v2. Existing workspace routes and principles
are not automatically migrated, deleted, or reclassified. Finish v1 work using a
checkout pinned to its version. For v2, link genuinely adopted existing commitments
into the workspace's chosen entry point after checking their authority and scope.
