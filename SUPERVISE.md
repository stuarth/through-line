# Supervise

Use this path when the human asks an existing map to **advance unattended**. The
supervisor schedules fresh [Work](./WORK.md) sessions; durable tracker state carries
the effort between them.

## Loop

1. Refresh the map, principles, decision rights, frontier, and claims.
2. Stop when the map is complete or progress needs human judgment, a doctrine or
   scope change, an external unblock, or ownership resolution. Report that frontier.
3. Otherwise choose one non-human unit: a builder-owned round or decision, a
   research or prototype ticket, or an in-scope task.
4. Start a fresh Work session with the map reference, exact selection, reaching
   premises, useful references, checks, and any execution receipts. Do not pass the
   supervisor's conversation. Dispatch at the host's default reasoning effort;
   reserve elevated effort for a named risk.
5. Wait for completion without polling. When the worker resolves, blocks, or
   checkpoints, reload durable state and repeat. A worker that dies mid-unit
   leaves a live claim: dispatch a fresh session naming that claim to resume
   from its receipts.

Run workers serially because propagation can change the next frontier. A worker
report or generic continuation coordinates the effort; it never supplies a human
verdict.

If the host cannot wait without repeatedly waking the model, dispatch once and stop
supervision rather than spending tokens narrating unchanged state.
