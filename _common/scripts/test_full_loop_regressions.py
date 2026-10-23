#!/usr/bin/env python3
"""Run the complete loop runner against Git repositories and saved checkpoints."""

import hashlib
import os
import shutil
import signal
import sys
from pathlib import Path
import shlex
import subprocess
import tempfile
import time
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

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
        # Sanitized PATH: claude/codex resolve to guards that record any call, so a
        # fixture can never reach a real assistant CLI.
        self.guard = Path(self.temp.name) / "guard-bin"
        self.guard.mkdir()
        for name in ("claude", "codex"):
            stub = self.guard / name
            stub.write_text(f'#!/bin/sh\necho {name} >> "{self.guard}/invoked"\nexit 97\n')
            stub.chmod(0o755)
        self.safe_path = f"{self.guard}{os.pathsep}{os.environ['PATH']}"
        self.addCleanup(lambda: self.assertFalse(
            (self.guard / "invoked").exists(), "a fixture reached an assistant CLI"))

    def git(self, *args, cwd=None):
        return subprocess.check_output(
            ["git", *args], cwd=cwd or self.repo, env=fixture_environment(),
            text=True, stderr=subprocess.STDOUT,
        ).strip()

    def loop_env(self, body, **overrides):
        executor = self.loop / "executor.sh"
        executor.write_text("#!/bin/bash\nset -euo pipefail\n" + body)
        # SQUASH_MSG_ENGINE=none: fixtures never reach a real claude/codex CLI.
        return {
            **fixture_environment(), "LOOP_DIR": str(self.loop),
            "EXEC_CMD": "bash " + shlex.quote(str(executor)),
            "AUTOCOMMIT": "true", "BRANCH_ISOLATION": "false",
            "MAX_ITERATIONS": "1", "RETRY_LIMIT": "1",
            "SQUASH_ON_DONE": "false", "SQUASH_MSG_ENGINE": "none",
            "ALLOW_UNBOUNDED_RUN": "true", "PATH": self.safe_path,
            **overrides,
        }

    def run_loop(self, body='touch "$LOOP_DIR/done.md"\n', *, cwd=None, **overrides):
        return subprocess.run(
            ["bash", str(self.loop / "run-loop.sh")], cwd=cwd or self.repo,
            env=self.loop_env(body, **overrides), text=True, capture_output=True, timeout=15,
        )

    def write_checkpoint(self, text):
        (self.loop / "state.env").write_text(text)
        (self.loop / "state.env.sha256").write_text(hashlib.sha256(text.encode()).hexdigest() + "\n")

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
        # A failed squash still ends with a parseable footer.
        self.assertIn("NEXUS_LOOP_STATUS: CONTINUE", result.stdout)
        self.assertIn("status=BLOCKED", result.stdout)
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


    # --- Recovery cannot declare DONE without the DONE gate ---
    def test_recovered_done_checkpoint_reruns_the_done_gate(self):
        (self.loop / "progress.md").write_text("# Progress\n\n## Iteration 1 — DONE\n- Status: DONE\n")
        (self.loop / "state.env").write_text("NEXT_ITERATION=2\nLAST_STATUS=CONTINUE\n")
        (self.loop / "state.env.sha256").write_text("mismatch\n")
        (self.loop / "recover.sh").write_text(template("recover.sh"))
        result = self.run_loop('touch "$LOOP_DIR/executed"\n', MAX_ITERATIONS="2")
        self.assert_success(result)
        self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertTrue((self.loop / "executed").exists(), result.stdout)
        self.assertNotEqual(self.state()["LAST_STATUS"], "DONE")

    def test_done_checkpoint_without_done_evidence_is_not_trusted(self):
        self.write_checkpoint("NEXT_ITERATION=2\nLAST_STATUS=DONE\n")
        result = self.run_loop('touch "$LOOP_DIR/executed"\n', MAX_ITERATIONS="2")
        self.assert_success(result)
        self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertTrue((self.loop / "executed").exists(), result.stdout)

    # --- Pinned artifacts: verify.sh, PROMPT.md, .claude/settings*.json, PIN_PATHS ---
    def test_pinned_verify_script_cannot_be_rewritten_to_pass(self):
        (self.loop / "verify.sh").write_text("#!/bin/bash\nexit 1\n")
        result = self.run_loop(
            'printf "#!/bin/bash\\nexit 0\\n" > "$LOOP_DIR/verify.sh"\n'
            'touch "$LOOP_DIR/done.md"\n', AUTOCOMMIT="false",
        )
        self.assert_success(result)
        self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")
        self.assertIn("verify.sh", result.stdout)

    def test_pinned_settings_file_creation_aborts(self):
        result = self.run_loop(
            'mkdir -p .claude\necho "{}" > .claude/settings.local.json\n'
            'touch "$LOOP_DIR/done.md"\n', AUTOCOMMIT="false",
        )
        self.assert_success(result)
        self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")
        self.assertIn("settings.local.json", result.stdout)

    def test_pin_paths_cover_a_tests_tree(self):
        (self.repo / "tests").mkdir()
        (self.repo / "tests/test_fixture.py").write_text("assert True\n")
        result = self.run_loop(
            'echo "# weakened" >> tests/test_fixture.py\ntouch "$LOOP_DIR/done.md"\n',
            AUTOCOMMIT="false", PIN_PATHS="tests",
        )
        self.assert_success(result)
        self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")

    # --- Symlinked checkout path ---
    def test_deleting_the_pin_manifest_cannot_approve_a_rewritten_verify(self):
        (self.loop / "verify.sh").write_text("#!/bin/bash\nexit 1\n")
        result = self.run_loop(
            'printf "#!/bin/bash\\nexit 0\\n" > "$LOOP_DIR/verify.sh"\n'
            'rm -f "$LOOP_DIR/.pins.sha256"\ntouch "$LOOP_DIR/done.md"\n', AUTOCOMMIT="false",
        )
        self.assert_success(result)
        self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")
        self.assertIn(".pins.sha256", result.stdout)

    def test_rewriting_the_pin_manifest_cannot_approve_a_rewritten_verify(self):
        (self.loop / "verify.sh").write_text("#!/bin/bash\nexit 1\n")
        result = self.run_loop(
            'printf "#!/bin/bash\\nexit 0\\n" > "$LOOP_DIR/verify.sh"\n'
            'h=$(shasum -a 256 < "$LOOP_DIR/verify.sh" | awk \'{print $1}\')\n'
            'sed -i "s|^[^ ]*  $LOOP_DIR/verify.sh\\$|$h  $LOOP_DIR/verify.sh|" "$LOOP_DIR/.pins.sha256"\n'
            'touch "$LOOP_DIR/done.md"\n', AUTOCOMMIT="false",
        )
        self.assert_success(result)
        self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")
        self.assertIn(".pins.sha256", result.stdout)

    def test_self_restoring_verify_replacement_cannot_pass(self):
        # The replacement restores the pinned verify.sh before exiting 0, so a pin
        # check that only runs after verification sees nothing.
        (self.loop / "verify.sh").write_text("#!/bin/bash\nexit 1\n")
        result = self.run_loop(
            'cp "$LOOP_DIR/verify.sh" "$LOOP_DIR/verify.orig"\n'
            "printf '#!/bin/bash\\ncp \"$LOOP_DIR/verify.orig\" \"$LOOP_DIR/verify.sh\"\\nexit 0\\n'"
            ' > "$LOOP_DIR/verify.sh"\ntouch "$LOOP_DIR/done.md"\n', AUTOCOMMIT="false",
        )
        self.assert_success(result)
        self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")
        self.assertIn("verify.sh", result.stdout)

    def test_goal_pin_cannot_be_deleted_or_rewritten_to_hide_goal_drift(self):
        for action in ('rm -f "$LOOP_DIR/.goal.sha256"\n',
                       'shasum -a 256 "$LOOP_DIR/goal.md" | awk \'{print $1}\' > "$LOOP_DIR/.goal.sha256"\n'):
            with self.subTest(action=action):
                for name in ("state.env", "state.env.sha256", ".goal.sha256", ".pins.sha256",
                             ".pin-violation", "done.md"):
                    (self.loop / name).unlink(missing_ok=True)
                (self.loop / "goal.md").write_text("# Goal\n\n## Objective\nFinish the fixture\n")
                result = self.run_loop(
                    'echo "## Objective" > "$LOOP_DIR/goal.md"\n' + action
                    + 'touch "$LOOP_DIR/done.md"\n', AUTOCOMMIT="false")
                self.assert_success(result)
                self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
                self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")
                self.assertIn("goal.md changed", result.stdout)

    # A violation outlives the run that found it: the next start must not re-pin
    # whatever the executor left behind.
    def tamper_then_fail(self):
        (self.loop / "verify.sh").write_text("#!/bin/bash\nexit 1\n")
        return self.run_loop(
            'printf "#!/bin/bash\\nexit 0\\n" > "$LOOP_DIR/verify.sh"\n'
            'rm -f "$LOOP_DIR/.pins.sha256" "$LOOP_DIR/.goal.sha256"\n'
            'echo weakened >> "$LOOP_DIR/goal.md"\nexit 1\n', AUTOCOMMIT="false", RETRY_LIMIT="1")

    def test_tampering_before_a_tool_failure_is_reported(self):
        result = self.tamper_then_fail()
        self.assert_success(result)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")
        self.assertIn("goal.md changed", result.stdout)
        self.assertIn("pin manifest", result.stdout)

    def test_rerun_after_a_pin_violation_does_not_re_pin(self):
        self.tamper_then_fail()
        result = self.run_loop('touch "$LOOP_DIR/executed" "$LOOP_DIR/done.md"\n', AUTOCOMMIT="false")
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertIn("recover.sh --repin-goal", result.stdout)
        self.assertFalse((self.loop / "executed").exists())

    def test_repin_goal_clears_a_pin_violation(self):
        self.tamper_then_fail()
        recover = self.loop / "recover.sh"
        recover.write_text(template("recover.sh"))
        repin = subprocess.run(
            ["bash", str(recover), "--repin-goal", str(self.loop)], cwd=self.repo,
            env=fixture_environment(), text=True, capture_output=True, timeout=10)
        self.assert_success(repin)
        result = self.run_loop('touch "$LOOP_DIR/done.md"\n', AUTOCOMMIT="false")
        self.assert_success(result)
        self.assertIn("NEXUS_LOOP_STATUS: DONE", result.stdout)

    def test_signalling_the_runner_does_not_escape_a_pin_violation(self):
        for sig in ("TERM", "HUP", "USR1"):
            with self.subTest(sig=sig):
                for name in ("state.env", "state.env.sha256", ".goal.sha256", ".pins.sha256",
                             ".pin-violation", "done.md"):
                    (self.loop / name).unlink(missing_ok=True)
                (self.loop / "verify.sh").write_text("#!/bin/bash\nexit 1\n")
                self.run_loop(
                    'printf "#!/bin/bash\\nexit 0\\n" > "$LOOP_DIR/verify.sh"\n'
                    'rm -f "$LOOP_DIR/.pins.sha256" "$LOOP_DIR/.goal.sha256"\n'
                    f'kill -{sig} "$(cat "$LOOP_DIR/.run-loop.lock")"\nsleep 5\n', AUTOCOMMIT="false")
                self.assertTrue((self.loop / ".pin-violation").exists())
                result = self.run_loop('touch "$LOOP_DIR/done.md"\n', AUTOCOMMIT="false")
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)

    def test_a_fifo_at_the_marker_path_refuses_without_blocking(self):
        os.mkfifo(self.loop / ".pin-violation")
        result = self.run_loop('touch "$LOOP_DIR/executed"\n', AUTOCOMMIT="false")
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("unresolved pin violation", result.stdout)
        self.assertFalse((self.loop / "executed").exists())

    def test_a_directory_cannot_stand_in_for_the_pin_violation_marker(self):
        (self.loop / "verify.sh").write_text("#!/bin/bash\nexit 1\n")
        self.run_loop(
            'printf "#!/bin/bash\\nexit 0\\n" > "$LOOP_DIR/verify.sh"\n'
            'rm -f "$LOOP_DIR/.pins.sha256"\nmkdir "$LOOP_DIR/.pin-violation"\nexit 1\n',
            AUTOCOMMIT="false", RETRY_LIMIT="1")
        result = self.run_loop('touch "$LOOP_DIR/done.md"\n', AUTOCOMMIT="false")
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)

    def test_pin_paths_detect_a_retargeted_directory_symlink(self):
        for name, code in (("safe", 1), ("malicious", 0)):
            (self.repo / name).mkdir()
            (self.repo / name / "check.sh").write_text(f"exit {code}\n")
        (self.repo / "tests").mkdir()
        (self.repo / "tests/current").symlink_to("../safe")
        self.git("add", ".")
        self.git("commit", "-qm", "symlinked check")
        (self.loop / "verify.sh").write_text("#!/bin/bash\nbash tests/current/check.sh\n")
        result = self.run_loop('ln -sfn ../malicious tests/current\ntouch "$LOOP_DIR/done.md"\n',
                               AUTOCOMMIT="false", PIN_PATHS="tests")
        self.assert_success(result)
        self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")
        self.assertIn("tests", result.stdout)

    def test_pin_paths_detect_a_retargeted_root_symlink(self):
        # The pinned path is itself a symlink; retargeting it to identical content
        # must still count, since what it points at can steer verify.sh.
        for name in ("safe", "other"):
            (self.repo / name).mkdir()
            (self.repo / name / "check.sh").write_text("exit 0\n")
        (self.repo / "tests").mkdir()
        (self.repo / "tests/current").symlink_to("../safe")
        self.git("add", ".")
        self.git("commit", "-qm", "symlinked tree")
        (self.loop / "verify.sh").write_text(
            '#!/bin/bash\n[[ "$(readlink tests/current)" != ../safe ]]\n')
        result = self.run_loop('ln -sfn ../other tests/current\ntouch "$LOOP_DIR/done.md"\n',
                               AUTOCOMMIT="false", PIN_PATHS="tests/current")
        self.assert_success(result)
        self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")
        self.assertIn("tests/current", result.stdout)

    def test_symlinked_repository_path_keeps_runtime_files_out_of_commits(self):
        (self.repo / ".gitignore").write_text("")
        self.git("commit", "-qam", "track loop directory")
        link = Path(self.temp.name) / "link"
        link.symlink_to(self.repo)
        result = self.run_loop(
            'echo "value = 2" > source.py\ntouch "$LOOP_DIR/done.md"\n',
            cwd=link, LOOP_DIR=str(link / ".loop"),
        )
        self.assert_success(result)
        self.assertEqual(
            self.git("diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"), "source.py")

    # --- Dirty-start snapshot survives resume ---
    def test_blocked_iteration_work_is_committed_after_resume(self):
        result = self.run_loop('echo "value = 2" > source.py\nexit 1\n')
        self.assert_success(result)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")
        result = self.run_loop('touch "$LOOP_DIR/done.md"\n')
        self.assert_success(result)
        self.assertIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertEqual(self.git("show", "HEAD:source.py"), "value = 2")
        self.assertFalse((self.loop / "dirty-start-paths.nul").exists())

    # --- Squash pre-flight and failure footer ---
    def test_second_loop_with_default_name_squashes_to_a_fresh_summary_branch(self):
        self.git("branch", "loop/summary-loop")
        result = self.run_loop(
            'echo "value = 2" > source.py\ntouch "$LOOP_DIR/done.md"\n',
            BRANCH_ISOLATION="true", SQUASH_ON_DONE="true",
        )
        self.assert_success(result)
        self.assertIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertEqual(self.git("branch", "--show-current"), "loop/summary-loop-2")
        self.assertEqual(self.git("show", "HEAD:source.py"), "value = 2")
        self.assertEqual(self.git("rev-list", "--count", "loop/summary-loop"), "1")

    def test_detached_head_aborts_before_branch_isolation(self):
        self.git("checkout", "-q", "--detach")
        result = self.run_loop(
            'touch "$LOOP_DIR/executed"\n', BRANCH_ISOLATION="true", SQUASH_ON_DONE="true")
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("detached HEAD", result.stdout)
        self.assertFalse((self.loop / "executed").exists())
        self.assertEqual(self.git("branch", "--list", "loop/*"), "")

    # --- Signals reach the executor ---
    def interrupt_runner(self, env, *, settle=10, descendant=None):
        """Start the runner, SIGTERM it once the job touched "started", return (code, output).

        descendant: a pid file the job wrote; asserted gone before the fixture's own
        process-group KILL could reap it on the runner's behalf.
        """
        output = Path(self.temp.name) / "runner-output.txt"
        survivor = None
        with output.open("w") as sink:
            proc = subprocess.Popen(
                ["bash", str(self.loop / "run-loop.sh")], cwd=self.repo, env=env,
                stdout=sink, stderr=subprocess.STDOUT, start_new_session=True,
            )
            try:
                deadline = time.monotonic() + 10
                while not (self.loop / "started").exists():
                    self.assertLess(time.monotonic(), deadline, "job never started")
                    time.sleep(0.05)
                proc.send_signal(signal.SIGTERM)
                code = proc.wait(timeout=settle)
                if descendant is not None:
                    pid = int(descendant.read_text())
                    deadline = time.monotonic() + 3
                    while self.process_alive(pid) and time.monotonic() < deadline:
                        time.sleep(0.05)
                    survivor = pid if self.process_alive(pid) else None
            except subprocess.TimeoutExpired:
                self.fail("SIGTERM waited for the job to finish")
            finally:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                proc.wait()
        text = output.read_text()
        self.assertIsNone(survivor, f"descendant {survivor} survived the runner\n{text}")
        return code, text

    @staticmethod
    def process_alive(pid):
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        try:
            return Path(f"/proc/{pid}/stat").read_text().split(")")[-1].split()[0] != "Z"
        except OSError:
            return True

    def test_sigterm_interrupts_a_running_executor_promptly(self):
        env = self.loop_env('touch "$LOOP_DIR/started"\nexec sleep 30\n', AUTOCOMMIT="false")
        code, output = self.interrupt_runner(env, settle=5)
        self.assertEqual(code, 130, output)
        self.assertEqual(self.state()["LAST_STATUS"], "CONTINUE")

    def test_sigterm_reaches_grandchildren_of_an_unlimited_verify(self):
        # verify always runs with no local limit; without LOOP_TIMEOUT nothing bounds it.
        (self.loop / "verify.sh").write_text(
            '#!/bin/bash\nsleep 30 &\necho $! > "$LOOP_DIR/grandchild.pid"\n'
            'touch "$LOOP_DIR/started"\nwait\n')
        env = self.loop_env('true\n', AUTOCOMMIT="false", KILL_GRACE="1")
        code, output = self.interrupt_runner(env, descendant=self.loop / "grandchild.pid")
        self.assertEqual(code, 130, output)

    def test_term_ignoring_executor_and_its_child_are_killed_after_grace(self):
        for exec_timeout in ("0", "600"):
            with self.subTest(exec_timeout=exec_timeout):
                for name in ("started", "child.pid"):
                    (self.loop / name).unlink(missing_ok=True)
                env = self.loop_env(
                    "trap '' TERM\nsleep 30 &\necho $! > \"$LOOP_DIR/child.pid\"\n"
                    'touch "$LOOP_DIR/started"\nwhile :; do wait || true; done\n',
                    AUTOCOMMIT="false", KILL_GRACE="2", EXEC_TIMEOUT=exec_timeout)
                start = time.monotonic()
                code, output = self.interrupt_runner(env, descendant=self.loop / "child.pid")
                self.assertEqual(code, 130, output)
                self.assertLess(time.monotonic() - start, 9, output)

    def test_iteration_timeout_sends_term_before_kill(self):
        start = time.monotonic()
        result = self.run_loop(
            'trap \'touch "$LOOP_DIR/got-term"; exit 1\' TERM\nsleep 10 &\nwait\n',
            AUTOCOMMIT="false", ITER_TIMEOUT="4",
        )
        self.assert_success(result)
        self.assertLess(time.monotonic() - start, 8)
        self.assertTrue((self.loop / "got-term").exists(), result.stdout)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")

    def test_iteration_timeout_kills_term_ignoring_descendants_of_an_exited_job(self):
        # The job's top process exits on TERM; a TERM-ignoring child must not outlive
        # the hard limit just because the command `timeout` watches is gone.
        result = self.run_loop(
            '(trap "" TERM; exec sleep 30 >/dev/null 2>&1) &\necho $! > "$LOOP_DIR/child.pid"\nwait\n',
            AUTOCOMMIT="false", ITER_TIMEOUT="4", KILL_GRACE="1",
        )
        self.assert_success(result)
        pid = int((self.loop / "child.pid").read_text())
        deadline = time.monotonic() + 3
        while self.process_alive(pid) and time.monotonic() < deadline:
            time.sleep(0.05)
        alive = self.process_alive(pid)
        if alive:
            os.kill(pid, signal.SIGKILL)
        self.assertFalse(alive, f"TERM-ignoring child {pid} outlived the job\n{result.stdout}")

    def test_reaping_descendants_does_not_extend_the_hard_limit(self):
        # Top process and child both ignore TERM: `timeout` KILLs the top at the hard
        # limit, and the child must die then too, not a second grace later.
        start = time.monotonic()
        result = self.run_loop(
            "trap '' TERM\n(exec sleep 30 >/dev/null 2>&1) &\n"
            'echo $! > "$LOOP_DIR/child.pid"\nwhile :; do wait || true; done\n',
            AUTOCOMMIT="false", ITER_TIMEOUT="6", KILL_GRACE="3",
        )
        elapsed = time.monotonic() - start
        self.assert_success(result)
        pid = int((self.loop / "child.pid").read_text())
        alive = self.process_alive(pid)
        if alive:
            os.kill(pid, signal.SIGKILL)
        self.assertFalse(alive, result.stdout)
        self.assertLess(elapsed, 8, result.stdout)

    # --- External terminator required for unattended runs ---
    def test_unbounded_unattended_run_is_refused(self):
        result = self.run_loop('touch "$LOOP_DIR/executed"\n', ALLOW_UNBOUNDED_RUN="false")
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("LOOP_TIMEOUT", result.stdout)
        self.assertFalse((self.loop / "executed").exists())
        result = self.run_loop(ALLOW_UNBOUNDED_RUN="false", LOOP_TIMEOUT="60")
        self.assert_success(result)
        self.assertIn("NEXUS_LOOP_STATUS: DONE", result.stdout)

    # --- Executor runs in the project root ---
    def test_runner_changes_into_project_root(self):
        project = self.repo / "nested"
        result = self.run_loop(
            'pwd -P > "$LOOP_DIR/cwd"\ntouch "$LOOP_DIR/done.md"\n',
            AUTOCOMMIT="false", PROJECT_ROOT=str(project),
        )
        self.assert_success(result)
        self.assertEqual((self.loop / "cwd").read_text().strip(), str(project.resolve()))

    # --- State writers are temp-then-rename ---
    def hardlink_snapshots(self, *names):
        snapshots = {}
        for name in names:
            link = Path(self.temp.name) / ("snapshot" + name)
            os.link(self.loop / name, link)
            snapshots[link] = link.read_text()
        return snapshots

    def test_runner_state_writers_replace_files_instead_of_truncating_them(self):
        self.write_checkpoint("NEXT_ITERATION=1\nLAST_STATUS=READY\n")
        (self.loop / ".circuit-state").write_text(
            "CB_STATE=CLOSED\nCB_FAIL_COUNT=0\nCB_LAST_SIGNATURE=\nCB_LAST_UPDATED=0\n")
        snapshots = self.hardlink_snapshots("state.env.sha256", ".circuit-state")
        result = self.run_loop(AUTOCOMMIT="false")
        self.assert_success(result)
        for link, before in snapshots.items():
            self.assertEqual(link.read_text(), before, link.name)
        self.assertNotEqual((self.loop / "state.env.sha256").read_text(),
                            snapshots[Path(self.temp.name) / "snapshotstate.env.sha256"])

    def test_recovery_writers_replace_files_instead_of_truncating_them(self):
        self.write_checkpoint("NEXT_ITERATION=1\nLAST_STATUS=READY\n")
        (self.loop / ".goal.sha256").write_text("previous\n")
        snapshots = self.hardlink_snapshots("state.env.sha256", ".goal.sha256")
        recover = self.loop / "recover.sh"
        recover.write_text(template("recover.sh"))
        result = subprocess.run(
            ["bash", str(recover), "--repin-goal", str(self.loop)], cwd=self.repo,
            env=fixture_environment(), text=True, capture_output=True, timeout=10,
        )
        self.assert_success(result)
        for link, before in snapshots.items():
            self.assertEqual(link.read_text(), before, link.name)
        self.assertNotEqual((self.loop / ".goal.sha256").read_text(), "previous\n")

    # --- A command's own exit code is not the loop deadline ---
    def test_verify_exit_124_is_not_a_loop_timeout(self):
        body = "timeout 1 sleep 5\n" if shutil.which("timeout") else "exit 124\n"
        (self.loop / "verify.sh").write_text("#!/bin/bash\n" + body)
        result = self.run_loop(LOOP_TIMEOUT="3600", AUTOCOMMIT="false")
        self.assert_success(result)
        self.assertNotIn("[TIMEOUT]", result.stdout)
        self.assertIn("verify=FAIL", result.stdout)
        self.assertEqual(self.state()["LAST_STATUS"], "CONTINUE")

    def test_executor_exit_124_or_137_is_a_tool_failure_not_a_loop_timeout(self):
        for code in ("124", "137"):
            with self.subTest(code=code):
                result = self.run_loop(f"exit {code}\n", LOOP_TIMEOUT="3600", EXEC_TIMEOUT="0",
                                       AUTOCOMMIT="false")
                self.assert_success(result)
                self.assertNotIn("[TIMEOUT]", result.stdout)
                self.assertIn("TOOL_FAILURE", result.stdout)

    def test_loop_deadline_still_stops_a_running_executor(self):
        start = time.monotonic()
        result = self.run_loop("sleep 30\n", LOOP_TIMEOUT="3", KILL_GRACE="1", AUTOCOMMIT="false")
        self.assert_success(result)
        self.assertLess(time.monotonic() - start, 8)
        self.assertIn("[TIMEOUT]", result.stdout)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")

    # --- Directory pins cover source, not ignored build output ---
    def test_pin_paths_ignore_gitignored_build_output(self):
        (self.repo / "tests").mkdir()
        (self.repo / "tests/test_fixture.py").write_text("assert True\n")
        (self.repo / ".gitignore").write_text(".loop/\n__pycache__/\n")
        self.git("add", ".")
        self.git("commit", "-qm", "add tests")
        result = self.run_loop(
            'mkdir -p tests/__pycache__\necho compiled > tests/__pycache__/test_fixture.pyc\n'
            'touch "$LOOP_DIR/done.md"\n', AUTOCOMMIT="false", PIN_PATHS="tests")
        self.assert_success(result)
        self.assertIn("NEXUS_LOOP_STATUS: DONE", result.stdout)

    def test_pin_paths_detect_a_new_untracked_test_file(self):
        (self.repo / "tests").mkdir()
        (self.repo / "tests/test_fixture.py").write_text("assert True\n")
        result = self.run_loop(
            'echo "assert True" > tests/test_added.py\ntouch "$LOOP_DIR/done.md"\n',
            AUTOCOMMIT="false", PIN_PATHS="tests")
        self.assert_success(result)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")

    def test_pin_paths_cover_an_ignored_pinned_directory(self):
        # Ignore rules drop build output inside a pinned tree; a pinned root that is
        # itself ignored would otherwise hash as empty and never change.
        (self.repo / "fixtures").mkdir()
        (self.repo / "fixtures/expected.txt").write_text("baseline\n")
        (self.repo / ".gitignore").write_text(".loop/\nfixtures/\n")
        self.git("commit", "-qam", "ignore fixtures")
        result = self.run_loop(
            'echo weakened > fixtures/expected.txt\ntouch "$LOOP_DIR/done.md"\n',
            AUTOCOMMIT="false", PIN_PATHS="fixtures")
        self.assert_success(result)
        self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")
        self.assertIn("fixtures", result.stdout)

    def test_pin_paths_cover_an_ignored_directory_with_a_force_added_file(self):
        # Against the index, one tracked file makes an ignored directory read as
        # not ignored, which would leave its other ignored files unpinned.
        (self.repo / "fixtures").mkdir()
        (self.repo / "fixtures/tracked.txt").write_text("baseline\n")
        (self.repo / "fixtures/golden.txt").write_text("baseline\n")
        (self.repo / ".gitignore").write_text(".loop/\nfixtures/\n")
        self.git("add", "-f", "fixtures/tracked.txt")
        self.git("commit", "-qam", "ignore fixtures, force-add one")
        result = self.run_loop(
            'echo weakened > fixtures/golden.txt\ntouch "$LOOP_DIR/done.md"\n',
            AUTOCOMMIT="false", PIN_PATHS="fixtures")
        self.assert_success(result)
        self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")

    # Ignore rules decide what a directory pin lists, and the executor can write them:
    # a rule it adds must not hide the file it adds next.
    def assert_ignore_rule_cannot_hide_a_pinned_file(self, hide):
        (self.repo / "tests").mkdir()
        (self.repo / "tests/test_fixture.py").write_text("assert True\n")
        self.git("add", "tests")
        self.git("commit", "-qm", "tests")
        result = self.run_loop(
            hide + 'echo "skip = True" > tests/conftest.py\ntouch "$LOOP_DIR/done.md"\n',
            AUTOCOMMIT="false", PIN_PATHS="tests")
        self.assert_success(result)
        self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")
        self.assertIn("tests", result.stdout)

    def test_a_tool_cache_gitignore_in_an_ignored_directory_is_not_a_mutation(self):
        # pytest, ruff and mypy write a .gitignore into their cache directory; git never
        # reads one inside an already-ignored directory, so it decides nothing.
        (self.repo / "tests").mkdir()
        (self.repo / "tests/test_fixture.py").write_text("assert True\n")
        (self.repo / ".gitignore").write_text(".loop/\n.pytest_cache/\n")
        self.git("add", ".")
        self.git("commit", "-qm", "tests")
        (self.loop / "verify.sh").write_text(
            '#!/bin/bash\nroot=$(git rev-parse --show-toplevel)\n'
            'mkdir -p "$root/tests/.pytest_cache" && echo "*" > "$root/tests/.pytest_cache/.gitignore"\n')
        result = self.run_loop(AUTOCOMMIT="false", PIN_PATHS="tests")
        self.assert_success(result)
        self.assertIn("NEXUS_LOOP_STATUS: DONE", result.stdout)

    def test_pin_paths_cover_a_file_hidden_by_info_exclude(self):
        self.assert_ignore_rule_cannot_hide_a_pinned_file(
            'echo tests/conftest.py >> "$(git rev-parse --git-path info/exclude)"\n')

    def test_pin_paths_cover_a_file_hidden_by_the_root_gitignore(self):
        self.assert_ignore_rule_cannot_hide_a_pinned_file('echo tests/conftest.py >> .gitignore\n')

    def test_pin_paths_cover_a_file_hidden_by_a_self_ignoring_gitignore(self):
        self.assert_ignore_rule_cannot_hide_a_pinned_file(
            'printf "conftest.py\\n.gitignore\\n" > tests/.gitignore\n')

    def test_pin_paths_cover_a_file_hidden_by_core_excludes_file(self):
        self.assert_ignore_rule_cannot_hide_a_pinned_file(
            'echo conftest.py > "$LOOP_DIR/excludes"\n'
            'git config core.excludesFile "$LOOP_DIR/excludes"\n')

    # --- A conflicted squash waits for a human instead of taking a new suffix ---
    def conflicting_squash(self):
        self.git("branch", "loop/iter-loop")
        (self.repo / "source.py").write_text("value = 3\n")
        self.git("commit", "-qam", "origin changed")
        self.git("checkout", "-q", "loop/iter-loop")
        (self.loop / "state.env").write_text("NEXT_ITERATION=1\nLAST_STATUS=READY\nORIGIN_BRANCH=main\n")
        result = self.run_loop(
            'echo "value = 2" > source.py\ntouch "$LOOP_DIR/done.md"\n',
            BRANCH_ISOLATION="true", SQUASH_ON_DONE="true")
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("[BRANCH:CONFLICT]", result.stdout)

    def rerun_squash(self):
        return self.run_loop('touch "$LOOP_DIR/unexpected-execution"\n',
                             BRANCH_ISOLATION="true", SQUASH_ON_DONE="true")

    def assert_squash_pending(self, result):
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("NEXUS_LOOP_STATUS: CONTINUE", result.stdout)
        self.assertIn("status=BLOCKED", result.stdout)
        self.assertIn("loop/summary-loop", result.stdout)
        self.assertIn("git branch -D loop/iter-loop", result.stdout)
        self.assertEqual(self.git("branch", "--list", "loop/summary-loop-*"), "")
        self.assertFalse((self.loop / "unexpected-execution").exists())

    def test_executor_leaving_the_iteration_branch_blocks_before_commit(self):
        main_head = self.git("rev-parse", "main")
        result = self.run_loop(
            'git checkout -q main\necho "value = 2" > source.py\ntouch "$LOOP_DIR/done.md"\n',
            BRANCH_ISOLATION="true", SQUASH_ON_DONE="true")
        self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")
        self.assertIn("loop/iter-loop", result.stdout)
        self.assertEqual(self.git("rev-parse", "main"), main_head)
        self.assertFalse((self.loop / ".squash-pending").exists())

    def test_signal_during_the_squash_keeps_done_and_waits_for_a_human(self):
        slow = Path(self.temp.name) / "slow-bin"
        slow.mkdir()
        started = slow / "started"
        (slow / "claude").write_text(f'#!/bin/sh\ntouch "{started}"\nsleep 30\n')
        (slow / "claude").chmod(0o755)
        env = self.loop_env('echo "value = 2" > source.py\ntouch "$LOOP_DIR/done.md"\n',
                            BRANCH_ISOLATION="true", SQUASH_ON_DONE="true",
                            SQUASH_MSG_ENGINE="claude", MAX_ITERATIONS="3")
        env["PATH"] = f"{slow}{os.pathsep}{env['PATH']}"
        runner = subprocess.Popen(["bash", str(self.loop / "run-loop.sh")], cwd=self.repo, env=env,
                                  text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        deadline = time.monotonic() + 10
        while not started.exists() and time.monotonic() < deadline:
            time.sleep(0.1)
        self.assertTrue(started.exists(), "the squash never reached its message engine")
        runner.send_signal(signal.SIGTERM)
        output = runner.communicate(timeout=20)[0]
        self.assertEqual(self.state()["LAST_STATUS"], "DONE", output)
        self.assertTrue((self.loop / ".squash-pending").exists(), output)
        self.assertNotIn("INTERRUPTED", (self.loop / "progress.md").read_text())
        result = self.run_loop('touch "$LOOP_DIR/unexpected-execution"\n',
                               BRANCH_ISOLATION="true", SQUASH_ON_DONE="true", MAX_ITERATIONS="3")
        self.assertIn("[BRANCH:PENDING]", result.stdout)
        self.assertFalse((self.loop / "unexpected-execution").exists())

    def test_signal_after_the_done_checkpoint_keeps_done(self):
        # notify.sh runs after DONE is saved; a signal while it runs must not turn the
        # saved DONE back into CONTINUE and rerun the executor.
        started = self.loop / "notify-started"
        (self.loop / "notify.sh").write_text(f'#!/bin/bash\ntouch "{started}"\nsleep 3\n')
        env = self.loop_env('touch "$LOOP_DIR/done.md"\n', NOTIFY_ENABLED="true", AUTOCOMMIT="false")
        runner = subprocess.Popen(["bash", str(self.loop / "run-loop.sh")], cwd=self.repo, env=env,
                                  text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        deadline = time.monotonic() + 10
        while not started.exists() and time.monotonic() < deadline:
            time.sleep(0.1)
        self.assertTrue(started.exists(), "notify.sh never ran")
        runner.send_signal(signal.SIGTERM)
        output = runner.communicate(timeout=20)[0]
        self.assertEqual(self.state()["LAST_STATUS"], "DONE", output)
        self.assertEqual(self.state()["NEXT_ITERATION"], "2", output)

    def test_rerun_after_resolving_a_squash_conflict_does_not_open_a_new_summary(self):
        self.conflicting_squash()
        # Follow the printed "Resolve" instruction.
        (self.repo / "source.py").write_text("value = 4\n")
        self.git("add", "source.py")
        self.git("commit", "-qm", "resolve squash")
        self.assert_squash_pending(self.rerun_squash())
        self.assertEqual(self.git("branch", "--show-current"), "loop/summary-loop")
        # Deleting the iteration branch marks the squash done.
        self.git("branch", "-D", "loop/iter-loop")
        result = self.rerun_squash()
        self.assert_success(result)
        self.assertIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertEqual(self.git("branch", "--list", "loop/summary-loop-*"), "")
        self.assertEqual(self.git("show", "HEAD:source.py"), "value = 4")

    def test_rerun_after_aborting_a_squash_conflict_does_not_open_a_new_summary(self):
        self.conflicting_squash()
        # Follow the printed "Or abort" instruction.
        self.git("reset", "--merge")
        self.git("checkout", "-q", "loop/iter-loop")
        self.assert_squash_pending(self.rerun_squash())
        self.assertEqual(self.git("branch", "--show-current"), "loop/iter-loop")

    def test_rerun_after_a_rejected_summary_commit_does_not_open_a_new_summary(self):
        hook = self.repo / ".git/hooks/pre-commit"
        hook.write_text('#!/bin/sh\ncase "$(git branch --show-current)" in loop/summary-*) exit 1;; esac\n')
        hook.chmod(0o755)
        first = self.run_loop('echo "value = 2" > source.py\ntouch "$LOOP_DIR/done.md"\n',
                              BRANCH_ISOLATION="true", SQUASH_ON_DONE="true")
        self.assertNotEqual(first.returncode, 0, first.stdout + first.stderr)
        self.assertIn("NEXUS_LOOP_STATUS: CONTINUE", first.stdout)
        self.assert_squash_pending(self.rerun_squash())
        self.assertEqual(self.git("stash", "list"), "")

    # --- A rejected DONE checkpoint at the iteration cap stops cleanly ---
    def test_rejected_done_checkpoint_at_the_cap_blocks_without_an_iteration_branch(self):
        self.write_checkpoint("NEXT_ITERATION=2\nLAST_STATUS=DONE\n")
        for attempt in (1, 2):
            with self.subTest(attempt=attempt):
                result = self.run_loop('touch "$LOOP_DIR/executed"\n',
                                       BRANCH_ISOLATION="true", SQUASH_ON_DONE="true")
                self.assert_success(result)
                self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
                self.assertIn("MAX_ITERATIONS", result.stdout)
                self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")
                self.assertEqual(self.git("branch", "--show-current"), "main")
                self.assertEqual(self.git("branch", "--list", "loop/*"), "")
                self.assertFalse((self.loop / "executed").exists())

    def test_recovery_keeps_done_for_the_runner_gate(self):
        (self.loop / "progress.md").write_text("# Progress\n\n## Iteration 1 — DONE\n- Status: DONE\n")
        recover = self.loop / "recover.sh"
        recover.write_text(template("recover.sh"))
        result = subprocess.run(
            ["bash", str(recover), str(self.loop)], cwd=self.repo,
            env=fixture_environment(), text=True, capture_output=True, timeout=10)
        self.assert_success(result)
        self.assertEqual(self.state()["LAST_STATUS"], "DONE")
        self.assertEqual(self.state()["NEXT_ITERATION"], "2")

    # --- Numeric terminators are validated, not coerced ---
    def test_non_integer_limits_abort(self):
        cases = {"LOOP_TIMEOUT": ("1m", "2.5"), "EXEC_TIMEOUT": ("10s",),
                 "KILL_GRACE": ("-1", "x"), "USD_PER_RUN_CAP": ("1usd",),
                 "USD_PER_ITER_CAP": ("$1",)}
        for key, values in cases.items():
            for value in values:
                with self.subTest(key=key, value=value):
                    result = self.run_loop('touch "$LOOP_DIR/executed"\n', **{key: value})
                    self.assertNotEqual(result.returncode, 0, result.stdout)
                    self.assertIn("[ABORT]", result.stdout)
                    self.assertIn(key, result.stdout)
                    self.assertFalse((self.loop / "executed").exists())

    def test_run_budget_stops_retries(self):
        # A cap is a hard terminator: a failed attempt that spent past it must not
        # buy the next retry.
        result = self.run_loop(
            'echo attempt >> "$LOOP_DIR/attempts"\necho 5 >> "$LOOP_DIR/.cost-usd"\nexit 1\n',
            USD_PER_RUN_CAP="1", RETRY_LIMIT="4", RETRY_BACKOFF_BASE="1")
        self.assert_success(result)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")
        self.assertIn("[BUDGET:RUN]", result.stdout)
        self.assertEqual((self.loop / "attempts").read_text().count("attempt"), 1)

    def test_adaptive_timeout_reads_only_numeric_timings(self):
        # The timings log sits where the executor writes, and its median reaches bash
        # arithmetic: an expression there would run in the runner, outside the timeout.
        marker = self.loop / "evaluated"
        injected = f"PIN_TARGETS[$(touch {shlex.quote(str(marker))})0]\n"
        (self.loop / ".iter-timings.log").write_text(
            "100\n200\n300\n" + injected * 3 + "foo\n08\n")
        result = self.run_loop(ADAPTIVE_TIMEOUT="true", EXEC_TIMEOUT="60")
        self.assert_success(result)
        self.assertFalse(marker.exists(), result.stdout + result.stderr)
        self.assertIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertIn("median=200s", result.stdout)

    def test_bootstrap_next_step_sets_an_external_terminator(self):
        script = template("bootstrap.sh")
        for key, value in {"VERIFY_CMD": "", "RUN_LOOP_CONTENT": "#!/bin/bash\ntrue",
                           "NOTIFY_CONTENT": "#!/bin/bash\ntrue"}.items():
            script = script.replace("{{" + key + "}}", value)
        path = self.loop / "bootstrap.sh"
        path.write_text(script)
        result = subprocess.run(
            ["bash", str(path), str(self.loop)], cwd=self.repo, env=fixture_environment(),
            text=True, capture_output=True, timeout=10)
        self.assert_success(result)
        hint = [line for line in result.stdout.splitlines() if line.startswith("Next:")]
        self.assertEqual(len(hint), 1, result.stdout)
        self.assertIn("LOOP_TIMEOUT=", hint[0])

    # --- Human edits made while the loop is stopped stay out of auto-commits ---
    def test_human_edit_during_blocked_pause_is_not_auto_committed(self):
        result = self.run_loop('echo "value = 2" > source.py\nexit 1\n')
        self.assert_success(result)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")
        (self.repo / "user.txt").write_text("human edit while blocked\n")
        (self.repo / "notes.txt").write_text("human note\n")
        result = self.run_loop('touch "$LOOP_DIR/done.md"\n')
        self.assert_success(result)
        self.assertIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertEqual(self.git("show", "HEAD:source.py"), "value = 2")
        self.assertEqual(self.git("show", "HEAD:user.txt"), "baseline")
        self.assertEqual(self.git("ls-files", "notes.txt"), "")
        self.assertEqual((self.repo / "user.txt").read_text(), "human edit while blocked\n")


    # --- Generated squash messages follow _common/GIT_GUIDELINES.md rule 6 ---
    def test_squash_message_drops_assistant_session_trailers(self):
        stub_dir = Path(self.temp.name) / "bin"
        stub_dir.mkdir()
        stub = stub_dir / "claude"  # stub engine; never the real CLI
        stub.write_text(
            "#!/bin/bash\nprintf '%s\\n' 'feat(loop): finish fixture' '' 'Body line.' '' "
            "'Co-Authored-By: Jane Doe <jane@example.invalid>' "
            "'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>' "
            "'Claude-Session: https://claude.ai/code/session_fixture'\n")
        stub.chmod(0o755)
        result = self.run_loop(
            'echo "value = 2" > source.py\ntouch "$LOOP_DIR/done.md"\n',
            BRANCH_ISOLATION="true", SQUASH_ON_DONE="true", SQUASH_MSG_ENGINE="claude",
            PATH=f"{stub_dir}{os.pathsep}{self.safe_path}",
        )
        self.assert_success(result)
        self.assertEqual(
            self.git("log", "-1", "--format=%B"),
            "feat(loop): finish fixture\n\nBody line.\n\n"
            "Co-Authored-By: Jane Doe <jane@example.invalid>")


    def test_squash_message_drops_codex_session_metadata(self):
        stub_dir = Path(self.temp.name) / "bin"
        stub_dir.mkdir()
        stub = stub_dir / "codex"  # stub engine; never the real CLI
        stub.write_text(
            '#!/bin/bash\nwhile [[ $# -gt 0 && "$1" != "-o" ]]; do shift; done\n'
            "printf '%s\\n' 'feat(loop): finish fixture' '' 'Body line.' '' "
            "'Generated with Codex' 'Session: https://chatgpt.com/codex/tasks/task_e_fixture' "
            "'Co-Authored-By: Jane Doe <jane@example.invalid>' "
            "'Co-authored-by: Codex <codex@openai.com>' > \"$2\"\n")
        stub.chmod(0o755)
        result = self.run_loop(
            'echo "value = 2" > source.py\ntouch "$LOOP_DIR/done.md"\n',
            BRANCH_ISOLATION="true", SQUASH_ON_DONE="true", SQUASH_MSG_ENGINE="codex",
            PATH=f"{stub_dir}{os.pathsep}{self.safe_path}",
        )
        self.assert_success(result)
        self.assertEqual(
            self.git("log", "-1", "--format=%B"),
            "feat(loop): finish fixture\n\nBody line.\n\n"
            "Co-Authored-By: Jane Doe <jane@example.invalid>")

if __name__ == "__main__":
    unittest.main()
