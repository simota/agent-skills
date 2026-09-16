#!/usr/bin/env python3
"""Protect installation boundaries and hook dispatch in disposable repositories."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
MAKE = shutil.which("make")


@unittest.skipUnless(MAKE and shutil.which("git"), "make and git are required")
class InstallBoundaryTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="install-boundaries-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.repo = self.root / "source"
        self.repo.mkdir()
        shutil.copyfile(REPO_ROOT / "Makefile", self.repo / "Makefile")
        (self.repo / "alpha").mkdir()
        self.cli = self.root / "cli" / "skills"
        self.cli.mkdir(parents=True)
        self.env = {
            key: value for key, value in os.environ.items()
            if not key.startswith("GIT_") and key not in ("MAKEFLAGS", "MFLAGS", "MAKELEVEL")
        }
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)

    def run_command(self, *args):
        return subprocess.run(
            args, cwd=self.repo, env=self.env, text=True, capture_output=True,
        )

    def make(self, target):
        return self.run_command(
            MAKE, "--no-print-directory", target, f"CLAUDE_DIR={self.cli}",
            f"CODEX_DIR={self.root / 'codex' / 'skills'}",
            f"AGY_DIR={self.root / 'agy' / 'skills'}",
        )

    def assert_ok(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def codex_default(self, home, target="link-codex"):
        return self.run_command(MAKE, "--no-print-directory", target, f"HOME={home}")

    def test_codex_default_uses_agents_root_and_preserves_legacy(self):
        home = self.root / "home"
        legacy = home / ".codex" / "skills"
        legacy.mkdir(parents=True)
        (legacy / "foreign.md").write_text("preserve\n")
        self.assert_ok(self.codex_default(home))
        current = home / ".agents" / "skills"
        self.assertEqual((current / "alpha").resolve(), self.repo / "alpha")
        (current / "foreign").mkdir()
        self.assert_ok(self.codex_default(home))
        self.assert_ok(self.codex_default(home, "unlink-codex"))
        self.assertFalse((current / "alpha").is_symlink())
        self.assertTrue((current / "foreign").is_dir())
        self.assertEqual((legacy / "foreign.md").read_text(), "preserve\n")

    def test_codex_default_skips_when_cli_and_shared_root_are_absent(self):
        home = self.root / "home"
        home.mkdir()
        result = self.codex_default(home)
        self.assert_ok(result)
        self.assertIn("skip", result.stdout)
        self.assertFalse((home / ".agents").exists())

    def test_codex_default_refuses_first_use_parent_inside_repository(self):
        home = self.repo / "home"
        (home / ".codex").mkdir(parents=True)
        result = self.codex_default(home)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse((home / ".agents").exists())

    def test_codex_default_refuses_parent_symlink_into_repository(self):
        home = self.root / "home"
        home.mkdir()
        (home / ".agents").symlink_to(self.repo, target_is_directory=True)
        result = self.codex_default(home)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse((self.repo / "skills").exists())

    def test_unlink_rejects_a_directory_inside_the_source_tree(self):
        self.cli = self.repo / "alpha"
        contract = self.cli / "shared"
        contract.symlink_to(self.repo / "shared")
        result = self.make("unlink-claude")
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(contract.is_symlink())

    def test_unlink_rejects_a_source_directory_through_an_ancestor_symlink(self):
        alias = self.root / "source alias"
        alias.symlink_to(self.repo, target_is_directory=True)
        self.cli = alias / "alpha"
        contract = self.cli / "shared"
        contract.symlink_to(self.repo / "shared")
        result = self.make("unlink-claude")
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(contract.is_symlink())

    def test_link_and_unlink_preserve_foreign_links_with_a_source_prefix(self):
        outside = self.root / "outside"
        outside.mkdir()
        for command in ("link-claude", "unlink-claude"):
            for name in ("outside", "missing"):
                with self.subTest(command=command, target=name):
                    link = self.cli / "foreign"
                    link.symlink_to(f"{self.repo}/../{name}")
                    self.assert_ok(self.make(command))
                    self.assertTrue(link.is_symlink())
                    link.unlink()

    def test_unlink_preserves_custom_aliases_into_the_source(self):
        alias = self.cli / "custom-name"
        alias.symlink_to(self.repo / "alpha")
        self.assert_ok(self.make("unlink-claude"))
        self.assertTrue(alias.is_symlink())

    def test_status_counts_only_links_managed_by_the_installer(self):
        self.assert_ok(self.make("link-claude"))
        (self.cli / "custom-name").symlink_to(self.repo / "alpha")
        (self.cli / "foreign").symlink_to(f"{self.repo}/../outside")
        (self.cli / "removed").symlink_to(self.repo / "removed")
        result = self.make("status")
        self.assert_ok(result)
        self.assertIn("1/1 linked", result.stdout)

    def test_hook_detects_quoted_paths_and_workflow_changes(self):
        for args in (
            ("init", "--quiet"),
            ("config", "user.name", "Install Test"),
            ("config", "user.email", "install-test@example.invalid"),
            ("add", "."),
            ("commit", "--quiet", "-m", "test: create fixture"),
        ):
            self.assert_ok(self.run_command("git", *args))
        self.assert_ok(self.make("hooks"))
        bin_dir = self.root / "bin"
        bin_dir.mkdir()
        stub = bin_dir / "make"
        stub.write_text('#!/bin/sh\nprintf "%s\\n" "$@" > "$INSTALL_TEST_LOG"\n')
        stub.chmod(0o755)
        log = self.root / "hook.log"
        self.env.update(PATH=str(bin_dir) + os.pathsep + self.env["PATH"], INSTALL_TEST_LOG=str(log))
        hook = self.repo / ".git" / "hooks" / "pre-commit"
        for relative, expected in (
            ("launch/scripts/日本語.js", "check"),
            ("launch/templates/line\nbreak.html", "check"),
            (".github/workflows/checks.yml", "check"),
            ("README.md", "validate"),
        ):
            with self.subTest(path=relative):
                path = self.repo / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture\n")
                self.assert_ok(self.run_command("git", "add", "--", relative))
                self.assert_ok(self.run_command(str(hook)))
                self.assertEqual(log.read_text().splitlines()[-1], expected)
                self.assert_ok(self.run_command("git", "reset", "--quiet"))


if __name__ == "__main__":
    unittest.main()
