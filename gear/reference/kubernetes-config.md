# Kubernetes Operational Config Reference

Purpose: Day-1 and Day-2 in-cluster configuration — Deployment / StatefulSet / Service / Ingress manifests, Helm chart structure, Kustomize overlays, resource requests / limits tuning, HPA / VPA, PodDisruptionBudget, NetworkPolicy, probes. Gear `k8s` configures workloads INSIDE an already-provisioned cluster; it does not create the cluster.

## Scope Boundary

- **Gear `k8s`**: workload configuration after cluster exists. Manifests, Helm, Kustomize, HPA, PDB, probes, resource tuning, NetworkPolicy.
- **Scaffold (IaC)**: cluster PROVISIONING. EKS / GKE / AKS creation via Terraform, VPC, IAM / IRSA / WI roles, node groups / Karpenter, managed addons.

If input is "create the EKS cluster" → `Scaffold`. If input is "deploy this service with HPA and a PDB" → Gear `k8s`. Typical handoff: Scaffold → Gear once `kubectl get nodes` works.

## Config Organization Matrix

| Approach | Pick when | Skip when |
|----------|-----------|-----------|
| Raw manifests + Kustomize | ≤ 5 services, GitOps-native, no templating needs | Complex conditional logic, library reuse |
| Helm chart (owned) | Many knobs, distributing internally, values-driven | Small app with no variability |
| Helm chart (upstream) + values | Deploying ingress-nginx, cert-manager, prometheus, etc. | Need to patch upstream behavior heavily |
| Helm + Kustomize post-render | Need to patch upstream chart's raw output | Pure Helm works |
| cdk8s / Pulumi Kubernetes | Typed-language team, generate manifests programmatically | Team unfamiliar with TS/Python for infra |

Default: Helm for packaged deliverables, Kustomize overlays (base + `overlays/{dev,staging,prod}`) for env differentiation.

## Workflow

```
TUNE     → inspect existing manifests (`kubectl get deploy -o yaml`)
         → check resource usage (`kubectl top pod`) vs requests/limits
         → audit probes, PDB, HPA, NetworkPolicy coverage

TIGHTEN  → pick ONE: resource tuning, HPA addition, probe fix, PDB add, NP add
         → target QoS class (Guaranteed for critical, Burstable for most)
         → decide rolling-update strategy (maxSurge / maxUnavailable)

GREASE   → edit Helm values / Kustomize overlay (never live-edit with `kubectl edit`)
         → `helm template` / `kustomize build` diff against current state
         → apply via CI/CD (ArgoCD / Flux / Helmfile), not local kubectl apply in prod

VERIFY   → rollout succeeds (`kubectl rollout status`)
         → HPA scales on synthetic load; probes pass/fail as expected
         → PDB respected during node drain test
         → NetworkPolicy blocks unauthorized traffic (test from neighboring pod)

PRESENT  → diff summary, resource-change table, rollback command
```

## Resource Requests / Limits

```yaml
resources:
  requests:
    cpu: 100m      # scheduling guarantee
    memory: 256Mi  # OOM-safe floor
  limits:
    cpu: 500m      # throttle ceiling (CPU) — often omit to avoid throttling
    memory: 512Mi  # HARD kill ceiling (memory) — ALWAYS set
```

Rules of thumb:
- **Always set memory request + memory limit** (equal → Guaranteed QoS). OOM is unrecoverable.
- **Set CPU request, consider skipping CPU limit** — CPU throttling often hurts tail latency more than noisy neighbors do (controversial but widely practiced post-2023).
- Measure before setting: p95 usage × 1.5 as a starting point, then adjust.
- Guaranteed QoS (requests == limits) for stateful / critical; Burstable for stateless web tier.

## HPA / VPA

```yaml
# HPA v2
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  scaleTargetRef: { kind: Deployment, name: api }
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource: { name: cpu, target: { type: Utilization, averageUtilization: 70 } }
    - type: Pods
      pods: { metric: { name: http_requests_per_second }, target: { type: AverageValue, averageValue: 100 } }
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # avoid flapping
```

- HPA: scale replicas on CPU / custom metrics (prefer RPS or queue depth over CPU).
- VPA: right-size requests over time — **never run VPA in `Auto` mode alongside HPA on the same resource**; use `Off` (recommendation-only) with HPA.
- Min replicas ≥ 2 for any service behind a PDB.

## PodDisruptionBudget

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
spec:
  minAvailable: 2  # or maxUnavailable: 1
  selector:
    matchLabels: { app: api }
```

- Required for any service in the HA path. Without a PDB, `kubectl drain` can take the whole service down during upgrades.
- `minAvailable` scales with replica count; prefer `maxUnavailable: 1` for fixed-size critical pools.

## NetworkPolicy

Default-deny ingress and egress per namespace, then allow-list. Zero-trust inside the cluster.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: default-deny, namespace: prod }
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
```

CNI must support NetworkPolicy (Calico, Cilium, AWS VPC CNI with policy enabled). If not, fix the cluster layer first (back to Scaffold).

## Probes

```yaml
startupProbe:    # gives slow-boot apps time before liveness kicks in
  httpGet: { path: /healthz, port: 8080 }
  failureThreshold: 30
  periodSeconds: 10
readinessProbe:  # REMOVES pod from Service endpoints — NOT fatal
  httpGet: { path: /ready, port: 8080 }
  periodSeconds: 5
livenessProbe:   # KILLS pod — must be safe to fail briefly
  httpGet: { path: /healthz, port: 8080 }
  periodSeconds: 10
  failureThreshold: 3
```

- `/ready` checks downstream dependencies (DB, cache); `/healthz` checks only self.
- Never make liveness depend on external systems — one DB blip kills the fleet.

## Helm Chart Structure (Owned)

```
charts/my-app/
  Chart.yaml               # name, version, appVersion
  values.yaml              # defaults
  values.schema.json       # validation (Helm 3.5+)
  templates/
    _helpers.tpl
    deployment.yaml
    service.yaml
    ingress.yaml
    hpa.yaml
    pdb.yaml
    networkpolicy.yaml
    servicemonitor.yaml    # if using Prometheus Operator
  templates/tests/
    connection-test.yaml   # `helm test` smoke check
```

Use `values.schema.json` to fail fast on bad values; pin chart version in dependent repos.

## Anti-Patterns

- `kubectl edit` / `kubectl apply -f` in prod — bypasses GitOps, drifts from source.
- No memory limit → OOM-kill the node, not just the pod.
- Liveness probe that hits a DB — cascading failure multiplier.
- No PDB + min replicas 1 → `kubectl drain` = outage.
- `latest` image tag — silent version drift, no rollback. Pin by digest for prod.
- HPA on CPU for an I/O-bound workload — use custom metrics (RPS, queue depth).
- VPA Auto + HPA on CPU → fight each other, oscillation.
- Running as root UID, `privileged: true`, or missing `securityContext` — 28% of 2025 container incidents root-caused here.
- One giant Helm chart for unrelated services — split per service, share via library chart.

## Handoff

- **From Scaffold**: cluster, IRSA / WI roles, CNI + policy enforcement, managed addons, ingress controller.
- **To Gear `alert` / Beacon**: ServiceMonitor / PodMonitor for Prometheus scrape; alert rules.
- **To Gear `secret`**: external-secrets / sealed-secrets integration for app credentials.
- **To Launch**: rollout strategy (rolling / blue-green / canary via Argo Rollouts or Flagger) for release safety.
- **To Bolt**: if requests/limits tuning exposes app-level perf issues (GC pressure, N+1, etc.).
