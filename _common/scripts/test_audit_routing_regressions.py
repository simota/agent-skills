"""Audit regressions for recipe publication and routing/token evidence checks."""

from __future__ import annotations

import contextlib
import io
import json
import sys
import unittest
from unittest.mock import patch

from test_routing_regressions import TABLE, TempCase, directory, economy, recipes, routing


class TestRecipePublication(TempCase):
    def test_bare_dispatch_heading_allows_trailing_whitespace(self):
        path = self.write("skill/SKILL.md", "## Recipes\n\n" + TABLE
                          + "\n## Subcommand Dispatch  \n")
        self.assertEqual(recipes.validate("skill", path)[0], [])

    def test_missing_or_empty_external_registry_preserves_published_directory(self):
        skill = self.write("skill/SKILL.md", "## Recipes\n\n"
                           "`reference/recipes-index.md`\n")
        output = self.write("directory.md", "previous valid directory\n")
        for registry in (None, "# Registry without a table\n"):
            with self.subTest(registry=registry):
                if registry is not None:
                    self.write("skill/reference/recipes-index.md", registry)
                with patch.multiple(directory, SKILLS_ROOT=self.root, OUTPUT=output), \
                        patch.object(directory, "iter_skill_dirs", return_value=[(skill.parent, False)]), \
                        contextlib.redirect_stderr(io.StringIO()), \
                        contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(directory.main(), 1)
                self.assertEqual(output.read_text(), "previous valid directory\n")

    def test_project_local_directory_uses_the_validation_corpus(self):
        local = self.root / ".claude" / "skills"
        owned = self.write(".claude/skills/owned/SKILL.md", "# Owned\n").parent
        self.write(".claude/skills/.hidden/SKILL.md", "# Hidden\n")
        external = self.write("external/SKILL.md", "# External\n").parent
        (local / "linked").symlink_to(external, target_is_directory=True)
        with patch.multiple(directory, SKILLS_ROOT=self.root, PROJECT_LOCAL_ROOT=local):
            local_entries = [path for path, is_local in directory.iter_skill_dirs() if is_local]
        self.assertEqual(local_entries, [owned])


class TestRoutingSectionEvidence(TempCase):
    def check_bare_dispatch(self, dispatch, *, next_section=True):
        content = "## Recipes\n\ndispatch allowlist only\n```\noptimize pack\n```\n" \
            "\n## Subcommand Dispatch\n" + dispatch
        if next_section:
            content += "\n## Workflow\n"
        skill = self.write("nexus/SKILL.md", content)
        self.write("nexus/reference/task-battery.md", 'bare "optimize"\n')
        findings = []
        with patch.multiple(routing, NEXUS_DIR=skill.parent, NEXUS_SKILL=skill):
            routing.check_bare_subcommand_dispatch(findings)
        return findings

    def test_exempt_label_matches_the_current_colon_inside_bold_format(self):
        findings = self.check_bare_dispatch(
            "- **Bare-subcommand exception.** Bare tokens reach GATE. **Exempt:** `optimize`.\n")
        self.assertTrue(any(f.level == "ERROR" and "exempt" in f.message for f in findings),
                        [str(f) for f in findings])

    def test_dispatch_at_eof_is_checked(self):
        findings = self.check_bare_dispatch("Match the first token and dispatch.\n", next_section=False)
        self.assertTrue(any(f.level == "ERROR" for f in findings), [str(f) for f in findings])

    def test_valid_dispatch_at_eof_does_not_warn(self):
        findings = self.check_bare_dispatch(
            "- **Bare-subcommand exception.** Bare tokens reach GATE. **Exempt:** `pack`.\n",
            next_section=False)
        self.assertEqual(findings, [])

    def test_other_sections_cannot_supply_the_complete_template(self):
        path = self.write("formats.md", "## NEXUS_COMPLETE\nTemplate was deleted.\n\n"
                          "## UNRELATED\n```\nFallback: fallback_taken = "
                          "compass-invoked | architect-invoked | neither\n```\n")
        findings = []
        with patch.object(routing, "OUTPUT_FORMATS", path):
            routing.check_fallback_field(findings)
        self.assertTrue(findings, "a missing NEXUS_COMPLETE template must not pass")

    def test_template_headings_inside_fences_do_not_end_the_section(self):
        path = self.write("formats.md", "## NEXUS_COMPLETE (AUTORUN)\n```\n"
                          "## NEXUS_COMPLETE\nFallback: fallback_taken = "
                          "compass-invoked | architect-invoked | neither\n```\n")
        findings = []
        with patch.object(routing, "OUTPUT_FORMATS", path):
            routing.check_fallback_field(findings)
        self.assertEqual(findings, [])

    def test_non_fences_before_a_template_do_not_hide_its_section(self):
        prefixes = ("```inline```\n\n", "<!--\n```md\n-->\n\n", "    ```md\n\n")
        for prefix in prefixes:
            with self.subTest(prefix=prefix):
                path = self.write("formats.md", prefix + "## NEXUS_COMPLETE\n```\n"
                                  "Fallback: fallback_taken = "
                                  "compass-invoked | architect-invoked | neither\n```\n")
                findings = []
                with patch.object(routing, "OUTPUT_FORMATS", path):
                    routing.check_fallback_field(findings)
                self.assertEqual(findings, [])

    def test_commented_template_cannot_hide_a_broken_active_template(self):
        path = self.write("formats.md", "<!--\n## NEXUS_COMPLETE\n```\n"
                          "Fallback: fallback_taken = "
                          "compass-invoked | architect-invoked | neither\n```\n-->\n"
                          "## NEXUS_COMPLETE\n```\nTask: active template without fallback\n```\n")
        findings = []
        with patch.object(routing, "OUTPUT_FORMATS", path):
            routing.check_fallback_field(findings)
        self.assertTrue(any(f.level == "ERROR" for f in findings), [str(f) for f in findings])


class TestTranscriptIntegrity(TempCase):
    def record(self, *, thinking=2):
        return {"type": "assistant", "requestId": "request-1", "sessionId": "session-1",
                "message": {"id": "msg_response", "usage": {
                    "input_tokens": 10, "output_tokens": 5,
                    "output_tokens_details": {"thinking_tokens": thinking}}}}

    def test_dedup_detects_conflicting_thinking_usage(self):
        self.write("session.jsonl", "\n".join(json.dumps(self.record(thinking=n)) for n in (2, 3)))
        report = economy.Report()
        turns, missing, _, _ = economy.load_turns(self.root, report)
        self.assertEqual((len(turns), missing), (1, 0))
        self.assertTrue(report.by_priority("P0"))

    def test_corrupt_json_is_reported_and_valid_records_remain_counted(self):
        self.write("session.jsonl", '{"private prompt":\n' + json.dumps(self.record()) + "\n")
        report = economy.Report()
        turns, _, _, _ = economy.load_turns(self.root, report)
        self.assertEqual(economy.compute(turns)["grand_total"], 15)
        self.assertTrue(report.by_priority("P0"))
        self.assertNotIn("private prompt", str(report.findings))

    def test_malformed_record_shapes_are_reported_instead_of_crashing(self):
        for record in ([], {"type": "assistant", "message": ["invalid"]}):
            with self.subTest(record=record):
                self.write("session.jsonl", json.dumps(record) + "\n")
                report = economy.Report()
                turns, _, _, _ = economy.load_turns(self.root, report)
                self.assertEqual(turns, [])
                self.assertTrue(report.by_priority("P0"))

    def test_invalid_usage_cannot_produce_false_or_negative_totals(self):
        for value in (-1, "10", None, True):
            with self.subTest(value=value):
                record = self.record()
                record["message"]["usage"]["input_tokens"] = value
                self.write("session.jsonl", json.dumps(record) + "\n")
                report = economy.Report()
                turns, _, _, _ = economy.load_turns(self.root, report)
                self.assertEqual(turns, [])
                self.assertTrue(report.by_priority("P0"))

    def test_empty_request_id_is_missing_integrity_data(self):
        record = self.record()
        record["requestId"] = ""
        self.write("session.jsonl", json.dumps(record) + "\n")
        report = economy.Report()
        turns, missing, _, _ = economy.load_turns(self.root, report)
        self.assertEqual((turns, missing), ([], 1))
        self.assertTrue(report.by_priority("P0"))

    def test_invalid_agent_event_identifier_does_not_crash_usage_accounting(self):
        record = self.record()
        record["message"]["content"] = [{"type": "tool_use", "name": "Agent", "id": ["invalid"]}]
        self.write("session.jsonl", json.dumps(record) + "\n")
        report = economy.Report()
        turns, _, spawns, _ = economy.load_turns(self.root, report)
        self.assertEqual((len(turns), spawns), (1, 0))
        self.assertTrue(report.by_priority("P0"))

    def test_empty_malformed_thinking_details_are_not_treated_as_missing(self):
        record = self.record()
        record["message"]["usage"]["output_tokens_details"] = []
        self.write("session.jsonl", json.dumps(record) + "\n")
        report = economy.Report()
        turns, _, _, _ = economy.load_turns(self.root, report)
        self.assertEqual(turns, [])
        self.assertTrue(report.by_priority("P0"))

    def test_thinking_is_a_subset_of_output(self):
        self.write("session.jsonl", json.dumps(self.record(thinking=6)) + "\n")
        report = economy.Report()
        turns, _, _, _ = economy.load_turns(self.root, report)
        self.assertEqual(turns, [])
        self.assertTrue(report.by_priority("P0"))

    def test_invalid_utf8_returns_the_documented_internal_error(self):
        self.write("session.jsonl", "").write_bytes(b"\xff\n")
        with patch.object(sys, "argv", ["token-economy.py", "--project-dir", str(self.root)]), \
                contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(economy.main(), 2)


if __name__ == "__main__":
    unittest.main()
