# through-line

**Work together without starting over in judgment.**

Consider a makerspace that sells prepaid workshop visits alongside monthly access.
Its pause flow consumes a prepaid visit each week because someone reused calendar
logic. A later agent working on renewals could follow that behavior as though it
were intentional policy. Reading the code accurately would still leave the business
question unanswered: should a pause use up something the customer already paid for?

Through-line is a skill for carrying that judgment through everyday engineering,
product, and operating work. It helps an agent find relevant commitments, use them
in its choices, and start a focused discussion when the current work exposes a gap.
The aim is for one well-examined decision to improve many later changes, while
keeping its conclusions open to challenge.

## Why now

Agents can shorten the path from a request to a proposed implementation. Establishing
that it is correct still takes judgment. With separate sessions handling different
parts of a system, each can produce a plausible change from the context it has.
The reasoning that informed one session does not automatically inform the next.

Successive edits can spread a mistaken interpretation before anyone questions its
basis. A workaround becomes a pattern; tests preserve it; later features depend on
it. The cost is more than explaining yourself again. A product can acquire rules
that nobody deliberately chose, making them harder to change later.

Human teams face this too, and design records, review, and people who remember help.
Agents can use those resources and their own memory. Remembering a workaround,
however, does not establish that anyone adopted it as policy. As producing changes
gets easier, carrying the reasons and qualifications behind them deserves deliberate
attention.

## What it should feel like

In the makerspace example, Through-line should bring the distinction between prepaid
visits and time-based access into discussion. You might decide that a pause must
preserve unused prepaid visits, with monthly access explicitly outside that rule.
The record carries your decision, its reason, and that boundary.

A later session changing booking should discover the commitment, preserve unused
visits, and check the result. It should leave the monthly-pass question open. If a
new case challenges the commitment, it should bring the evidence back to you. A
routine typo fix should finish without a principles discussion. This illustrates
the intended experience; live reliability remains to be evaluated.

## Core ideas

**Keep commitments that change a choice.** A principle earns its place by preventing
a plausible future mistake or disagreement. Preserve the alternative it rules out,
the reason for choosing it, its scope, and a contrasting case where it stops.
Most tasks should add nothing to the collection.

**Develop judgment through real work.** Discussion helps form principles when a
concrete tradeoff needs deciding. The agent can recommend and challenge; the human
adopts the commitment. A one-off choice, an observed behavior, and a working
explanation remain useful without becoming policy. A new case can expose a weak
premise or justify a revision.

**Discover by meaning.** A small index describes when a concern matters and points
to its authoritative record. A principle about prepaid visits may affect booking
and renewals in different directories. Read the relevant records and their
supporting cases, then stop when the present choice has enough context to proceed.

**Make the consequence visible.** A commitment should change a proposal,
implementation, or review, with evidence appropriate to the choice. When the
commitment changes, inspect its known and likely consequences and distinguish what
was checked from what remains unknown. The prose still requires interpretation;
that interpretation should be open to inspection and correction.

Existing architecture decision records, domain documentation, and policies can stay
authoritative in their established locations. Through-line adds the practice of
consulting, applying, and questioning that judgment during work. The workspace owns
the records; the installed skill supplies the practice. A new collection defaults
to `principles/index.md` and focused records. None is required to begin a task.

## Where the ideas come from

[Peter Naur's *Programming as Theory Building*](https://pages.cs.wisc.edu/~remzi/Naur.pdf)
describes programming knowledge as an understanding of how a program relates to the
world, why it is constructed as it is, and how to respond to new demands. He also
argues that this knowledge exceeds what rules and documentation can express.
Through-line's records support the reconstruction of relevant judgment; they cannot
contain the whole understanding.

[Sean Goedecke's *In defense of not understanding your codebase*](https://www.seangoedecke.com/in-defense-of-not-understanding-your-codebase/)
challenges Naur's pessimism about recovering lost understanding and argues for useful
work with partial understanding. Through-line takes a practical limit from that:
recover what the current decision needs and leave unrelated gaps alone.

An Inferal manifesto by Through-line's author, *Edit the business, not the software*,
explores directly editable business rules with governed consequences. It contributes
the demand that changing a commitment should visibly change the work. Through-line
applies that idea through an interpreting agent; its principles are not executable
business rules.

Through-line brings these influences together. [DESIGN.md](DESIGN.md) describes the
author-supplied manifesto and explains the distinctions and design choices.

## Try it

Follow [HOSTS.md](HOSTS.md) to install the skill for Codex or Claude Code and add the
small workspace instruction to `AGENTS.md` or `CLAUDE.md`. The intended experience
is automatic attention during ordinary work, with discussion only when it helps.
Explicit invocation is available as `$through-line` or `/through-line`.

Start with one real task where a business distinction matters. Then try a related
change in a fresh session without naming the principle. Check whether the agent
finds the relevant judgment and makes an appropriate choice.

## Status and checks

This is a draft. Package checks pass; reliable invocation, useful discussion, and
selective retrieval across fresh sessions remain to be tested. Automatic invocation
is enabled but not deterministically enforced. See [the evaluation protocol](evals/README.md).

V2 replaces v1's route coordination and works alongside existing execution tools and
authorization rules. V1 remains in Git history; existing workspace records are not
automatically migrated.

Run the dependency-free checks with Python 3.10 or later:

```sh
python3 -m unittest discover -s tests -v
```

Or run `just check`. These checks cover package integrity and fixtures, not model
behavior. The operating entry point is [SKILL.md](SKILL.md), with focused guides for
[discovery](DISCOVER.md), [discussion](DISCUSS.md), and [records](RECORDS.md).
