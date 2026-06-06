# Observability Templates

Structured logging, health checks, error tracking, metrics collection, alerting, and distributed tracing.

Signal-maturity snapshot (OpenTelemetry, 2026-05):

| Signal | Status | Notes |
|--------|--------|-------|
| Traces | **Stable** (since 2021, all major SDKs) | OTLP wire format and semantic conventions stable |
| Metrics | **Stable** in most SDKs (JS/Java/Go/.NET/Python) | Some host metric instrumentations still Beta |
| Logs | **Stable** in spec; SDK GA progressing through 2024-2026 | Bridge appenders for Pino/Winston/Log4j/slf4j are production-ready |
| **Profiling (4th signal)** | **Release Candidate** Q1 2026, GA target Q3 2026 | pprof-compatible OTLP profile signal |

SDK version notes (2026-05):
- **OTel JS SDK 2.0** (released 2025-02): minimum Node.js raised to `^18.19.0 || >=20.6.0` (Node 14/16 dropped); TypeScript minimum 5.0.4; compile target ES2022. Classes/namespaces replaced with plain objects for better tree-shaking. `InstrumentationLibrary` → `InstrumentationScope`. See [migration guide](https://github.com/open-telemetry/opentelemetry-js/blob/main/doc/upgrade-to-2.x.md) before upgrading. [Source: [OTel JS SDK 2.0 announcement](https://opentelemetry.io/blog/2025/otel-js-sdk-2-0/)]
- **OTel Collector** latest stable: v1.x line (v1.52.0 as of 2026-05). The Release SIG is targeting "epoch" releases — a tested, stable component manifest for production pinning. [Source: [OTel Collector releases](https://github.com/open-telemetry/opentelemetry-collector/releases)]

[Source: [OpenTelemetry stability docs](https://opentelemetry.io/docs/concepts/signals/); [OpenTelemetry stabilization proposal](https://opentelemetry.io/blog/2025/stability-proposal-announcement/)]

The OTel Collector, semantic conventions for GenAI/AI agent workloads, and declarative YAML config are detailed in the dedicated section near the end of this file. Pair this reference with `Beacon` for SLO/alert *strategy* — Gear configures the plumbing, Beacon defines what is worth alerting on.

---

## Structured Logging (Pino)

Pino 9 (current stable, 2026-05) is ~7× faster than Winston with worker-thread transports. Pair with `@opentelemetry/instrumentation-pino` to auto-inject `trace_id` / `span_id` into every log line. [Source: [@opentelemetry/instrumentation-pino](https://www.npmjs.com/package/@opentelemetry/instrumentation-pino)]

```typescript
// src/lib/logger.ts
import pino from 'pino';

export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
  // Redact sensitive fields
  redact: ['req.headers.authorization', 'password', 'token', 'apiKey'],
  transport: process.env.NODE_ENV === 'development'
    ? { target: 'pino-pretty' }
    : {
        // Production: send logs to OTel Collector via worker-thread transport
        target: 'pino-opentelemetry-transport',
        options: {
          resourceAttributes: {
            'service.name': process.env.SERVICE_NAME,
            'service.version': process.env.SERVICE_VERSION,
          },
        },
      },
});

// Usage: logger.info({ userId, action }, 'User performed action');
// → JSON output is automatically enriched with trace_id/span_id when inside an active span
```

---

## Winston Alternative

```typescript
// src/lib/logger.ts
import winston from 'winston';

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: process.env.SERVICE_NAME },
  transports: [
    new winston.transports.Console({
      format: process.env.NODE_ENV === 'development'
        ? winston.format.simple()
        : winston.format.json(),
    }),
  ],
});
```

---

## Health Check Endpoint

```typescript
// src/routes/health.ts
import { Router } from 'express';
import { prisma } from '../lib/db';
import { redis } from '../lib/redis';

const router = Router();

interface HealthCheck {
  status: 'ok' | 'degraded' | 'unhealthy';
  timestamp: string;
  uptime: number;
  checks: {
    database: boolean;
    redis: boolean;
    memory: { used: number; total: number };
  };
}

router.get('/health', async (req, res) => {
  const checks = {
    database: await checkDatabase(),
    redis: await checkRedis(),
    memory: {
      used: process.memoryUsage().heapUsed,
      total: process.memoryUsage().heapTotal,
    },
  };

  const healthy = checks.database && checks.redis;
  const response: HealthCheck = {
    status: healthy ? 'ok' : 'degraded',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    checks,
  };

  res.status(healthy ? 200 : 503).json(response);
});

async function checkDatabase(): Promise<boolean> {
  try {
    await prisma.$queryRaw`SELECT 1`;
    return true;
  } catch {
    return false;
  }
}

async function checkRedis(): Promise<boolean> {
  try {
    await redis.ping();
    return true;
  } catch {
    return false;
  }
}

export { router as healthRouter };
```

---

## Sentry Error Tracking

```typescript
// src/lib/sentry.ts
import * as Sentry from '@sentry/node';

export function initSentry() {
  if (!process.env.SENTRY_DSN) return;

  Sentry.init({
    dsn: process.env.SENTRY_DSN,
    environment: process.env.NODE_ENV,
    tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,
    integrations: [
      Sentry.httpIntegration(),
      Sentry.expressIntegration(),
    ],
  });
}

// Express error handler
export const sentryErrorHandler = Sentry.expressErrorHandler();
```

---

## Prometheus Metrics

```typescript
// src/lib/metrics.ts
import { Registry, Counter, Histogram, collectDefaultMetrics } from 'prom-client';

export const register = new Registry();
collectDefaultMetrics({ register });

export const httpRequestsTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'path', 'status'],
  registers: [register],
});

export const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration',
  labelNames: ['method', 'path'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 5],
  registers: [register],
});

// Middleware
export function metricsMiddleware(req, res, next) {
  const start = Date.now();
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    httpRequestsTotal.inc({
      method: req.method,
      path: req.route?.path || req.path,
      status: res.statusCode,
    });
    httpRequestDuration.observe(
      { method: req.method, path: req.route?.path || req.path },
      duration,
    );
  });
  next();
}

// Endpoint: GET /metrics
```

---

## Alert Rules (Prometheus / Alertmanager)

Use **Prometheus 3.x** (GA 2024-11; Grafana Alloy bumped its embedded Prometheus from 2.55 → 3.4 in 2026). Key v3 changes to be aware of:
- OTLP ingestion is **stable** at `/api/v1/otlp/v1/metrics`; use `otlp/http` exporter from OTel Collector directly. [Source: [Prometheus OTLP guide](https://prometheus.io/docs/guides/opentelemetry/)]
- **Native histograms** stable from v3.8.0 (requires `scrape_native_histograms: true` in scrape config). [Source: [Prometheus 3.0 announcement](https://prometheus.io/blog/2024/11/14/prometheus-3-0/)]
- **Remote Write 2.0**: natively transports native histograms, exemplars, metadata, and created timestamps — still experimental; enable with `send_native_histograms: true` in remote_write config. [Source: [Remote-Write 2.0 spec](https://prometheus.io/docs/specs/prw/remote_write_spec_2_0/)]
- **Regex change**: `.` now matches newline in PromQL label matchers — audit existing rules that relied on the old behaviour.
- UTF-8 metric/label names supported natively — no more dot-to-underscore mangling for OTel metrics.
Grafana 13.x adds dashboards-as-code and Grafana-managed recording rules.

The thresholds below are a **starter template**, not an SLO strategy — route SLO/burn-rate alert design to `Beacon`.

### SLO burn-rate alerting (Google SRE multi-window, multi-burn-rate)

Industry consensus in 2026: replace single-window threshold alerts with **multi-window multi-burn-rate (MWMBR)** — both a fast (5 min) and a slow (1 hour) window must breach simultaneously, dramatically reducing flapping while keeping detection latency low. [Source: [Google SRE Workbook — Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)]

| Tier | Burn rate | Short window | Long window | Severity |
|------|-----------|--------------|-------------|----------|
| 1 (Page) | 14.4× | 5 min | 1 h | P1 |
| 2 (Page) | 6× | 30 min | 6 h | P2 |
| 3 (Ticket) | 3× | 2 h | 24 h | P3 |
| 4 (Ticket) | 1× | 3 d | 30 d | P4 |

```yaml
# alertmanager/rules/app.yml — mix of legacy threshold and SLO burn-rate examples
groups:
  - name: application
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }} over last 5 minutes"

      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "p95 latency is {{ $value }}s"

      - alert: HealthCheckFailing
        expr: up{job="app"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Health check failing"

  # --- SLO burn-rate (Tier 1: 14.4x, 5 min AND 1 h) ---
  - name: slo-burn
    rules:
      - alert: SLOBurnRateFast
        expr: |
          (
            sum(rate(http_requests_total{status=~"5..",job="app"}[5m]))
            / sum(rate(http_requests_total{job="app"}[5m])) > (14.4 * 0.001)
          )
          and
          (
            sum(rate(http_requests_total{status=~"5..",job="app"}[1h]))
            / sum(rate(http_requests_total{job="app"}[1h])) > (14.4 * 0.001)
          )
        labels:
          severity: page
          tier: "1"
        annotations:
          summary: "Burning SLO budget at 14.4x (P1 page)"
```

---

## OpenTelemetry Setup (Node.js SDK)

The Node.js SDK (`@opentelemetry/sdk-node` 1.x) covers traces, metrics, and logs — wire all three so OTLP-compatible backends (Tempo, Jaeger, SigNoz, Honeycomb, Grafana Cloud, Datadog, etc.) receive a single correlated stream.

```typescript
// src/lib/telemetry.ts
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-http';
import { OTLPLogExporter } from '@opentelemetry/exporter-logs-otlp-http';
import { PeriodicExportingMetricReader } from '@opentelemetry/sdk-metrics';
import { BatchLogRecordProcessor } from '@opentelemetry/sdk-logs';
import { resourceFromAttributes } from '@opentelemetry/resources';
import {
  ATTR_SERVICE_NAME,
  ATTR_SERVICE_VERSION,
  ATTR_DEPLOYMENT_ENVIRONMENT_NAME,
} from '@opentelemetry/semantic-conventions';

const endpoint = process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://localhost:4318';

const sdk = new NodeSDK({
  resource: resourceFromAttributes({
    [ATTR_SERVICE_NAME]: process.env.SERVICE_NAME ?? 'app',
    [ATTR_SERVICE_VERSION]: process.env.SERVICE_VERSION ?? '0.0.0',
    [ATTR_DEPLOYMENT_ENVIRONMENT_NAME]: process.env.NODE_ENV ?? 'development',
  }),
  traceExporter: new OTLPTraceExporter({ url: `${endpoint}/v1/traces` }),
  metricReader: new PeriodicExportingMetricReader({
    exporter: new OTLPMetricExporter({ url: `${endpoint}/v1/metrics` }),
    exportIntervalMillis: 30_000,
  }),
  logRecordProcessors: [
    new BatchLogRecordProcessor(new OTLPLogExporter({ url: `${endpoint}/v1/logs` })),
  ],
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
process.on('SIGTERM', () => sdk.shutdown());
```

---

## OpenTelemetry Collector

The Collector is the single ingestion hop you want in front of any backend. Two important rules:

1. **`memory_limiter` MUST be the first processor**, before any enrichment.
2. **`batch` MUST come after `tail_sampling`** — putting `batch` first can split a single trace across multiple batches and make tail sampling decide on partial data. Recommended ordering: `memory_limiter → enrichment → filter/transform → tail_sampling → batch`. [Source: [tail_sampling processor docs](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/tailsamplingprocessor/README.md)]

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc: { endpoint: 0.0.0.0:4317 }
      http: { endpoint: 0.0.0.0:4318 }

processors:
  memory_limiter:
    check_interval: 1s
    limit_percentage: 80
    spike_limit_percentage: 25
  resourcedetection:
    detectors: [env, system, gcp, ec2, eks, aks]
  tail_sampling:
    decision_wait: 10s
    num_traces: 100000
    policies:
      - { name: errors, type: status_code, status_code: { status_codes: [ERROR] } }
      - { name: slow,   type: latency,     latency:     { threshold_ms: 1000 } }
      - { name: rate,   type: probabilistic, probabilistic: { sampling_percentage: 5 } }
  batch:
    timeout: 5s
    send_batch_size: 8192

exporters:
  otlphttp/backend:
    endpoint: ${env:BACKEND_OTLP_ENDPOINT}
    auth: { authenticator: bearertokenauth }

service:
  pipelines:
    traces:  { receivers: [otlp], processors: [memory_limiter, resourcedetection, tail_sampling, batch], exporters: [otlphttp/backend] }
    metrics: { receivers: [otlp], processors: [memory_limiter, resourcedetection, batch],                exporters: [otlphttp/backend] }
    logs:    { receivers: [otlp], processors: [memory_limiter, resourcedetection, batch],                exporters: [otlphttp/backend] }
```

---

## eBPF-based Observability (Zero-Instrumentation)

For Kubernetes workloads, eBPF gives you HTTP/gRPC/DB traces, service maps, and L3-L7 network flow data **without modifying application code or sidecars**. According to the 2026 CNCF Observability TAG survey, 67% of teams operating Kubernetes at scale run at least one eBPF observability tool in production. Hyperscalers (Google, Meta, Netflix, AWS) deploy eBPF at production scale. [Source: [Building a Production eBPF Observability Stack 2026](https://dev.to/x4nent/building-a-production-ebpf-observability-security-stack-for-kubernetes-in-2026-5051)]

| Tool | Layer | Use when |
|------|-------|----------|
| **Cilium + Hubble** | CNI + L3-L7 network visibility | You already use Cilium as CNI; pairs with Tetragon |
| **Cilium Tetragon** | Runtime security observability + enforcement | You want syscall-level audit + policy enforcement |
| **Pixie** | Auto-instrumented APM, full-request capture (8 GB rolling buffer per node) | You want zero-config APM without sampling for debugging |
| **Coroot** | Service maps + SLO health insights from eBPF traffic | You want SRE-style health views without instrumenting code |
| **Grafana Beyla 2.5 / OTel eBPF Instrumentation** | App-level RED metrics from eBPF | Beyla donated to OTel as *OpenTelemetry eBPF Instrumentation* (May 2025); Beyla 2.5 is the first release vendoring upstream OTel eBPF code directly. Works with any OTel/Prometheus backend. [Source: [Beyla OTel donation](https://grafana.com/blog/2025/05/07/opentelemetry-ebpf-instrumentation-beyla-donation/)] |
| **Parca** | Continuous profiling (CPU/memory) | Profiling signal before OTel Profiling SDK reaches GA |

eBPF is complementary to OTel, not a replacement: use eBPF for *zero-instrumentation* coverage of unowned binaries (databases, third-party sidecars), and OTel SDKs for in-process business spans.

---

## EU CRA Reporting (2026-09-11)

For any product placed on the EU market, the CRA reporting obligation takes effect **2026-09-11**: a 24-hour Early Warning + 72-hour Full Notification through the **ENISA Single Reporting Platform** for actively exploited vulnerabilities and severe incidents. The observability stack must therefore (a) detect anomalies fast enough to trigger the 24h timer, and (b) preserve enough forensic context (traces + logs + SBOM diff) to produce the 72h report. CE marking with SBOM as a *legal requirement* applies from **2027-12-11** — but SBOM tooling must already be operational by 2026-09 to support the reporting workflow.
