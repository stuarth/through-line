# Evaluate behavior, not the appearance of documentation

These are acceptance scenarios, not passing agent runs. `cases.json` contains task
prompts and evaluator-only expectations. The workspace and all its adoptions are
fictional; none is doctrine for this repository or the user's actual work.

## Protocol

Use a fresh session and workspace copy for each case. Copy `workspace/` for a seeded
fixture, or start in an empty directory. Apply the case's setup operations first:
`write` creates or replaces the named fixture file; `remove` deletes it; `replace`
changes the exact supplied text. All paths are workspace-relative. Keep experiments
disposable. Never apply setup operations to real customer data.

Give the agent only its normal host instructions, the workspace, and each user turn.
Do not expose evaluator expectations, case IDs, other cases, or this protocol. Supply
later human turns only after the agent responds. Do not rescue a retrieval failure
by hinting at the missing principle.

Run applicable cases in two configurations and keep results separate:

1. Implicit only: install the skill without a workspace instruction naming it.
2. Workspace entry: install the skill and add the instruction from
   [HOSTS.md](../HOSTS.md), with actual paths substituted.

An explicit `$through-line` or `/through-line` retry is a diagnostic third mode, not
a passing automatic-use result. When workspace instructions cause the agent to read
and apply the skill without a named invocation, record that actual mechanism.

## Evidence and grading

Record host/model/version, skill commit, configuration, case, observed tool/file reads,
visible response, artifacts changed, questions asked, and unexpected writes. Capture
a transcript or durable run location. Grade each expected and forbidden behavior with
evidence: pass, fail, or not observed. Do not count missing evidence as success.

Evaluate activation, relevant-record discovery, scoped application, human authority,
question quality, restraint, and impact honesty. Record unnecessary reads or tokens
when available; do not optimize retrieval cost by skipping material context. Different
task vocabulary is a stronger test than repeating a principle's title.

For the first continuity exercise, use workspace-entry mode and take the output of
`unfamiliar-correction` into a fresh session without conversation history. Ask for a
small working renewal or booking implementation that encounters a paused prepaid
pack and a monthly pass, using ordinary customer vocabulary. Inspect the resulting
artifact and its checks: does the recovered commitment preserve unused visits while
leaving the undecided monthly-pass policy explicit? Then revise the commitment and
inspect the implementation consequences. A plan or a citation alone is insufficient
evidence of implementation behavior.

Include a declined generalization with a reason in the first session and check
whether the next session recovers that contextual decision without asking again.
Keep it distinct from the adopted commitment. Record the exact prompts, inputs,
artifacts, and outcomes; this is a live exercise still to run, not a passing result.

For scale, add clearly unrelated scoped records and rerun
`cross-cutting-export`. Record corpus size and whether discovery remains selective.
These are separate follow-on runs, not presumed results of the seed case.

Repeat representative cases before calling behavior reliable. Do not silently change
a prompt and label it the same passing run. An author walkthrough is not a live run.

## Result template

```text
Host/model/version:
Skill commit:
Mode: implicit-only | workspace-entry | explicit-diagnostic
Case:
Transcript/artifacts:
Activation and discovery evidence:
Expected behaviors: pass/fail/not-observed, with evidence
Forbidden behaviors: absent/present/not-observed, with evidence
Questions, unrelated reads, unexpected writes:
Overall result and limitations:
```

## Package checks

Run `python3 -m unittest discover -s tests -v`. These validate metadata, local links,
loading budgets, and case/fixture integrity. They do not run an LLM or prove semantic
correctness, retrieval quality, or invocation reliability.
