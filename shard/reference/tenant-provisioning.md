# Tenant Provisioning Reference

Purpose: Tenant onboarding, lifecycle management, and deprovisioning. Treats provisioning as IaC-driven, idempotent, and replayable — every tenant transition is a state-machine event with a durable record, default-data seed timing is explicit, and deprovisioning honors retention contracts (GDPR, contractual, regulatory).

## Scope Boundary

- **shard `provisioning`**: tenant lifecycle state machine, onboarding pipeline, default-data seeding, idempotent re-provisioning, and deprovisioning + retention rules.
- **shard `isolation` / `rls` / `routing` / `scale` (elsewhere)**: the multi-tenant model itself. Provisioning instantiates a tenant inside an existing model; it does not define the model.
- **shard `migration` (elsewhere)**: moving an *existing* tenant between shards. Provisioning creates new tenants; migration relocates them.
- **schema (elsewhere)**: DB schema and migration DDL. Provisioning runs schema migrations as a step but does not author them.
- **scaffold (elsewhere)**: cloud IaC for shared infra (VPC, clusters). Provisioning generates *per-tenant* IaC (DB, schema, KMS key) on top.
- **tempo (elsewhere)**: scheduled retention sweeps and grace-period timers. Provisioning specifies the retention contract; Tempo schedules its enforcement.
- **comply / cloak (elsewhere)**: GDPR/CCPA legal contract for data retention. Provisioning implements the technical erasure; Comply/Cloak owns the policy.

## Workflow

```
INTAKE    →  receive tenant request: id, plan tier, region, compliance class
          →  validate uniqueness, generate idempotency key

PLAN      →  resolve target shard (pool|dedicated) from plan tier + capacity
          →  enumerate provisioning steps as IaC plan; dry-run

PROVISION →  execute: schema/DB create, RLS attach, KMS key, routing entry
          →  every step idempotent; resumable on partial failure

SEED      →  insert default data (roles, settings, demo content) under tenant_id
          →  seeding is part of provisioning, not first-login lazy-init

ACTIVATE  →  flip state pending → active; emit tenant.activated event
          →  send onboarding webhook / email; notify billing

OPERATE   →  state transitions: suspend, reactivate, plan-change
          →  every transition is an event with audit row

DEPROVISION → grace period → soft-delete → hard-erase per retention contract
            → emit erasure-complete record for compliance audit
```

## Lifecycle State Machine

```
       ┌─────────┐    create     ┌───────────────┐
       │ pending │ ────────────► │ provisioning  │
       └─────────┘               └──────┬────────┘
                                        │ success
                                        ▼
       ┌──────────────┐  reactivate  ┌────────┐  suspend  ┌───────────┐
       │ deprovisioning│ ◄────────── │ active │ ────────► │ suspended │
       └──────┬────────┘  request    └────────┘ ◄──────── └───────────┘
              │ grace expires                  reactivate
              ▼
       ┌──────────────┐
       │   archived   │  (soft-delete; readable for audit window)
       └──────┬───────┘
              │ retention period elapses
              ▼
       ┌──────────────┐
       │    erased    │  (hard-delete; only metadata + erasure proof retained)
       └──────────────┘
```

## State Transition Table

| From | To | Trigger | Required action |
|------|-----|---------|-----------------|
| pending | provisioning | API call / signup | Acquire idempotency lock |
| provisioning | active | All steps succeeded | Emit `tenant.activated`, start metering |
| provisioning | pending | Partial failure | Roll back partial state; allow retry with same idempotency key |
| active | suspended | Non-payment / policy violation | Block writes; reads optional; pause metering |
| suspended | active | Payment / appeal | Unblock; resume metering |
| active | deprovisioning | Customer cancel / admin action | Begin grace period; freeze new writes after T |
| deprovisioning | active | Reactivate within grace | Restore writes; cancel erasure timer |
| deprovisioning | archived | Grace expired | Soft-delete; queries return 410 Gone |
| archived | erased | Retention elapsed | Hard-delete rows; retain erasure proof |

## Sync vs Async Provisioning

| Dimension | Sync | Async |
|-----------|------|-------|
| User waits | Yes (seconds) | No (returns immediately) |
| Steps | Schema-only or pre-existing pool | Includes DB create, KMS, routing, seed |
| Failure UX | Caller sees error, retries | Caller polls or webhook; retry queue handles |
| Default for | RLS pool tenants | Schema-per-tenant, dedicated-DB tenants |
| Latency budget | < 5s typical | seconds to minutes |
| Required infra | Single transaction | Job queue, status endpoint, idempotency store |

Pick async when total provisioning > 3s or any step calls a slow external API (DNS, KMS, certificate issue). Async with a status endpoint scales; long-blocking sync requests do not.

## Idempotency Pattern

Every provisioning request carries an idempotency key (UUID, client-generated or assigned at intake). Server stores `(idempotency_key → tenant_id, step_state, result)` for ≥ 24h.

| Replay scenario | Behavior |
|-----------------|----------|
| Same key, original still running | Return current status; do not start a second run |
| Same key, original succeeded | Return cached result |
| Same key, original failed | Resume from last completed step |
| New key, same tenant id | Reject (409 Conflict) |

Without idempotency keys, retried API calls produce duplicate tenants or partial state corruption.

## Default-Data Seed Timing

| Strategy | When | Pros | Cons |
|----------|------|------|------|
| Eager (during provisioning) | Before activation | Tenant active = tenant ready; no first-login surprise | Slower provisioning; failed seed = failed provision |
| Lazy (on first login) | First user request | Fast provisioning | Race conditions; first-user latency hit; partial-seed bugs |
| Hybrid (critical eager, optional lazy) | Roles+settings eager; demo content lazy | Balanced | Two code paths to maintain |

Default to eager + hybrid for non-trivial templates. Lazy-only causes "empty workspace" UX bugs and concurrent-init races.

## Deprovisioning + Retention Rules

| Data class | Retention contract | Action at retention |
|------------|--------------------|--------------------|
| User PII (GDPR Art 17) | 30-90 days grace + erase on request | Hard-delete; retain erasure proof |
| Financial / invoice | 7-10 years (jurisdiction-dependent) | Move to cold archive; do NOT erase |
| Audit logs | Per SOC2/ISO contract (typically 1-7 years) | Move to immutable archive |
| Backup snapshots | Pruned per backup retention (separate policy) | Document — backups outlive primary |
| Derived analytics | Aggregate-only after deprovision | Anonymize or drop tenant-scoped granularity |

GDPR Article 17 (right to erasure) requires honoring deletion requests within 30 days. But "erase from primary, keep in legal-hold" is a legitimate exception — document which class each table falls into *before* the deletion request arrives.

## Per-Tenant IaC Pattern

Treat each tenant's resources (schema, DB, KMS key, DNS entry, S3 bucket prefix) as IaC modules, not imperative scripts. Benefits: provisioning is a `terraform apply` with idempotency built in; deprovisioning is `terraform destroy` with state file as audit trail; drift detection is automatic.

```
modules/tenant/
  main.tf           # schema, RLS attach, KMS key alias, S3 prefix
  variables.tf      # tenant_id, plan_tier, region
  outputs.tf        # connection string, kms_arn, audit metadata

per-tenant state: terraform-state/tenants/<tenant_id>.tfstate
```

## Anti-Patterns

- **Non-idempotent provisioning** — retried call creates a second tenant or leaves orphaned schema. Always require an idempotency key.
- **Lazy-only seeding** — empty tenant on activation; first user hits init race condition or sees broken UI.
- **Provisioning as imperative script** — drift between expected and actual state; deprovisioning misses resources created mid-flight.
- **Skipping the suspended state** — going active → deprovisioning loses recovery affordance for non-payment cases that resolve.
- **Hard-delete on cancellation** — violates contractual retention (financial records, audit logs); creates legal exposure.
- **Erasure with no proof artifact** — GDPR auditors require evidence the deletion happened; keep an erasure record (tenant_id, timestamp, scope, operator).
- **Synchronous provisioning that calls slow external APIs** — DNS, certificate issuance, KMS provisioning each take seconds; chained synchronously they exceed gateway timeouts.
- **No state-machine enforcement** — code paths flip tenant state directly; transitions skip required actions (metering, audit). Centralize transitions through a single function.
- **Confusing soft-delete with erase** — archived tenants are queryable for audit; erased tenants are not. Conflating them breaks compliance reporting.

## Handoff

- **To Schema**: DDL for tenant-specific objects (per-tenant schema, indexes, RLS policy attach) — Schema authors and runs.
- **To Scaffold**: shared infra IaC (cluster, VPC, baseline KMS) that per-tenant IaC builds on.
- **To Tempo**: scheduled jobs for grace-period expiry, retention sweeps, archived-to-erased transitions.
- **To Beacon**: provisioning SLO (success rate, P95 latency, time-to-active), per-tenant activation funnel.
- **To Ledger**: tenant unit-cost line items, plan-tier mapping, metering start/stop events.
- **To Comply / Cloak**: retention contract, erasure proof artifact format, GDPR Article 17 compliance evidence.
- **To Builder**: provisioning service implementation, idempotency store, state-machine code, webhook handlers.
