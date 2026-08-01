# Execution

Use this branch for repository work. The Work session implements its task directly,
so discovery is paid once, in the session that edits. Compact receipts carry
progress; store them on the task ticket or in one linked artifact.

## Resume

Load the ticket and its receipts, then continue from the first unfinished or invalid
stage. Keep earlier work when its commits still exist and later edits have not changed
what it established. A checkpoint names that stage and the next plan so resumption
does not repeat orientation, implementation, or review.

## Plan

Keep the task atomic: an independently landable result deserves its own ticket.

Before editing, record a compact plan on the ticket: the outcome, acceptance
criteria, reaching premises, exact entry points and constraints, focused checks,
exclusions, and stop condition. For persistent data work, include the governing
schema and an isolated database check. The plan is ready when implementation can
proceed from those entry points without a new product or architecture decision.

Delegate only work disjoint enough to run in parallel: give each fresh leaf its own
plan as a packet with [IMPLEMENT.md](./IMPLEMENT.md), at the host's default
reasoning effort unless one named uncertainty warrants more. A returned gap sharpens
the packet; it does not widen the leaf's assignment. When a delegated check fails,
send the leaf the failing evidence — diagnosis belongs to the leaf, and the
coordinator's context stays lean.

## Candidate

Implement the plan — directly, or by landing the delegated packets' receipts — and
run the focused checks, committing only the plan's files. Record the base and
candidate commits, changed files, acceptance mapping, focused checks, and any
remaining gap.
The candidate is ready for review when every criterion and reaching premise maps to
implementation and a verification path: green focused evidence, a review check, or a
named deferred check.

## Review and correction

Give one fresh integrated reviewer the ticket, premises, candidate receipt, and
[REVIEW.md](./REVIEW.md). Add a specialist only for a named risk the reviewer cannot
judge. Record the candidate range, decision, material findings, checks, and gaps.

Fix related findings together as the smallest complete correction. Return the
correction range and prior receipt to the same reviewer, or a fresh reviewer when
resumption is unavailable, for a targeted pass. Preserve unaffected review coverage.
Start over only when the correction materially changes the candidate's architecture,
authority, persistence, destructive behavior, or overall shape.

Keep adjacent hardening out of the correction loop. If the loop stops converging,
checkpoint it for a fresh Work session rather than accumulating more context.

## Verify and record

After review is clean, run deferred checks and the full suite once. Keep full output
outside conversation and record only the command, candidate commit, status, duration,
and useful failure excerpt. An edit returns to correction; afterward rerun the checks
that edit invalidated and the full suite.

Resolve the ticket when candidate, review, and verification receipts describe the
same final work. Record the commits and evidence, propagate through the map, reconcile
the tracker, validate it, and stop after this ticket's cascade.
