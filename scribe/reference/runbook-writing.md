# Runbook Writing Reference

Purpose: Author an operational runbook — the document an on-call responder or an automated remediation agent follows to take a known symptom from detection to verified recovery. A runbook is an executable-by-humans-or-agents artifact: prescriptive, idempotent, and authorized.

## Scope Boundary

- **Scribe `runbook`**: AUTHORS the runbook document itself. The output is a committed, reviewed, versioned artifact under `docs/runbooks/`.
- **Triage (elsewhere)**: diagnoses live incidents and identifies which runbook applies. Does not author runbooks; consumes them.
- **Mend (elsewhere)**: executes runbooks for automated remediation with safety-tier classification, staged verification, and rollback. Does not author runbooks; consumes them.

If the question is "what happened and which runbook applies?" → `Triage`. If the question is "execute the recovery now" → `Mend`. If the question is "we keep hitting this — document the recovery so next time is faster" → Scribe `runbook`.

## Workflow

```
UNDERSTAND  ->  confirm the failure mode is reproducible or has been seen ≥2 times
            ->  gather the postmortem or incident ticket that motivated this runbook
            ->  identify the authorized-executor set (who MAY run this)

STRUCTURE   ->  assign runbook ID (RB-NNNN) and place under docs/runbooks/
            ->  decide safety tier: SAFE (idempotent, reversible) / GUARDED (needs approval) / DESTRUCTIVE (data loss risk)

DRAFT       ->  Symptom: the observable signal (alert name, log pattern, user report)
            ->  Pre-condition: required state before execution (e.g., primary is up, backup completed < 1h ago)
            ->  Authorization: who MAY execute (role, on-call rotation, approval gate)
            ->  Triage: binary checks that confirm this is the right runbook
            ->  Recover: numbered, idempotent steps. Each step MUST state expected output
            ->  Verify: success signals (metric returns to baseline, synthetic probe green)
            ->  Rollback: how to undo if recovery fails mid-way
            ->  Root-cause link: reference the postmortem or ADR

REVIEW      ->  every step is idempotent — rerunning MUST NOT worsen state
            ->  every command includes expected output or exit code
            ->  escalation path is explicit (who to page if step N fails)
            ->  no step requires tribal knowledge not in the doc

FINALIZE    ->  commit; link from alert definition (Beacon) and Mend registry
            ->  schedule a quarterly drill or chaos injection to verify the runbook still works
```

## Required Sections

```markdown
# RB-0042: Recover from Redis replica lag > 30s

- Owner: @sre-team
- Safety Tier: GUARDED
- Last Verified: 2026-04-10 (drill)
- Related: POSTMORTEM-2026-03-11, ADR-0018

## Symptom
Alert `redis_replica_lag_seconds > 30` fires for ≥ 5 minutes.

## Pre-condition
- Primary Redis is reachable.
- No ongoing failover.

## Authorization
On-call SRE MAY execute steps 1-4. Step 5 (replica rebuild) SHOULD be approved by the storage owner.

## Triage
1. Confirm primary is healthy: `redis-cli -h $PRIMARY PING` returns `PONG`.
2. Confirm lag is on one replica, not all.

## Recover
1. ...  (expected output: ...)
2. ...

## Verify
- `redis_replica_lag_seconds` returns below 5s within 10 minutes.
- Synthetic read against replica succeeds.

## Rollback
If step 3 fails, fail the replica out of the read pool via ... ; do NOT rerun step 3.

## Escalation
If step 2 did not reduce lag within 15 minutes, page @storage-owner.
```

## Idempotency Rule

Every step in Recover MUST be safe to rerun. Rationale: on-call responders retry under stress; automated remediation (Mend) retries on ambiguous failure. Steps that are not naturally idempotent require an explicit guard:

- Bad: `kubectl delete pod foo-123` (pod name changes on restart).
- Good: `kubectl delete pod -l app=foo,role=stuck --field-selector status.phase=Pending`.

If a step cannot be made idempotent, mark it `NON-IDEMPOTENT` and route it through the Rollback section instead of Recover.

## Authorization Levels

| Tier | Who MAY execute | Gate |
|------|-----------------|------|
| SAFE | Any on-call engineer, Mend autorun | None |
| GUARDED | On-call SRE, Mend with approval token | Second-person confirm for high-blast-radius |
| DESTRUCTIVE | Storage owner or higher | Written approval in incident channel; dual-control required |

Use RFC 2119 keywords (MUST / SHOULD / MAY) in Authorization to leave no ambiguity.

## Anti-Patterns

- "Check the dashboard and use your judgment" — not a runbook; that is tribal knowledge. Runbooks are binary.
- No expected output on a step — responder cannot tell success from partial failure.
- Commands containing placeholders like `<YOUR_CLUSTER>` without a resolution table. Provide the lookup or a script.
- Runbook that has never been drilled. Untested runbooks are fiction; schedule chaos drills or tabletop exercises.
- Mixing incident response and root-cause investigation into one document. Runbook = recovery. RCA = postmortem. Link them, do not merge.
- Missing rollback. Every real runbook has a failure mode of the recovery itself.

## Handoff

- From `Triage`: postmortem or incident identifies a recurring failure; Triage hands off the symptom + recovery steps for Scribe to canonicalize.
- From `Beacon`: new alert definition needs a runbook before going live.
- To `Mend`: once committed, the runbook ID is registered with Mend for automated or assisted execution.
- To `Triage`: the runbook becomes the reference consulted during next occurrence.
- To `Sherpa`: if authoring the runbook reveals tooling gaps, decompose the fix into tasks.

## Citations

- Google SRE Workbook, Ch. 9 "Incident Response" — runbook structure.
- RFC 2119 — MUST / SHOULD / MAY for authorization language.
- NIST SP 800-61r2 — computer security incident handling, applicable to security runbooks.
- ITIL 4 — standard operating procedure (SOP) alignment.
