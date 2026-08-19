#!/usr/bin/env python3
"""
Lint SKILL.md frontmatter and structural constraints for the claude-skills repository.

Checks (all derived from official Anthropic Agent Skills spec + repository conventions):

  F1  name: kebab-case, <=64 chars, no reserved prefixes (anthropic/claude), no XML tags
  F2  description: non-empty, <=1024 chars, no XML tags, no Japanese chars,
                   contains WHAT (capability) AND WHEN (trigger) phrasing
  F3  No frontmatter keys outside the allowlist (name, description, optional: model, tools)
  N1  Skill folder name == frontmatter name field (kebab-case match)
  N2  Skill folder name is kebab-case (no spaces, no underscores, no capitals)
  C1  Filename is exactly "SKILL.md" (case-sensitive, official spec)
  C2  No README.md inside the skill folder (forbidden by Anthropic Complete Guide)
  S1  SKILL.md body line count. Tiers: >500 P3 (Anthropic recommendation), >700 P2, >1000 P1
  S2  SKILL.md body token estimate (char_count / 3.5). Tiers: >7000 P3, >10000 P2, >15000 P1
  H1  CAPABILITIES_SUMMARY HTML comment block present (presence only; rule ID aligned
      with gauge's 19-item checklist H1)
  H2  COLLABORATION_PATTERNS marker present inside the CAPABILITIES_SUMMARY block (H2)
  H3  PROJECT_AFFINITY marker present inside the CAPABILITIES_SUMMARY block (H3)
  H4  BIDIRECTIONAL_PARTNERS marker present inside the CAPABILITIES_SUMMARY block.
      Declared by _templates/SKILL_TEMPLATE.md and read by nexus/compass for routing;
      went unchecked until 2026-08-17, by which point 4 skills had silently dropped it.
  ST1 Required section headings present (see REQUIRED_HEADINGS below) — headings
      standardized empirically at >=90% frequency across the corpus, not hardcoded
      by convention alone

All H1-H3/ST1 findings are presence-only checks (P2, non-blocking) — quality
judgment on marker *content* stays with the Gauge agent's H1-H3 checklist items.

Severity tiers:
  --severity warning  (default)  print findings, exit 0
  --severity error    exit 1 if any P0/P1 finding is reported
  --severity strict   exit 1 if any finding is reported

Usage:
  python3 _common/scripts/lint-frontmatter.py [--severity warning|error|strict]
                                              [--paths skill1 skill2 ...]
                                              [--changed-only]   # only lint paths under git diff
                                              [--json]           # machine-readable output

Exit codes:
  0  no blocking findings under the chosen severity
  1  blocking findings present
  2  internal error (bad regex, missing file, etc.)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[2]

FRONTMATTER_KEY_ALLOWLIST = {"name", "description", "model", "tools"}
RESERVED_PREFIXES = {"anthropic", "claude"}
NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
JAPANESE_PATTERN = re.compile(r"[぀-ゟ゠-ヿ一-鿿]")
XML_TAG_PATTERN = re.compile(r"<[a-zA-Z/!?][^>]*>")
WHEN_PHRASES = (
    "when",
    "use this",
    "use it",
    "trigger",
    "use to",
    "use for",
    "needs",
    "needed",
    "intended for",
    "designed for",
    "for ",
    "applies",
)
WHAT_HINTS = (
    "agent",
    "specialist",
    "generator",
    "audit",
    "analyzer",
    "design",
    "build",
    "create",
    "generate",
    "review",
    "implement",
    "specialist",
    "orchestrator",
    "expert",
    "tool",
    "framework",
)
SKIP_DIRS = {".git", "node_modules", ".agents", "_loops", "_prompts", "_templates"}

SEVERITY_RANK = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}

CAPABILITIES_SUMMARY_PATTERN = re.compile(r"<!--[^>]*CAPABILITIES_SUMMARY:", re.DOTALL)

# Headings required empirically at >=90% frequency across the 133-skill corpus
# (measured via `grep -c '^## ' */SKILL.md` heading-set frequency, 2026-07-29).
# Anything below 90% is corpus convention, not a near-universal structural norm,
# so it is left to Gauge's content-quality judgment rather than hardcoded here.
REQUIRED_HEADINGS = (
    "Trigger Guidance",
    "Core Contract",
    "Boundaries",
    "Collaboration",
    "Workflow",
    "Recipes",
    "Subcommand Dispatch",
    "Output Requirements",
    "Reference Map",
    "Operational",
    "AUTORUN Support",
    "Nexus Hub Mode",
)
# Documented equivalents: some headings have an accepted alternate spelling
# per the normalization checklist. "References" is the accepted short form
# of "Reference Map" (same section, same content contract).
HEADING_EQUIVALENTS = {
    "Reference Map": ("References",),
}
HEADING_PATTERN = re.compile(r"^##\s+(.+)$", re.MULTILINE)


@dataclass
class Finding:
    skill: str
    item: str
    priority: str
    message: str
    file: str
    line: int = 0


@dataclass
class Report:
    skill_count: int = 0
    findings: list[Finding] = field(default_factory=list)

    def add(self, f: Finding) -> None:
        self.findings.append(f)

    def by_priority(self, p: str) -> list[Finding]:
        return [f for f in self.findings if f.priority == p]


def iter_skill_dirs(roots: Iterable[Path]) -> list[Path]:
    skills: list[Path] = []
    for root in roots:
        # Resolve relative paths against REPO_ROOT so `--paths gauge` works
        # regardless of the caller's CWD.
        if not root.is_absolute():
            root = (REPO_ROOT / root).resolve()
        if root.is_file() and root.name == "SKILL.md":
            skills.append(root.parent)
            continue
        if not root.is_dir():
            continue
        # If the dir itself contains a SKILL.md, treat it as a skill (direct target).
        if (root / "SKILL.md").exists():
            skills.append(root)
            continue
        # Otherwise treat root as a parent directory and scan one level down.
        for entry in sorted(root.iterdir()):
            if entry.is_dir() and entry.name not in SKIP_DIRS and not entry.name.startswith("."):
                skill_md = entry / "SKILL.md"
                if skill_md.exists():
                    skills.append(entry)
    return skills


def parse_frontmatter(text: str) -> tuple[dict[str, str], int, list[str]]:
    """Return (key/value, body_start_line_idx_1based, raw_lines)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, 1, lines
    fm: dict[str, str] = {}
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$", lines[i])
        if m:
            fm[m.group(1)] = m.group(2).strip()
    body_start = (end_idx + 1) if end_idx is not None else 1
    return fm, body_start, lines


def approx_token_count(text: str) -> int:
    # tiktoken-free estimate: ~3.5 chars/token in mixed Markdown+English.
    return max(1, int(len(text) / 3.5))


def has_when_phrase(desc: str) -> bool:
    low = desc.lower()
    return any(p in low for p in WHEN_PHRASES)


def has_what_phrase(desc: str) -> bool:
    low = desc.lower()
    if any(p in low for p in WHAT_HINTS):
        return True
    # Fallback: a description with a verb-ish first clause longer than 30 chars
    head = re.split(r"[.\n]", desc, maxsplit=1)[0].strip()
    return len(head) >= 30


def lint_skill(skill_dir: Path, report: Report) -> None:
    name = skill_dir.name
    skill_md = skill_dir / "SKILL.md"
    rel = str(skill_md.relative_to(REPO_ROOT))

    # C1: filename case sensitivity
    siblings = {p.name for p in skill_dir.iterdir() if p.is_file()}
    bad_case = {n for n in siblings if n.lower() == "skill.md" and n != "SKILL.md"}
    if bad_case:
        report.add(Finding(name, "C1", "P0",
                           f"non-canonical SKILL.md filename: {sorted(bad_case)}", rel))

    # C2: README.md inside skill folder is forbidden
    if "README.md" in siblings:
        report.add(Finding(name, "C2", "P1",
                           "README.md inside skill folder is forbidden by Anthropic spec",
                           rel))

    # N1/N2: folder name kebab-case
    if not NAME_PATTERN.match(name):
        report.add(Finding(name, "N2", "P1",
                           f"skill folder '{name}' is not kebab-case", rel))

    if not skill_md.exists():
        report.add(Finding(name, "C1", "P0", "SKILL.md missing", rel))
        return

    text = skill_md.read_text(encoding="utf-8")
    fm, body_start, lines = parse_frontmatter(text)

    # F1: name
    fm_name = fm.get("name", "").strip()
    if not fm_name:
        report.add(Finding(name, "F1", "P0", "frontmatter 'name:' missing or empty", rel, 1))
    else:
        if len(fm_name) > 64:
            report.add(Finding(name, "F1", "P0",
                               f"name length {len(fm_name)} > 64 chars", rel, 1))
        if not NAME_PATTERN.match(fm_name):
            report.add(Finding(name, "F1", "P0",
                               f"name '{fm_name}' not kebab-case", rel, 1))
        if any(fm_name == p or fm_name.startswith(p + "-") for p in RESERVED_PREFIXES):
            report.add(Finding(name, "F1", "P0",
                               f"name '{fm_name}' uses reserved prefix (anthropic/claude)",
                               rel, 1))
        if XML_TAG_PATTERN.search(fm_name):
            report.add(Finding(name, "F1", "P0",
                               "name contains XML tags", rel, 1))
        if fm_name != name:
            report.add(Finding(name, "N1", "P1",
                               f"frontmatter name '{fm_name}' != folder '{name}'", rel, 1))

    # F2: description
    desc = fm.get("description", "").strip()
    if not desc:
        report.add(Finding(name, "F2", "P0",
                           "frontmatter 'description:' missing or empty", rel, 1))
    else:
        if len(desc) > 1024:
            report.add(Finding(name, "F2", "P0",
                               f"description length {len(desc)} > 1024 chars", rel, 1))
        if XML_TAG_PATTERN.search(desc):
            report.add(Finding(name, "F2", "P0",
                               "description contains XML tags (system-prompt injection risk)",
                               rel, 1))
        if JAPANESE_PATTERN.search(desc):
            report.add(Finding(name, "F2", "P0",
                               "description contains Japanese characters (must be English)",
                               rel, 1))
        # WHAT+WHEN are heuristic — keep at P2 to avoid false-positive CI noise.
        # Hard P0 only triggers on missing/over-long/XML/JP characters above.
        if not has_when_phrase(desc):
            report.add(Finding(name, "F2", "P2",
                               "description lacks WHEN trigger phrase "
                               "(e.g. 'Use when ...', 'Triggers when ...', 'for ...')",
                               rel, 1))
        if not has_what_phrase(desc):
            report.add(Finding(name, "F2", "P2",
                               "description lacks WHAT capability statement", rel, 1))

    # F3: frontmatter key allowlist
    extra_keys = set(fm.keys()) - FRONTMATTER_KEY_ALLOWLIST
    if extra_keys:
        priority = "P0" if extra_keys & {"permissions", "trust", "capabilities", "required_tools"} else "P1"
        report.add(Finding(name, "F3", priority,
                           f"non-spec frontmatter keys: {sorted(extra_keys)}", rel, 1))

    # S1/S2: size constraints (body only, excluding frontmatter)
    # Tiered against the actual repository floor — official Anthropic guidance is
        # "<5000 tokens / <500 lines" but the existing corpus runs higher (125 skills as of 2026-08-18),
    # so P0/P1 fire only at egregious sizes. Refactor targets are P2/P3.
    body_lines = lines[body_start:]
    line_count = len(body_lines)
    body_text = "\n".join(body_lines)
    token_estimate = approx_token_count(body_text)

    if line_count > 1000:
        report.add(Finding(name, "S1", "P1",
                           f"SKILL.md body {line_count} lines > 1000 (egregious)",
                           rel, body_start))
    elif line_count > 700:
        report.add(Finding(name, "S1", "P2",
                           f"SKILL.md body {line_count} lines > 700 (refactor candidate)",
                           rel, body_start))
    elif line_count > 500:
        report.add(Finding(name, "S1", "P3",
                           f"SKILL.md body {line_count} lines > 500 (Anthropic recommendation)",
                           rel, body_start))

    if token_estimate > 15000:
        report.add(Finding(name, "S2", "P1",
                           f"SKILL.md body ~{token_estimate} tokens > 15000 (egregious)",
                           rel, body_start))
    elif token_estimate > 10000:
        report.add(Finding(name, "S2", "P2",
                           f"SKILL.md body ~{token_estimate} tokens > 10000 (refactor candidate)",
                           rel, body_start))
    elif token_estimate > 7000:
        report.add(Finding(name, "S2", "P3",
                           f"SKILL.md body ~{token_estimate} tokens > 7000 (over Anthropic 5000 rec)",
                           rel, body_start))

    # H1/H2/H3: CAPABILITIES_SUMMARY block + its COLLABORATION_PATTERNS/PROJECT_AFFINITY
    # markers. Presence only — marker *content* quality is Gauge's H1-H3 checklist job.
    cap_match = CAPABILITIES_SUMMARY_PATTERN.search(text)
    if not cap_match:
        report.add(Finding(name, "H1", "P2",
                           "CAPABILITIES_SUMMARY HTML comment block not found", rel, 1))
    else:
        # The block's true closing tag is "-->" on its own line. A naive
        # text.find("-->", ...) can match an embedded "-->" inside an
        # inline-code example within a bullet (e.g. a literal
        # "`<!-- translator comment -->`" snippet), truncating the scan
        # window before later markers like COLLABORATION_PATTERNS /
        # PROJECT_AFFINITY are reached. Anchor on a standalone closing line.
        closing_match = re.search(r"^\s*-->\s*$", text[cap_match.start():], re.MULTILINE)
        comment_end = (cap_match.start() + closing_match.start()) if closing_match else -1
        block = text[cap_match.start():comment_end if comment_end != -1 else len(text)]
        if "COLLABORATION_PATTERNS:" not in block:
            report.add(Finding(name, "H2", "P2",
                               "COLLABORATION_PATTERNS marker missing inside "
                               "CAPABILITIES_SUMMARY block", rel, 1))
        if "PROJECT_AFFINITY:" not in block:
            report.add(Finding(name, "H3", "P2",
                               "PROJECT_AFFINITY marker missing inside "
                               "CAPABILITIES_SUMMARY block", rel, 1))
        if "BIDIRECTIONAL_PARTNERS:" not in block:
            report.add(Finding(name, "H4", "P2",
                               "BIDIRECTIONAL_PARTNERS marker missing inside "
                               "CAPABILITIES_SUMMARY block", rel, 1))

    # ST1: required section headings (>=90% corpus frequency, see REQUIRED_HEADINGS)
    present_headings = {h.strip() for h in HEADING_PATTERN.findall(body_text)}
    missing_headings = [
        h for h in REQUIRED_HEADINGS
        if h not in present_headings
        and not any(alt in present_headings for alt in HEADING_EQUIVALENTS.get(h, ()))
    ]
    if missing_headings:
        report.add(Finding(name, "ST1", "P2",
                           f"missing required section heading(s): {missing_headings}",
                           rel, body_start))


def changed_paths() -> list[Path]:
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=str(REPO_ROOT), check=True, capture_output=True, text=True,
        ).stdout.strip().splitlines()
    except subprocess.CalledProcessError:
        return []
    paths = []
    for p in out:
        path = REPO_ROOT / p
        if path.name == "SKILL.md":
            paths.append(path)
    return paths


def render_text(report: Report) -> str:
    if not report.findings:
        return f"OK  no findings across {report.skill_count} skill(s)\n"
    out = [f"Scanned {report.skill_count} skill(s); {len(report.findings)} finding(s):", ""]
    for priority in ("P0", "P1", "P2", "P3"):
        bucket = report.by_priority(priority)
        if not bucket:
            continue
        out.append(f"[{priority}] {len(bucket)}")
        for f in bucket:
            out.append(f"  {f.skill:20s} {f.item:4s} {f.file}: {f.message}")
        out.append("")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--severity", choices=("warning", "error", "strict"),
                        default="warning")
    parser.add_argument("--paths", nargs="*", default=None,
                        help="explicit skill folders or SKILL.md paths to lint")
    parser.add_argument("--changed-only", action="store_true",
                        help="lint only SKILL.md files modified vs HEAD")
    parser.add_argument("--json", action="store_true",
                        help="emit JSON instead of text")
    args = parser.parse_args()

    if args.changed_only:
        targets = changed_paths()
        if not targets:
            print("no changed SKILL.md vs HEAD")
            return 0
        skills = iter_skill_dirs(targets)
    elif args.paths:
        skills = iter_skill_dirs(Path(p) for p in args.paths)
    else:
        skills = iter_skill_dirs([REPO_ROOT])

    report = Report(skill_count=len(skills))
    for s in skills:
        try:
            lint_skill(s, report)
        except Exception as e:  # never crash the linter on one bad skill
            report.add(Finding(s.name, "INTERNAL", "P1",
                               f"linter exception: {e}", str(s.relative_to(REPO_ROOT))))

    if args.json:
        print(json.dumps({
            "skill_count": report.skill_count,
            "findings": [asdict(f) for f in report.findings],
        }, indent=2, ensure_ascii=False))
    else:
        sys.stdout.write(render_text(report))

    if args.severity == "warning":
        return 0
    if args.severity == "error":
        blocking = report.by_priority("P0") + report.by_priority("P1")
        return 1 if blocking else 0
    return 1 if report.findings else 0


if __name__ == "__main__":
    sys.exit(main())
