# Terraform Operations

Purpose: Use this file when working with state, import, drift detection, workspaces, module versioning, or backend migration.

Contents:
1. State command safety
2. Moved blocks and import
3. Workspace guidance
4. Drift detection
5. Versioning and backend migration

## State Command Safety

| Command | Purpose | Risk |
|---------|---------|------|
| `terraform state list` | List state addresses | Safe |
| `terraform state show <addr>` | Inspect a state entry | Safe |
| `terraform state mv <src> <dst>` | Refactor state addresses | Medium |
| `terraform state rm <addr>` | Stop managing a resource | High |
| `terraform state pull` | Download remote state | Safe |
| `terraform state push` | Upload local state | High |
| `terraform state replace-provider` | Provider rewrite | Medium |

## Moved Blocks And Import

Prefer declarative `moved` blocks over ad hoc `terraform state mv`.

```hcl
moved {
  from = aws_instance.web
  to   = aws_instance.app
}
```

Best practice: keep `moved` blocks for `2-3 months` after apply, then remove them.

Prefer Terraform `import` blocks on `1.5+`:

```hcl
import {
  to = aws_s3_bucket.existing
  id = "my-existing-bucket-name"
}
```

## Workspace Guidance

| Approach | Use when | Recommendation |
|----------|----------|----------------|
| Workspaces | Same config, different state | small/simple projects |
| Directory-per-env | Different config per env | complex projects; recommended default |
| Terragrunt | Shared multi-env orchestration | large estates |

## Drift Detection

```bash
terraform plan -detailed-exitcode -out=drift.tfplan
terraform plan -refresh-only
terraform apply -refresh-only
```

Interpretation:
- `0` = no drift
- `1` = error
- `2` = changes detected

## Versioning And Backend Migration

- Pin Terraform with `>= 1.5.0, < 2.0.0`.
- Pin providers with bounded constraints such as `~> 5.0`.
- Upgrade through `dev -> staging -> prod`.

Backend migration pattern:

```bash
terraform state pull > terraform.tfstate.backup
terraform init -migrate-state
terraform plan
```

`terraform plan` after migration should show no changes.
