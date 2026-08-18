# Supervise

Use this path when the human asks an existing map to **advance unattended**. The
supervisor schedules fresh [Work](./WORK.md) sessions; durable tracker state carries
the effort between them. Keep advancing until the map resolves or the frontier
reaches a stop condition in step 2. A worker completion advances the loop; it does
not complete supervision.

## Loop

1. Refresh the map, principles, decision rights, frontier, and claims.
   If this supervision effort already owns a live Work claim, resume its wait at
   step 5; do not dispatch another worker.
2. When the map is open and no unresolved destination ticket remains, ensure one
   unresolved **Final map closure** task exists and select it. It uses ordinary claim,
   blocker, and checkpoint mechanics; review findings reopen affected roots or create
   one integrated outcome ticket when no root owns them.
   Otherwise stop when the map is resolved or progress needs human judgment, a
   doctrine or scope change, an external unblock, or ownership resolution. Report
   that frontier.
3. Otherwise dispatch a `/research` subagent for each open, unclaimed research
   ticket through [receipt-only coordination](./SKILL.md#coordination) — research
   does not consume a session's unit — and choose one non-human unit: a builder-owned
   round or decision, a prototype ticket, or an in-scope task. Select a reopened root
   next when its current [Convergence verdict](./WORK.md#falsify) is **continue**,
   **re-slice**, or **redesign**. A **defer** verdict yields to the independent
   frontier; if none remains, stop at that verdict.
4. Start a fresh Work session with [WORK.md](./WORK.md) from an explicit packet: map
   reference, exact selection, reaching premises, useful references, checks, and
   execution receipts. Use the host's no-history option (`fork_turns: none` in
   Codex); never pass the supervisor's conversation. Dispatch at the host's default
   reasoning effort and reserve elevated effort for a named risk. Follow
   [receipt-only coordination](./SKILL.md#coordination). A terminal receipt retires
   that worker—the next unit always gets a new Work session.
5. Keep the supervisor turn active under receipt-only coordination until the selected
   receipt arrives, then reload durable state and repeat from step 1. A failed worker
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

The supervisor returns a final answer only at a step 2 stop condition. A live worker
or expired wait is not a stop condition. A host without a completion-aware wait does
not support **advance unattended**; report that before dispatch instead of silently
degrading to one unit per user continuation.
