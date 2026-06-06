# Docker / Dev Environment Anti-Patterns

Purpose: Use this file when reviewing Docker Compose, container design, Dockerfiles, or secret handling for local environments.

Contents:
1. Container anti-patterns
2. Compose anti-patterns
3. Secret anti-patterns
4. Local-dev anti-patterns
5. Dockerfile anti-patterns

## Container Anti-Patterns

| ID | Anti-pattern | Signal | Safer pattern |
|----|--------------|--------|---------------|
| `DC-01` | Multi-Concern Container | app + DB + reverse proxy + SSH in one image | one service / one process |
| `DC-02` | Dev = Prod Image | production image contains compilers/test tools | multi-stage build |
| `DC-03` | Different Images Per Env | each environment uses a different Dockerfile | single image, env-specific config |
| `DC-04` | Fat Image | image size `>1GB` or lots of unused packages | `.dockerignore`, multi-stage, smaller base |
| `DC-05` | `latest` Tag Dependency | unpinned base images | pin tags or digests |
| `DC-06` | Root User Default | container runs as root | non-root `USER` |
| `DC-07` | Secrets in Image Layer | secrets copied or baked into build layers | runtime secrets or BuildKit secrets |

## Compose Anti-Patterns

- Secrets committed in YAML
- No health checks
- Over-broad bind mounts
- No resource limits
- Default bridge with no deliberate network design
- YAML override complexity spiral

## Secret Anti-Patterns

| ID | Anti-pattern | Safer pattern |
|----|--------------|---------------|
| `SE-01` | Secrets in env vars for sensitive production use | Docker secrets or cloud secret stores |
| `SE-02` | Committed `.env` files | `.gitignore` + `.env.example` |
| `SE-03` | Build-time secrets left in layers | BuildKit secret mount |
| `SE-04` | No rotation | managed rotation or rotation runbook |

## Local-Dev Anti-Patterns

- “Works on my machine” dependencies outside Docker
- No hot reload
- Missing seed data
- Platform mismatch between `amd64` and `arm64`
- Using Compose as the production orchestrator

## Dockerfile Anti-Patterns

| ID | Anti-pattern | Safer pattern |
|----|--------------|---------------|
| `DF-01` | No `.dockerignore` | ignore `.git`, `.env`, `node_modules`, test artifacts |
| `DF-02` | Poor layer ordering | copy lockfiles before source |
| `DF-03` | No cache optimization | order low-change layers first |
| `DF-04` | Too many `RUN` layers | consolidate where sensible |
