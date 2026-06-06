# Staleness Detection

Purpose: load this when running `gauge staleness` to audit `claude-skills` itself for outdated references. Defines the detection pattern catalog, the false-positive guard rules (so that valid historical citations and migration-guide context are not falsely flagged), and the output format consumed by Gauge's compliance report.

> **Not a code-review tool.** Staleness Detection only catches references that are mechanically out of date — archived OSS, EOL runtimes, superseded version numbers, broken internal `reference/` links, unannotated benchmarks. Conceptual drift, technical-debt scoring, and refactor planning belong to `atlas` / `hex` / `zen`.

## Contents

1. Detection categories
2. Pattern catalog with grep commands
3. False-positive guard rules
4. Severity matrix
5. Output format
6. Self-update protocol (keeping the catalog itself fresh)

## 1. Detection Categories

| ID | Category | What it catches |
|----|----------|-----------------|
| `SD-1` | Archived OSS / repos | References to projects that have been archived or unmaintained |
| `SD-2` | Superseded versions | Version numbers that have been replaced by a newer GA release |
| `SD-3` | EOL runtimes | Language/runtime versions past their end-of-life date |
| `SD-4` | Broken internal links | `reference/xxx.md` pointers that do not resolve |
| `SD-5` | Single-year benchmarks | "as of 2024" / "as of 2025" anchors without a current-year note |
| `SD-6` | Old standards / specs | Standard references where a newer revision exists (e.g. ISO 25010:2011 vs :2023) |
| `SD-7` | Single-CVE windows | CVE-YYYY references where the same threat class has more recent named incidents |
| `SD-8` | Deprecated API names | Vendor API / CLI names that have been renamed or replaced |
| `SD-9` | Drift across skills | Same fact stated with different numbers / versions in two or more skills |
| `SD-10` | Dangling optional pointers | `(if present)` / `(optional)` references that point at files that never existed |

## 2. Pattern Catalog with Grep Commands

Each pattern ships with a grep command and the verification step that must run before flagging.

### SD-1 Archived OSS / Repos

```bash
# Add new archived projects here as the ecosystem changes.
grep -rln -E 'Stack Graphs|SpecFlow\b|Beyla\b(?!.*OBI)' SKILL_GLOBS \
  | xargs -I{} grep -L 'archived\|superseded\|deprecated\|donated' {} 2>/dev/null
```

Verification: a match is a finding only when the surrounding sentence does NOT already note the archived/superseded status. Files that mention the project as part of a migration guide (e.g. `archived → use X`) are not findings.

Known archived as of the catalog's last refresh: `github/stack-graphs` (2025-09-09), `SpecFlow` (stagnant since 2022, fork is Reqnroll), `Beyla` (donated to OpenTelemetry as OBI).

### SD-2 Superseded Versions

```bash
grep -rln -E 'SLSA v1\.0\b|SLSA v1\.1\b|Cosign v2\b|Rekor v1\b|OWASP Top 10:2021' SKILL_GLOBS
```

Verification: same as SD-1 — flag only if the line does not also reference the current version.

### SD-3 EOL Runtimes

EOL dates as of 2026-05 (update via Self-Update Protocol):

| Runtime | EOL date | Action when found alone |
|---------|----------|--------------------------|
| Node.js 18 | 2025-04 | Replace with Node 22 LTS or 24 |
| Node.js 16 | 2023-09 | Hard reject — long past EOL |
| Python 3.9 | 2025-10 | Replace with 3.12 / 3.13 |
| Python 3.10 | 2026-10 | Annotate as approaching EOL |
| Go ≤ 1.21 | 2024-08 (1.22 GA, 1.20 EOL) | Replace with current minor |
| Ruby 3.0 | 2024-03 | Replace with 3.2+ |
| Java 8 | 2025-12 (Oracle premier) | Replace with 17 / 21 LTS |

```bash
grep -rln -E 'Node\.js 18\b|Node 16\b|Python 3\.9\b|Ruby 3\.0\b|Java 8\b' SKILL_GLOBS
```

Verification: matches inside migration-guide context (`shift`, `port`, `quill`, `trail` static-rules) are PASS — they describe the source side of a migration and SHOULD reference the old version. Matches inside min-version baselines (`iOS X+`, `Node Y+`) with the "+" suffix are PASS. Bare references in bootstrap / setup / recommended-runtime tables are FAILS.

### SD-4 Broken Internal Links

```bash
for f in */SKILL.md; do
  skill=$(dirname "$f")
  grep -Eho '`reference/[a-zA-Z0-9_-]+\.md`' "$f" | sed 's/`//g' | sort -u | while read ref; do
    if [ ! -f "$skill/$ref" ]; then
      echo "P0 SD-4 $f: missing $ref"
    fi
  done
done
```

Verification: zero false positives by construction — the file either exists or it does not. P0 because broken links degrade downstream agent navigation.

### SD-5 Single-Year Benchmarks

```bash
grep -rEn '(as of|in) 20(24|25)[^-]' SKILL_GLOBS \
  | grep -vE 'current|present-day|historical|archive|EOL|deprecated|2026'
```

Verification: a benchmark dated 2024/2025 is a finding only when the surrounding paragraph does not explicitly mark it as a historical anchor (e.g. "2025-Q1 historical reference"). The fix is annotation, not deletion.

### SD-6 Old Standards / Specs

```bash
grep -rln -E 'ISO 25010:2011|IEEE 830[^\.]|OWASP Top 10 \(2021\)|WCAG 2\.0\b|WCAG 2\.1\b' SKILL_GLOBS
```

Verification: matches inside change-history notes (`replaces`, `superseded by`, `formerly`) are PASS. Bare references in current-state recommendations are FAILS.

### SD-7 Single-CVE Windows

```bash
grep -rln -E 'CVE-2023-[0-9]+|CVE-2024-[0-9]+' SKILL_GLOBS
```

Verification: most matches will be valid historical references (XZ Utils CVE-2024-3094, tj-actions CVE-2025-30066). Flag only when the same threat class has a more recent named incident the catalog should reference (e.g. Shai-Hulud 3.0 supersedes any 2024 npm-worm reference for the "self-replicating npm worm" claim).

### SD-8 Deprecated API Names

```bash
grep -rln -E 'claude-3-5-sonnet|claude-3-opus|claude-instant|gpt-4-turbo|text-davinci-00[0-9]' SKILL_GLOBS
```

Verification: vendor-managed model identifiers move fast. Flag any bare model-id reference; the fix is to either annotate as historical or replace with a family-level reference (`Claude 4.x family`, `frontier LLM`).

### SD-9 Drift Across Skills

```bash
# Example: same metric quoted with different numbers
grep -rEho '[0-9]+(\.[0-9]+)?%' SKILL_GLOBS \
  | sort | uniq -c | awk '$1 >= 2 {print}'
```

Verification: numbers shared across skills are flagged only when they refer to the same underlying fact stated differently (e.g. one skill says `19.7%` for slopsquat hallucination rate while another says `19%`). Cross-check the source citation; if the citation is the same study, harmonise to a single number.

### SD-10 Dangling Optional Pointers

```bash
grep -rn '(if present)' SKILL_GLOBS
```

Verification: every `(if present)` pointer must actually have a present file. If the pointer always resolves to "not present", remove the pointer rather than leaving it as decorative speculation.

`SKILL_GLOBS` expands to `*/SKILL.md */reference/*.md` from the repo root.

## 3. False-Positive Guard Rules

A staleness scan that flags every legitimate historical citation is worse than no scan at all. Apply these rules **before** emitting any finding:

| Guard | Rule |
|-------|------|
| **Migration-guide context** | `shift` (incl. `detect`/`modernize`/`radar` recipes absorbed from horizon), `port`, `quill`, `trail` (static-rules recipe) legitimately reference legacy versions on the SOURCE side. Skip findings in these skills when the pattern matches "X → Y" or "X to Y" syntax. |
| **Min-version baseline** | "iOS 17+", "Node 22+", "Python 3.12+" are forward-looking floor declarations, not stale. Skip when a `+` immediately follows the version. |
| **Historical anchor** | A version/benchmark annotated with a year and an "as of" / "historical" / "archive" qualifier is annotation-complete. Skip. |
| **Migration-target context** | Pattern `${OLD} → ${NEW}` or `from ${OLD} to ${NEW}` legitimately names the OLD version. Skip the OLD side. |
| **Feature-support boundary** | "Available since Node 18", "iOS 16.4 introduced …" name the lower bound of a feature's availability and are not stale. Skip. |
| **CVE registry reference** | A CVE-YYYY-NNNNN reference inside a security-history paragraph (XZ Utils, Shai-Hulud, tj-actions, etc.) is a permanent record. Skip. |
| **Deliberate cross-skill repetition** | The same fact may legitimately appear in multiple skills if each enforces a different defense layer (chain / sentinel / builder slopsquat checks). Skip SD-9 when source citations match. |

If a pattern triggers but a guard rule applies, log it as `INFO` for the catalog refresh but do not include in the finding list.

## 4. Severity Matrix

| Finding | Severity | Default action |
|---------|----------|----------------|
| SD-4 broken internal link | `P0` | Repair or remove the pointer immediately |
| SD-3 EOL runtime in bootstrap / setup / recommendation | `P0` | Bump to current LTS |
| SD-1 archived OSS without annotation | `P1` | Add "archived; use X" note |
| SD-2 superseded version | `P1` | Update to current GA |
| SD-8 deprecated API name | `P1` | Annotate or generalise |
| SD-6 old standard without revision note | `P2` | Add "superseded by …" note |
| SD-5 single-year benchmark | `P2` | Add "as of YYYY-Q?" annotation |
| SD-10 dangling optional pointer | `P2` | Remove or materialise the file |
| SD-9 drift across skills | `P2` | Harmonise the number; pick one source of truth |
| SD-7 single CVE window | `P3` | Add the more recent incident if applicable |

## 5. Output Format

Gauge's `staleness` recipe emits findings in this YAML envelope so downstream automation (Builder for repair, Guardian for PR composition) can consume directly:

```yaml
staleness_audit:
  audited_at: 2026-05-12T00:00:00Z
  scope: claude-skills/
  catalog_version: "1"
  guard_rules_applied: 7
  summary:
    p0: 0
    p1: 2
    p2: 4
    p3: 1
  findings:
    - id: SD-1
      severity: P1
      file: attest/reference/gherkin-authoring.md
      line: 3
      excerpt: "Cover Cucumber-JVM, Cucumber-JS, SpecFlow (.NET), Behave …"
      pattern: "SpecFlow listed as peer rather than predecessor"
      recommended_fix: "Replace 'SpecFlow (.NET)' with 'Reqnroll (.NET, the active fork of SpecFlow)'"
      verified_archived: true
      source: "reqnroll.net/news/2024/02/from-specflow-to-reqnroll-why-and-how/"
    - id: SD-4
      severity: P0
      file: atelier/SKILL.md
      line: 299
      excerpt: "`reference/onboarding.md` (if present)"
      pattern: "Dangling (if present) pointer; file does not exist"
      recommended_fix: "Remove the pointer or create reference/onboarding.md"
      verified_missing: true
```

Findings without an actionable fix (e.g. a P3 informational note) emit `recommended_fix: null` rather than being omitted entirely — silence and noise are both worse than a "no action needed" entry.

## 6. Self-Update Protocol

The detection catalog itself goes stale. Refresh it every 90 days (or after any major ecosystem event — a new Node LTS, an Anthropic model line transition, an OWASP Top 10 revision) using this protocol:

1. **Read** this file (the current `staleness-detection.md`).
2. **Survey** the ecosystem for newly archived / superseded / EOL items:
   - endoflife.date for runtime EOL
   - GitHub archived-status for projects in the catalog
   - OWASP latest Top 10 / MCP Top 10 / Agentic Skills Top 10 revisions
   - Anthropic / OpenAI / Google model lifecycle pages
3. **Diff** the new findings against the catalog. New ecosystem changes become new entries; resolved ones get retired (date-stamped, not deleted, for audit).
4. **Re-run** `gauge staleness` against the repo with the updated catalog and produce a fresh finding list.
5. **Bump** `catalog_version` and journal the refresh in `.agents/gauge.md`.

The catalog is itself a long-lived spec; treat each refresh as a small ADR rather than an ad-hoc edit.
