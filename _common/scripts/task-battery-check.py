#!/usr/bin/env python3
"""
Task Battery Check — mechanical checker for the Nexus routing regression
battery (`nexus/reference/task-battery.md`).

The battery has 64 items across two verification tiers (IDs 1-65, with no #14):

  Mechanical items: each item's "Expected routing" column
  claims a specific Recipe/task-type/entry-mode mapping backed by literal text in
  `nexus/reference/routing-matrix.md`, `nexus/reference/signal-keywords.md`,
  or the Recipe registry/default dispatch in `nexus/SKILL.md`. This script asserts that literal
  evidence is still present (verbatim substring match) — it proves the
  routing *artifact* hasn't drifted out from under the battery's claim.
  It does NOT simulate classify's live semantic mapping of the item's
  example sentence to a Recipe — that step still requires an LLM.

  Judgment items 29-35: out-of-coverage LADDER walks (29, 30, 33,
  34, 35) and ambiguous GATE/REDIRECT stress tests (31, 32) can only be
  proven by actually running classify (compass Gap-mode, architect
  proposal, confidence scoring) — no static text search substitutes for
  that. These are reported as `SKIPPED (judgment item)` so the battery's
  coverage stays fully accounted for (no silent caps).

Also runs a lightweight STALE guard: flags any task-battery.md item that
still names a retired agent (Dawn / Hex / Sonar / Realm / Haul, plus the
2026-08-20 consolidation set: Trawl / Grok / Bond / Morph / Mint / Relay /
Riff / Helm / Tempo / Anvil — sunset
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
RECIPES_INDEX = NEXUS_DIR / "reference" / "recipes-index.md"

FILES = {
    "SKILL.md": NEXUS_SKILL,
    "routing-matrix.md": ROUTING_MATRIX,
    "signal-keywords.md": SIGNAL_KEYWORDS,
    "agent-chains.md": AGENT_CHAINS,
    "recipes-index.md": RECIPES_INDEX,
}

# Items 1-28: (item, short description, file key, required verbatim substring).
# Each substring is the literal textual evidence in the routing artifact that
# backs the item's "Expected routing" claim in task-battery.md.
MECHANICAL_ITEMS = [
    (1, "bug subcommand routes directly", "recipes-index.md", "| Bug Fix | `bug` |"),
    (2, "memory leak carve-out -> bug", "signal-keywords.md",
     "`memory leak`/`OOM over time`/`unbounded growth` → `bug`"),
    (3, "CVE keyword -> security", "signal-keywords.md",
     "`security`, `vulnerability`, `CVE` | `security`"),
    (4, "clean up keyword -> refactor", "signal-keywords.md",
     "`refactor`, `clean up`, `code smell` | `refactor`"),
    (5, "optimize is measure-first", "routing-matrix.md",
     "**Measure-first / prove-with-a-number"),
    (6, "polish (feature-scoped) -> kaizen", "signal-keywords.md",
     "`polish`/`improve`/`enhance` a *feature* → `kaizen`"),
    (7, "improve the design REDIRECT -> anneal/restyle", "signal-keywords.md",
     "architecture/code design → `anneal`; UI/visual/look-and-feel → `restyle`"),
    (8, "design weaknesses keyword -> anneal", "signal-keywords.md", "`design weaknesses`"),
    (9, "redesign the screen keyword -> restyle", "signal-keywords.md", "`redesign the screen`"),
    (10, "loop shape-resolves to goal/converge/local-orbit/apex", "signal-keywords.md",
     "unattended runner (scripts/contracts/recovery) → project-local `orbit` when available, otherwise `goal` or `apex` · discovery→ship one-shot → `apex`"),
    (11, "goal keyword row -> goal", "signal-keywords.md",
     "`goal`, `/goal setup`, `goal recipe`, `long-running goal`, `autonomous loop setup` | `goal`"),
    (12, "feature subcommand/keyword exists", "recipes-index.md", "| Feature | `feature` |"),
    (13, "end-to-end feature keyword -> apex", "signal-keywords.md", "`end-to-end feature`"),
    (15, "spec out keyword -> spec", "signal-keywords.md", "`spec out`"),
    (16, "self-driving team charter keyword -> charter", "signal-keywords.md",
     "`self-driving team charter`"),
    (17, "gedanken worked example matches verbatim", "signal-keywords.md",
     "think through whether microservices are worth it here, no code"),
    (18, "evolve this feature keyword -> delve", "signal-keywords.md", "`evolve this feature`"),
    (19, "map the system keyword -> cartograph", "signal-keywords.md", "`map the system`"),
    (20, "how did we get here keyword -> chronicle", "signal-keywords.md", "`how did we get here`"),
    (36, "named-figure keyword -> FIGURE_CHANNELING (Magi)", "signal-keywords.md",
     "`how would <figure> approach this`"),
    (37, "Magi conclave hands the verdict to Magi decide", "agent-chains.md",
     "| FIGURE_CHANNELING | decide | Magi[advisor] \u2192 Magi[decide] \u2192 Builder |"),
    (21, "must-have keyword -> essential", "signal-keywords.md", "`essential`, `must-have`"),
    (22, "dead weight keyword -> trim", "signal-keywords.md", "`dead weight`"),
    (23, "copy this product keyword -> clone", "signal-keywords.md",
     "`clone`, `replicate`, `copy this product`"),
    (24, "once-in-a-lifetime keyword -> wish", "signal-keywords.md", "`once-in-a-lifetime request`"),
    (25, "best possible design keyword -> runway", "signal-keywords.md", "`best possible design`"),
    (26, "generate a full package keyword -> package", "signal-keywords.md",
     "`generate a full package`"),
    (27, "bare /Nexus -> proactive mode", "signal-keywords.md", "`/Nexus` (no arguments) | `proactive mode` (non-Recipe)"),
    (45, "review-to-zero keyword -> quell", "signal-keywords.md",
     "`loop until zero findings`"),
    (46, "behavior-preserving review loop -> quell profile=refactor", "signal-keywords.md",
     "→ `quell profile=refactor`"),
    (47, "design review-to-zero keyword -> burnish", "signal-keywords.md",
     "`loop until zero design findings`"),
    (48, "burnish subcommand registered", "recipes-index.md", "| Burnish | `burnish` |"),
    (49, "mutation-survivor keyword -> whet", "signal-keywords.md",
     "`kill the surviving mutants`"),
    (50, "whet subcommand registered", "recipes-index.md", "| Whet | `whet` |"),
    (51, "scanner sweep -> security mode=to-zero", "signal-keywords.md",
     "`drive vulnerabilities to zero`"),
    (52, "budget sweep -> optimize mode=to-zero", "signal-keywords.md",
     "`clear the performance budget violations`"),
    (53, "docs-contradict-code keyword -> verity", "signal-keywords.md",
     "`the docs contradict the code`"),
    (54, "verity subcommand registered", "recipes-index.md", "| Verity | `verity` |"),
    (55, "spec-code drift splits register-vs-fix (anneal guard)", "signal-keywords.md",
     "**`spec-code drift` splits on register-vs-fix**"),
    (56, "docs-vs-code drift splits scope-vs-record (pdm guard)", "signal-keywords.md",
     "**`docs-vs-code drift` splits on the question asked:**"),
    (57, "ADR-drift keyword -> abide", "signal-keywords.md",
     "`audit the recent changes against the docs`"),
    (58, "abide subcommand registered", "recipes-index.md", "| Abide | `abide` |"),
    (59, "verity-vs-abide splits on the change anchor", "signal-keywords.md",
     "the split from `verity` is the anchor, not the subject"),
    (60, "vague-prompt keyword -> PROMPT_SPEC (Chisel)", "signal-keywords.md",
     "`make this prompt explicit`"),
    (61, "PROMPT_SPEC requires supplied prompt text (over-capture guard)",
     "signal-keywords.md",
     "**Every anchor is prompt-scoped by construction: the object must be supplied prompt text.**"),
    (62, "SPECIFY is gated, not unconditional", "SKILL.md",
     "`SPECIFY?` is gated"),
    (63, "SPECIFY sits between CHAIN_SELECT and EXECUTE", "SKILL.md",
     "CHAIN_SELECT → SPECIFY? → EXECUTE"),
    (64, "SPECIFY runs only after Ask First resolves", "SKILL.md",
     "runs only after every applicable `Ask First` gate has resolved"),
    (65, "product/MVP build routes to deliver", "recipes-index.md",
     "| Deliver | `deliver` |"),
    (28, "switch profile keyword -> pack", "signal-keywords.md",
     "`pack`, `skill pack`, `skill profile`, `enable skills`, `switch profile`, `skill preset` | `pack`"),
]

# Items 29-35: judgment items. Each requires actually walking CLASSIFY
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
RETIRED_AGENTS = ["Dawn", "Hex", "Sonar", "Realm", "Haul",
                  "Trawl", "Grok", "Bond", "Morph", "Mint",
                  "Relay", "Riff", "Helm", "Tempo", "Anvil"]


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
        print(f"PASS  stale-agent-check -- none of {len(RETIRED_AGENTS)} retired agents referenced in task-battery.md")


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
