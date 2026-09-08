# Develop judgment through concrete choices

## Earn the interruption

Discuss when the answer could materially change the current work or prevent a
credible future misinterpretation. Useful signals include a consequential tradeoff
with no settled direction, a user correction with wider implications, conflicting
commitments, and a counterexample to an adopted principle.

Do not ask for a philosophy interview, manufacture a principle for every task, repeat
a settled question, or use discussion to avoid ordinary judgment. Do not repeatedly
resurface a declined candidate without new evidence. An absent principles collection
is not itself a problem to solve.

## Make the question do work

Ground it in the user's actual task. State the choice and plausible alternative,
your recommendation and main downside, and the boundary that needs a human decision.
Prefer one focused question over a bundle of speculative policies.

For example:

> Replacing this timestamp would lose the distinction between the device's observation
> and the manager's correction. I recommend keeping both, at the cost of making
> consumers choose which interpretation they need. Should that distinction apply to
> recorded events generally, or only to this workflow?

Use a contrasting case to test the proposed scope, such as correcting a parser's
staging value before an event is accepted. Do not bundle adoption with permission to
implement, publish, or change data. Acceptance of the implementation is not agreement
to a broader policy. A user can settle the immediate task and decline generalization.

When the user clearly says "Use that distinction for all accepted events going
forward," adoption is explicit. Record it accurately when authorized; do not ask the
same question again in a formal ritual.

## Admit only consequential commitments

Before proposing a standing principle, answer:

- **Which plausible choice does it change?** Name an alternative it requires,
  excludes, or deliberately deprioritizes. Generic advice fails this test.
- **What judgment would otherwise be lost?** Capture a domain distinction, a chosen
  tradeoff, or a non-obvious reason. Easily rediscovered implementation facts belong
  in their existing sources.
- **Where will it matter again?** Show another application or a credible costly
  failure. Recurrence is useful evidence, not a requirement to repeat a serious mistake.
- **Where does it stop?** Test a concrete counterexample, state the scope and the
  human authority for it, and expose any premise that could change the answer.

Ask whether an existing record should be clarified or consolidated before adding a
new one. A short, bounded commitment with a contrasting case is more useful than a
slogan followed by a long list of exceptions. Do not encode task plans, temporary
workarounds, stylistic preferences unrelated to this workspace, or generic engineering
wisdom as principles merely because they sound reasonable.

## Handle challenges honestly

A failed implementation does not by itself falsify a principle. Identify whether the
case challenges a factual premise, exposes an ambiguous term, changes the tradeoff,
or demonstrates that the commitment's scope is wrong. Human value choices are not
empirical claims that a test can independently overturn.

Present the specific conflict and its consequence. The human can retain the commitment,
make a scoped exception, narrow it, replace it, or retire it. Until resolved, stop
relying on the challenged interpretation for that case; do not suspend unrelated
applications or silently choose a replacement doctrine. Continue independent work.

A current user request can override an earlier workspace commitment within the user's
authority. Establish whether it is an exception or a lasting revision only when that
is unclear. Do not turn yesterday's record into a veto over an explicit new decision.

## Preserve the verdict, not an invented consensus

Separate what was explicitly adopted from your proposed formulation and inferences.
For an exception, record its case and limits without weakening the general commitment.
For a lasting revision, follow [RECORDS.md](RECORDS.md), including impact discovery.
For a decision without broader adoption, leave a contextual decision only when its
future value warrants it. When a declined generalization is likely to recur, retain
the reason and what new evidence would warrant revisiting it in that decision's
existing home. Link it as contextual evidence from the relevant discovery entry
when later work should consult it. No response means no adoption. If the human is unavailable,
make the consequential open choice visible and continue only work that does not
require inventing an answer.
