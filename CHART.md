# Chart

Chart one effort from a loose idea. Establish the route; do not start resolving its
decisions.

1. **Name the destination.** Use `/grilling` and `/domain-modeling` to state what the
   effort is trying to decide or change. The human confirms its scope. Set
   `Repository execution: in-scope` when the destination includes repository
   deliverables; otherwise set `out-of-scope`. With execution in scope, also record
   in **Notes** the first end-to-end result and the human's expected active effort to
   reach it.
2. **Set decision rights.** Propose which choices remain human-owned and which
   reversible choices the builder may make under adopted principles. Protect domain
   meaning, external behavior, irreversible effects, and expensive reversals.
3. **Distill first.** Mine prior decisions, ADRs, code, and closed maps for recurring
   commitments. Take each candidate through [Admission](./ADMISSION.md).
4. **Map in proof order.** With execution in scope, make the first executable outcome
   the thin complete path across the components to an exposed result, and map the rest
   of the route under the [ticket rule](./SKILL.md#map-and-tickets). Without execution,
   map sharp residual questions and above-threshold builder choices. Keep settled
   implications outside the human Question and leave genuinely unshaped uncertainty
   as fog. A ticket that adds a durable mechanism, persisted artifact, or acceptance
   gate names the current consumer or protected invariant it serves and the existing
   path it extends; a replacement carries the human verdict approving that change.
   Defer the rest in **Not yet specified**.
5. **Create, then wire.** Create the map and tickets before adding dependency edges.
   Record completed legwork as Findings.
6. **Confirm the route.** Show the mapped route beside the smallest credible route:
   what each reuses, what each defers, and what deferring the difference costs. The
   human confirms only the route shown; expanding it requires another verdict.
7. **Fire research.** Dispatch a `/research` subagent for each research ticket on the
   confirmed route, capturing findings on a throwaway `research/<name>` branch with
   a context pointer from the ticket. Dispatch only for a named ticket and follow
   [receipt-only coordination](./SKILL.md#coordination).
8. **Validate and stop.** Reconcile through [Record](./SKILL.md#record). A Work
   session, not Chart, resolves the route.

If the whole journey is already clear enough for one session, skip the map and ask
the human how to proceed.

If mining finds no recurring commitment likely to determine several decisions, use
an ordinary implementation plan instead. Through-line earns its ceremony by
collapsing later judgment.
