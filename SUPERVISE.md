# Supervise

Use this path when the human asks an existing map to **advance unattended**. The
supervisor schedules fresh [Work](./WORK.md) sessions; durable tracker state carries
the effort between them.

## Loop

1. Refresh the map, principles, decision rights, frontier, and claims.
2. When the map is open and no unresolved destination ticket remains, ensure one
   unresolved **Final map closure** task exists and select it. It uses ordinary claim,
   blocker, and checkpoint mechanics; review findings block it on correction tickets.
   Otherwise stop when the map is resolved or progress needs human judgment, a
   doctrine or scope change, an external unblock, or ownership resolution. Report
   that frontier.
3. Otherwise dispatch a `/research` subagent for each open, unclaimed research
   ticket — research does not consume a session's unit — and choose one non-human
   unit: a builder-owned round or decision, a prototype ticket, or an in-scope task.
4. Start a fresh Work session with [WORK.md](./WORK.md) from an explicit packet: map
   reference, exact selection, reaching premises, useful references, checks, and
   execution receipts. Use the host's no-history option (`fork_turns: none` in
   Codex); never pass the supervisor's conversation. Dispatch at the host's default
   reasoning effort and reserve elevated effort for a named risk. Require one
   terminal receipt, blocker, or checkpoint as inter-agent communication; omit
   progress chatter. A terminal receipt retires that worker—the next unit always
   gets a new Work session.
5. Classify the host's completion mechanism once. If worker completion wakes the
   supervisor without a model timeout, wait for that event. On a timeout-only host,
   state that continuous unattended advancement conflicts with token-safe waiting,
   dispatch one unit, make one bounded wait, and end the turn if it expires. Resume
   from the later receipt or a continuation; never loop on timed waits. A dead worker
   leaves a live claim: recover it from its receipts, inspecting the agent tree only
   when the claim does not identify its owner.

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
