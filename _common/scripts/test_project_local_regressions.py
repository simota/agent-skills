#!/usr/bin/env python3
"""Regression tests for project-local skill validation."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("lint-project-local.py")
SPEC = importlib.util.spec_from_file_location("lint_project_local", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ProjectLocalValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        (self.root / ".claude/skills").mkdir(parents=True)
        (self.root / ".agents/skills").mkdir(parents=True)
        (self.root / "_common").mkdir()
        (self.root / "_common/OPERATIONAL.md").write_text(
            "# Operational\n", encoding="utf-8"
        )
        (self.root / "_common/PROJECT_LOCAL_SKILLS.md").write_text(
            """# Project-Local Skills

## Registry

| Skill | Responsibility |
|-------|----------------|
| `demo` | fixture |
""",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _write_skill(
        self, root: Path, body: str = "See `_common/OPERATIONAL.md`."
    ) -> Path:
        skill = root / "demo"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\nname: demo\ndescription: fixture\n---\n\n" + body + "\n",
            encoding="utf-8",
        )
        (skill / "_common").symlink_to("../../../_common", target_is_directory=True)
        return skill

    def _write_pair(self) -> tuple[Path, Path]:
        canonical = self._write_skill(self.root / ".claude/skills")
        mirror = self._write_skill(self.root / ".agents/skills")
        return canonical, mirror

    def _rules(self) -> set[str]:
        return {finding.rule for finding in MODULE.check(self.root)}

    def test_clean_pair_passes(self) -> None:
        self._write_pair()
        self.assertEqual(MODULE.check(self.root), [])

    def test_registry_catches_symmetric_deletion(self) -> None:
        self.assertIn("PL-1", self._rules())

    def test_missing_mirror_skill_is_rejected(self) -> None:
        self._write_skill(self.root / ".claude/skills")
        self.assertIn("PL-1", self._rules())

    def test_content_drift_is_rejected(self) -> None:
        _, mirror = self._write_pair()
        (mirror / "SKILL.md").write_text("drift\n", encoding="utf-8")
        self.assertIn("PL-2", self._rules())

    def test_missing_shared_link_is_rejected(self) -> None:
        canonical, mirror = self._write_pair()
        (canonical / "_common").unlink()
        (mirror / "_common").unlink()
        self.assertIn("PL-3", self._rules())

    def test_wrong_shared_link_target_is_rejected(self) -> None:
        canonical, mirror = self._write_pair()
        wrong = self.root / "wrong-common"
        wrong.mkdir()
        for skill in (canonical, mirror):
            (skill / "_common").unlink()
            (skill / "_common").symlink_to(wrong, target_is_directory=True)
        self.assertIn("PL-3", self._rules())


if __name__ == "__main__":
    unittest.main()
