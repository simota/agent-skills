# Helm Chart Authoring Reference

Purpose: Scaffold a Helm chart that is safe to `helm install` across multiple environments and tenants. Covers `Chart.yaml` metadata, a typed `values.yaml` schema, template best practices, subchart strategy, release lifecycle (install / upgrade / rollback), and rendered-manifest testing — so the chart is reusable, versioned, and reviewable before it reaches a real cluster.

## Scope Boundary

- **Scaffold `helm`**: authoring and packaging a chart for reuse (Chart.yaml, values, templates, subcharts, `values.schema.json`, `helm test`, chart-releaser workflow).
- **Scaffold `k8s`**: single-workload, single-cluster raw manifests. If the workload will never be re-deployed elsewhere, stay on `k8s`.
- **Scaffold `terraform`**: cluster provisioning. The chart runs *on* the cluster Terraform builds.
- **Pipe (elsewhere)**: CI that runs `helm upgrade --install` / `helm diff` / chart-releaser. `helm` scaffolds the chart; `Pipe` ships it.
- **Gateway (elsewhere)**: API rules / auth / rate limit for any Ingress the chart exposes.

Escalate `k8s` → `helm` when any of: (1) same workload, 3+ envs; (2) multi-tenant parameterization; (3) external consumers; (4) the values matrix outgrows kustomize overlays.

## Chart Skeleton

```
my-chart/
  Chart.yaml
  values.yaml
  values.schema.json        # JSON Schema for values (required for reviewable charts)
  templates/
    _helpers.tpl            # named templates, labels, fullname
    deployment.yaml
    service.yaml
    ingress.yaml
    hpa.yaml
    pdb.yaml
    serviceaccount.yaml
    NOTES.txt
    tests/
      test-connection.yaml  # helm test target
  charts/                   # vendored subcharts (if not remote)
  README.md
  .helmignore
```

## Chart.yaml Essentials

```yaml
apiVersion: v2
name: payments-api
description: Payments API service
type: application
version: 0.3.0          # chart version; bump on every release
appVersion: "1.24.3"    # app version; bump independently
kubeVersion: ">=1.28.0-0"
dependencies:
  - name: postgresql
    version: "15.x.x"
    repository: oci://registry-1.docker.io/bitnamicharts
    condition: postgresql.enabled
maintainers:
  - name: platform-team
    email: platform@example.com
annotations:
  artifacthub.io/changes: |
    - kind: added
      description: readiness probe timeout tunable
```

Use SemVer strictly on `version`. Breaking values schema change = major bump. Never reuse a version — chart repos cache aggressively.

## values.yaml Schema

Every chart over trivial size needs `values.schema.json`. It turns typos into install-time failures instead of runtime outages.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["image", "resources"],
  "properties": {
    "replicaCount": { "type": "integer", "minimum": 1 },
    "image": {
      "type": "object",
      "required": ["repository", "tag"],
      "properties": {
        "repository": { "type": "string" },
        "tag": { "type": "string", "pattern": "^(?!latest$).+" },
        "pullPolicy": { "enum": ["Always", "IfNotPresent", "Never"] }
      }
    },
    "resources": {
      "type": "object",
      "required": ["requests"],
      "properties": {
        "requests": { "$ref": "#/$defs/resourceBlock" }
      }
    }
  }
}
```

Forbid `latest` tags in schema. Require `resources.requests`. This is cheaper than debugging "why did prod OOM after the chart bump."

## Template Best Practices

- Use `_helpers.tpl` for `fullname`, `labels`, `selectorLabels`. Never inline `{{ .Release.Name }}-{{ .Chart.Name }}` in multiple templates.
- Quote every string value from `.Values` — unquoted `true`/`false`/numbers silently coerce.
- Use `toYaml | nindent` for structured blocks (resources, nodeSelector, tolerations).
- Gate optional resources with `{{- if .Values.ingress.enabled }}` — avoid rendering empty objects.
- Surface every pod-affecting config change via `checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}` — otherwise pods ignore ConfigMap edits.

```yaml
# templates/deployment.yaml (excerpt)
spec:
  template:
    metadata:
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
      labels:
        {{- include "payments-api.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
```

## Subchart Strategy

| Strategy | Use when | Avoid when |
|----------|----------|------------|
| Remote dependency (`repository:` in Chart.yaml) | Chart is maintained upstream (postgres, redis) | You need to patch upstream behavior |
| Vendored (`helm dependency update` commits tgz) | Air-gapped clusters, immutable supply chain | Upstream iterates weekly |
| Library chart | Shared `_helpers.tpl` across 3+ app charts | Only one chart needs it |

Never fork a public chart into `templates/` — diff drift is permanent. Patch via values first; if that fails, write a thin wrapper chart.

## Release Lifecycle

```
helm lint ./my-chart                          # static checks
helm template ./my-chart -f values-prod.yaml  # render without installing
helm install --dry-run --debug ...            # server-side validate
helm upgrade --install ... --atomic --timeout 5m
helm test <release>                           # run tests/ hooks
helm rollback <release> <revision>            # on failure
```

`--atomic` rolls back automatically on failed upgrade. Always use it outside of hotfix exceptions. `--timeout` must exceed the slowest startup probe.

## Rendered-Manifest Testing

Treat rendered output as a review artifact. Run in CI:

- **helm lint + helm template** with committed golden files for regression diffing.
- **helm-unittest** (`quintush/helm-unittest`) for template unit tests.
- **kubeconform** / **kubeval** on rendered output — schema-validates against the target Kubernetes version.
- **helm test** post-install — a hook pod (annotation `"helm.sh/hook": test`) that curls the Service's `/healthz`.

## Anti-Patterns

- Editing `charts/` vendored tarballs by hand — changes disappear on next `helm dependency update`.
- Shipping without `values.schema.json` — typos go undetected until runtime.
- `hook-delete-policy: before-hook-creation` on destructive hooks — catastrophic on upgrade.
- Storing secrets in `values.yaml` — use `--set` from a secret manager or ESO, never commit plaintext.
- Reusing chart `version` — Helm repos cache the first tarball forever; consumers never get the fix.
- Forking public charts into `templates/` — you own every future CVE and compatibility break.
- Cross-namespace hardcoded references in templates — breaks multi-tenant installs.
- `--force` on `helm upgrade` as a habit — recreates resources and can cause downtime on Services with NodePort/LoadBalancer.
- No `checksum/config` annotation on pods — ConfigMap updates silently do nothing until the next rollout.
- Coupling Chart version to appVersion 1:1 — blocks chart-only fixes without an app release.

## Handoff

When the chart is ready:

- **To Pipe**: the CI contract — `helm lint`, `helm template | kubeconform`, `helm-unittest`, `helm upgrade --install --atomic`, `helm test`, and chart-releaser / OCI push steps.
- **To Sentinel**: values-driven RBAC scope, `ServiceAccount` and `NetworkPolicy` behavior under default values, and the secret hydration path (ESO / CSI / sealed).
- **To Beacon**: metrics, scrape labels, and default alert thresholds encoded in the chart (or intentionally deferred to consumer).
- **To Gateway**: Ingress behavior the chart installs — host rules, TLS, auth annotations — so Gateway can enforce API contract.
- **To Canvas**: release topology — chart → releases → namespaces → workloads — for ecosystem diagrams.
- **Consumer docs**: README must list required values, schema link, upgrade notes, and known breaking changes per minor version.
