# Supervise

Use this path when the human asks an existing map to **advance unattended**. The
supervisor schedules fresh [Work](./WORK.md) sessions; durable tracker state carries
the effort between them.

## Loop

1. Refresh the map, principles, decision rights, frontier, and claims.
2. Stop when the map is complete or progress needs human judgment, a doctrine or
   scope change, an external unblock, or ownership resolution. Report that frontier.
3. Otherwise dispatch a `/research` subagent for each open, unclaimed research
   ticket — research does not consume a session's unit — and choose one non-human
   unit: a builder-owned round or decision, a prototype ticket, or an in-scope task.
4. Start a fresh Work session with the map reference, exact selection, reaching
   premises, useful references, checks, and any execution receipts. Do not pass the
   supervisor's conversation. Dispatch at the host's default reasoning effort;
   reserve elevated effort for a named risk. Require one final receipt, blocker, or
   checkpoint as inter-agent communication; omit progress chatter.
5. Wait once through the host's completion mechanism. On a result, reload durable
   state and repeat. On a timed-wait wake without a durable result, end the turn;
   resume from the worker's later result or a continuation. A dead worker leaves a
   live claim: recover it from its receipts, inspecting the agent tree only when the
   claim does not identify its owner.

Run workers serially because propagation can change the next frontier. A worker
report or generic continuation coordinates the effort; it never supplies a human
verdict.

Record and propagate an explicit human verdict directly, or resume the decision
worker. Recording a verdict is not a separate Work unit: never dispatch a record-only
worker.

Supervision is event-driven. User-visible updates are limited to unit dispatch, a
material finding or scope change, and completion, checkpoint, blocker, or human
frontier. Host-required status updates stay terse and report the active stage, never
unchanged worker, branch, test, or review state.
