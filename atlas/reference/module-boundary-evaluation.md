# Module Boundary Evaluation Reference

Purpose: Evaluate whether module/package boundaries align with **bounded contexts** (DDD) and domain boundaries. Detect cross-boundary leaks, shared-kernel abuse, and absent anti-corruption layers. Produce a boundary-health report with prioritized fixes.

## Contents

- What a boundary should be
- Boundary smells
- Evaluation dimensions
- Anti-corruption layer patterns
- Command recipes
- Output template

## What a Boundary Should Be

A healthy module boundary has:

1. **Ubiquitous language** — terminology inside the module is consistent and differs meaningfully from neighbors
2. **Explicit contract** — public API is small, intentional, and versioned
3. **Data translation** — types crossing the boundary are translated, not raw-shared
4. **Behavior, not just data** — the module owns decisions, not just CRUD
5. **Team ownership alignment** — boundary tends to match team / sub-system responsibility
6. **Test isolation** — can be tested without running neighbor modules

Violation of any of these is a boundary smell.

## Boundary Smells

| Smell | Signal | Example |
|-------|--------|---------|
| **Chatty boundary** | 10+ imports from one module to another | `order` imports 14 types from `user` |
| **Shared database** | two contexts read/write the same tables | `billing` and `analytics` both mutate `payments` |
| **Shared kernel abuse** | "common" module grows to contain domain logic | `shared/types` has 30+ business types |
| **Leaky entity** | domain entity used across contexts verbatim | `User` shape used in billing, auth, email all with different needs |
| **Reverse dependency** | lower layer imports from upper | `domain/` imports from `api/` |
| **Missing ACL** | external system's model leaks into domain | Stripe's `Invoice` appears inside `billing/domain` |
| **God module** | one module has >20% of total package imports | `core/` is imported by 80% of modules |
| **Feature envy** | module A mostly uses module B's data | `order/reporting` only reads `user/*` |
| **Cycle at boundary** | A ↔ B at module level | handoff to `cycle` Recipe |
| **Public-field data class** | boundary types are anemic structs, logic lives elsewhere | `UserDTO` + `UserService` pattern everywhere |
| **Type tunneling** | generics/any erase the boundary | `Handler<any>` passed across modules |

## Evaluation Dimensions

For each boundary pair (A, B):

| Dimension | Measurement | Healthy |
|-----------|-------------|---------|
| **Surface** | count of public types/functions A exposes to B | < 10 |
| **Directionality** | unidirectional? | yes |
| **Translation** | does B convert A's types to B's own? | yes for domain-crossing |
| **Purity** | does A leak infra types (DB rows, HTTP) into B? | no |
| **Data ownership** | does only one side own persistence? | yes |
| **Change correlation** | do A and B churn together (git co-change)? | low (<30%) |

### Co-change signal

```bash
# Files that changed together in last 180 days
git log --since=180.days --name-only --format=%H | \
  awk '/^[0-9a-f]/{c=$1; next} NF{print c" "$0}' | \
  sort | uniq | \
  <pair-counting-script>
```

Modules with high co-change are candidates for **merge** (too split) or **shared dependency extraction** (missing abstraction).

## Anti-Corruption Layer (ACL) Patterns

When an external/legacy system's model must not leak into your domain:

### 1. Adapter (simplest)

```
external_client → Adapter → domain_model
                             ↑
                    (translation in Adapter)
```

### 2. Facade + Adapter

```
domain → Facade (your vocabulary)
            ↓
         Adapter (translates)
            ↓
         external_client
```

### 3. Repository with domain types only

```
domain/Repository (interface, returns domain types)
    implementations/
      PostgresRepo → translates rows to domain
      RedisCache → translates cached payload to domain
```

### 4. Event translation

```
external_bus → ExternalEvent → Translator → DomainEvent → domain_handlers
```

### 5. Published Language (Stable API)

For contexts you control: publish a versioned API contract. Changes to either side go through the contract, not internal types.

## When to Split vs Merge a Boundary

| Condition | Action |
|-----------|--------|
| Co-change > 60%, shared vocabulary | **Merge** — they're one context |
| Shared DB table but divergent logic | **Split** with event-driven sync |
| 15+ cross-module imports, symmetric | **Introduce shared kernel** (small, frozen) |
| External system model leaks | **Insert ACL** |
| Same team owns both | Tolerate thinner boundary |
| Different teams, heavy coordination | **Harden boundary** (versioned contract) |

## Command Recipes

### Surface and directionality

```bash
# List cross-module imports
grep -rE "^(import|from)" src/module_a/ | grep -c "module_b"
# Reverse direction
grep -rE "^(import|from)" src/module_b/ | grep -c "module_a"

# If both > 0, bidirectional boundary violation
```

### Co-change analysis

```bash
# Pairs of modules changed in the same commit (top 20)
git log --since=6.months --name-only --format='COMMIT%n' | \
  awk '/^COMMIT$/{if(length(files))print files; files=""; next}
       {mod=$0; sub(/\/.*/,"",mod); if(!seen[mod]++)files=files" "mod}
       END{if(length(files))print files}' | \
  awk '{for(i=1;i<NF;i++)for(j=i+1;j<=NF;j++){
          if($i<$j)print $i" "$j; else print $j" "$i}}' | \
  sort | uniq -c | sort -rn | head -20
```

### Leaky-entity detection

Look for the same type name appearing across multiple module namespaces:

```bash
# TS example: export interface User from many files
grep -rn "export (interface|type|class) User" src/ | \
  awk -F: '{n=split($1,a,"/"); print a[2]}' | sort -u
```

If `User` is exported from 3+ modules, they likely disagree on what a User is → candidate for per-context renaming (`auth.User`, `billing.Customer`, `email.Recipient`).

### Shared-DB detection

Parse ORM/migration files:

```bash
grep -rE "class .* extends Model|@Entity|CREATE TABLE" \
  --include="*.ts" --include="*.py" --include="*.sql" src/ | \
  awk -F: '{n=split($1,a,"/"); print a[2]" "$0}' | \
  <group by table, flag tables touched from >1 module>
```

## Output Template

```markdown
## Atlas Boundary Evaluation

**Scope**: `src/` (TypeScript, 12 top-level modules)
**Reference**: DDD Bounded Context alignment
**Boundary health**: 7/12 well-bounded, 3 weak, 2 broken

### Module Role Map

| Module | Intended context | Surface | I/A |
|--------|------------------|---------|-----|
| `auth` | Identity & access | 8 exports | (0.2, 0.6) |
| `user` | User profile | 14 exports | (0.4, 0.4) |
| `order` | Ordering | 6 exports | (0.5, 0.5) |
| `billing` | Billing & invoicing | 22 exports | (0.6, 0.2) |
| `inventory` | Stock management | 4 exports | (0.5, 0.5) |
| `shared/types` | ??? | 47 exports | (0.0, 0.3) |

### 🔴 Broken: `shared/types`

**Smell**: Shared-kernel abuse — 47 exports, imported by 10/12 modules, contains domain types from multiple contexts.

**Evidence**:
- `shared/types/User` used differently by `auth`, `billing`, `email`
- `shared/types/Order` used by `order`, `billing`, `inventory`
- Changes to this module touched 6 PRs in the last 90 days, all cross-cutting

**Fix**: Split into per-context types, inline the truly universal ones.
1. `auth/types/AuthUser` (id, roles, session)
2. `billing/types/Customer` (id, tax_id, billing_address)
3. `email/types/Recipient` (email, display_name, locale)
4. Keep only truly universal: `shared/types/ISODate`, `shared/types/Uuid`

**Effort**: L (2 weeks) — requires coordinated migration
**Handoff**: `adr` → Zen

### 🔴 Broken: `order ↔ billing` (chatty bidirectional)

**Smell**: 18 cross-imports, both directions, co-change rate 74%.

**Evidence**:
- `billing/invoice.ts` imports 8 types from `order/`
- `order/service.ts` imports 10 functions from `billing/`
- Co-change rate 74% → these are actually **one context**

**Options**:
- (A) **Merge** into `commerce/` module (if same team)
- (B) **Harden boundary** with published contract + event sync (if different teams)

**Recommendation**: (A) merge — confirmed single team ownership in CODEOWNERS.

**Effort**: M (4–5 days)
**Handoff**: Zen (rename + restructure)

### 🟡 Weak: `billing` leaks Stripe types

**Smell**: Missing ACL — `stripe.Invoice` appears in `billing/domain/` directly.

**Fix**: Insert adapter layer.
1. Define `billing/domain/Invoice` (our vocabulary)
2. `billing/infra/stripe/StripeAdapter` translates
3. Domain depends on `InvoiceRepository` interface only

**Effort**: M (2–3 days)
**Handoff**: `adr` (ACL pattern choice) → Builder

### Co-change Hotspots

| Pair | Co-change rate | Verdict |
|------|----------------|---------|
| `order` ↔ `billing` | 74% | → merge |
| `user` ↔ `auth` | 31% | tolerable |
| `inventory` ↔ `order` | 22% | healthy |
| `email` ↔ `user` | 12% | healthy |

### Fitness Function Recommendations

```yaml
- name: No cross-domain leaks
  run: |
    # billing must not import Stripe types outside infra/
    grep -rE "import .* from 'stripe'" src/billing/ | \
      grep -v 'src/billing/infra/' && exit 1 || exit 0

- name: Bounded shared kernel
  run: |
    # shared/types has max 10 exports
    grep -cE "^export " src/shared/types/index.ts | \
      awk '$1 > 10 {exit 1}'
```

### Next Steps

1. `shared/types` split → ADR decision + phased rollout
2. `order + billing` merge → team decision, then Zen
3. Stripe ACL → `adr` + Builder
```

## Anti-Patterns

- Splitting modules by technical layer only (controllers/services/models) ignoring domain
- One "utils" or "common" dumping ground
- Sharing entities verbatim instead of translating per context
- Defining boundary by filesystem folder alone (rename doesn't fix leaks)
- Hardening a boundary that should actually be merged
- Tolerating a cycle at the boundary (handoff `cycle` Recipe first)
