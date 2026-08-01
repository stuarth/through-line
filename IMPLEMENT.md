# Implement

Implement one packet as a leaf. The packet is the route; do not load the through-line
map or coordinate more work.

If a missing boundary prevents an aligned implementation, return the smallest useful
gap before editing. Otherwise inspect the named entry points, make the change, run the
focused checks, and commit only the packet's files.

Return a compact receipt:

- base and candidate commits;
- changed-file summary;
- acceptance mapping;
- check command and result; and
- any unresolved gap.

The coordinator owns further packets, review, full-suite verification, propagation,
and tracker state.
