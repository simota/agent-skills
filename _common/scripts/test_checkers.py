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

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = Path("_common/scripts")

#: Excluded from the working copy: `.git` is large and no checker reads it, and
#: `__pycache__` would shadow edited sources. Nothing else is excluded, and that
#: is deliberate -- the first draft dropped `.archive/` on the reasoning that
#: `_corpus.INFRA_DIRS` skips it, and the baseline immediately failed: RO-1
#: resolves a reference by searching the whole tree, archive included. An
#: exclusion that changes what a checker sees makes the suite test a repository
#: nobody has.
IGNORE = shutil.ignore_patterns(".git", "__pycache__", "*.pyc")

#: One shared copy for the whole suite. Each test edits and restores; copying
#: 24MB per test would make the suite slow enough that nobody runs it, which is
#: the same failure this file exists to prevent.
_WORKSPACE: Path | None = None
_TMP: Path | None = None


def setUpModule() -> None:
    global _WORKSPACE, _TMP
    _TMP = Path(tempfile.mkdtemp(prefix="checker-tests-"))
    _WORKSPACE = _TMP / "repo"
    shutil.copytree(REPO_ROOT, _WORKSPACE, ignore=IGNORE, symlinks=True)


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

    def test_a_dead_path_in_an_instruction_file_fails(self):
        self.edit(
            "CLAUDE.md", "`_common/PROJECT_LOCAL_SKILLS.md`", "`_common/NO_SUCH_CONTRACT.md`"
        )
        self.expect_caught("lint-instructions.py", "NO_SUCH_CONTRACT.md", "--severity", "error")


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
        """CD-6. An undeclared tier makes CD-1 unable to see the file at all."""
        self.edit(
            "_common/VALUES.md",
            "> **Tier:** `spine` — in effect on every run.",
            "This file has no tier line.",
        )
        self.expect_caught("lint-contracts.py", "CD-", "--severity", "error")

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


class TestSkillStructure(CheckerCase):
    """`lint-frontmatter.py`."""

    def test_a_non_spec_frontmatter_key_fails(self):
        """F3. `permissions:` and friends are escalated as supply-chain risk."""
        self.edit("zen/SKILL.md", "name: zen", "name: zen\npermissions: all")
        self.expect_caught("lint-frontmatter.py", "F3", "--severity", "error")

    def test_an_oversized_body_is_reported(self):
        """S2 is advisory (P3), so it is asserted as *reported*, not blocking.
        Asserting the exit code here would encode the tier, and the tier is a
        judgement that may move."""
        self.append("zen/SKILL.md", "\n" + ("padding sentence for the size check. " * 900))
        self.expect_reported("lint-frontmatter.py", "S2", "--severity", "warning")


class TestRoutingSurface(CheckerCase):
    """`routing-oracle.py`. Fail-open by design, so these assert the finding is
    reported; a bug in the oracle must not block an unrelated change."""

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

    def test_a_mechanism_living_nowhere_fails(self):
        """A `Where` that stopped resolving means the mechanism was deleted and
        the lesson quietly stopped being kept."""
        self.add_row(mech="A check enforces it.", where="`_common/scripts/no-such-check.py`")
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

    def test_a_quoted_intention_inside_code_is_not_a_false_positive(self):
        """The mechanism describing a check that *rejects* "remember to" must
        not be caught by its own quotation, or the rule cannot describe itself."""
        self.add_row(mech="The linter rejects any mechanism containing `remember to`.")
        self.expect_clean("lint-lessons.py", "--severity", "error")


if __name__ == "__main__":
    unittest.main(verbosity=2, argv=[sys.argv[0]] + sys.argv[1:])
