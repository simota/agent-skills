# Security And Environment Patterns

Purpose: Use this file when the task involves secrets, IAM, network controls, `.env` templates, or environment validation.

Contents:
1. Secrets strategy
2. IAM least privilege
3. Network guardrails
4. Pre-commit hooks
5. `.env.example`
6. Zod validation

## Secrets Strategy

| Approach | Use when | Notes |
|----------|----------|-------|
| `.env` (gitignored) | Local development only | never commit |
| Cloud Secrets Manager | Staging and production | preferred for secrets |
| Parameter Store | Non-sensitive runtime config | lighter-weight option |
| Vault | Enterprise / multi-cloud | centralized secret lifecycle |

Terraform pattern:

```hcl
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "/${var.project_name}/${var.environment}/db-password"
}

resource "aws_db_instance" "main" {
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}
```

## IAM Least Privilege

- Scope actions and resources narrowly.
- Prefer roles or workload identity over long-lived keys.
- Separate service accounts/roles per workload.
- Enforce MFA or equivalent admin controls where applicable.

## Network Guardrails

- Prefer security-group-to-security-group rules over wide CIDR rules.
- Default outbound should be explicit where the platform allows it.
- Treat `0.0.0.0/0` as an exception requiring justification and policy review.

Example:

```hcl
ingress {
  from_port       = var.app_port
  to_port         = var.app_port
  protocol        = "tcp"
  security_groups = [aws_security_group.alb.id]
}
```

## Pre-Commit Hooks

```yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.86.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_tflint

  - repo: https://github.com/bridgecrewio/checkov
    rev: 3.1.0
    hooks:
      - id: checkov

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

## `.env.example`

```bash
NODE_ENV=development
PORT=3000
APP_URL=http://localhost:3000
DATABASE_URL=postgresql://user:password@localhost:5432/app_dev
REDIS_URL=redis://localhost:6379
JWT_SECRET=REPLACE_WITH_SECURE_SECRET
SESSION_SECRET=REPLACE_WITH_SECURE_SECRET
FEATURE_NEW_UI=false
LOG_LEVEL=debug
```

## Zod Validation

```typescript
export const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'staging', 'production']).default('development'),
  PORT: z.coerce.number().default(3000),
  APP_URL: z.string().url(),
  DATABASE_URL: z.string().url(),
  REDIS_URL: z.string().url().optional(),
  JWT_SECRET: z.string().min(32),
  SESSION_SECRET: z.string().min(32),
  FEATURE_NEW_UI: z.coerce.boolean().default(false),
  LOG_LEVEL: z.enum(['error', 'warn', 'info', 'debug']).default('info'),
});
```
