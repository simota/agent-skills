# 5 Whys RCA Reference

Purpose: Apply Toyota Production System's 5 Whys — an iterative interrogative technique that drills from a surface symptom to a systemic root cause. Each answer becomes the next "why?". Stop when you reach a process or design cause, never a person.

## Scope Boundary

- **scout `5whys`**: Linear why-chain RCA (this document).
- **scout `fishbone` (elsewhere)**: Categorical multi-factor RCA.
- **scout `timeline` (elsewhere)**: Event sequence reconstruction.
- **scout `bug` / `regression` / `prod` (elsewhere)**: Upstream investigation to obtain symptom.
- **Triage (elsewhere)**: Full incident response incorporating 5 Whys.

## Method

```
SYMPTOM: "Production error rate spiked to 15% at 14:00 UTC"
  Why 1? → Payment service returned 503
  Why 2? → Payment service pool exhausted all connections to DB
  Why 3? → A migration script was running without connection limits
  Why 4? → Migration script merged without code review for resource use
  Why 5? → CI pipeline has no check for DB connection limits in migrations
  ROOT CAUSE: Missing CI guardrail for migration resource limits
```

### Stopping rules

- Stop at systemic cause (process / design / tooling), NOT at a person.
- Stop when the next "why?" crosses an organizational boundary (vendor, customer, regulator).
- Don't force 5 — sometimes 3, sometimes 7. "5" is heuristic.

## Why It Works — and Where It Fails

### Works when
- Failure is a single causal chain.
- Facts are well-established (post-incident with logs).
- Team is psychologically safe to blame process, not person.

### Fails when
- Multi-factor causation (use `fishbone` instead).
- Narrative bias: "the answer I wanted to hear."
- Blaming last person who touched the system.
- Stopping too early (at "operator error" without asking why operator was in position to err).

## Anti-Blame Discipline

Every "why" must land on process, design, tooling, training, or information flow — never a person.

| Bad | Good |
|-----|------|
| "...because Alice forgot to check" | "...because the checklist didn't include that step" |
| "...because the team rushed" | "...because there was no slack in the sprint plan for review" |
| "...because ops missed the alert" | "...because the alert was tuned too sensitive and drowned in noise" |

## Workflow

```
ESTABLISH   →  agreed symptom statement (1 sentence, factual)

ASK         →  "Why did [symptom] happen?"
            →  answer with direct cause (observable, verifiable)

ITERATE     →  for each answer: "Why did [answer] happen?"
            →  track chain in a tree or list
            →  branches OK when one why has multiple direct causes

STOP        →  at systemic cause (process / design / tooling)
            →  at organizational boundary
            →  when further drilling becomes speculative

VERIFY      →  does fixing the root cause prevent this symptom?
            →  does the chain logically reconstruct from root to symptom?

RECOMMEND   →  one fix per root cause, process-focused
            →  define a preventive control
            →  consider: is there detection-gap too?
```

## Output Template

```markdown
## 5 Whys Analysis: [Incident / Bug ID]

### Symptom
[one-sentence factual statement]

### Why-Chain
1. Why [symptom]? → [direct cause 1]
2. Why [direct cause 1]? → [direct cause 2]
3. Why [direct cause 2]? → [direct cause 3]
4. Why [direct cause 3]? → [direct cause 4]
5. Why [direct cause 4]? → [ROOT CAUSE]

### Root Cause
[systemic cause — process / design / tooling]

### Branches (optional)
If any "why" had multiple answers, list the branches and annotate which was pursued and why.

### Verification
- [ ] Does fixing root cause prevent symptom?
- [ ] Is chain reconstructible from root to symptom?
- [ ] Root cause is process, not person

### Preventive Actions
- **Fix**: [specific change to prevent recurrence]
- **Detection upgrade**: [new alert / test / check]
- **Process upgrade**: [review gate / runbook / training]

### Handoffs
- Builder: implement fix
- Mend / Gear: detection/CI upgrade
- Triage: attach to post-mortem
- Lore: record pattern if recurring
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Stopping at "person did X" | Ask one more why: why was the person in position to do X? |
| Forcing exactly 5 | Stop when systemic cause is reached; 3 is OK, 7 is OK |
| Speculating past evidence | Mark speculation; don't log as fact |
| One chain when multiple factors present | Use `fishbone` instead |
| No preventive action identified | RCA without prevention = wasted effort |
| Blame chain runs up the org chart | Re-run with process lens |
| Fix only the deepest cause | Often detection gap also exists; fix both |

## References

- Taiichi Ohno — *Toyota Production System: Beyond Large-Scale Production* (1988)
- Art Byrne — *The Lean Turnaround* (5 Whys in transformation context)
- Don Reinertsen — *The Principles of Product Development Flow*
- Google SRE Book — chapter on postmortems and blameless RCA
- Sidney Dekker — *The Field Guide to Understanding Human Error* (anti-blame discipline)
- John Allspaw — "Blameless PostMortems and a Just Culture" (Etsy blog)
- AWS Well-Architected — OPS 11 (Learn from experience)
