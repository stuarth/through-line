# Working notes

These are observations and tentative explanations, not adopted principles.

## Export rounding

Three inspected examples suggest an existing export rounds each entry before summing.
Other paths are unverified. The reason is unknown; it could be an old provider limit.
This observation does not establish a required rounding policy.

## Earlier provider choice

An earlier integration used short batches because its provider imposed a small
request limit. That provider is no longer used. The decision was contextual; nobody
adopted a general preference for small batches.

## Candidate raised by an agent

"Favor maintainability" was suggested as a principle. No human adopted it, and no
concrete alternative or boundary was identified.
