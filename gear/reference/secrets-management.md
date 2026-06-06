# Secrets Management Reference

Purpose: Design the secret-management architecture — choose the backend (Vault vs AWS Secrets Manager vs Doppler), define rotation policies, separate `.env` per environment, prevent CI-secret leaks, and wire Kubernetes sealed-secrets or external-secrets. Gear `secret` does NOT scan for already-leaked secrets in code; it designs the system that prevents leaks in the first place.

## Scope Boundary

- **Gear `secret`**: architecture. Backend selection, rotation cadence, lease TTL, `.env` hygiene per env, sealed-secrets vs external-secrets decision, CI-leak prevention tooling, least-privilege auth paths (AppRole, IRSA, Workload Identity).
- **Sentinel (secret scanning)**: static audit. Grep-style repo scan for hardcoded API keys, tokens, `.env` committed by mistake. Complementary, not overlapping.

If input is "did we commit an AWS key last month?" → `Sentinel`. If input is "design Vault + rotation for this service" → Gear `secret`. Typical flow: Gear designs → Sentinel audits before deploy → Gear patches if findings.

## Backend Matrix

| Backend | Pick when | Skip when |
|---------|-----------|-----------|
| HashiCorp Vault (OSS / HCP) | Multi-cloud, dynamic DB creds, PKI, strong audit needs | Team can't operate a Vault cluster |
| AWS Secrets Manager | AWS-only, want managed + auto-rotation Lambdas | Multi-cloud or want dynamic secrets |
| GCP Secret Manager | GCP-only | Multi-cloud |
| Azure Key Vault | Azure-only, HSM-backed needs | Multi-cloud |
| Doppler | SaaS-first team, fast onboarding, good DX | Air-gapped / strict compliance (FedRAMP, etc.) |
| 1Password / Bitwarden Secrets | Small team, dev-secret focus | Production workloads |
| Kubernetes sealed-secrets (Bitnami) | GitOps-native, want secrets in Git (encrypted) | Need dynamic / short-TTL secrets |
| external-secrets operator | Kubernetes app pulls from Vault / SM / Doppler | Non-K8s stack |

Default: Vault for regulated / multi-cloud; AWS SM for AWS-only; Doppler for small fast-moving teams; external-secrets for K8s apps fronting any of the above.

## Workflow

```
TUNE     → inventory current secrets (env vars, .env files, CI vars, K8s Secrets)
         → map who/what accesses each: humans, CI jobs, services
         → classify by blast radius (prod DB creds vs dev SMTP)

TIGHTEN  → pick ONE scope: one app, one env, one backend migration
         → decide rotation cadence per class (90d static, 1h dynamic DB)
         → pick auth method (AppRole, IRSA, Workload Identity, K8s ServiceAccount)

GREASE   → provision backend path / namespace via Terraform
         → wire app via SDK or sidecar (Vault Agent, external-secrets)
         → add pre-commit hooks (trufflehog / gitleaks / detect-secrets)
         → add CI job: `gitleaks detect --redact` on PR

VERIFY   → rotate one secret end-to-end (old → new → old revoked)
         → confirm app picks up new value without restart (if dynamic)
         → confirm CI fails on planted test secret (leak-detection smoke test)

PRESENT  → architecture diagram, rotation schedule, runbook for break-glass
```

## .env Separation Strategy

```
.env.example         # committed, placeholder values only
.env.local           # gitignored, dev-only, per-developer
.env.development     # gitignored, shared dev env
.env.staging         # NEVER on disk; fetched from backend at runtime
.env.production      # NEVER on disk; fetched from backend at runtime
```

- `.env.example` is the single source of truth for what keys must exist.
- Staging / prod values never touch a developer laptop.
- Frameworks that load `.env.production` from disk (Next.js default) must be configured to pull from backend instead.

## Rotation Policy

| Secret Class | Cadence | Mechanism |
|--------------|---------|-----------|
| DB password (static) | 90 days | SM rotation Lambda / Vault DB engine |
| DB credentials (dynamic) | 1 hour lease | Vault DB engine (Postgres / MySQL plugin) |
| Cloud IAM user keys | 60 days | SM rotation or replace with IRSA / WI |
| API keys (third-party) | per-vendor policy, max 180d | Vault KV v2 + manual rotation runbook |
| TLS certs | Let's Encrypt 60-90d, internal 1y | cert-manager + ACME |
| SSH / signing keys | 1 year | Vault SSH / PKI engine |

Default to **dynamic over static** wherever the backend supports it — eliminates rotation as a human task.

## CI-Secret Leak Prevention

- **Pre-commit**: `detect-secrets scan --baseline .secrets.baseline` or `gitleaks protect --staged`.
- **PR check**: `gitleaks detect --redact` + `trufflehog git file://. --only-verified` as required CI status.
- **Server-side**: GitHub Push Protection enabled at org level (blocks known secret formats).
- **History rewrite ban**: leaked secrets are ROTATED, not rewritten out of history — rotation is the only defense that works.
- **CI job secrets**: use OIDC to cloud (short-lived tokens) instead of static `AWS_ACCESS_KEY_ID` vars whenever possible.

## Kubernetes Patterns

| Pattern | Use when |
|---------|----------|
| sealed-secrets (Bitnami) | GitOps workflow, secrets committed encrypted; simple threat model |
| external-secrets operator | App pulls from Vault / SM / Doppler at runtime; best for dynamic / rotated secrets |
| CSI Secrets Store Driver | Mount secrets as files, sync to env vars; good for rotation without pod restart |
| Native `Secret` resource | Throwaway dev-cluster only — base64 is NOT encryption |

Production rule: never use raw `kind: Secret` as the source of truth. Source = Vault / SM / sealed-secrets.

## Anti-Patterns

- `.env` files committed then force-pushed out of history — assume leaked, rotate every value.
- Long-lived AWS IAM user access keys on CI — use OIDC / IRSA.
- Rotating a secret without updating downstream consumers — schedule overlap window ≥ 1 rotation interval.
- Single `admin` Vault token used by every app — use AppRole or K8s auth, least-privilege policies.
- Sealed-secrets without controller key backup — losing the key bricks every encrypted secret.
- Shipping a secret into a container image layer — image is public surface, layers are cacheable.
- Echoing secrets into CI logs (`echo $API_KEY`) — mask them or fail the job.

## Handoff

- **To Sentinel**: post-design static scan to confirm repo is clean before rollout.
- **To Scaffold**: IAM / IRSA / Workload Identity role provisioning that Gear's auth method depends on.
- **To Crypt**: when the design needs HSM, envelope encryption, or custom key hierarchy.
- **To Comply**: SOC2 / PCI-DSS / HIPAA mapping of rotation cadence and audit trail.
