# Organizational Complexity Anti-Patterns

Purpose: Use this file when Void is evaluating bloated process, meetings, approvals, reporting, or document sprawl.

Contents:
- Eight anti-patterns for organizational complexity
- Process CoK and ceremony audit thresholds
- `Two-way Door` decision rule
- Document and reporting reduction criteria

## 8 Anti-Patterns

| ID | Anti-pattern | Symptom | Void question |
|----|--------------|---------|---------------|
| `OC-01` | Too many approval layers | Small changes need `3+` approvals | What risk does this approval prevent, and did it actually prevent it? |
| `OC-02` | Meeting bloat | Large meetings with unclear decision ownership | Who decides, and who only needs notification? |
| `OC-03` | Fossilized process | No one remembers why the process exists | Is the original reason still valid? |
| `OC-04` | Document sprawl | Multiple conflicting sources of truth | When was this document last used? |
| `OC-05` | Tool sprawl | Several tools solve the same class of problem | Can this be consolidated into one tool? |
| `OC-06` | Ceremony accumulation | Agile rituals consume work time | Does this ceremony still fit the current team? |
| `OC-07` | Committee multiplication | Decision ownership is diluted | Could one accountable owner decide this? |
| `OC-08` | Stacked reporting obligations | Multiple overlapping reports cost more than they return | Who reads this report, and what action does it drive? |

## Process CoK Signals

| Signal | Healthy | Warning | High complexity |
|--------|---------|---------|-----------------|
| Meeting share of working time | `<20%` | `20-40%` | `>40%` |
| Fossilized-process rate | `<10%` | `10-30%` | `>30%` |
| Approval layers | `1-2` | `3` | `>3` |
| Same-tool count per job type | `1` | `2` | `>2` |

## Ceremony Audit

Use ceremony pruning when:
- planning is already prepared but the meeting still runs long
- standups repeat status without decisions
- retrospectives do not create follow-through
- demos are information-only and could be asynchronous

Example heuristic:
- sprint planning should shrink or split if the meaningful planning content fits in `30 min`

## Decision Speed: One-way vs Two-way Door

| Door type | Meaning | Default action |
|-----------|---------|----------------|
| `Two-way Door` | Reversible decision | simplify and decide quickly |
| `One-way Door` | Hard to reverse | escalate and decide carefully |

Rule: if a reversible decision is being treated like a one-way door, recommend simpler approval flow.

## Document and Report Reduction

### Document Audit Rules

| Signal | Threshold | Default action |
|--------|-----------|----------------|
| Unread | no meaningful views for `6+` months | `REMOVE` candidate |
| Unupdated | no update for `12+` months | verify accuracy, then update, merge, or retire |
| Duplicated truth | overlaps with a newer source | merge or retire |

### Reporting Audit Rules

Ask:
- who reads it?
- what action follows?
- can the same signal live in an existing dashboard or summary?

If the report creates work but no decision, recommend removal or consolidation.

## Void Use

- Apply `Process Pruning` to approval flows, meetings, and recurring ceremonies.
- Apply `Document Retirement` to stale or unread docs.
- Use `Two-way Door` as the reversibility test before escalating.

Quality gates:
- meeting share `>40%` -> audit ceremony load
- approval layers `>3` -> simplify approvals
- unread docs `>30%` of the corpus -> batch retirement review
- same-tool count `>2` -> consolidation review

Sources: [Amazon shareholder letter](https://www.aboutamazon.com/news/company-news/andy-jassy-2024-letter-to-shareholders) · [Jeff Bezos on Two-way Door decisions](https://www.sec.gov/Archives/edgar/data/1018724/000119312516530910/d168744dex991.htm) · [HBR on organizational drag](https://hbr.org/2017/03/great-companies-obsess-over-productivity-not-efficiency)
