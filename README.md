# through-line

Work together without starting over in judgment.

Through-line is an agent skill that preserves the reasoning behind product and
engineering decisions and brings it into later work. It helps people and agents
develop shared principles as they work, then uses those principles to guide
related changes across sessions.

## Why now

Agents make it easier to change several parts of a system in separate sessions.
Each session has the code in front of it, but may lack the reasoning behind an
earlier decision. A temporary workaround can become the precedent for a new feature.
Tests can reinforce it. Over time, the product acquires behavior that nobody chose
as policy.

Code and conversation history can explain what happened. They do not always explain
which decisions still apply, why they were made, or which cases they cover.
As the volume of agent-written changes grows, those gaps affect more of the product.
Through-line makes that judgment available where the next decision happens.

## How it works

Through-line runs alongside ordinary work. The agent looks for relevant principles
and follows links to the records that explain them. When a task exposes an unresolved
tradeoff, it raises that choice for discussion. The discussion can produce a local
decision or a principle for future work. The human decides which.

A principle records a commitment, the reason for choosing it over an alternative,
and the limits of its application. Each principle must rule out a plausible future
mistake or disagreement. Observed behavior and provisional explanations remain
distinct from adopted policy.

For example, a makerspace might sell both prepaid workshop visits and monthly
access. Reusing calendar logic for both could make a pause consume prepaid visits.
A decision to preserve unused visits would affect renewals as well as booking.
Recording why that decision applies to prepaid visits also leaves the monthly
access policy open for a separate decision.

A small index describes when a principle matters and links to its authoritative
record. An agent working on renewals can find the prepaid-visit decision even if
it originated in a booking task. The agent loads the relevant context without
reading the entire collection.

In the makerspace example, the renewal change would preserve unused visits, with
a test for that behavior. If a later case challenges the principle, the agent brings
the conflict back for discussion. Revising a principle includes examining the work
affected by the change.

Existing architecture decision records, domain documentation, and policies can
remain in their current locations. Through-line links to them. New records default
to `principles/index.md` and focused files in the workspace. The skill calls for
discussion when a consequential choice needs it; routine work does not require a
new principle or a review of the collection.

## Heritage

[Peter Naur's *Programming as Theory Building*](https://pages.cs.wisc.edu/~remzi/Naur.pdf)
describes programming knowledge as an understanding of how a program relates to the
world, why it is constructed as it is, and how to respond to new demands. Through-line
builds on that account of judgment. Its records help a later worker recover the
reasoning relevant to a change, while recognizing Naur's argument that documentation
cannot capture the whole understanding.

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
