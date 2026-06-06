# Terraform Compliance And Policy-as-Code

Purpose: Use this file when you need static analysis, policy gates, custom validation, or Terraform linting rules.

Contents:
1. Tool matrix
2. Key tfsec / Checkov rules
3. OPA / Sentinel enforcement
4. Terraform built-in validation
5. Pre-commit and TFLint

## Tool Matrix

| Tool | Best for |
|------|----------|
| `terraform validate` | syntax and type checks |
| `tfsec` / `trivy config` | quick security scanning |
| `Checkov` | broad compliance coverage |
| `OPA` / `Conftest` | custom organizational policies |
| `Sentinel` | HCP Terraform / Enterprise policy gates |
| `TFLint` | provider-aware linting |

## Key tfsec / Checkov Rules

### tfsec / Trivy examples

| Rule ID | Meaning | Severity |
|---------|---------|----------|
| `AVD-AWS-0089` | S3 bucket public access | CRITICAL |
| `AVD-AWS-0107` | RDS without encryption | HIGH |
| `AVD-AWS-0104` | Security group with unrestricted ingress | HIGH |
| `AVD-AWS-0178` | ECS task definition runs as root | HIGH |
| `AVD-GCP-0029` | Cloud SQL without SSL | HIGH |
| `AVD-GCP-0024` | GKE without network policy | MEDIUM |

### Checkov examples

| Check ID | Meaning |
|----------|---------|
| `CKV_AWS_79` | IMDSv2 enforced |
| `CKV_AWS_88` | EC2 public IP disabled |
| `CKV_AWS_145` | RDS encryption enabled |
| `CKV_GCP_6` | Cloud SQL has no public IP |
| `CKV_GCP_12` | GKE network policy enabled |

## OPA / Sentinel Enforcement

Required tags in policy examples:
- `Environment`
- `Project`
- `ManagedBy`

Security policy example should block unnecessary `0.0.0.0/0` ingress.

Sentinel enforcement levels:

| Level | Behavior |
|-------|----------|
| `advisory` | warn only |
| `soft-mandatory` | block, override possible |
| `hard-mandatory` | block, no override |

## Terraform Built-In Validation

```hcl
variable "environment" {
  type = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}
```

Use lifecycle preconditions/postconditions for non-trivial invariants.

## Pre-Commit And TFLint

Pre-commit should typically include:
- `terraform_fmt`
- `terraform_validate`
- `terraform_tflint`
- `checkov` or `trivy`

TFLint is the provider-aware linter for:
- invalid instance or database types
- naming conventions
- unused declarations
