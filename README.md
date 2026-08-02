# through-line

A skill for driving huge efforts: distill the recurring commitments beneath an
effort's many decisions into human-adopted principles, propagate each verdict
through the remaining map, and surface only the residual judgment that genuinely
needs a human.

This repo **is** the skill — [SKILL.md](./SKILL.md) at the root, with its phase
runbooks alongside:

- [CHART.md](./CHART.md) — turn a loose idea into a map
- [WORK.md](./WORK.md) — advance an existing map, one round or ticket per session
- [SUPERVISE.md](./SUPERVISE.md) — opt-in unattended advancement
- [ADMISSION.md](./ADMISSION.md), [REVIEW.md](./REVIEW.md),
  [IMPLEMENT.md](./IMPLEMENT.md), [EXECUTION.md](./EXECUTION.md) — supporting
  stages
- [PRINCIPLES-FORMAT.md](./PRINCIPLES-FORMAT.md) — the shape of adopted doctrine
- [trackers/](./trackers/) and [scripts/](./scripts/) — the bundled
  local-markdown tracker and its map validator

[docs/through-line.md](./docs/through-line.md) is the human-facing guide.

## Install

Symlink the repo into your harness's skill directory, then invoke with
`/through-line`:

```bash
ln -s "$(pwd)" ~/.claude/skills/through-line
```

A `git pull` keeps the installed skill current.

## Relationship to mattpocock/skills

through-line began inside a fork of
[mattpocock/skills](https://github.com/mattpocock/skills) and grew until it was
the fork's entire purpose; this repo carries that full history. It builds on
that ecosystem rather than forking it: install mattpocock/skills separately for
the skills through-line hands off to (wayfinder, grilling, to-spec, and the
tracker wiring from setup-matt-pocock-skills). Without that wiring,
through-line falls back to its bundled local-markdown tracker.
