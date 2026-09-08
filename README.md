# through-line v2

**Work together without starting over in judgment.**

Through-line helps an agent discover the commitments relevant to everyday work,
apply them to its choices, and discuss consequential gaps or counterexamples with
the human. Useful judgment survives the session that produced it. The collection
stays small because each addition must prevent a plausible future misinterpretation.

This is a fresh-start draft. It replaces v1's substantial-change coordination model
with a practice that fits ordinary engineering, product, and operating work.

## What it feels like

You ask for managers to correct recorded times. The agent notices that overwriting
an observation and recording a later correction mean different things. It explains
the tradeoff and asks whether the distinction should govern future cases or just this
workflow. You adopt a bounded commitment, with a contrasting example that tests its
scope.

A new session later handles an export. It discovers the observation/correction
commitment through the affected meaning, even though the task concerns a different
part of the system. It explains the consequence for the export and checks that
consequence. If the reporting policy is still undecided, it asks that question
rather than inventing an answer from the principle.

A routine typo fix finishes without an interview, a new principle, or a knowledge-base
cleanup. Most work should not grow the collection. These are fictional examples of
the intended behavior, not reports of evaluated performance.

## The practice

**Discover selectively.** Start at a small workspace index, read the few always-consult
records, and follow applicability descriptions into relevant scoped commitments.
Read supporting cases when they can change the current choice. Stop when enough is
understood to act responsibly.

**Discuss real choices.** Prompt discussion when a consequential choice lacks
direction, a correction exposes reusable judgment, or existing commitments no longer
fit. Help the human form a principle by testing a concrete alternative and boundary.
Silence and one-off decisions do not establish standing doctrine.

**Apply and revise.** Make principles affect proposals, implementations, and reviews.
Reference the particular consequence instead of announcing compliance. When a human
changes a commitment, inspect known and likely consumers, apply authorized changes,
and distinguish confirmed impacts from areas not investigated.

## A small corpus, progressively discovered

The installed skill contains the practice. Each workspace owns its knowledge. Reuse
existing authoritative locations; when a new collection is needed, the default is
`principles/index.md` with focused records underneath it. Longer decision evidence
stays in its existing home.

A discovery entry says when a concern matters, not merely what a file is called.
An adopted record states the commitment, its tradeoff, scope, boundary example, and
human source. Observations and tentative explanations remain useful without being
promoted into policy. Prefer amending or consolidating a record to adding overlapping
ones. Do not build a monolithic principles file, duplicate canon, or candidate backlog.

No corpus is required to begin work. No principle is required to finish it.

## Install and activate

Follow [HOSTS.md](HOSTS.md) for local installation and the small workspace instruction
for `AGENTS.md` or `CLAUDE.md`. For draft review, use the extracted skill folder or
branch `v2/shared-judgment` after publication. Installing the draft does not change
`main`.

Automatic invocation is enabled in the package. The workspace instruction also directs
ordinary work through the skill's entry point without loading the corpus at startup.
This draft does not install hooks or claim deterministic activation. Explicit
invocation remains available as `$through-line` or `/through-line` for diagnosis.

## Scope and authority

V2 has no routes, charters, task graph, supervisor, tracker dependency, integration refs,
or special execution process. It operates alongside the tools doing the task, including
non-code work. It neither claims to encode a complete theory of a system nor requires
comprehensive understanding before action.

A human adopts commitments. The agent may propose and apply them within scope.
Neither a principle nor automatic invocation authorizes publication, deployment,
messages, spending, destructive actions, or changes to host permissions.

## Files and checks

[SKILL.md](SKILL.md) is the compact operating entry point. Load focused guides only
when needed: [discovery](DISCOVER.md), [discussion](DISCUSS.md), and
[records](RECORDS.md). [DESIGN.md](DESIGN.md) explains the sources and design choices.

Run the dependency-free package checks with Python 3.10 or later:

```sh
python3 -m unittest discover -s tests -v
```

Or use `just check` when `just` is installed. These checks validate metadata, local
links, loading budgets, and evaluation fixtures. They do not establish model behavior.
[The evaluation protocol](evals/README.md) covers automatic activation, selective
retrieval, contextual application, discussion, restraint, and revision in fresh sessions.

V1 remains in Git history. Existing routes and workspace knowledge are not migrated
or modified by installing v2.
