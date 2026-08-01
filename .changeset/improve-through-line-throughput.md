---
"mattpocock-skills": patch
---

Make `/through-line` task execution converge without replaying long-lived review
contexts. Review candidates now account for every acceptance criterion, each
candidate gets a fresh integrated review, repeated findings trigger root-cause
diagnosis or a checkpoint, verification reruns stay scoped to affected checks,
full-suite output stays bounded, and unattended supervision reports only real state
transitions.
