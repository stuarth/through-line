# Execution

Use this branch only for a task that lands work in a repository. The Work session is
the coordinator; durable **receipts**, not conversation, carry progress between
sessions. Store receipts on the task ticket or in one artifact linked from it.

## Resume

Load the exact ticket and linked receipts. Start at the first missing or invalid
receipt and retain earlier valid receipts. Commits must remain reachable and mapped
premises must still hold; each gate below defines what else invalidates its receipt.
A review receipt is valid only for its named candidate range and recorded targeted
extensions; a candidate produced by another path has no review receipt.

A checkpoint records the receipts, the first invalid gate, and the next exact packet.
Resuming a checkpoint continues that gate. It does not replay orientation, prior
implementation, or a completed whole-candidate review.

## 1. Packet receipt

Re-check atomicity. Make an independently landable and reviewable slice its own task;
use packets only when partial implementation cannot resolve the ticket.

Write one compact packet containing:

- outcome and stop condition;
- acceptance criteria and named premises advanced;
- exact code, documentation, test, and constraint entry points;
- focused checks and explicit exclusions; and
- effort: the host default unless one named uncertainty requires more.

For persistent data work, include the governing migrations or constraints and an
isolated verification database command. The packet is complete when a leaf can act
from its named entry points without route discovery or architectural judgment.
Resolve a missing fact with bounded coordinator search, a research ticket, or a
split before dispatch.

## 2. Candidate receipt

Dispatch a fresh leaf with the packet and [IMPLEMENT.md](./IMPLEMENT.md). Use the host's
default capable reasoning level; raise it only for the packet's named uncertainty.
The coordinator remains on receipts and durable state while the leaf owns its files.

Persist the returned candidate receipt:

- base and candidate commits;
- changed files and acceptance mapping;
- focused check command, status, and candidate commit; and
- any gap and the exact entry point needed to close it.

A gap produces a revised packet, not a widened executor. The candidate gate is
complete when every acceptance criterion and reachable premise maps to implementation
and to focused, review-mapped, or deferred verification evidence at fixed commits.

## 3. Review receipt

When no valid review receipt exists, dispatch one fresh integrated leaf with the
ticket, candidate receipt, relevant premises, and [REVIEW.md](./REVIEW.md). Add one
specialist only when the receipt names a risk the integrated reviewer cannot judge.

Persist its review receipt:

- candidate range and decision;
- material findings tied to acceptance, a named premise, or an evidenced correctness,
  security, or data-integrity invariant;
- risks actually covered and checks run; and
- direct testing gaps that remain.

An existing receipt with unresolved findings resumes at Correction. A fresh session
receives that receipt and the correction range for a targeted pass; it does not repeat
the whole-candidate review.

## 4. Correction

Aggregate the review receipt's findings by root cause and write the smallest complete
packet for the next cause. Dispatch a fresh executor, update the candidate receipt,
and invalidate only checks or premises touched by its commits.

Return the correction range to the same reviewer for a targeted pass. When that
session cannot resume, dispatch a fresh reviewer with the prior review receipt and
correction range. The pass adjudicates the recorded findings and direct regressions
in touched code. Adjacent hardening becomes a later ticket unless it falsifies a
mapped acceptance criterion or premise, or violates a material correctness, security,
or data-integrity invariant.

A correction that materially changes architecture, authorization, persistence,
destructive behavior, or the candidate's overall shape invalidates the whole review
receipt. After two targeted passes with findings, record a checkpoint and stop the
Work session so the next session resumes from the receipts with fresh context.

## 5. Verification receipt

After a clean review receipt, run every deferred check and the full suite once. Keep
complete output outside conversation and record command, commit, status, duration,
and one-line result. The verification receipt is valid only for the mapped final
candidate.

A behavioral failure returns to Correction. When the only proposed fix changes an
expected output or fixture for already-reviewed behavior, make a narrow test-only
correction. Give its fixed range and failed check to targeted Review; inspect only
whether the expectation matches mapped behavior without weakening the oracle. Record
a clean pass as a targeted extension, then rerun the full suite.

## 6. Record

Resolve the ticket only when the candidate, clean review, and verification receipts
reference the same final candidate. Record the commits and evidence, propagate the
result through the map, reconcile the tracker, validate it, and stop after this
ticket's cascade.
