"""Regression coverage for catalog navigation and documented recipe dispatch."""

from __future__ import annotations

import re
import unittest

from test_catalog_regressions import ROOT, SCRIPT, load_validator, run_javascript


class CatalogNavigationTests(unittest.TestCase):
    def test_expansion_focuses_the_first_previously_hidden_card(self):
        data = SCRIPT[:SCRIPT.index("/* ==========================================\n   i18n")]
        utility = SCRIPT[SCRIPT.index("function getCategoryColor("):SCRIPT.index("/* ==========================================\n   Nav")]
        catalog = SCRIPT[SCRIPT.index("let activeCategory ="):SCRIPT.index("document.getElementById('searchInput').addEventListener")]
        harness = r"""
const currentLang = 'ja';
const document = {activeElement: null};
let markup = '', cards = [], more = null;
const count = {};
const grid = {
  get innerHTML() { return markup; },
  set innerHTML(value) {
    document.activeElement = null; // Replacing focused descendants loses focus.
    markup = value;
    cards = [...value.matchAll(/<div class="agent-name">([^<]+)<\/div>/g)].map(match => ({
      name: match[1], attributes: {},
      setAttribute(key, val) { this.attributes[key] = val; },
      focus() { document.activeElement = this; },
    }));
    more = value.includes('id="showMoreBtn"') ? {
      addEventListener(name, callback) { this[name] = callback; },
    } : null;
  },
  querySelectorAll() { return cards; },
};
document.getElementById = id => ({catalogGrid: grid, catalogCount: count, showMoreBtn: more})[id];
document.createElement = () => ({set textContent(value) { this.innerHTML = value; }});
SOURCE
renderCatalog();
const initialCount = cards.length;
document.activeElement = more;
more.click();
console.log(JSON.stringify({initialCount, count: cards.length,
  expected: AGENTS[initialCount].name, active: document.activeElement?.name,
  tabindex: document.activeElement?.attributes.tabindex}));
"""
        result = run_javascript(harness.replace("SOURCE", data + utility + catalog))
        self.assertGreater(result["count"], result["initialCount"])
        self.assertEqual(result.get("active"), result["expected"])
        self.assertEqual(result.get("tabindex"), "-1")

    def test_language_switch_updates_accessible_control_names(self):
        translations = SCRIPT[SCRIPT.index("const TRANSLATIONS ="):SCRIPT.index("const AGENT_DESC_EN =")]
        switching = SCRIPT[SCRIPT.index("function setLanguage("):SCRIPT.index("// Language toggle event")]
        harness = r"""
let currentLang = 'ja';
const nodes = {};
const document = {
  documentElement: {}, querySelectorAll() { return []; }, querySelector() { return {}; },
  getElementById(id) {
    return nodes[id] ||= {setAttribute(key, value) { this[key] = value; }};
  },
};
const localStorage = {setItem() {}};
function renderFilterBar() {}
function renderCatalog() {}
SOURCE
const names = [];
for (const lang of ['en', 'ja']) {
  setLanguage(lang);
  names.push(Object.fromEntries(['searchInput', 'navToggle', 'heroCopyBtn'].map(id =>
    [id, nodes[id]?.['aria-label']])));
}
console.log(JSON.stringify(names));
"""
        result = run_javascript(harness.replace("SOURCE", translations + switching))
        self.assertEqual(result, [
            {"searchInput": "Search agents", "navToggle": "Menu", "heroCopyBtn": "Copy command"},
            {"searchInput": "エージェントを検索", "navToggle": "メニュー", "heroCopyBtn": "コマンドをコピー"},
        ])


class CatalogDispatchTests(unittest.TestCase):
    def test_catalog_recipe_names_are_dispatchable(self):
        validator = load_validator()
        commands = {}
        for name, path in validator.iter_skills():
            block = validator.extract_recipes_block(path.read_text(encoding="utf-8"), path.parent)
            commands[name] = {row[1] for row in validator.parse_rows(block or "")}
        # These inline code identifiers describe types, runners, or profiles,
        # rather than recipes exposed by the named skill.
        identifiers = {"any", "nexus-autoloop", "skill-meta", "legal-jp",
                       "incident-response", "ai-cli-admin"}
        for filename in ("README.md", "README_ja.md", "compass/reference/catalog.md"):
            for line in (ROOT / filename).read_text(encoding="utf-8").splitlines():
                match = re.match(r"^\| \*\*([A-Za-z]+)\*\*", line)
                if not match or match[1].lower() not in commands:
                    continue
                tokens = set(re.findall(r"`([a-z][a-z-]*)`", line)) - identifiers
                with self.subTest(file=filename, skill=match[1]):
                    self.assertLessEqual(tokens, commands[match[1].lower()])


if __name__ == "__main__":
    unittest.main(verbosity=2)
