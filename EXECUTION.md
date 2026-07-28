# Execution

**One slice, one session.** An execution session owns one implementation ticket
and reconstructs its context from the map and repository artifacts.

## Slice

Claim a ticket only when it names one outcome, the included behavior and paths,
explicit exclusions, acceptance checks, and the fixed point for review.
Re-chart a ticket whose outcome cannot be implemented and reviewed within one
session.

If a slice outgrows its session mid-flight, stop. Keep what is integrated and
verified, re-chart the remainder as new tickets, and handoff.

## Ownership

Establish one writer for every overlapping path before editing. When another
session owns overlapping uncommitted work, record that owner and the committed
or released state that unblocks this ticket, unclaim it, and handoff.

End the session. Resume in a fresh session only after the recorded condition
holds; never spawn a worker to wait or poll for it.

## Delegation

Brief each worker from the ticket, the map, the applicable principles and
policies, and the fixed point. Keep one worker to one role on one slice:
corrections to an artifact return to the worker that made it; a different role
or ticket gets a fresh worker. Parallel workers own explicitly independent
artifacts with a named integration order.

## Quality gate

The root driver integrates the slice, runs the acceptance checks and every
practical repository-required check, then invokes `/code-review` once against
the ticket's fixed point. Its Standards and Spec reviewers remain independent.

Resolve every verified finding before closing the ticket and rerun affected
checks. Return corrections to the reviewer that raised them for one verification
pass; never spawn a new general reviewer. If a correction materially expands
the slice, re-chart the remainder as a new ticket. Add a reviewer only for a
distinct named risk — migration safety, security, or specialized UX.

Close the ticket with implementation, verification, and review evidence, then
handoff.
