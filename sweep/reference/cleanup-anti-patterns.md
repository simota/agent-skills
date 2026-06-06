# Cleanup Anti-Patterns

Purpose: safety guardrails against destructive or low-signal cleanup behavior.

## Contents

1. Process anti-patterns
2. Misjudgment anti-patterns
3. Organizational anti-patterns
4. Pre-delete checklist
5. Zombie code handling

## Process Anti-Patterns

| ID | Anti-Pattern | Why It Is Dangerous | Sweep Response |
|----|--------------|---------------------|----------------|
| `ANTI-001` | Big Bang Cleanup | Regression source becomes hard to isolate; rollback is hard | Split by category and keep deletions reviewable |
| `ANTI-002` | Blind Trust in Tools | Static tools miss dynamic and convention-based references | Treat tool output as evidence only |
| `ANTI-003` | No Backup Deletion | Revert becomes messy, especially with lockfiles | Always create a backup branch first |
| `ANTI-004` | Cleanup Without Tests | Hidden dependencies break builds and runtime | Run build/tests before and after cleanup |

## Misjudgment Anti-Patterns

| ID | Anti-Pattern | Why It Is Dangerous | Sweep Response |
|----|--------------|---------------------|----------------|
| `ANTI-005` | Age-Based Deletion | Stable code can look inactive | Age is only one factor in confidence scoring |
| `ANTI-006` | Comment Out Instead of Delete | Dead code accumulates and confuses readers | Prefer deletion and rely on git history |
| `ANTI-007` | Ignoring Dynamic References | Static analysis misses runtime loading | Apply false-positive guards and string scans |
| `ANTI-008` | Blind Config Removal | CI, hooks, IDEs, or external tools may still depend on it | Ask first and verify full tool ownership |

## Organizational Anti-Patterns

| ID | Anti-Pattern | Why It Is Dangerous | Sweep Response |
|----|--------------|---------------------|----------------|
| `ANTI-009` | One-Off Cleanup Project | Dead code returns immediately | Use Maintenance Mode continuously |
| `ANTI-010` | No Cleanup Ownership | Candidates linger without decisions | Route by owners, PR flow, or partner agents |

## Safe Deletion Checklist

```text
□ Confidence score is at least 50
□ Two or more signals support the candidate when possible
□ Dynamic references were checked
□ Framework convention files were ruled out
□ CI/CD and config references were checked
□ Recent modification (<30 days) was reviewed
□ Backup branch exists
□ Post-delete build/test plan exists
□ Documentation impact is known
```

## Zombie Code

Zombie code is dormant code that can become active through a flag, config flip, or runtime path change.

Treat it with higher severity:
- report it separately
- check feature-flag TTLs and runtime evidence
- prefer phased removal and explicit confirmation
