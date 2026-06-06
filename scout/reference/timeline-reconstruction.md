# Timeline Reconstruction Reference

Purpose: Build a precise, second-by-second event timeline interleaving user actions, system events, alerts, and responder actions. Used for incident post-mortems, regression analysis, and complex bug investigations where ordering matters.

## Scope Boundary

- **scout `timeline`**: Event sequence reconstruction (this document).
- **scout `5whys` / `fishbone` (elsewhere)**: Cause analysis after timeline is built.
- **Triage (elsewhere)**: Owns full incident report; consumes timeline.
- **Trail (elsewhere)**: Git history. Timeline integrates code-deploy events from Trail.
- **Beacon (elsewhere)**: Trace/log/metric source.

## Timeline Structure

Every entry includes:

| Field | Required |
|-------|----------|
| Timestamp (ISO 8601 UTC) | Yes |
| Source (system / human / external) | Yes |
| Actor (service name / responder name / user) | Yes |
| Event (1 line, factual) | Yes |
| Evidence (log link, trace ID, screenshot) | Yes |
| Type (cause / symptom / detection / response / mitigation) | Recommended |

## Multi-Track Layout

```
Time      User      System          Alerts          Responders
─────────────────────────────────────────────────────────────
14:00:12  click→    -               -               -
14:00:13  -         api 200         -               -
14:00:30  -         deploy v2.4.1   -               -
14:00:45  -         pool growing    -               -
14:01:10  -         pool exhausted  PagerDuty fired -
14:01:14  -         api 503         -               oncall ack
14:01:30  -         -               -               oncall: open dashboard
14:02:05  -         -               -               oncall: rollback decision
14:02:18  -         deploy revert   -               -
14:02:42  -         pool recovered  alert resolved  -
14:03:00  -         api 200         -               oncall: confirm green
─────────────────────────────────────────────────────────────
```

## Sources to Stitch

| Source | Type | Notes |
|--------|------|-------|
| Distributed traces | system | High-resolution per-request |
| Application logs | system | Free-form; correlate by trace ID |
| Infrastructure metrics | system | CPU/mem/disk gauges |
| Deploy events | system | Code shipping markers |
| Feature flag changes | system | Often missed; major cause |
| External provider events | external | DNS, CDN, payments status pages |
| User reports | user | First customer report timestamp |
| Alert firing / resolving | system | PagerDuty/Opsgenie history |
| Slack / chat transcripts | human | Responder coordination |
| Runbook executions | human | Action timestamps |
| Approvals / change tickets | human | Pre-incident context |

## Detection / Response Gap Analysis

Two derived metrics from timeline:

| Metric | Definition |
|--------|-----------|
| **Time to Detect (TTD)** | first symptom event → first alert / first user report |
| **Time to Mitigate (TTM)** | first alert → mitigation effective |
| **Time to Resolve (TTR)** | first symptom → fully resolved |
| **Time to Acknowledge (TTA)** | alert fired → responder acknowledges |
| **Time to Communicate (TTC)** | alert → status page update |

Each gap is a separate fix opportunity:
- TTD too long → upgrade alerting or symptom detection.
- TTA too long → on-call rotation or alert routing.
- TTM too long → runbook readiness or rollback automation.
- TTC too long → status-page automation.

## Workflow

```
COLLECT     →  pull all sources for the relevant window
            →  expand window to include pre-event (~30 min before symptom)

NORMALIZE   →  convert all timestamps to UTC
            →  unify timestamp resolution (preferably millisecond)

INTERLEAVE  →  sort by timestamp
            →  multi-track layout: separate columns for user / system / alerts / responders

ANNOTATE    →  mark first symptom, first detection, first mitigation, full resolution
            →  classify each event (cause / symptom / detection / response / mitigation)

GAP-ANALYZE →  compute TTD / TTA / TTM / TTR / TTC
            →  identify gap > expected → improvement candidate

IDENTIFY    →  cause events (deploys, flag changes, external triggers) before symptom
            →  candidate root cause from causes preceding symptom

HANDOFF     →  Triage: full incident report
            →  scout `5whys` / `fishbone`: drill the identified cause
            →  Beacon: detection upgrade per gap
            →  Mend: runbook upgrade per gap
            →  Trail: deeper code archaeology if cause is a deploy
```

## Output Template

```markdown
## Timeline: [Incident ID]

### Window
- **Start**: [UTC timestamp]
- **End**: [UTC timestamp]
- **Sources stitched**: [list]

### Timeline Table
| Time (UTC) | Source | Actor | Event | Type | Evidence |
|------------|--------|-------|-------|------|----------|
| 14:00:12 | user | u/12345 | clicked checkout | — | session-id |
| 14:00:30 | system | deploy | shipped v2.4.1 | cause | commit-sha |
| 14:01:10 | system | api | first 503 returned | symptom | trace-id |
| 14:01:10 | alert | PagerDuty | error_rate > 5% fired | detection | alert-id |
| 14:01:14 | human | oncall@alice | acknowledged | response | pd-link |
| 14:02:05 | human | oncall@alice | initiated rollback | response | runbook-id |
| 14:02:42 | system | api | error rate normalized | mitigation | trace-id |
| 14:03:00 | human | oncall@alice | declared resolved | resolution | slack-link |

### Key Beats
- **Cause**: deploy v2.4.1 at 14:00:30
- **First symptom**: api 503 at 14:01:10 (40s after deploy)
- **First detection**: alert at 14:01:10 (concurrent with first symptom — good)
- **Acknowledgment**: 14:01:14 (4s after alert — good)
- **Mitigation start**: 14:02:05 (51s after ack — review)
- **Effective mitigation**: 14:02:42 (37s after start — good)
- **Resolution**: 14:03:00

### Gap Metrics
- **TTD**: 0s (alert concurrent with symptom)
- **TTA**: 4s
- **TTM**: 1m 32s
- **TTR**: 1m 50s
- **TTC**: not yet measured

### Improvement Candidates
- TTM: 51s from ack to mitigation start — runbook decision time
  → faster decision criteria documented in runbook
- Pre-deploy detection: 0 → upgrade canary monitoring to catch in 5% rollout
- TTC: status-page update missing → add to runbook step 3

### Suspected Cause
deploy v2.4.1 — drill via `5whys` or `fishbone` next.

### Handoffs
- Triage: full post-mortem report
- scout `5whys`: drill cause
- Trail: code archaeology on v2.4.1
- Beacon: detection upgrade
- Mend: runbook upgrade
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Local timezone instead of UTC | Always UTC; convert at presentation |
| Mixing milliseconds and seconds | Pick one resolution; document |
| Single track (all events in one column) | Multi-track separates user / system / alerts / responders |
| Missing pre-event window | Include 30 min before first symptom |
| No event classification | Classify cause/symptom/detection/response/mitigation |
| Skipping responder actions | Responder timing reveals process gaps |
| No evidence links | Each event needs verifiable source |
| Speculation mixed with fact | Mark speculative entries; keep facts clean |
| Status page updates omitted | TTC is a separate metric |
| Treating timeline as final report | Timeline feeds analysis; analysis is separate |

## References

- Google SRE Book — chapter on incident command and post-mortem
- Google SRE Workbook — incident response patterns
- DORA / Accelerate — MTTR metrics and definitions
- John Allspaw — "How Complex Systems Fail" + Etsy postmortem culture
- Sidney Dekker — *The Field Guide to Understanding Human Error*
- Resilience Engineering Association — incident analysis methods
- Atlassian Incident Handbook — timeline structure templates
- AWS Well-Architected — Reliability Pillar (failure analysis)
- O'Reilly — *Site Reliability Engineering* (incident chapters)
- PagerDuty — Incident Response Documentation
