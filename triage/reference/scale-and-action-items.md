# Incident Zoom Ladder & Action Item Classes

Read when: an incident's cause is being escalated toward an abstraction ("complexity", "human error", "communication problem"), when a postmortem's action items are being drafted, or when the same incident class recurs after a previous fix.

Two failures this file prevents:
1. **Zooming out without returning.** The investigation climbs to an organizational abstraction and stops there. An abstraction is not a control — it cannot be tested, owned, or verified.
2. **Collapsing every action item into "prevention".** A postmortem whose items are all "add a test" / "improve monitoring" leaves containment, detection latency, recovery safety, and decision rights untouched.

---

## 1. Incident Zoom Ladder

Do **not** search for a root cause first. Stop customer impact, then move the magnification deliberately. Each rung has its own questions; skipping a rung is a choice to be stated, not an omission.

| Rung | Questions |
|------|-----------|
| `Runtime` | Which customers and which invariant are affected? What propagation can be stopped right now? Is this data corruption or availability loss — they are not the same incident. |
| `Code / State` | Which inputs, states, and versions trigger it? How did retry, timeout, idempotency, and ordering actually behave? Is there an unrecorded state transition? |
| `Component / Dependency` | Which boundary did the failure cross? Did bulkhead / queue / circuit breaker / backpressure work? Is a shared resource saturated? |
| `System / Platform` | Is there a common cause in deploy, config, identity, network, or observability? Did one control plane reach multiple systems? |
| `Team / Organization` | Were owner, escalation path, decision rights, and expertise present? How much of the recovery time was coordination delay? |
| `Time / Business` | Which signal would have caught this before the customer did? What remains for error budget, support, contracts, and lost opportunity? |

**Order in an active incident:** `Impact → Containment → Zoom In → Zoom Out → Zoom Across → Zoom Through Time → Return to action`.

- `Zoom Across` is the rung most often skipped: find other services, regions, jobs, and clients that share the same assumption. The fix target is rarely one place.
- `Zoom Through Time` asks which *feedback* failed (detection, escalation, mitigation, recovery, learning) — not how many years ago the design decision was made.

### Return to action (mandatory)

Every abstract cause must be walked back down to a control someone can build and verify:

```
"communication problem"
→ schema owner unavailable during the window
→ emergency change path undefined
→ on-call directory + delegated approval rule + game day
```

A postmortem that ends at "organizational culture", "complexity", or "human error" has produced no verifiable intervention. Reject it and descend one more rung.

---

## 2. Action Item Classes

Every action item carries a **class**, an **owner**, a **deadline**, and a **verification**. The class is orthogonal to the existing `P0/P1/P2` priority — priority says *when*, class says *what kind of leverage*.

| Class | Buys | Example |
|-------|------|---------|
| `Containment` | A smaller blast radius next time | Per-tenant rate limit; feature flag on the risky path |
| `Detection` | Knowing sooner | SLI on the customer journey, not on host CPU |
| `Diagnosis` | Narrowing candidate causes faster | Correlation ID propagation; a per-cohort dashboard |
| `Recovery` | Returning safely | Tested rollback for persisted state; a repair job |
| `Prevention` | Removing the failure mechanism | Idempotency key; contract test on the broken assumption |
| `Governance` | Fixing who decides and who owns | Named schema owner; delegated emergency approval |
| `Learning` | Updating assumptions | Correct the runbook's stated dependency SLO; game day |

### Rules

- **"Add a test" is not an action item.** State which failure, over which input space, detected at which stage.
- **Do not file every item as `Prevention`.** If a postmortem has zero `Detection` or `Recovery` items, the next occurrence will take the same time to notice and to undo.
- **`Governance` items are not optional politeness.** If recovery stalled on an approval, absent owner, or missing decision right, that is the highest-leverage item in the list — and it is invisible in a purely technical taxonomy.
- **Attribute each item to the rung that produced it.** An item with no rung usually came from a guess.

---

## 3. Repeat-incident check

When the same class of incident recurs after a fix, the previous intervention was probably applied at the wrong magnification. Before strengthening the same mechanism, write five separate lines:

```
Observed symptom:
Observed at rung:
Likely mechanism and rung:
Intervention rung:
Validation rung and horizon:
```

Common mismatches worth naming explicitly in the postmortem:

- **Local patch for a systemic cause** — the same guard, retry, or exception handler keeps reappearing at different call sites while a shared contract, capacity limit, or missing owner goes untouched. The local guard is correct *as containment*; the mismatch is calling it the permanent fix.
- **Responsibility mismatch** — the team that can trigger a company-wide failure lacks the budget, authority, or change rights to prevent it. Either shrink the blast radius or widen the authority; never move responsibility alone.
- **Observability mismatch** — dashboards are green while a specific tenant, version, or cohort fails. Aggregation level does not match the magnification diagnosis needs.
- **Detection-horizon mismatch** — the validation signal for the fix arrives later than the next occurrence, so the fix is never actually confirmed.

If a repeat incident produces the same class of action items as its predecessor, escalate the postmortem rather than re-filing them.
