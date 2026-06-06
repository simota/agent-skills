# Docker Patterns

Dockerfile best practices, multi-stage builds, docker-compose, BuildKit optimizations, and security scanning.

Current stable lines (2026-05): **Docker Engine 27.x** (auto-provenance `mode=min` on every `docker buildx build`), **Buildx 0.21+** (GHA cache v2 default, `image-manifest` enabled since BuildKit 0.21), **Compose Spec 5.x "Mont Blanc"** (released Dec 2025; internal builder removed in favour of Bake delegation), **Docker Desktop 4.x / 5.0** (Compose-for-Kubernetes lets you deploy Compose files directly to a cluster without manual conversion). [Source: [Buildx v0.21.0 release](https://github.com/docker/buildx/releases/tag/v0.21.0); [Compose release notes](https://docs.docker.com/compose/release-notes/); [Docker Hardened Images announcement](https://www.docker.com/blog/docker-hardened-images-for-every-developer/)]

---

## Multi-Stage Build (Node.js)

```dockerfile
# syntax=docker/dockerfile:1.10
# ============================================
# Stage 1: Dependencies (pin base by digest, not tag)
# ============================================
FROM node:22-alpine@sha256:<digest> AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Copy package files
COPY package.json pnpm-lock.yaml ./
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
    corepack enable pnpm && pnpm install --frozen-lockfile

# ============================================
# Stage 2: Builder
# ============================================
FROM node:22-alpine@sha256:<digest> AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build application
RUN corepack enable pnpm && pnpm build

# ============================================
# Stage 3: Production
# ============================================
FROM node:22-alpine@sha256:<digest> AS runner
WORKDIR /app

ENV NODE_ENV=production

# Security: Run as non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 appuser

# Copy only necessary files
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

USER appuser

EXPOSE 3000
ENV PORT=3000

# HEALTHCHECK helps Compose/K8s wait for readiness; cheap shallow probe
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD node -e "fetch('http://127.0.0.1:3000/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"

CMD ["node", "dist/index.js"]
```

Use Node 22 LTS (active LTS through Apr 2027) or Node 24 (Oct 2026 release) — Node 20 is in maintenance from Apr 2026. Pin by digest so a hijacked tag cannot silently replace the base layer.

---

## Next.js Optimized Dockerfile

```dockerfile
# ============================================
# Base: Alpine with Node
# ============================================
FROM node:20-alpine AS base
RUN apk add --no-cache libc6-compat
RUN corepack enable pnpm

# ============================================
# Dependencies
# ============================================
FROM base AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# ============================================
# Builder
# ============================================
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Disable telemetry during build
ENV NEXT_TELEMETRY_DISABLED=1

RUN pnpm build

# ============================================
# Production Runner
# ============================================
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy public assets
COPY --from=builder /app/public ./public

# Set correct permissions for prerender cache
RUN mkdir .next
RUN chown nextjs:nodejs .next

# Copy standalone output
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

---

## Distroless / Hardened Base Images (Minimal Attack Surface)

Three production-grade hardened-base families are stable in 2026:

| Family | Origin | License | Provenance |
|--------|--------|---------|-----------|
| Google Distroless | Google | Apache-2.0 | Container Image v1 |
| Chainguard Images (Wolfi) | Chainguard | Apache-2.0 (free public catalog; FIPS / extended-LTS = paid) | SLSA L2, Sigstore-signed, nightly rebuilds |
| Docker Hardened Images (DHI) | Docker | Apache-2.0 (1,000+ images **open-sourced 2025-12-17**) | SLSA L3 provenance, full SBOM, signed |

DHI claims up to 95% CVE reduction vs community images; Wolfi → DHI migration is straightforward because DHI ships an Alpine-like variant. [Source: [Docker — Hardened Images for Everyone](https://www.docker.com/blog/docker-hardened-images-for-every-developer/); [Chainguard vs Docker comparison](https://www.chainguard.dev/compare/chainguard-vs-docker)]

```dockerfile
# Build stage
FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable pnpm && pnpm install --frozen-lockfile
COPY . .
RUN pnpm build

# --- Production: Google Distroless ---
FROM gcr.io/distroless/nodejs22-debian12@sha256:<digest>
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
USER nonroot
EXPOSE 3000
CMD ["dist/index.js"]

# --- Alternative: Chainguard Wolfi (rolling, nightly CVE-patched) ---
# FROM cgr.dev/chainguard/node:latest@sha256:<digest>

# --- Alternative: Docker Hardened Image (since 2025-12) ---
# FROM dhi.docker.com/node:22-debian@sha256:<digest>
```

---

## docker-compose Development

Compose v2 dropped the `version:` field — it has been ignored since 2023 and warns since Compose 2.30. The current schema is the **Compose Specification 5.x** ("Mont Blanc", Dec 2025). Always invoke as `docker compose` (plugin); the standalone `docker-compose` binary is deprecated. [Source: [Compose v2 release notes](https://docs.docker.com/compose/release-notes/); [Compose Develop Spec](https://docs.docker.com/reference/compose-file/develop/)]

```yaml
# compose.yaml  (no top-level `version:` — modern spec)
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: deps  # Stop at deps stage for dev
    volumes:
      - .:/app
      - /app/node_modules  # Anonymous volume for node_modules
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      db:
        condition: service_healthy
    command: pnpm dev

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

---

## .dockerignore

```dockerignore
node_modules
.pnpm-store
dist
.next
.git
.vscode
.env
.env.local
*.log
coverage
Dockerfile*
docker-compose*
.github
```

---

## BuildKit Optimizations

```dockerfile
# syntax=docker/dockerfile:1.10

# Cache mount for package manager (reusable across builds)
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
    corepack enable pnpm && pnpm install --frozen-lockfile

# Parallel build stages
FROM deps AS build-app
COPY src ./src
RUN pnpm build

FROM deps AS build-assets
COPY public ./public
RUN pnpm build:assets

# Merge in final stage
FROM node:22-alpine AS runner
COPY --from=build-app /app/dist ./dist
COPY --from=build-assets /app/public ./public
```

### Cache backends (Buildx)

Pick by environment, not by habit:

| Backend | Use when | Notes |
|---------|----------|-------|
| `type=registry` | Default for multi-runner CI / production | Stores cache as a separate image; works anywhere a registry is reachable. |
| `type=gha` (v2) | GitHub-hosted runners | Buildx 0.21+ reads the v2 endpoint from env; **requires BuildKit ≥ 0.20**. |
| `type=s3` / `type=azblob` | Self-hosted CI on AWS/Azure | Cheap blob storage, OIDC-auth supported. |
| `type=local` | Single dev machine | Not portable. |

`mode=max` caches every intermediate layer (best hit-rate, larger storage); `mode=min` (default) caches only what is exported. For incremental builds the difference between a cache miss and `mode=max` hit is routinely 5 min → 30 s. [Source: [Buildx cache backends](https://docs.docker.com/build/cache/backends/)]

```bash
docker buildx build \
  --cache-from type=registry,ref=ghcr.io/org/app:buildcache \
  --cache-to   type=registry,ref=ghcr.io/org/app:buildcache,mode=max \
  --sbom=true --provenance=mode=max \
  -t ghcr.io/org/app:$(git rev-parse --short HEAD) --push .
```

---

## Docker Security Scanning

Reference scanners (2026):

| Tool | Strengths | Caveats |
|------|-----------|---------|
| Docker Scout | First-party UX, policy gates, SBOM | Tied to Docker ecosystem |
| **Syft + Grype** (Anchore) | Modular: Syft generates SBOM once, Grype rescans on each CVE DB update. ~30-40% faster vulnerability-only scans | Grype is vulnerability-only (no IaC/secret/license scanning) |
| Trivy | All-in-one (CVE, misconfig, secret, license, IaC, K8s) | The Trivy distribution channels were compromised in the 2026-03 TeamPCP campaign — verify the binary via `cosign verify` against the signed release and audit `scan.aquasecurtiy.org` (typosquat C2) before reintroducing |

[Source: [Trivy vs Grype 2026](https://appsecsanta.com/sca-tools/trivy-vs-grype); [SBOM generation tools compared](https://sbomify.com/2026/01/26/sbom-generation-tools-comparison/)]

```bash
# Docker Scout (CVE scan)
docker scout cves myimage:latest --only-severity critical,high

# Generate SBOM via Scout
docker scout sbom myimage:latest --format spdx-json > sbom.json

# Syft + Grype (modular alternative)
syft myimage:latest -o cyclonedx-json=sbom.cdx.json
grype sbom:sbom.cdx.json --fail-on high

# Cosign v3 keyless verify (Fulcio + Rekor v2)
cosign verify ghcr.io/org/app@sha256:<digest> \
  --certificate-identity-regexp "^https://github\.com/org/app/.+" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

```yaml
# CI integration — pin actions to commit SHA, not @v1
- uses: docker/scout-action@<sha>   # was @v1
  with:
    command: cves
    image: ${{ env.IMAGE }}
    only-severities: critical,high
    exit-code: true
```

---

## Compose Watch (Dev Hot Reload)

Watch uses filesystem events (no polling) and — since Compose 5.x — delegates builds to **Docker Bake** for parallel/cached multi-platform rebuilds. [Source: [Compose Develop Spec](https://docs.docker.com/reference/compose-file/develop/)]

```yaml
# compose.yaml
services:
  app:
    build: .
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
        - action: rebuild
          path: package.json
        - action: sync+restart
          path: ./config
          target: /app/config
```

Run with: `docker compose watch`

---

## Compose Bridge (Compose → Kubernetes)

For teams migrating from Compose to Kubernetes, **Compose Bridge** (Docker Desktop 4.43+, July 2025) converts `compose.yaml` to Deployments, Services, ConfigMaps, Secrets, NetworkPolicies, and PVCs in one command. Since Docker Desktop 5.0 (March 2026) the new **Compose for Kubernetes** can deploy Compose files **directly** to a cluster without intermediate manifest generation. Useful for local prod-parity testing; for hand-tuned manifests still hand off to `reference/kubernetes-config.md`. [Source: [Compose Bridge docs](https://docs.docker.com/compose/bridge/); [InfoQ — Docker Desktop 4.43 Kubernetes Bridge](https://www.infoq.com/news/2025/07/docker-desktop-kubernetes-bridge/)]

```bash
# One-shot conversion
docker compose bridge convert -f compose.yaml -o ./k8s/

# Or use as kubectl plugin
kubectl compose-bridge convert -f compose.yaml | kubectl apply -f -
```

---

## Container Runtime Hardening

Combine with the Dockerfile patterns above. Runtime flags belong in compose / orchestrator config, not the Dockerfile.

```yaml
# compose.yaml — hardened runtime
services:
  app:
    image: ghcr.io/org/app@sha256:<digest>
    read_only: true
    tmpfs:
      - /tmp:size=64m
    cap_drop: [ALL]
    cap_add: [NET_BIND_SERVICE]   # only add back what you need
    security_opt:
      - no-new-privileges:true
      - seccomp=./seccomp-profile.json
    user: "1001:1001"
    pids_limit: 200
    ulimits:
      nofile: { soft: 1024, hard: 2048 }
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 10s
```
