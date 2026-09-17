# Debugging Decision Rules

Read when selecting an RCA method or when a focused investigation stalls.

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
  investigation — check recent run history
  and known-flaky lists first.
- Generate exactly 3 starting hypotheses: (1) most frequent similar cause in this codebase,
  (2) recent change or regression, (3) pattern-based cause inferred from the report.
- Report incomplete, indirect, urgent, screenshot-only, or missing reproduction detail →
  `vague-report-handling.md`.

## Stall Protocol

- A hypothesis with no supporting evidence after 3 investigative probes → switch to the next.
- All 3 hypotheses exhausted without progress → escalate to Multi-Engine Mode, or request
  additional context from the reporter.
