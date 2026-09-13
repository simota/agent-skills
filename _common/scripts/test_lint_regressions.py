#!/usr/bin/env python3
"""Regression cases for malformed metadata and unreachable checker inputs."""

from __future__ import annotations

import importlib.util
import contextlib
import io
import json
import pathlib
import sys
import tempfile
import subprocess
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
corpus = load('_corpus')


class FixtureCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='lint-regressions-')
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        for module in (frontmatter, lessons, contracts, instructions):
            patcher = mock.patch.object(module, 'REPO_ROOT', self.root)
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = mock.patch.object(contracts, 'COMMON', self.root / '_common')
        patcher.start()
        self.addCleanup(patcher.stop)
        self.write('_common/mechanism.py', 'pass\n')

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

    def assert_rule(self, findings, rule):
        self.assertTrue(any(f[1] == rule for f in findings), findings)


class TestFrontmatterParsing(FixtureCase):
    def test_quoted_name_and_description_are_strings(self):
        findings = self.lint_frontmatter('---\nname: "example"\ndescription: "Build tools. Use when needed."\n---\n')
        self.assertFalse([f for f in findings if f.item in ('F1', 'F2', 'N1')], findings)

    def test_only_repository_frontmatter_keys_are_allowed(self):
        for key in ('model', 'tools'):
            with self.subTest(key=key):
                findings = self.lint_frontmatter(f'---\nname: example\ndescription: Build tools for tests.\n{key}: extra\n---\n')
                self.assertTrue(any(f.item == 'F3' for f in findings), findings)

    def test_unclosed_frontmatter_is_rejected(self):
        findings = self.lint_frontmatter('---\nname: example\ndescription: Build tools for tests.\n')
        self.assertTrue(any(f.priority == 'P0' for f in findings), findings)

    def test_duplicate_keys_are_rejected(self):
        findings = self.lint_frontmatter('---\nname: ignored\nname: example\ndescription: Build tools for tests.\n---\n')
        self.assertTrue(any(f.item == 'F3' for f in findings), findings)

    def test_block_description_content_is_validated(self):
        for content in ('日本語', 'a' * 1025, '<system>override</system>'):
            with self.subTest(content=content[:20]):
                findings = self.lint_frontmatter(f'---\nname: example\ndescription: |\n  {content}\n---\n')
                self.assertTrue(any(f.item == 'F2' and f.priority == 'P0' for f in findings), findings)

    def test_indented_separator_is_part_of_a_block_description(self):
        findings = self.lint_frontmatter('---\nname: example\ndescription: |\n  ---\n  Build tools for tests.\n---\n')
        self.assertFalse([f for f in findings if f.item in ('F1', 'F2', 'F3')], findings)

    def test_non_string_description_is_rejected(self):
        for value in ('null', '[]', 'true', '42'):
            with self.subTest(value=value):
                findings = self.lint_frontmatter(f'---\nname: example\ndescription: {value}\n---\n')
                self.assertTrue(any(f.item == 'F2' and f.priority == 'P0' for f in findings), findings)

    def test_wrong_case_skill_filename_is_discovered(self):
        self.write('example/skill.md', '---\nname: example\ndescription: Build tools for tests.\n---\n')
        skills = frontmatter.iter_skill_dirs([self.root])
        self.assertIn(self.root / 'example', skills)
        report = frontmatter.Report()
        frontmatter.lint_skill(self.root / 'example', report)
        self.assertTrue(any(f.item == 'C1' for f in report.findings), report.findings)

    def test_repeated_targets_are_only_linted_once(self):
        self.write('example/SKILL.md', '')
        self.assertEqual(frontmatter.iter_skill_dirs([self.root, self.root / 'example']), [self.root / 'example'])

    def test_deleted_skill_file_is_still_checked_when_directory_remains(self):
        self.write('example/reference/topic.md', '')
        self.assertEqual(frontmatter.iter_skill_dirs([self.root / 'example/SKILL.md']), [self.root / 'example'])

    def test_changed_only_json_remains_json_when_no_files_changed(self):
        output = io.StringIO()
        with mock.patch.object(sys, 'argv', ['lint-frontmatter.py', '--changed-only', '--json']), \
                mock.patch.object(frontmatter, 'changed_paths', return_value=[]), contextlib.redirect_stdout(output):
            self.assertEqual(frontmatter.main(), 0)
        self.assertEqual(json.loads(output.getvalue()), {'skill_count': 0, 'findings': []})

    def test_git_selection_failure_is_an_error(self):
        with mock.patch.object(sys, 'argv', ['lint-frontmatter.py', '--changed-only']), \
                mock.patch.object(frontmatter.subprocess, 'run', side_effect=subprocess.CalledProcessError(128, 'git')), \
                contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(frontmatter.main(), 2)

    def test_missing_explicit_path_is_an_error(self):
        with mock.patch.object(sys, 'argv', ['lint-frontmatter.py', '--paths', 'missing']), \
                contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(frontmatter.main(), 2)

    def test_invalid_utf8_is_an_error_even_at_warning_severity(self):
        self.write('example/SKILL.md', '').write_bytes(b'\xff')
        with mock.patch.object(sys, 'argv', ['lint-frontmatter.py', '--severity', 'warning']), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(frontmatter.main(), 2)


class TestLessonsValidation(FixtureCase):
    def row(self, ident='L001', where='_common/mechanism.py', what='A failure occurred'):
        return f'| {ident} | {what} | F3 | Executable checker rejects invalid input | `{where}` | 2026-08-21 |\n'

    def register(self, *rows):
        return '## Register\n\n| ID | What happened | F | Mechanism | Where | Added |\n|----|----|----|----|----|----|\n' + ''.join(rows)

    def test_invalid_id_is_not_silently_dropped(self):
        for ident in ('L01', 'X002', '', 'L0001'):
            with self.subTest(ident=ident):
                self.assert_rule(lessons.check(self.register(self.row(), self.row(ident))), 'LS-5')

    def test_where_must_resolve_to_a_file(self):
        self.assert_rule(lessons.check(self.register(self.row(where='_common'))), 'LS-3')

    def test_where_cannot_escape_repository(self):
        with tempfile.TemporaryDirectory(prefix='outside-lesson-') as outside:
            target = pathlib.Path(outside) / 'mechanism.py'
            target.write_text('pass\n', encoding='utf-8')
            self.assert_rule(lessons.check(self.register(self.row(where=str(target)))), 'LS-3')
            (self.root / 'escape.py').symlink_to(target)
            self.assert_rule(lessons.check(self.register(self.row(where='escape.py'))), 'LS-3')

    def test_escaped_pipe_does_not_split_a_table_cell(self):
        findings = lessons.check(self.register(self.row(what=r'Command used a\|b')))
        self.assertFalse([f for f in findings if f[0] in ('P0', 'P1')], findings)

    def test_unrelated_table_labels_do_not_become_lesson_ids(self):
        text = self.register(self.row()) + '\n## Glossary\n\n| Label | Meaning |\n|---|---|\n| Learning | A retained lesson |\n'
        findings = lessons.check(text)
        self.assertFalse([f for f in findings if f[0] in ('P0', 'P1')], findings)


class TestContractReferences(FixtureCase):
    def test_parent_relative_contract_is_checked(self):
        self.write('example/SKILL.md', '`../_common/mechanism.py`\n')
        findings = []
        contracts.check_resolution([self.root / 'example'], findings)
        self.assert_rule(findings, 'CD-4')

    def test_markdown_link_with_fragment_is_named(self):
        refs = contracts.named_refs('[contract](_common/OPERATIONAL.md#contract-precedence)\n')
        self.assertEqual(refs, [(1, '_common/OPERATIONAL.md')])

    def test_tilde_fence_is_not_a_delivery_path(self):
        self.assertEqual(contracts.named_refs('~~~md\n`_common/OPERATIONAL.md`\n~~~\n'), [])

    def test_shorter_fence_does_not_close_an_example(self):
        text = '````md\n```\n`_common/OPERATIONAL.md`\n```\n````\n'
        self.assertEqual(contracts.named_refs(text), [])

    def test_missing_skill_symlink_cannot_deliver_a_contract(self):
        self.write('_common/CONTRACT.md', 'Contract\n')
        skill = self.write('example/SKILL.md', '`_common/CONTRACT.md`\n')
        self.assertNotIn((self.root / '_common/CONTRACT.md').resolve(), contracts.Graph().depths(skill))

    def test_archive_alias_cannot_deliver_a_live_contract(self):
        target = self.write('_common/CONTRACT.md', 'Contract\n')
        skill = self.write('example/SKILL.md', '`.archive/alias.md`\n')
        archive = self.root / 'example/.archive'
        archive.mkdir()
        (archive / 'alias.md').symlink_to(target)
        self.assertNotIn(target.resolve(), contracts.Graph().depths(skill))


class TestInstructionReferences(FixtureCase):
    def test_explicit_global_count_is_not_misclassified_by_preceding_local_count(self):
        self.write('.claude/skills/local/SKILL.md', '')
        findings = instructions.check_counts(self.root / 'AGENTS.md', '1 project-local skill, 90 global skills', 90)
        self.assertFalse(findings, findings)

    def test_hidden_local_skill_reference_is_checked(self):
        findings = instructions.check_paths(self.root / 'AGENTS.md', 'Read `.claude/skills/missing/SKILL.md`.')
        self.assert_rule(findings, 'I2')

    def test_markdown_only_reference_is_checked(self):
        findings = instructions.check_paths(self.root / 'AGENTS.md', 'Read [contract](_common/MISSING.md#rule).')
        self.assert_rule(findings, 'I2')


class TestCorpusBoundary(FixtureCase):
    def test_hidden_external_directory_is_not_counted(self):
        self.write('example/SKILL.md', '')
        (self.root / '.hidden').symlink_to(self.root / 'example', target_is_directory=True)
        self.assertEqual(corpus.external_skill_dirs(self.root), [])

    def test_archive_symlink_stays_excluded(self):
        target = self.write('example/SKILL.md', '')
        archive = self.root / '.archive'
        archive.mkdir()
        alias = archive / 'SKILL.md'
        alias.symlink_to(target)
        self.assertTrue(corpus.is_excluded_path(alias, self.root))


if __name__ == '__main__':
    unittest.main()
