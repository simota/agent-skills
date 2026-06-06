# Error Handling

Purpose: Use this reference when Harvest hits authentication, rate-limit, network, API, permission, or partial-data failures.

## Contents

- Error categories
- Preflight checks
- Recovery rules
- Graceful degradation
- Nexus and escalation formats

## Error Categories

| Category | Typical errors | Recoverability | Priority |
|----------|----------------|----------------|----------|
| Authentication | `401`, expired token | High | `P0` |
| Rate limiting | `403`, quota exhausted | High | `P0` |
| Network | timeout, DNS failure | Medium | `P1` |
| API | `500`, `502`, malformed upstream response | Medium | `P1` |
| Data | invalid JSON, missing fields | Partial | `P2` |
| Permission | `403`, `404` on repo access | Low | `P3` |

## Preflight Checks

Run before collection when the request is large or time-sensitive:

```bash
command -v gh
gh auth status
gh repo view --json nameWithOwner
gh api rate_limit --jq '.resources.core.remaining'
```

## Recovery Rules

| Failure | Response |
|---------|----------|
| Authentication | Stop and return `BLOCKED`; recommend `gh auth login` |
| Rate limit low (`<100`) | Warn, prefer cache, or narrow scope |
| Rate limit exhausted | Wait for reset if `< 3600s`; otherwise return partial/blocking output |
| Secondary rate limit hit (403 with `retry-after`) | Exponential backoff with jitter; never poll continuously — GitHub may ban integrations that keep hammering past secondary limits (`docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api`) |
| Network/API transient error | Retry up to `3` attempts with backoff `5s -> 10s -> 20s` |
| Full-field fetch fails | Retry with a minimal field set |
| Repo permission issue | Stop; do not guess repository visibility or access |

## Graceful Degradation

If partial data is still usable, report the degradation explicitly.

| Available data | Degradation level | Report quality |
|----------------|-------------------|----------------|
| Full fields | `FULL` | `100%` |
| Missing additions/deletions | `NO_STATS` | `80%` |
| Missing dates | `NO_DATES` | `60%` |
| Missing author | `NO_AUTHOR` | `50%` |
| Only PR numbers/titles | `MINIMAL` | `20%` |
| No usable data | `FAILED` | `0%` |

Rules:
- Never fabricate missing fields.
- State the degradation level in the report body.
- If data quality drops below decision usefulness, stop instead of over-polishing.

## `_STEP_COMPLETE:` Patterns

Use the same status vocabulary as the main skill.

```yaml
_STEP_COMPLETE:
  Agent: Harvest
  Status: BLOCKED
  Output: Authentication failed - GitHub CLI not authenticated
  Next: USER_ACTION
```

```yaml
_STEP_COMPLETE:
  Agent: Harvest
  Status: PARTIAL
  Output: Collected partial PR data after rate limiting
  Next: RETRY_OR_REPORT_WITH_CAVEAT
```

## `## NEXUS_HANDOFF` Failure Notes

Include these fields when failure details materially affect downstream work:

- `Error Code`
- `Impact`
- `Partial Data Available`
- `Recovery Recommendation`

## Escalation

Use this payload when the failure blocks reporting at the workflow level:

```yaml
HARVEST_TO_TRIAGE_ESCALATION:
  trigger: "critical_error"
  error:
    code: "AUTH_REVOKED"
    message: "GitHub token has been revoked"
  context:
    task: "Weekly PR report generation"
    repository: "org/project"
    user_impact: "All automated reports blocked"
  recommended_actions:
    - "Re-authenticate with 'gh auth login'"
    - "Verify token permissions"
    - "Check for security alerts"
```
