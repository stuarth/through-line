# Installation and automatic use

The package supports model-selected invocation. Claude Code enables it by default;
`agents/openai.yaml` sets `allow_implicit_invocation: true` for Codex. The shared
frontmatter omits Claude-specific invocation fields. Neither host guarantees that a
model will invoke the skill on every relevant task.
Use a small workspace instruction as the normal integration for ongoing work. No
principles corpus belongs in the always-loaded instruction file.

## Install a local checkout

Clone the repository into a dedicated location for the published default version:

```sh
git clone https://github.com/stuarth/through-line.git ~/dev/through-line
cd ~/dev/through-line
```

For local v2 review, use a checkout of `v2/shared-judgment` or the extracted draft's
`through-line-v2` folder. The review branch may exist only locally; cloning the remote
default branch does not install an unpublished draft. Use the chosen v2 folder as
the symlink source below.

For Codex, symlink the checkout or extracted skill folder:

```sh
mkdir -p ~/.agents/skills
ln -s ~/dev/through-line ~/.agents/skills/through-line
```

For Claude Code:

```sh
mkdir -p ~/.claude/skills
ln -s ~/dev/through-line ~/.claude/skills/through-line
```

Replace the source path with your extracted folder when testing without a checkout.
Do not replace an existing installation blindly. Inspect its target and deliberately
switch versions to avoid loading both under the same name. These commands intentionally
do not force an overwrite. Restart the host if a changed installation is not discovered.

Explicit invocation remains available as `$through-line` in Codex and `/through-line`
in Claude Code, but ordinary use should not depend on remembering those commands.

## Add the workspace entry instruction

With permission, merge the following into the workspace's existing `AGENTS.md` for
Codex or `CLAUDE.md` for Claude Code. Set the principles path to the existing workspace
location. Keep machine-specific installation paths in local configuration, preserve
other instructions, and reuse the existing knowledge collection.

```markdown
## Through-line

During substantive work in this workspace, apply the through-line skill before
making recommendations or changes, and revisit discovery when scope changes.
Use the installed through-line skill and read its SKILL.md entry point.
Principles entry: principles/index.md (may not exist yet).
Read the always-consult records and relevant scoped records, not the whole corpus.
Discuss consequential gaps or counterexamples; do not interrupt settled routine work.
No corpus is required to begin, and no new principle is required to finish.
```

If the host cannot find the installed skill, report that limitation and continue
unaffected work. Resolve installation paths through the host's skill discovery or
local configuration.

The instruction directs the agent to read/apply the skill even when model-selected
skill invocation is missed. It is still an instruction, not deterministic enforcement.
This draft ships no host hook and does not claim guaranteed activation. Where a host
requires enforcement, implement and test that integration separately; do not silently
install hooks or change permissions on the user's behalf.

If tools cannot read the configured records, expose the limitation when it matters
and continue unaffected work. Do not pretend conversation memory is the authoritative
collection.

## Check the actual integration

Start a fresh session with relevant records. Give it an ordinary task without naming
through-line. Inspect whether it reads the skill and discovers the right records before
deciding. Then try an unrelated question and a mundane change; neither should provoke
a principles interview. Repeat after context compaction or with a new session. Test
implicit discovery and the workspace-instruction path separately; explicit invocation
is diagnostic, not a passing automatic-use result.

See [the evaluation protocol](evals/README.md) for repeatable cases. Package checks
establish file integrity and metadata, not live host behavior.

## Host references

- [Codex skills](https://developers.openai.com/codex/skills/)
- [Codex workspace instructions](https://developers.openai.com/codex/guides/agents-md)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
