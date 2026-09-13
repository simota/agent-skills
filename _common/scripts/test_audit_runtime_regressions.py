#!/usr/bin/env python3
"""Runtime regressions for report snapshots and required PDF chart rendering."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

import test_launch_regressions as launch_tests


ROOT = Path(__file__).resolve().parents[2]
NODE = shutil.which("node")
REPORT_ROOTS = ("launch", ".archive/harvest")


@unittest.skipUnless(NODE, "Node.js is required")
class CatalogFocusRegressions(unittest.TestCase):
    def focus_after_render(self, activate):
        html = (ROOT / "index.html").read_text()
        source = html[html.index("function renderFilterBar() {"):html.index("function renderCatalog() {")]
        harness = r"""
const vm = require('vm');
const document = {activeElement: {id: 'searchInput'}, getElementById() {return bar;}};
let buttons = [];
const bar = {
  contains(node) { return buttons.includes(node); },
  set innerHTML(html) {
    if (this.contains(document.activeElement)) document.activeElement = {id: 'body'};
    buttons = [...html.matchAll(/data-cat="([^"]+)"/g)].map(match => ({
      dataset: {cat: match[1]},
      addEventListener(event, fn) {this.click = fn;},
      focus() {document.activeElement = this;},
    }));
  },
  querySelectorAll() {return buttons;},
  querySelector(selector) {return buttons.find(button => selector.includes('"' + button.dataset.cat + '"'));},
};
const context = {document, activeCategory: 'all', currentLang: 'en', AGENTS: [],
  CATEGORIES: [{id: 'all', name: 'All', name_en: 'All', color: '#000'},
               {id: 'quality', name: 'Quality', name_en: 'Quality', color: '#111'}],
  renderCatalog() {},
};
vm.createContext(context);
vm.runInContext(SOURCE + '\nrenderFilterBar();', context);
if (ACTIVATE) { buttons[1].focus(); buttons[1].click(); }
else vm.runInContext('renderFilterBar()', context);
console.log(JSON.stringify({focused: document.activeElement.dataset?.cat || document.activeElement.id,
                           selected: context.activeCategory}));
"""
        harness = harness.replace("SOURCE", json.dumps(source)).replace("ACTIVATE", json.dumps(activate))
        result = subprocess.run([NODE, "-e", harness], capture_output=True, text=True, check=True)
        return json.loads(result.stdout)

    def test_keyboard_filter_activation_preserves_focus(self):
        result = self.focus_after_render(True)
        self.assertEqual(result["selected"], "quality")
        self.assertEqual(result["focused"], "quality")

    def test_translation_render_does_not_steal_focus_from_search(self):
        self.assertEqual(self.focus_after_render(False)["focused"], "searchInput")


@unittest.skipUnless(NODE, "Node.js is required")
class ReportTemplateRegressions(unittest.TestCase):
    def test_dependency_failure_remains_visible_until_both_charts_initialize(self):
        for base in REPORT_ROOTS:
            html = (ROOT / base / "templates/client-report.html").read_text()
            self.assertRegex(html, r'<p\b[^>]*id="chartStatus"[^>]*>[^<]+</p>')
            self.assertEqual(len(re.findall(r'<canvas\b[^>]*\bdata-chartjs\b', html)), 2)
            source = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)[-1]
            source = re.sub(r'\{\{[A-Z_]+\}\}', '[]', source)
            for available in (False, True):
                with self.subTest(base=base, available=available):
                    harness = """
const vm = require('vm');
let statusVisible = true, count = 0;
const context = {document: {getElementById(id) {
  return id === 'chartStatus' ? {remove() {statusVisible = false;}} : {getContext() {return {};}};
}}};
if (AVAILABLE) context.Chart = function() {count++;};
try {vm.runInNewContext(SOURCE, context);} catch (error) {
  if (error.name !== 'ReferenceError' || !error.message.includes('Chart')) throw error;
}
console.log(JSON.stringify({statusVisible, count}));
"""
                    harness = harness.replace("AVAILABLE", json.dumps(available)).replace("SOURCE", json.dumps(source))
                    result = subprocess.run([NODE, "-e", harness], text=True, capture_output=True, check=True)
                    state = json.loads(result.stdout)
                    self.assertEqual(state["statusVisible"], not available)
                    self.assertEqual(state["count"], 2 if available else 0)


@unittest.skipUnless(NODE, "Node.js is required")
class RuntimeRegressions(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.env = dict(os.environ)
        self.env.pop("NODE_OPTIONS", None)

    def run_script(self, base, script, *args):
        return subprocess.run(
            [NODE, str(ROOT / base / "scripts" / script), *map(str, args)],
            cwd=self.work, env=self.env, text=True, capture_output=True, timeout=10,
        )

    def test_report_period_is_frozen_when_fetch_crosses_utc_midnight(self):
        clock = self.work / "clock.txt"
        preload = self.work / "clock.cjs"
        preload.write_text("""
const fs = require('fs');
const RealDate = Date;
global.Date = class extends RealDate {
  constructor(...args) {
    super(...(args.length ? args : [fs.readFileSync(process.env.TEST_CLOCK, 'utf8').trim()]));
  }
  static now() { return new RealDate(fs.readFileSync(process.env.TEST_CLOCK, 'utf8').trim()).getTime(); }
};
""")
        gh = self.work / "gh"
        gh.write_text(f"#!{sys.executable}\n" + """
import json, os, sys
from pathlib import Path
if sys.argv[1:3] == ['pr', 'list']:
    Path(os.environ['TEST_CLOCK']).write_text('2026-09-14T00:00:01Z')
    print(json.dumps([{'number': 1, 'title': 'fix: repair report', 'author': {'login': 'alice'},
        'additions': 100, 'deletions': 0, 'changedFiles': 2, 'labels': [],
        'createdAt': '2026-09-12T00:00:00Z', 'mergedAt': '2026-09-13T23:00:00Z',
        'url': 'https://github.com/owner/repo/pull/1'}]))
else:
    print('owner/repo')
""")
        gh.chmod(0o755)
        self.env.update(
            PATH=str(self.work) + os.pathsep + os.environ["PATH"],
            TEST_CLOCK=str(clock), NODE_OPTIONS=f"--require={preload}",
        )
        for base in REPORT_ROOTS:
            with self.subTest(base=base):
                clock.write_text("2026-09-13T23:59:59Z")
                result = self.run_script(base, "generate-report.js", "--days", "1", "--json")
                self.assertEqual(result.returncode, 0, result.stderr)
                report = json.loads(result.stdout)
                self.assertEqual(report["meta"]["startDate"], "2026-09-13")
                self.assertEqual(report["meta"]["endDate"], "2026-09-13")
                self.assertEqual(report["summary"]["totalTasks"], 1)
                self.assertEqual(sum(report["charts"]["daily"]["data"]),
                                 float(report["summary"]["totalHours"]))
                self.assertEqual(report["charts"]["daily"]["labels"], ["9/13"])

    def prepare_pdf(self, *, required=True, chart_state="missing"):
        module = self.work / "node_modules/puppeteer"
        module.mkdir(parents=True)
        (module / "index.js").write_text("""
const fs = require('fs');
const vm = require('vm');
const canvases = process.env.REQUIRED_CHARTS === '1' ? [{id: 'dailyChart'}, {id: 'categoryChart'}] : [];
const log = item => fs.appendFileSync(process.env.BROWSER_LOG, JSON.stringify(item) + '\\n');
const charts = canvases.map(canvas => ({canvas,
  stop() { log({stopped: canvas.id}); },
  update(mode) { log({updated: canvas.id, mode}); },
}));
const context = {document: {fonts: {ready: Promise.resolve()}, querySelectorAll() { return canvases; }}};
if (process.env.CHART_STATE !== 'missing') {
  context.Chart = {instances: Object.fromEntries(charts.map((chart, i) => [i, chart])),
    getChart(canvas) {
      return process.env.CHART_STATE === 'partial' && canvas.id === 'categoryChart'
        ? undefined : charts.find(chart => chart.canvas === canvas);
    }};
}
module.exports.launch = async () => ({
  async newPage() { return {
    async goto() {},
    async evaluate(fn) { return vm.runInNewContext('(' + fn.toString() + ')()', context); },
    async pdf(options) { log({printed: true}); fs.writeFileSync(options.path, '%PDF-1.7\\nfixture'); },
  }; },
  async close() { log({closed: true}); },
});
""")
        self.env.update(
            NODE_PATH=str(self.work / "node_modules"),
            REQUIRED_CHARTS="1" if required else "0", CHART_STATE=chart_state,
            BROWSER_LOG=str(self.work / "browser.jsonl"),
        )
        self.input = self.work / "report.html"
        self.input.write_text('<html><canvas id="dailyChart" data-chartjs></canvas></html>')

    def pdf_logs(self):
        return [json.loads(line) for line in (self.work / "browser.jsonl").read_text().splitlines()]

    def test_missing_chart_dependency_does_not_publish_incomplete_pdf(self):
        self.prepare_pdf()
        for base in REPORT_ROOTS:
            with self.subTest(base=base):
                output = self.work / "report.pdf"
                output.write_bytes(b"previous complete PDF")
                result = self.run_script(base, "puppeteer-pdf.js", self.input, output)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Chart", result.stderr)
                self.assertEqual(output.read_bytes(), b"previous complete PDF")
                self.assertIn({"closed": True}, self.pdf_logs())
                self.assertNotIn({"printed": True}, self.pdf_logs())

    def test_uninitialized_required_chart_is_an_export_failure(self):
        self.prepare_pdf(chart_state="partial")
        for base in REPORT_ROOTS:
            with self.subTest(base=base):
                output = self.work / "partial.pdf"
                result = self.run_script(base, "puppeteer-pdf.js", self.input, output)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("categoryChart", result.stderr)
                self.assertFalse(output.exists())
                self.assertIn({"closed": True}, self.pdf_logs())

    def test_initialized_charts_are_finished_before_printing(self):
        self.prepare_pdf(chart_state="ready")
        for base in REPORT_ROOTS:
            with self.subTest(base=base):
                output = self.work / "complete.pdf"
                result = self.run_script(base, "puppeteer-pdf.js", self.input, output)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(output.read_bytes().startswith(b"%PDF-"))
                self.assertIn({"updated": "dailyChart", "mode": "none"}, self.pdf_logs())
                self.assertIn({"updated": "categoryChart", "mode": "none"}, self.pdf_logs())

    def test_generic_html_without_chartjs_can_still_be_printed(self):
        self.prepare_pdf(required=False)
        for base in REPORT_ROOTS:
            with self.subTest(base=base):
                result = self.run_script(base, "puppeteer-pdf.js", self.input, self.work / "plain.pdf")
                self.assertEqual(result.returncode, 0, result.stderr)


class ArchivedReportRegressions(launch_tests.ReportRegressions):
    """The archived CLI is executable and must retain the same safety guarantees."""

    def report(self, *args):
        return self.run_cli([NODE, str(ROOT / ".archive/harvest/scripts/generate-report.js"), *args])


class ArchivedPdfShellRegressions(launch_tests.PdfShellRegressions):
    def pdf(self, *args):
        return self.run_cli([launch_tests.BASH,
                             str(ROOT / ".archive/harvest/scripts/html-to-pdf.sh"),
                             *map(str, args)])


class ArchivedPuppeteerRegressions(launch_tests.PuppeteerRegressions):
    def pdf(self):
        return self.run_cli([NODE, str(ROOT / ".archive/harvest/scripts/puppeteer-pdf.js"),
                             str(self.input), str(self.work / "output.pdf")])


if __name__ == "__main__":
    unittest.main(verbosity=2)
