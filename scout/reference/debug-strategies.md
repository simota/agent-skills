# Scout Debug Strategy Reference

**Purpose:** First-move debugging guide by error type, reproducibility, or environment difference.
**Read when:** You need the next probe quickly and do not yet know which debugging path is cheapest.

## Contents

- By error type
- By reproducibility
- By environment
- Quick triage flow
- Checklist

## By Error Type

| Error Type | First Step | Tools | Look For |
|------------|------------|-------|----------|
| `TypeError` | Check stack trace | DevTools Console | null or undefined access |
| `NetworkError` | Open network tab | DevTools Network | failed requests, CORS, timeouts |
| `SyntaxError` | Check line number | linter, editor | typos, missing delimiters |
| `ReferenceError` | Check variable scope | DevTools Sources | undefined variables |
| `RangeError` | Check numeric operations | logs, debugger | array bounds, recursion |
| `Custom Error` | Search error message | code search | throw site and error mapping |

## By Reproducibility

| Reproducibility | Strategy | Focus |
|-----------------|----------|-------|
| `Always` | Direct debugging | Step through with debugger |
| `Sometimes (>50%)` | Add targeted logging | Capture state at key points |
| `Rarely (<20%)` | Stress and timing tests | race conditions, edge cases |
| `Never locally` | Environment diff | config, data, versions, infra |

## By Environment

| Works In | Fails In | Investigation Target |
|----------|----------|----------------------|
| Dev | Prod | env vars, endpoints, build config |
| Prod | Dev | data differences, missing mocks |
| Chrome | Firefox/Safari | browser APIs, CSS |
| Fast machine | Slow machine | race conditions, timeouts |
| Fresh install | Existing user | cached data, migrations |

## Quick Triage Flow

1. Can you reproduce locally?
2. Is there an exact error message?
3. Is there a recent change?
4. Is the issue data-dependent or environment-dependent?

If the answer sequence stays unclear, switch to [vague-report-handling.md](vague-report-handling.md).

## Debugging Checklist

- [ ] Exact error message recorded
- [ ] Stack trace captured
- [ ] Environment details noted
- [ ] Minimal reproduction attempted
- [ ] Network and logs checked if relevant
- [ ] Recent commits reviewed
- [ ] Suspected file, line, or condition narrowed down
