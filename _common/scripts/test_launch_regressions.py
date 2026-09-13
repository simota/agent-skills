#!/usr/bin/env python3
"""Offline CLI regressions for report generation, PDF export, and render gates."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[2]
NODE = shutil.which("node")
BASH = shutil.which("bash")


class CliFixtures(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.bin = self.work / "bin"
        self.bin.mkdir()
        self.env = dict(os.environ, PATH=f"{self.bin}{os.pathsep}{os.environ['PATH']}")
        self.env.pop("NODE_OPTIONS", None)

    def executable(self, name, body):
        target = self.bin / name
        target.write_text(f"#!{sys.executable}\n" + body)
        target.chmod(0o755)
        return target

    def run_cli(self, argv, **kwargs):
        return subprocess.run(argv, cwd=self.work, env=self.env, capture_output=True,
                              text=True, timeout=10, **kwargs)


@unittest.skipUnless(NODE, "Node.js is required")
class ReportRegressions(CliFixtures):
    def setUp(self):
        super().setUp()
        self.prs = self.work / "prs.json"
        self.calls = self.work / "calls.jsonl"
        self.env.update(PR_FIXTURE=str(self.prs), GH_CALLS=str(self.calls))
        self.executable("gh", """import json, os, sys
from pathlib import Path
with open(os.environ['GH_CALLS'], 'a') as log:
    log.write(json.dumps(sys.argv[1:]) + '\\n')
if sys.argv[1:3] == ['pr', 'list']:
    print(Path(os.environ['PR_FIXTURE']).read_text())
else:
    print('owner/repo')
""")
        clock = self.work / "clock.cjs"
        clock.write_text("const RealDate = Date; global.Date = class extends RealDate {"
                         "constructor(...args) { super(...(args.length ? args : ['2026-09-13T12:00:00Z'])); }"
                         "static now() { return new RealDate('2026-09-13T12:00:00Z').getTime(); }};")
        self.env["NODE_OPTIONS"] = f"--require={clock}"
        self.write_prs([self.pr()])

    def pr(self, **overrides):
        return dict(dict(number=7, title="feat(api)!: ship <new> endpoint", author={"login": "alice"},
                    additions=100, deletions=0, changedFiles=2, labels=[],
                    createdAt="2026-01-01T12:00:00Z", mergedAt="2026-09-13T01:00:00Z",
                    url="https://github.com/owner/repo/pull/7"), **overrides)

    def write_prs(self, prs):
        self.prs.write_text(json.dumps(prs))

    def report(self, *args):
        return self.run_cli([NODE, str(ROOT / "launch/scripts/generate-report.js"), *args])

    def data(self, *args):
        result = self.report("--json", *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        # Permit old diagnostic prefixes here so independent aggregation bugs remain visible.
        return json.loads(result.stdout[result.stdout.find("{"):])

    def test_json_stdout_contains_only_json(self):
        result = self.report("--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["summary"]["totalTasks"], 1)

    def test_empty_period_still_emits_json(self):
        self.write_prs([])
        result = self.report("--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["summary"]["totalTasks"], 0)

    def test_empty_period_replaces_previous_html_with_empty_report(self):
        self.write_prs([])
        output = self.work / "report.html"
        output.write_text("old report")
        result = self.report("--output", str(output))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("old report", output.read_text())
        self.assertIn('<div class="summary-value">0</div>', output.read_text())

    def test_author_is_not_interpreted_by_a_shell(self):
        marker = self.work / "injected"
        author = f"alice; touch {marker}; #"
        result = self.report("--json", "--author", author)
        self.assertFalse(marker.exists(), "author argument executed a shell command")
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = [json.loads(line) for line in self.calls.read_text().splitlines()]
        self.assertIn(author, calls[0])

    def test_invalid_options_fail_before_fetching(self):
        for args in [("--days", "0"), ("--days", "-1"), ("--days", "7days"),
                     ("--days", "NaN"), ("--author",), ("--repo",), ("--output",),
                     ("--template",), ("--unknown",)]:
            with self.subTest(args=args):
                self.calls.unlink(missing_ok=True)
                result = self.report(*args)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(self.calls.exists(), "invalid options reached gh")

    def test_scoped_breaking_conventional_commit_is_classified(self):
        self.assertEqual(self.data()["prs"][0]["category"], "feat")

    def test_period_and_chart_cover_every_requested_utc_day(self):
        self.env["TZ"] = "America/Los_Angeles"
        data = self.data("--days", "30")
        self.assertEqual(data["meta"]["startDate"], "2026-08-15")
        self.assertEqual(data["meta"]["startDateFormatted"], "2026年8月15日")
        self.assertEqual(len(data["charts"]["daily"]["data"]), 30)
        self.assertEqual(data["charts"]["daily"]["labels"][-1], "9/13")
        self.assertEqual(sum(data["charts"]["daily"]["data"]), float(data["summary"]["totalHours"]))
        self.assertEqual(data["prs"][0]["mergedDate"], "09/13")

    def test_date_filter_is_sent_before_server_limit(self):
        self.data()
        args = json.loads(self.calls.read_text().splitlines()[0])
        self.assertIn("--search", args)
        self.assertIn("merged:>=2026-09-07", args[args.index("--search") + 1])

    def test_truncated_collection_does_not_create_partial_report(self):
        self.write_prs([dict(self.pr(), number=i) for i in range(501)])
        result = self.report("--output", "partial.html")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.work / "partial.html").exists())
        self.assertIn("500", result.stderr)

    def test_default_html_has_real_rows_and_no_sample_tasks(self):
        result = self.report("--output", "report.html")
        self.assertEqual(result.returncode, 0, result.stderr)
        html = (self.work / "report.html").read_text()
        self.assertIn("feat(api)!: ship &lt;new&gt; endpoint", html)
        self.assertNotIn("Sweep スキル安全性", html)
        self.assertNotIn("79.5h", html)
        self.assertNotIn("Guardian, Arena", html)
        self.assertNotIn("{{", html)

    def test_custom_template_escapes_metadata_without_replacement_expansion(self):
        template = self.work / "custom.html"
        template.write_text("<p>{{AUTHOR}}</p><div>{{TABLE_ROWS}}</div>")
        author = "<img src=x onerror=alert(1)> $& {{AUTHOR}}"
        result = self.report("--author", author, "--template", "custom.html", "--output", "report.html")
        self.assertEqual(result.returncode, 0, result.stderr)
        html = (self.work / "report.html").read_text()
        self.assertIn("<p>&lt;img src=x onerror=alert(1)&gt; $&amp; {{AUTHOR}}</p>", html)
        self.assertNotIn("<img", html)

    def test_explicit_missing_template_is_an_error(self):
        result = self.report("--template", "missing.html", "--output", "report.html")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.work / "report.html").exists())


@unittest.skipUnless(BASH, "Bash is required")
class PdfShellRegressions(CliFixtures):
    def setUp(self):
        super().setUp()
        self.input = self.work / "input.html"
        self.input.write_text("<html>fixture</html>")
        self.output = self.work / "output.pdf"
        self.executable("google-chrome", """import json, os, sys
from pathlib import Path
args = sys.argv[1:]
if os.environ.get('CHROME_NO_OUTPUT') != '1':
    output = next(a.split('=', 1)[1] for a in args if a.startswith('--print-to-pdf='))
    Path(output).write_bytes(b'%PDF-1.7\\n' + b'x' * 1100 + b'\\n%%EOF\\n')
if os.environ.get('CHROME_ARGS'):
    Path(os.environ['CHROME_ARGS']).write_text(json.dumps(args))
""")

    def pdf(self, *args):
        return self.run_cli([BASH, str(ROOT / "launch/scripts/html-to-pdf.sh"), *map(str, args)])

    def test_shell_metacharacters_in_paths_are_literal(self):
        path = self.work / 'input$(touch injected) #%.html'
        path.write_text("<html>fixture</html>")
        self.env["CHROME_ARGS"] = str(self.work / "chrome-args.json")
        result = self.pdf("--method", "chrome", path, self.output)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.work / "injected").exists())
        args = json.loads(Path(self.env["CHROME_ARGS"]).read_text())
        self.assertIn(path.as_uri(), args)

    def test_stale_output_is_not_accepted(self):
        previous = b'%PDF-1.7\n' + b'old' * 400
        self.output.write_bytes(previous)
        self.env["CHROME_NO_OUTPUT"] = "1"
        result = self.pdf("--method", "chrome", self.input, self.output)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.output.read_bytes(), previous)

    def test_input_and_output_cannot_be_the_same_file(self):
        original = self.input.read_bytes()
        result = self.pdf("--method", "chrome", self.input, self.input)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.input.read_bytes(), original)

    def test_timeout_without_gnu_timeout_stops_converter(self):
        for command in ("dirname", "mktemp", "rm", "sleep", "wc", "head", "mv"):
            target = shutil.which(command)
            self.assertIsNotNone(target)
            (self.bin / command).symlink_to(target)
        self.env["PATH"] = str(self.bin)
        self.env["CONVERTER_PID"] = str(self.work / "converter.pid")
        self.executable("google-chrome", """import os, signal, time
from pathlib import Path
Path(os.environ['CONVERTER_PID']).write_text(str(os.getpid()))
signal.signal(signal.SIGTERM, signal.SIG_IGN)
time.sleep(30)
""")
        started = time.monotonic()
        result = self.pdf("--method", "chrome", "--timeout", "1", self.input, self.output)
        self.assertNotEqual(result.returncode, 0)
        self.assertLess(time.monotonic() - started, 5)
        pid = int(Path(self.env["CONVERTER_PID"]).read_text())
        with self.assertRaises(ProcessLookupError):
            os.kill(pid, 0)
        self.assertFalse(self.output.exists())

    def test_failed_converter_falls_back_to_next_method(self):
        self.env["CHROME_NO_OUTPUT"] = "1"
        self.executable("wkhtmltopdf", """import sys
from pathlib import Path
Path(sys.argv[-1]).write_bytes(b'%PDF-1.7\\n' + b'x' * 1100 + b'\\n%%EOF\\n')
""")
        result = self.pdf(self.input, self.output)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Done (wkhtmltopdf)", result.stdout)
        self.assertTrue(self.output.read_bytes().startswith(b"%PDF-"))

    def test_unknown_options_and_extra_paths_are_rejected(self):
        for args in [("--bad", self.input), ("--timeout", "0", self.input),
                     (self.input, self.output, self.work / "extra.pdf")]:
            with self.subTest(args=args):
                result = self.pdf(*args)
                self.assertNotEqual(result.returncode, 0)


@unittest.skipUnless(NODE, "Node.js is required")
class PuppeteerRegressions(CliFixtures):
    def setUp(self):
        super().setUp()
        module = self.work / "node_modules/puppeteer"
        module.mkdir(parents=True)
        self.env.update(NODE_PATH=str(self.work / "node_modules"), PDF_LOG=str(self.work / "browser.jsonl"))
        (module / "index.js").write_text("""
const fs = require('fs');
const log = x => fs.appendFileSync(process.env.PDF_LOG, JSON.stringify(x) + '\\n');
module.exports.launch = async options => {
  log({launch: options});
  return {
    async newPage() { return {
      async goto(url) { log({url}); if (process.env.PDF_FAIL) throw Error('navigation failed'); },
      async evaluate() {},
      async pdf(options) { log({pdf: options}); fs.writeFileSync(options.path, '%PDF-1.7\\nfixture\\n%%EOF\\n'); }
    }; },
    async close() { log({closed: true}); }
  };
};
""")
        self.input = self.work / "input #%.html"
        self.input.write_text("<html>fixture</html>")

    def pdf(self):
        return self.run_cli([NODE, str(ROOT / "launch/scripts/puppeteer-pdf.js"),
                             str(self.input), str(self.work / "output.pdf")])

    def logs(self):
        return [json.loads(x) for x in Path(self.env["PDF_LOG"]).read_text().splitlines()]

    def test_current_api_and_encoded_file_url(self):
        result = self.pdf()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn({"url": self.input.as_uri()}, self.logs())
        self.assertIn({"closed": True}, self.logs())

    def test_browser_is_closed_when_navigation_fails(self):
        self.env["PDF_FAIL"] = "1"
        result = self.pdf()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn({"closed": True}, self.logs())


@unittest.skipUnless(BASH, "Bash is required")
class RenderGateRegressions(CliFixtures):
    def gate(self, *args):
        return self.run_cli([BASH, str(ROOT / "_templates/learning-loop-kit/_scripts/check-rendered.sh"), *map(str, args)])

    def test_scan_error_is_not_reported_as_clean(self):
        self.executable("grep", "import sys\nsys.exit(2)\n")
        result = self.gate(self.work)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("is clean", result.stdout)

    def test_leading_dash_directory_is_not_an_option(self):
        kit = self.work / "-kit"
        kit.mkdir()
        (kit / "README.md").write_text("{{KIT_NAME}}")
        result = self.gate("-kit")
        self.assertEqual(result.returncode, 1, result.stderr)

    def test_template_date_placeholders_are_allowed(self):
        kit = self.work / "kit"
        (kit / "_templates").mkdir(parents=True)
        (kit / "README.md").write_text("A fully rendered kit")
        (kit / "_templates/entry.md").write_text("YYYY-MM-DD <slug>")
        self.assertEqual(self.gate(kit).returncode, 0)


if __name__ == "__main__":
    unittest.main()
