# through-line

Work together without starting over in judgment.

Through-line is an agent skill for developing shared principles during everyday
work and applying them in later sessions.

Experienced colleagues build an understanding of the business over time. They
remember why apparently similar cases need different treatment and which shortcuts
were temporary. That understanding informs decisions nobody thought to spell out
in the next task.

A coding agent is a worker on its first day, every day. Each fresh session builds
its understanding from the context available to it. Without the reasoning behind
previous decisions, it has to infer intent from a prompt and the behavior of the
code.

A workaround can then become the model for a new feature. The next session sees
both implementations and treats the pattern as deliberate. Each change can carry
an earlier guess further into the product, until you have to explain the same
distinction again or undo behavior you never intended.

Through-line records those decisions and the reasoning behind them for later
sessions. As new work exposes unresolved choices, you and the agent develop that
understanding further.

## How it works

During substantive work, the agent follows a small discovery index to relevant
principles and their reasoning. Entries describe when a principle matters, so a
renewal task can find a decision first made about booking. Existing documentation
can remain the authoritative source.

When a consequential choice needs discussion, the agent recommends an approach and
helps establish how far its reasoning applies. You decide whether it becomes a
principle for future work. A principle earns a place by preventing a plausible
future mistake or disagreement; most tasks add nothing.

The resulting record holds the commitment, reason, scope, and source decision.
The agent applies it in later work and reopens the discussion when a new case
challenges it. Changing a principle includes examining the work it affects.

## Installation

Install with the [skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills@latest add stuarth/through-line
```

Update with `npx skills update through-line`.

Add a workspace entry to `AGENTS.md` for Codex or `CLAUDE.md` for Claude Code,
using the location of the workspace's principles:

```markdown
## Through-line

Apply the installed through-line skill during substantive work in this workspace.
Read its SKILL.md entry point and revisit discovery when the task's scope changes.
Principles entry: principles/index.md.
```

The skill supports automatic invocation and the explicit commands `$through-line`
in Codex and `/through-line` in Claude Code.

[SKILL.md](SKILL.md) contains the operating instructions.
