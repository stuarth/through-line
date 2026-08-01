---
"mattpocock-skills": patch
---

Simplify `/through-line`'s durable-state bookkeeping. Ticket sections now express
verdict status structurally — one `## Provisional verdict` on an unresolved ticket,
`## Resolution` as the sole final premise, `## Verdict history` as an inert
archive — replacing the per-entry `State: active|finalized|superseded` markers.
Claim doctrine lives only in `SKILL.md`, the propagation sweep and session-finish
steps lose their duplicated bookkeeping, a wording clarification no longer counts
as a human verdict, and the local-map validator now enforces the mechanical
Record invariants (status/type validity, assignee consistency, resolution and
checkpoint placement).
