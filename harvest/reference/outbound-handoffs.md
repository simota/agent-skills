# Outbound Handoffs

Purpose: Use these payloads when Harvest must pass structured results to another agent without re-describing the same data manually.

## Contents

- Guardian release flow
- Pulse metrics sync
- Canvas visualization
- Zen title analysis
- Sherpa large-PR escalation
- Radar coverage correlation
- Launch release handoff

## Guardian Release Request

```yaml
GUARDIAN_TO_HARVEST_HANDOFF:
  request: "release_notes"
  tag_range:
    from: "v1.1.0"
    to: "v1.2.0"
  version: "1.2.0"
  include_contributors: true
```

## Harvest -> Pulse

```yaml
HARVEST_TO_PULSE_HANDOFF:
  metrics:
    - name: "weekly_merged_prs"
      value: 25
      period: "2026-05-15/2026-05-21"
    - name: "avg_merge_time_hours"
      value: 18.5
    - name: "pr_size_distribution"
      data: { xs: 10, s: 8, m: 5, l: 2 }
    - name: "dora_2025_bands"
      data:
        deployment_frequency: "top_15"
        lead_time_for_changes: "top_15_30"
        failed_deployment_recovery_time: "mid"
        change_failure_rate: "top_15"
        rework_rate: "mid"
    - name: "team_archetype"
      value: "Pragmatic Performers"   # 7-archetype label per DORA 2025
```

## Harvest -> Canvas

```yaml
HARVEST_TO_CANVAS_HANDOFF:
  visualization_type: "trend_chart"
  data:
    - week: "W1"
      merged: 12
      opened: 15
  format: "mermaid_xychart"
```

## Harvest -> Zen

```yaml
HARVEST_TO_ZEN_HANDOFF:
  request: "pr_title_analysis"
  prs:
    - number: 123
      title: "fix bug"
    - number: 124
      title: "feat: add user authentication with OAuth2 support"
  conventions:
    - "Conventional Commits"
    - "50 characters max"
```

## Harvest -> Sherpa

Use when PR size exceeds the split threshold used by your report.

```yaml
HARVEST_TO_SHERPA_HANDOFF:
  request: "large_pr_analysis"
  large_prs:
    - number: 150
      title: "feat: complete user management system"
      additions: 2500
      deletions: 300
      files: 45
  threshold:
    lines: 1000
    files: 20
```

## Harvest -> Radar

```yaml
HARVEST_TO_RADAR_HANDOFF:
  request: "coverage_correlation"
  prs:
    - number: 123
      category: "feat"
      files_changed: ["src/auth.ts", "src/utils.ts"]
      test_files: ["tests/auth.test.ts"]
```

## Harvest -> Launch

```yaml
HARVEST_TO_LAUNCH_HANDOFF:
  type: "release_notes_generated"
  release:
    version: "1.2.0"
  output:
    file: "release-notes-v1.2.0.md"
  summary:
    total_prs: 25
    features: 10
    bugfixes: 12
    breaking_changes: 1
  status: "SUCCESS"
```
