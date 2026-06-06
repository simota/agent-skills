# Deprecation Lifecycle Reference

Purpose: Manage the lifecycle of deprecating a public API, library feature, CLI flag, SDK version, or UI affordance — from announcement to safe removal. Designs warn → deprecate → sunset → remove timeline, communication plan, SemVer alignment, and usage-metric gates.

## Scope Boundary

- **horizon `sunset`**: Deprecation lifecycle for existing features (this document).
- **horizon `detect` (elsewhere)**: Identify deprecated third-party dependencies *you consume*. `sunset` manages things you *publish*.
- **horizon `strangler` (elsewhere)**: Full system replacement. Sunset can be the exit stage of a Strangler.
- **Launch (elsewhere)**: SemVer versioning and release gating.
- **Prose (elsewhere)**: User-facing deprecation notice copy.
- **Pulse (elsewhere)**: Usage metrics that gate safe removal.
- **Clause (elsewhere)**: Customer-contract review for SLA-affected deprecations.

## Stages

```
ANNOUNCE → WARN → DEPRECATE → SUNSET → REMOVE
    │        │         │          │         │
    │        │         │          │         └── code and docs removed
    │        │         │          │
    │        │         │          └── feature disabled for most; final cutoff
    │        │         │
    │        │         └── formal deprecation; version-gated behavior
    │        │
    │        └── soft warnings in logs/UI/headers; still works
    │
    └── public notice; no behavior change yet
```

### Stage durations (typical)

| Stage | Minimum | Typical | Use longer for |
|-------|---------|---------|----------------|
| ANNOUNCE → WARN | 0 weeks | 2-4 weeks | Enterprise APIs |
| WARN → DEPRECATE | 1 month | 3 months | SDKs with app-store release cycles |
| DEPRECATE → SUNSET | 3 months | 6-12 months | Enterprise or regulated APIs |
| SUNSET → REMOVE | 3 months | 6 months | Long-tail customers |

**Total from announce to remove**: typically 9-18 months for production APIs. Faster for internal-only or pre-1.0.

## Per-Stage Contract

### ANNOUNCE

- Public notice (blog post / email / docs banner / CHANGELOG).
- Timeline published.
- Replacement path identified.
- No code behavior change.

### WARN

- `Deprecation: true` HTTP response header.
- Deprecation-warning log line per call.
- Docs marked ⚠️ deprecated.
- In-product banner pointing to replacement.
- `@deprecated` annotation in SDK.
- In-IDE squiggle / warning.
- No breaking behavior change.

### DEPRECATE

- Formal SemVer minor release marks the feature deprecated.
- Documentation relegates to "Legacy" section.
- New users cannot opt into it (SDK hides, API returns 403 for new keys, UI hides).
- Existing users still work.
- Metrics dashboard tracks remaining usage.

### SUNSET

- Hard cutoff date in the near future (weeks).
- Repeated customer emails with migration deadline.
- Optional: feature disabled for a % of traffic daily (ramp-down).
- `Sunset:` HTTP response header with RFC 8594 date.
- Final-60-day, final-30-day, final-7-day, final-24-hour reminders.

### REMOVE

- Major SemVer bump (for libraries) or scheduled API breaking-change window.
- Code removed.
- Database rows archived.
- Docs moved to "Removed" section with gravestone linking to replacement.
- Monitoring alert if any call still reaches the removed endpoint (404 expected).

## HTTP Headers (RFC 8594 / IETF)

```
Deprecation: Wed, 11 Nov 2026 23:59:59 GMT
Sunset: Wed, 11 May 2027 23:59:59 GMT
Link: <https://api.example.com/v2/users>; rel="successor-version"
Link: <https://example.com/deprecations/v1-users>; rel="deprecation"
```

Emit `Deprecation` in the WARN stage; add `Sunset` at the DEPRECATE stage with the cutoff date.

## Usage-Metric Gate for Safe Removal

Before REMOVE, require the usage-metric gate (via Pulse):

| Metric | Target before REMOVE |
|--------|---------------------|
| Daily active unique callers | 0 for ≥ 7 consecutive days |
| Total calls last 30 days | < threshold (e.g., < 100 internal-only) |
| Enterprise customers using it | 0 (or explicitly opted-out with contract modification) |
| Time since SUNSET announcement | ≥ minimum per SLA |

If any gate fails, extend the SUNSET period and re-notify. Do not remove until all gates pass.

## Communication Plan

Per deprecation, the communication plan includes:

| Channel | When |
|---------|------|
| Docs banner | ANNOUNCE onward |
| CHANGELOG entry | ANNOUNCE (with full timeline) |
| Email to affected customers | ANNOUNCE, DEPRECATE, SUNSET -60d, -30d, -7d, -24h |
| In-product banner | WARN onward |
| Status page entry | SUNSET (link from main banner) |
| Support macro | DEPRECATE onward |
| SDK release notes | Each stage |
| Conference talk / public session | Major changes only |

Customer segmentation:
- **Enterprise / SLA customers**: direct account manager, customized timeline if contractually required.
- **Paid tier**: email + in-product + SDK warning.
- **Free tier**: docs + in-product banner + automated email.
- **Internal services**: Slack + internal wiki + automated PR notifications.

## SemVer Alignment (for libraries)

| Stage | SemVer event |
|-------|--------------|
| ANNOUNCE | No change |
| WARN | Minor release: add `@deprecated` annotation |
| DEPRECATE | Minor release: keep working, warn loudly |
| SUNSET | Minor release: feature disabled by default, opt-in flag |
| REMOVE | Major release: feature gone |

For APIs without SemVer (internal tools), use dated API versions and route by version header.

## One-Way Deprecations

Some deprecations are one-way (once removed, hard to restore):

- Public API endpoint with unique URL.
- Database column after hard-delete.
- SDK function with unique name.
- UI affordance that users have trained habits around.

For one-way deprecations, require:
1. Sign-off from stakeholders (product, support, legal if SLA).
2. Snapshot / archive of behavior for possible reference.
3. Customer migration verification (calls on new path > calls on old path for 30+ days).
4. Observability post-removal to detect calls to the removed endpoint and alert.

## Output Template

```markdown
## Deprecation Plan: [Feature Name]

### Context
- **What is deprecated**: [specific endpoint / function / UI / flag]
- **Why**: [security / performance / design evolution / replaced by X]
- **Replacement**: [link to new path]
- **Affected customers**: [segment breakdown]

### Timeline
| Stage | Date | Duration | Gate for next |
|-------|------|----------|--------------|
| ANNOUNCE | [date] | [2-4 weeks] | Public notice shipped |
| WARN | [date] | [3 months] | All channels warned |
| DEPRECATE | [date] | [6-12 months] | Usage < threshold |
| SUNSET | [date] | [3-6 months] | All gates pass |
| REMOVE | [date] | — | Confirmed zero calls |

### Per-Stage Actions
- ANNOUNCE: [blog post, CHANGELOG, docs banner]
- WARN: [Deprecation header, SDK @deprecated, in-product banner]
- DEPRECATE: [SemVer minor, docs to Legacy section, metric dashboard]
- SUNSET: [Sunset header, final-60/30/7/24h reminders]
- REMOVE: [SemVer major, code + DB cleanup, post-removal monitor]

### Usage-Metric Gates (Pulse)
- [ ] Daily unique callers = 0 for ≥ 7 days
- [ ] 30-day call volume < [threshold]
- [ ] Enterprise customers = 0
- [ ] SLA timelines met

### Communication Plan
| Channel | ANNOUNCE | WARN | DEPRECATE | SUNSET-60 | SUNSET-30 | SUNSET-7 | SUNSET-24h | REMOVE |
|---------|---------|------|-----------|-----------|-----------|----------|------------|--------|
| Docs | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ (gravestone) |
| Email | ✓ | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| In-product banner | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| Status page | — | — | — | — | — | ✓ | ✓ | ✓ |

### SemVer / Versioning
- Library: [version number changes]
- API: [version header policy]

### Post-Removal Monitoring
- Alert if any call reaches removed endpoint
- Archive / snapshot location: [path]
- Runbook: [link — what to do if someone reports regression]

### Handoffs
- Prose: notification copy for each channel (notification-copy reference).
- Launch: SemVer gating and release cadence.
- Pulse: usage-metric dashboard and gate alerts.
- Clause: customer-contract review if SLA-affected.
- Scribe: migration guide authoring.
- Beacon: post-removal monitoring.
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Removing without WARN stage | Always go through WARN first |
| No replacement path communicated | Block ANNOUNCE until replacement exists and works |
| SUNSET → REMOVE same day | Minimum gap; reminders must go out |
| Silent removal (patch release) | Major SemVer bump for any removal |
| No usage metrics | Cannot know if safe to remove; add metrics first |
| One-way deprecation without sign-off | Require approval gate |
| Removing during support holiday | Schedule REMOVE on a weekday with on-call coverage |
| Customer emails only at REMOVE | Distribute reminders across SUNSET stage |
| Ignoring SLA contracts | Clause review for enterprise customers |

## Deliverable Contract

When `sunset` completes, emit:

- **Timeline** with per-stage dates and durations.
- **Per-stage actions** (what ships in each stage).
- **Usage-metric gates** (Pulse dashboard) with pass thresholds.
- **Communication plan matrix** (channel × stage).
- **SemVer / versioning strategy**.
- **Post-removal monitoring plan**.
- **One-way approval gate** if applicable.
- **Handoffs**: Prose, Launch, Pulse, Clause, Scribe, Beacon.

## References

- RFC 8594 — The `Sunset` HTTP Header Field
- IETF draft — `Deprecation` HTTP header
- Stripe API versioning policy
- GitHub API deprecation policy
- Google Cloud deprecation policy
- Semantic Versioning 2.0.0
- Martin Fowler — "ToleranceReadingService" / evolutionary APIs
- ThoughtWorks Tech Radar — deprecation patterns
