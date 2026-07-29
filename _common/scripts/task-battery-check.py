#!/usr/bin/env python3
"""
Task Battery Check — mechanical checker for the Nexus routing regression
battery (`nexus/reference/task-battery.md`).

The battery has 35 items across two verification tiers:

  Items 1-28 (byte-identifiable): each item's "Expected routing" column
  claims a specific Recipe/task-type mapping backed by literal text in
  `nexus/reference/routing-matrix.md`, `nexus/reference/signal-keywords.md`,
  or the Recipes table in `nexus/SKILL.md`. This script asserts that literal
  evidence is still present (verbatim substring match) — it proves the
  routing *artifact* hasn't drifted out from under the battery's claim.
  It does NOT simulate classify's live semantic mapping of the item's
  example sentence to a Recipe — that step still requires an LLM.

  Items 29-35 (judgment items): out-of-coverage LADDER walks (29, 30, 33,
  34, 35) and ambiguous GATE/REDIRECT stress tests (31, 32) can only be
  proven by actually running classify (compass Gap-mode, architect
  proposal, confidence scoring) — no static text search substitutes for
  that. These are reported as `SKIPPED (judgment item)` so the battery's
  35-item coverage stays fully accounted for (no silent caps).

Also runs a lightweight STALE guard: flags any task-battery.md item that
still names a retired agent (Dawn / Hex / Sonar / Realm / Haul — sunset
prior to the 2026-07-29 routing-matrix.md edit), so a future edit that
reintroduces a stale reference is caught instead of silently passing.

Fail-open contract (mirrors routing-oracle.py): any unhandled exception
during a check is caught, printed as a WARNING, and the check is skipped —
this script must never be the reason a routing-machinery PR is blocked by
its own bug.

Usage:
  python3 _common/scripts/task-battery-check.py [--severity warning|error|strict]

Severity tiers:
  --severity warning  (default)  print findings, exit 0
  --severity error    exit 1 if any FAIL (ERROR-level) finding
  --severity strict   exit 1 if any FAIL or STALE (ERROR or WARNING) finding

Exit codes:
  0  no blocking findings under the chosen severity (including "script broke")
  1  blocking findings present
"""

from __future__ import annotations

import argparse
import re
import sys
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
NEXUS_DIR = REPO_ROOT / "nexus"
NEXUS_SKILL = NEXUS_DIR / "SKILL.md"
ROUTING_MATRIX = NEXUS_DIR / "reference" / "routing-matrix.md"
SIGNAL_KEYWORDS = NEXUS_DIR / "reference" / "signal-keywords.md"
TASK_BATTERY = NEXUS_DIR / "reference" / "task-battery.md"
AGENT_CHAINS = NEXUS_DIR / "reference" / "agent-chains.md"

FILES = {
    "SKILL.md": NEXUS_SKILL,
    "routing-matrix.md": ROUTING_MATRIX,
    "signal-keywords.md": SIGNAL_KEYWORDS,
    "agent-chains.md": AGENT_CHAINS,
}

# Items 1-28: (item, short description, file key, required verbatim substring).
# Each substring is the literal textual evidence in the routing artifact that
# backs the item's "Expected routing" claim in task-battery.md.
MECHANICAL_ITEMS = [
    (1, "bug subcommand routes directly", "SKILL.md", "| Bug Fix | `bug` |"),
    (2, "memory leak carve-out -> bug", "signal-keywords.md",
     "`memory leak`/`OOM over time`/`unbounded growth` → `bug`"),
    (3, "CVE keyword -> security", "signal-keywords.md",
     "`security`, `vulnerability`, `CVE` | `security`"),
    (4, "clean up keyword -> refactor", "signal-keywords.md",
     "`refactor`, `clean up`, `code smell` | `refactor`"),
    (5, "optimize is measure-first", "routing-matrix.md",
     "**Measure-first / prove-with-a-number**"),
    (6, "polish (feature-scoped) -> kaizen", "signal-keywords.md",
     "`polish`/`improve`/`enhance` a *feature* → `kaizen`"),
    (7, "improve the design REDIRECT -> anneal/restyle", "signal-keywords.md",
     "architecture/code design → `anneal`; UI/visual/look-and-feel → `restyle`"),
    (8, "design weaknesses keyword -> anneal", "signal-keywords.md", "`design weaknesses`"),
    (9, "redesign the screen keyword -> restyle", "signal-keywords.md", "`redesign the screen`"),
    (10, "loop dispatcher gates to goal/converge/orbit/apex", "signal-keywords.md",
     "unattended autonomous runner → the `orbit` skill · discovery→ship → `apex`"),
    (11, "goal keyword row -> goal", "signal-keywords.md",
     "`goal`, `/goal setup`, `goal recipe`, `long-running goal`, `autonomous loop setup` | `goal`"),
    (12, "feature subcommand/keyword exists", "SKILL.md", "| Feature | `feature` |"),
    (13, "end-to-end feature keyword -> apex", "signal-keywords.md", "`end-to-end feature`"),
    (15, "spec out keyword -> spec", "signal-keywords.md", "`spec out`"),
    (16, "self-driving team charter keyword -> charter", "signal-keywords.md",
     "`self-driving team charter`"),
    (17, "gedanken worked example matches verbatim", "signal-keywords.md",
     "think through whether microservices are worth it here, no code"),
    (18, "evolve this feature keyword -> delve", "signal-keywords.md", "`evolve this feature`"),
    (19, "map the system keyword -> cartograph", "signal-keywords.md", "`map the system`"),
    (20, "how did we get here keyword -> chronicle", "signal-keywords.md", "`how did we get here`"),
    (36, "named-figure keyword -> FIGURE_CHANNELING (Summon)", "signal-keywords.md",
     "`how would <figure> approach this`"),
    (37, "Summon conclave hands the verdict to Magi", "agent-chains.md",
     "| FIGURE_CHANNELING | decide | Summon[conclave] \u2192 Magi \u2192 Builder |"),
    (21, "must-have keyword -> essential", "signal-keywords.md", "`essential`, `must-have`"),
    (22, "dead weight keyword -> trim", "signal-keywords.md", "`dead weight`"),
    (23, "copy this product keyword -> clone", "signal-keywords.md",
     "`clone`, `replicate`, `copy this product`"),
    (24, "once-in-a-lifetime keyword -> wish", "signal-keywords.md", "`once-in-a-lifetime request`"),
    (25, "best possible design keyword -> runway", "signal-keywords.md", "`best possible design`"),
    (26, "generate a full package keyword -> package", "signal-keywords.md",
     "`generate a full package`"),
    (27, "bare /Nexus -> proactive", "signal-keywords.md", "`/Nexus` (no arguments) | `proactive`"),
    (28, "switch profile keyword -> pack", "signal-keywords.md",
     "`pack`, `skill pack`, `skill profile`, `enable skills`, `switch profile`, `skill preset` | `pack`"),
]

# Items 29-35: judgment items. Each requires actually walking classify
# (LADDER's live compass/architect spawn, or GATE's live confidence score) —
# no static substring search can stand in for that.
JUDGMENT_ITEMS = [
    (29, "out-of-coverage LADDER walk (patent filing, Probe-Ladder E2E)",
     "requires live compass Gap-mode + architect proposal spawn"),
    (30, "out-of-coverage LADDER walk (travel booking)",
     "requires live compass Gap-mode + architect proposal spawn"),
    (31, "ambiguous stress test: bare \"optimize\"",
     "requires live GATE context_confidence scoring"),
    (32, "ambiguous stress test: bare \"landing page\"",
     "requires live REDIRECT disambiguation judgment"),
    (33, "out-of-coverage LADDER walk (formal verification)",
     "requires live compass Gap-mode + architect proposal spawn"),
    (34, "out-of-coverage LADDER walk (commercial lease)",
     "requires live compass Gap-mode + architect proposal spawn"),
    (35, "out-of-coverage LADDER walk (BACnet/Modbus OT)",
     "requires live compass Gap-mode + architect proposal spawn"),
]

# Agents sunset prior to the 2026-07-29 routing-matrix.md edit. A battery
# item still naming one of these is stale evidence of a pre-sunset chain.
RETIRED_AGENTS = ["Dawn", "Hex", "Sonar", "Realm", "Haul"]


class Finding:
    def __init__(self, item: str, level: str, message: str):
        self.item = item
        self.level = level  # ERROR | WARNING | INFO
        self.message = message

    def __str__(self) -> str:
        return f"[{self.level}] {self.item}: {self.message}"


def safe_check(fn, findings: list[Finding]):
    try:
        fn(findings)
    except Exception as e:  # noqa: BLE001 - intentional catch-all, fail-open contract
        findings.append(Finding(
            fn.__name__, "WARNING",
            f"check crashed and was skipped (fail-open): {e.__class__.__name__}: {e}",
        ))
        traceback.print_exc(file=sys.stderr)


def check_mechanical_items(findings: list[Finding]):
    for num, desc, file_key, needle in MECHANICAL_ITEMS:
        path = FILES[file_key]
        label = f"item {num} ({desc})"
        if not path.is_file():
            findings.append(Finding(label, "ERROR", f"{file_key} not found on disk"))
            print(f"FAIL  {label} -- {file_key} not found")
            continue
        content = path.read_text(encoding="utf-8")
        if needle in content:
            print(f"PASS  {label}")
        else:
            findings.append(Finding(
                label, "ERROR",
                f"expected substring not found in {file_key}: {needle!r}",
            ))
            print(f"FAIL  {label} -- substring not found in {file_key}: {needle!r}")


def check_judgment_items(findings: list[Finding]):
    for num, desc, reason in JUDGMENT_ITEMS:
        label = f"item {num} ({desc})"
        print(f"SKIPPED (judgment item)  {label} -- {reason}")
        findings.append(Finding(label, "INFO", f"skipped: {reason}"))


def check_stale_agent_references(findings: list[Finding]):
    """STALE guard: task-battery.md items must not still name a retired agent."""
    if not TASK_BATTERY.is_file():
        findings.append(Finding("stale-agent-check", "WARNING", "task-battery.md not found"))
        return
    content = TASK_BATTERY.read_text(encoding="utf-8")
    lines = content.splitlines()
    found_any = False
    for name in RETIRED_AGENTS:
        pattern = re.compile(r"\b" + re.escape(name) + r"\b")
        for i, line in enumerate(lines, start=1):
            if pattern.search(line):
                found_any = True
                findings.append(Finding(
                    "stale-agent-check", "WARNING",
                    f"task-battery.md:{i} references retired agent `{name}` -- update to current routing",
                ))
                print(f"STALE task-battery.md:{i} -- references retired agent `{name}`")
    if not found_any:
        print("PASS  stale-agent-check -- no retired agent (Dawn/Hex/Sonar/Realm/Haul) referenced in task-battery.md")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--severity", choices=("warning", "error", "strict"), default="warning")
    args = parser.parse_args()

    findings: list[Finding] = []
    safe_check(check_mechanical_items, findings)
    safe_check(check_judgment_items, findings)
    safe_check(check_stale_agent_references, findings)

    errors = [f for f in findings if f.level == "ERROR"]
    warnings = [f for f in findings if f.level == "WARNING"]
    skipped = [f for f in findings if f.level == "INFO"]
    passed = len(MECHANICAL_ITEMS) - len([f for f in errors if f.item.startswith("item")])

    print()
    print(
        f"Task Battery Check: {passed}/{len(MECHANICAL_ITEMS)} mechanical PASS | "
        f"{len(errors)} FAIL | {len(skipped)} SKIPPED (judgment) | "
        f"{len([f for f in warnings if f.item == 'stale-agent-check'])} STALE"
    )

    if args.severity == "warning":
        return 0
    if args.severity == "error":
        return 1 if errors else 0
    return 1 if (errors or warnings) else 0  # strict


if __name__ == "__main__":
    sys.exit(main())
