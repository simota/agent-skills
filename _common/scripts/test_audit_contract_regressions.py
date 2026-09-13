#!/usr/bin/env python3
"""Behavioral regressions for executable prompt contracts."""

from __future__ import annotations

from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile
import unittest

from test_skill_templates import fixture_environment, template


class ExecutorContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = tempfile.TemporaryDirectory(prefix="contract-regressions-")
        self.addCleanup(self.workspace.cleanup)
        self.cwd = Path(self.workspace.name)
        self.git("init", "-q")
        self.loop = self.cwd / ".loop"
        self.loop.mkdir()
        (self.loop / "goal.md").write_text("# Goal\n", encoding="utf-8")
        self.runner = self.loop / "run-loop.sh"
        self.runner.write_text(template("run-loop.sh"), encoding="utf-8")

    def run_loop(self, command: str, **overrides: str) -> subprocess.CompletedProcess[str]:
        environment = {
            **fixture_environment(), "AUTOCOMMIT": "false", "BRANCH_ISOLATION": "false",
            "MAX_ITERATIONS": "1", "RETRY_LIMIT": "1", "SQUASH_ON_DONE": "false",
            "EXEC_CMD": command, **overrides,
        }
        return subprocess.run(["bash", str(self.runner)], cwd=self.cwd, env=environment,
                              text=True, capture_output=True, timeout=15)

    def git(self, *args: str) -> None:
        subprocess.run(["git", *args], cwd=self.cwd, env=fixture_environment(),
                       check=True, capture_output=True)

    def test_executor_preserves_quoted_prompt_and_executable_path(self) -> None:
        executable = self.cwd / "custom executor.sh"
        executable.write_text('#!/bin/bash\nprintf "%s\\n" "$#" "$1" > arguments.txt\n')
        executable.chmod(0o755)
        prompt = 'Read goal.md and keep * literal'
        result = self.run_loop(f"{shlex.quote(str(executable))} {shlex.quote(prompt)}")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.cwd / "arguments.txt").exists(), result.stdout)
        self.assertEqual((self.cwd / "arguments.txt").read_text().splitlines(), ["1", prompt])

    def test_untracked_source_progress_does_not_trigger_stall(self) -> None:
        self.git("init", "-q")
        (self.cwd / "tracked.txt").write_text("baseline\n")
        self.git("add", "tracked.txt")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "baseline")
        executable = self.cwd / "executor.sh"
        executable.write_text('#!/bin/bash\necho iteration >> output.py\n')
        executable.chmod(0o755)
        result = self.run_loop(str(executable), MAX_ITERATIONS="6", CONVERGENCE_WINDOW="3")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("CONVERGENCE:STALL", result.stdout)
        self.assertEqual(len((self.cwd / "output.py").read_text().splitlines()), 6)

    def test_runtime_logs_do_not_hide_a_real_stall(self) -> None:
        self.git("init", "-q")
        (self.cwd / "tracked.txt").write_text("baseline\n")
        self.git("add", "tracked.txt")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "baseline")
        result = self.run_loop("true", MAX_ITERATIONS="6", CONVERGENCE_WINDOW="3")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("CONVERGENCE:STALL", result.stdout)

    def test_iteration_timeout_alias_bounds_executor(self) -> None:
        result = self.run_loop("sleep 3", ITER_TIMEOUT="1", EXEC_TIMEOUT="10")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("TOOL_FAILURE", result.stdout)
        self.assertIn("LAST_STATUS=BLOCKED", (self.loop / "state.env").read_text())


    def test_notification_falls_back_when_audio_has_no_player(self) -> None:
        binary_dir = self.cwd / "bin"
        binary_dir.mkdir()
        for name in ("mkdir", "date"):
            (binary_dir / name).symlink_to(shutil.which(name))
        edge = binary_dir / "edge-tts"
        edge.write_text("#!/bin/bash\nexit 0\n")
        edge.chmod(0o755)
        notifier = self.loop / "notify.sh"
        notifier.write_text(template("notify.sh"), encoding="utf-8")
        result = subprocess.run(["bash", str(notifier), "1", "CONTINUE", "PASS", "1", str(self.loop)],
                                cwd=self.cwd, env={**fixture_environment(), "PATH": str(binary_dir)},
                                executable=shutil.which("bash"), text=True, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[NOTIFY]", result.stdout)

    def test_notification_does_not_launch_an_interactive_text_engine(self) -> None:
        binary_dir = self.cwd / "bin"
        binary_dir.mkdir()
        engine = binary_dir / "agy"
        engine.write_text("#!/bin/bash\ntouch agy-invoked\nsleep 2\n")
        engine.chmod(0o755)
        notifier = self.loop / "notify.sh"
        notifier.write_text(template("notify.sh"), encoding="utf-8")
        result = subprocess.run(
            ["bash", str(notifier), "1", "CONTINUE", "PASS", "1", str(self.loop), "HEAD"],
            cwd=self.cwd, env={**fixture_environment(), "PATH": f"{binary_dir}:{shutil.which('bash').rsplit('/', 1)[0]}",
                              "NOTIFY_ENGINE": "text"}, text=True, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.cwd / "agy-invoked").exists())
        self.assertIn("[NOTIFY]", result.stdout)

    def test_squash_finishes_when_optional_text_engine_hangs(self) -> None:
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        (self.cwd / "tracked.txt").write_text("baseline\n")
        self.git("add", "tracked.txt")
        self.git("commit", "-qm", "baseline")
        binary_dir = self.cwd / "bin"
        binary_dir.mkdir()
        engine = binary_dir / "claude"
        engine.write_text("#!/bin/bash\nsleep 3\necho should-not-be-used\n")
        engine.chmod(0o755)
        executor = self.cwd / "executor.sh"
        executor.write_text("#!/bin/bash\necho completed > output.txt\ntouch .loop/done.md\n")
        executor.chmod(0o755)
        environment = fixture_environment()
        result = self.run_loop(str(executor), AUTOCOMMIT="true", BRANCH_ISOLATION="true",
                               SQUASH_ON_DONE="true", SQUASH_MSG_ENGINE="claude", TOOL_TIMEOUT="1",
                               PATH=f"{binary_dir}:{environment['PATH']}")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("NEXUS_LOOP_STATUS: DONE", result.stdout)
        self.assertIn("using heuristic commit message", result.stdout)
        self.git("show-ref", "--verify", "refs/heads/loop/summary-loop")


    def test_squash_reads_codex_artifact_instead_of_stdout(self) -> None:
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        (self.cwd / "tracked.txt").write_text("baseline\n")
        self.git("add", "tracked.txt")
        self.git("commit", "-qm", "baseline")
        binary_dir = self.cwd / "bin"
        binary_dir.mkdir()
        engine = binary_dir / "codex"
        engine.write_text(
            '#!/bin/bash\nwhile [[ $# -gt 0 ]]; do\n'
            '  if [[ "$1" == "-o" ]]; then shift; output="$1"; fi\n  shift\ndone\n'
            'echo "fix(test): artifact commit" > "$output"\necho progress-noise\n')
        engine.chmod(0o755)
        executor = self.cwd / "executor.sh"
        executor.write_text("#!/bin/bash\necho completed > output.txt\ntouch .loop/done.md\n")
        executor.chmod(0o755)
        environment = fixture_environment()
        result = self.run_loop(str(executor), AUTOCOMMIT="true", BRANCH_ISOLATION="true",
                               SQUASH_ON_DONE="true", SQUASH_MSG_ENGINE="codex", TOOL_TIMEOUT="2",
                               PATH=f"{binary_dir}:{environment['PATH']}")
        self.assertEqual(result.returncode, 0, result.stderr)
        commit = subprocess.run(["git", "log", "-1", "--format=%s"], cwd=self.cwd,
                                env=environment, text=True, capture_output=True, check=True)
        self.assertEqual(commit.stdout.strip(), "fix(test): artifact commit")

    def test_squash_discards_artifact_from_failed_codex(self) -> None:
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        (self.cwd / "tracked.txt").write_text("baseline\n")
        self.git("add", "tracked.txt")
        self.git("commit", "-qm", "baseline")
        binary_dir = self.cwd / "bin"
        binary_dir.mkdir()
        engine = binary_dir / "codex"
        engine.write_text(
            '#!/bin/bash\nwhile [[ $# -gt 0 ]]; do\n'
            '  if [[ "$1" == "-o" ]]; then shift; output="$1"; fi\n  shift\ndone\n'
            'echo "fix(test): artifact commit" > "$output"\nexit 1\n')
        engine.chmod(0o755)
        executor = self.cwd / "executor.sh"
        executor.write_text("#!/bin/bash\necho completed > output.txt\ntouch .loop/done.md\n")
        executor.chmod(0o755)
        environment = fixture_environment()
        result = self.run_loop(str(executor), AUTOCOMMIT="true", BRANCH_ISOLATION="true",
                               SQUASH_ON_DONE="true", SQUASH_MSG_ENGINE="codex", TOOL_TIMEOUT="2",
                               PATH=f"{binary_dir}:{environment['PATH']}")
        self.assertEqual(result.returncode, 0, result.stderr)
        commit = subprocess.run(["git", "log", "-1", "--format=%s"], cwd=self.cwd,
                                env=environment, text=True, capture_output=True, check=True)
        self.assertNotEqual(commit.stdout.strip(), "fix(test): artifact commit")
        self.assertIn("using heuristic commit message", result.stdout)


if __name__ == "__main__":
    unittest.main()
