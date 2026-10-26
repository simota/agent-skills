#!/usr/bin/env python3
"""
Routing Oracle — mechanical reliability checks for Nexus's routing machinery.

Eleven checks. A check that crashes is recorded as an ERROR and the remaining
checks still run; a crashed check verified nothing, so error and strict modes
block on it (mirrors task-battery-check.py's crash contract):

  RO-1 Dead-reference check
       Every `reference/*.md` / `_common/*.md` path cited inside nexus/SKILL.md
       and nexus/reference/*.md must exist on disk. Catches a renamed/deleted
       file left dangling in prose (e.g. the routing-quick-start.md retirement).

  RO-2 Default-dispatch token-order assertion
       nexus/SKILL.md's explicit `phase:CLASSIFY` Default dispatch must contain
       REDIRECT before SELECT before LADDER (in that relative order), and
       nexus/reference/routing-matrix.md's LADDER clause must mention
       `compass` before `architect` (the ladder is compass-first,
       architect-second, never the reverse).

  RO-3 Producer != verifier check
       In nexus/reference/routing-matrix.md's Primary Chain / Recipe Hints
       columns, whenever a step is annotated `[...verify...]`, the agent
       name immediately before it in the same chain must differ from the
       verifying agent's name — a step cannot self-verify its own output.

  RO-4 Fallback-taken field presence
       nexus/reference/output-formats.md's NEXUS_COMPLETE template must
       contain a `Fallback:` line naming the `fallback_taken` field, and
       that line must enumerate all three enum values (compass-invoked,
       architect-invoked, neither) — catches the LADDER outcome silently
       going unreported in the final handoff.

  RO-5 Roster completeness
       Every skill directory under the repo root (a directory containing
       a SKILL.md, excluding names starting with `_` or `.`) must appear
       (case-insensitive, word-boundary substring match) in at least one
       of nexus/reference/routing-matrix.md or
       nexus/reference/signal-keywords.md. Catches a live skill that has
       no routing surface at all — the mirror image of RO-1's dead
       reference (a routing mention with no skill behind it).

  RO-6 Bare-subcommand dispatch consistency
       nexus/SKILL.md's Subcommand Dispatch says a first-token match
       skips CLASSIFY. But nexus/reference/task-battery.md carries
       fixtures asserting that certain *bare* subcommands (a Recipe name
       with no object/target) must NOT dispatch silently and must instead
       reach GATE for one clarifying question. Those two rules contradict
       unless Subcommand Dispatch declares a bare-subcommand exception.
       This check asserts (a) the exception clause exists whenever such a
       fixture exists, and (b) no token named by a fixture is also listed
       as exempt from the exception. Found live: `optimize` is both a
       registered subcommand and a battery fixture requiring a GATE.

  RO-7 Retired-reference residue
       Reference files removed during Nexus scope consolidation must stay
       absent, and no Nexus document may cite their retired filenames. The
       owning contracts are routing-matrix, handoff-validation,
       intent-clarification, orchestration-patterns, and apex-recipe.

  RO-8 Confidence-gate shape
       confidence-scoring.md must retain typed blocking unknowns and discrete
       evidence bands, and must not reintroduce the retired source-weight
       arithmetic or fixed clarification bonuses.

  RO-9 Recipe-hint subcommand existence
       In every routing-matrix.md column after Task Type (Primary Chain,
       Recipe Hints, Additions), every
       single-token hint `Skill[token]` naming a live skill must name a token
       that skill actually dispatches (its `## Recipes` allowlist / table, or
       an alias declared on an `alias` line of that section). `_common/RECIPES.md` defines the
       hint as the exact Subcommand token, and a token the skill does not
       know silently falls back to its default Recipe (found live:
       `Pixel[gap-report]` ran Pixel's code-generating `reproduce`).
       Descriptive annotations (`Scout[RCA+defect-confirm]`,
       `Radar[safety-net characterization]`) are not single tokens and are
       not checked.

  RO-10 Corpus-wide subcommand references
       RO-9's rule, applied outside the routing matrix, but only to the two
       forms that are unambiguous across the whole corpus (every SKILL.md and
       reference/**/*.md of a live skill, nested directories included but not
       through symlinks, plus _common/*.md; fenced examples and CHANGELOG.md
       excluded):
         (a) a bold lead-in `**Skill `token`**` / `**Skill `token mode`**`
             — the Scope Boundary convention, where the backticked first token
             names the skill's Recipe. Found live: `**Shift `migrate`**`,
             `**Siege `mutate`**`, `**echo `request`**` (a `demand` mode
             written in subcommand position), `**Oracle `eval`**`.
         (b) `Skill[mode]` where `mode` is not a subcommand but is declared in
             that skill's SKILL.md as the second token of one (`advisor
             expert`). Found live: `Magi[expert]`, `Magi[office-hours]` —
             the dispatch reads `expert` as the first token and falls back.
         (c) a code span holding exactly a lower-case `skill[token]` — the
             invocation-shaped spelling, which the corpus uses only for real
             subcommands. Found live: `canon[legal]` (~22 sites; Canon has no
             `legal` Recipe, so each fell back to `owasp`) and
             `magi[arbitrate-tri-engine]`.
       Bare bracket forms in prose (`Atlas[architecture]`, `Builder[codex]`,
       `Nexus[classify]`) are role / engine / phase annotations outside the
       routing matrix and are deliberately not checked here: nothing in their
       spelling separates them from a mistyped subcommand.
       Complexity Budget (`_common/HARNESS_DEBT.md` 3b):
         failure  — a cross-skill pointer names a subcommand the target does
                    not dispatch, so following it silently runs the default
                    Recipe; RO-9 only covered routing-matrix.md
         effect   — the two forms above cannot drift. Does NOT check free
                    `Skill[token]` annotations or plain-prose mentions
         owner    — gauge (it owns the checker suite)
         removal  — delete when skill pointers become structured data resolved
                    at load time instead of prose, or fold into RO-9 when the
                    corpus adopts one hint notation everywhere

  RO-11 Handoff-token endpoints
       Every `SENDER[_MODE...]_TO_RECEIVER` token in an owned or project-local
       SKILL.md or reference/**/*.md (fenced examples included -- templates
       are what agents emit) must name a live skill as its sender (first
       segment) and receiver (first segment after `_TO_`). Also accepted: a
       pseudo-endpoint in HANDOFF_PSEUDO_ENDPOINTS, a Recipe token of the
       skill that owns the file (an intra-skill transition such as
       `MAGI_SIMULATE_TO_DECIDE`), and the reviewed legacy aliases in
       HANDOFF_TOKEN_ALLOWLIST, each pinned to the files that document it.
       Only handoff-shaped tokens are read: one carrying a `_HANDOFF` segment
       after the receiver, or one with exactly one known endpoint. An
       identifier naming no endpoint at all (`PATH_TO_CONFIG`,
       `TIME_TO_FIRST_BYTE`) is a config key or metric, not a handoff.
       Found live: the showcase -> vitrine and researcher -> field renames
       left live tokens naming skills that no longer exist.
       Complexity Budget (`_common/HARNESS_DEBT.md` 3b):
         failure  — F3: a skill rename that never reaches the `X_TO_Y` tokens,
                    so the sender emits a handoff no receiver matches
         effect   — a token naming a retired or misspelled skill cannot land.
                    Does NOT check that sender and receiver both document the
                    same token, or the payload fields
         owner    — gauge (it owns the checker suite)
         removal  — delete when handoffs are declared as structured data whose
                    endpoints are resolved at load time instead of prose tokens

Usage:
  python3 _common/scripts/routing-oracle.py [--severity warning|error|strict]

Severity tiers (mirrors lint-frontmatter.py / validate-recipes.py):
  --severity warning  (default)  print findings, exit 0
  --severity error    exit 1 if any ERROR-level finding is reported
  --severity strict   exit 1 if any finding (ERROR or WARNING) is reported

Crash contract: any unhandled exception during a check is caught, printed as a
single ERROR line with its traceback on stderr, and the remaining checks still
run. It blocks under --severity error and strict, so incomplete verification
never appears clean; --severity warning still exits 0.

Exit codes:
  0  no blocking findings under the chosen severity
  1  blocking findings present
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import traceback
from pathlib import Path

import _corpus
from _markdown import fenced_blocks, markdown_section as read_markdown_section, without_fenced_examples
from _recipes import active_text, dispatch_allowlist, recipe_cells

REPO_ROOT = Path(__file__).resolve().parents[2]
NEXUS_DIR = REPO_ROOT / "nexus"
NEXUS_SKILL = NEXUS_DIR / "SKILL.md"
ROUTING_MATRIX = NEXUS_DIR / "reference" / "routing-matrix.md"
OUTPUT_FORMATS = NEXUS_DIR / "reference" / "output-formats.md"
CONFIDENCE_SCORING = NEXUS_DIR / "reference" / "confidence-scoring.md"

RETIRED_NEXUS_REFERENCES = (
    "agent-communication-anti-patterns.md",
    "apex-walkthrough.md",
    "managed-agents-mapping.md",
    "official-skill-categories.md",
    "orchestration-anti-patterns.md",
    "production-reliability-anti-patterns.md",
    "routing-explanation.md",
    "task-routing-anti-patterns.md",
)

# Matches backticked or plain repo-relative paths under reference/ or _common/
# ending .md. Skill references may use either the global `<skill-name>/` form
# or the canonical project-local `.claude/skills/<skill-name>/` form.
REF_PATH_RE = re.compile(
    r"`?((?:(?:\.(?:claude|agents)/skills/)?[a-z][a-z0-9_-]*/)?"
    r"(?:reference|_common)/[A-Za-z0-9_\-{}/.,]+?\.md)`?"
)


class Finding:
    def __init__(self, check: str, level: str, message: str):
        self.check = check
        self.level = level  # ERROR | WARNING
        self.message = message

    def __str__(self) -> str:
        return f"[{self.level}] {self.check}: {self.message}"


def safe_check(fn, findings: list[Finding]):
    """Run a check function; on any exception, record an ERROR, never raise."""
    try:
        fn(findings)
    except Exception as e:  # noqa: BLE001 - intentional catch-all, see crash contract
        findings.append(Finding(
            fn.__name__, "ERROR",
            f"check crashed and was skipped: {e.__class__.__name__}: {e}",
        ))
        traceback.print_exc(file=sys.stderr)


def _resolve_ref(raw_path: str, referencing_file: Path) -> Path:
    """Resolve a cited path to an absolute file.
    - `_common/X.md` and `<skill>/reference/X.md` (leading skill-name segment present)
      are always repo-root-relative.
    - Bare `reference/X.md` (no leading skill-name segment) is relative to the skill
      folder containing the referencing file (e.g. cited from within nexus/ itself)."""
    if raw_path.startswith("_common/") or not raw_path.startswith("reference/"):
        return REPO_ROOT / raw_path
    skill_dir = referencing_file.parent if referencing_file.parent.name != "reference" else referencing_file.parent.parent
    return skill_dir / raw_path


def check_dead_references(findings: list[Finding]):
    """RO-1: every reference/*.md or _common/*.md path cited in nexus/ docs must exist."""
    files_to_scan = [NEXUS_SKILL] + sorted((NEXUS_DIR / "reference").glob("*.md"))
    checked = 0
    for f in files_to_scan:
        if not f.is_file():
            continue
        content = f.read_text(encoding="utf-8")
        for m in REF_PATH_RE.finditer(content):
            raw_path = m.group(1)
            # Skip glob/brace patterns used as shorthand for "several files"
            # (e.g. `reference/{a,b,c}-recipe.md`) — not a single resolvable path.
            if "{" in raw_path or "}" in raw_path:
                continue
            checked += 1
            candidate = _resolve_ref(raw_path, f)
            if candidate.is_file():
                continue
            # Fallback: some prose uses an implicit-prefix shorthand — e.g.
            # "`architect/SKILL.md` (+ `reference/agent-categories.md`, ...)"
            # means the reference/ file belongs to the just-named architect/ skill,
            # not to the citing file's own skill dir. Before flagging a true
            # dead link, check whether exactly one same-named file exists
            # anywhere else in the repo under a reference/ dir, owned by a skill
            # the citing line names as a code-span path (`rally/...`, `<...-orbit-skill-root>/`)
            # -- any owner would let a nexus file cite a reference it lost because
            # some other skill has one by that name, and a bare word would let
            # names like `chain` or `stage` in ordinary prose stand in as owners.
            basename = Path(raw_path).name
            # Archived and gitignored trees do not count as "resolvable elsewhere".
            # A retired skill under `.archive/` is not installed and not loadable, so
            # a reference that resolves only there is dead in every way that matters
            # -- and resolving it made two genuinely broken links read as live.
            line_end = content.find("\n", m.end())
            line = content[content.rfind("\n", 0, m.start()) + 1 : None if line_end < 0 else line_end]
            elsewhere = [
                p for p in REPO_ROOT.rglob(f"reference/{basename}")
                if p.is_file() and not _corpus.is_excluded_path(p, REPO_ROOT)
                and re.search(rf"(?<=`){re.escape(p.parent.parent.name)}/"
                              rf"|-{re.escape(p.parent.parent.name)}-skill-root>/", line)
            ] if raw_path.startswith("reference/") else []
            if len(elsewhere) == 1:
                continue  # shorthand cross-skill reference, resolvable elsewhere — not dead
            findings.append(Finding(
                "RO-1", "ERROR",
                f"{f.relative_to(REPO_ROOT)} references `{raw_path}` — file not found "
                f"(resolved to {candidate.relative_to(REPO_ROOT)}"
                + (f"; {len(elsewhere)} same-named files exist elsewhere, ambiguous" if elsewhere else "")
                + ")",
            ))
    if checked == 0:
        findings.append(Finding("RO-1", "WARNING", "no reference/_common paths found to check — regex may be stale"))


def check_ladder_token_order(findings: list[Finding]):
    """RO-2: REDIRECT before SELECT before LADDER in the CLASSIFY Default dispatch;
    compass before architect in the LADDER clause."""
    skill_content = active_text(NEXUS_SKILL.read_text(encoding="utf-8"))
    m = re.search(
        r"\*\*Default dispatch:\*\*\s*`phase:CLASSIFY`\s+with flow\s+(`[^`]+`)",
        skill_content,
    )
    if not m:
        findings.append(Finding(
            "RO-2", "ERROR",
            "explicit `phase:CLASSIFY` Default dispatch with a flow was not found in nexus/SKILL.md",
        ))
        return
    chain_template = m.group(1)
    tokens = ["REDIRECT", "SELECT", "LADDER"]
    positions = []
    for t in tokens:
        # Whole-token match: a bare find("SELECT") also hits CHAIN_SELECT.
        m = re.search(rf"(?<![A-Z_]){t}(?![A-Z_])", chain_template)
        idx = m.start() if m else -1
        if idx == -1:
            findings.append(Finding("RO-2", "ERROR", f"token `{t}` missing from CLASSIFY Default dispatch flow: {chain_template}"))
            return
        positions.append(idx)
    if positions != sorted(positions):
        findings.append(Finding("RO-2", "ERROR", f"token order violated in Chain Template (expected REDIRECT < SELECT < LADDER): {chain_template}"))

    if not ROUTING_MATRIX.is_file():
        findings.append(Finding("RO-2", "WARNING", "routing-matrix.md not found — compass/architect order check skipped"))
        return
    matrix_content = active_text(ROUTING_MATRIX.read_text(encoding="utf-8"))
    ladder_match = re.search(r"\*\*LADDER \(no task-type match.*?\*\*\s*—\s*(.*?)(?:\n- \*\*Multi-domain|\n\n)", matrix_content, re.DOTALL)
    if not ladder_match:
        findings.append(Finding("RO-2", "WARNING", "LADDER clause not found in routing-matrix.md — compass/architect order check skipped"))
        return
    ladder_text = ladder_match.group(1)
    compass_idx = ladder_text.find("compass")
    architect_idx = ladder_text.find("architect")
    if compass_idx == -1 or architect_idx == -1:
        findings.append(Finding("RO-2", "ERROR", "LADDER clause must mention both `compass` and `architect`"))
        return
    if not (compass_idx < architect_idx):
        findings.append(Finding("RO-2", "ERROR", "LADDER clause must invoke compass before architect (compass-first, architect-second)"))


# RO-3 reviewed exceptions: (Recipe name, agent) pairs where a same-agent
# verify step was reviewed and accepted as an intentional self-contained
# continuous-measurement loop, not a producer grading its own correctness
# claim without independent review. Keep this list short and each entry
# reviewed — it downgrades the finding's message, not its WARNING severity.
RO3_REVIEWED_EXCEPTIONS = {
    # Pixel re-measures its own fidelity gap after remediation (gap -> verify
    # is the same specialist re-running its own audit instrument, matching
    # DESIGN_AUDIT's documented gap -> remediation -> re-audit loop).
    ("DESIGN_AUDIT", "Pixel"),
}


def _split_cells(line: str) -> list[str]:
    """Split a table row on unescaped pipes.

    A pipe is escaped only by an odd run of backslashes: in `a\\\\|b` the
    first backslash escapes the second, so the pipe still separates cells.
    """
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    cells, current, backslashes = [], [], 0
    for char in body:
        if char == "|" and backslashes % 2 == 0:
            cells.append("".join(current))
            current = []
        else:
            current.append(char)
        backslashes = backslashes + 1 if char == "\\" else 0
    if "".join(current).strip():
        cells.append("".join(current))
    return cells


def _matrix_rows(content: str, malformed: list[str] | None = None):
    """Yield body-row cells of every routing-matrix table, honoring `\\|` escapes.

    A plain `split("|")` let `Forge[ui|api|fullstack]` push a row's later hints
    into columns no check reads. Rows whose width differs from their header are
    appended to `malformed` (when given) as well as yielded.
    """
    separator = re.compile(r"\|?[\s:|-]+\|?")
    lines = content.splitlines()
    header_width = None
    for index, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        if separator.fullmatch(line.strip()) and "-" in line:
            continue
        cells = [c.strip() for c in _split_cells(line)]
        following = lines[index + 1].strip() if index + 1 < len(lines) else ""
        if separator.fullmatch(following) and "-" in following:
            # A header is the row directly above a separator line; a row resumed
            # after a blank line or masked comment keeps the previous header.
            header_width = len(cells)
            continue
        if malformed is not None and header_width is not None and len(cells) != header_width:
            malformed.append(f"{cells[0]} ({len(cells)} cells, header has {header_width})")
        yield cells


def _chain_steps(chain: str) -> list[tuple[set[str], str]]:
    """Split a chain cell into steps: (agent names, annotation) per element.

    Elements are separated by `→` or `,` outside brackets and parentheses, so an
    unannotated step (`Builder → Builder[verify]`) still occupies its position and
    an unannotated step between two others breaks their adjacency. Alternatives
    (`Probe/Radar`, `(Bolt ‖ Zen)`) give a step several names.
    """
    elements, current, depth = [], [], 0
    for char in chain:
        if char in "([":
            depth += 1
        elif char in ")]":
            depth = max(depth - 1, 0)
        if depth == 0 and char in "→,":
            elements.append("".join(current))
            current = []
        else:
            current.append(char)
    elements.append("".join(current))
    steps = []
    for element in elements:
        annotations = re.findall(r"\[([^\]]*)\]", element)
        names = set(re.findall(r"\b[A-Z][A-Za-z0-9]*\b", re.sub(r"\[[^\]]*\]", " ", element)))
        if names:
            steps.append((names, " ".join(annotations)))
    return steps


def check_producer_verifier(findings: list[Finding]):
    """RO-3: in a chain's Primary Chain or Recipe Hints column, the step immediately
    preceding a `[...verify...]`-annotated step must not be the same agent as the verifier."""
    if not ROUTING_MATRIX.is_file():
        findings.append(Finding("RO-3", "WARNING", "routing-matrix.md not found — producer/verifier check skipped"))
        return
    content = active_text(ROUTING_MATRIX.read_text(encoding="utf-8"))
    rows_checked = 0
    for cells in _matrix_rows(content):
        if len(cells) < 3:
            continue
        for column, chain in (("Primary Chain", cells[1]), ("Recipe Hints", cells[2])):
            steps = _chain_steps(chain)
            if column == "Recipe Hints" and "[" in chain and steps:
                rows_checked += 1
            for i, (agents, annotation) in enumerate(steps):
                if "verify" not in annotation.lower() or i == 0:
                    continue  # no verify step, or nothing before it in this list
                for agent in sorted(agents & steps[i - 1][0]):
                    # WARNING not ERROR: a same-agent verify step can be a legitimate
                    # self-contained continuous-measurement loop rather than a
                    # producer grading its own correctness claim. Surface for
                    # human review; don't hard-block on a pattern this heuristic
                    # can't structurally distinguish from an intentional design.
                    if (cells[0], agent) in RO3_REVIEWED_EXCEPTIONS:
                        findings.append(Finding(
                            "RO-3", "WARNING",
                            f"{cells[0]}: same-agent verify — `{agent}` immediately precedes its own "
                            f"`{agent}[{annotation}]` verify step in {column}: {chain} "
                            f"(reviewed exception — accepted self-measurement loop, see RO3_REVIEWED_EXCEPTIONS)",
                        ))
                    else:
                        findings.append(Finding(
                            "RO-3", "WARNING",
                            f"{cells[0]}: same-agent verify — `{agent}` immediately precedes its own "
                            f"`{agent}[{annotation}]` verify step in {column}: {chain} "
                            f"(review: is this a self-contained measurement loop, or a missing independent verifier?)",
                        ))
    if rows_checked == 0:
        findings.append(Finding("RO-3", "WARNING", "no bracket-annotated Recipe Hints rows found — producer/verifier check may be stale vs table format"))


def markdown_section(content: str, title: str) -> str | None:
    """Read one level-two section without treating examples or comments as headings."""
    return read_markdown_section(content, title, allow_suffix=True)


def check_fallback_field(findings: list[Finding]):
    """RO-4: the NEXUS_COMPLETE template in output-formats.md must carry a
    `Fallback:` line naming the `fallback_taken` field with all three enum
    values, so the LADDER outcome (compass-invoked / architect-invoked /
    neither) can never go silently unreported in the final handoff."""
    if not OUTPUT_FORMATS.is_file():
        findings.append(Finding("RO-4", "WARNING", "output-formats.md not found — fallback-field check skipped"))
        return
    content = OUTPUT_FORMATS.read_text(encoding="utf-8")
    section = markdown_section(content, "NEXUS_COMPLETE")
    template = next(fenced_blocks(section), None) if section is not None else None
    if template is None:
        findings.append(Finding("RO-4", "WARNING", "NEXUS_COMPLETE template block not found — fallback-field check skipped"))
        return
    fallback = re.search(r"^\s*Fallback:[^\n]*", template, re.MULTILINE)
    if fallback is None or "fallback_taken" not in fallback.group(0):
        findings.append(Finding("RO-4", "ERROR", "NEXUS_COMPLETE template is missing the `Fallback:` / `fallback_taken` field"))
        return
    required_values = ("compass-invoked", "architect-invoked", "neither")
    missing = [v for v in required_values if v not in fallback.group(0)]
    if missing:
        findings.append(Finding(
            "RO-4", "ERROR",
            f"NEXUS_COMPLETE template's Fallback field is missing enum value(s): {', '.join(missing)}",
        ))


def check_roster_completeness(findings: list[Finding]):
    """RO-5: every skill directory (contains SKILL.md, name not starting with
    `_` or `.`) must appear, case-insensitive word-boundary substring, in at
    least one of routing-matrix.md or signal-keywords.md — the mirror image
    of RO-1's dead-reference check (a live skill with no routing surface)."""
    signal_keywords = NEXUS_DIR / "reference" / "signal-keywords.md"
    if not ROUTING_MATRIX.is_file() or not signal_keywords.is_file():
        findings.append(Finding("RO-5", "WARNING", "routing-matrix.md or signal-keywords.md not found — roster completeness check skipped"))
        return
    combined_text = active_text(ROUTING_MATRIX.read_text(encoding="utf-8")) + "\n" \
        + active_text(signal_keywords.read_text(encoding="utf-8"))

    skill_dirs = sorted(
        d.name for d in _corpus.iter_skill_dirs(REPO_ROOT)
    )
    if not skill_dirs:
        findings.append(Finding("RO-5", "WARNING", "no skill directories with SKILL.md found — roster completeness check may be stale vs repo layout"))
        return

    orphans = []
    for name in skill_dirs:
        pattern = re.compile(r"\b" + re.escape(name) + r"\b", re.IGNORECASE)
        if not pattern.search(combined_text):
            orphans.append(name)

    if orphans:
        findings.append(Finding(
            "RO-5", "WARNING",
            f"{len(orphans)} skill(s) with no routing surface in routing-matrix.md or signal-keywords.md: {', '.join(orphans)}",
        ))


def check_bare_subcommand_dispatch(findings: list[Finding]):
    """RO-6: task-battery fixtures of the form `bare "<token>"` assert that a
    bare Recipe subcommand must reach GATE instead of dispatching silently.
    SKILL.md's Subcommand Dispatch must therefore carry a bare-subcommand
    exception, and must not list any such token as exempt from it."""
    battery = NEXUS_DIR / "reference" / "task-battery.md"
    if not NEXUS_SKILL.is_file() or not battery.is_file():
        findings.append(Finding("RO-6", "WARNING", "nexus/SKILL.md or task-battery.md not found — bare-subcommand check skipped"))
        return

    skill_text = NEXUS_SKILL.read_text(encoding="utf-8")

    # The dispatch allowlist is the fenced block inside the Recipe Registry section.
    recipes = read_markdown_section(skill_text, "Recipes")
    registry = dispatch_allowlist(recipes) if recipes is not None else None
    if registry is None:
        findings.append(Finding("RO-6", "WARNING", "Recipe Registry allowlist block not found in nexus/SKILL.md — bare-subcommand check skipped"))
        return
    subcommands = set(registry)

    # Fixtures written as: bare "optimize" / bare "landing page"
    fixtures = {m.lower() for m in re.findall(r'bare\s+"([^"]+)"',
                                             active_text(battery.read_text(encoding="utf-8")))}
    contested = sorted(f for f in fixtures if f in subcommands)
    if not contested:
        return  # no fixture asserts a bare subcommand must not dispatch — nothing to enforce

    section = markdown_section(skill_text, "Subcommand Dispatch")
    if section is None:
        findings.append(Finding("RO-6", "WARNING", "`## Subcommand Dispatch` section not found in nexus/SKILL.md — bare-subcommand check skipped"))
        return
    section = active_text(section)
    # Require the exception's DEFINITION (a bolded bullet lead-in), not merely a
    # cross-reference to it — a surviving "see the bare-subcommand exception below"
    # must not satisfy the check after the defining bullet has been deleted.
    defined = re.search(r"\*\*Bare-subcommand exception[.:]?\*\*", section)
    # GATE must be the exception's own destination: the Default dispatch flow above
    # it always names GATE, so a section-wide search passed an exception that
    # dispatched bare tokens without asking, and a bare mention passed "skipping
    # GATE". The item ends at a list item no deeper than its own, a heading, table,
    # fence or blank line; its own sub-bullets belong to it.
    item = ""
    if defined:
        line_start = section.rfind("\n", 0, defined.start()) + 1
        indent = len(section[line_start:]) - len(section[line_start:].lstrip(" \t"))
        item = re.match(
            rf".*?(?=\n[ \t]{{0,{indent}}}(?:[-*+][ \t]|\d+[.)][ \t])|\n[ \t]*(?:#|\||```|~~~|\n)|\Z)",
            section[defined.end():], re.S).group()
    routes_to_gate = re.search(
        r"(?<!never )(?<!not )(?<!n't )(?<!no )\b(?:enters?\s+CLASSIFY\s+at|reach(?:es)?|routes?\s+to)"
        r"\s+`?GATE\b", item, re.I)
    if not (defined and routes_to_gate):
        findings.append(Finding(
            "RO-6", "ERROR",
            "Subcommand Dispatch skips CLASSIFY on a first-token match, but task-battery.md requires "
            f"bare {', '.join('`' + c + '`' for c in contested)} to reach GATE instead of dispatching silently. "
            "Subcommand Dispatch must define a **Bare-subcommand exception** routing them to GATE, "
            "or the fixture(s) must be retired.",
        ))
        return

    # The exception's own exempt list must not re-admit a contested token. The list
    # ends at its sentence end -- any period before whitespace -- except where the
    # period closes an abbreviation ("i.e.", "e.g.", "cf.", "vs.", "etc.") that the
    # sentence runs on past; such an abbreviation still ends it before a capital, bold
    # or not. It also ends with its list item, so a line wrap does not cut it short.
    abbreviations = (r"\bi\.e", r"\be\.g", r"\bcf", r"\bvs", r"\betc")  # each fixed-width
    not_after = "".join(f"(?<!{a})" for a in abbreviations)
    after = "|".join(f"(?<={a})" for a in abbreviations)
    exempt_clause = re.search(
        r"\*\*Exempt(?::\*\*|\*\*[^.\n]*?:)\s*(.+?)"
        rf"(?:{not_after}\.(?=\s)|(?:{after})\.(?=\s+[*_~\[(]*[A-Z])"
        r"|\.?[ \t]*(?=\n[ \t]*(?:[-*+][ \t]|\d+[.)][ \t]|#|\||```|~~~|\n)|\Z))",
        section, re.S)
    if exempt_clause:
        exempt = {t.lower() for t in re.findall(r"`([a-z][a-z0-9-]*)`", exempt_clause.group(1))}
        clashes = sorted(exempt & set(contested))
        if clashes:
            findings.append(Finding(
                "RO-6", "ERROR",
                f"bare-subcommand exception lists {', '.join('`' + c + '`' for c in clashes)} as exempt, "
                "but task-battery.md has a fixture requiring the same token to reach GATE — contradiction.",
            ))


def check_retired_reference_residue(findings: list[Finding]):
    """RO-7: consolidated Nexus references must not be recreated or cited."""
    reference_dir = NEXUS_DIR / "reference"
    files_to_scan = [NEXUS_SKILL] + sorted(reference_dir.glob("*.md"))
    residue: list[str] = []

    for name in RETIRED_NEXUS_REFERENCES:
        if (reference_dir / name).exists():
            residue.append(f"retired file exists: nexus/reference/{name}")
        for path in files_to_scan:
            if path.name == name:
                continue
            if name in path.read_text(encoding="utf-8"):
                residue.append(f"{path.relative_to(REPO_ROOT)} cites retired `{name}`")

    if residue:
        findings.append(Finding("RO-7", "ERROR", "; ".join(residue)))


def check_confidence_gate_shape(findings: list[Finding]):
    """RO-8: confidence stays typed/discrete instead of pseudo-precise."""
    if not CONFIDENCE_SCORING.is_file():
        findings.append(Finding("RO-8", "ERROR", "nexus/reference/confidence-scoring.md is missing"))
        return

    text = active_text(CONFIDENCE_SCORING.read_text(encoding="utf-8"))
    required = ("## Blocking Unknown Gate", "## Discrete Evidence Bands", "`authority`")
    missing = [token for token in required if token not in text]
    retired_patterns = {
        "source-weight formula": r"git_score\s*[×*]\s*0\.30",
        "fixed clarification bonus": r"(?:boost|bonus)[^\n]*\+0\.20",
        "weighted source table": r"\|\s*Source\s*\|\s*Weight\s*\|",
    }
    returned = [label for label, pattern in retired_patterns.items() if re.search(pattern, text, re.IGNORECASE)]

    if missing or returned:
        parts = []
        if missing:
            parts.append("missing " + ", ".join(missing))
        if returned:
            parts.append("retired construct returned: " + ", ".join(returned))
        findings.append(Finding("RO-8", "ERROR", "; ".join(parts)))


RECIPE_HINT_RE = re.compile(r"(?<![A-Za-z0-9])([A-Za-z][A-Za-z0-9]*)\[([a-z0-9][a-z0-9-]*)\]")


def _dispatchable_tokens(skill_md: Path) -> set[str] | None:
    """Tokens a skill dispatches: its labelled allowlist, its Recipe-table
    Subcommand column, and backticked tokens on `alias` lines of `## Recipes`.
    None when the skill has no Recipes section (nothing to check against)."""
    recipes = read_markdown_section(skill_md.read_text(encoding="utf-8"), "Recipes")
    if recipes is None:
        return None
    tokens = set(dispatch_allowlist(recipes) or [])
    for cells in recipe_cells(recipes):
        if len(cells) >= 2:
            tokens.update(re.findall(r"`([a-z0-9][a-z0-9-]*)`", cells[1]))
    # Prose tokens count only on a line that declares them as aliases (e.g.
    # Tome's "first-token aliases for `article <platform>`"); keyword tables
    # and descriptive prose also carry backticked words that are not subcommands.
    for line in active_text(recipes).splitlines():
        if re.search(r"\balias", line, re.IGNORECASE):
            tokens.update(re.findall(r"`([a-z0-9][a-z0-9-]*)`", line))
    return tokens or None


def _reference_markdown(skill_dir: Path) -> list[Path]:
    """Every `.md` under `skill_dir/reference/`, nested directories included.

    Symlinks are not followed: skills link `_common/` and sibling skills' trees
    into `reference/`, and those files belong to (and are scanned with) their
    owner, so following them would report one defect under several paths.
    """
    reference = skill_dir / "reference"
    if not reference.is_dir() or reference.is_symlink():
        return []
    found = []
    for directory, _, names in os.walk(reference):
        for name in names:
            path = Path(directory) / name
            if name.endswith(".md") and not path.is_symlink() \
                    and not _corpus.is_excluded_path(path, REPO_ROOT):
                found.append(path)
    return sorted(found)


def _live_skills() -> dict[str, Path]:
    """Lower-cased live skill name -> SKILL.md: owned top-level skills, then
    the canonical project-local `.claude/skills/` copies (never the mirror)."""
    skills: dict[str, Path] = {}
    for d in _corpus.iter_skill_dirs(REPO_ROOT):
        skills[d.name.lower()] = d / "SKILL.md"
    local = REPO_ROOT / ".claude" / "skills"
    if local.is_dir():
        for d in sorted(local.iterdir()):
            if (d / "SKILL.md").is_file():
                skills.setdefault(d.name.lower(), d / "SKILL.md")
    return skills


def check_recipe_hint_subcommands(findings: list[Finding]):
    """RO-9: single-token `Skill[token]` hints in every routing-matrix.md
    column after Task Type must name a subcommand the skill dispatches."""
    if not ROUTING_MATRIX.is_file():
        findings.append(Finding("RO-9", "WARNING", "routing-matrix.md not found — recipe-hint check skipped"))
        return
    skills = _live_skills()
    allow_cache: dict[str, set[str] | None] = {}
    checked = 0
    bad = []
    content = active_text(ROUTING_MATRIX.read_text(encoding="utf-8"))
    malformed = []
    for cells in _matrix_rows(content, malformed):
        if len(cells) < 3:
            continue
        for column in cells[1:]:
            for agent, token in RECIPE_HINT_RE.findall(column):
                skill_md = skills.get(agent.lower())
                if skill_md is None:
                    continue
                if agent.lower() not in allow_cache:
                    allow_cache[agent.lower()] = _dispatchable_tokens(skill_md)
                allowed = allow_cache[agent.lower()]
                if allowed is None:
                    continue
                checked += 1
                if token not in allowed:
                    bad.append(f"{cells[0]}: `{agent}[{token}]`")
    if malformed:
        findings.append(Finding(
            "RO-9", "ERROR",
            "routing-matrix.md rows whose cell count differs from their header (an unescaped `|` "
            "inside a cell shifts later hints out of the checked columns; escape it as `\\|`): "
            + "; ".join(malformed),
        ))
    if bad:
        findings.append(Finding(
            "RO-9", "ERROR",
            "routing-matrix.md hints name subcommand(s) the target skill does not dispatch "
            "(the skill would silently fall back to its default Recipe): " + "; ".join(sorted(set(bad))),
        ))
    if checked == 0:
        findings.append(Finding("RO-9", "WARNING", "no single-token Skill[token] hints found — recipe-hint check may be stale vs table format"))


# RO-10 form (a): `**Skill `token`` or `**Skill `token mode ...``. The tail is
# kebab words only, so `**Native `git --update-refs`` (an adjective plus a
# command line) does not read as a skill pointer.
BOLD_SUBCOMMAND_RE = re.compile(
    r"\*\*([A-Za-z][A-Za-z0-9]*) `([a-z0-9][a-z0-9-]*)(?: [a-z0-9][a-z0-9-]*)*`")
# A backticked `subcommand mode` pair declared in a skill's Recipes or Subcommand
# Dispatch section. A pair that is itself mapped somewhere (`security review` ->
# security focus) or sits in a table's first, trigger-keyword cell is an input
# phrase, not a mode declaration, and is skipped.
MODE_PAIR_RE = re.compile(r"`([a-z0-9][a-z0-9-]*) ([a-z][a-z0-9-]*)`(?!\s*(?:->|→))")
# RO-10 form (c): a code span that is exactly `skill[token]`, skill lower-case.
CODE_HINT_RE = re.compile(r"(?<!`)`([a-z][a-z0-9]*)\[([a-z0-9][a-z0-9-]*)\]`(?!`)")


def check_corpus_subcommand_references(findings: list[Finding]):
    """RO-10: unambiguous cross-skill subcommand pointers outside the routing
    matrix must name a token the target skill dispatches."""
    skills = _live_skills()
    allowed: dict[str, set[str]] = {}
    modes: dict[str, dict[str, str]] = {}  # skill -> {mode: owning subcommand}
    for name, skill_md in skills.items():
        tokens = _dispatchable_tokens(skill_md)
        if tokens is None:
            continue
        allowed[name] = tokens
        skill_text = without_fenced_examples(skill_md.read_text(encoding="utf-8"))
        text = "\n".join(read_markdown_section(skill_text, section) or ""
                         for section in ("Recipes", "Subcommand Dispatch"))
        modes[name] = {}
        for line in text.splitlines():
            if line.lstrip().startswith("|"):
                line = "|".join(line.split("|")[2:])  # drop the trigger cell
            for m in MODE_PAIR_RE.finditer(line):
                if m.group(1) in tokens and m.group(2) not in tokens:
                    modes[name].setdefault(m.group(2), m.group(1))

    files: list[Path] = []
    for skill_md in skills.values():
        files.append(skill_md)
        files.extend(_reference_markdown(skill_md.parent))
    files.extend(sorted((REPO_ROOT / "_common").glob("*.md")))

    checked = 0
    bad: list[str] = []
    for path in files:
        if path.name == "CHANGELOG.md" or _corpus.is_excluded_path(path, REPO_ROOT):
            continue
        rel = path.relative_to(REPO_ROOT)
        text = without_fenced_examples(path.read_text(encoding="utf-8"))
        for number, line in enumerate(text.splitlines(), 1):
            for match in BOLD_SUBCOMMAND_RE.finditer(line):
                name, token = match.group(1).lower(), match.group(2)
                if name not in allowed:
                    continue
                checked += 1
                if token not in allowed[name]:
                    bad.append(f"{rel}:{number}: `{match.group(0)}` — `{token}` is not a {name} subcommand")
            code_spans = []
            for match in CODE_HINT_RE.finditer(line):
                name, token = match.group(1), match.group(2)
                if name not in allowed:
                    continue
                checked += 1
                code_spans.append(match.span())
                if token in allowed[name]:
                    continue
                hint = (f"; `{token}` is a mode of `{modes[name][token]}`"
                        if token in modes[name] else "")
                bad.append(f"{rel}:{number}: {match.group(0)} — `{token}` is not a {name} subcommand{hint}")
            for match in RECIPE_HINT_RE.finditer(line):
                name, token = match.group(1).lower(), match.group(2)
                if any(start <= match.start() < end for start, end in code_spans):
                    continue  # already judged as form (c)
                if name not in allowed or token in allowed[name] or token not in modes[name]:
                    continue
                owner = modes[name][token]
                bad.append(f"{rel}:{number}: `{match.group(0)}` — `{token}` is a mode of "
                           f"`{owner}`, write `{match.group(1)}[{owner} {token}]`")
    if bad:
        findings.append(Finding(
            "RO-10", "ERROR",
            "subcommand reference(s) the target skill does not dispatch "
            "(following them silently runs its default Recipe): " + "; ".join(bad),
        ))
    if checked == 0:
        findings.append(Finding("RO-10", "WARNING", "no `**Skill `token`` / `skill[token]` references found — corpus check may be stale vs prose format"))


# RO-11. Endpoints that are not skills but are documented handoff parties:
# the human requester, a generic agent placeholder, and "whichever skill
# implements the step" (Sherpa -> Builder/Forge).
HANDOFF_PSEUDO_ENDPOINTS = frozenset({"USER", "AGENT", "IMPL"})

# RO-11 reviewed exceptions: token -> (files that document it, why it stays).
# Pinned to files so a legacy spelling cannot spread as a live emission.
HANDOFF_TOKEN_ALLOWLIST = {
    "NATIVE_TO_SHOWCASE": (("native/reference/handoffs.md",),
                           "legacy name, normalised to NATIVE_TO_VITRINE on receipt"),
    "ACCORD_TO_SCRIBE": (("scribe/reference/unified-spec/README.md",
                          "scribe/reference/unified-spec/handoff-formats.md"),
                         "legacy Accord alias, consumed until the reactivation window closes"),
    "RESEARCHER_TO_ACCORD": (("scribe/reference/unified-spec/handoff-formats.md",), "legacy Accord alias"),
    "CAST_TO_ACCORD": (("scribe/reference/unified-spec/handoff-formats.md",), "legacy Accord alias"),
    "VOICE_TO_ACCORD": (("scribe/reference/unified-spec/handoff-formats.md",), "legacy Accord alias"),
    "UNIFIED_TO_FORMAL": (("scribe/reference/unified-spec/handoff-formats.md",),
                          "internal Scribe recipe transition, documented as not a handoff"),
}

# Group 3 (a lookahead, so group 0 stays `SENDER_TO_RECEIVER` for the
# allowlist) holds the segments after the receiver, e.g. `_HANDOFF`.
HANDOFF_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9_])([A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*?)_TO_([A-Z][A-Z0-9]*)(?=((?:_[A-Z0-9]+)*))"
)
# The corpus's handoff payloads end in `_HANDOFF`; other suffixes (FEEDBACK,
# REQUEST, ...) occur only between two live skills, so they decide nothing.
HANDOFF_SUFFIXES = frozenset({"HANDOFF"})


RENAME_ROW_RE = re.compile(r"\|\s*`([a-z0-9-]+)`\s*→\s*`[a-z0-9-]+`")

# Skills no longer in the tree. Mostly packages deleted from `.archive/` in commit 7969059 (CHANGELOG "Removed —
# retired skill packages"). With the directory gone this is the only record of
# their names short of git history, which a shallow CI checkout does not have.
# A future sunset keeps its package under `.archive/` and is read from there.
REMOVED_SKILLS = frozenset({
    "accord", "anvil", "bazaar", "bond", "clause", "crest", "cull", "director",
    "grok", "harvest", "hearth", "helm", "latch", "loom", "mint", "morph", "nest",
    "oath", "pipe", "plea", "relay", "riff", "sage", "shard", "sketch", "snap",
    "summon", "tempo", "titan", "trawl", "zine",
    # Retired without an archived package: absorbed in CHANGELOG prose
    # (`dock`, `wield`), renamed then retired (`agora`), or guarded only by the
    # task-battery stale-agent list (`dawn`, `hex`, `sonar`, `realm`, `haul`).
    "dock", "wield", "agora", "dawn", "hex", "sonar", "realm", "haul",
})


def _retired_endpoint_names() -> set[str]:
    """Names a token may still carry after a skill left: archived skill
    directories, the packages removed from the archive, and the old side of
    every `old → new` rename in CHANGELOG.md."""
    names = set(REMOVED_SKILLS)
    archive = REPO_ROOT / ".archive"
    if archive.is_dir():
        names |= {p.name for p in archive.iterdir() if p.is_dir()}
    changelog = REPO_ROOT / "CHANGELOG.md"
    if changelog.is_file():
        names |= set(RENAME_ROW_RE.findall(changelog.read_text(encoding="utf-8")))
    return {name.upper().replace("-", "_") for name in names}


def check_handoff_token_endpoints(findings: list[Finding]):
    """RO-11: `X_TO_Y` handoff tokens must name live skills (or a documented
    pseudo-endpoint, own-Recipe transition, or reviewed legacy alias)."""
    skills = _live_skills()
    names = {name.upper().replace("-", "_") for name in skills}
    retired = _retired_endpoint_names() - names
    own_tokens: dict[str, set[str]] = {}
    checked = 0
    bad: list[str] = []
    for name, skill_md in skills.items():
        own = {token.upper().replace("-", "_") for token in (_dispatchable_tokens(skill_md) or ())}
        for path in [skill_md, *_reference_markdown(skill_md.parent)]:
            if _corpus.is_excluded_path(path, REPO_ROOT):
                continue
            rel = path.relative_to(REPO_ROOT).as_posix()
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                for match in HANDOFF_TOKEN_RE.finditer(line):
                    token = match.group(0)
                    sender = match.group(1).split("_")[0]
                    receiver = match.group(2)
                    unknown = [seg for seg in (sender, receiver)
                               if seg not in names and seg not in HANDOFF_PSEUDO_ENDPOINTS
                               and seg not in own]
                    suffixed = not HANDOFF_SUFFIXES.isdisjoint(match.group(3).split("_"))
                    if len(unknown) == 2 and not suffixed and not set(unknown) <= retired:
                        # names no live endpoint: `PATH_TO_CONFIG`, or `SNAP_TO_GRID`
                        # where one retired name is an ordinary word. Both sides
                        # retired (`RESEARCHER_TO_SHOWCASE`) is a stale handoff.
                        continue
                    checked += 1
                    if rel in HANDOFF_TOKEN_ALLOWLIST.get(token, ((), ""))[0]:
                        continue
                    if unknown:
                        bad.append(f"{rel}:{number}: `{token}` — not a live skill: "
                                   + ", ".join(f"`{seg}`" for seg in dict.fromkeys(unknown)))
    if bad:
        findings.append(Finding(
            "RO-11", "ERROR",
            "handoff token(s) naming no live skill (a rename that never reached the token; "
            "fix the spelling, or add a reviewed legacy alias to HANDOFF_TOKEN_ALLOWLIST): "
            + "; ".join(bad),
        ))
    if checked == 0:
        findings.append(Finding("RO-11", "WARNING", "no `X_TO_Y` handoff tokens found — check may be stale vs prose format"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--severity", choices=("warning", "error", "strict"), default="warning")
    args = parser.parse_args()

    findings: list[Finding] = []
    safe_check(check_dead_references, findings)
    safe_check(check_ladder_token_order, findings)
    safe_check(check_producer_verifier, findings)
    safe_check(check_fallback_field, findings)
    safe_check(check_roster_completeness, findings)
    safe_check(check_bare_subcommand_dispatch, findings)
    safe_check(check_retired_reference_residue, findings)
    safe_check(check_confidence_gate_shape, findings)
    safe_check(check_recipe_hint_subcommands, findings)
    safe_check(check_corpus_subcommand_references, findings)
    safe_check(check_handoff_token_endpoints, findings)

    errors = [f for f in findings if f.level == "ERROR"]
    warnings = [f for f in findings if f.level == "WARNING"]

    for f in findings:
        print(str(f))
    print()
    print(f"Routing Oracle: {len(errors)} errors | {len(warnings)} warnings")

    if args.severity == "warning":
        return 0
    if args.severity == "error":
        return 1 if errors else 0
    return 1 if (errors or warnings) else 0  # strict


if __name__ == "__main__":
    sys.exit(main())
