# Terraform / OpenTofu Module Templates

Purpose: Use this file when you need Terraform / OpenTofu layout, module boundaries, backend configuration, or reusable AWS-first module patterns.

Contents:
1. Engine selection (Terraform vs OpenTofu, 2026)
2. Recommended repository layout
3. Module design rules
4. Backend patterns
5. Minimal module skeletons

## Engine Selection (2026-05 snapshot)

Both engines speak HCL and consume the same modules; the choice is primarily **license** and **feature set**:

| Engine | License | Current line | Picks itself when... |
|--------|---------|----------------|----------------------|
| HashiCorp **Terraform** | Business Source License v1.1 (since Aug 2023) | `1.14.x` (2026), `1.15` in alpha | Existing HCP / Terraform Cloud / Sentinel investment, or `ephemeral` values feature is required |
| **OpenTofu** | MPL 2.0 (community fork) | `1.9.x` | Greenfield project, or you need **state encryption** (AES-GCM / AWS KMS / GCP KMS at-rest), or you need provider-defined functions, or BSL is a procurement blocker |

Adoption signal (April 2026): OpenTofu sits at `~12%` of IaC practitioners with `~27%` planning to evaluate. New projects in 2026 default to **OpenTofu** unless the team is already committed to HCP/Terraform Cloud features that have no OpenTofu equivalent. Existing Terraform `~> 1.5` projects migrate when state encryption or BSL avoidance becomes load-bearing — both engines remain backwards-compatible with HCL written for the other.

### Picking The Version Constraint

```hcl
terraform {
  required_version = ">= 1.9.0"  # OpenTofu 1.9.x baseline OR Terraform 1.14.x — both honour this

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

Lock with a bounded constraint (`~> 5.0`) — never leave provider versions unbounded; both engines hit the same provider supply-chain risks.

## Recommended Repository Layout

```text
modules/
  vpc/
  rds/
  ecs/
environments/
  dev/
  staging/
  prod/
```

## Module Design Rules

- Root module owns providers, backend, and environment wiring.
- Child modules own one responsibility only.
- `required_version` should be `>= 1.9.0` (covers both OpenTofu 1.9.x and Terraform 1.14.x).
- Pin providers with bounded constraints such as `~> 5.0`.
- Validate user-facing variables.
- Expose only necessary outputs.
- Merge common tags/labels centrally.
- For OpenTofu, prefer **encrypted state** (see backend section) — leaving state unencrypted in S3 / GCS exposes IAM ARNs, secrets references, and resource metadata to whoever can read the bucket.

## Backend Patterns

| Backend | Use when | Notes |
|---------|----------|-------|
| S3 + DynamoDB | AWS teams | server-side encryption + locking required |
| GCS | GCP teams | separate bucket prefix per environment |
| Azure Blob | Azure teams | isolate by container/key |
| HCP Terraform / Terraform Cloud | Already using HCP for runs, policy-as-code | BSL-licensed; tied to Terraform 1.14.x line |

Example (Terraform, S3 backend):

```hcl
terraform {
  backend "s3" {
    bucket         = "myproject-terraform-state"
    key            = "dev/terraform.tfstate"
    region         = "ap-northeast-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

### OpenTofu Client-Side State Encryption

OpenTofu 1.9.x ships native, configurable encryption of the state file itself, including remote state. This protects sensitive resource attributes when the storage backend (S3, GCS, Azure Blob) is compromised or misconfigured.

```hcl
terraform {
  encryption {
    # Key provider — AWS KMS / GCP KMS / raw key
    key_provider "aws_kms" "main" {
      kms_key_id = "alias/opentofu-state-key"
      region     = "ap-northeast-1"
    }

    # Encryption method
    method "aes_gcm" "main" {
      keys = key_provider.aws_kms.main
    }

    # Apply to local + remote state
    state    { method = method.aes_gcm.main }
    plan     { method = method.aes_gcm.main }
  }

  backend "s3" {
    bucket = "myproject-tofu-state"
    key    = "dev/terraform.tfstate"
    region = "ap-northeast-1"
  }
}
```

When migrating an existing project to OpenTofu encryption, configure the `key_provider` block first, run `tofu init` and `tofu apply` with `enforced = false` (the default), then flip `enforced = true` once every state path is confirmed encrypted. Never roll out `enforced = true` without a verified rollback for the encryption keys — losing the KMS key equals losing the state.

## Minimal Module Skeleton

### VPC-style module

```hcl
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}
```

### Variable validation

```hcl
variable "environment" {
  type = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}
```

### Outputs

```hcl
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}
```
