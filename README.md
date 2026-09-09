# through-line

Work together without starting over in judgment.

Through-line is an agent skill for developing shared principles during everyday
work and applying them in later sessions. It preserves the reasoning behind
product and engineering decisions so related changes can build on it.

## Why now

Agents make it easier to change several parts of a system in separate sessions.
Each session can read the code, but may lack the reasoning behind an earlier
decision. A temporary workaround can become the precedent for a new feature, then
acquire tests and dependencies. The product gains behavior nobody chose as policy.

For example, a makerspace might sell prepaid visits alongside monthly access.
Reusing calendar logic could make a pause consume prepaid visits. Deciding to
preserve unused visits establishes a rule for booking and renewals, while leaving
the monthly access policy open. The code alone may not explain that distinction.

Through-line records the decision and its limits, and directs the agent to consult
it when related work comes up.

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

## Heritage

[Peter Naur's *Programming as Theory Building*](https://pages.cs.wisc.edu/~remzi/Naur.pdf)
describes programming knowledge as understanding how a program relates to the world,
why it is constructed as it is, and how to respond to new demands. Through-line's
records help later workers recover the reasoning relevant to a change.

## Installation

Clone the repository:

```sh
git clone https://github.com/stuarth/through-line.git ~/dev/through-line
```

For Codex:

```sh
mkdir -p ~/.agents/skills
ln -s ~/dev/through-line ~/.agents/skills/through-line
```

For Claude Code:

```sh
mkdir -p ~/.claude/skills
ln -s ~/dev/through-line ~/.claude/skills/through-line
```

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
