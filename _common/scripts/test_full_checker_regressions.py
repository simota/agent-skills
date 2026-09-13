#!/usr/bin/env python3
"""Regression coverage for malformed transcript and Markdown checker boundaries."""

from __future__ import annotations

import importlib.util
import datetime as dt
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


SCRIPTS = Path(__file__).resolve().parent


def load(name: str):
    spec = importlib.util.spec_from_file_location(
        "full_checker_" + name.replace("-", "_"), SCRIPTS / f"{name}.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


frontmatter = load("lint-frontmatter")
instructions = load("lint-instructions")
economy = load("token-economy")
lessons = load("lint-lessons")


class CheckerBoundaryTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="full-checker-")
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        for module in (frontmatter, instructions, lessons):
            patcher = mock.patch.object(module, "REPO_ROOT", self.root)
            patcher.start()
            self.addCleanup(patcher.stop)

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return target

    def lint_headings(self, heading):
        body = "\n\n".join(heading(name) for name in frontmatter.REQUIRED_HEADINGS)
        skill = self.write("example/SKILL.md", "---\nname: example\n"
                           "description: Build tools for tests.\n---\n" + body)
        report = frontmatter.Report()
        frontmatter.lint_skill(skill.parent, report)
        return [finding for finding in report.findings if finding.item == "ST1"]

    def test_bare_atx_marker_does_not_consume_next_paragraph_as_heading(self):
        self.assertTrue(self.lint_headings(lambda name: "##\n" + name))

    def test_valid_atx_indentation_and_closing_hashes_are_accepted(self):
        for indent in ("", " ", "   "):
            with self.subTest(indent=indent):
                self.assertEqual(self.lint_headings(lambda name: indent + "## " + name + " ##"), [])

    def test_four_space_indented_text_is_not_a_heading(self):
        self.assertTrue(self.lint_headings(lambda name: "    ## " + name))

    def test_local_count_does_not_change_scope_of_next_unqualified_count(self):
        self.write(".claude/skills/local/SKILL.md", "")
        findings = instructions.check_counts(
            self.root / "AGENTS.md", "1 project-local skill and 90 specialist skill agents", 90
        )
        self.assertEqual(findings, [])

    def test_local_prefix_still_scopes_its_own_count(self):
        self.write(".claude/skills/local/SKILL.md", "")
        for text in ("Project-local: 1 skill", "プロジェクトローカル: 1 スキル"):
            with self.subTest(text=text):
                self.assertEqual(instructions.check_counts(self.root / "AGENTS.md", text, 90), [])

    def test_lesson_code_spans_can_quote_the_intention_the_checker_rejects(self):
        self.write("_common/check.py", "pass\n")
        for quote in ("`remember to`", "``remember to``", "`` `remember to` ``"):
            with self.subTest(quote=quote):
                row = ("| L001 | A weak mechanism passed | F3 | The checker rejects " + quote
                       + " | `_common/check.py` | " + dt.date.today().isoformat() + " |\n")
                findings = lessons.check(row)
                self.assertFalse([finding for finding in findings if finding[1] == "LS-2"], findings)

    def record(self):
        return {"type": "assistant", "requestId": "request-1", "sessionId": "session-1",
                "message": {"id": "msg_response", "usage": {"input_tokens": 10, "output_tokens": 5}}}

    def load_records(self, *records):
        self.write("session.jsonl", "\n".join(json.dumps(record) for record in records) + "\n")
        report = economy.Report()
        return economy.load_turns(self.root, report), report

    def test_falsy_malformed_messages_are_integrity_errors_not_synthetic(self):
        for malformed in (None, False, 0, "", []):
            with self.subTest(message=malformed):
                bad = {"type": "assistant", "message": malformed}
                (turns, missing, spawns, skipped), report = self.load_records(bad, self.record())
                self.assertEqual((len(turns), missing, spawns, skipped), (1, 0, 0, 0))
                self.assertTrue(report.by_priority("P0"), report.findings)
                self.assertEqual(economy.compute(turns)["grand_total"], 15)

    def test_missing_message_is_an_integrity_error(self):
        (turns, _, _, skipped), report = self.load_records({"type": "assistant"})
        self.assertEqual((turns, skipped), ([], 0))
        self.assertTrue(report.by_priority("P0"), report.findings)

    def test_invalid_zero_usage_is_not_a_synthetic_placeholder(self):
        for usage in ({"input_tokens": False, "output_tokens": 0},
                      {"input_tokens": 0.0, "output_tokens": 0},
                      {"input_tokens": 0, "output_tokens": 0, "output_tokens_details": []},
                      {"input_tokens": 0, "output_tokens": 0,
                       "output_tokens_details": {"thinking_tokens": 1}}):
            with self.subTest(usage=usage):
                record = {"type": "assistant", "message": {
                    "id": "msg_interrupted", "stop_reason": "stop_sequence", "usage": usage}}
                (turns, _, _, skipped), report = self.load_records(record)
                self.assertEqual((turns, skipped), ([], 0))
                self.assertTrue(report.by_priority("P0"), report.findings)

    def test_valid_synthetic_placeholders_stay_excluded(self):
        placeholders = [
            {"type": "assistant", "message": {"id": "synthetic-interruption"}},
            {"type": "assistant", "message": {"id": "msg_interrupted", "stop_reason": "stop_sequence",
                                                "usage": {"input_tokens": 0, "output_tokens": 0}}},
        ]
        (turns, missing, spawns, skipped), report = self.load_records(*placeholders, self.record())
        self.assertEqual((len(turns), missing, spawns, skipped), (1, 0, 0, 2))
        self.assertEqual(report.findings, [])


if __name__ == "__main__":
    unittest.main()
