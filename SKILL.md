---
name: through-line
description: Find the through-line of a huge effort — distill the principles running through its thousand decisions into a standing PRINCIPLES.md, then resolve open questions in batched derivation rounds you confirm.
disable-model-invocation: true
---

A loose idea has arrived — too big for one agent session, and dense with open questions. Worked one at a time, those questions become a thousand one-off decisions — each sound, none generalised, all quietly obeying commitments nobody has written down. Those commitments are the effort's **through-line**: the thread of intent running through every decision. This skill finds it and writes it down — first principles in `PRINCIPLES.md` — then lets derivation do the deciding: once articulated, the principles imply answers to whole batches of open questions, and the human confirms **derivations** instead of reasoning out every decision from scratch. Only the genuinely novel questions get decided the slow way — and a cluster of those is the signal the through-line has a gap.

The effort has a **destination** — the spec, decision, or change it is finding its way to — named first, because it fixes the scope. Produce decisions, not deliverables, unless the map's **Notes** says otherwise.

## First principles

`PRINCIPLES.md` is **standing**: it belongs to the repo, not the effort. It shares `CONTEXT.md`'s *shape* — a root file, per-context files once a `CONTEXT-MAP.md` divides the repo, spanning principles at the root the way system-wide decisions stay in the root `docs/adr/` — but not its *trigger*: vocabulary pressure and principle pressure split that structure independently. A principle scoped narrower than its file needs no split — boundaries do that — and a cluster of principles sharing one territorial boundary is a bounded context announcing itself: surface it to `/domain-modeling`, whose artifact the context map is. Create files lazily, when the first principle is adopted. Efforts come and go; each leaves the principles sharper than it found them.

Each principle has a **name**, a statement, the **boundaries** of where it holds, and a trail of **evidence** — format in [PRINCIPLES-FORMAT.md](./PRINCIPLES-FORMAT.md). Two disciplines keep it honest:

- **Adopted only.** The principles are the human's. The agent proposes, derives, and challenges; nothing enters or changes `PRINCIPLES.md` without the human adopting it. Apply the principles; never extend them.
- **Falsifiable only.** A principle must forbid something — there must be a decision it would rule out. A principle nothing could contradict is a platitude; sharpen it until it bites, or reject it.

### Admission

**Adoption is slow; derivation is fast.** A badly framed principle multiplies one error into many, so friction belongs at the door: candidates may be previewed together, but each is put to the human one at a time — adopted standing, adopted as a local policy, amended, or rejected before the next; the agent proposes the scope by the altitude test, the human disposes. On top of **Falsifiable only**, a candidate must pass four tests:

- **Recurrence** — grounded in at least two independent decisions, or in an explicit human commitment tested against two materially different scenarios.
- **Atomicity** — violating one part cannot leave the rest intact; if it can, split the candidate.
- **Counterexample** — a plausible scenario where following it gives the wrong answer has been probed, and the statement or a boundary survived.
- **Leverage** — it has shaped, or will plausibly shape, more than one decision, and it holds beyond this effort's destination. A commitment that only explains a single hard-to-reverse choice is an ADR; one true only for this route is at most a local policy — neither is standing doctrine.

A candidate that passes is put to the human **grounded** — never the statement alone:

- **Statement** — the exact standing text; abstract is fine, this is what is adopted verbatim.
- **Concretely** — the statement re-said in the effort's domain language: what it means *here*. A second abstraction in this field is a failed field.
- **Evidence** — the decisions it distills from, named and linked; on adoption these seed the principle's evidence trail.
- **Predictions** — the frontier tickets it would determine or constrain, and how; a named alternative it forbids; a plausible scenario where no applicable ticket exists yet. Predictions preview the validation pass, and a prediction the human dislikes is a boundary found before adoption — the cheapest time to find one.

Revision proposals are candidates too: a boundary, split, or standing priority proposed during an audit or collision is presented the same grounded way.

`PRINCIPLES.md` does not replace ADRs: an ADR records one hard-to-reverse decision and its trade-off; a principle is what several decisions turn out to obey. They cross-cite.

Nor does it hold every rule that passes the tests. The **altitude test**: violated, would the system be *wrong about the domain*, or merely *inconsistent*? Wrong is a principle; inconsistent is a **local policy** — adopted into the map's **Local policies** section in the same entry format, classifying and determining tickets exactly as a principle does, and dying with the map. Dilution is a portfolio failure the per-candidate tests can't see, so **when in doubt, local**: a local policy graduates through the normal gate on **independent evidence** — a second effort reaching for it, evidence predating its effort, genuinely disparate scenario classes — never on trial count alone, since within-effort derivations all share one destination. Where it graduates *to* follows altitude: scope-locals promote into `PRINCIPLES.md`; a replicated convention is still a convention — it moves to the repo's conventions home, never the constitution. Un-admitting a diluting principle takes an audit.

## The map

Each effort gets a **map** — a single issue on the repo's issue tracker, labelled `through-line:map`; its tickets are child issues of the map. Where the map, its child tickets, blocking, and frontier queries physically live is tracker-specific — the issue tracker should have been provided to you; consult the tracker doc's section covering those operations — canonically "Wayfinding operations", whatever the doc names it — and default to the local-markdown tracker if none was provided. Refer to the map, every ticket, and every principle by **name**, never by a bare id.

The map is the whole effort at low resolution, loaded once per session. Open tickets are **not** listed — they are open child issues, found by query.

```markdown
## Destination

<one or two lines; every session orients to it before anything else>

## Notes

<domain; skills every session should consult; effort preferences; whether execution is in scope>

## Local policies

<!-- principle-shaped rules below constitutional altitude or scoped to this route: PRINCIPLES.md entry format, full derivation power within this map, dead when the map closes -->

## Decisions so far

<!-- the index — one line per closed ticket: gist of the confirmed answer, detail on the ticket -->

- [<closed ticket title>](link) — <gist of the confirmed answer>

## Not yet specified

<!-- the fog: in-scope questions not yet sharp enough to ticket; graduates as answers clear it -->

## Out of scope

<!-- work consciously ruled beyond the destination; never graduates — scope, not sharpness, lands it here -->
```

## Tickets

Each ticket is a child issue of the map; its body is the question it resolves:

```markdown
## Question

<the decision or legwork this ticket resolves>
```

Each carries a `through-line:<type>` label:

- **decision** (HITL) — the default: a question whose resolution is a decision. Resolved by derivation in a round when an adopted principle determines it, the slow way when none does.
- **research** (AFK) — a fact a decision waits on, outside the working directory; resolved by a `/research` subagent.
- **prototype** (AFK build, HITL reaction) — a cheap concrete artifact to react to; build it, link it as an asset, and the human reacts in session.
- **task** (HITL or AFK) — manual legwork that unblocks a decision: provisioning, data moves, sign-ups.

A session **claims** a ticket by assigning it to the dev driving the map, **first**, before any work; the assignee _is_ the claim. Blocking uses the tracker's **native** dependency relationship, so the **frontier** — the open, unblocked, unclaimed tickets — renders visually in the tracker's own UI. The answer isn't part of the body; it's recorded on resolution. Assets are linked from the ticket, not pasted in.

## The round

First classify every frontier `decision` ticket against the adopted principles and the map's local policies:

- **Determines** — the recommendation follows from the principle with no material judgment left.
- **Constrains** — the principle rules out some answers, but material judgment remains.
- **Does not reach** — the principle has no real bearing here.

A principle supplies direction, never missing facts: a ticket is determined only when its material factual premises are established — or stated as explicit assumptions in its **Scenario**. If an unresolved fact could change the recommendation, create or link the `research` ticket that resolves it, wire it as a blocker, and let the ticket wait off the frontier.

A round holds only **determined** tickets — a merely compatible answer is not a derivation; constrained and unreached tickets take the slow way. Size the round to what the human can genuinely weigh side by side — about five, favouring materially different scenarios — and leave the rest open for a later round. A newly adopted principle gets a **validation pass** first: its first round holds at most three tickets. **Claim the round's tickets** — and only those — so concurrent sessions skip them.

Phrase each as a **derivation**:

- **Principle** — cited by name; a local policy is cited as *local*.
- **Scenario** — the concrete situation this ticket presents.
- **Implications** — what the principle rules in or rules out here.
- **Residual judgment** — `none`, and mean it: if material judgment remains, the ticket was constrained, not determined — drop it from the round and take it the slow way.
- **Recommendation** — the answer that follows.

Present the round at two resolutions. First the **overview** — every ticket's name and one-line recommendation, side by side. The overview is the coherency test: derivations viewed together expose an incoherence each would hide alone, and when a principle pulls different directions across items, say so right there — that friction is data about a boundary, not noise to smooth over. Then zoom: **one derivation per turn**, at full detail, the human's verdict given before the next is presented. Each item is confirmed on its own — a round-level "confirm all" confirms nothing. A material amendment — one that changes the recommendation — is a rejection of the presented derivation: diagnose which link broke before resolving the ticket; a wording clarification that leaves the recommendation unchanged is confirmation. A round is human-in-the-loop by definition — an agent that answers its own round items has broken the skill.

Principles collide, too: when two adopted principles determine one ticket incompatibly, residual judgment is not `none` — drop the ticket from the round and audit both boundaries. If both genuinely still hold, the trade-off is the human's, made in the open the slow way. Its resolution may set a boundary, expose a missing higher-order principle, adopt a standing priority — itself principle-shaped, so it enters through [Admission](#admission) — or stay a one-off decision; weakening either principle is one possible outcome, never the automatic one.

A rejection is diagnosed, not just recorded — which link broke?

- **Wrong principle cited** — re-derive under the right one; the principles are untouched.
- **Scenario outside the boundary** — the principle doesn't hold here; record the boundary in `PRINCIPLES.md`.
- **Bad derivation** — the reasoning slipped; fix it and re-present.
- **Constrained, not determined** — the round was assembled too aggressively; unclaim the ticket and take it the slow way. The principle needn't change.
- **The principle itself is wrong** — the deepest outcome: bound, split, or refute it (see Falsify).

**Record each confirmed item on its ticket**: post the derivation — principle cited, scenario, implications, confirmed answer — as a resolution comment, **close** the ticket, and gist it into **Decisions so far**. Update `PRINCIPLES.md` inline for every boundary set or revision adopted; a ticket that set or tested a boundary joins the principle's evidence trail. One decision, one ticket, one link.

## The slow way

A frontier ticket no principle determines — unreached, or merely constrained — gets decided the slow way: `/grilling` and `/domain-modeling`, one ticket at a time, its resolution recorded like any other. Take it gladly rather than stretching a principle to cover it. Watch for the cluster: several such tickets leaning the same direction are not several problems — they are one missing principle. Distill it, adopt it, and the cluster collapses into coming rounds' derivations. The slow way funds the fast way.

## Distill

Principles arrive from two directions:

- **Opportunistically** — mid-round or mid-grilling, a decision smells like an instance of something general. Name the candidate on the spot.
- **By mining** — a deliberate pass over the accumulated decision record: the map's Decisions so far, `docs/adr/`, the codebase, and closed maps — including their **Local policies** and closing sweeps, ready-made candidates awaiting independence. Recurring commitments are candidate principles.

Either way, a candidate is grilled through the [Admission](#admission) tests and put to the human grounded. Adoption attaches to the exact **Statement** and boundaries as written, never to agreement with a slogan, a philosophy document, or a past recommendation. Adopted, it enters `PRINCIPLES.md` — and its first applicable round is its validation pass.

## Falsify

A principle is held the way science holds a law: adopted on evidence, applied by derivation, revised the moment a counterexample survives. Hunt counterexamples two ways:

- **Vigilance** — every session applying principles watches for contradictions: code that violates one, a past decision that defies one, a fresh confirmation that sits badly against one. Surface it immediately.
- **Audit** — on request, a dedicated pass that stress-tests the principles against the code, the decision record, and invented edge scenarios.

An audit is also **event-driven**: pause derivation rounds and audit a principle when two of its derivations are rejected or materially amended; when exceptions or boundary qualifications recur; when the destination or its context shifts; when its boundary text grows more complex than its statement; or when confirmed answers keep needing material residual judgment despite citing it. Each signals a principle due to be bounded, split, or refuted — never one to reword more permissively.

A counterexample that survives scrutiny resolves one of three ways, each adopted by the human: it **bounds** the principle (it sits outside where the principle holds — record the boundary), **splits** it (two principles were hiding in one), or **refutes** it. When a principle is revised or refuted, its evidence trail and the resolution comments find every ticket derived from it; surface them as a **review round** — same overview-then-zoom format — and the human decides which to revisit. Nothing is silently re-decided.

## Fog and scope

The map is deliberately incomplete — don't chart what you can't yet see. **Fog or ticket?** The test is whether you can state the question precisely now — not whether you can answer it. Sharp enough to state, it's a ticket — even if it's blocked; not yet, it stays in **Not yet specified** — the fog. Don't pre-slice the fog into ticket-sized pieces: one patch may graduate into several tickets, or none, once answers sharpen it.

Work ruled beyond the destination goes to **Out of scope** and never graduates — scope, not sharpness, lands it there. Ruling a ticket out is a scoping act, not a step on the route: **close it** and record the gist plus why it's out, linking the closed ticket — and keep it out of **Decisions so far**, which records only the route actually walked.

## Invocation

### Chart

User invokes with a loose idea.

1. **Name the destination** — `/grilling` and `/domain-modeling`; the destination fixes the scope.
2. **Distill first.** Run Distill's mining pass over the record and grill the human on their commitments — philosophy before questions, because the principles decide how many questions there really are. Candidates pass [Admission](#admission) and are adopted one at a time into `PRINCIPLES.md`.
3. **Map the frontier.** Grill breadth-first for the open questions. **If this surfaces no fog** — the whole journey fits one session — you don't need a map: stop and ask the user how they'd like to proceed.
4. **Create the map** (label `through-line:map`) and the tickets you can specify now as its children — then wire blocking edges in a **second pass** (issues need ids before they can reference each other). Everything not yet sharp stays in **Not yet specified**. Fire a `/research` subagent per research ticket.
5. Stop — charting is one session's work; it adopts principles, not answers.

### Work

User invokes with a map.

1. Load `PRINCIPLES.md` and the map — the low-res view; harvest any completed legwork tickets.
2. **Run one round** — at most one per session: classify the frontier (determines / constrains / does not reach), claim the determined tickets, present. If nothing is determined, distill when the record shows rhyme — a cluster on the frontier, or slow-way decisions since the last pass that lean together; otherwise grill one ticket the slow way.
3. Record: resolution comments, closed tickets, **Decisions so far**, `PRINCIPLES.md` updates inline.
4. Re-chart: add newly surfaced tickets (create-then-wire), graduate fog the answers have sharpened, rule mis-scoped tickets out of scope.
5. **Destination reached? Close the map** with a **closing sweep** of its local policies: record each policy's track record — derivations determined, scenario spread, whether its evidence predates the effort; review the group for common threads, distilling any higher-altitude candidate the policies jointly imply; promote through normal Admission wherever the evidence is already independent. The rest stay on the closed map — persistent and minable — for a future effort to supply the missing independence.

Expect other sessions to edit the tracker concurrently; the map and its tickets, not the conversation, are the shared state.
