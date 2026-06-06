# Terraform / IaC Anti-Patterns

Purpose: Use this file when reviewing Terraform module design, state strategy, provider/version hygiene, or CI/CD integration.

Contents:
1. Core anti-patterns
2. State management risks
3. HCL quality risks
4. Provider and workspace risks
5. CI/CD gates

## Core Anti-Patterns

| ID | Anti-pattern | Signal | Safer pattern |
|----|--------------|--------|---------------|
| `TF-01` | Monolithic State | `100+` resources in one state, slow plans, huge blast radius | split by service × environment |
| `TF-02` | God Module | one module owns VPC + compute + DB + IAM, or module exceeds `50` lines/concerns | split by responsibility |
| `TF-03` | Hardcoded Values | region, ARN, CIDR, AMI, or IDs are inline | move to variables or data sources |
| `TF-04` | Version Drift | Terraform/provider versions are unbounded | pin with `required_version` and `required_providers` |
| `TF-05` | Reinventing Modules | common modules are reimplemented repeatedly | prefer registry modules unless customization is real |
| `TF-06` | Resource-Type Organization | folders reflect resource type instead of service ownership | organize by service / ownership boundary |
| `TF-07` | Copy-Paste Environments | dev/staging/prod are duplicated trees | share modules, vary config |

## State Management Risks

- Local state for team workflows
- State files committed to VCS
- No state locking
- Manual state surgery without backup or plan
- Too much or too little state splitting

## HCL Quality Risks

| ID | Anti-pattern | Safer pattern |
|----|--------------|---------------|
| `HC-01` | Secrets in plaintext | secrets manager + sensitive vars |
| `HC-02` | No validation | `validation`, `precondition`, `postcondition` |
| `HC-03` | No formatting | pre-commit `terraform fmt` |
| `HC-04` | No documentation | description on every variable/output |
| `HC-05` | Deep nesting | extract locals or submodules |

## Provider And Workspace Risks

- Unpinned providers
- Workspace abuse for highly divergent environments
- Provider configuration hidden inside reusable modules
- Over-abstracting for multi-cloud before there is a real need

## CI/CD Gates

| ID | Anti-pattern | Safer pattern |
|----|--------------|---------------|
| `CI-01` | No plan review | `plan -> review -> approval -> apply` |
| `CI-02` | Console drift | scheduled drift detection |
| `CI-03` | No policy gates | tfsec / Checkov / OPA / Sentinel in CI |
| `CI-04` | `apply -auto-approve` in prod | manual approval in prod |

## 2026 Engine / Feature Gaps

| ID | Anti-pattern | Safer pattern |
|----|--------------|---------------|
| `ENG-01` | Mixing Terraform 1.14 and OpenTofu 1.9 in the same state path on the same project | Pick one engine per project; cross-engine state migrations require a clean `init` + verified diff, never an in-place switch |
| `ENG-02` | Plaintext state on object storage (`encrypt = true` on the S3 backend only protects at-rest server-side, not against the bucket reader) | OpenTofu native client-side state encryption (AES-GCM + AWS KMS / GCP KMS); see `terraform-modules.md` |
| `ENG-03` | Hardcoding sensitive values that should be `ephemeral` (Terraform 1.14+) — token bursts, just-in-time credentials, write-only secret material | Use Terraform `ephemeral` blocks so secrets never land in state; OpenTofu equivalent: `write-only` arguments where supported |
| `ENG-04` | Hand-rolling helper logic in HCL that a provider-defined function could express | OpenTofu provider-defined functions; reuse community-published ones before authoring custom |
