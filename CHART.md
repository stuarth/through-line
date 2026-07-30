# Chart

Chart one effort from a loose idea. Adopt governance and principles; do not resolve
the route's decision tickets.

1. **Name the destination.** Use `/grilling` and `/domain-modeling` to state the spec,
   decision, or change the effort is finding its way to. The human adopts its scope.
2. **Set decision rights.** Propose one posture using the repo background and the
   destination: reversal budget, protected classes, and escalation conditions
   included. Define protected classes by consequence—domain meaning, external
   behaviour, irreversible effect, or reversal cost—rather than by implementation
   noun. Keep internal representations builder-owned when they implement meaning
   already settled by principles or resolved decisions within the reversal budget,
   unless the human reserves them. The human confirms the posture once every known
   decision class can be classified.
3. **Distill first.** Mine prior decisions, ADRs, code, and closed maps; grill the
   human on recurring commitments. Before presenting the first candidate, read
   [ADMISSION.md](./ADMISSION.md) and take each candidate through it one at a time.
4. **Map breadth-first.** Ticket every sharp human-owned question and each
   above-threshold builder-owned choice. The frontier is mapped when each human-owned
   decision's **Question** holds one independently rejectable residual judgment,
   each builder-owned decision holds one independently resolvable choice, derived
   implications and builder discretion sit outside human Questions, and the
   remaining in-scope uncertainty is honestly fog.
5. **Create, then wire.** Create the map and currently specifiable tickets, then add
   native blocking edges in a second pass. For pre-existing completed legwork, create
   and claim its ticket, record its resolution, close it, and link it from
   **Findings**. Fire one `/research` agent per new research ticket.
6. **Validate and stop.** Take the new map through [Record](./SKILL.md#record).
   Charting is one session: stop before resolving any route decision.

If breadth-first grilling produces no fog and the whole journey fits one session,
skip the map and ask the human how to proceed.
