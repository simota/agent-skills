# Gear Recipe Registry

The full Recipe table for `gear`. `gear/SKILL.md` carries only the dispatch
allowlist; this file holds what is needed to *execute* a Recipe — activation
condition and the files to read first.

**Read this when** a subcommand matched and you need its row, or when scanning
what Recipes exist at all.

---

| Recipe | Subcommand | Default? | When to Use | Read First |
|--------|-----------|---------|-------------|------------|
| Dependency Management | `deps` | ✓ | Dependency management and upgrades | `reference/dependency-management.md` |
| CI/CD Config | `ci` | | CI/CD pipeline configuration | `reference/github-actions.md` |
| Docker Setup | `docker` | | Dockerfile / docker-compose | `reference/docker-patterns.md` |
| Logging Setup | `logs` | | Logging configuration (structured logs, etc.) | `reference/observability.md` |
| Health Checks | `health` | | Health check design | `reference/observability.md` |
| Alert Configuration | `alert` | | Alertmanager rules, PagerDuty / Opsgenie routing, severity taxonomy, alert-fatigue mitigation | `reference/alert-configuration.md` |
| Secrets Management | `secret` | | Vault / AWS Secrets Manager / Doppler, .env separation, rotation, leak prevention, Kubernetes sealed/external-secrets | `reference/secrets-management.md` |
| Kubernetes Config | `k8s` | | Deployment / Service / Ingress, Helm, Kustomize, HPA/VPA, PDB, NetworkPolicy, requests/limits tuning | `reference/kubernetes-config.md` |
| GitHub Actions Architecture | `gha` | | New or advanced GHA workflows; select `workflow|reusable|security|pr-automation|matrix|cache|secret` mode | `reference/gha-triggers-and-events.md`, matching `reference/gha-*.md` |
