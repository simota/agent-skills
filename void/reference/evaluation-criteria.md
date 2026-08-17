# Evaluation Criteria Reference — Void

Purpose: Use this file to investigate existence, blast radius, staleness, and YAGNI status before scoring a target.

Contents:
- The 5 Existence Questions with investigation prompts
- Blast-radius labels and staleness thresholds
- Target categories and default subtraction patterns
- The YAGNI decision path and evaluation summary template

## 5 Existence Questions

### Q1: Who uses it?

Goal: separate real users from hypothetical users.

```yaml
question: "Who uses it?"
investigation_by_domain:
  Code:
    - "Who imports or calls this?"
    - "Are there real external clients for this API?"
  Feature:
    - "What is the DAU or usage frequency?"
    - "When did someone last use it, and how many users did that include?"
  Process:
    - "How many people or work items pass through this step each month?"
    - "Who actually verifies or approves it?"
  Document:
    - "Who last viewed or updated it?"
    - "Can you point to a decision that relied on it?"
  Design:
    - "What share of users traverse this path?"
    - "What are dwell time and abandonment rate?"

scoring:
  high_confidence_keep: "Observed active users backed by logs or direct evidence"
  medium_confidence: "Indirect usage exists, but the direct user is unclear"
  high_confidence_remove: "No identifiable user; only speculative future value"

red_flags:
  - "Someone might need it one day"
  - "Another team probably uses it"
  - "Let's keep it just in case"
```

### Q2: What breaks if removed?

Goal: separate real dependency from assumed dependency.

```yaml
question: "What breaks if removed?"
investigation_by_domain:
  Code:
    - "Does build or compile fail?"
    - "Do tests fail, and are those tests themselves still justified?"
    - "Does a runtime path error?"
  Feature:
    - "Does a user journey break?"
    - "Does data consistency break?"
    - "Is there an alternative path?"
  Process:
    - "Does compliance break?"
    - "Does quality materially degrade?"
    - "Is there legal or regulatory impact?"
  Document:
    - "Does onboarding become materially harder?"
    - "Do decision records disappear?"
    - "Does audit readiness break?"
  Design:
    - "Does a key journey break?"
    - "Does the conversion funnel suffer?"

blast_radius_levels:
  NONE: "Nothing breaks -> immediate REMOVE candidate"
  LOCAL: "Only local module or team impact -> REMOVE or SIMPLIFY candidate"
  CROSS_MODULE: "Cross-team or cross-module impact -> cautious SIMPLIFY or DEFER"
  PUBLIC_API: "External client or stakeholder impact -> Magi escalation required"
  DATA: "Data-integrity impact -> highest caution, usually DEFER"
```

### Q3: When was it last meaningfully changed?

Goal: distinguish healthy stability from abandonment.

```yaml
question: "When was it last meaningfully changed?"
investigation:
  - "When was the last meaningful bug fix, feature change, or content update?"
  - "Ignore formatting-only or automated churn."
  - "Check related issues, PRs, or tickets."

staleness_thresholds:
  fresh: "Meaningful change within 3 months"
  aging: "No meaningful change for 3-12 months"
  stale: "No meaningful change for 12-24 months -> SIMPLIFY or REMOVE candidate"
  fossilized: "No meaningful change for more than 24 months -> strong REMOVE candidate"

exceptions:
  - "Stable by design, so change is rare"
  - "Regulatory or compliance requirements block change"
  - "Disaster-recovery or emergency-only logic"
```

### Q4: Why was it built?

Goal: compare original intent with current reality.

```yaml
question: "Why was it built?"
investigation:
  - "What did the original issue, PR, or spec say?"
  - "Is the original requirement still valid?"
  - "Does the original problem still exist?"
  - "Was the same problem solved elsewhere?"

obsolescence_signals:
  - "The original requirement was withdrawn"
  - "A different approach already solved the same problem"
  - "Business, technical, or org context changed"
  - "It was experimental and the experiment is over"
  - "No one can explain the original reason anymore"
```

### Q5: What does keeping it cost?

Goal: expose hidden maintenance cost.

```yaml
question: "What does keeping it cost?"
investigation_by_domain:
  Code:
    - "How much does it add to test time or build time?"
    - "How long does it take a new engineer to understand?"
    - "How often does it contribute to bugs?"
  Process:
    - "How much person-time does this step consume?"
    - "How much wait time does it impose?"
    - "How expensive are exceptions?"
  Document:
    - "How costly is it to keep accurate?"
    - "What is the risk of wrong decisions from stale content?"
    - "How much search noise does it add?"
  Design:
    - "What maintenance or support cost does it create?"
    - "Does it add user confusion?"
  Dependency:
    - "How often does it create security or compatibility work?"

hidden_costs:
  - "Cognitive load"
  - "Opportunity cost"
  - "Propagation cost"
  - "Onboarding cost"
  - "Reliability risk from stale or unclear knowledge"
```

## Target Categories

| Category | Definition | Examples | Default pattern |
|----------|------------|----------|-----------------|
| `Feature` | User-facing behavior | Dashboard, export, notifications | `Feature Sunset` |
| `Abstraction` | Design layers in code | Base classes, handlers, plugin systems | `Abstraction Collapse` |
| `Scope` | Variants and supported breadth | Output formats, configuration options | `Scope Cut` |
| `Dependency` | External package or service | npm package, API, SaaS | `Dependency Elimination` |
| `Configuration` | User or system options | env vars, flags, admin settings | `Configuration Reduction` |
| `Process` | Workflow or approval flow | code review flow, approvals, meetings | `Process Pruning` |
| `Document` | Specs, guides, checklists | design doc, wiki, playbook | `Document Retirement` |
| `Design/Specification` | UI structure or stated requirements | screens, stories, acceptance criteria | `Scope Cut` or `Feature Sunset` |

## YAGNI Decision Guide

```text
1. Is it used now?
   -> Yes: continue to Q2-Q5
   -> No: immediate REMOVE candidate unless compliance, regulation, or emergency exception applies

2. Is there a concrete plan to need it within 6 months?
   -> Yes: KEEP-WITH-WARNING
   -> No or speculative: REMOVE candidate

3. Is re-creating it later expensive?
   -> High: DEFER and schedule periodic review
   -> Low: REMOVE and recreate only if the need becomes real
```

## Admission Gate — the same questions, asked before it exists

The 5 Existence Questions interrogate something already built, where the sunk cost, the incumbency, and
"someone might be using it" all argue for keeping it. The cheapest removal is the one that never gets
proposed, so run this gate on **additions**: a new abstraction, layer, protocol document, registry entry,
config surface, or dependency.

**Six conditions under which the structure is not worth adding.** Any one is sufficient to decline.

| Condition | Signal | Use instead |
|-----------|--------|-------------|
| The relation is simple | one key maps to one value | a map / a field |
| The access pattern is fixed | a small stable set of queries, no exploration | a view / a direct lookup |
| The update path is single | one writer, one transaction, no traversal | keep the existing source of truth |
| Correctness lives in a transaction | balances, counts, effect identity, approval state | the transactional store; the new structure is at most a projection |
| Topology buys nothing | modeling it as nodes and edges improves no selection, no constraint, and no diagnosis | a list / a table |
| No owner for the operating cost | nobody owns schema, resolution, migration, tuning, or freshness | do not adopt at any scale |

Privacy is a seventh, asymmetric condition: if linking the entities enables inference or re-identification
that the separate pieces did not, the partitioned model wins even when the linked one is more useful.

**The load-bearing test — is the relation *used*?** An edge that no query traverses, no constraint checks, no
recovery path follows, and no audit reads is not neutral. It costs schema surface, update work, and one more
thing that can be wrong. **Relations do not become more valuable by being more numerous.** The same holds for
a rule nothing enforces, a reference nothing loads, and a field nothing reads.

**Name the tax before adopting.** Schema complexity · identity resolution · migration · indexing · query
tuning · visualization · operational skill · data quality · edge explosion · provenance upkeep. Write it on
the same page as the benefit; a benefit stated alone is not a comparison.

**Adopt at the smallest scope that can be evaluated**, and state up front what would make it unnecessary
(the removal condition — `prune/reference/retention-criteria.md` § Registry Drag). Expand only after the
current scope demonstrably paid.

## Evaluation Summary Template

```yaml
target_evaluation:
  target_name: "<Target Name>"
  domain: "CODE | FEATURE | PROCESS | DOCUMENT | DESIGN | DEPENDENCY | CONFIGURATION | SPECIFICATION"
  category: "FEATURE | ABSTRACTION | SCOPE | DEPENDENCY | CONFIGURATION | PROCESS | DOCUMENT | DESIGN_SPEC"
  questions:
    q1_who_uses: { answer: "string", confidence: "HIGH | MEDIUM | LOW" }
    q2_what_breaks: { answer: "string", blast_radius: "NONE | LOCAL | CROSS_MODULE | PUBLIC_API | DATA" }
    q3_last_changed: { answer: "YYYY-MM-DD", staleness: "FRESH | AGING | STALE | FOSSILIZED" }
    q4_why_built: { answer: "string", still_valid: true }
    q5_keeping_cost: { answer: "string", cost_level: "NEGLIGIBLE | LOW | MEDIUM | HIGH | CRITICAL" }
  yagni_verdict: "CURRENTLY_USED | PLANNED_USE | SPECULATIVE | DEAD"
  next_phase: "-> WEIGH"
```
