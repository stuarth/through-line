# Supervise

Use this path only when the human asks an existing route to **advance unattended**.
The host must support a completion-aware wait; otherwise report that limitation
before dispatching.

Repeat:

1. Refresh the charter, principles, frontier, and claimed unit. If a live worker owns
   it, resume waiting. If ownership is stale, recover from its durable checkpoint or
   release it before selecting work.
2. Stop when the route is resolved, the frontier requires human authority, the
   charter must change, progress needs an external unblock, or ownership is unclear.
   Before the first end-to-end result, if the recorded effort-review trigger is
   reached, dispatch only work that can produce path evidence; if none exists, return
   the route shape to the human.
3. Select one builder-owned unit, preferring the thin complete path. When no unit is
   open, select the **Advance** route transition that evaluates Deferred or closes the
   route. Start a fresh no-history [Advance](./ADVANCE.md) worker with the route
   reference, exact selection, reaching evidence, useful references, and completion
   checks. The worker's first mutation persists its host-addressable identifier.
4. Run workers serially because each result can change the frontier. Wait for the
   terminal result using the host's maximum completion-aware timeout. An expired wait
   or unrelated wake changes nothing while the returned worker status remains live:
   re-arm without reloading route state or reporting unchanged progress. Recover a
   worker the host reports terminal without a durable result as stale ownership.
5. On completion, reload durable state and repeat from step 1. A worker completion
   advances the loop; it does not end supervision.

Record an explicit human verdict directly rather than dispatching a record-only
worker. User-visible updates are limited to dispatch, a material finding or scope
change, and completion, checkpoint, blocker, or human frontier. A live worker or
expired wait is never a final answer.
