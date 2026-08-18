# Triage Response Workflow Reference

Detailed incident response phases and templates.

Purpose: Read this when Triage needs phase-by-phase operating detail, containment or mitigation options, verification checklists, or post-resolution capture rules.

Contents:
- `Phase 1: DETECT & CLASSIFY`: first-5-minute acknowledgement and initial report
- `Phase 2: ASSESS & CONTAIN`: containment options and impact framing
- `Phase 3: INVESTIGATE & MITIGATE`: handoff sequence, parallel execution, and mitigation comparison
- `Phase 4: RESOLVE & VERIFY`: recovery checklist and extended verification
- `Phase 5: LEARN & IMPROVE`: deadlines, external report decisions, and knowledge capture

## Phase 1: DETECT & CLASSIFY (First 5 minutes)

**Immediate Actions:**
1. Acknowledge the incident
2. Gather initial information
3. Classify severity
4. Notify stakeholders (if SEV1/SEV2)

### Initial Incident Report Template

```markdown
## Initial Incident Report

**Reported By:** [name/system]
**Reported At:** [YYYY-MM-DD HH:MM UTC]
**Initial Description:** [what was reported]

**Symptoms:**
- [ ] Error messages: [exact text]
- [ ] Affected URL/endpoint: [path]
- [ ] Error rate: [X% of requests]
- [ ] Latency: [current vs baseline]
- [ ] User reports: [count/nature]

**Environment:**
- [ ] Production / Staging / Dev
- [ ] Region: [if applicable]
- [ ] Version: [deployed version]
```

---

## Phase 2: ASSESS & CONTAIN (Minutes 5-15)

**Impact Assessment:**
- Determine scope of affected users/features
- Identify potential data impact
- Check for cascading failures
- Document timeline of events

### Containment Options

| Action | When to Use | Risk |
|--------|-------------|------|
| Feature flag disable | Feature-specific issue | Functionality loss |
| Rollback deploy | Recent deploy caused issue | May lose good changes |
| Scale up resources | Load-related issue | Cost increase |
| Block traffic | DDoS/abuse | Legitimate users blocked |
| Failover to backup | Primary system failure | Data sync lag |
| Disable integration | Third-party issue | Feature degradation |

---

## Phase 3: INVESTIGATE & MITIGATE (Minutes 15-60)

**Coordinate Investigation:**
- Hand off to Scout for root cause analysis
- Request Lens for evidence collection
- Request Beacon for monitoring data (if available)

### Handoff Sequence (Standard Flow)

```
1. Triage → Scout   : request RCA with symptoms, timeline, and initial hypotheses
2. Scout → Triage   : return RCA with root cause, fix location, and recommended approach
3. Triage → Builder : request remediation with Scout findings and urgency
4. Builder → Radar  : request verification with fix details and regression scope
5. Radar → Triage   : return verification results and coverage impact
6. Triage → Close   : close the incident after verification completes
```

**Parallel Execution (When applicable):**
- Lens can capture evidence while Scout is running RCA.
- If the cause is already clear, Builder may start remediation before Scout fully completes when Triage approves.

### AI SRE Co-pilot in Phase 3 (2026)

When an AI SRE co-pilot is running (Bits AI SRE, Rootly AI SRE, incident.io AI SRE), step 1 changes shape: the agent has *already* started parallel investigation from the moment of detection. Triage's job is not to wait for Scout but to **validate and route** the agent's findings.

| Step | Triage action | What changes when AI SRE is on |
|------|---------------|----------------------------------|
| 1 | Read agent's top-3 candidate causes with confidence | Skip Scout if confidence ≥ `high` on a candidate that matches a known runbook; otherwise still escalate to Scout for human RCA |
| 2 | Verify the agent's correlated metrics / logs / traces / deploys are real | Reject any candidate that cannot be backed by a specific query — hallucinated correlations get filtered here, not in the postmortem |
| 3 | Route to Mend if the agent proposes a runbook match | The runbook still passes through Mend's safety-tier classification — the AI agent's confidence does not bypass T3 / T4 approval gates |
| 4 | Route to Builder if the agent proposes a code fix | The agent's draft PR is reviewed by a human; the PR-as-safety-gate rule remains in force (see `mend/reference/safety-model.md`) |

Hard rules:

- **Triage owns the routing decision**, not the AI agent. The agent recommends; Triage accepts, modifies, or escalates to Scout for human RCA.
- **No autonomous remediation in SEV1 / SEV2.** Even when the agent's confidence is high, a named human owner approves every state-changing action.
- **Investigation transcript is captured as evidence.** Same audit-trail rule as in `first-response.md` — the transcript becomes input to the AI-assisted postmortem draft.

Reported gains in 2026 published case studies: MTTR reductions of `~40-70%` are typical when the AI co-pilot is wired into a mature Triage process; the same tools deliver near-zero improvement (and sometimes regressions) when the Triage process itself is loose, because the agent amplifies whatever discipline it is given.

### Mitigation Options Template

```markdown
## Mitigation Options

| Option | Impact | Reversibility | Time to Implement |
|--------|--------|---------------|-------------------|
| [Option 1] | [impact] | [easy/medium/hard] | [X min] |
| [Option 2] | [impact] | [easy/medium/hard] | [X min] |
| [Option 3] | [impact] | [easy/medium/hard] | [X min] |

**Recommended:** [Option] because [reason]
```

---

## Phase 4: RESOLVE & VERIFY (Variable)

### Resolution Checklist

- [ ] Root cause identified (via Scout)
- [ ] Fix implemented (via Builder)
- [ ] Fix deployed to production
- [ ] Monitoring shows recovery
- [ ] User-facing symptoms resolved
- [ ] No regression in other areas

### Resolution Verification Template

```markdown
## Resolution Verification

**Service Health:**
- [ ] Error rate returned to baseline: [X%]
- [ ] Latency returned to baseline: [X ms]
- [ ] Success rate recovered: [X%]

**User Verification:**
- [ ] Test account can complete affected flow
- [ ] No new error reports
- [ ] Affected users notified (if applicable)

**Monitoring:**
- [ ] Alerts cleared
- [ ] Dashboards show normal
- [ ] No secondary issues detected

**Extended Verification (SEV1/SEV2):**
- [ ] Primary user flow tested end-to-end
- [ ] Data integrity verified (no loss/corruption)
- [ ] Related systems verified (no cascading impact)
- [ ] 30-minute observation period completed without recurrence
- [ ] Rollback plan confirmed still viable
```

---

## Phase 5: LEARN & IMPROVE (Post-resolution)

### Postmortem Timeline

| Severity | Deadline |
|----------|----------|
| SEV1 | Within 24 hours |
| SEV2 | Within 48 hours |
| SEV3/4 | Within 1 week (if warranted) |

### External Incident Report Decision

| Report Type | Audience | Timing |
|-------------|----------|--------|
| Detailed Report | Customers, Partners, Executives | After SEV1/SEV2 resolution (Recommended) |
| Summary Report | When quick sharing is needed | On request |
| None | Internal impact only | SEV3/SEV4 |

### Knowledge Capture (Required for SEV1/SEV2)

After postmortem completion, add learnings to `.agents/PROJECT.md`:

```markdown
| YYYY-MM-DD | Triage | Postmortem: [incident title] | Root cause: [brief] | Prevention: [action item] |
```

Also update `.agents/triage.md` if:
- New incident pattern discovered
- Effective mitigation strategy found
- Runbook gap identified


## Agent-Origin Incidents

Phases 1-5 assume a production system misbehaved. These incidents differ: the failing component is the
**agent harness itself**, the blast radius is often outside the monitored system, and the usual first move —
ask the agent what happened — is compromised, because the agent's own context may be the contaminated
evidence.

**Three rules override the standard flow.**

1. **Freeze before you ask.** The first action is stopping effects — writes, deploys, external sends, and
   durable-memory writes — not sending another prompt. An agent asked to explain itself keeps acting.
2. **Preserve two sides separately.** Capture the *context* side (transcript, tool calls, memory contents,
   loaded instructions) and the *reality* side (repository revision, external state, logs, artifacts) as
   independent evidence. Reconciling them is the investigation; merging them destroys it.
3. **Severity is not token count.** Grade by side effects reached, propagation, recoverability, and whether a
   security boundary was crossed — not by how large or how long the run was.

### Runbooks

| # | Incident | Trigger | Immediate actions | Recovery / prevention |
|---|----------|---------|-------------------|----------------------|
| `A1` | **Secret exposure** | token-shaped value in a transcript; `.env` in an artifact; internal data sent to an external tool; session cookie in a browser trace | stop the session → cut network egress → revoke and rotate the credential → restrict artifact/log access → preserve timestamp, session ID, tool calls, destinations → escalate to a named owner | fix the mount and permission, not just the context exclusion; move to a broker / short-lived credential; re-test the same path adversarially |
| `A2` | **Compromised or malicious MCP server** | unknown network destination; tool schema changed without notice; a read-only tool wrote; checksum mismatch; operation outside credential scope | disable the server in the catalog → kill process and connections → revoke credentials → preserve package, version, digest, source → reconcile every tool call against observed side effects | pin version/digest, split read/write credentials, enforce server-side, allowlist destinations, alert on tool-schema diff, test removal → `chain` §6b |
| `A3` | **Prompt injection reaching an external write** | after reading untrusted content, the agent attempts an issue comment, email, upload, or cloud API call | deny unless the *trusted task intent* required that write; if required, surface destination + payload + data class before approving; deny or escalate when the payload carries a higher data class | record: untrusted source, context envelope, proposed payload, destination, permission decision, tool-policy result → `_common/WEB_FETCH_SAFETY.md` |
| `A4` | **Push to the wrong branch** | commit on a protected or unintended branch | halt merge/deploy on protected branches → record SHA and actor → check what workflows the push triggered → if secrets are involved, escalate to `A1` → preserve artifacts *before* revert or branch deletion | usual root causes: over-scoped token, no branch allowlist, wrong working directory, push treated as the same tier as workspace write. Fix with PR-only output, protected branches, short-lived tokens, branch patterns |
| `A5` | **Cloud/remote run differs from local** | reproduces in one environment only | diff the environment manifest **first** — revision, submodules/LFS, OS/arch, runtime versions, lockfile, system packages, env vars, network, secrets, timezone/locale, filesystem case sensitivity, cache state | never patch environment drift by adding prompt text; fix the manifest and re-verify |
| `A6` | **Context poisoning / stale memory** | repeats a deprecated command; treats a removed API as current; an old exception overrides current policy; personal data or secrets persist in memory | export persistent memory and restrict access → check each item's source, created-at, last-verified, owner → delete unsafe items → rebuild from authoritative repository sources → re-run the same task to confirm | every retained memory item carries `source` / `authority` / `scope` / `created_at` / `last_verified` / `expires_at` / `owner` / `contains_sensitive_data`; items that cannot carry them are not retained |
| `A7` | **Dependency added without review** | a lockfile or manifest changed outside an approved task | stop the install → preserve the lockfile/manifest diff → verify package identity, source, maintainer, version → inspect lifecycle scripts and network use → reproduce behavior in a clean sandbox → revert and purge caches if unneeded → check for credential exposure | → `gear` dependency policy, `cull` if worm-class indicators appear |
| `A8` | **Auto-approval scope too broad** | an unknown command, network call, or external write executed with no confirmation | disable auto-approval → revoke session tokens and credentials → extract executed commands, child processes, network destinations → reconcile side effects → decompose the policy into capabilities → allow only safe wrappers | **post-incident test, all four must deny:** the same command outside the wrapper · redirect / subshell / script variants · a destination outside the allowlist · session-wide escalation persisting into a new session |

**Two fields the table above deliberately separates from "recovery".**

- **Containment** — the action that stops the blast radius growing, taken *before* diagnosis and *before*
  recovery. Cutting egress, disabling a server, revoking a token, and freezing writes are containment; they
  do not fix anything and are not supposed to. An incident where the first action was diagnostic is one where
  the damage kept accruing while it was being understood.
- **Residual risk** — what remains after recovery, stated explicitly at close: effects that could not be
  reconciled, data whose exposure cannot be ruled out, a workaround still in place, a detection gap not yet
  covered. **Prevention alone is not a closure**; an incident closed with prevention and no residual-risk line
  claims a completeness nobody verified.

### Remedy selection — undo is one option, not the category

Once an effect has left the harness, "roll it back" is a single choice among four, and picking it reflexively
destroys value in the cases where the effect was wrong in *authority* but right in *substance*. Reconcile each
reached effect individually and name which of the four applies:

| Remedy | Use when | What it must record |
|--------|----------|---------------------|
| **Ratify** | the effect is acceptable on its merits and a party with the standing to authorize it now does so | who ratified, on what basis, and that the effect was **unauthorized when it happened** — ratification approves the effect, never retroactively widens the grant |
| **Cancel** | the reversibility window is still open and nothing downstream depends on the effect yet | the deadline relied on, and confirmation the reversal actually landed |
| **Correct** | the effect stands but part of it is wrong, and a follow-up effect can amend it | both effects as one linked pair, so the record is not a correct-looking second state with an unexplained first |
| **Re-perform** | the effect must be withdrawn and redone under a valid grant | that the withdrawal completed *before* the redo, and a new idempotency key — a re-performance sharing the old key is a duplicate |

**Choosing between them is a factual question, not a preference.** Ask, in order: is the reversibility window
still open · has an external party or a third party already relied on the effect · is any part of it correct ·
who has standing to authorize it now. An answer of "unknown" to the first two selects the most conservative
remedy available, never the cheapest.

**Ratify is not a lowered bar.** `nexus` Q20 forbids moving the goalpost so a run can pass; ratification moves
nothing — it leaves the authority violation on the record as a finding and disposes of the *effect* separately.
An incident that closes with a ratified effect and no `HD-LOOP` fix in the layer that permitted it has used
ratification as the goalpost move Q20 names.

**Recurrence check.** An agent-origin incident closes only when the fix landed in the layer that produced it —
instruction file, tool contract, permission policy, or verification gate. A fix that lives only in a prompt or
a personal memory has not closed the incident; it has moved it. → `_common/HARNESS_DEBT.md` `HD-LOOP`.

## Method Sources (SKILL.md excerpt)

- **Adopt the Howie ("How We Got Here") postmortem method** from PagerDuty (Jeli lineage) as the default for SEV-1/SEV-2 reviews. Howie reframes the postmortem as a *facilitated narrative* rather than a 5-Whys interrogation: a Narrative Builder reconstructs the timeline, a Takeaways round captures what the team learned, and a Learning Review session translates those takeaways into durable changes. Use 5-Whys / fault tree only as supplementary analysis inside this frame, not as the frame itself. [Source: howie-guide.pagerduty.com]
- **Parallelise hypothesis tracking with a Dynamic Knowledge Graph (Resolve AI pattern).** Live-connect Pods, Grafana, GitHub, and Jenkins evidence into a graph that the triage agent maintains across multiple concurrent hypotheses; each hypothesis carries its own evidence list and disconfirmation criteria. Resolve.ai's production deployments report ~80% incident auto-resolution targeting this design. Replace the single-thread "Scout investigates one hypothesis" handoff with parallel hypothesis evidence requests when severity is SEV-1 / SEV-2. [Source: resolve.ai/product/ai-sre]
- **Catalogue + Scribe pattern (incident.io)** for incident-comms authoring. Use a service catalogue to determine scope (which downstream services consume the failing component) and a Scribe agent to auto-transcribe the war-room call into the timeline. incident.io reports `5×` faster timeline assembly and `90%` accuracy on the scope determination. Wire this into `incident_comms_authoring` so the human IC drives, not types. [Source: incident.io/blog — What is AI SRE Complete Guide 2026]
- **Use Causal Inference RCA** when high-cardinality traces are available: build a directed acyclic graph from traces, apply Granger causality between time-series, and reduce to a Minimum Spanning Tree (Kruskal) to separate symptom from cause. IBM Instana RCI deployments in financial production cut MTTR from 47 min to 8 min (−83%). When traces are sparse, fall back to the Swiss-cheese model already in scope. [Source: ijetcsit.org/index.php/ijetcsit/article/view/676]
- **Apply Autonomy with Guardrails** to AI-assisted triage actions: investigation steps can run autonomously, but every *remediation* action (rollback, restart, scale, flag-flip) passes through an explicit policy layer with named approvers. When agent confidence is below threshold (44% of incident leaders report only moderate AI confidence as of 2026), `pause` is the correct action, not `continue`. Pair this rule with the existing severity-tiered confirmation matrix. [Source: tldrecap.tech/posts/2026/conf42-sre/autonomous-agent-safety/]

