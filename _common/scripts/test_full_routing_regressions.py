"""Regressions for active Recipe definitions and routing evidence integrity."""

from __future__ import annotations

import contextlib
import io
import subprocess
import unittest
from unittest.mock import patch

from test_routing_regressions import TABLE, TempCase, battery, directory, recipes, routing


class RecipeSourceTests(TempCase):
    def test_literal_backtick_in_prior_paragraph_cannot_hide_recipes(self):
        content = "A literal unmatched ` in prose.\n\n## Recipes\n" + TABLE \
            + "\n## Subcommand Dispatch\n"
        path = self.write("skill/SKILL.md", content)
        self.assertEqual(recipes.validate("skill", path)[0], [])
        self.assertEqual(directory.extract_recipes(content), [("bug", True)])

    def test_literal_backtick_cannot_hide_a_comment_in_another_paragraph(self):
        content = "A literal unmatched ` in prose.\n\n<!--\n## Recipes\n" \
            + TABLE.replace("`bug`", "`decoy`") + "-->\n\n## Recipes\n" + TABLE \
            + "\n## Subcommand Dispatch\n"
        self.assertEqual(directory.extract_recipes(content), [("bug", True)])

    def test_unmatched_backtick_in_comment_does_not_hide_live_recipes(self):
        content = "<!-- retired ` note -->\n## Recipes\n" + TABLE \
            + "\n## Subcommand Dispatch\n"
        path = self.write("skill/SKILL.md", content)
        self.assertEqual(recipes.validate("skill", path)[0], [])
        self.assertEqual(directory.extract_recipes(content), [("bug", True)])

    def test_examples_and_comments_cannot_replace_the_active_recipes(self):
        for before, after in (("```markdown\n", "```\n"), ("<!--\n", "-->\n")):
            with self.subTest(before=before):
                decoy = "## Recipes\n" + TABLE.replace("`bug`", "`decoy`")
                content = before + decoy + after + "## Recipes\n" + TABLE \
                    + "\n## Subcommand Dispatch\n"
                path = self.write("skill/SKILL.md", content)
                self.assertEqual(directory.extract_recipes(content), [("bug", True)])
                self.assertEqual(recipes.validate("skill", path)[0], [])

    def test_example_tables_do_not_add_defaults_or_duplicate_commands(self):
        content = "## Recipes\n" + TABLE + "\n```markdown\n" + TABLE + "```\n" \
            + "\n<!--\n" + TABLE + "-->\n## Subcommand Dispatch\n"
        path = self.write("skill/SKILL.md", content)
        self.assertEqual(recipes.validate("skill", path)[0], [])
        self.assertEqual(directory.extract_recipes(content), [("bug", True)])

    def test_commented_or_example_default_dispatch_is_not_a_fallback(self):
        for before, after in (("```markdown\n", "```\n"), ("<!--\n", "-->\n")):
            with self.subTest(before=before):
                content = "## Recipes\n" + TABLE.replace("✓", "") \
                    + "\n## Subcommand Dispatch\n" + before \
                    + "**Default dispatch:** `phase:CLASSIFY`\n" + after
                path = self.write("skill/SKILL.md", content)
                self.assertTrue(any("R-REC-01" in error for error in recipes.validate("skill", path)[0]))

    def test_comment_cannot_supply_the_required_dispatch_heading(self):
        content = "## Recipes\n" + TABLE + "\n<!--\n## Subcommand Dispatch\n-->\n"
        path = self.write("skill/SKILL.md", content)
        self.assertTrue(any("H-REC-01" in error for error in recipes.validate("skill", path)[0]))

    def test_escaped_pipe_in_recipe_name_does_not_shift_subcommand_column(self):
        content = "## Recipes\n" + TABLE.replace("| Bug |", r"| Bug \| Incident |") \
            + "\n## Subcommand Dispatch\n"
        path = self.write("skill/SKILL.md", content)
        self.assertEqual(recipes.validate("skill", path)[0], [])
        self.assertEqual(directory.extract_recipes(content), [("bug", True)])

    def external_registry(self, commands="bug", default="bug"):
        self.write("skill/reference/recipes-index.md", TABLE)
        return self.write("skill/SKILL.md", "## Recipes\n`reference/recipes-index.md`\n"
                          "dispatch allowlist only\n```\n" + commands + "\n```\n"
                          "Default Recipe: `" + default + "`.\n\n## Subcommand Dispatch\n")

    def test_external_allowlist_must_match_registry_and_have_no_duplicates(self):
        for commands in ("other", "bug · ghost", "bug · bug"):
            with self.subTest(commands=commands):
                path = self.external_registry(commands)
                self.assertTrue(any("allowlist" in error for error in recipes.validate("skill", path)[0]))
        self.assertEqual(recipes.validate("skill", self.external_registry())[0], [])

    def test_external_default_must_match_registry(self):
        path = self.external_registry(default="other")
        self.assertTrue(any("R-REC-01" in error for error in recipes.validate("skill", path)[0]))

    def test_empty_inline_registry_cannot_erase_a_published_skill(self):
        skill = self.write("skill/SKILL.md", "## Recipes\nThe table was deleted.\n")
        output = self.write("directory.md", "previous valid directory\n")
        with patch.multiple(directory, SKILLS_ROOT=self.root, OUTPUT=output), \
                patch.object(directory, "iter_skill_dirs", return_value=[(skill.parent, False)]), \
                contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(directory.main(), 1)
        self.assertEqual(output.read_text(), "previous valid directory\n")


class ChangedRecipeTests(TempCase):
    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True,
                              text=True, capture_output=True)

    def test_registry_edits_and_untracked_skills_are_validated(self):
        self.git("init", "--quiet")
        self.write("owned/SKILL.md", "# Owned\n")
        registry = self.write("owned/reference/recipes-index.md", TABLE)
        self.git("add", ".")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "commit", "--quiet", "-m", "fixture")
        registry.write_text(TABLE.replace("`bug`", "`invalid--name`"))
        self.write("new-skill/SKILL.md", "# New\n")
        with patch.object(recipes, "SKILLS_ROOT", self.root):
            self.assertEqual(recipes.changed_skill_names(), {"owned", "new-skill"})

    def test_git_failure_falls_back_to_full_validation(self):
        self.git("init", "--quiet")  # An unborn HEAD cannot produce the requested diff.
        with patch.object(recipes, "SKILLS_ROOT", self.root), \
                contextlib.redirect_stderr(io.StringIO()):
            self.assertIsNone(recipes.changed_skill_names())


class RoutingEvidenceTests(TempCase):
    def test_project_local_agents_reference_resolves_from_repo_root(self):
        skill = self.write("nexus/SKILL.md", "Read `.agents/skills/local/reference/run.md`.\n")
        self.write(".agents/skills/local/reference/run.md", "# Reference\n")
        findings = []
        with patch.multiple(routing, REPO_ROOT=self.root, NEXUS_DIR=skill.parent, NEXUS_SKILL=skill):
            routing.check_dead_references(findings)
        self.assertEqual(findings, [])

    def test_tilde_and_long_backtick_template_fences_are_checked(self):
        for fence in ("~~~", "````"):
            with self.subTest(fence=fence):
                path = self.write("formats.md", "## NEXUS_COMPLETE\n" + fence + "text\n"
                                  "Fallback: fallback_taken = compass-invoked | architect-invoked | neither\n"
                                  + fence + "\n")
                findings = []
                with patch.object(routing, "OUTPUT_FORMATS", path):
                    routing.check_fallback_field(findings)
                self.assertEqual(findings, [])

    def test_commented_template_inside_section_cannot_mask_missing_fallback(self):
        path = self.write("formats.md", "## NEXUS_COMPLETE\n<!--\n```\n"
                          "Fallback: fallback_taken = compass-invoked | architect-invoked | neither\n"
                          "```\n-->\n```\nTask: actual template without fallback\n```\n")
        findings = []
        with patch.object(routing, "OUTPUT_FORMATS", path):
            routing.check_fallback_field(findings)
        self.assertTrue(any(f.level == "ERROR" for f in findings))

    def test_commented_bare_subcommand_exception_does_not_satisfy_gate(self):
        skill = self.write("nexus/SKILL.md", "## Recipes\ndispatch allowlist only\n"
                           "```\noptimize\n```\n## Subcommand Dispatch\n"
                           "<!-- **Bare-subcommand exception.** Route to GATE. -->\n")
        self.write("nexus/reference/task-battery.md", 'bare "optimize"\n')
        findings = []
        with patch.multiple(routing, NEXUS_DIR=skill.parent, NEXUS_SKILL=skill):
            routing.check_bare_subcommand_dispatch(findings)
        self.assertTrue(any(f.level == "ERROR" for f in findings))


class BatteryEvidenceTests(TempCase):
    def test_retired_evidence_in_comments_or_examples_does_not_pass(self):
        for content in ("<!-- required evidence -->\n", "```markdown\nrequired evidence\n```\n"):
            with self.subTest(content=content):
                path = self.write("routing.md", content)
                findings = []
                with patch.object(battery, "MECHANICAL_ITEMS", [(1, "fixture", "source", "required evidence")]), \
                        patch.object(battery, "FILES", {"source": path}), \
                        contextlib.redirect_stdout(io.StringIO()):
                    passed = battery.check_mechanical_items(findings)
                self.assertEqual(passed, 0)
                self.assertTrue(any(f.level == "ERROR" for f in findings))

    def test_commented_battery_rows_are_not_coverage(self):
        path = self.write("battery.md", "<!--\n| 1 | removed item | route |\n-->\n")
        findings = []
        with patch.object(battery, "TASK_BATTERY", path), \
                patch.object(battery, "MECHANICAL_ITEMS", [(1, "fixture", "source", "evidence")]), \
                patch.object(battery, "JUDGMENT_ITEMS", []):
            battery.check_battery_coverage(findings)
        self.assertTrue(any(f.level == "ERROR" for f in findings))


if __name__ == "__main__":
    unittest.main()
