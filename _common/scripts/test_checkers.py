#!/usr/bin/env python3
"""Prove the checkers in this directory actually catch things.

A checker nobody has watched fail is indistinguishable from one that returns
zero unconditionally. It passes CI, it passes review, and it enforces nothing --
and because it is *reported* as enforcement, it also stops anyone from looking
for the enforcement that is missing. Two live instances motivated this file:

  * `lint-instructions.py` I1 matched neither instruction file's phrasing and
    reported OK across three unchecked skill-count claims.
  * `lint-contracts.py` CD-3 walked `.agents/`, which is gitignored, and so
    reported OK locally on precisely the state CI rejected.

Neither is a subtle bug. Both survived because nothing here had ever seen the
check fail.

Each test breaks one thing in a copy of the repository and asserts that the
matching check fails *and says why*. A test that only asserts a non-zero exit
would pass against a checker that crashes, which is a different defect wearing
the same exit code.

    python3 _common/scripts/test_checkers.py
    python3 _common/scripts/test_checkers.py -k contracts     # one group

Adding a check to any script in this directory means adding a test here that
watches it fail. That rule is the point of the file.
"""

from __future__ import annotations

import datetime
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = Path("_common/scripts")

#: Excluded from the working copy: `.git` is large and no checker reads it, and
#: `__pycache__` would shadow edited sources. Interrupted `checker-tests-*`
#: fixtures are generated copies, not corpus content. No corpus directory is
#: excluded -- the first draft dropped `.archive/` on the reasoning that
#: `_corpus.INFRA_DIRS` skips it, and the baseline immediately failed: RO-1
#: resolves a reference by searching the whole tree, archive included. An
#: exclusion that changes what a checker sees makes the suite test a repository
#: nobody has.
IGNORE = shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "checker-tests-*")

#: One shared copy for the whole suite. Each test edits and restores; copying
#: 24MB per test would make the suite slow enough that nobody runs it, which is
#: the same failure this file exists to prevent.
_WORKSPACE: Path | None = None
_TMP: Path | None = None


def copy_repository(source: Path, destination: Path, temporary_root: Path) -> None:
    """Copy a fixture even when tempfile falls back to a directory in the repo."""
    excluded_parent = temporary_root.parent.resolve()

    def ignore(directory: str, names: list[str]) -> set[str]:
        excluded = set(IGNORE(directory, names))
        if Path(directory).resolve() == excluded_parent:
            excluded.add(temporary_root.name)
        return excluded

    shutil.copytree(source, destination, ignore=ignore, symlinks=True)


def setUpModule() -> None:
    global _WORKSPACE, _TMP
    _TMP = Path(tempfile.mkdtemp(prefix="checker-tests-"))
    _WORKSPACE = _TMP / "repo"
    try:
        copy_repository(REPO_ROOT, _WORKSPACE, _TMP)
    except BaseException:
        shutil.rmtree(_TMP, ignore_errors=True)
        raise


def tearDownModule() -> None:
    if _TMP is not None:
        shutil.rmtree(_TMP, ignore_errors=True)


class CheckerCase(unittest.TestCase):
    """Edit the working copy, run one checker against it, restore."""

    def setUp(self) -> None:
        assert _WORKSPACE is not None
        self.repo = _WORKSPACE
        self._saved: dict[Path, str] = {}

    def tearDown(self) -> None:
        for path, text in self._saved.items():
            path.write_text(text, encoding="utf-8")

    # -- editing -----------------------------------------------------------

    def _remember(self, rel: str) -> Path:
        path = self.repo / rel
        if path not in self._saved:
            self._saved[path] = path.read_text(encoding="utf-8")
        return path

    def edit(self, rel: str, old: str, new: str) -> None:
        """Replace the first occurrence of `old`, asserting it was there.

        The assertion matters as much as the edit: when the corpus moves, a
        fixture that silently matches nothing turns its test into one that
        breaks nothing and passes anyway.
        """
        path = self._remember(rel)
        text = path.read_text(encoding="utf-8")
        if old not in text:
            self.fail(f"fixture drifted: {old!r} absent from {rel}")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def append(self, rel: str, text: str) -> None:
        path = self._remember(rel)
        path.write_text(path.read_text(encoding="utf-8") + text, encoding="utf-8")

    def write_new(self, rel: str, text: str) -> None:
        path = self.repo / rel
        self.assertFalse(path.exists(), f"{rel} already exists; pick another fixture path")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        self.addCleanup(path.unlink)

    # -- running -----------------------------------------------------------

    def run_checker(self, script: str, *args: str) -> tuple[int, str]:
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / script), *args],
            cwd=self.repo, capture_output=True, text=True,
        )
        return proc.returncode, proc.stdout + proc.stderr

    def expect_clean(self, script: str, *args: str) -> None:
        code, out = self.run_checker(script, *args)
        self.assertEqual(code, 0, f"{script} failed on an unbroken repository\n{out}")

    def expect_caught(self, script: str, needle: str, *args: str) -> None:
        """The checker must exit 1 *and* name the defect."""
        code, out = self.run_checker(script, *args)
        self.assertEqual(code, 1, f"{script} passed a broken repository\n{out}")
        self.assertIn(needle, out, f"{script} failed without naming the defect\n{out}")

    def expect_reported(self, script: str, needle: str, *args: str) -> None:
        """For advisory findings: reported, but not necessarily blocking."""
        _, out = self.run_checker(script, *args)
        self.assertIn(needle, out, f"{script} did not report the defect\n{out}")


class TestBaseline(CheckerCase):
    """An unbroken working copy passes every blocking checker.

    Without this, every other test in the file could be passing because the
    repository is broken for some unrelated reason.
    """

    def test_lint_frontmatter_is_clean(self):
        self.expect_clean("lint-frontmatter.py", "--severity", "error")

    def test_lint_instructions_is_clean(self):
        self.expect_clean("lint-instructions.py", "--severity", "error")

    def test_lint_contracts_is_clean(self):
        self.expect_clean("lint-contracts.py", "--severity", "error")

    def test_validate_recipes_is_clean(self):
        self.expect_clean("validate-recipes.py", "--severity", "error")

    def test_routing_oracle_is_clean(self):
        self.expect_clean("routing-oracle.py", "--severity", "error")

    def test_lint_lessons_is_clean(self):
        self.expect_clean("lint-lessons.py", "--severity", "error")

    def test_index_subcommands_are_fresh(self):
        self.expect_clean("generate-index-subcommands.py", "--check")

    def test_recipes_directory_is_fresh(self):
        self.expect_clean("generate-recipes-directory.py", "--check")

    def test_task_battery_is_clean(self):
        self.expect_clean("task-battery-check.py", "--severity", "error")

    def test_project_local_is_clean(self):
        self.expect_clean("lint-project-local.py", "--severity", "error")


class TestInstructionDrift(CheckerCase):
    """`lint-instructions.py`. I1 is here in three phrasings because its
    original form matched none of them -- a matcher that recognises no claim
    reports OK over every claim, which is the failure mode the whole file is
    about."""

    def test_a_global_skill_count_that_drifts_fails(self):
        self.edit("CLAUDE.md", "90のグローバルスキル", "88のグローバルスキル")
        self.expect_caught("lint-instructions.py", "claims 88 skills", "--severity", "error")

    def test_a_project_local_count_that_drifts_fails(self):
        self.edit("CLAUDE.md", "このリポジトリ専用の3スキル", "このリポジトリ専用の5スキル")
        self.expect_caught(
            "lint-instructions.py", "claims 5 project-local skills", "--severity", "error"
        )

    def test_an_english_count_that_drifts_fails(self):
        """Multi-word qualifier: the first fix handled `global` but not
        `global specialist`, and passed this exact sentence."""
        self.edit("AGENTS.md", "90 global specialist skill", "91 global specialist skill")
        self.expect_caught("lint-instructions.py", "claims 91 skills", "--severity", "error")

    def test_a_global_count_written_as_the_local_one_still_fails(self):
        """Scope matters: a checker that accepted either count would pass a
        sentence claiming three global skills."""
        self.edit("CLAUDE.md", "90のグローバルスキル", "3のグローバルスキル")
        self.expect_caught("lint-instructions.py", "claims 3 skills", "--severity", "error")

    def test_a_repository_local_extension_count_that_drifts_fails(self):
        """I1. AGENTS.md counts the project-local skills as "operating
        extensions", which is not a skill noun, so the claim was never read."""
        self.edit("AGENTS.md", "plus 3 repository-local operating", "plus 7 repository-local operating")
        self.expect_caught(
            "lint-instructions.py", "claims 7 project-local skills", "--severity", "error"
        )

    def test_an_unscoped_extension_count_is_not_a_skill_count(self):
        """I1. "extensions" counts skills only under a local qualifier."""
        self.append("CLAUDE.md", "\n- 2 extensions are loaded by the editor.\n")
        self.expect_clean("lint-instructions.py", "--severity", "error")

    def test_a_dead_path_in_an_instruction_file_fails(self):
        self.edit(
            "CLAUDE.md", "`_common/PROJECT_LOCAL_SKILLS.md`", "`_common/NO_SUCH_CONTRACT.md`"
        )
        self.expect_caught("lint-instructions.py", "NO_SUCH_CONTRACT.md", "--severity", "error")

    def test_a_dead_path_with_a_section_pointer_inside_the_backticks_fails(self):
        """I2. The matcher required the closing backtick right after the suffix,
        so `path § Section` -- the shape lint-contracts accepts -- was skipped."""
        self.append("CLAUDE.md", "\n- see `_common/NO_SUCH_SECTIONED.md § Rules`\n")
        self.expect_caught("lint-instructions.py", "NO_SUCH_SECTIONED.md", "--severity", "error")

    def test_a_path_into_the_archive_fails(self):
        """I2. A retired skill is on disk but not installed; resolving against it
        turned a dead reference into a passing one."""
        self.edit(
            "CLAUDE.md", "`_common/PROJECT_LOCAL_SKILLS.md`", "`.archive/anvil/SKILL.md`"
        )
        self.expect_caught("lint-instructions.py", ".archive/anvil/SKILL.md", "--severity", "error")

    def test_a_path_into_the_tracked_codex_mirror_passes(self):
        """I2. `.agents/skills/` is the tracked Codex mirror, not an exclusion:
        rejecting it with `.archive/` failed valid links to the mirror."""
        self.edit(
            "CLAUDE.md", "`_common/PROJECT_LOCAL_SKILLS.md`", "`.agents/skills/darwin/SKILL.md`"
        )
        self.expect_clean("lint-instructions.py", "--severity", "error")

    def test_a_count_wrapped_across_a_soft_line_break_still_fails(self):
        """I1. Barring newlines outright let a drifted count escape the check
        through an ordinary line wrap inside one paragraph."""
        self.edit("AGENTS.md", "90 global specialist skill", "91 global specialist\nskill")
        self.expect_caught("lint-instructions.py", "claims 91 skills", "--severity", "error")

    def test_a_hyphenated_count_that_drifts_fails(self):
        """I1. Only whitespace and 個/件/本 could sit between the number and the
        noun, so "a 91-skill corpus" was never read as a claim."""
        self.edit("AGENTS.md", "90 global specialist skill agents", "a 91-skill corpus of agents")
        self.expect_caught("lint-instructions.py", "claims 91 skills", "--severity", "error")

    def test_routing_prose_with_the_tsu_counter_is_not_a_count(self):
        """I1. Counting つ read "1つのスキルで完結する" as a claim of one skill and
        blocked ordinary routing prose."""
        self.append("CLAUDE.md", "\n- 依頼が1つのスキルで完結する場合は直接呼び出す。\n")
        self.expect_clean("lint-instructions.py", "--severity", "error")

    def test_a_list_number_does_not_pair_with_skills_on_the_next_line(self):
        """I1. `\\s*` crossed blank lines and read "step 7" + "Skills" as a claim."""
        self.append("CLAUDE.md", "\n1. step 7\n\nSkills are listed in the catalog.\n")
        self.expect_clean("lint-instructions.py", "--severity", "error")

    def test_a_count_written_noun_first_that_drifts_fails(self):
        """I1. Only number-then-noun was read, so "スキル数は 77" and
        "Skill count: 77" stated a corpus quantity no check re-derived."""
        for claim in ("\nスキル数は 77。\n", "\nSkill count: 77.\n", "\nThe number of skills is 77.\n"):
            with self.subTest(claim=claim):
                self.tearDown()  # restore first: a failed case must not carry over
                self.append("CLAUDE.md", claim)
                self.expect_caught("lint-instructions.py", "claims 77 skills", "--severity", "error")

    def test_a_noun_first_project_local_count_is_scoped(self):
        """I1. The local qualifier before a noun-first claim scopes it as it does
        a number-first one."""
        self.append("CLAUDE.md", "\nproject-local skill count: 3\n")
        self.expect_clean("lint-instructions.py", "--severity", "error")

    def test_a_noun_first_bound_is_a_threshold_not_a_count(self):
        """I1. "スキル数は 7 以下" defines a rule; it does not count the corpus."""
        for rule in ("\nチェーンのスキル数は 7 以下に抑える。\n", "\nKeep the skill count: 7 or fewer per chain.\n",
                     "\nチェーンのスキル数は 7 個以下に抑える。\n", "\nスキル数は 3〜7 が目安。\n", "\nスキル数は 3～7 が目安。\n",
                     "\nKeep the skill count: 7 at most.\n", "\nskill count: max 7\n"):
            with self.subTest(rule=rule):
                self.tearDown()  # restore first: a failed case must not carry over
                self.append("CLAUDE.md", rule)
                self.expect_clean("lint-instructions.py", "--severity", "error")

    def test_a_count_inside_a_fenced_example_is_not_a_claim(self):
        """I1. A fenced block is an example, as I2 already treats it; reading
        its text blocked validate on sample output."""
        self.append("CLAUDE.md", "\n```text\nexample: a 2-skill chain\n```\n")
        self.expect_clean("lint-instructions.py", "--severity", "error")

    def test_a_dead_at_import_in_an_instruction_file_fails(self):
        """I2. CLAUDE.md loads `@path` imports into every session; the backtick-only
        matcher never read them, so a renamed import target passed."""
        self.edit("CLAUDE.md", "@_common/GIT_GUIDELINES.md", "@_common/NO_SUCH_GUIDELINES.md")
        self.expect_caught("lint-instructions.py", "NO_SUCH_GUIDELINES.md", "--severity", "error")

    def test_an_at_word_inside_an_inline_code_span_is_not_an_import(self):
        """I2. A shell example such as `curl -d @file` is code, not a CLAUDE.md
        import; reading it as one blocked validate on a false P1."""
        self.append("CLAUDE.md", "\nUse `curl -d @payload/body.json https://example.invalid` to post.\n")
        self.expect_clean("lint-instructions.py", "--severity", "error")

    def test_an_at_word_inside_a_fenced_code_block_is_not_an_import(self):
        """I2. Claude Code does not load imports from fenced code blocks, so a
        fenced `@path` makes no claim that the file exists."""
        self.append("CLAUDE.md", "\n```text\n@docs/no-such-example.md\n```\n")
        self.expect_clean("lint-instructions.py", "--severity", "error")

    def test_a_dead_import_after_a_code_span_still_fails_on_its_own_line(self):
        """I2. Blanking code must keep offsets: the finding still names the
        dead import, and the code before it does not hide it."""
        self.append(
            "CLAUDE.md",
            "\n```sh\ncurl -d @payload/body.json\n```\n\nSee `x` then @_common/NO_SUCH_IMPORT.md\n",
        )
        self.expect_caught("lint-instructions.py", "NO_SUCH_IMPORT.md", "--severity", "error")

    def test_a_dead_script_path_in_an_instruction_file_fails(self):
        """I2. Only `.md` paths were checked; a moved checker script passed."""
        self.edit("CLAUDE.md", "`_common/scripts/_corpus.py`", "`_common/scripts/_no_such_corpus.py`")
        self.expect_caught("lint-instructions.py", "_no_such_corpus.py", "--severity", "error")


class TestContractDelivery(CheckerCase):
    """`lint-contracts.py`."""

    def test_a_spine_file_missing_from_the_precedence_order_fails(self):
        """CD-1, roster side."""
        self.edit("_common/OPERATIONAL.md", "`VALUES.md` · `BOUNDARIES.md`", "`BOUNDARIES.md`")
        self.expect_caught("lint-contracts.py", "CD-1", "--severity", "error")

    def test_a_spine_tier_declaration_removed_fails(self):
        """CD-1, declaration side. Drift in either direction is a defect, and
        neither statement corrects the other."""
        self.edit(
            "_common/WORK_GATE.md",
            "> **Tier:** `spine`",
            "> **Tier:** `domain`",
        )
        self.expect_caught("lint-contracts.py", "CD-1", "--severity", "error")

    def test_a_spine_contract_reachable_only_indirectly_fails(self):
        """CD-2. Depth 2 means the contract arrives only if the agent opens an
        intermediate document, which is itself conditional."""
        self.edit(
            "zen/SKILL.md",
            "`_common/VALUES.md` · `_common/BOUNDARIES.md`",
            "`_common/BOUNDARIES.md`",
        )
        self.expect_caught("lint-contracts.py", "CD-2", "--severity", "error")

    def test_a_contract_no_skill_reaches_fails(self):
        """CD-3."""
        self.write_new(
            "_common/ORPHAN_FIXTURE.md",
            "# Orphan Fixture\n\n> **Tier:** `domain` — fixture for the checker suite.\n",
        )
        self.expect_caught("lint-contracts.py", "ORPHAN_FIXTURE.md", "--severity", "error")

    def test_a_contract_with_no_declared_tier_fails(self):
        """CD-6. An undeclared tier makes CD-1 unable to see the file at all.
        A spine fixture passed only because CD-1 fired; CD-6 itself was advisory."""
        self.edit(
            "_common/RECIPES.md",
            "> **Tier:** `authoring`",
            "> This file has no tier line.",
        )
        self.expect_caught("lint-contracts.py", "CD-6", "--severity", "error")

    def test_an_unknown_tier_is_not_a_declaration(self):
        """CD-6. Any lowercase word counted as declared, so a misspelt
        `spine` dropped the file out of CD-1 exactly as a missing line did."""
        self.edit("_common/SECURITY.md", "> **Tier:** `domain`", "> **Tier:** `domian`")
        self.expect_caught("lint-contracts.py", "CD-6", "--severity", "error")

    def test_a_gitignored_journal_does_not_deliver_a_contract(self):
        """Regression. `.agents/` is gitignored, so an edge through it made a
        contract look addressed locally while CI -- which has no such file --
        rejected the same commit. Reachability is a property of what ships."""
        self.write_new(
            "_common/ORPHAN_FIXTURE.md",
            "# Orphan Fixture\n\n> **Tier:** `domain` — fixture for the checker suite.\n",
        )
        # The journal is written here rather than borrowed from the working
        # copy. `.agents/` is gitignored, so a checkout has none: a test resting
        # on the developer's own journal passes locally and errors in CI, which
        # is the very asymmetry it exists to catch.
        self.write_new(
            ".agents/JOURNAL_FIXTURE.md",
            "# Journal Fixture\n\nSee `_common/ORPHAN_FIXTURE.md` for the rule.\n",
        )
        self.expect_caught("lint-contracts.py", "ORPHAN_FIXTURE.md", "--severity", "error")

    def test_a_dead_path_with_a_section_suffix_fails(self):
        """CD-5. `reference/x.md §Section` is the corpus's usual pointer shape, but
        the matcher required the whole code span to be a path and skipped it."""
        self.append("zen/SKILL.md", "\nSee `reference/no-such-section-file.md §Intro`.\n")
        self.expect_caught("lint-contracts.py", "no-such-section-file.md", "--severity", "error")

    def test_a_dead_shell_script_reference_fails(self):
        """CD-5. Only md/py/yaml/json references were read, so a moved script
        under `reference/` stayed cited with nothing to run."""
        self.append("gauge/SKILL.md", "\nRun `reference/no-such-runner.sh` first.\n")
        self.expect_caught("lint-contracts.py", "no-such-runner.sh", "--severity", "error")


class TestSkillStructure(CheckerCase):
    """`lint-frontmatter.py`."""

    def test_a_non_spec_frontmatter_key_fails(self):
        """F3. `permissions:` and friends are escalated as supply-chain risk."""
        self.edit("zen/SKILL.md", "name: zen", "name: zen\npermissions: all")
        self.expect_caught("lint-frontmatter.py", "F3", "--severity", "error")

    def test_a_reserved_word_inside_a_name_fails(self):
        """F1. The spec forbids `claude`/`anthropic` anywhere in a name; only a
        leading segment was rejected, so `zen-claude-helper` passed."""
        self.edit("zen/SKILL.md", "name: zen", "name: zen-claude-helper")
        self.expect_caught("lint-frontmatter.py", "reserved word", "--severity", "error")

    def test_an_oversized_body_is_reported(self):
        """S2 is advisory (P3), so it is asserted as *reported*, not blocking.
        Asserting the exit code here would encode the tier, and the tier is a
        judgement that may move."""
        self.append("zen/SKILL.md", "\n" + ("padding sentence for the size check. " * 900))
        self.expect_reported("lint-frontmatter.py", "S2", "--severity", "warning")

    def test_a_lowercase_readme_in_a_skill_folder_fails(self):
        """C2. The check compared names case-sensitively, so `readme.md` passed."""
        self.write_new("zen/readme.md", "# zen\n")
        self.expect_caught("lint-frontmatter.py", "C2", "--severity", "error")


class TestRoutingSurface(CheckerCase):
    """`routing-oracle.py`. Most of these assert the finding is reported; a
    crashed check blocks in error mode, because it verified nothing."""

    def test_a_dead_reference_in_the_nexus_surface_is_reported(self):
        self.edit(
            "nexus/SKILL.md",
            "`reference/routing-matrix.md`",
            "`reference/no-such-routing-file.md`",
        )
        self.expect_reported(
            "routing-oracle.py", "no-such-routing-file.md", "--severity", "error"
        )

    def test_a_ladder_ordered_architect_before_compass_is_reported(self):
        """RO-2. The ladder is compass-first; reversing the two names is a
        routing change that reads as a wording change."""
        self.edit(
            "nexus/reference/routing-matrix.md",
            "Spawn `compass(recommend)` as a hub-spoke step",
            "Spawn `architect` first, then `compass(recommend)`, as a hub-spoke step",
        )
        self.expect_reported("routing-oracle.py", "RO-2", "--severity", "error")

    def test_a_flow_whose_select_survives_only_inside_chain_select_is_reported(self):
        """RO-2. A substring search found `SELECT` inside `CHAIN_SELECT` and
        passed a flow whose SELECT step had been deleted."""
        self.edit(
            "nexus/SKILL.md",
            "`RESOLVE → GATE → MULTI? → REDIRECT? → SELECT → LADDER? → CHAIN_SELECT`",
            "`RESOLVE → GATE → MULTI? → REDIRECT? → CHAIN_SELECT → LADDER?`",
        )
        self.expect_reported("routing-oracle.py", "token `SELECT` missing", "--severity", "error")

    def test_an_unescaped_pipe_inside_a_hint_cell_fails(self):
        """RO-9. `Forge[ui|api|fullstack]` split the FEATURE row into extra
        cells, so its later hints were never checked."""
        self.edit(
            "nexus/reference/routing-matrix.md",
            "Forge[ui\\|api\\|fullstack]",
            "Forge[ui|api|fullstack]",
        )
        self.expect_caught("routing-oracle.py", "FEATURE (6 cells, header has 4)", "--severity", "error")

    def test_a_pipe_after_an_even_backslash_run_still_splits(self):
        """RO-9. `\\\\|` is an escaped backslash followed by a real cell break;
        a single-backslash lookbehind hid it and the row passed as well-formed."""
        self.edit(
            "nexus/reference/routing-matrix.md",
            "Forge[ui\\|api\\|fullstack]",
            "Forge[ui\\\\|api\\\\|fullstack]",
        )
        self.expect_caught("routing-oracle.py", "FEATURE (6 cells, header has 4)", "--severity", "error")

    def test_a_bad_hint_in_a_row_resumed_after_a_blank_line_fails(self):
        """RO-9. Taking the first row after any gap as a header skipped it
        silently; only the row above a separator line is a header."""
        self.edit(
            "nexus/reference/routing-matrix.md",
            "| DESIGN_AUDIT | Pixel[gap] → Canon/Judge |",
            "\n| DESIGN_AUDIT | Pixel[gap-report] → Canon/Judge |",
        )
        self.expect_caught(
            "routing-oracle.py", "Pixel[gap-report]", "--severity", "error"
        )

    def test_a_recipe_hint_naming_an_unknown_subcommand_fails(self):
        """RO-9. `Pixel[gap-report]` read as a hint but Pixel has no such
        Recipe, so dispatch fell back to the code-generating default."""
        self.edit(
            "nexus/reference/routing-matrix.md",
            "| DESIGN_AUDIT | Pixel[gap] → Canon/Judge |",
            "| DESIGN_AUDIT | Pixel[gap-report] → Canon/Judge |",
        )
        self.expect_caught(
            "routing-oracle.py", "Pixel[gap-report]", "--severity", "error"
        )

    def test_a_recipe_hint_found_only_in_a_keyword_table_fails(self):
        """RO-9. `audit` is backticked in Gateway's Signal Keywords table but is
        not a Gateway subcommand; a keyword mention must not pass as one."""
        self.edit(
            "nexus/reference/routing-matrix.md",
            "| API | Gateway → Builder → Radar | Gateway[design],",
            "| API | Gateway → Builder → Radar | Gateway[audit],",
        )
        self.expect_caught(
            "routing-oracle.py", "Gateway[audit]", "--severity", "error"
        )

    def test_a_scope_boundary_pointer_to_a_retired_subcommand_fails(self):
        """RO-10. `**Shift `migrate`**` survived the rename to `plan` in a
        reference file RO-9 never read; Shift would fall back to its default."""
        self.edit(
            "shift/reference/framework-migration.md",
            "**Shift `plan` (default)**",
            "**Shift `migrate` (default)**",
        )
        self.expect_caught(
            "routing-oracle.py", "`migrate` is not a shift subcommand", "--severity", "error"
        )

    def test_a_recipe_mode_in_subcommand_position_fails(self):
        """RO-10. `expert` is a mode of Magi's `advisor`, not a subcommand:
        `Magi[expert]` dispatches on `expert` and falls back."""
        self.edit(
            "magi/SKILL.md",
            "→ Magi[advisor expert] →",
            "→ Magi[expert] →",
        )
        self.expect_caught(
            "routing-oracle.py", "write `Magi[advisor expert]`", "--severity", "error"
        )

    def test_a_trigger_phrase_is_not_read_as_a_mode_declaration(self):
        """RO-10. Judge maps the input phrase `security review` -> security
        focus; that must not make `review` a mode of `security`, or an ordinary
        `Judge[review]` annotation would be rejected."""
        self.append("judge/reference/codex-review-usage.md", "\nSee Judge[review] for the default pass.\n")
        self.expect_clean("routing-oracle.py", "--severity", "error")

    def test_an_invocation_shaped_pointer_to_a_missing_subcommand_fails(self):
        """RO-10. `canon[legal]` read as a Canon invocation at ~22 sites, but
        Canon has no `legal` Recipe; every one fell back to `owasp`."""
        self.edit(
            "_common/GROWTH_BRAND_PROOF.md",
            "| `canon[claims]` + `canon[regulatory]` validators |",
            "| `canon[legal]` + `canon[regulatory]` validators |",
        )
        self.expect_caught(
            "routing-oracle.py", "`legal` is not a canon subcommand", "--severity", "error"
        )

    def test_a_pointer_in_a_nested_reference_directory_fails(self):
        """RO-10. The scan globbed `reference/*.md` only, so pointers one directory
        deeper (`scribe/reference/unified-spec/`) were never read; eight named
        `unified` modes as Scribe subcommands."""
        self.edit(
            "scribe/reference/unified-spec/raci-matrix.md",
            "**scribe `unified raci`**",
            "**scribe `raci`**",
        )
        self.expect_caught(
            "routing-oracle.py", "`raci` is not a scribe subcommand", "--severity", "error"
        )

    def test_a_crashed_check_blocks_in_error_mode(self):
        """A crash was a WARNING, so one undecodable reference file disabled RO-10
        for the whole corpus and `--severity error` still exited 0."""
        path = self._remember("zen/reference/consistency-audit.md")
        path.write_bytes(path.read_bytes() + b"\n\xff\xfe\n")
        self.expect_caught("routing-oracle.py", "check crashed", "--severity", "error")

    def test_a_bad_hint_in_the_additions_column_fails(self):
        """RO-9. Only the Primary Chain and Recipe Hints columns were read; the
        Additions column carries `Skill[token]` hints too."""
        self.edit(
            "nexus/reference/routing-matrix.md",
            "+Flux[reframe] (lateral thinking)",
            "+Flux[refrme] (lateral thinking)",
        )
        self.expect_caught("routing-oracle.py", "Flux[refrme]", "--severity", "error")

    def test_a_handoff_token_naming_no_skill_fails(self):
        """RO-11. The showcase -> vitrine and researcher -> field renames left
        live `X_TO_Y` tokens naming skills that no longer exist; nothing caught it."""
        self.append("zen/reference/agent-integrations.md", "\nEmit `FOO_TO_SHOWCASE_HANDOFF`.\n")
        self.expect_caught("routing-oracle.py", "FOO_TO_SHOWCASE", "--severity", "error")

    def test_a_retired_receiver_from_a_live_sender_fails(self):
        """RO-11. The sender is a live skill; the receiver alone is stale."""
        self.append("zen/SKILL.md", "\n- Zen -> Vitrine: `ZEN_TO_SHOWCASE_HANDOFF`\n")
        self.expect_caught("routing-oracle.py", "ZEN_TO_SHOWCASE", "--severity", "error")

    def test_a_bare_token_with_one_live_endpoint_still_fails(self):
        """RO-11. Without a `_HANDOFF` suffix the token is still handoff-shaped
        when one side names a live skill and the other does not."""
        self.append("zen/SKILL.md", "\n- Zen -> Vitrine: `ZEN_TO_SHOWCASE`\n")
        self.expect_caught("routing-oracle.py", "ZEN_TO_SHOWCASE", "--severity", "error")

    def test_a_bare_token_between_two_retired_names_fails(self):
        """RO-11. Two renames left in one token (`RESEARCHER_TO_SHOWCASE`) name
        no live skill on either side, yet it is the stale handoff RO-11 exists
        for: a retired or renamed endpoint keeps it in scope without a suffix."""
        self.append("zen/SKILL.md", "\n- legacy: `RESEARCHER_TO_SHOWCASE`\n")
        self.expect_caught("routing-oracle.py", "RESEARCHER_TO_SHOWCASE", "--severity", "error")

    def test_a_bare_token_between_two_absorbed_names_fails(self):
        """RO-11. Absorbed skills are recorded only in CHANGELOG prose
        (`shard` → `schema`, `sketch` → `builder`) once their packages leave the
        tree, so the retired set cannot come from `.archive/` alone: routing-oracle
        carries them in its hard-coded `REMOVED_SKILLS` list (transcribed from that history)."""
        self.append("zen/SKILL.md", "\n- legacy: `SHARD_TO_SKETCH`\n")
        self.expect_caught("routing-oracle.py", "SHARD_TO_SKETCH", "--severity", "error")

    def test_a_bare_token_between_names_retired_outside_the_archive_fails(self):
        """RO-11. `dock`/`wield` were absorbed (CHANGELOG prose only), `hex` and
        `sonar` are battery-guarded retirees never archived: still stale names."""
        self.append("zen/SKILL.md", "\n- legacy: `DOCK_TO_WIELD`, `HEX_TO_SONAR`\n")
        self.expect_caught("routing-oracle.py", "DOCK_TO_WIELD", "--severity", "error")
        self.expect_caught("routing-oracle.py", "HEX_TO_SONAR", "--severity", "error")

    def test_a_common_word_beside_one_retired_name_passes(self):
        """RO-11. Retired names that are ordinary words (`snap`, `pipe`, `hex`)
        must not turn `SNAP_TO_GRID` or `HEX_TO_RGB` into handoff errors."""
        self.append("gear/SKILL.md", "\nUse `SNAP_TO_GRID`, `PIPE_TO_FILE` and `HEX_TO_RGB`.\n")
        self.expect_clean("routing-oracle.py", "--severity", "error")

    def test_an_identifier_that_merely_contains_to_passes(self):
        """RO-11. Any UPPER_CASE identifier with `_TO_` was read as a handoff, so
        a config key or metric name in a reference file blocked validate."""
        self.append(
            "gear/SKILL.md",
            "\nSet `PATH_TO_CONFIG`, watch `TIME_TO_FIRST_BYTE` and `MAX_TIME_TO_LIVE`.\n",
        )
        self.expect_clean("routing-oracle.py", "--severity", "error")


class TestNexusReferences(CheckerCase):
    """`routing-oracle.py` RO-1."""

    def test_a_bare_reference_owned_by_another_skill_is_dead(self):
        """RO-1. A bare `reference/X.md` resolved through any skill owning an X.md,
        so a nexus file citing a reference it does not have passed."""
        self.append("nexus/reference/spec-recipe.md",
                    "\nSee `reference/communication-patterns.md`.\n")
        self.expect_caught("routing-oracle.py", "communication-patterns.md", "--severity", "error")

    def test_a_reference_shorthand_after_its_owning_skill_resolves(self):
        """RO-1. "`rally/SKILL.md` (+ `reference/X.md`)" names the owner."""
        self.append("nexus/reference/spec-recipe.md",
                    "\nSee `rally/SKILL.md` (+ `reference/communication-patterns.md`).\n")
        self.expect_clean("routing-oracle.py", "--severity", "error")

    def test_a_common_word_is_not_an_owning_skill(self):
        """RO-1. Skill names such as `chain` are ordinary words, so "Before the
        chain runs, read `reference/X.md`" took chain/ as the owner of X.md."""
        self.append("nexus/reference/spec-recipe.md",
                    "\nBefore the rally starts, read `reference/communication-patterns.md`.\n")
        self.expect_caught("routing-oracle.py", "communication-patterns.md", "--severity", "error")

    def test_a_word_before_a_slash_is_not_an_owning_skill(self):
        """RO-1. "field/value" or "per-field/step" in prose named `field/` as the owner."""
        for prose in ("field/value pair", "per-field/step value"):
            with self.subTest(prose=prose):
                self.tearDown()  # restore first: a failed case must not carry over
                self.append("nexus/reference/spec-recipe.md",
                            f"\nRecord each {prose} per `reference/diary-longitudinal-study.md`.\n")
                self.expect_caught("routing-oracle.py", "diary-longitudinal-study.md",
                                   "--severity", "error")

    def test_a_bare_subcommand_exception_must_itself_route_to_gate(self):
        """RO-6. GATE was searched across the whole section, and the Default
        dispatch flow above the exception always names GATE, so an exception
        that dispatched bare tokens without a question still passed."""
        self.edit("nexus/SKILL.md",
                  "enters CLASSIFY at `GATE` and asks one focused question",
                  "dispatches directly to its Recipe")
        self.expect_caught("routing-oracle.py", "RO-6", "--severity", "error")

    def test_a_bare_subcommand_exception_that_skips_gate_fails(self):
        """RO-6. Any mention of GATE passed, so "skipping `GATE`" did too."""
        self.edit("nexus/SKILL.md",
                  "enters CLASSIFY at `GATE` and asks one focused question",
                  "dispatches directly to its Recipe, skipping `GATE`")
        self.expect_caught("routing-oracle.py", "RO-6", "--severity", "error")

    def test_a_negated_route_to_gate_fails(self):
        """RO-6. Only lowercase "never"/"not" negated the route."""
        for said in ("dispatches directly and doesn't route to `GATE`",
                     "Never enters CLASSIFY at `GATE`; it dispatches directly"):
            with self.subTest(said=said):
                self.tearDown()  # restore first: a failed case must not carry over
                self.edit("nexus/SKILL.md",
                          "enters CLASSIFY at `GATE` and asks one focused question", said)
                self.expect_caught("routing-oracle.py", "RO-6", "--severity", "error")

    def test_a_bare_subcommand_exception_may_continue_in_a_sub_bullet(self):
        """RO-6. A nested list marker ended the item, so the exception's own
        sub-bullet was read as outside it."""
        self.edit("nexus/SKILL.md",
                  "(`/nexus optimize`, `/nexus kaizen`) enters CLASSIFY",
                  "(`/nexus optimize`, `/nexus kaizen`):\n  - enters CLASSIFY")
        self.expect_clean("routing-oracle.py", "--severity", "error")


class TestLessonsRegister(CheckerCase):
    """`lint-lessons.py`. The register's entire value is what it refuses, so
    every refusal is tested; a gate that accepts everything is a filing cabinet."""

    ROW = "\n| L900 | A fixture failure happened once. | `F3` | {mech} | {where} | {added} |\n"

    def add_row(self, mech: str, where: str = "`Makefile`", added: str = "2026-08-21") -> None:
        self.append("_common/LESSONS.md", self.ROW.format(mech=mech, where=where, added=added))

    def test_a_lesson_with_no_mechanism_fails(self):
        self.add_row(mech="")
        self.expect_caught("lint-lessons.py", "LS-1", "--severity", "error")

    def test_a_mechanism_that_reads_as_an_intention_fails(self):
        """The rule the file exists for. 'Be careful' is the disposition that
        failed the first time, rewritten as though it were a control."""
        self.add_row(mech="Be careful to check the count before committing.")
        self.expect_caught("lint-lessons.py", "LS-2", "--severity", "error")

    def test_remember_to_is_rejected_as_a_mechanism(self):
        self.add_row(mech="Remember to re-run the matcher against both files.")
        self.expect_caught("lint-lessons.py", "LS-2", "--severity", "error")

    def test_a_curly_apostrophe_intention_is_rejected(self):
        """LS-2. "Don’t forget" with a typographic apostrophe missed "don't forget"."""
        self.add_row(mech="Don\u2019t forget to re-run the matcher.")
        self.expect_caught("lint-lessons.py", "LS-2", "--severity", "error")

    def test_shouldnt_is_rejected(self):
        """LS-2. Whole-word "should" does not match inside "shouldn't"."""
        self.add_row(mech="Reviewers shouldn't skip the matcher.")
        self.expect_caught("lint-lessons.py", "LS-2", "--severity", "error")

    def test_ought_to_is_rejected(self):
        self.add_row(mech="Reviewers ought to re-run the matcher.")
        self.expect_caught("lint-lessons.py", "LS-2", "--severity", "error")

    def test_the_registers_own_counter_example_is_rejected(self):
        """LS-2. LESSONS.md names "we will be more careful" as the answer that
        is not a mechanism; a literal "be careful" match let it through."""
        self.add_row(mech="We will be more careful when editing counts.")
        self.expect_caught("lint-lessons.py", "LS-2", "--severity", "error")

    def test_a_japanese_should_is_rejected(self):
        """LS-2. Bare English "should" was rejected but べき, its Japanese
        counterpart, was accepted as a mechanism."""
        for mech in ("コミット前にゲートを確認するべき。", "PR では必ず diff を読むべき",
                     "チェッカーを使うべき場面がある。"):
            with self.subTest(mech=mech):
                self.tearDown()  # restore first: a failed case must not carry over
                self.add_row(mech=mech)
                self.expect_caught("lint-lessons.py", "LS-2", "--severity", "error")

    def test_a_verb_ending_in_beki_is_not_should(self):
        """LS-2. 調べきる ("examine exhaustively") contains べき but is not "should"."""
        for mech in ("`lint-lessons.py` が全行を調べきるまで pre-commit が止める。",
                     "`lint-lessons.py` が述べきれない行を pre-commit で止める。"):
            with self.subTest(mech=mech):
                self.tearDown()  # restore first: a failed case must not carry over
                self.add_row(mech=mech)
                self.expect_clean("lint-lessons.py", "--severity", "error")

    def test_a_japanese_intention_is_rejected(self):
        """LS-2. The repository writes Japanese; an English-only phrase list
        accepted the same disposition written in Japanese."""
        self.add_row(mech="件数を忘れずに確認する。")
        self.expect_caught("lint-lessons.py", "LS-2", "--severity", "error")

    def test_a_placeholder_mechanism_fails(self):
        """LS-1. "TBD" is an empty cell with characters in it."""
        self.add_row(mech="TBD")
        self.expect_caught("lint-lessons.py", "LS-1", "--severity", "error")

    def test_a_formatted_placeholder_mechanism_fails(self):
        """LS-1. Only backticks were stripped, so emphasis or a trailing
        period turned a placeholder back into a mechanism."""
        for mech in ("**TBD**", "_TBD_", "TBD.", "*n/a*", "**TBD**.", "`n/a`."):
            with self.subTest(mech=mech):
                self.tearDown()  # restore first: a failed case must not carry over
                self.add_row(mech=mech)
                self.expect_caught("lint-lessons.py", "LS-1", "--severity", "error")

    def test_a_row_without_a_leading_pipe_is_still_checked(self):
        """GFM makes the leading pipe optional; such a row ended the register
        and skipped every rule."""
        self.append(
            "_common/LESSONS.md",
            "\nL902 | Something happened. | `F9` | A check enforces it. | `Makefile` | 2026-08-21 |\n",
        )
        self.expect_caught("lint-lessons.py", "L902", "--severity", "error")

    def test_a_where_with_a_section_pointer_resolves(self):
        """LS-3. `path` § Section names a file; stripping only the outer
        backticks read the pointer as part of the path and blocked validate."""
        self.add_row(mech="A check enforces it.", where="`_common/scripts/test_checkers.py` § I1")
        self.expect_clean("lint-lessons.py", "--severity", "error")

    def test_a_mechanism_living_nowhere_fails(self):
        """A `Where` that stopped resolving means the mechanism was deleted and
        the lesson quietly stopped being kept."""
        self.add_row(mech="A check enforces it.", where="`_common/scripts/no-such-check.py`")
        self.expect_caught("lint-lessons.py", "LS-3", "--severity", "error")

    def test_a_mechanism_living_in_the_archive_fails(self):
        self.add_row(mech="A check enforces it.", where="`.archive/anvil/SKILL.md`")
        self.expect_caught("lint-lessons.py", "LS-3", "--severity", "error")

    def test_an_unknown_failure_class_fails(self):
        self.append(
            "_common/LESSONS.md",
            "\n| L901 | Something happened. | `F9` | A check enforces it. | `Makefile` | 2026-08-21 |\n",
        )
        self.expect_caught("lint-lessons.py", "LS-4", "--severity", "error")

    def test_a_reused_id_fails(self):
        self.append(
            "_common/LESSONS.md",
            "\n| L001 | A different thing happened. | `F3` | A check enforces it. | `Makefile` | 2026-08-21 |\n",
        )
        self.expect_caught("lint-lessons.py", "LS-5", "--severity", "error")

    def test_a_future_date_fails(self):
        self.add_row(mech="A check enforces it.", added="2099-01-01")
        self.expect_caught("lint-lessons.py", "LS-6", "--severity", "error")

    def test_tomorrow_is_not_the_future_across_timezones(self):
        """A JST committer's date is often tomorrow on a UTC runner."""
        tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
        self.add_row(mech="A check enforces it.", added=tomorrow)
        self.expect_clean("lint-lessons.py", "--severity", "error")

    def test_a_quoted_intention_inside_code_is_not_a_false_positive(self):
        """The mechanism describing a check that *rejects* "remember to" must
        not be caught by its own quotation, or the rule cannot describe itself."""
        self.add_row(mech="The linter rejects any mechanism containing `remember to`.")
        self.expect_clean("lint-lessons.py", "--severity", "error")


class TestTaskBattery(CheckerCase):
    """`task-battery-check.py`. Its blocking exit is the only thing `make
    validate` sees, so the exit code is tested, not just the findings."""

    def test_a_routing_needle_removed_from_signal_keywords_fails(self):
        self.edit("nexus/reference/signal-keywords.md",
                  "`refactor`, `clean up`, `code smell` | `refactor`",
                  "`refactor`, `code smell` | `refactor`")
        self.expect_caught("task-battery-check.py", "item 4 (clean up keyword -> refactor)",
                           "--severity", "error")

    def test_a_keyword_moved_to_another_recipes_row_fails(self):
        """Item 8 searched only for `design weaknesses`, so moving it from the
        anneal row to restyle's kept the item passing while classify would
        send the battery's sentence to restyle."""
        self.edit("nexus/reference/signal-keywords.md", "`design weaknesses`, ", "")
        self.edit("nexus/reference/signal-keywords.md",
                  "`redesign the screen`", "`redesign the screen`, `design weaknesses`")
        self.expect_caught("task-battery-check.py", "item 8 (design weaknesses keyword -> anneal)",
                           "--severity", "error")

    def test_a_crashed_check_blocks_in_error_mode(self):
        """Fail-open let an unreadable artifact skip every mechanical item and exit 0."""
        path = self._remember("nexus/reference/signal-keywords.md")
        path.write_bytes(path.read_bytes() + b"\n\xff\xfe\n")
        self.expect_caught("task-battery-check.py", "check crashed", "--severity", "error")

    def test_a_bold_battery_id_is_counted(self):
        """`**66**` was not read as an ID, so an item with no check passed."""
        self.edit("nexus/reference/task-battery.md",
                  "| 35 | **[out-of-coverage]**",
                  "| **66** | \"fixture item\" | Build | `deliver` |\n| 35 | **[out-of-coverage]**")
        self.expect_caught("task-battery-check.py", "items without a check: [66]",
                           "--severity", "error")

    def test_a_non_integer_battery_id_fails(self):
        """`66a` matched nothing and the row was silently uncounted."""
        self.edit("nexus/reference/task-battery.md",
                  "| 35 | **[out-of-coverage]**",
                  "| 66a | \"fixture item\" | Build | `deliver` |\n| 35 | **[out-of-coverage]**")
        self.expect_caught("task-battery-check.py", "unrecognised item ID", "--severity", "error")


class TestProjectLocalMirror(CheckerCase):
    """`lint-project-local.py`. A mirror edited on one side only must block."""

    def test_a_mirror_that_diverges_from_its_canonical_tree_fails(self):
        self.append(".agents/skills/orbit/reference/examples.md", "\nmirror-only drift\n")
        self.expect_caught("lint-project-local.py", "orbit: canonical/mirror trees differ",
                           "--severity", "error")


    def test_a_shell_reference_without_its_shared_symlink_fails(self):
        """PL-3. Only md/py/json/yaml references were read, so a `.sh` under
        `_templates/` passed with no `_templates` symlink beside the skill."""
        ref = "\nRun `_templates/learning-loop-kit/_scripts/check-rendered.sh`.\n"
        self.append(".claude/skills/lore/SKILL.md", ref)
        self.append(".agents/skills/lore/SKILL.md", ref)
        self.expect_caught("lint-project-local.py", "references `_templates/`",
                           "--severity", "error")

    def test_a_directory_or_dot_slash_reference_without_its_symlink_fails(self):
        """PL-3. A reference needed a file extension and no `/` before it, so
        `_templates/learning-loop-kit/` and `./_templates/X.md` passed with no
        `_templates` symlink beside the skill."""
        for ref in ("\nCopy `_templates/learning-loop-kit/` into the target.\n",
                    "\nScaffold from `./_templates/SKILL_TEMPLATE.md`.\n"):
            with self.subTest(ref=ref):
                self.tearDown()  # restore first: a failed case must not carry over
                self.append(".claude/skills/lore/SKILL.md", ref)
                self.append(".agents/skills/lore/SKILL.md", ref)
                self.expect_caught("lint-project-local.py", "references `_templates/`",
                                   "--severity", "error")

    def test_a_directory_reference_through_its_symlink_resolves(self):
        """PL-3. A directory reference resolves as a directory, not a file."""
        ref = "\nThe checkers live in `_common/scripts/`.\n"
        self.append(".claude/skills/lore/SKILL.md", ref)
        self.append(".agents/skills/lore/SKILL.md", ref)
        self.expect_clean("lint-project-local.py", "--severity", "error")


class TestRecipeValidator(CheckerCase):
    """`validate-recipes.py`."""

    def test_a_recipe_named_dash_is_a_row_not_a_separator(self):
        """A first cell of dashes alone marked a separator, so a Recipe named
        `-` was invisible to every rule -- here a second default and `help`."""
        self.edit("scout/SKILL.md",
                  "| Focused Hunt | `bug` | ✓ |",
                  "| - | `help` | ✓ | x | y |\n| Focused Hunt | `bug` | ✓ |")
        self.expect_caught("validate-recipes.py", "R-REC-03", "--severity", "error")

    def test_a_missing_recipes_section_cites_the_requirement_that_owns_it(self):
        """R-REC-05 still called the section RECOMMENDED for Tier 1-2 after
        `_common/RECIPES.md` made it historical: lint-frontmatter ST1 requires it."""
        self.edit("zen/SKILL.md", "## Recipes", "## Recipe Notes")
        with mock.patch.dict(os.environ, {"VERBOSE": "1"}):
            _, out = self.run_checker("validate-recipes.py", "--severity", "error")
        self.assertIn("lint-frontmatter ST1", out)
        self.assertNotIn("RECOMMENDED for Tier 1-2", out)

    def test_a_suffixed_recipes_heading_fails(self):
        """R-REC-05. ST1 is advisory, and a suffixed heading is not `## Recipes`,
        so every Recipe rule was skipped for the skill and validate passed."""
        self.edit("scout/SKILL.md", "## Recipes", "## Recipes (Subcommands)")
        self.expect_caught("validate-recipes.py", "R-REC-05", "--severity", "error")

    def test_a_bold_external_default_declaration_is_still_compared(self):
        """R-REC-01. Only plain `Default Recipe:` was read, so the bold form --
        the style `**Default dispatch:**` uses -- could name any Recipe."""
        self.edit("builder/SKILL.md", "Default Recipe: `fix`.", "**Default Recipe:** `crud`.")
        self.expect_caught("validate-recipes.py", "declaration differs", "--severity", "error")

    def test_a_missing_external_default_declaration_fails(self):
        """R-REC-01. The allowlist is all SKILL.md shows; without the declaration
        the default is visible only one read away."""
        self.edit("builder/SKILL.md", "Default Recipe: `fix`.", "")
        self.expect_caught("validate-recipes.py", "declaration differs", "--severity", "error")


class TestRecipesDirectory(CheckerCase):
    """compass's Recipe directory is generated; a Recipe added without regenerating must fail."""

    def test_a_subcommand_renamed_only_in_skill_md_fails(self):
        self.edit("architect/SKILL.md", "| `create` |", "| `forge-new` |")
        self.expect_caught("generate-recipes-directory.py", "recipes-directory.md is stale", "--check")


class TestIndexSubcommands(CheckerCase):
    """index.html's recipe list is generated; editing either side alone must fail."""

    def test_a_recipe_description_changed_only_in_skill_md_fails(self):
        self.edit("architect/SKILL.md", "New skill generation (from gap analysis through design)",
                  "New skill generation from a gap report")
        self.expect_caught("generate-index-subcommands.py", "SUBCOMMANDS is stale", "--check")

    def test_a_hand_edit_to_the_page_fails(self):
        self.edit("index.html", '{"n":"create","d":"New skill generation (from gap analysis through design)"}',
                  '{"n":"create","d":"Hand-written copy"}')
        self.expect_caught("generate-index-subcommands.py", "SUBCOMMANDS is stale", "--check")

    def test_a_skill_without_a_recipes_section_is_skipped_not_fatal(self):
        """validate-recipes R-REC-05 owns the `## Recipes` requirement. The
        generator must drop such a skill from the page, not abort the run."""
        self.edit("architect/SKILL.md", "## Recipes", "## Recipe Notes")
        self.expect_caught("generate-index-subcommands.py", "SUBCOMMANDS is stale", "--check")

    def test_a_row_without_a_description_cell_fails(self):
        """A short row was dropped from the page with no message, while
        validate-recipes and the Recipe directory still listed it."""
        self.edit("breach/reference/recipes-index.md", "| Purple Team | `purple` |",
                  "| Short Row | `short-row` |\n| Purple Team | `purple` |")
        self.expect_caught("generate-index-subcommands.py", "short-row", "--check")

    def test_a_table_without_a_description_column_fails(self):
        """Falling back to a fixed column published Mode tokens (`FULL`) as descriptions."""
        self.edit("attest/SKILL.md", "| Recipe | Subcommand | Default? | Mode | Behavior | Read First |",
                  "| Recipe | Subcommand | Default? | Mode | Summary | Read First |")
        self.expect_caught("generate-index-subcommands.py", "no 'When to Use' or 'Behavior' column", "--check")


if __name__ == "__main__":
    unittest.main(verbosity=2, argv=[sys.argv[0]] + sys.argv[1:])
