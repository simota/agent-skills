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

---

## RCA Methodology Selection

Pick the analysis shape from the failure's structure, not from habit.

| Method | Use when | Recipe |
|--------|----------|--------|
| **5 Whys** | Linear single-chain causation. Iterate until a systemic cause is reached (typically 3-7 levels). | `5whys` |
| **Fishbone (Ishikawa)** | Multiple contributing-factor categories are suspected. | `fishbone` |
| **Fault Tree Analysis** | Safety-critical or data-loss failures — enumerate all failure paths with AND/OR Boolean logic. | — |
| **Causal Graph Synthesis** | Cascading failures across services — build a DAG to identify the critical step and propagation path. | `cascade` |
| **Pareto Analysis** | Fishbone surfaced too many contributing causes; rank by frequency or impact and focus on the vital few. | — |

## TRIAGE Guardrails

- Investigate first, ask last.
- Reports from automated suites (Radar, CI): assess flaky-test probability before deep
  investigation — roughly 30% of CI failures are environmental. Check recent run history
  and known-flaky lists first.
- Generate exactly 3 starting hypotheses: (1) most frequent similar cause in this codebase,
  (2) recent change or regression, (3) pattern-based cause inferred from the report.
- Report incomplete, indirect, urgent, screenshot-only, or missing reproduction detail →
  `vague-report-handling.md`.

## Stall Protocol

- A hypothesis with no supporting evidence after 3 investigative probes → switch to the next.
- All 3 hypotheses exhausted without progress → escalate to Multi-Engine Mode, or request
  additional context from the reporter.
