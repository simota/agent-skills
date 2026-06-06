# Incident Learning & Postmortem

> Blameless postmortem culture, incident learning patterns, templates, organizational metrics

## 1. Blameless Postmortem: 5 Principles

| # | Principle | Description | Practice |
|---|-----------|-------------|----------|
| **BL-01** | **Assume good faith** | All participants acted on the best information available and made the best decision they could | Focus on system flaws, not individuals |
| **BL-02** | **Ask What/How, not Why** | Analyze "what happened" and "how it happened" | Avoid "why did you do that?" — it forces defensiveness |
| **BL-03** | **Forward-built timeline** | Construct timeline from before the incident forward | Prevents hindsight bias (don't reason backward from outcome) |
| **BL-04** | **Systems thinking** | Analyze system interactions, not individual mistakes | Examine tools, processes, communication, organizational structure |
| **BL-05** | **Accountability ≠ Punishment** | Assign ownership for fixes, but do not assign fault | "Eliminate blame, establish ownership" |

---

## 2. Cognitive Bias Countermeasures

| Bias | Description | Countermeasure |
|------|-------------|----------------|
| **Fundamental attribution error** | Attributing actions to character rather than circumstances | Focus analysis on situational factors |
| **Confirmation bias** | Attending only to information that supports existing beliefs | Appoint Devil's Advocate, include external team members |
| **Hindsight bias** | Perceiving events as "predictable" after the fact | Forward-built timeline (BL-03) |
| **Negativity bias** | Disproportionate focus on negative events | Explicitly document what went well |

---

## 3. Postmortem Template

```
Required sections:
  1. Incident Metadata
     - Date/time, duration, severity, participants, publication date

  2. Executive Summary
     - Impact (quantitative: QPS drop rate, latency increase, affected users, revenue impact)
     - Root cause (1-2 sentences)
     - Trigger (direct cause)

  3. Detailed Timeline
     - Minute-by-minute chronology (detection → response → recovery)
     - Decision-making context for each action

  4. Root Cause Analysis
     - Focus on system defects (not human error)
     - 5 Whys or fishbone diagram
     - List of contributing factors

  5. Lessons Learned
     - What went well (mandatory)
     - What went poorly
     - Where we got lucky

  6. Action Items
     - Single owner per item (multiple owners prohibited)
     - Priority (P0/P1/P2)
     - Tracking ticket link
     - Type: Prevention / Mitigation / Detection / Repair
     - Measurable success criteria

  7. Glossary (for readers outside the domain)

  8. Appendix (graphs, log excerpts, supporting data)
```

---

## 4. Postmortem Anti-Patterns

| # | Anti-Pattern | Problem | Countermeasure |
|---|-------------|---------|----------------|
| **PA-01** | **Blaming language** | Destroys psychological safety → reporting avoidance | Reviewer checks language before publication |
| **PA-02** | **Vague action items** | "Improve it" / "Be more careful" → unactionable | SMART criteria (specific, measurable, time-bound) |
| **PA-03** | **Multiple owners** | Diffusion of responsibility → nobody acts | Single POC (Point of Contact) per item |
| **PA-04** | **Delayed publication** | Information freshness degrades, learning opportunity lost | Mandate publication within 7 days |
| **PA-05** | **Behavioral fixes only** | "Be more careful next time" → recurrence | Prioritize systemic fixes (automation, guardrails) |
| **PA-06** | **Closed postmortems** | Shared only within team → no organizational learning | Default to company-wide publication, hold reading sessions |
| **PA-07** | **Unclosed action items** | Action items abandoned | Track closure rate, hold FixIt Weeks |

---

## 5. Incident Learning Metrics

```
Postmortem quality indicators:
  - Time to publication (target: < 7 days)
  - Action item specificity score
  - Prevention vs Mitigation action ratio
  - Reader reach (team-only / cross-organization)
  - Data completeness (quantitative impact, timeline detail)

Organizational health metrics:
  - Action item closure rate (target: > 80%)
  - Average time to closure
  - Similar incident recurrence rate
  - MTTD (Mean Time to Detect) trend
  - MTTR (Mean Time to Resolve) trend

Culture indicators:
  - Voluntary participation rate in postmortem reviews
  - Language blamelessness (checked during review)
  - Leadership consistency in blameless behavior
  - On-call team attrition rate
  - Psychological safety survey score

Knowledge sharing practices:
  - Weekly/monthly outage report distribution
  - Postmortem reading sessions (cross-team)
  - "Wheel of Misfortune" (past incident training exercises)
  - "Greatest Hits" annual compilation
  - Presentations by incident responders
```

---

## 6. Beacon Integration

```
Usage in Beacon:
  1. Post-incident monitoring improvement proposals (reduce detection time)
  2. Integration with SLO violation analysis (track budget consumption causes)
  3. Alert effectiveness validation (was it detected? was it timely?)
  4. Dashboard improvement proposals (visibility gaps during incidents)

Quality gates:
  - Postmortem includes quantitative impact data
  - Each action item has a single owner assigned
  - Systemic fixes are prioritized over behavioral fixes
  - Monitoring improvement items are included (Beacon integration point)
  - Published within 7 days
  - Closure rate exceeds 80% (quarterly check)
```

---

## 7. AI-Assisted Postmortems (2026)

By 2026 the autonomous-investigation tooling that triages incidents in real time (Datadog **Bits AI SRE**, Azure **SRE Agent** + GitHub Copilot, Wiz **Green Agent** for security incidents, Resolve KG / Howie / dynamic incident knowledge graphs) also drafts the *initial* postmortem from the investigation transcript. Treat the AI-drafted artefact as a **first pass**, never as the final document.

### Operating Rules

1. **Human editor of record is mandatory.** The AI agent collects telemetry, candidate root causes, contributing factors, and a draft timeline; a named human owner reviews, edits, and signs the postmortem before publication. The signature does not transfer to the agent.
2. **Blamelessness is a human judgement.** The agent can flag tone issues, but a human reviewer must confirm every BL-01 / BL-02 principle (assume good faith, ask what/how not why) before the document leaves draft.
3. **Action items still need a single human owner.** PA-03 (multiple owners) extends to AI agents — an action item owned by "Bits AI" does not get done. Either name a human or convert the item to a runbook automation request (see `mend/reference/canary-remediation.md`).
4. **Cite the investigation source.** Postmortem appendix must include the investigation ID from the agent transcript so the chain from telemetry → diagnosis → postmortem → action items is traceable end-to-end. This is the same `investigation_source` field required in Mend's audit trail.

### Quality Gates (extending §6)

- Reviewer confirms every paragraph the AI drafted; no copy-paste-without-edit.
- The draft's confidence on candidate root cause is preserved verbatim in the document — "high confidence" / "medium confidence" / "low confidence" — so future readers can calibrate the lessons against the original certainty.
- Hallucination check: every numeric impact figure in the postmortem must trace to a metric / log query in the appendix. Unsourced numbers from an AI draft fail review.

**Source:** [Google SRE: Postmortem Culture](https://sre.google/workbook/postmortem-culture/) · [PagerDuty: The Blameless Postmortem](https://postmortems.pagerduty.com/culture/blameless/) · [Atlassian: Blameless Postmortem](https://www.atlassian.com/incident-management/postmortem/blameless) · [Datadog Bits AI SRE (2026)](https://www.datadoghq.com/blog/bits-ai-sre-deeper-reasoning/) · [Azure SRE Agent + GitHub Copilot self-healing pipelines (2026)](https://stochasticcoder.com/2026/04/29/beyond-the-alert-building-self-healing-pipelines-with-azure-sre-agent-and-github-copilot/)
