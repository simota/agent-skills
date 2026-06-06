# Cost-Allocation Tagging Strategy Reference

Purpose: Subcommand-scoped methodology for designing and enforcing a cloud-cost tagging taxonomy across AWS Cost Allocation Tags, GCP Labels, and Azure Tags. Produces a mandatory tag set, allocation model (showback / chargeback / hybrid), enforcement architecture (SCP / IAM / Azure Policy / Org Policy), and remediation playbook for untagged resources. Outcome: > 95% cost coverage attributable to a team, service, environment, and cost center — without which optimization recommendations are speculation.

## Scope Boundary

- **ledger `tagging`**: tag taxonomy design, allocation-model decision, enforcement policy, untagged-resource remediation, showback/chargeback reporting structure.
- **ledger `estimate` (default, elsewhere)**: forward-looking IaC cost. Consumes the tag taxonomy to produce cost-by-team estimates.
- **ledger `rightsizing` (elsewhere)**: needs tags to attribute right-sizing savings to teams. Run `tagging` BEFORE `rightsizing` if coverage is < 80%.
- **ledger `anomaly` (elsewhere)**: anomaly attribution depends on tags. Untagged spike = team unknown = no escalation owner.
- **scaffold (elsewhere)**: applies tag policy to IaC modules (Terraform `default_tags`, CloudFormation Stack tags, Pulumi resource transforms). `tagging` defines the schema; Scaffold enforces in code.
- **beacon (elsewhere)**: reliability tags (oncall team, runbook URL) overlap with cost tags. `tagging` owns cost-allocation tags only — coordinate but do not collapse the tag sets.
- **comply (elsewhere)**: regulatory tags (data classification, residency, PII flag) audit-trail. `tagging` references these but does not own classification policy.
- **cloak (elsewhere)**: data-classification taxonomy. Cost tagging consumes Cloak's classification levels, never invents them.

## Workflow

```
INTAKE     →  identify scope (account/org), maturity stage (no tags / partial / mature)
           →  capture business model: single team / multi-team / multi-tenant SaaS

DESIGN     →  define mandatory tag set (5-7 keys); reject taxonomies with > 10 mandatory tags
           →  set allowed-value lists per tag; define case + separator convention

ALLOCATE   →  choose model: Showback (visibility only) / Chargeback (real $ transfer) / Hybrid
           →  define shared-cost split rule (network egress, observability, control plane)

ENFORCE    →  layer prevention (SCP/Org Policy) + detection (Config/Recommender) + remediation
           →  set untagged-resource SLA: detect within 24h, tag within 7d, terminate / chargeback at 30d

ROLL OUT   →  apply default_tags to IaC; backfill existing resources; soft-fail then hard-fail
           →  publish allocation report; reconcile against finance cost center master

HANDOFF    →  Scaffold: IaC default_tags + tag-policy modules; Beacon: untagged-resource alert;
           →  Atlas: org tag-coverage map; Comply: tag-evidence trail
```

## Mandatory Tag Set (Recommended Baseline)

| Tag key | Purpose | Example values | Source of truth |
|---------|---------|----------------|-----------------|
| `Environment` | Lifecycle stage | `prod`, `staging`, `dev`, `sandbox` | Platform team enum |
| `Team` | Owning team | `team-platform`, `team-payments` | HR / org chart |
| `Service` | Logical service | `checkout-api`, `recs-engine` | Service catalog (Backstage) |
| `CostCenter` | Finance allocation | `cc-1042`, `cc-2310` | Finance master |
| `ManagedBy` | Provisioning tool | `terraform`, `manual`, `console` | IaC repo |
| `DataClassification` | Sensitivity (optional but recommended) | `public`, `internal`, `confidential`, `restricted` | Cloak / Comply |
| `Project` | Time-boxed initiative (optional) | `proj-q2-migration` | PM tool |

Rule: every mandatory tag must have an enforced allowed-value list. Free-text tags fragment into 200+ variants and break allocation reports.

## Vendor Capability Comparison

| Capability | AWS | GCP | Azure |
|-----------|-----|-----|-------|
| Tag/Label name | Cost Allocation Tags | Labels | Tags |
| Activation required | Yes (Billing console, 24h delay) | Auto | Auto |
| Inheritance | None (per-resource) | Project / Folder labels propagate | Resource Group inherits to resources (opt-in) |
| Char constraints | 128/256, Unicode | 63/63 lowercase + `_` `-` | 512/256 |
| Case sensitivity | Yes | No (lowercase only) | Yes (preserved, case-insensitive lookup) |
| Max tags / resource | 50 | 64 | 50 |
| Enforcement primitive | SCP, Tag Policy, Config Rule | Org Policy (`constraints/resourcemanager.allowedExportDestinations`-style), Asset Inventory | Azure Policy (deny / modify / append) |
| Cost report integration | Cost Explorer, CUR, Cost Categories | BigQuery billing export, Looker | Cost Management, exports |
| Auto-remediation | EventBridge -> Lambda | Asset feed -> Cloud Function | Policy `modify` effect |
| Untagged-resource report | CUR `bill_payer_account_id` + tag columns | BigQuery `labels` STRUCT | Cost Management `Tags` filter |

Cross-cloud rule: pick a single canonical case (lowercase recommended) and a single separator (`-` recommended). Do NOT mix `costCenter`, `cost_center`, `cost-center` across clouds.

## Allocation Models

| Model | Mechanism | Pros | Cons | Best for |
|-------|-----------|------|------|----------|
| **Showback** | Cost reports per team, no $ transfer | Low friction, fast adoption | No behavior change incentive | Early FinOps maturity |
| **Chargeback (full)** | Internal cost transfer to team budgets | Strongest incentive | Requires finance integration, dispute process | Mature multi-BU orgs |
| **Hybrid** | Showback + chargeback for shared services only | Balanced | Two reports to maintain | Most common |
| **Tenant-based** | Per-customer attribution (SaaS) | Unit economics | Requires shared-resource splitting | SaaS COGS reporting |

Shared-cost split rules:
- **Network egress**: split by source-tag traffic ratio (CloudWatch Logs / VPC Flow Logs).
- **Observability** (CloudWatch, Datadog, New Relic): split by log/metric volume per tag.
- **Control plane** (EKS, GKE, AKS): split by namespace/workload share when available, else even split.
- **Reservations / Savings Plans**: prefer fair-allocation (utilization-weighted) over equal split.

## Enforcement Thresholds & SLAs

| Stage | Coverage threshold | Action |
|-------|-------------------|--------|
| Discovery | < 50% tagged | Soft-warn only; no enforcement; build report |
| Adoption | 50-80% tagged | Detect-and-alert; weekly untagged-resource digest to teams |
| Enforcement | 80-95% tagged | Deny-create on missing mandatory tags (SCP / Azure Policy `deny`) |
| Mature | > 95% tagged | Deny + auto-remediate (`modify` to add `Team=unallocated`); chargeback unallocated to platform |
| Untagged-resource SLA | any | Detect 24h / Notify 48h / Tag 7d / Terminate or chargeback 30d |
| Mandatory tag count | > 10 | Reduce — taxonomy bloat causes selective enforcement and gaming |
| Allowed-value drift | > 20 distinct values per enum tag | Audit and consolidate |

## Anti-Patterns

- Designing > 10 mandatory tags — operators game the system, IaC modules fragment, and only 3-4 actually get used. Cap at 5-7 mandatory; everything else optional.
- Free-text values on `Team` / `Service` / `CostCenter` — produces 200+ variants of the same team name across regions and accounts. Always enforce an allowed-value enum.
- Mixed case and separator across clouds (`costCenter` in AWS, `cost_center` in GCP) — joins in the data warehouse silently drop rows. Standardize on lowercase + dash before any tagging campaign.
- Enforcement before discovery — flipping SCP `deny` at < 80% coverage breaks deployments and triggers blanket exemptions that never expire. Soft-warn -> alert -> deny, not the reverse.
- Treating untagged resources as a security finding only — they are a financial finding too. Untagged = unowned = no rightsizing, no anomaly escalation, no chargeback.
- Tagging the resource but not the children (EBS volumes, snapshots, ENIs, S3 objects) — child resources represent 30-50% of spend in storage-heavy workloads and inherit nothing by default. Use `default_tags` (Terraform AWS) and explicit propagation.
- Using cost tags for security / compliance / oncall — overloaded tag sets become inconsistent because each owner edits independently. Keep cost-allocation tags separate; cross-reference via stable IDs.
- Ignoring shared-cost allocation — leaving control-plane / network / observability as "Other" hides 15-25% of spend and undermines unit economics. Define split rules at design time.
- Skipping the IaC default-tags layer — manual per-resource tagging always drifts. Tag at the provider/project/subscription level so omission is the exception.

## Handoff

- **To Scaffold**: `default_tags` block (Terraform AWS), Pulumi resource transforms, CloudFormation template `Tags`, Azure Policy `append` ARM. Includes allowed-value enum and case convention.
- **To Beacon**: untagged-resource SLO (coverage >= 95%, alert at < 90% for 7 days); cost-anomaly rule keyed off `Team=unallocated` spike.
- **To Atlas**: org tag-coverage map — by account, by service, by team — surfaced as a periodic architecture-health signal.
- **To Comply**: tag-evidence trail for SOC2 / ISO 27001 cost-allocation control; data-classification tag audit linkage.
- **To Ledger `estimate` / `rightsizing` / `anomaly`**: certified tag taxonomy + coverage report. Downstream recipes refuse to produce per-team output below 80% coverage.
- **To Cloak**: confirm `DataClassification` tag values align with Cloak's classification framework before publication.
