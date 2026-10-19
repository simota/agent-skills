#!/usr/bin/env python3
"""Run the complete loop runner against Git repositories and saved checkpoints."""

import hashlib
import os
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
            "ALLOW_UNBOUNDED_RUN": "true",
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
    def test_sigterm_interrupts_a_running_executor_promptly(self):
        env = self.loop_env('touch "$LOOP_DIR/started"\nexec sleep 30\n', AUTOCOMMIT="false")
        output = Path(self.temp.name) / "runner-output.txt"
        with output.open("w") as sink:
            proc = subprocess.Popen(
                ["bash", str(self.loop / "run-loop.sh")], cwd=self.repo, env=env,
                stdout=sink, stderr=subprocess.STDOUT, start_new_session=True,
            )
            try:
                deadline = time.monotonic() + 10
                while not (self.loop / "started").exists():
                    self.assertLess(time.monotonic(), deadline, "executor never started")
                    time.sleep(0.05)
                proc.send_signal(signal.SIGTERM)
                code = proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.fail("SIGTERM waited for the executor to finish")
            finally:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                proc.wait()
        self.assertEqual(code, 130, output.read_text())
        self.assertEqual(self.state()["LAST_STATUS"], "CONTINUE")

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
            PATH=f"{stub_dir}{os.pathsep}{os.environ['PATH']}",
        )
        self.assert_success(result)
        self.assertEqual(
            self.git("log", "-1", "--format=%B"),
            "feat(loop): finish fixture\n\nBody line.\n\n"
            "Co-Authored-By: Jane Doe <jane@example.invalid>")


if __name__ == "__main__":
    unittest.main()
