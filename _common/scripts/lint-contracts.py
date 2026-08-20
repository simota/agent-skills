#!/usr/bin/env python3
"""
Lint contract *delivery* -- whether the contracts in `_common/` can actually reach a
running agent, and whether the paths a SKILL.md names resolve at runtime.

Nothing under `_common/` is loaded automatically. A contract arrives only because some
file the agent already has open names it, and the agent follows that name. A contract
that declares itself binding on every run but that no SKILL.md reaches is not a weak
rule -- it is an absent one, and nothing in the repository says so out loud.

Runtime path resolution is the second half of the same problem. A skill is invoked with
one base directory (its own), so `_common/OPERATIONAL.md` in `foo/SKILL.md` resolves as
`foo/_common/OPERATIONAL.md` and reaches the shared contract only through the `_common`
symlink beside it. A skill that names a repo file it has no symlink for prints a path
that exists to a reader browsing the repo and resolves to nothing to the agent.

Checks:

  CD-1  The spine roster in `_common/OPERATIONAL.md` s Contract Precedence and the set
        of files declaring `Tier: spine` name the same files. Drift here means a file
        believes it binds every run while the precedence order never lists it (or the
        reverse), and neither statement corrects the other.
  CD-2  Every owned SKILL.md reaches every spine contract. Depth 1 is a direct naming;
        depth 2 means the contract arrives only if the agent opens the intermediate
        document, which is itself conditional. Both are blocking: every spine contract
        reaches all 90 skills directly today, so anything less is a regression rather
        than a backlog item.
  CD-3  Every `_common/*.md` is reachable from at least one SKILL.md. A contract no
        skill can reach has no addressee -- it is maintained but never applied.
  CD-4  A SKILL.md never names a repo file that does not resolve from its own base
        directory. Scoped to paths that *do* exist at the repo root: a path that exists
        nowhere is a target-project artifact (`docs/prd/PRD-x.md`, `agents/eval-set.json`)
        and is CD-5's business, not a wiring fault.
  CD-5  A repo-internal reference (`_common/`, `_templates/`, `reference/`) resolves
        somewhere. These namespaces exist only inside this repository, so one that
        resolves nowhere is a dead pointer rather than a path into a user's project.
  CD-6  Every `_common/*.md` declares its tier. An undeclared tier makes CD-1 and the
        precedence order in OPERATIONAL.md unable to see the file at all.

Severity tiers:
  --severity warning  (default)  print findings, exit 0
  --severity error    exit 1 if any P0/P1 finding is reported

Usage:
  python3 _common/scripts/lint-contracts.py
  python3 _common/scripts/lint-contracts.py --severity error
  python3 _common/scripts/lint-contracts.py --report      # delivery matrix, always exit 0

Complexity Budget (`_common/HARNESS_DEBT.md` 3b):
  failure  -- a contract declared binding on every run that no skill reaches, and a
              named path that resolves for a human reading the repo but not for the
              agent reading the skill. Both are silent: the contract stays authored,
              the reference stays rendered, and only behaviour is missing
  effect    -- contract reachability becomes a measured property with a printable
              matrix (`--report`). Does NOT prove a contract was read at run time;
              it proves only that a path to it exists and resolves
  owner     -- gauge (it owns the checker suite)
  removal   -- delete when contract delivery stops depending on documents naming each
              other, i.e. when the runtime loads `_common/` by tier without a reference
"""

from __future__ import annotations

import argparse
import collections
import re
import sys
from pathlib import Path

import _corpus

REPO_ROOT = Path(__file__).resolve().parents[2]
COMMON = REPO_ROOT / "_common"

#: How far a BFS follows document-to-document references before giving up. Three hops
#: is already past the point where a contract can be relied on to arrive; it exists so
#: CD-3 does not call a deeply-buried file orphaned when a path to it does exist.
MAX_HOPS = 3

#: Spine contracts should be named directly. Depth above this is reported, not failed.
DIRECT_DEPTH = 1

#: Backtick-quoted references to markdown documents, e.g. `_common/HANDOFF.md`.
TICKED_MD = re.compile(r"`([A-Za-z0-9_~.][A-Za-z0-9_./~-]*\.md)`")

#: Backtick-quoted references to any file this repository could own.
TICKED_ANY = re.compile(r"`([A-Za-z0-9_~.][A-Za-z0-9_./~-]*\.(?:md|py|ya?ml|json))`")

#: Markdown link targets, e.g. [`token-economy.py`](scripts/token-economy.py).
MD_LINK = re.compile(r"\]\(([A-Za-z0-9_.][A-Za-z0-9_./-]*\.(?:md|py|ya?ml|json))\)")

#: Namespaces that exist only inside this repository (CD-5 scope).
REPO_NAMESPACES = ("_common/", "_templates/", "reference/", "_prompts/", "_loops/")

#: Self-declared tier line, e.g. "> **Tier:** `spine` -- in effect on every run."
TIER_LINE = re.compile(r"\*\*Tier:\*\*\s*`?([a-z]+)`?")

#: The authoritative spine roster: the Contract Precedence entry that enumerates it.
SPINE_ROSTER_LINE = re.compile(r"^\d+\.\s+\*\*The spine\*\*(.+)$", re.M)


def read(path: Path) -> str:
    """File text, or empty when the sandbox or the filesystem refuses the read.

    Some paths under the skills root are read-denied by the agent sandbox (credential
    patterns). A checker that dies on one of them reports nothing about the other 90
    skills, so an unreadable file is treated as having no outgoing references.
    """
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def exists(path: Path) -> bool:
    """Whether `path` is there. An unverifiable path counts as present.

    The agent sandbox denies `stat` on credential-shaped names, so `gear/reference/
    secrets-management.md` raises rather than answering. Reporting an unreadable path
    as missing would make this checker fail on exactly the files it cannot see.
    """
    try:
        return path.exists()
    except OSError:
        return True


def is_placeholder(ref: str) -> bool:
    """True for template patterns rather than concrete paths."""
    return any(c in ref for c in "*{}[]<>") or ref.startswith(("~", "/"))


def named_refs(text: str) -> list[tuple[int, str]]:
    """(line number, reference) for every path this document names outside code fences."""
    out: list[tuple[int, str]] = []
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for pattern in (TICKED_ANY, MD_LINK):
            for ref in pattern.findall(line):
                if not is_placeholder(ref):
                    out.append((lineno, ref))
    return out


def base_dir(path: Path) -> Path:
    """The directory a reference inside `path` is resolved against at run time.

    A skill is invoked with exactly one base directory -- its own. Opening a file under
    `reference/` does not move that base, so a reference in `foo/reference/bar.md` still
    resolves from `foo/`, not from `foo/reference/`.
    """
    if COMMON in path.parents or path.parent == COMMON:
        return COMMON
    for parent in [path.parent, *path.parents]:
        if (parent / "SKILL.md").is_file():
            return parent
    return REPO_ROOT


def resolve(ref: str, origin: Path) -> Path | None:
    """The file `ref` names when read from `origin`, or None when it resolves nowhere."""
    for candidate in (base_dir(origin) / ref, REPO_ROOT / ref, COMMON / ref):
        if exists(candidate):
            try:
                return candidate.resolve()
            except OSError:
                return candidate
    return None


class Graph:
    """Documents as nodes, "this file names that file" as edges."""

    def __init__(self) -> None:
        self._edges: dict[Path, set[Path]] = {}

    def edges(self, node: Path) -> set[Path]:
        if node not in self._edges:
            self._edges[node] = {
                target
                for _, ref in named_refs(read(node))
                if ref.endswith(".md") and (target := resolve(ref, node)) is not None
            }
        return self._edges[node]

    def depths(self, root: Path, max_hops: int = MAX_HOPS) -> dict[Path, int]:
        """Shortest hop count from `root` to every document reachable within `max_hops`."""
        seen = {root.resolve(): 0}
        queue = collections.deque([root.resolve()])
        while queue:
            node = queue.popleft()
            if seen[node] >= max_hops:
                continue
            for target in self.edges(node):
                if target not in seen:
                    seen[target] = seen[node] + 1
                    queue.append(target)
        return seen


def declared_tiers() -> dict[str, str | None]:
    """Tier each `_common/*.md` declares for itself, None when it declares none."""
    tiers: dict[str, str | None] = {}
    for path in sorted(COMMON.glob("*.md")):
        match = TIER_LINE.search(read(path)[:2000])
        tiers[path.name] = match.group(1) if match else None
    return tiers


def roster_spine() -> set[str] | None:
    """The spine as OPERATIONAL.md's Contract Precedence enumerates it."""
    match = SPINE_ROSTER_LINE.search(read(COMMON / "OPERATIONAL.md"))
    if not match:
        return None
    return set(re.findall(r"`([A-Z0-9_]+\.md)`", match.group(1)))


def check_spine_roster(tiers: dict[str, str | None], findings: list) -> set[str]:
    """CD-1. Returns the spine set to check delivery against."""
    declared = {name for name, tier in tiers.items() if tier == "spine"}
    roster = roster_spine()
    if roster is None:
        findings.append(("P1", "CD-1", "OPERATIONAL.md has no enumerated spine roster in Contract Precedence"))
        return declared
    for name in sorted(declared - roster):
        findings.append(
            ("P0", "CD-1", f"_common/{name} declares `Tier: spine` but Contract Precedence does not list it")
        )
    for name in sorted(roster - declared):
        findings.append(
            ("P0", "CD-1", f"Contract Precedence lists `{name}` in the spine but the file does not declare `Tier: spine`")
        )
    return declared | roster


def check_delivery(graph: Graph, skills: list[Path], spine: set[str], findings: list) -> dict[str, dict[str, int]]:
    """CD-2. Returns {contract: {skill: depth}}, depth 99 meaning unreachable."""
    matrix: dict[str, dict[str, int]] = {name: {} for name in sorted(spine)}
    for skill in skills:
        depths = graph.depths(skill / "SKILL.md")
        for name in matrix:
            target = (COMMON / name).resolve()
            matrix[name][skill.name] = depths.get(target, 99)

    for name, per_skill in matrix.items():
        unreachable = sorted(s for s, d in per_skill.items() if d == 99)
        indirect = sorted(s for s, d in per_skill.items() if DIRECT_DEPTH < d < 99)
        if unreachable:
            findings.append(
                ("P0", "CD-2", f"_common/{name} is spine but unreachable from {len(unreachable)} skill(s): "
                               f"{', '.join(unreachable[:5])}{' ...' if len(unreachable) > 5 else ''}")
            )
        if indirect:
            findings.append(
                ("P1", "CD-2", f"_common/{name} reaches {len(indirect)}/{len(per_skill)} skill(s) only "
                               f"indirectly (depth 2+): {', '.join(indirect[:5])}"
                               f"{' ...' if len(indirect) > 5 else ''}")
            )
    return matrix


def check_orphans(graph: Graph, skills: list[Path], findings: list) -> None:
    """CD-3."""
    reached: set[Path] = set()
    for skill in skills:
        reached |= set(graph.depths(skill / "SKILL.md"))
    for path in sorted(COMMON.glob("*.md")):
        if path.resolve() not in reached:
            findings.append(
                ("P1", "CD-3", f"_common/{path.name} is reachable from no SKILL.md within {MAX_HOPS} hops")
            )


def check_resolution(skills: list[Path], findings: list) -> None:
    """CD-4 and CD-5.

    Scoped to references into this repository. A SKILL.md also names paths in the
    *user's* project -- `CLAUDE.md`, `AGENTS.md`, `.agents/PROJECT.md`, `docs/prd/…` --
    and those are supposed not to resolve from the skill directory. This repository
    happens to contain files by some of those names, so "exists at the repo root" alone
    would report every journal-writing skill as mis-wired.
    """
    own_names = {skill.name for skill in skills}

    def repo_internal(ref: str) -> bool:
        head = ref.split("/", 1)[0]
        return ref.startswith(REPO_NAMESPACES) or (head in own_names and "/" in ref)

    for skill in skills:
        skill_md = skill / "SKILL.md"
        seen: set[str] = set()
        for lineno, ref in named_refs(read(skill_md)):
            if ref in seen or not repo_internal(ref):
                continue
            seen.add(ref)
            if ".." in Path(ref).parts:
                findings.append(
                    ("P2", "CD-4", f"{skill.name}/SKILL.md:{lineno} references `{ref}` -- `..` resolves today only "
                                   f"because the skills root and the repo root are the same directory; it breaks "
                                   f"wherever the skill is linked in from elsewhere (`_common/PORTABILITY.md`). "
                                   f"Name it repo-relative and reach it through the symlink beside the skill")
                )
                continue
            if exists(base_dir(skill_md) / ref):
                continue
            if exists(REPO_ROOT / ref):
                findings.append(
                    ("P0", "CD-4", f"{skill.name}/SKILL.md:{lineno} names `{ref}`, which exists at the repo root "
                                   f"but not from {skill.name}/ -- the skill needs a symlink for it")
                )
            else:
                findings.append(
                    ("P1", "CD-5", f"{skill.name}/SKILL.md:{lineno} names `{ref}`, which resolves nowhere")
                )


def check_tier_declarations(tiers: dict[str, str | None], findings: list) -> None:
    """CD-6."""
    for name, tier in sorted(tiers.items()):
        if tier is None:
            findings.append(("P2", "CD-6", f"_common/{name} declares no `Tier:` line"))


def print_report(matrix: dict[str, dict[str, int]], skills: list[Path]) -> None:
    print(f"Spine delivery across {len(skills)} owned skills (depth = hops from SKILL.md)\n")
    print(f"  {'contract':26} {'direct':>7} {'depth2+':>8} {'unreached':>10}")
    for name, per_skill in sorted(matrix.items()):
        counts = collections.Counter(per_skill.values())
        direct = counts[DIRECT_DEPTH]
        indirect = sum(v for d, v in counts.items() if DIRECT_DEPTH < d < 99)
        gone = counts[99]
        print(f"  _common/{name:<18}{direct:>7} {indirect:>8} {gone:>10}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--severity", choices=["warning", "error"], default="warning")
    parser.add_argument(
        "--report",
        action="store_true",
        help="print the delivery matrix above the findings and always exit 0",
    )
    args = parser.parse_args()

    skills = list(_corpus.iter_skill_dirs(REPO_ROOT))
    graph = Graph()
    tiers = declared_tiers()
    findings: list[tuple[str, str, str]] = []

    spine = check_spine_roster(tiers, findings)
    matrix = check_delivery(graph, skills, spine, findings)

    if args.report:
        print_report(matrix, skills)
        print()

    check_orphans(graph, skills, findings)
    check_resolution(skills, findings)
    check_tier_declarations(tiers, findings)

    if not findings:
        print(f"lint-contracts: OK ({len(skills)} skills, {len(tiers)} contracts, {len(spine)} spine)")
        return 0

    for severity, rule, message in sorted(findings):
        print(f"[{severity}] {rule}: {message}")

    blocking = [f for f in findings if f[0] in ("P0", "P1")]
    print(f"\n{len(findings)} finding(s), {len(blocking)} blocking")
    if args.report:
        return 0
    return 1 if args.severity == "error" and blocking else 0


if __name__ == "__main__":
    sys.exit(main())
