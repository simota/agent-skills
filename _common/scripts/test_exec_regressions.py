#!/usr/bin/env python3
"""Regressions for executable launch/report code, token-economy CLI defaults,
and the catalog page's storage handling."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
NODE = shutil.which("node")


def node_json(source: str) -> dict:
    result = subprocess.run([NODE, "-e", source], text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


class TempDir(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.work = Path(temp.name)


@unittest.skipUnless(NODE, "Node.js is required")
class PuppeteerResolution(TempDir):
    def test_puppeteer_installed_in_the_working_directory_is_found(self):
        # The documented install is `npm install puppeteer` in the caller's
        # project; Node's bare require() only searches the script's directory.
        module = self.work / "node_modules/puppeteer"
        module.mkdir(parents=True)
        (module / "index.js").write_text("""
const fs = require('fs');
module.exports.launch = async () => ({
  async newPage() { return {
    async goto() {}, async evaluate() {},
    async pdf(o) { fs.writeFileSync(o.path, '%PDF-1.7\\n%%EOF\\n'); }
  }; },
  async close() {}
});
""")
        (self.work / "in.html").write_text("<html></html>")
        env = {k: v for k, v in os.environ.items() if k not in ("NODE_PATH", "NODE_OPTIONS")}
        result = subprocess.run(
            [NODE, str(ROOT / "launch/scripts/puppeteer-pdf.js"), "in.html", "out.pdf"],
            cwd=self.work, env=env, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.work / "out.pdf").read_bytes().startswith(b"%PDF-"))


class TokenEconomyDefaults(TempDir):
    def setUp(self):
        super().setUp()
        self.repo = self.work / "my.repo_root"
        self.repo.mkdir()
        # Claude Code's naming: absolute path, every non-alphanumeric -> '-'.
        self.name = re.sub(r"[^A-Za-z0-9]", "-", str(self.repo))
        project = self.work / "home/.claude/projects" / self.name
        project.mkdir(parents=True)
        record = {"type": "assistant", "requestId": "req_1", "sessionId": "s1",
                  "timestamp": "2026-01-01T00:00:00Z", "version": "1.0.0",
                  "message": {"id": "msg_1", "content": [], "usage": {
                      "input_tokens": 1, "cache_creation_input_tokens": 2,
                      "cache_read_input_tokens": 3, "output_tokens": 4}}}
        (project / "s1.jsonl").write_text(json.dumps(record) + "\n")
        self.env = dict(os.environ, HOME=str(self.work / "home"))

    def economy(self, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / "_common/scripts/token-economy.py"), "--json", *args],
            env=self.env, capture_output=True, text=True, timeout=30)

    def test_default_project_dir_is_derived_from_the_repo_root(self):
        result = self.economy("--repo-root", str(self.repo))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["grand_total"], 10)

    def test_explicit_repo_root_never_falls_back_to_the_legacy_dir(self):
        # Only the legacy directory exists: an explicit --repo-root that has no
        # transcripts must fail rather than report this repository's usage.
        legacy = self.work / "home/.claude/projects/-Users-simota--claude-skills"
        (self.work / "home/.claude/projects" / self.name).rename(legacy)
        result = self.economy("--repo-root", str(self.repo))
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("project dir not found", result.stderr)

    def test_project_dir_name_with_leading_dash_is_accepted(self):
        result = self.economy("--project-dir", self.name)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["grand_total"], 10)


@unittest.skipUnless(NODE, "Node.js is required")
class ReportCategoryChart(unittest.TestCase):
    def test_every_category_gets_a_distinct_doughnut_color(self):
        report = (ROOT / "launch/scripts/generate-report.js").read_text()
        labels = re.search(r"const categoryLabels = \{(.*?)\};", report, re.DOTALL).group(1)
        categories = re.findall(r"^\s*(\w+):", labels, re.MULTILINE)
        self.assertGreaterEqual(len(categories), 9)
        html = (ROOT / "launch/templates/client-report.html").read_text()
        source = re.findall(r"<script>(.*?)</script>", html, re.DOTALL)[-1]
        source = re.sub(r"\{\{[A-Z_]+\}\}", "[]", source)
        harness = """
const vm = require('vm');
const configs = [];
const context = {document: {getElementById() { return {getContext() { return {}; }, remove() {}}; }},
  Chart: function(ctx, config) { configs.push(config); }};
vm.runInNewContext(SOURCE, context);
console.log(JSON.stringify(configs.map(c => c.data.datasets[0].backgroundColor)));
""".replace("SOURCE", json.dumps(source))
        colors = node_json(harness)[1]
        self.assertIsInstance(colors, list)
        self.assertGreaterEqual(len(set(colors)), len(categories))

    def test_chart_library_version_is_pinned(self):
        html = (ROOT / "launch/templates/client-report.html").read_text()
        src = re.search(r'<script src="([^"]*chart\.js[^"]*)"', html).group(1)
        self.assertRegex(src, r"chart\.js@\d+\.\d+\.\d+")


@unittest.skipUnless(NODE, "Node.js is required")
class CatalogDisabledStorage(unittest.TestCase):
    def test_null_local_storage_does_not_break_translation(self):
        # Browsers with DOM storage disabled expose `localStorage` as null.
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        script = re.findall(r"<script>(.*?)</script>", html, re.DOTALL)[-1]
        start = script.index("/* ==========================================\n   i18n")
        source = (script[start:script.index("const AGENT_DESC_EN =")]
                  + script[script.index("function setLanguage("):script.index("// Language toggle event")])
        harness = r"""
const vm = require('vm');
const text = {dataset: {i18n: 'catalog.title'}, innerHTML: 'エージェントを探す'};
const node = {setAttribute() {}, textContent: '', content: ''};
let renders = 0;
const context = {
  localStorage: null,
  document: {
    documentElement: {lang: 'ja'},
    querySelectorAll(selector) { return selector === '[data-i18n]' ? [text] : []; },
    querySelector() { return node; },
    getElementById() { return node; },
  },
  renderFilterBar() { renders++; }, renderCatalog() { renders++; },
};
vm.createContext(context);
vm.runInContext(SOURCE, context);
const initial = vm.runInContext('currentLang', context);
vm.runInContext("setLanguage('en')", context);
console.log(JSON.stringify({initial, lang: context.document.documentElement.lang, text: text.innerHTML, renders}));
""".replace("SOURCE", json.dumps(source))
        result = node_json(harness)
        self.assertEqual(result["initial"], "ja")
        self.assertEqual(result["lang"], "en")
        self.assertEqual(result["text"], "Find an Agent")
        self.assertEqual(result["renders"], 2)


if __name__ == "__main__":
    unittest.main()
