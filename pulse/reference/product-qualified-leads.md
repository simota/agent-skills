# Product-Qualified Leads (PQL)

Purpose: define and instrument the signal that a user (or account) has experienced enough
product value to be worth a sales/expansion motion. PQL is the measurement backbone of
**product-led growth (PLG)** — it replaces the marketing-qualified-lead (MQL) "filled a form"
proxy with "did meaningful work in the product."

Use this when designing a PLG funnel's conversion layer, defining activation→monetization
handoffs, or instrumenting which in-product behavior should trigger sales/expansion.

## Contents
- PQL vs MQL vs SQL
- Defining the PQL (signal model)
- PQL vs PQA (account-level)
- Instrumentation
- Thresholds & handoff

## PQL vs MQL vs SQL

| Lead type | Qualified by | Owner | Weakness it fixes |
|-----------|--------------|-------|-------------------|
| `MQL` | marketing engagement (downloads, form fills) | marketing | engagement ≠ intent |
| `SQL` | sales acceptance after discovery | sales | slow, manual |
| `PQL` | **demonstrated in-product value** | product + growth | predicts conversion far better in PLG motions |

PQL does not replace the funnel — it is the **conversion event between activation and revenue**
in the PLG funnel (`Acquisition → Activation → PQL → Conversion → Expansion`).

## Defining the PQL — Signal Model

A PQL is a scored combination of three signal classes. Avoid single-event PQLs (one click is
noise); avoid 20-factor models (unexplainable). Aim for 3-6 weighted signals.

| Signal class | Examples | What it proxies |
|--------------|----------|-----------------|
| `Activation depth` | reached the aha-moment, completed core workflow N times | value experienced |
| `Breadth / habit` | used ≥K features, returned on ≥D days in window | stickiness |
| `Expansion intent` | hit a plan limit, invited teammates, used a gated feature | willingness to pay |

PQL score = weighted sum, with a **hard gate** on activation (no activation → never a PQL,
regardless of other signals). Define the aha-moment with `activation-design.md`; define the
underlying events with `event-schema.md`.

## PQL vs PQA (Product-Qualified Account)

- **PQL** = an individual user crosses the threshold (self-serve / prosumer motions).
- **PQA** = an *account* crosses it — aggregate signals across all users in the org (seat
  count, cross-team adoption, account-level limit hits). Use PQA for B2B sales-assist motions
  where the buyer ≠ the active user.

Model PQA as a roll-up of PQL signals plus account-only signals (domain, seats, billing tier).

## Instrumentation
- Every PQL signal must map to a tracked event with stable naming (`event-schema.md`) — a PQL
  model built on ad-hoc events silently drifts as the product changes.
- Compute the score in the warehouse / product-analytics tool, not in the app, so weights can
  be re-tuned without a deploy.
- Emit a `pql_reached` event when the threshold is crossed (timestamped, with the contributing
  signals) so downstream funnels and `experiment` can measure conversion lift on the PQL cohort.

## Thresholds & Handoff
- Calibrate the threshold against *historical conversion*: pick the score where the
  conversion-to-paid rate justifies a sales touch (don't guess — backtest on converted users).
- Re-tune quarterly; PQL definitions decay as the product and ICP evolve.
- Handoffs: aha-moment / activation definition → `activation-design.md`; event contracts →
  `event-schema.md`; PQL-cohort conversion lift → `experiment`; retention of the PQL cohort →
  `growth`; PQL→revenue dashboards → `dashboard-spec.md` / `revenue-analytics.md`.
