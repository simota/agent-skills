#!/usr/bin/env python3
"""Check public catalog data and language switching against real skill definitions."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")
SCRIPT = re.findall(r"<script>(.*?)</script>", HTML, re.DOTALL)[-1]


def run_javascript(source: str) -> dict:
    result = subprocess.run(
        ["node", "-e", source], cwd=ROOT, text=True, capture_output=True, check=True,
    )
    return json.loads(result.stdout)


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "catalog_recipes", Path(__file__).with_name("validate-recipes.py"),
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CatalogDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        prefix = SCRIPT[:SCRIPT.index("/* ==========================================\n   i18n")]
        cls.data = run_javascript(prefix + "\nconsole.log(JSON.stringify({agents:AGENTS,subs:SUBCOMMANDS,categories:CATEGORIES}));")
        cls.global_skills = {path.parent.name for path in ROOT.glob("*/SKILL.md")}
        cls.local_skills = {
            path.parent.name for path in (ROOT / ".claude/skills").glob("*/SKILL.md")
        }

    def test_only_active_skills_are_advertised_once(self):
        names = [agent["name"].lower() for agent in self.data["agents"]]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(set(names), self.global_skills | self.local_skills)
        local = {
            agent["name"].lower() for agent in self.data["agents"]
            if agent["category"] == "project-local"
        }
        self.assertEqual(local, self.local_skills)
        categories = {category["id"] for category in self.data["categories"]}
        self.assertTrue(all(agent["category"] in categories for agent in self.data["agents"]))

    def test_advertised_subcommands_match_the_skill_recipe_tables(self):
        validator = load_validator()
        expected = {}
        for name, path in validator.iter_skills():
            block = validator.extract_recipes_block(path.read_text(encoding="utf-8"), path.parent)
            expected[name] = {row[1] for row in validator.parse_rows(block or "")}
        actual = {name.lower(): rows for name, rows in self.data["subs"].items()}
        self.assertEqual(set(actual), set(expected))
        for name, commands in expected.items():
            with self.subTest(skill=name):
                names = [row["n"] for row in actual[name]]
                self.assertEqual(len(names), len(set(names)), "duplicate subcommand")
                self.assertEqual(set(names), commands)
                self.assertTrue(all(row["d"] for row in actual[name]))

    def test_counts_and_english_descriptions_match_the_active_roster(self):
        metadata = json.loads(re.search(
            r'<script type="application/ld\+json">(.*?)</script>', HTML, re.DOTALL,
        ).group(1))
        item_list = next(item for item in metadata if item["@type"] == "ItemList")
        self.assertEqual(item_list["numberOfItems"], len(self.global_skills | self.local_skills))
        self.assertIn(f'data-count="{len(self.global_skills)}"', HTML)
        for description in [item["description"] for item in metadata if "description" in item]:
            self.assertIn(f"{len(self.global_skills)} global", description)
        source = SCRIPT[SCRIPT.index("const AGENT_DESC_EN ="):SCRIPT.index("function setLanguage(")]
        translations = run_javascript(source + "console.log(JSON.stringify(AGENT_DESC_EN));")
        self.assertEqual({name.lower() for name in translations}, self.global_skills | self.local_skills)


class LanguagePreferenceTests(unittest.TestCase):
    def run_switch(self, stored=None, read_error=None, write_error=None, switches=None):
        # Execute the actual preference and translation functions with only the
        # storage/DOM boundary replaced. No browser package is required in CI.
        preference = SCRIPT[SCRIPT.index("/* ==========================================\n   i18n"):SCRIPT.index("const TRANSLATIONS =")]
        translations = SCRIPT[SCRIPT.index("const TRANSLATIONS ="):SCRIPT.index("const AGENT_DESC_EN =")]
        switching = SCRIPT[SCRIPT.index("function setLanguage("):SCRIPT.index("// Language toggle event")]
        options = json.dumps({"stored": stored, "readError": read_error, "writeError": write_error, "switches": switches or []})
        harness = r"""
const options = OPTIONS;
const vm = require('node:vm');
const saved = [];
const title = {textContent: ''};
const description = {content: ''};
const search = {setAttribute() {}};
const text = {dataset: {i18n: 'catalog.title'}, innerHTML: 'エージェントを探す'};
const input = {dataset: {i18nPlaceholder: 'catalog.search'}, placeholder: 'エージェントを検索'};
const buttons = ['ja', 'en'].map(lang => ({dataset: {lang}, classList: {toggle() {}}, setAttribute() {}}));
let renders = 0;
const fail = name => { const error = new Error(name); error.name = name; throw error; };
const context = {
  localStorage: {
    getItem() { if (options.readError) fail(options.readError); return options.stored; },
    setItem(key, value) { if (options.writeError) fail(options.writeError); saved.push(value); },
  },
  document: {
    documentElement: {lang: 'ja'},
    querySelectorAll(selector) {
      return selector === '.lang-btn' ? buttons : selector === '[data-i18n]' ? [text] : [input];
    },
    querySelector(selector) { return selector === 'title' ? title : description; },
    getElementById() { return search; },
  },
  renderFilterBar() { renders++; }, renderCatalog() { renders++; },
};
vm.createContext(context);
vm.runInContext(SOURCE, context);
const initial = vm.runInContext('currentLang', context);
for (const lang of options.switches) vm.runInContext(`setLanguage(${JSON.stringify(lang)})`, context);
console.log(JSON.stringify({initial, current: vm.runInContext('currentLang', context),
  lang: context.document.documentElement.lang, text: text.innerHTML, placeholder: input.placeholder, saved, renders}));
"""
        harness = harness.replace("OPTIONS", options).replace("SOURCE", json.dumps(preference + translations + switching))
        return run_javascript(harness)

    def test_blocked_storage_does_not_prevent_translation(self):
        result = self.run_switch(read_error="SecurityError", write_error="SecurityError", switches=["en"])
        self.assertEqual(result["initial"], "ja")
        self.assertEqual(result["lang"], "en")
        self.assertEqual(result["text"], "Find an Agent")
        self.assertEqual(result["renders"], 2)

    def test_full_storage_does_not_prevent_translation(self):
        result = self.run_switch(write_error="QuotaExceededError", switches=["en", "ja"])
        self.assertEqual(result["current"], "ja")
        self.assertEqual(result["text"], "エージェントを探す")
        self.assertEqual(result["placeholder"], "エージェントを検索")
        self.assertEqual(result["renders"], 4)

    def test_unsupported_stored_language_uses_japanese(self):
        self.assertEqual(self.run_switch(stored="fr")["initial"], "ja")
        self.assertEqual(self.run_switch(stored="en")["initial"], "en")

    def test_language_round_trip_restores_original_text(self):
        result = self.run_switch(switches=["en", "ja", "fr"])
        self.assertEqual(result["lang"], "ja")
        self.assertEqual(result["text"], "エージェントを探す")
        self.assertEqual(result["saved"], ["en", "ja"])


class ClipboardTests(unittest.TestCase):
    def run_copy(self, mode):
        source = SCRIPT[SCRIPT.index("const copyResetTimers ="):SCRIPT.index("document.querySelectorAll('.copy-btn')")]
        setup = r"""
const mode = MODE;
const writes = [];
let warnings = 0;
const navigator = {};
if (mode !== 'unsupported') navigator.clipboard = {async writeText(text) {
  if (mode === 'denied') throw new Error('Clipboard permission denied');
  writes.push(text);
}};
const currentLang = 'en';
const button = {textContent: 'Copy', title: '', classList: {toggle() {}, remove() {}}, setAttribute() {}};
const console = {warn() { warnings++; }};
const setTimeout = () => 1;
const clearTimeout = () => {};
"""
        # The promise must settle even when permissions or API support are absent.
        finish = "\ncopyCommand(button, 'git clone example').then(copied => process.stdout.write(JSON.stringify({copied, text:button.textContent, title:button.title, writes, warnings})));"
        return run_javascript(setup.replace("MODE", json.dumps(mode)) + source + finish)

    def test_successful_copy_shows_confirmation(self):
        result = self.run_copy('success')
        self.assertTrue(result['copied'])
        self.assertEqual(result['writes'], ['git clone example'])
        self.assertEqual(result['text'], 'Copied!')
        self.assertFalse(result['warnings'])

    def test_denied_copy_provides_manual_instructions(self):
        result = self.run_copy('denied')
        self.assertFalse(result['copied'])
        self.assertEqual(result['text'], 'Copy failed')
        self.assertIn('manually', result['title'])
        self.assertEqual(result['warnings'], 1)

    def test_unsupported_clipboard_provides_manual_instructions(self):
        result = self.run_copy('unsupported')
        self.assertFalse(result['copied'])
        self.assertEqual(result['text'], 'Copy failed')
        self.assertIn('manually', result['title'])


if __name__ == "__main__":
    unittest.main(verbosity=2)
