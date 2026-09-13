#!/usr/bin/env python3
"""Exercise installation and hook commands in disposable repositories only."""

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
    "lint-frontmatter", "validate-recipes", "routing-oracle",
    "lint-instructions", "lint-contracts", "lint-lessons", "task-battery-check",
)


@unittest.skipUnless(MAKE and shutil.which("git"), "make and git are required")
class InstallRegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="install-regressions-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "source with spaces"
        self.repo.mkdir()
        shutil.copyfile(REPO_ROOT / "Makefile", self.repo / "Makefile")
        self.scripts = self.repo / "_common" / "scripts"
        self.scripts.mkdir(parents=True)
        for checker in CHECKERS:
            (self.scripts / f"{checker}.py").write_text("print('checked')\n")
        (self.repo / "alpha").mkdir()
        self.cli = self.root / "cli with spaces" / "skills"
        self.cli.parent.mkdir()
        self.env = os.environ.copy()
        # Git exports repository paths into hooks; inherited paths must never
        # redirect these fixture commands into the repository being committed.
        for key in list(self.env):
            if key.startswith("GIT_") or key in ("MAKEFLAGS", "MFLAGS", "MAKELEVEL"):
                self.env.pop(key)
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)

    def run_make(self, target: str, *, repo: Path | None = None):
        return subprocess.run(
            [MAKE, "--no-print-directory", target, f"CLAUDE_DIR={self.cli}"],
            cwd=repo or self.repo, env=self.env, text=True, capture_output=True,
        )

    def assert_ok(self, result) -> None:
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def git(self, *args: str, repo: Path | None = None) -> str:
        result = subprocess.run(
            ["git", *args], cwd=repo or self.repo, env=self.env,
            text=True, capture_output=True,
        )
        self.assert_ok(result)
        return result.stdout.strip()

    def initialize_git(self) -> None:
        self.git("init", "--quiet")
        self.git("config", "user.name", "Install Test")
        self.git("config", "user.email", "install-test@example.invalid")
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "test: create fixture")

    def stub_command(self, name: str, body: str) -> None:
        bin_dir = self.root / "bin"
        bin_dir.mkdir(exist_ok=True)
        script = bin_dir / name
        script.write_text("#!/bin/sh\n" + body + "\n")
        script.chmod(0o755)
        self.env["PATH"] = str(bin_dir) + os.pathsep + os.environ["PATH"]

    def test_link_unlink_preserve_foreign_entries_and_prune_stale_links(self):
        self.cli.mkdir()
        (self.cli / "alpha").mkdir()
        foreign = self.root / "foreign"
        foreign.mkdir()
        (self.cli / "foreign").symlink_to(foreign, target_is_directory=True)
        (self.repo / "beta").mkdir()
        (self.repo / ".private").mkdir()

        self.assert_ok(self.run_make("link-claude"))
        self.assert_ok(self.run_make("link-claude"))
        self.assertEqual((self.cli / "beta").resolve(), self.repo / "beta")
        self.assertFalse((self.cli / "alpha").is_symlink())
        self.assertFalse((self.cli / ".private").exists())

        (self.repo / "beta").rmdir()
        self.assert_ok(self.run_make("link-claude"))
        self.assertFalse((self.cli / "beta").is_symlink())
        self.assert_ok(self.run_make("unlink-claude"))
        self.assertEqual(sorted(p.name for p in self.cli.iterdir()), ["alpha", "foreign"])

    def test_link_reports_a_failed_symlink_command(self):
        self.stub_command("ln", "echo 'fixture: cannot create link' >&2; exit 23")
        result = self.run_make("link-claude")
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("fixture: cannot create link", result.stderr)
        self.assertNotIn("linked  ", result.stdout)

    def test_unlink_reports_a_failed_removal(self):
        self.assert_ok(self.run_make("link-claude"))
        self.stub_command("rm", "echo 'fixture: cannot remove link' >&2; exit 23")
        result = self.run_make("unlink-claude")
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("fixture: cannot remove link", result.stderr)

    def test_link_rejects_a_target_inside_the_repository(self):
        self.cli = self.repo / "installed"
        result = self.run_make("link-claude")
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(self.cli.exists())

    def test_validate_accepts_a_repository_path_with_spaces(self):
        self.assert_ok(self.run_make("validate"))

    def test_commands_treat_quotes_in_paths_as_literal_characters(self):
        quoted = self.root / "source with 'single' and \"double\" quotes"
        self.repo.rename(quoted)
        self.repo = quoted
        self.cli = self.cli.parent / "skills with 'single' and \"double\" quotes"
        self.assert_ok(self.run_make("link-claude"))
        self.assertEqual((self.cli / "alpha").resolve(), self.repo / "alpha")
        self.assert_ok(self.run_make("validate"))
        self.assert_ok(self.run_make("unlink-claude"))

    def test_test_target_discovers_new_suites(self):
        (self.scripts / "test_extra.py").write_text(
            "import unittest\nclass Extra(unittest.TestCase):\n"
            "    def test_extra(self): self.fail('fixture discovered')\n"
        )
        result = self.run_make("test")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("fixture discovered", result.stdout + result.stderr)

    def test_hook_installs_in_a_git_worktree(self):
        self.initialize_git()
        worktree = self.root / "linked worktree"
        self.git("worktree", "add", "--quiet", "--detach", str(worktree))
        self.assert_ok(self.run_make("hooks", repo=worktree))
        self.assertTrue((self.repo / ".git" / "hooks" / "pre-commit").is_file())
        self.assertTrue((worktree / ".git").is_file())

    def test_shared_hook_checks_the_current_worktree(self):
        self.initialize_git()
        self.assert_ok(self.run_make("hooks"))
        worktree = self.root / "linked worktree"
        self.git("worktree", "add", "--quiet", "--detach", str(worktree))
        (worktree / "marker.txt").write_text("staged in linked worktree\n")
        self.git("add", "marker.txt", repo=worktree)
        self.stub_command(
            "make", 'printf "%s\\n" "$@" > "$INSTALL_TEST_LOG"\n'
            'cat "$2/marker.txt" >> "$INSTALL_TEST_LOG"',
        )
        log = self.root / "hook.log"
        self.env["INSTALL_TEST_LOG"] = str(log)
        hook = self.repo / ".git" / "hooks" / "pre-commit"
        result = subprocess.run([str(hook)], cwd=worktree, env=self.env, capture_output=True, text=True)
        self.assert_ok(result)
        args = log.read_text().splitlines()
        self.assertEqual(args[0], "-C")
        self.assertEqual(args[2:], ["--no-print-directory", "validate", "staged in linked worktree"])
        self.assertNotEqual(args[1], str(worktree))
        self.assertFalse(Path(args[1]).exists(), "the index snapshot must be removed")

    def test_hooks_respect_core_hooks_path(self):
        self.initialize_git()
        self.git("config", "core.hooksPath", "custom hooks")
        self.assert_ok(self.run_make("hooks"))
        self.assertTrue((self.repo / "custom hooks" / "pre-commit").is_file())
        result = self.run_make("validate")
        self.assert_ok(result)
        self.assertIn("hooks on", result.stdout)

    def test_hooks_preserve_an_existing_custom_hook(self):
        self.initialize_git()
        hook = self.repo / ".git" / "hooks" / "pre-commit"
        original = "#!/bin/sh\nprintf 'custom checks\\n'\n"
        hook.write_text(original)
        result = self.run_make("hooks")
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(hook.read_text(), original)

    def test_executable_changes_run_the_full_hook_check(self):
        self.initialize_git()
        self.assert_ok(self.run_make("hooks"))
        self.stub_command("make", 'printf "%s\\n" "$@" > "$INSTALL_TEST_LOG"')
        log = self.root / "hook.log"
        self.env["INSTALL_TEST_LOG"] = str(log)
        hook = self.repo / ".git" / "hooks" / "pre-commit"
        for relative in (
            "Makefile", "requirements-checks.txt", "index.html",
            "launch/scripts/generate-report.js", "launch/templates/client-report.html",
            "_templates/learning-loop-kit/_scripts/check-rendered.sh",
        ):
            with self.subTest(path=relative):
                target = self.repo / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("a") as stream:
                    stream.write("\n# staged fixture change\n")
                self.git("add", relative)
                result = subprocess.run([str(hook)], cwd=self.repo, env=self.env, capture_output=True, text=True)
                self.assert_ok(result)
                self.assertEqual(log.read_text().splitlines()[-1], "check")
                self.git("reset", "--quiet")


if __name__ == "__main__":
    unittest.main()
