#!/usr/bin/env python3
"""Verify installer path checks before a source tree can be modified."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
MAKE = shutil.which("make")


@unittest.skipUnless(MAKE, "make is required")
class InstallPathRegressionTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="install-paths-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.repo = self.root / "source"
        self.repo.mkdir()
        shutil.copyfile(REPO_ROOT / "Makefile", self.repo / "Makefile")
        self.skill = self.repo / "alpha"
        self.skill.mkdir()
        self.env = {
            key: value for key, value in os.environ.items()
            if key not in ("MAKEFLAGS", "MFLAGS", "MAKELEVEL")
        }

    def test_link_rejects_a_source_alias_with_trailing_slashes(self):
        alias = self.root / "source alias"
        alias.symlink_to(self.skill, target_is_directory=True)
        for suffix in ("/", "///"):
            with self.subTest(suffix=suffix):
                result = subprocess.run(
                    [MAKE, "--no-print-directory", "link-claude", f"CLAUDE_DIR={alias}{suffix}"],
                    cwd=self.repo, env=self.env, text=True, capture_output=True,
                )
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("inside this repo", result.stdout)
                self.assertEqual(list(self.skill.iterdir()), [])
                self.assertTrue(alias.is_symlink())


if __name__ == "__main__":
    unittest.main()
