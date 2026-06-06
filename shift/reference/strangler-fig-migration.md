# Strangler Fig Migration Reference

Purpose: Incrementally replace a legacy system by routing a growing share of traffic through a façade. Design façade placement, per-route cutover criteria, parallel-run validation (shadow traffic), rollback plan, and final shutdown conditions.

## Scope Boundary

- **horizon `strangler`**: Strangler Fig pattern design (this document).
- **horizon `poc` (elsewhere)**: Isolated proof of concept. Strangler is the production rollout of a validated PoC.
- **horizon `codemod` (elsewhere)**: In-code transformation. Used inside a Strangler on the remaining legacy code.
- **ripple `canary-scope` (elsewhere)**: Traffic ramp details. Strangler uses canary mechanics per route.
- **ripple `rollback-plan` (elsewhere)**: Reversibility contract per cutover.
- **shift (elsewhere)**: Broader migration orchestration. `strangler` is one pattern in `shift`'s toolkit.
- **Launch (elsewhere)**: Release gating per cutover.

## Definition (Fowler)

> "Gradually create a new system around the edges of the old, letting it grow slowly over several years until the old system is strangled."
> — Martin Fowler, "Strangler Fig Application"

The metaphor: a strangler fig plant wraps around a host tree, slowly replacing it. The host (legacy) remains functional throughout until the fig (new) is self-supporting.

## When to Use

- Legacy system is too large to rewrite in one release.
- Legacy must stay operational during migration (business cannot pause).
- Migration will span weeks to years.
- Some features can be extracted cleanly; others are tangled.
- Incremental validation is possible (route-by-route).

## When Not to Use

- System small enough to rewrite in a single cutover window (< 1 week).
- Legacy is fully decommissionable with a big-bang cutover.
- No clear seam where a façade can sit.

## Façade Placement

The façade is the traffic router. It sits in front of the legacy and routes per-request to either legacy or new.

| Façade type | Use when |
|-------------|----------|
| Reverse proxy (nginx, Envoy, ALB, Cloudflare Worker) | HTTP traffic, clean URL-based routing |
| API gateway (Kong, Apigee, AWS API Gateway) | Multiple services, API-centric |
| Application-layer router (inside legacy app) | Monolith with URL routing; cheapest to introduce |
| Adapter in legacy code | Function-level migration inside a monolith |
| Message router (Kafka topic split) | Async / event-driven legacy |
| Database view / dual-write | Data-layer migration |

Anti-pattern: the façade itself becomes a dumping ground of business logic. Keep it routing-only.

## Per-Route Cutover Criteria

For each route / capability you cut over, define:

1. **Entry**: legacy implementation exists.
2. **Parallel-run validation**: new impl runs alongside legacy (shadow or mirror), diffs are sampled.
3. **Canary cut**: flag routes small % of traffic to new.
4. **Ramp**: 1% → 5% → 25% → 50% → 100% (per ripple `canary-scope`).
5. **Exit**: 100% traffic on new for ≥ cooldown window with no regression.
6. **Cleanup**: delete legacy code, remove façade rule.

## Parallel-Run (Shadow) Validation

Before taking any real traffic on the new implementation, run it in shadow mode:

```
client → façade ──┬──► legacy (returns to client, authoritative)
                  │
                  └──► new (response discarded, diff logged)
```

For each shadow-matched request:
- Log inputs.
- Log both responses.
- Compute diff (structural or semantic).
- Aggregate diff rate; fix sources of divergence.

Target: diff rate < 0.1% on representative traffic for ≥ 48 hours before starting the cut.

### Diffing approaches

| Approach | Use when |
|----------|----------|
| Exact JSON equality | APIs with stable schemas |
| Structural diff (ignore order, floats) | When non-semantic differences exist |
| Business-semantic comparator | When both outputs can be slightly different but both correct (e.g., pricing with rounding) |
| Statistical sampling | High-volume endpoints where full diffing is cost-prohibitive |

## Cutover State Machine per Route

```
  ┌─────────┐      ┌──────────┐      ┌────────────┐      ┌───────┐
  │ legacy  ├─────►│ shadow   ├─────►│ canary 1%  ├──...─►│ 100%  │
  └─────────┘      │ (new dark│      │ (new live  │      │ (legacy│
                   │  runs)   │      │  for subset)│      │ dead)  │
                   └──────────┘      └────────────┘      └───────┘
       │                │                    │                │
       │   rollback     │     rollback       │     rollback   │
       ▼                ▼                    ▼                ▼
    remove shadow    remove canary       ramp back down    resurrect legacy
                                                           (expensive!)
```

## Route Prioritization

Order routes from low-risk to high-risk:

1. **Read-only, low-traffic, no side effects** — perfect first cut.
2. **Internal-only admin endpoints** — small blast radius.
3. **Customer-facing reads** — cache + fallback easy.
4. **Writes with idempotency** — can be retried on legacy if new fails.
5. **Writes without idempotency** — need careful design.
6. **Critical transactional flows** — last; after pattern is proven.

## Database Strategy

The database is the stickiest part. Options:

| Strategy | Approach | Use when |
|----------|----------|----------|
| Shared DB | Both legacy and new read/write same DB | Fastest to start; tight coupling |
| DB per service, dual-write | Both write to both DBs; reads go to new | Needed before DB split can complete |
| DB per service, new reads from replica | New reads replicated data | When new can tolerate eventual consistency |
| CDC replication | Change-data-capture keeps new DB synced | Industrial-scale migrations |
| Event sourcing / replay | Events flow to both DBs via log | Complex event-driven systems |

Schema migrations inside the Strangler use expand-contract (see ripple `rollback-plan`).

## Final Shutdown Checklist

Before removing legacy code / infra:

- [ ] 100% traffic on new for ≥ 2 weeks.
- [ ] No regressions logged in observability.
- [ ] All customer-reported bugs resolved.
- [ ] Data migration complete and verified.
- [ ] Legacy infrastructure no longer receiving requests (confirmed via logs).
- [ ] Dependency graph shows no callers of legacy endpoints.
- [ ] Cost audit confirms legacy infra can be decommissioned.
- [ ] Team has rolled incident playbook from legacy to new.
- [ ] Final archive (code + data snapshot) stored for audit.

## Output Template

```markdown
## Strangler Fig Migration: [System Name]

### Scope
- **Legacy system**: [description, LOC, tech stack]
- **Target system**: [description, tech stack, architecture]
- **Expected duration**: [weeks / months / years]

### Façade
- **Type**: [reverse proxy / API gateway / app-layer / adapter / DB view / event router]
- **Location**: [where in the architecture]
- **Routing rule engine**: [feature flags / path regex / tenant allowlist]
- **Observability**: [logging both paths, diff metrics, SLO tracking]

### Route Inventory
| Route | Complexity | Priority | Parallel-run diff target | Cutover window |
|-------|-----------|---------|--------------------------|----------------|
| GET /users/:id | low | 1 | < 0.01% | Week 1 |
| GET /orders | medium | 2 | < 0.05% | Week 2-3 |
| POST /orders | high | 5 | < 0.01% | Month 2 |
| ... | ... | ... | ... | ... |

### Database Strategy
- **Approach**: [shared DB / dual-write / CDC / event-sourced]
- **Schema evolution**: [expand-contract plan — see rollback-plan]
- **Data validation**: [sampled consistency checks]

### Parallel-Run Validation
- **Diff method**: [exact / structural / semantic]
- **Sampling rate**: [% of traffic]
- **Diff aggregation window**: [hours]
- **Pass threshold**: [< 0.1% diff for ≥ 48h]

### Canary Ramp (per route — see ripple `canary-scope`)
- Standard ramp: 1% → 5% → 25% → 50% → 100%
- Stage windows: [durations per route category]

### Rollback
- Per-cutover: flip façade flag to legacy (≤ 5 min ToR).
- Cleanup phase rollback: harder (data may have diverged); document explicitly.

### Final Shutdown
- [ ] All checklist items above completed.
- **Target shutdown date**: [estimate]
- **Archive location**: [path / bucket]

### Handoffs
- ripple `canary-scope` per route.
- ripple `rollback-plan` per cutover.
- schema `migration` / `rollback` for DB changes.
- Beacon for SLO tracking during migration.
- Builder for per-route implementation.
- Launch for cutover gating.
- Judge for cutover PR review.
```

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Skipping shadow validation | Always run shadow ≥ 48h with < 0.1% diff |
| Cutting over hardest route first | Start low-risk read endpoints |
| Façade accumulating business logic | Keep routing-only; push logic into services |
| No cleanup phase planned | Legacy lingers forever → document sunset |
| DB migration left for "later" | Plan DB strategy at the start |
| No diff metric | Can't tell if new is correct; add diff metric |
| Rollback only via code deploy | Use façade flag for < 5min ToR |
| Decommissioning legacy too early | Wait ≥ 2 weeks at 100% + all checks |
| No observability of dual-path costs | Track infrastructure cost; dual-run is expensive |

## Deliverable Contract

When `strangler` completes, emit:

- **Façade design** (type, location, routing rules).
- **Route inventory** with priority and cutover window.
- **Database strategy** for data-layer migration.
- **Parallel-run / shadow validation plan** with diff threshold.
- **Per-route canary ramp** (hand off to ripple `canary-scope`).
- **Rollback plan** per cutover (hand off to ripple `rollback-plan`).
- **Final shutdown checklist**.
- **Handoffs**: ripple, schema, Beacon, Builder, Launch, Judge.

## References

- Martin Fowler — "StranglerFigApplication"
- Sam Newman — *Monolith to Microservices* (Strangler patterns)
- GitHub — Scientist library (for parallel-run comparison)
- Shopify — "Shopify's Modular Monolith"
- Stripe / GitHub — CDC-based migrations
- Chris Richardson — *Microservices Patterns*
