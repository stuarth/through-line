"""Structural checks only; no test here evaluates an agent's behavior."""
from __future__ import annotations
import json
import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / 'evals' / 'workspace'
GUIDES = ('DISCOVER.md', 'DISCUSS.md', 'RECORDS.md', 'HOSTS.md')


def prose(text: str) -> str:
    return re.sub(r'(?ms)^(`{3,}|~{3,})[^\n]*\n.*?^\1[ \t]*$', '', text)


def local_links(path: Path):
    for label, raw in re.findall(r'\[([^\]]+)\]\(([^\s)]+)\)', prose(path.read_text())):
        parsed = urlsplit(raw)
        if parsed.scheme or parsed.netloc:
            continue
        target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
        yield label, target, unquote(parsed.fragment)


def heading_anchors(path: Path) -> set[str]:
    return {re.sub(r'[^\w\- ]', '', h.lower()).replace(' ', '-')
            for h in re.findall(r'(?m)^#{1,6}\s+(.+)$', prose(path.read_text()))}


def safe_fixture_path(relative: str) -> Path:
    path = (WORKSPACE / relative).resolve()
    if not path.is_relative_to(WORKSPACE) or path == WORKSPACE:
        raise ValueError(f'Not a workspace file path: {relative}')
    return path


class PackageTests(unittest.TestCase):
    def test_skill_frontmatter_and_automatic_eligibility(self):
        text = (ROOT / 'SKILL.md').read_text()
        self.assertTrue(text.startswith('---\n'))
        front = text.split('---\n', 2)[1]
        self.assertIn('name: through-line\n', front)
        # Claude's automatic default needs no host-specific frontmatter extension.
        self.assertNotIn('disable-model-invocation:', front)
        self.assertIn('version: "2.0.0-draft"', front)
        description = front.split('description: >-\n', 1)[1].split('metadata:', 1)[0]
        self.assertLessEqual(len(' '.join(description.split())), 1024)
        self.assertIn('Skip unrelated', description)

    def test_codex_automatic_eligibility(self):
        text = (ROOT / 'agents/openai.yaml').read_text()
        self.assertRegex(text, r'(?m)^policy:\n  allow_implicit_invocation: true$')
        self.assertIn('$through-line', text)

    def test_no_added_tool_permissions_or_context_fork(self):
        front = (ROOT / 'SKILL.md').read_text().split('---\n', 2)[1]
        self.assertNotIn('allowed-tools:', front)
        self.assertNotIn('context: fork', front)
        self.assertNotIn('dependencies:', (ROOT / 'agents/openai.yaml').read_text())

    def test_one_installable_skill(self):
        self.assertEqual(list(ROOT.rglob('SKILL.md')), [ROOT / 'SKILL.md'])

    def test_attention_budgets(self):
        self.assertLessEqual(len((ROOT / 'SKILL.md').read_text().split()), 1200)
        self.assertLessEqual(len((ROOT / 'SKILL.md').read_text().splitlines()), 200)
        for guide in GUIDES:
            with self.subTest(guide=guide):
                self.assertLessEqual(len((ROOT / guide).read_text().split()), 1000)
        self.assertLessEqual(len((WORKSPACE / 'principles/index.md').read_text().split()), 400)

    def test_guides_discoverable_from_entry(self):
        targets = {target for _, target, _ in local_links(ROOT / 'SKILL.md')}
        for guide in GUIDES:
            self.assertIn(ROOT / guide, targets)

    def test_markdown_links_and_fragments(self):
        for path in ROOT.rglob('*.md'):
            for label, target, fragment in local_links(path):
                with self.subTest(source=str(path.relative_to(ROOT)), label=label):
                    self.assertTrue(target.is_relative_to(ROOT), f'Link escapes package: {target}')
                    self.assertTrue(target.exists(), f'Missing target: {target}')
                    if fragment and target.suffix == '.md':
                        self.assertIn(fragment, heading_anchors(target))

    def test_legacy_runtime_removed(self):
        for name in ('ADVANCE.md', 'CHART.md', 'EXECUTION.md', 'IMPLEMENT.md',
                     'REVIEW.md', 'SUPERVISE.md', 'PRINCIPLES-GUIDE.md', 'trackers',
                     'scripts/validate_local_map.py', 'scripts/test_validate_local_map.py'):
            self.assertFalse((ROOT / name).exists(), f'Legacy runtime remains: {name}')

    def test_fixture_authority_and_boundaries(self):
        index = WORKSPACE / 'principles/index.md'
        self.assertIn('## Always consult', index.read_text())
        self.assertIn('## By concern', index.read_text())
        for path in index.parent.glob('*.md'):
            if path == index:
                continue
            with self.subTest(record=path.name):
                text = path.read_text()
                self.assertIn('Status: adopted\n', text)
                self.assertIn('Authority:', text)
                for heading in ('Commitment', 'Why this choice', 'Applies when', 'Boundary', 'Evidence'):
                    self.assertIn(f'## {heading}\n', text)
                self.assertIn('decisions/adoptions.md', text)

    def test_case_ids_and_assertions(self):
        cases = json.loads((ROOT / 'evals/cases.json').read_text())
        ids = [case['id'] for case in cases]
        self.assertEqual(len(ids), len(set(ids)))
        for case in cases:
            with self.subTest(case=case['id']):
                self.assertIn(case['fixture'], {'empty', 'seeded'})
                for key in ('turns', 'expect', 'forbid'):
                    self.assertTrue(case[key])
                    self.assertTrue(all(isinstance(x, str) and x.strip() for x in case[key]))
                self.assertIsInstance(case['setup'], list)

    def test_case_setups_apply(self):
        """Dry-run setup changes in memory so fixtures and replacement text cannot drift."""
        cases = json.loads((ROOT / 'evals/cases.json').read_text())
        seed = {str(p.relative_to(WORKSPACE)): p.read_text()
                for p in WORKSPACE.rglob('*') if p.is_file()}
        for case in cases:
            state = seed.copy() if case['fixture'] == 'seeded' else {}
            with self.subTest(case=case['id']):
                for op in case['setup']:
                    path = op['path']
                    safe_fixture_path(path)
                    if op['op'] == 'write':
                        self.assertIsInstance(op['content'], str)
                        state[path] = op['content']
                    elif op['op'] == 'remove':
                        del state[path]
                    elif op['op'] == 'replace':
                        self.assertEqual(state[path].count(op['old']), 1)
                        state[path] = state[path].replace(op['old'], op['new'])
                    else:
                        self.fail(f'Unknown operation: {op}')

    def test_fixture_paths_cannot_escape(self):
        for path in ('../outside.md', '/tmp/outside.md', '.'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                safe_fixture_path(path)

    def test_link_extractor_ignores_examples(self):
        text = '# Actual\n```markdown\n[placeholder](not-a-file.md)\n```\n[real](README.md)\n'
        self.assertNotIn('not-a-file', prose(text))
        self.assertIn('[real](README.md)', prose(text))


if __name__ == '__main__':
    unittest.main()
