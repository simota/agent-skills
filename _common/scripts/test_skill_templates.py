#!/usr/bin/env python3
"""Execute generated loop templates against isolated local fixtures."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / ".agents/skills/orbit/reference"


def fixture_environment() -> dict[str, str]:
    """Git hooks export repository overrides; never pass those into fixtures."""
    environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    return {**environment, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}


def template(name: str) -> str:
    filename = "script-template-runner.md" if name == "run-loop.sh" else "script-template-support.md"
    text = (REFERENCE / filename).read_text(encoding="utf-8")
    if name != "run-loop.sh":
        text = text.split(f" Template (`{name}`)", 1)[1]
    match = re.search(r"^(`{3,})bash\n(.*?)^\1$", text, re.M | re.S)
    if not match:
        raise AssertionError(f"missing template: {name}")
    return match.group(2)


class LoopTemplateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = tempfile.TemporaryDirectory(prefix="loop-template-tests-")
        self.addCleanup(self.workspace.cleanup)
        self.cwd = Path(self.workspace.name)
        self.loop = self.cwd / "custom loop"
        self.loop.mkdir()
        (self.loop / "goal.md").write_text("# Goal\n", encoding="utf-8")
        (self.loop / "progress.md").write_text("# Progress\n", encoding="utf-8")

    def run_script(self, name: str, *args: str, env: dict[str, str] | None = None,
                   replacements: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        script = template(name)
        for key, value in (replacements or {}).items():
            script = script.replace("{{" + key + "}}", value)
        path = self.loop / name
        path.write_text(script, encoding="utf-8")
        defaults = {
            "AUTOCOMMIT": "false", "BRANCH_ISOLATION": "false",
            "MAX_ITERATIONS": "1", "RETRY_LIMIT": "1", "EXEC_CMD": "true",
            "CONVERGENCE_WINDOW": "3", "SQUASH_ON_DONE": "false",
        }
        return subprocess.run(["bash", str(path), *args], cwd=self.cwd,
                              env={**fixture_environment(), **defaults, **(env or {})},
                              text=True, capture_output=True, timeout=15)

    def state(self) -> dict[str, str]:
        return dict(line.split("=", 1) for line in (self.loop / "state.env").read_text().splitlines())

    def test_recovery_without_iteration_history(self) -> None:
        result = self.run_script("recover.sh", str(self.loop))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.state()["NEXT_ITERATION"], "1")
        self.assertEqual(self.state()["LAST_STATUS"], "CONTINUE")

    def test_recovery_does_not_infer_done_from_free_text(self) -> None:
        (self.loop / "progress.md").write_text(
            "## Iteration 1 — DONE\n- Status: DONE\n"
            "## Iteration 2 — CONTINUE\n- Remaining: task not completed\n- Status: CONTINUE\n")
        result = self.run_script("recover.sh", str(self.loop))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.state()["LAST_STATUS"], "CONTINUE")
        self.assertEqual(self.state()["NEXT_ITERATION"], "3")

    def test_recovery_retries_blocked_iteration(self) -> None:
        (self.loop / "progress.md").write_text("## Iteration 4 — BLOCKED\n- TOOL_FAILURE: false\n")
        result = self.run_script("recover.sh", str(self.loop))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.state()["NEXT_ITERATION"], "4")
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")

    def test_recovery_ignores_status_outside_iteration_section(self) -> None:
        (self.loop / "progress.md").write_text(
            "## Iteration 2 — CONTINUE\n- Status: CONTINUE\n"
            "## Earlier migration\n- Status: DONE\n")
        result = self.run_script("recover.sh", str(self.loop))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.state()["LAST_STATUS"], "CONTINUE")

    def test_recovery_parses_state_as_data(self) -> None:
        (self.loop / "progress.md").write_text("## Iteration 1 — CONTINUE\n- Status: CONTINUE\n")
        (self.loop / "state.env").write_text("ORIGIN_BRANCH=feature/fix+test\nLAST_STATUS=READY touch injected\nPATH=/nowhere\n")
        result = self.run_script("recover.sh", str(self.loop))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.cwd / "injected").exists())
        self.assertEqual(self.state()["ORIGIN_BRANCH"], "feature/fix+test")

    def test_bootstrap_preserves_existing_resume_state(self) -> None:
        state = "NEXT_ITERATION=7\nLAST_STATUS=CONTINUE\nORIGIN_BRANCH=feature/start\n"
        (self.loop / "state.env").write_text(state)
        result = self.run_script("bootstrap.sh", str(self.loop), replacements={
            "VERIFY_CMD": "", "RUN_LOOP_CONTENT": "#!/bin/bash\ntrue",
            "NOTIFY_CONTENT": "#!/bin/bash\ntrue",
        })
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.loop / "state.env").read_text(), state)

    def test_runner_defaults_to_its_own_directory(self) -> None:
        result = self.run_script("run-loop.sh")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.state()["NEXT_ITERATION"], "2")

    def test_runner_parses_state_as_data(self) -> None:
        (self.loop / "state.env").write_text("NEXT_ITERATION=1\nLAST_STATUS=READY touch injected\n")
        result = self.run_script("run-loop.sh", env={"LOOP_DIR": str(self.loop)})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.cwd / "injected").exists())

    def test_runner_preserves_resume_metadata(self) -> None:
        (self.loop / "state.env").write_text(
            "NEXT_ITERATION=1\nLAST_STATUS=READY\nCONTRACT_VERSION=1.2.0\n"
            "TOTAL_TOKENS=17\nTOTAL_API_CALLS=2\nESTIMATED_COST_USD=0.125\n")
        result = self.run_script("run-loop.sh", env={"LOOP_DIR": str(self.loop)})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.state()["CONTRACT_VERSION"], "1.2.0")
        self.assertEqual(self.state()["TOTAL_TOKENS"], "17")
        self.assertEqual(self.state()["TOTAL_API_CALLS"], "2")
        self.assertEqual(self.state()["ESTIMATED_COST_USD"], "0.125")

    def test_runner_does_not_execute_circuit_state(self) -> None:
        (self.loop / ".circuit-state").write_text("CB_STATE=CLOSED\ntouch injected\n")
        result = self.run_script("run-loop.sh", env={"LOOP_DIR": str(self.loop)})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.cwd / "injected").exists())

    def executor(self, body: str) -> dict[str, str]:
        path = self.cwd / "executor.sh"
        path.write_text("#!/bin/bash\nset -euo pipefail\n" + body)
        path.chmod(0o755)
        return {"LOOP_DIR": str(self.loop), "EXEC_CMD": str(path)}

    def test_goal_drift_cannot_finish_the_last_iteration(self) -> None:
        result = self.run_script("run-loop.sh", env=self.executor(
            'echo changed > "$LOOP_DIR/goal.md"\ntouch "$LOOP_DIR/done.md"\n'))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")
        self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)

    def test_final_iteration_budget_overrun_cannot_finish(self) -> None:
        result = self.run_script("run-loop.sh", env={**self.executor(
            'echo 2 > "$LOOP_DIR/.cost-usd"\ntouch "$LOOP_DIR/done.md"\n'),
            "USD_PER_RUN_CAP": "1"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")

    def assert_wall_clock_blocked(self, environment: dict[str, str]) -> None:
        # date +%s rounds down: two seconds leave at least one second to enter
        # the operation under test, while uncapped four-second work still fails.
        start = time.monotonic()
        result = self.run_script("run-loop.sh", env={**environment,
                                "LOOP_TIMEOUT": "2", "EXEC_TIMEOUT": "30"})
        elapsed = time.monotonic() - start
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.state()["LAST_STATUS"], "BLOCKED")
        self.assertFalse((self.loop / ".run-loop.lock").exists())
        self.assertLess(elapsed, 3.5, f"2-second budget took {elapsed:.2f}s")

    def test_wall_clock_caps_executor_even_when_term_is_ignored(self) -> None:
        self.assert_wall_clock_blocked(self.executor(
            'trap "" TERM\nsleep 4\ntouch "$LOOP_DIR/done.md"\n'))
        self.assertFalse((self.loop / "done.md").exists())

    def test_wall_clock_caps_retry_backoff(self) -> None:
        self.assert_wall_clock_blocked({**self.executor(
            'echo attempt >> "$LOOP_DIR/attempts"\nexit 1\n'),
            "RETRY_LIMIT": "2", "RETRY_BACKOFF_BASE": "4"})
        self.assertEqual((self.loop / "attempts").read_text().splitlines(), ["attempt"])

    def test_wall_clock_caps_verification(self) -> None:
        (self.loop / "verify.sh").write_text(
            '#!/bin/bash\nsleep 4\ntouch "$LOOP_DIR/verify-finished"\n')
        self.assert_wall_clock_blocked(self.executor('touch "$LOOP_DIR/done.md"\n'))
        self.assertFalse((self.loop / "verify-finished").exists())

    def test_corrupt_checkpoint_without_recovery_fails_closed(self) -> None:
        (self.loop / "state.env").write_text("NEXT_ITERATION=1\nLAST_STATUS=DONE\n")
        (self.loop / "state.env.sha256").write_text("incorrect\n")
        result = self.run_script("run-loop.sh", env={"LOOP_DIR": str(self.loop)})
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.loop / ".run-loop.lock").exists())
        self.assertNotIn("NEXUS_LOOP_STATUS: DONE", result.stdout)

    def git(self, *args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=self.cwd,
                                       env=fixture_environment(), text=True).strip()

    def init_repo(self) -> None:
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        (self.cwd / ".gitignore").write_text("custom loop/\nexecutor.sh\n")
        (self.cwd / "existing.txt").write_text("baseline\n")
        self.git("add", ".gitignore", "existing.txt")
        self.git("commit", "-qm", "initial")

    def test_autocommit_preserves_preexisting_staged_changes(self) -> None:
        self.init_repo()
        (self.cwd / "existing.txt").write_text("user staged\n")
        self.git("add", "existing.txt")
        result = self.run_script("run-loop.sh", env={**self.executor(
            'echo new > "new file.txt"\ntouch "$LOOP_DIR/done.md"\n'),
            "AUTOCOMMIT": "true"})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.git("show", "HEAD:existing.txt"), "baseline")
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "existing.txt")
        self.assertEqual(self.git("show", "HEAD:new file.txt"), "new")

    def test_autocommit_excludes_runtime_files_without_gitignore(self) -> None:
        self.init_repo()
        (self.cwd / ".gitignore").write_text("executor.sh\n")
        self.git("add", ".gitignore")
        self.git("commit", "-qm", "include loop directory in worktree")
        result = self.run_script("run-loop.sh", env={**self.executor(
            'echo new > "new file.txt"\ntouch "$LOOP_DIR/done.md"\n'),
            "AUTOCOMMIT": "true"})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.git("diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"), "new file.txt")

    def test_placeholder_gate_handles_spaces_and_committed_changes(self) -> None:
        self.init_repo()
        result = self.run_script("run-loop.sh", env={**self.executor(
            'printf "def pending():\\n    pass\\n" > "pending work.py"\ntouch "$LOOP_DIR/done.md"\n'),
            "AUTOCOMMIT": "true"})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.state()["LAST_STATUS"], "CONTINUE")

    def test_structured_log_escapes_dynamic_values(self) -> None:
        prefix = template("run-loop.sh").split("#--- Circuit breaker ---", 1)[0]
        result = subprocess.run(["bash", "-c", prefix + '\nemit_log INFO sample detail "$DETAIL"\n'],
                                cwd=self.cwd, env={**fixture_environment(), "LOOP_DIR": str(self.loop),
                                "AUTOCOMMIT": "false", "DETAIL": 'a "quote" and\\slash\nnext\tline'},
                                text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = [json.loads(line) for line in (self.loop / "runner.jsonl").read_text().splitlines()]
        self.assertEqual(rows[-1]["detail"], 'a "quote" and\\slash\nnext\tline')

    def test_verify_requires_at_least_one_check(self) -> None:
        result = self.run_script("verify.sh", replacements={"VERIFY_CHECKS": ""})
        self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_verify_accepts_a_successful_check(self) -> None:
        result = self.run_script("verify.sh", replacements={"VERIFY_CHECKS": 'run_check "works" true'})
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_mirrored_templates_match(self) -> None:
        for source in REFERENCE.glob("*.md"):
            mirror = ROOT / ".claude/skills/orbit/reference" / source.name
            self.assertEqual(source.read_bytes(), mirror.read_bytes(), source.name)


if __name__ == "__main__":
    unittest.main()
