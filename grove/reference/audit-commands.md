# Grove Audit Commands Reference

Purpose: Use this reference when you need quick audit commands, score calculation, baseline handling, or the Sweep handoff template.

## Contents

- Language-specific quick scan commands
- Health Score calculation
- Baseline management
- `GROVE_TO_SWEEP_HANDOFF` template

Quick scan commands, Health Score calculation, baseline management, and handoff templates.

---

## Language-Specific Quick Scan

### TS/JS

```bash
# God Directory (AP-001): >50 files in single dir
find src -maxdepth 1 -type f | wc -l

# Config Soup (AP-003): >10 config files at root
ls -1 *.config.* .*.rc .*.js .*.json .*.yaml 2>/dev/null | wc -l

# Flat Hell (AP-008): >20 src files, 0 subdirs
echo "files: $(find src -maxdepth 1 -type f | wc -l), dirs: $(find src -maxdepth 1 -type d | wc -l)"

# Nested Abyss (AP-009): >6 levels
find . -type d -mindepth 6 -not -path '*/node_modules/*' -not -path '*/.git/*'

# Doc Desert (AP-005): 0 .md in docs/
find docs -name '*.md' 2>/dev/null | wc -l
```

### Python

```bash
# God Directory
find src -maxdepth 1 -name '*.py' | wc -l

# Config Soup
ls -1 pyproject.toml setup.cfg setup.py tox.ini .flake8 .mypy.ini .pylintrc 2>/dev/null | wc -l

# Nested Abyss
find . -type d -mindepth 6 -not -path '*/.venv/*' -not -path '*/__pycache__/*'

# Doc Desert
find docs -name '*.md' -o -name '*.rst' 2>/dev/null | wc -l
```

### Go

```bash
# God Directory (Go uses package dirs, check cmd/ and internal/)
find cmd -maxdepth 1 -type f -name '*.go' 2>/dev/null | wc -l
find internal -maxdepth 1 -type f -name '*.go' 2>/dev/null | wc -l

# Nested Abyss
find . -type d -mindepth 6 -not -path '*/vendor/*'

# Doc Desert
find docs -name '*.md' 2>/dev/null | wc -l
```

### Rust

```bash
# God Directory
find src -maxdepth 1 -name '*.rs' | wc -l

# Nested Abyss
find . -type d -mindepth 6 -not -path '*/target/*'

# Doc Desert
find docs -name '*.md' 2>/dev/null | wc -l
```

### Cross-Language: Repository Size Analysis

```bash
# git-sizer: GitHub-maintained tool for detecting repo scaling risks
# Install: brew install git-sizer (macOS) or go install github.com/github/git-sizer@latest
git-sizer --verbose

# Key metrics and concern thresholds (from git-sizer defaults):
#   Overall repository size: >250 MiB packed → concern
#   Maximum blob size: >10 MiB → concern (large files belong in Git LFS)
#   Maximum tree entries: >2,500 → concern (God Directory signal)
#   Maximum path depth: >10 → concern (Nested Abyss signal)
#   Maximum path length: >200 chars → concern (CI path issues on Windows)

# Quick check without install: count objects and packed size
git count-objects -vH
```

---

## Health Score Calculation

### 5-Axis Measurement

| Axis | Weight | Measurement |
|------|--------|-------------|
| Directory Structure | 25% | Anti-pattern count (AP-001, 008, 009) |
| Doc Completeness | 25% | .md count in docs/, README presence |
| Test Organization | 20% | tests/ structure, co-location pattern |
| Config Hygiene | 15% | Root config count, consolidation |
| Anti-pattern Score | 15% | Total AP findings weighted by severity |

### Scoring Rules

```
Directory Structure (25pt):
  Base: 25
  - AP-001 (God Dir): -8 per instance
  - AP-008 (Flat Hell): -6
  - AP-009 (Nested Abyss): -5 per path
  Min: 0

Doc Completeness (25pt):
  Base: 25
  - No docs/ dir: -15
  - No README.md: -5
  - AP-005 (Doc Desert): -10
  - Missing required subdirs (prd/specs/design): -3 each
  Min: 0

Test Organization (20pt):
  Base: 20
  - AP-002 (Scattered Tests): -10
  - No test directory: -15
  - Missing fixtures/: -3
  Min: 0

Config Hygiene (15pt):
  Base: 15
  - AP-003 (Config Soup): -8
  - AP-004 (Script Chaos): -5
  Min: 0

Anti-pattern Score (15pt):
  Base: 15
  - Critical AP: -5 each
  - High AP: -3 each
  - Medium AP: -1 each
  Min: 0

TOTAL = sum of all axes (0-100)
```

---

## Baseline Management

### AUDIT_BASELINE Format

Record in `.agents/grove.md`:

```yaml
AUDIT_BASELINE:
  date: "YYYY-MM-DD"
  score: 75
  grade: B
  axes:
    directory_structure: 20
    doc_completeness: 18
    test_organization: 15
    config_hygiene: 12
    anti_pattern: 10
  findings:
    - AP-001: 1  # God Directory in src/
    - AP-003: 1  # Config Soup at root
  file_count: 342
  dir_count: 48
```

### Baseline Comparison

```
Delta Report:
  Previous: 75 (B) @ 2025-01-15
  Current:  82 (B) @ 2025-02-15
  Change:   +7 (improved)

  Axis Changes:
    directory_structure: 20 → 23 (+3) — AP-001 resolved
    config_hygiene: 12 → 14 (+2) — 2 configs consolidated
    (others unchanged)

  Resolved: AP-001 (God Directory)
  New:      (none)
  Alert:    (none — no score drop >5)
```

Alert if score drops >5 points between measurements.

---

## GROVE_TO_SWEEP_HANDOFF Template

When Grove audit finds orphaned or unnecessary files, hand off to Sweep:

```yaml
GROVE_TO_SWEEP_HANDOFF:
  source: grove
  date: "YYYY-MM-DD"
  audit_score: 75
  candidates:
    - path: "src/utils/deprecated-helper.ts"
      reason: "structural_orphan"
      evidence: "No directory-level references, isolated from module graph"
      ap_related: "AP-001"
    - path: "config/old-webpack.config.js"
      reason: "config_remnant"
      evidence: "Project migrated to Vite, webpack no longer in devDependencies"
      ap_related: "AP-003"
    - path: "docs/draft-v1.md"
      reason: "orphaned_doc"
      evidence: "Superseded by docs/prd/requirements.md, no inbound links"
      ap_related: "AP-006"
  context:
    project_type: "ts-nextjs"
    total_files: 342
    audit_grade: B
```

Sweep receives this and processes each candidate through its Confidence Score pipeline, adding tool-based verification before proposing deletion.
