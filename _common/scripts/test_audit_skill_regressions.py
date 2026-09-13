"""Execute the cross-language port examples against controlled fixtures."""

from __future__ import annotations

import json
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / "builder/reference/cross-language-port.md"


def example(language: str) -> str:
    return re.search(
        rf"^```{language}\n(.*?)^```$", REFERENCE.read_text(), re.M | re.S
    ).group(1)


def hook_example(path: Path, heading: str) -> str:
    section = path.read_text().split(heading, 1)[1]
    return re.search(r"^```bash\n(.*?)^```$", section, re.M | re.S).group(1)


class TestPortGoldenExamples(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="port-example-")
        self.addCleanup(self.temp.cleanup)
        self.cwd = Path(self.temp.name)

    def test_capture_preserves_nullable_object_cases(self) -> None:
        (self.cwd / "source.py").write_text(
            "def parse_phone(raw):\n"
            "    return None if raw is None else raw.strip()\n"
        )
        (self.cwd / "test_golden.py").write_text(
            example("python") + "\ntest_capture_goldens()\n"
        )
        result = subprocess.run(
            [sys.executable, "test_golden.py"], cwd=self.cwd,
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        cases = json.loads((self.cwd / "goldens.json").read_text())
        self.assertEqual(len(cases), 6)
        self.assertTrue(all(set(case) == {"input", "expected"} for case in cases))
        self.assertIn({"input": None, "expected": None}, cases)
        self.assertIn({"input": "", "expected": ""}, cases)

    def run_harness(self, source: str, target: str) -> subprocess.CompletedProcess:
        (self.cwd / "gen_inputs.py").write_text("print('{}')\n")
        (self.cwd / "source.py").write_text(source)
        executable = self.cwd / "target"
        executable.write_text(f"#!{sys.executable}\n" + target)
        executable.chmod(0o755)
        (self.cwd / "compare.sh").write_text(example("bash"))
        return subprocess.run(
            ["bash", "compare.sh"], cwd=self.cwd,
            env={**os.environ, "PATH": str(Path(sys.executable).parent)
                 + os.pathsep + os.environ.get("PATH", "")},
            text=True, capture_output=True,
        )

    @unittest.skipUnless(shutil.which("jq"), "jq is required by the port harness")
    def test_equivalent_objects_ignore_key_order(self) -> None:
        result = self.run_harness(
            "print('{\"a\": 1, \"b\": null}')\n",
            "print('{\"b\": null, \"a\": 1}')\n",
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    @unittest.skipUnless(shutil.which("jq"), "jq is required by the port harness")
    def test_different_output_fails_comparison(self) -> None:
        result = self.run_harness("print('1')\n", "print('2')\n")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("-1", result.stdout)
        self.assertIn("+2", result.stdout)

    @unittest.skipUnless(shutil.which("jq"), "jq is required by the port harness")
    def test_malformed_json_fails_even_when_both_outputs_match(self) -> None:
        result = self.run_harness("print('invalid')\n", "print('invalid')\n")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("parse error", result.stderr)

    @unittest.skipUnless(shutil.which("jq"), "jq is required by the port harness")
    def test_failed_source_stops_before_running_target(self) -> None:
        result = self.run_harness(
            "raise SystemExit(7)\n",
            "from pathlib import Path\nPath('target-ran').touch()\n",
        )
        self.assertEqual(result.returncode, 7)
        self.assertFalse((self.cwd / "target-ran").exists())

    @unittest.skipUnless(shutil.which("jq"), "jq is required by the port harness")
    def test_failed_target_cannot_pass_with_matching_stdout(self) -> None:
        result = self.run_harness(
            "print('1')\n", "print('1')\nraise SystemExit(9)\n"
        )
        self.assertEqual(result.returncode, 9)


@unittest.skipUnless(shutil.which("jq"), "jq is required by the hook examples")
class TestSessionStartExamples(unittest.TestCase):
    REFERENCES = (
        ROOT / "hone/reference/hooks/sessionstart-hook.md",
        ROOT / ".archive/latch/reference/sessionstart-hook.md",
    )

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="sessionstart-example-")
        self.addCleanup(self.temp.cleanup)
        self.cwd = Path(self.temp.name)
        self.environment = {**os.environ, "XDG_CACHE_HOME": str(self.cwd / "cache")}

    def test_dispatches_actual_stdin_source(self) -> None:
        for name, output in (("full-context", "full"), ("minimal-context", "minimal")):
            script = self.cwd / f"{name}.sh"
            script.write_text(f"#!/bin/sh\nprintf '%s\\n' {output}\n")
            script.chmod(0o755)
        for reference in self.REFERENCES:
            script = hook_example(reference, "## 3. Trigger Filtering")
            for source, expected in (("startup", "full"), ("resume", "full"),
                                     ("fork", "full"), ("clear", "minimal"),
                                     ("compact", "")):
                with self.subTest(reference=reference, source=source):
                    result = subprocess.run(
                        ["bash", "-c", script], cwd=self.cwd,
                        input=json.dumps({"hook_event_name": "SessionStart", "source": source}),
                        text=True, capture_output=True,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout.strip(), expected)

    def test_summary_cache_works_on_first_run(self) -> None:
        (self.cwd / "CLAUDE.md").write_text("Project instructions\n")
        for reference in self.REFERENCES:
            shutil.rmtree(self.cwd / "cache", ignore_errors=True)
            result = subprocess.run(
                ["bash", "-c", hook_example(reference, "### CLAUDE.md auto-summary")],
                cwd=self.cwd, env=self.environment, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Project instructions", result.stdout)
            caches = list((self.cwd / "cache/claude").glob("*-claude-md-summary.txt"))
            self.assertEqual(len(caches), 1)
            self.assertEqual(caches[0].read_text(), "Project instructions\n")

    def test_missing_project_instructions_are_a_noop(self) -> None:
        for reference in self.REFERENCES:
            result = subprocess.run(
                ["bash", "-c", hook_example(reference, "### CLAUDE.md auto-summary")],
                cwd=self.cwd, env=self.environment, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertFalse((self.cwd / "cache").exists())

    def test_fresh_pr_cache_does_not_refresh(self) -> None:
        key = hashlib.sha256((str(self.cwd) + "\n").encode()).hexdigest()
        cache = self.cwd / "cache/claude" / f"{key}-pr-list.txt"
        cache.parent.mkdir(parents=True)
        cache.write_text("cached PR\n")
        binary = self.cwd / "bin"
        binary.mkdir()
        gh = binary / "gh"
        gh.write_text("#!/bin/sh\ntouch refreshed\nprintf 'new PR\\n'\n")
        gh.chmod(0o755)
        environment = {**self.environment, "PATH": str(binary) + os.pathsep
                       + os.environ.get("PATH", "")}
        for reference in self.REFERENCES:
            result = subprocess.run(
                ["bash", "-c", hook_example(reference, "### Cache pattern for slow operations")],
                cwd=self.cwd, env=environment, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, "")
            self.assertEqual(result.stdout, "cached PR\n")
            self.assertFalse((self.cwd / "refreshed").exists())

    def test_same_basename_projects_have_separate_pr_caches(self) -> None:
        binary = self.cwd / "bin"
        binary.mkdir()
        gh = binary / "gh"
        gh.write_text("#!/bin/sh\npwd\n")
        gh.chmod(0o755)
        environment = {**self.environment, "PATH": str(binary) + os.pathsep
                       + os.environ.get("PATH", "")}
        projects = [self.cwd / "first/repo", self.cwd / "second/repo"]
        for project in projects:
            project.mkdir(parents=True)
        for reference in self.REFERENCES:
            shutil.rmtree(self.cwd / "cache", ignore_errors=True)
            for project in projects:
                script = hook_example(reference, "### Cache pattern for slow operations")
                result = subprocess.run(
                    ["bash", "-c", script + "\nwait\n"], cwd=project,
                    env=environment, text=True, capture_output=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
            caches = list((self.cwd / "cache/claude").glob("*-pr-list.txt"))
            self.assertEqual({cache.read_text().strip() for cache in caches},
                             {str(project) for project in projects})
            self.assertFalse(list((self.cwd / "cache/claude").glob("*.tmp.*")))

    def test_failed_pr_refresh_keeps_stale_cache_and_removes_tempfile(self) -> None:
        binary = self.cwd / "bin"
        binary.mkdir()
        gh = binary / "gh"
        gh.write_text("#!/bin/sh\nprintf 'partial result\\n'\nexit 5\n")
        gh.chmod(0o755)
        environment = {**self.environment, "PATH": str(binary) + os.pathsep
                       + os.environ.get("PATH", "")}
        key = hashlib.sha256((str(self.cwd) + "\n").encode()).hexdigest()
        cache = self.cwd / "cache/claude" / f"{key}-pr-list.txt"
        cache.parent.mkdir(parents=True)
        cache.write_text("stale PR\n")
        os.utime(cache, (1, 1))
        for reference in self.REFERENCES:
            script = hook_example(reference, "### Cache pattern for slow operations")
            result = subprocess.run(
                ["bash", "-c", script + "\nwait\n"], cwd=self.cwd,
                env=environment, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(cache.read_text(), "stale PR\n")
            self.assertFalse(list(cache.parent.glob("*.tmp.*")))


if __name__ == "__main__":
    unittest.main()
