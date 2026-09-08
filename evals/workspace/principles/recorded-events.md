# Preserve accepted observations
Status: adopted
Authority: Fictional workspace owner; [decision B](../decisions/adoptions.md#decision-b).

## Commitment

Keep an accepted observation distinct from any later correction. A correction records
a new judgment without replacing the observation it corrects. Consumers must make
clear which interpretation they use.

## Why this choice

We accept additional representation and consumer decisions so a reviewer can distinguish
what was recorded from what someone later concluded. In-place replacement is simpler
but erases that distinction.

## Applies when

Changing acceptance, editing, reconciliation, reporting, or export of observations,
including device events and accepted operator reports. Accepted means admitted as an
observation in the system of record, not merely present in an import buffer.

## Boundary

Repairing a parser's staging value before acceptance does not revise an accepted
observation. Fixing display formatting does not necessarily change an observation's
meaning. This principle does not decide which interpretation each report must use.

## Evidence

[Decision B](../decisions/adoptions.md#decision-b) captures the originating choice and
staging counterexample. Reporting behavior still needs a contextual decision.
