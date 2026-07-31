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
2. Stop and present the frontier when progress requires:
   - a human-owned verdict or exception review;
   - principle or local-policy admission, revision, boundary, or falsification;
   - a destination, scope, priority, or decision-rights change;
   - resolution of an external blocker or ownership conflict; or
   - work outside the map's execution scope.
3. Otherwise select one non-human round or ticket from the current frontier:
   - one round of determined builder-owned decisions;
   - one builder-owned individual decision;
   - one research or prototype ticket; or
   - one task ticket when execution is in scope.
4. Start a fresh, minimal-context worker session for that selection. Give it the map,
   the exact ticket or round, the premises that reach it, required references, and
   verification commands. Tell it to follow `WORK.md`: claim the ticket or every
   ticket in the round, advance it as far as the workflow permits, propagate and
   record every result, re-chart, report the frontier, and stop. Tell it the session
   is unattended: nothing it receives carries a human verdict or adoption, so
   determined human-owned decisions, residual questions, and admission candidates
   stay open on the frontier.
5. Wait for the worker to finish, then treat the tracker—not its conversation—as the
   result. Reload durable state and repeat from step 1 without asking the human to
   continue.

Run worker sessions serially because each propagation can change the next frontier.
A worker may still delegate bounded legwork under `SKILL.md`; every delegate works
only its selected ticket. A generic continuation, goal wake-up, or worker report is
coordination, never a human verdict.
