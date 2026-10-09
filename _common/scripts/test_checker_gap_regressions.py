#!/usr/bin/env python3
"""Regression cases for checker false negatives found in the 2026-10 scripts review.

Each case is the reproduction that showed the checker reporting OK on input it
claims to reject; it fails if the corresponding fix is reverted.
"""

from __future__ import annotations

import importlib.util
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SCRIPTS = pathlib.Path(__file__).resolve().parent


def load(name: str):
    spec = importlib.util.spec_from_file_location(name.replace('-', '_'), SCRIPTS / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


frontmatter = load('lint-frontmatter')
lessons = load('lint-lessons')
contracts = load('lint-contracts')
instructions = load('lint-instructions')

SKILL_BODY = """---
name: example
description: "Build tools for tests. Use when testing checkers."
---

{prose}

<!--
CAPABILITIES_SUMMARY:
- build: tools

COLLABORATION_PATTERNS:
- none

BIDIRECTIONAL_PARTNERS:
- none

PROJECT_AFFINITY: any
-->

## Trigger Guidance
`code` span after the stray backtick.
## Core Contract
## Boundaries
## Collaboration
## Workflow
## Recipes
## Subcommand Dispatch
## Output Requirements
## Reference Map
## Operational
## AUTORUN Support
## Nexus Hub Mode
"""


class FixtureCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='checker-gap-')
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name).resolve()
        for module in (frontmatter, lessons, contracts, instructions):
            patcher = mock.patch.object(module, 'REPO_ROOT', self.root)
            patcher.start()
            self.addCleanup(patcher.stop)
        for name, value in (('COMMON', self.root / '_common'),
                            ('PROJECT_LOCAL', self.root / '.claude' / 'skills')):
            patcher = mock.patch.object(contracts, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')
        return target

    def lint_frontmatter(self, text):
        self.write('example/SKILL.md', text)
        report = frontmatter.Report()
        frontmatter.lint_skill(self.root / 'example', report)
        return report.findings


class TestProjectLocalContractDelivery(FixtureCase):
    """lint-contracts enumerated only root skills; `.claude/skills` was never checked."""

    def setUp(self):
        super().setUp()
        self.write('_common/SPINE.md', '> **Tier:** `spine`\n')
        self.write('_common/HUB.md', 'See `_common/SPINE.md`.\n')
        self.write('.claude/skills/local/SKILL.md', 'Follow `_common/HUB.md`.\n')
        (self.root / '.claude/skills/local/_common').symlink_to('../../../_common')

    def test_project_local_skills_are_owned(self):
        self.assertIn(self.root / '.claude/skills/local', contracts.owned_skills())

    def test_indirect_spine_delivery_to_project_local_skill_is_reported(self):
        findings = []
        contracts.check_delivery(contracts.Graph(), contracts.owned_skills(), {'SPINE.md'}, findings)
        self.assertTrue(any(f[1] == 'CD-2' and 'local' in f[2] for f in findings), findings)


class TestInlineCodeParagraphBoundary(FixtureCase):
    """One literal backtick in prose masked every heading and comment after it."""

    def test_stray_backtick_does_not_hide_structure(self):
        findings = self.lint_frontmatter(SKILL_BODY.format(prose='Press the ` key to toggle.'))
        self.assertFalse([f for f in findings if f.item in ('H1', 'H2', 'H3', 'H4', 'ST1')], findings)

    def test_code_span_within_a_paragraph_is_still_masked(self):
        prose = 'Example: `<!-- CAPABILITIES_SUMMARY: fake -->` is quoted.'
        findings = self.lint_frontmatter(SKILL_BODY.format(prose=prose))
        self.assertFalse([f for f in findings if f.item == 'H1'], findings)


class TestJapaneseDescription(FixtureCase):
    """Kana+kanji ranges alone let Japanese punctuation and half-width kana through."""

    def test_japanese_outside_kana_and_kanji_is_rejected(self):
        for fragment in ('、', '。', '「x」', '（x）', 'ｽｷﾙ', '㐂', 'ㇰ'):
            with self.subTest(fragment=fragment):
                findings = self.lint_frontmatter(
                    f'---\nname: example\ndescription: "Build tools. Use when testing {fragment}"\n---\n')
                self.assertTrue(any(f.item == 'F2' and f.priority == 'P0' and 'Japanese' in f.message
                                    for f in findings), findings)

    def test_english_punctuation_is_not_japanese(self):
        findings = self.lint_frontmatter(
            '---\nname: example\ndescription: "Build tools (fast) -> done. Use when testing."\n---\n')
        self.assertFalse([f for f in findings if 'Japanese' in f.message], findings)


class TestSkillCountPhrasings(FixtureCase):
    """I1 matched none of these claims and so reported OK on a wrong number."""

    def test_unrecognised_phrasings_are_checked(self):
        for claim in ('999+ skills', '999 agent skills', '999 個のスキル', '999件のスキル', '1,234 skills'):
            with self.subTest(claim=claim):
                findings = instructions.check_counts(self.root / 'AGENTS.md', f'This repo has {claim}.', 90)
                self.assertTrue(findings, claim)

    def test_comma_grouped_number_is_read_whole(self):
        findings = instructions.check_counts(self.root / 'AGENTS.md', '1,234 skills', 90)
        self.assertIn('claims 1234 skills', findings[0][2])
        self.assertFalse(instructions.check_counts(self.root / 'AGENTS.md', '1,234 skills', 1234))

    def test_repository_local_count_is_scoped_locally(self):
        for name in ('a', 'b', 'c'):
            self.write(f'.claude/skills/{name}/SKILL.md', '')
        self.assertFalse(instructions.check_counts(self.root / 'AGENTS.md', '3 repository-local skills', 90))
        findings = instructions.check_counts(self.root / 'AGENTS.md', '4 repository-local skills', 90)
        self.assertIn('project-local skills', findings[0][2])


class TestChangedOnlyIncludesUntracked(FixtureCase):
    """`git diff HEAD` never lists an untracked file, so a new skill was skipped."""

    def git(self, *args):
        env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        subprocess.run(['git', *args], cwd=self.root, check=True, capture_output=True, env=env)

    def test_new_untracked_skill_is_selected(self):
        self.git('init', '-q')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                 'commit', '-q', '--allow-empty', '-m', 'baseline')
        self.write('newskill/SKILL.md', '---\nname: Bad_Name\ndescription: x\n---\n')
        env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        with mock.patch.dict(os.environ, env, clear=True):
            paths = frontmatter.changed_paths()
        self.assertIn(self.root / 'newskill/SKILL.md', paths)


class TestLessonIntentions(FixtureCase):
    """LS-2's docstring rejected "should"; the code did not, and spacing evaded it."""

    def register(self, mechanism):
        return ('| ID | What happened | F | Mechanism | Where | Added |\n|----|----|----|----|----|----|\n'
                f'| L001 | A failure occurred | F3 | {mechanism} | `_common/mechanism.py` | 2026-08-21 |\n')

    def setUp(self):
        super().setUp()
        self.write('_common/mechanism.py', 'pass\n')

    def ls2(self, mechanism):
        return [f for f in lessons.check(self.register(mechanism)) if f[1] == 'LS-2']

    def test_intentions_are_rejected(self):
        for mechanism in ('Reviewers should run the checker before merging.',
                          'Be  careful with counts.',
                          'Remember\tto rerun the count.'):
            with self.subTest(mechanism=mechanism):
                self.assertTrue(self.ls2(mechanism), mechanism)

    def test_checks_and_quoted_phrases_are_accepted(self):
        for mechanism in ('A test asserts the checker exits 1 on the claim.',
                          'The linter rejects `should` in rule text.',
                          'The parser now rejects any claim to coverage it cannot prove.'):
            with self.subTest(mechanism=mechanism):
                self.assertFalse(self.ls2(mechanism), mechanism)


if __name__ == '__main__':
    unittest.main()
