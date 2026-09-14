#!/usr/bin/env python3
"""Exercise the real pre-commit hook with partially staged changes."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
MAKE = shutil.which("make")
CHECKERS = (
    "lint-frontmatter", "lint-project-local", "validate-recipes", "routing-oracle",
    "lint-instructions", "lint-contracts", "lint-lessons", "task-battery-check",
)


@unittest.skipUnless(MAKE and shutil.which("git"), "make and git are required")
class StagedHookRegressionTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="staged-hook-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.repo = self.root / "source with spaces"
        self.repo.mkdir()
        self.snapshots = self.root / "temporary snapshots"
        self.snapshots.mkdir()
        self.env = {
            key: value for key, value in os.environ.items()
            if not key.startswith("GIT_") and key not in ("MAKEFLAGS", "MFLAGS", "MAKELEVEL")
        }
        self.env.update(
            GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
            TMPDIR=str(self.snapshots),
        )
        shutil.copyfile(REPO_ROOT / "Makefile", self.repo / "Makefile")
        scripts = self.repo / "_common" / "scripts"
        scripts.mkdir(parents=True)
        for name in CHECKERS:
            (scripts / f"{name}.py").write_text("# fixture checker\n")
        (scripts / "lint-frontmatter.py").write_text(
            "import os\nfrom pathlib import Path\n"
            "assert Path('alpha/SKILL.md').read_text().startswith('valid'), 'invalid staged skill'\n"
            "assert not Path('untracked.txt').exists(), 'untracked files reached validation'\n"
            "assert not any(os.environ.get(key) for key in "
            "('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')), 'Git environment leaked'\n"
        )
        self.skill = self.repo / "alpha" / "SKILL.md"
        self.skill.parent.mkdir()
        self.skill.write_text("valid baseline\n")
        for args in (
            ("init", "--quiet"),
            ("config", "user.name", "Hook Test"),
            ("config", "user.email", "hook-test@example.invalid"),
            ("add", "."),
            ("commit", "--quiet", "-m", "test: create fixture"),
        ):
            self.assert_ok(self.run_command("git", *args))
        self.assert_ok(self.run_command(MAKE, "--no-print-directory", "hooks"))

    def run_command(self, *args):
        return subprocess.run(
            args, cwd=self.repo, env=self.env, text=True, capture_output=True,
        )

    def assert_ok(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def git_output(self, *args):
        result = self.run_command("git", *args)
        self.assert_ok(result)
        return result.stdout

    def test_invalid_index_cannot_be_hidden_by_valid_unstaged_content(self):
        head = self.git_output("rev-parse", "HEAD")
        self.skill.write_text("invalid staged content\n")
        self.assert_ok(self.run_command("git", "add", "alpha/SKILL.md"))
        self.skill.write_text("valid unstaged content\n")
        untracked = self.repo / "untracked.txt"
        untracked.write_text("keep me\n")
        result = self.run_command("git", "commit", "-m", "test: invalid staged change")
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("invalid staged skill", result.stdout + result.stderr)
        self.assertEqual(self.git_output("rev-parse", "HEAD"), head)
        self.assertEqual(self.git_output("show", ":alpha/SKILL.md"), "invalid staged content\n")
        self.assertEqual(self.skill.read_text(), "valid unstaged content\n")
        self.assertEqual(untracked.read_text(), "keep me\n")
        self.assertEqual(list(self.snapshots.iterdir()), [])

    def test_valid_index_commits_without_changing_unstaged_or_untracked_files(self):
        self.skill.write_text("valid staged content\n")
        self.assert_ok(self.run_command("git", "add", "alpha/SKILL.md"))
        self.skill.write_text("invalid unstaged content\n")
        untracked = self.repo / "untracked.txt"
        untracked.write_text("keep me\n")
        self.assert_ok(self.run_command("git", "commit", "-m", "test: valid staged change"))
        self.assertEqual(self.git_output("show", "HEAD:alpha/SKILL.md"), "valid staged content\n")
        self.assertEqual(self.skill.read_text(), "invalid unstaged content\n")
        self.assertEqual(untracked.read_text(), "keep me\n")
        self.assertEqual(list(self.snapshots.iterdir()), [])

    def test_partial_commit_uses_the_temporary_index_and_clears_git_environment(self):
        self.skill.write_text("valid partial commit\n")
        staged = self.repo / "another.txt"
        staged.write_text("preserve this staged change\n")
        self.assert_ok(self.run_command("git", "add", "another.txt"))
        self.env.update(GIT_DIR=str(self.repo / ".git"), GIT_WORK_TREE=str(self.repo))
        self.assert_ok(self.run_command(
            "git", "commit", "--only", "-m", "test: partial commit", "--", "alpha/SKILL.md",
        ))
        self.assertEqual(self.git_output("show", "HEAD:alpha/SKILL.md"), "valid partial commit\n")
        self.assertEqual(self.git_output("diff", "--cached", "--name-only"), "another.txt\n")
        self.assertEqual(list(self.snapshots.iterdir()), [])

    def test_hook_uses_a_writable_directory_when_tmpdir_is_unavailable(self):
        self.env["TMPDIR"] = str(self.root / "missing" / "temporary")
        self.skill.write_text("valid with unavailable TMPDIR\n")
        self.assert_ok(self.run_command("git", "add", "alpha/SKILL.md"))
        self.assert_ok(self.run_command("git", "commit", "-m", "test: unavailable temporary directory"))
        self.assertEqual(
            self.git_output("show", "HEAD:alpha/SKILL.md"),
            "valid with unavailable TMPDIR\n",
        )
        self.assertEqual(list(self.repo.glob("agent-skills-index.*")), [])


if __name__ == "__main__":
    unittest.main()
