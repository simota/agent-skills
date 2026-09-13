#!/usr/bin/env python3
"""Run the complete loop runner against Git repositories and saved checkpoints."""

from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest

from test_skill_templates import ROOT, fixture_environment, template


class FullLoopRegressions(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="full-loop-", dir=ROOT.parent)
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        self.loop = self.repo / ".loop"
        self.loop.mkdir()
        (self.loop / "goal.md").write_text("# Goal\n\n## Objective\nFinish the fixture\n")
        (self.loop / "progress.md").write_text("# Progress\n")
        (self.loop / "run-loop.sh").write_text(template("run-loop.sh"))
        (self.repo / ".gitignore").write_text(".loop/\n")
        (self.repo / "source.py").write_text("value = 1\n")
        (self.repo / "user.txt").write_text("baseline\n")
        (self.repo / "nested").mkdir()
        (self.repo / "nested/local.py").write_text("value = 1\n")
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("add", ".")
        self.git("commit", "-qm", "initial")

    def git(self, *args, cwd=None):
        return subprocess.check_output(
            ["git", *args], cwd=cwd or self.repo, env=fixture_environment(),
            text=True, stderr=subprocess.STDOUT,
        ).strip()

    def run_loop(self, body='touch "$LOOP_DIR/done.md"\n', *, cwd=None, **overrides):
        executor = self.loop / "executor.sh"
        executor.write_text("#!/bin/bash\nset -euo pipefail\n" + body)
        env = {
            **fixture_environment(), "LOOP_DIR": str(self.loop),
            "EXEC_CMD": "bash " + shlex.quote(str(executor)),
            "AUTOCOMMIT": "true", "BRANCH_ISOLATION": "false",
            "MAX_ITERATIONS": "1", "RETRY_LIMIT": "1",
            "SQUASH_ON_DONE": "false", "SQUASH_MSG_ENGINE": "heuristic",
            **overrides,
        }
        return subprocess.run(
            ["bash", str(self.loop / "run-loop.sh")], cwd=cwd or self.repo,
            env=env, text=True, capture_output=True, timeout=15,
        )

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def state(self):
        return dict(line.split("=", 1) for line in (self.loop / "state.env").read_text().splitlines())

    def test_subdirectory_autocommit_keeps_root_relative_paths_consistent(self):
        (self.repo / "user.txt").write_text("user staged\n")
        self.git("add", "user.txt")
        result = self.run_loop(
            'echo "value = 2" > local.py\n'
            'echo "value = 3" > ../source.py\n'
            'echo created > ../new.txt\n'
            'touch "$LOOP_DIR/done.md"\n', cwd=self.repo / "nested",
        )
        self.assert_success(result)
        self.assertEqual(self.git("show", "HEAD:nested/local.py"), "value = 2")
        self.assertEqual(self.git("show", "HEAD:source.py"), "value = 3")
        self.assertEqual(self.git("show", "HEAD:new.txt"), "created")
        self.assertEqual(self.git("show", "HEAD:user.txt"), "baseline")
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "user.txt")

    def test_subdirectory_placeholder_check_scans_changed_root_source(self):
        result = self.run_loop(
            'printf "def pending():\\n    pass\\n" > ../source.py\n'
            'touch "$LOOP_DIR/done.md"\n', cwd=self.repo / "nested", AUTOCOMMIT="false",
        )
        self.assert_success(result)
        self.assertEqual(self.state()["LAST_STATUS"], "CONTINUE")

    def test_worktree_rebase_is_detected_in_preflight_and_health_check(self):
        worktree = Path(self.temp.name) / "worktree"
        self.git("worktree", "add", "-qb", "work", str(worktree))
        rebase_dir = Path(self.git("rev-parse", "--git-path", "rebase-merge", cwd=worktree))
        rebase_dir.mkdir()
        for skip in ("false", "true"):
            with self.subTest(skip_preflight=skip):
                result = self.run_loop(
                    'touch "$LOOP_DIR/executed"\n', cwd=worktree / "nested",
                    SKIP_PREFLIGHT=skip,
                )
                self.assertIn("Git rebase in progress", result.stdout)
                self.assertFalse((self.loop / "executed").exists())
                self.assertFalse((self.loop / ".run-loop.lock").exists())
                if skip == "false":
                    self.assertNotEqual(result.returncode, 0)
                else:
                    self.assert_success(result)
                    self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")

    def test_no_change_completion_does_not_attempt_an_empty_squash_commit(self):
        result = self.run_loop(BRANCH_ISOLATION="true", SQUASH_ON_DONE="true")
        self.assert_success(result)
        self.assertIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertEqual(self.git("branch", "--show-current"), "main")
        self.assertEqual(self.git("rev-list", "--count", "HEAD"), "1")
        self.assertEqual(self.git("branch", "--list", "loop/iter-*", "loop/summary-*"), "")

    def test_done_checkpoint_is_idempotent_after_iteration_branch_deleted(self):
        result = self.run_loop(
            'echo "value = 2" > source.py\ntouch "$LOOP_DIR/done.md"\n',
            BRANCH_ISOLATION="true", SQUASH_ON_DONE="true",
        )
        self.assert_success(result)
        first_head = self.git("rev-parse", "HEAD")
        result = self.run_loop(
            'touch "$LOOP_DIR/unexpected-execution"\n',
            BRANCH_ISOLATION="true", SQUASH_ON_DONE="true",
        )
        self.assert_success(result)
        self.assertIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertEqual(self.git("rev-parse", "HEAD"), first_head)
        self.assertEqual(self.git("branch", "--show-current"), "loop/summary-loop")
        self.assertEqual(self.git("branch", "--list", "loop/iter-*"), "")
        self.assertFalse((self.loop / "unexpected-execution").exists())

    def test_squash_preserves_preexisting_staged_changes(self):
        (self.repo / "user.txt").write_text("user staged\n")
        self.git("add", "user.txt")
        (self.repo / "user.txt").write_text("user unstaged\n")
        result = self.run_loop(
            'echo "value = 2" > source.py\ntouch "$LOOP_DIR/done.md"\n',
            BRANCH_ISOLATION="true", SQUASH_ON_DONE="true",
        )
        self.assert_success(result)
        self.assertEqual(self.git("show", "HEAD:source.py"), "value = 2")
        self.assertEqual(self.git("show", "HEAD:user.txt"), "baseline")
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "user.txt")
        self.assertEqual(self.git("show", ":user.txt"), "user staged")
        self.assertEqual((self.repo / "user.txt").read_text(), "user unstaged\n")

    def test_squash_conflict_reports_failure_and_preserves_prior_work(self):
        self.git("branch", "loop/iter-loop")
        (self.repo / "source.py").write_text("value = 3\n")
        self.git("commit", "-qam", "origin changed")
        self.git("checkout", "-q", "loop/iter-loop")
        (self.loop / "state.env").write_text("NEXT_ITERATION=1\nLAST_STATUS=READY\nORIGIN_BRANCH=main\n")
        (self.repo / "user.txt").write_text("user staged\n")
        self.git("add", "user.txt")
        result = self.run_loop(
            'echo "value = 2" > source.py\ntouch "$LOOP_DIR/done.md"\n',
            BRANCH_ISOLATION="true", SQUASH_ON_DONE="true",
        )
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("[BRANCH:CONFLICT]", result.stdout)
        self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertEqual(self.git("diff", "--name-only", "--diff-filter=U"), "source.py")
        # The suggested squash-abort command works without a MERGE_HEAD.
        self.git("reset", "--merge")
        self.git("checkout", "-q", "loop/iter-loop")
        self.git("stash", "pop", "--index")
        self.assertEqual(self.git("show", ":user.txt"), "user staged")

    def test_reverted_iteration_commits_finish_without_an_empty_summary(self):
        result = self.run_loop(
            'if [[ ! -f "$LOOP_DIR/first-pass" ]]; then\n'
            '  echo "value = 2" > source.py\n  touch "$LOOP_DIR/first-pass"\n'
            'else\n  echo "value = 1" > source.py\n  touch "$LOOP_DIR/done.md"\nfi\n',
            BRANCH_ISOLATION="true", SQUASH_ON_DONE="true", MAX_ITERATIONS="2",
        )
        self.assert_success(result)
        self.assertIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertEqual(self.git("branch", "--show-current"), "main")
        self.assertEqual(self.git("rev-list", "--count", "HEAD"), "1")

    def test_bootstrap_treats_quoted_verification_command_as_data(self):
        script = template("bootstrap.sh")
        replacements = {
            "VERIFY_CMD": 'python -c "print(1)" && echo "$(touch bootstrap-command-ran)"',
            "VERIFY_CHECKS": 'run_check "works" true',
            "RUN_LOOP_CONTENT": "#!/bin/bash\ntrue", "NOTIFY_CONTENT": "#!/bin/bash\ntrue",
        }
        for key, value in replacements.items():
            script = script.replace("{{" + key + "}}", value)
        path = self.loop / "bootstrap.sh"
        path.write_text(script)
        result = subprocess.run(
            ["bash", str(path), str(self.loop)], cwd=self.repo, env=fixture_environment(),
            text=True, capture_output=True, timeout=10,
        )
        self.assert_success(result)
        self.assertFalse((self.repo / "bootstrap-command-ran").exists())
        self.assertTrue((self.loop / "verify.sh").exists())

    def test_circuit_open_stops_retries_in_the_current_iteration(self):
        result = self.run_loop(
            'echo attempt >> "$LOOP_DIR/attempts"\nexit 1\n',
            RETRY_LIMIT="3", RETRY_BACKOFF_BASE="0", CIRCUIT_THRESHOLD="1",
        )
        self.assert_success(result)
        self.assertEqual((self.loop / "attempts").read_text().splitlines(), ["attempt"])
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")

    def test_failed_half_open_probe_cannot_retry_and_close_the_circuit(self):
        (self.loop / ".circuit-state").write_text(
            "CB_STATE=OPEN\nCB_FAIL_COUNT=3\nCB_LAST_SIGNATURE=exit_1\nCB_LAST_UPDATED=0\n"
        )
        result = self.run_loop(
            'if [[ ! -f "$LOOP_DIR/attempts" ]]; then\n'
            '  echo attempt > "$LOOP_DIR/attempts"\n  exit 1\nfi\n'
            'touch "$LOOP_DIR/done.md"\n',
            RETRY_LIMIT="3", RETRY_BACKOFF_BASE="0", CIRCUIT_COOLDOWN="300",
        )
        self.assert_success(result)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")
        self.assertFalse((self.loop / "done.md").exists())


if __name__ == "__main__":
    unittest.main()
