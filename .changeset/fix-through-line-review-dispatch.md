---
"mattpocock-skills": patch
---

Make `/through-line` task execution converge on fixed review candidates. Task
tickets now split when parts can land or be verified independently, reviewers judge
a stable diff in fresh context, findings are fixed as a batch, re-review follows the
affected risks, and full-suite verification waits for a clean review.
