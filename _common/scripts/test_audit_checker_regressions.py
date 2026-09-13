#!/usr/bin/env python3
"""Exercise real Markdown and filesystem boundaries in the repository linters."""

from __future__ import annotations

import importlib.util
import datetime as dt
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


SCRIPTS = Path(__file__).resolve().parent


def load(name: str):
    spec = importlib.util.spec_from_file_location(
        "audit_" + name.replace("-", "_"), SCRIPTS / f"{name}.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


frontmatter = load("lint-frontmatter")
contracts = load("lint-contracts")
instructions = load("lint-instructions")
lessons = load("lint-lessons")


class CheckerBoundaryTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="audit-checker-")
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        for module in (frontmatter, contracts, instructions, lessons):
            patcher = mock.patch.object(module, "REPO_ROOT", self.root)
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = mock.patch.object(contracts, "COMMON", self.root / "_common")
        patcher.start()
        self.addCleanup(patcher.stop)

    def write(self, path: str, text: str = "") -> Path:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return target

    def lint_skill(self, body: str, name: str = "example"):
        self.write(
            "example/SKILL.md",
            f'---\nname: "{name}"\ndescription: Build tools for tests.\n---\n{body}',
        )
        report = frontmatter.Report()
        frontmatter.lint_skill(self.root / "example", report)
        return report.findings

    def test_quoted_name_whitespace_is_not_silently_normalized(self):
        for name in (" example", "example ", "example\\n"):
            with self.subTest(name=name):
                findings = self.lint_skill("", name=name)
                self.assertTrue(
                    any(f.item == "F1" and f.priority == "P0" for f in findings), findings
                )

    def test_example_headings_do_not_satisfy_required_sections(self):
        headings = "\n".join("## " + name for name in frontmatter.REQUIRED_HEADINGS)
        for opener, closer in (("```md", "```"), ("~~~~md", "~~~~")):
            with self.subTest(opener=opener):
                findings = self.lint_skill(f"{opener}\n{headings}\n{closer}\n")
                self.assertTrue(any(f.item == "ST1" for f in findings), findings)

    def test_real_headings_following_fenced_example_are_checked(self):
        headings = "\n".join("## " + name for name in frontmatter.REQUIRED_HEADINGS)
        findings = self.lint_skill("````md\n```\n## Example\n```\n````\n" + headings)
        self.assertFalse(any(f.item == "ST1" for f in findings), findings)

    def test_capabilities_example_is_not_the_skill_declaration(self):
        body = "```md\n<!--\nCAPABILITIES_SUMMARY:\nCOLLABORATION_PATTERNS:\nPROJECT_AFFINITY:\nBIDIRECTIONAL_PARTNERS:\n-->\n```\n"
        findings = self.lint_skill(body)
        self.assertTrue(any(f.item == "H1" for f in findings), findings)

    def test_unclosed_capabilities_comment_is_reported(self):
        findings = self.lint_skill("<!--\nCAPABILITIES_SUMMARY:\nCOLLABORATION_PATTERNS:\nPROJECT_AFFINITY:\nBIDIRECTIONAL_PARTNERS:\n")
        self.assertTrue(any(f.item == "H1" for f in findings), findings)

    def test_markers_after_inline_comment_do_not_count_as_inside(self):
        findings = self.lint_skill("<!-- CAPABILITIES_SUMMARY: -->\nCOLLABORATION_PATTERNS:\nPROJECT_AFFINITY:\nBIDIRECTIONAL_PARTNERS:\n")
        self.assertEqual({f.item for f in findings} & {"H2", "H3", "H4"}, {"H2", "H3", "H4"})

    def test_commented_headings_do_not_satisfy_required_sections(self):
        headings = "\n".join("## " + name for name in frontmatter.REQUIRED_HEADINGS)
        findings = self.lint_skill("<!--\n" + headings + "\n-->\n")
        self.assertTrue(any(f.item == "ST1" for f in findings), findings)

    def test_inline_capabilities_comment_remains_valid(self):
        for suffix in ("", " trailing text"):
            with self.subTest(suffix=suffix):
                findings = self.lint_skill("<!-- CAPABILITIES_SUMMARY: COLLABORATION_PATTERNS: PROJECT_AFFINITY: BIDIRECTIONAL_PARTNERS: -->" + suffix + "\n")
                self.assertFalse({f.item for f in findings} & {"H1", "H2", "H3", "H4"}, findings)

    def test_literal_comment_example_does_not_close_capabilities(self):
        findings = self.lint_skill("<!--\nCAPABILITIES_SUMMARY:\n- example: `<!-- translator comment -->`\nCOLLABORATION_PATTERNS:\nPROJECT_AFFINITY:\nBIDIRECTIONAL_PARTNERS:\n-->\n")
        self.assertFalse({f.item for f in findings} & {"H1", "H2", "H3", "H4"}, findings)

    def non_fence_prefixes(self):
        return ("```inline```\n\n", "    ```md\n\n", "<!--\n```md\n-->\n\n", "`<!--`\n\n")

    def test_non_fences_do_not_hide_real_headings(self):
        headings = "\n".join("## " + name for name in frontmatter.REQUIRED_HEADINGS)
        for prefix in self.non_fence_prefixes():
            with self.subTest(prefix=prefix):
                findings = self.lint_skill(prefix + headings)
                self.assertFalse(any(f.item == "ST1" for f in findings), findings)

    def test_non_fences_do_not_hide_contract_references(self):
        for prefix in self.non_fence_prefixes():
            with self.subTest(prefix=prefix):
                refs = contracts.named_refs(prefix + "`_common/CONTRACT.md`\n")
                self.assertIn((prefix.count("\n") + 1, "_common/CONTRACT.md"), refs)

    def test_ticked_fragment_delivers_the_named_contract(self):
        target = self.write("_common/CONTRACT.md", "# Rule\n")
        skill = self.write("example/SKILL.md", "Read `_common/CONTRACT.md#rule`.\n")
        (skill.parent / "_common").symlink_to(target.parent, target_is_directory=True)
        self.assertEqual(contracts.named_refs(skill.read_text()), [(1, "_common/CONTRACT.md")])
        self.assertEqual(contracts.Graph().depths(skill).get(target), 1)

    def test_missing_ticked_fragment_reference_is_reported(self):
        self.write("example/SKILL.md", "Read `reference/missing.md#rule`.\n")
        findings = []
        contracts.check_resolution([self.root / "example"], findings)
        self.assertTrue(any(f[1] == "CD-5" for f in findings), findings)

    def test_directory_with_markdown_suffix_cannot_deliver_a_contract(self):
        skill = self.write("example/SKILL.md", "`reference/CONTRACT.md`\n")
        directory = self.root / "example/reference/CONTRACT.md"
        directory.mkdir(parents=True)
        findings = []
        contracts.check_resolution([skill.parent], findings)
        self.assertTrue(any(f[1] == "CD-5" for f in findings), findings)
        self.assertIsNone(contracts.resolve("reference/CONTRACT.md", skill))

    def test_archive_alias_is_reported_as_an_unavailable_reference(self):
        archived = self.write(".archive/CONTRACT.md", "Retired contract\n")
        skill = self.write("example/SKILL.md", "`reference/CONTRACT.md`\n")
        reference = skill.parent / "reference"
        reference.mkdir()
        (reference / "CONTRACT.md").symlink_to(archived)
        findings = []
        contracts.check_resolution([skill.parent], findings)
        self.assertTrue(any(f[1] == "CD-5" for f in findings), findings)

    def test_real_file_reference_remains_valid(self):
        skill = self.write("example/SKILL.md", "`reference/CONTRACT.md`\n")
        self.write("example/reference/CONTRACT.md", "Contract\n")
        findings = []
        contracts.check_resolution([skill.parent], findings)
        self.assertEqual(findings, [])

    def test_instruction_file_reference_cannot_resolve_to_a_directory(self):
        (self.root / "_common/CONTRACT.md").mkdir(parents=True)
        findings = instructions.check_paths(self.root / "AGENTS.md", "`_common/CONTRACT.md`")
        self.assertTrue(any(f[1] == "I2" for f in findings), findings)

    def test_instruction_reference_cannot_escape_the_repository(self):
        with tempfile.TemporaryDirectory(prefix="audit-outside-") as outside:
            target = Path(outside) / "CONTRACT.md"
            target.write_text("Outside repository\n", encoding="utf-8")
            (self.root / "_common").mkdir()
            (self.root / "_common/CONTRACT.md").symlink_to(target)
            findings = instructions.check_paths(self.root / "AGENTS.md", "`_common/CONTRACT.md`")
            self.assertTrue(any(f[1] == "I2" for f in findings), findings)

    def test_internal_instruction_symlink_remains_valid(self):
        target = self.write("_common/CONTRACT.md", "Contract\n")
        (self.root / "links").mkdir()
        (self.root / "links/CONTRACT.md").symlink_to(target)
        findings = instructions.check_paths(self.root / "AGENTS.md", "`links/CONTRACT.md`")
        self.assertEqual(findings, [])

    def lesson_register(self):
        self.write("_common/check.py", "pass\n")
        return (
            "| ID | What happened | F | Mechanism | Where | Added |\n"
            "|---|---|---|---|---|---|\n"
            "| L001 | An invalid file passed | F3 | A checker rejects invalid input | "
            f"`_common/check.py` | {dt.date.today().isoformat()} |\n"
        )

    def test_a_lesson_example_is_not_a_registered_lesson(self):
        register = self.lesson_register()
        for opener, closer in (("```md", "```"), ("~~~~md", "~~~~")):
            with self.subTest(opener=opener):
                findings = lessons.check(f"{opener}\n{register}{closer}\n")
                self.assertTrue(any(f[1] == "LS-5" for f in findings), findings)

    def test_fenced_lesson_example_does_not_duplicate_a_real_id(self):
        register = self.lesson_register()
        findings = lessons.check(register + "\n````md\n```\n" + register + "```\n````\n")
        self.assertEqual(findings, [])

    def test_non_fences_do_not_hide_the_lesson_register(self):
        register = self.lesson_register()
        for prefix in self.non_fence_prefixes():
            with self.subTest(prefix=prefix):
                self.assertEqual(lessons.check(prefix + register), [])


if __name__ == "__main__":
    unittest.main()
