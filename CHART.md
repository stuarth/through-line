# Chart

Chart one effort from a loose idea. Establish the route; do not start resolving its
decisions.

1. **Name the destination.** Use `/grilling` and `/domain-modeling` to state what the
   effort is trying to decide or change. The human confirms its scope. Set
   `Repository execution: in-scope` when the destination includes repository
   deliverables; otherwise set `out-of-scope`.
2. **Set decision rights.** Propose which choices remain human-owned and which
   reversible choices the builder may make under adopted principles. Protect domain
   meaning, external behavior, irreversible effects, and expensive reversals.
3. **Distill first.** Mine prior decisions, ADRs, code, and closed maps for recurring
   commitments. Take each candidate through [Admission](./ADMISSION.md).
4. **Map breadth-first.** Create a ticket for every sharp residual question and
   above-threshold builder choice. Keep settled implications outside the human
   Question and leave genuinely unshaped uncertainty as fog.
5. **Create, then wire.** Create the map and tickets before adding dependency edges.
   Record completed legwork as Findings.
6. **Fire research.** Dispatch a `/research` subagent for each research ticket to
   resolve it in parallel, capturing findings on a throwaway `research/<name>`
   branch with a context pointer from the ticket. Dispatch only for a named ticket.
7. **Validate and stop.** Reconcile through [Record](./SKILL.md#record). A Work
   session, not Chart, resolves the route.

If the whole journey is already clear enough for one session, skip the map and ask
the human how to proceed.

If mining finds no recurring commitment likely to determine several decisions, use
an ordinary implementation plan instead. Through-line earns its ceremony by
collapsing later judgment.
