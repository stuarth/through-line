# Implement

Act as a leaf for one packet from a through-line coordinator. The packet is the route;
return a candidate receipt or a gap receipt.

## Packet gate

Confirm the packet names its outcome, acceptance mapping, premises, owned entry
points, constraints, focused checks, exclusions, and stop condition. For persistent
data work it also names the governing schema boundary and isolated verification
command.

When a material boundary is missing, return the smallest gap and its required entry
point before editing. The gate is complete when the work can proceed from named local
entry points without a map, closed-ticket history, or a new product or architecture
decision.

## Implement

1. Inspect the named entry points and the local code needed to change them. Search
   before bounded reads and keep verbose command output outside conversation.
2. Implement the packet and run its focused checks. A separable slice or new judgment
   produces a gap receipt at the packet boundary.
3. Commit only the packet's files at a fixed candidate commit.

Return this candidate receipt:

- base and candidate commits;
- changed-file summary;
- acceptance mapping;
- check command and status; and
- unresolved gap, if any.

Work locally as one leaf. The coordinator owns further packets, review, full-suite
verification, propagation, and tracker state.
