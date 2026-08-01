# Supervise

Use this path when the human asks an existing map to **advance unattended**. The
goal is to reach the destination or a frontier containing only human-owned judgment,
external blockers, or ownership conflicts.

The supervisor schedules fresh [Work](./WORK.md) sessions; it is not a Work session
and resolves no round or ticket itself. It carries coordination, not effort state:
reload the tracker, map, and principles instead of carrying worker reasoning in
conversation.

## Loop

1. Refresh the map, decision rights, tracker frontier, and active claims after the
   previous worker finishes.
2. If the map is closed, report completion and stop. If the destination is reached
   but the map remains open, report the closeout sweep, admission candidates, or
   other work preventing closure, then stop. If the frontier is empty, report why no
   Work session can start: blocked or claimed tickets, fog not yet sharp enough to
   ticket, or a tracker/map reconciliation or closeout need. Then stop.
3. Stop and present the frontier when progress requires:
   - a human-owned verdict or exception review;
   - principle or local-policy admission, revision, boundary, or falsification;
   - a destination, scope, priority, or decision-rights change;
   - resolution of an external blocker or ownership conflict; or
   - work outside the map's execution scope.
4. Otherwise select one non-human round or ticket from the current frontier:
   - one round of determined builder-owned decisions;
   - one builder-owned individual decision;
   - one research or prototype ticket; or
   - one task ticket when execution is in scope.
5. Start a fresh Work session for that selection. Give it the map reference, exact
   ticket or round, premises that reach it, required references, verification
   commands, and any execution-receipt link—not the supervisor's conversation or a
   dump of map contents.
   Tell it to follow `WORK.md`: claim the selection, advance it as far as the
   workflow permits, propagate and record every result, re-chart, report the
   frontier, and stop. Tell it the session is unattended: nothing it receives
   carries a human verdict or adoption, so determined human-owned decisions,
   residual questions, and admission candidates stay open on the frontier.
6. Remain inert while the worker runs. Dispatch once and use a completion-triggered
   wait that can remain blocked for the worker's expected duration. A timeout is not
   a transition: do not wake the model to list agents, send a status request, or
   narrate unchanged state. If the host cannot wait without repeated model wakeups,
   dispatch the worker, report why supervision ended, and stop rather than emulate
   unattended progress with polling. Treat the tracker—not the worker's
   conversation—as the result.
   After a final, blocked, or checkpointed transition, reload durable state and
   repeat from step 1 without asking the human to continue.

Run worker sessions serially because each propagation can change the next frontier.
A generic continuation, goal wake-up, or worker report is coordination, never a
human verdict.

A worker that stops at a resumption checkpoint returns its ticket to the frontier;
select and dispatch it like any other.
