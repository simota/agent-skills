#!/usr/bin/env python3
"""Regression checks for recipe parsing, routing evidence, and token accounting.

Fixtures encode the published Recipes, Routing Oracle, and token data contracts;
no live transcripts or external services are read.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))


def load_script(filename):
    name = filename.replace("-", "_").removesuffix(".py")
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


recipes = load_script("validate-recipes.py")
directory = load_script("generate-recipes-directory.py")
routing = load_script("routing-oracle.py")
battery = load_script("task-battery-check.py")
economy = load_script("token-economy.py")

TABLE = "| Recipe | Subcommand | Default? |\n|---|---|---|\n| Bug | `bug` | ✓ |\n"


class TempCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path


class TestRecipes(TempCase):
    def test_invalid_subcommand_rows_are_reported(self):
        for cell in ("`bad-`", "`bad--name`", "`-bad`", "BAD", "bad", "", "`x`"):
            with self.subTest(cell=cell):
                content = "## Recipes\n\n" + TABLE + f"| Broken | {cell} | |\n" \
                    "\n## Subcommand Dispatch\n"
                path = self.write("skill/SKILL.md", content)
                errors, _, _ = recipes.validate("skill", path)
                self.assertTrue(any("R-REC-02" in error for error in errors), errors)

    def test_valid_compound_and_digit_leading_subcommands_remain_allowed(self):
        content = "## Recipes\n\n" + TABLE \
            + "| Compound | `growth-acceptance` | |\n| Domain | `5whys` | |\n" \
            + "\n## Subcommand Dispatch\n"
        path = self.write("skill/SKILL.md", content)
        errors, _, _ = recipes.validate("skill", path)
        self.assertEqual(errors, [])

    def test_directory_rejects_invalid_recipe_rows(self):
        for cell in ("`bad-`", "`bad--name`", "BAD", "bad", ""):
            with self.subTest(cell=cell):
                content = "## Recipes\n\n" + TABLE + f"| Broken | {cell} | |\n"
                with self.assertRaisesRegex(ValueError, "subcommand"):
                    directory.extract_recipes(content)

    def test_invalid_recipe_does_not_overwrite_existing_directory(self):
        skill = self.write("skill/SKILL.md", "## Recipes\n\n" + TABLE
                           + "| Broken | BAD | |\n")
        output = self.write("directory.md", "previous valid directory\n")
        errors = io.StringIO()
        with patch.multiple(directory, SKILLS_ROOT=self.root, OUTPUT=output), \
                patch.object(directory, "iter_skill_dirs", return_value=[(skill.parent, False)]), \
                contextlib.redirect_stderr(errors):
            result = directory.main()
        self.assertEqual(result, 1)
        self.assertIn("invalid Recipe subcommand", errors.getvalue())
        self.assertEqual(output.read_text(), "previous valid directory\n")

    def test_recipes_at_eof_still_validate_fallback(self):
        path = self.write("skill/SKILL.md", "## Subcommand Dispatch\n\n"
                          "## Recipes\n\n" + TABLE.replace("✓", ""))
        errors, _, _ = recipes.validate("skill", path)
        self.assertTrue(any("R-REC-01" in error for error in errors), errors)

    def test_directory_ignores_keyword_routing_tables(self):
        content = "## Recipes\n\n" + TABLE + "\n| Keyword | Target | Notes |\n" \
            "|---|---|---|\n| crash | `bug` | triage |\n"
        self.assertEqual(directory.extract_recipes(content), [("bug", True)])

    def test_external_registry_does_not_require_recipes_heading(self):
        self.write("skill/reference/recipes-index.md", "# Registry\n\n" + TABLE)
        content = "## Recipes\n\n`reference/recipes-index.md`\n"
        self.assertEqual(directory.extract_recipes(content, self.root / "skill"),
                         [("bug", True)])

    def test_external_registry_is_not_hidden_by_keyword_table(self):
        self.write("skill/reference/recipes-index.md", "## Recipes\n\n" + TABLE)
        content = "## Recipes\n\n`reference/recipes-index.md`\n\n" \
            "| Keyword | Target | Notes |\n|---|---|---|\n| crash | `bug` | triage |\n"
        self.assertEqual(directory.extract_recipes(content, self.root / "skill"),
                         [("bug", True)])


class TestRoutingEvidence(TempCase):
    def dead_references(self, reference):
        skill = self.write("nexus/SKILL.md", f"Read `{reference}`.\n")
        self.write("other/reference/shared.md", "# Existing file\n")
        findings = []
        with patch.multiple(routing, REPO_ROOT=self.root, NEXUS_DIR=skill.parent,
                            NEXUS_SKILL=skill):
            routing.check_dead_references(findings)
        return findings

    def test_explicit_broken_skill_path_is_not_resolved_by_basename(self):
        findings = self.dead_references("missing/reference/shared.md")
        self.assertTrue(any(f.check == "RO-1" and f.level == "ERROR"
                            for f in findings), [str(f) for f in findings])

    def test_explicit_broken_common_path_is_not_resolved_by_basename(self):
        findings = self.dead_references("_common/shared.md")
        self.assertTrue(any(f.check == "RO-1" and f.level == "ERROR"
                            for f in findings), [str(f) for f in findings])

    def test_unique_bare_reference_shorthand_remains_valid(self):
        self.assertEqual(self.dead_references("reference/shared.md"), [])

    def test_fallback_enums_must_be_on_the_fallback_field(self):
        path = self.write("formats.md", "## NEXUS_COMPLETE\n```\n"
                          "Fallback: fallback_taken\n"
                          "Notes: compass-invoked | architect-invoked | neither\n```\n")
        findings = []
        with patch.object(routing, "OUTPUT_FORMATS", path):
            routing.check_fallback_field(findings)
        self.assertTrue(any(f.level == "ERROR" for f in findings))


class TestBatteryAccounting(TempCase):
    def test_restored_items_fail_when_routing_evidence_is_removed(self):
        path = self.write("signal-keywords.md", "# No routing rules\n")
        items = [item for item in battery.MECHANICAL_ITEMS if 38 <= item[0] <= 44]
        findings = []
        with patch.object(battery, "MECHANICAL_ITEMS", items), \
                patch.object(battery, "FILES", {"signal-keywords.md": path}), \
                contextlib.redirect_stdout(io.StringIO()):
            passed = battery.check_mechanical_items(findings)
        self.assertEqual(passed, 0)
        self.assertEqual({int(f.item.split()[1]) for f in findings if f.level == "ERROR"},
                         {38, 39, 40, 41, 42, 43, 44})

    def test_current_battery_has_complete_check_coverage(self):
        findings = []
        battery.check_battery_coverage(findings)
        self.assertEqual([str(f) for f in findings], [])

    def test_new_battery_item_requires_a_check(self):
        source = battery.TASK_BATTERY.read_text(encoding="utf-8")
        path = self.write("battery.md", source + "\n| 999 | new case | family | route |\n")
        findings = []
        with patch.object(battery, "TASK_BATTERY", path):
            battery.check_battery_coverage(findings)
        self.assertTrue(any(f.level == "ERROR" and "[999]" in f.message for f in findings))

    def test_duplicate_battery_id_is_reported(self):
        source = battery.TASK_BATTERY.read_text(encoding="utf-8")
        path = self.write("battery.md", source + "\n| 1 | duplicate | family | route |\n")
        findings = []
        with patch.object(battery, "TASK_BATTERY", path):
            battery.check_battery_coverage(findings)
        self.assertTrue(any("duplicate documented item IDs: [1]" in f.message for f in findings))

    def test_crashed_check_never_claims_unexecuted_items_passed(self):
        def crash(findings):
            raise ValueError("fixture")

        output = io.StringIO()
        with patch.object(sys, "argv", ["task-battery-check.py"]), \
                patch.object(battery, "check_mechanical_items", crash), \
                patch.object(battery, "check_judgment_items"), \
                patch.object(battery, "check_stale_agent_references"), \
                contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(battery.main(), 0)
        self.assertIn(f"0/{len(battery.MECHANICAL_ITEMS)} mechanical PASS", output.getvalue())
        self.assertIn("check crashed and was skipped", output.getvalue())


class TestTokenAccounting(TempCase):
    def turns(self, reads):
        return [economy.Turn("session", f"{i:03d}", "1.0.0", False,
                             0, 0, read, 0, 0) for i, read in enumerate(reads)]

    def test_cold_start_is_not_charged_as_a_cache_read(self):
        result = economy.compute(self.turns([0, 100, 150]))
        self.assertEqual(result["always_on_cache_read"], 200)
        self.assertEqual(result["on_demand_cache_read"], 50)

    def test_cache_shrink_does_not_make_on_demand_negative(self):
        result = economy.compute(self.turns([100, 20, 0]))
        self.assertEqual(result["always_on_cache_read"], 120)
        self.assertEqual(result["on_demand_cache_read"], 0)

    def test_warm_prefix_is_charged_on_each_cache_read(self):
        result = economy.compute(self.turns([100, 150, 200]))
        self.assertEqual(result["always_on_cache_read"], 300)
        self.assertEqual(result["on_demand_cache_read"], 150)

    def test_duplicate_transcripts_do_not_duplicate_spawn_events(self):
        record = {"type": "assistant", "requestId": "request", "sessionId": "session",
                  "message": {"id": "msg_response", "content": [
                      {"type": "tool_use", "name": "Agent", "id": "toolu_spawn"}],
                      "usage": {"input_tokens": 10, "output_tokens": 5}}}
        for filename in ("a.jsonl", "b.jsonl"):
            self.write(filename, json.dumps(record) + "\n")
        turns, missing, spawns, synthetic = economy.load_turns(self.root, economy.Report())
        self.assertEqual((len(turns), missing, spawns, synthetic), (1, 0, 1, 0))


if __name__ == "__main__":
    unittest.main()
