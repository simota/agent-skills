# Replay from Production Logs with Safety Scrub

**Purpose:** Turn captured production traffic (HAR files / request logs / Kafka tap / OTel spans) into a replayable test-data set that can drive staging or regression runs, with a mandatory PII scrub pass, timestamp shifting, user-id remapping, and a finite retention lifecycle. Mint owns the safe, replayable dataset; the consumer (Voyager / Siege / Builder) owns replay execution.

## Scope Boundary

- **Mint `replay`**: captured-traffic-to-fixture pipeline — capture adapters, PII scrub, time shift, id remap, storage & retention policy.
- **Cloak (elsewhere)**: live-system PII governance, DPIA, lawful-basis for capture.
- **Oath (elsewhere)**: regulatory approval for production-capture programs (GDPR Art. 32, HIPAA safe-harbor).
- **Siege (elsewhere)**: replay-as-load-test (amplify / shuffle / time-warp for stress); `replay` produces the cleaned source set, Siege abuses it.
- **Voyager (elsewhere)**: E2E replay execution against staging.

If the question is "can I share this traffic capture with CI?" → `replay`. If it is "are we allowed to capture it in the first place?" → Cloak + Oath.

## Capture Sources

| Source | Strength | Watch-out |
|--------|----------|-----------|
| HAR (browser Network export) | full request + response, headers, timing | PII in query string, cookies, JWT payloads |
| Reverse-proxy / gateway access log | high volume, structured | body usually not captured — replay may be incomplete |
| Kafka tap / topic mirror | async event reconstruction | tenant partition keys, schema evolution drift |
| OpenTelemetry span export | cross-service correlation | span attributes often contain PII leaked via `http.url` |
| Application-level debug log | business-semantic signals | least structured, PII density highest |
| Session replay tool export (Trace / FullStory / Hotjar) | user-level behavioral | governed by vendor ToS — usually forbids export |

Default capture window: ≤ 24h, rolling. Long windows inflate PII exposure without adding replay value.

## Pipeline

```
CAPTURE      →  tap produces raw stream (HAR / access log / Kafka)
             →  write-once to scrub-staging volume (encrypted, 72h TTL)

SCRUB        →  PII detector pass (email / phone / SSN / JWT / PAN regex + NER)
             →  header strip: Authorization, Cookie, Set-Cookie, X-*-Token
             →  body mask: apply Mint `pii` rules per field
             →  URL scrub: remove query params matching PII allow-list

REMAP        →  user-id / session-id / tenant-id → deterministic token
             →  preserve within-capture joins (same real id → same token)

TIMESHIFT    →  anchor timestamp = capture_start
             →  shift all timestamps by (replay_anchor - capture_start)
             →  preserve relative delta (critical for retry / rate-limit replays)

VALIDATE     →  PII re-scan on scrubbed output — zero hits required
             →  schema validate (OpenAPI / protobuf) each record
             →  sample 1% for human spot-check before release

STORE        →  retention-tagged volume, auto-expire on policy
             →  manifest header: capture_window, scrub_rules_version, expires_at
```

Every stage is logged, every stage is reversible only with the **scrub key** which lives outside the dataset.

## PII Scrub Pass

A single regex sweep is insufficient. Layer detection:

| Layer | Catches |
|-------|---------|
| Regex allow / deny | email, phone, credit-card with Luhn, JWT pattern |
| Structured-field rule | map by key name (`user.email`, `ssn`, `authorization`) |
| Named-entity recognition | person / location / organization in free-text |
| Entropy filter | high-entropy tokens (likely secrets / API keys) |
| Denylist domain check | real corporate domains in email fields |

Reject the scrub run if the post-scrub scan finds ≥ 1 PII hit. Never "allow 3 false-positive-looking emails through" — emails are either fake-domain fake or the dataset fails.

## Timestamp Shifting

```python
from datetime import datetime, timedelta

def shift_timestamps(records: list[dict], original_anchor: datetime, target_anchor: datetime) -> list[dict]:
    delta = target_anchor - original_anchor
    for r in records:
        for key in ("ts", "created_at", "updated_at", "event_time"):
            if key in r:
                r[key] = (datetime.fromisoformat(r[key]) + delta).isoformat()
    return records
```

Shift **every** timestamp field by the **same delta**. Different deltas per field break causality (e.g. `updated_at < created_at`). Preserve DST boundaries only if the replay depends on them — otherwise anchor to UTC.

## User-ID Remapping

```python
import hmac, hashlib

def remap(real_id: str, secret: bytes) -> str:
    return "u_" + hmac.new(secret, real_id.encode(), hashlib.sha256).hexdigest()[:12]
```

Same `secret` across a capture window → joins preserved. New `secret` per capture window → cross-window correlation broken (desired default). Store `secret` outside the capture bundle.

## Replay-Against-Staging Workflow

```
1. Consumer (Voyager / Siege / Builder) requests capture bundle by manifest id
2. Mint verifies: not expired, scrub validated, consumer authorized
3. Consumer mounts bundle into staging environment
4. Replay tool (goreplay / vegeta / kafka-replay / k6) drives staging
5. Staging must be isolated: no outbound webhooks to third parties, no prod DB
6. Consumer returns replay report (coverage, failures, latency) — not raw data
```

If the replay surfaces a bug, the repro is the manifest id + replay config, not a copy of the bundle in a ticket.

## Storage Retention for Replay Sets

| Tier | TTL | Access |
|------|-----|--------|
| Scrub staging (pre-validation) | 72h hard | scrub service only |
| Active bundle (post-validation) | 30d default, 90d max | consumer agents with ticket |
| Golden regression set (long-lived) | 1y, quarterly re-scrub | requires Oath approval + re-validation |
| Expired | deleted, tombstone kept 1y | audit access only |

Every bundle carries its own expiry. Consumers check `expires_at` before load and hard-fail past it — no exceptions.

## Anti-Patterns

- "Replay the raw prod log in staging" — leaks PII, leaks secrets via Authorization header, violates retention.
- Scrubbing only request bodies while leaving `Referer` / `User-Agent` / `?email=` query strings untouched.
- Shifting `created_at` but not `updated_at` — temporal invariants break silently.
- Remapping user-ids but not tenant-ids in a multi-tenant capture — cross-tenant leakage in the replay set.
- Holding bundles "just in case" past expiry — compounds exposure without test value.
- Replaying against a staging environment that shares a DB, a webhook endpoint, or an SMTP relay with production.
- Trusting a single regex pass as "good enough scrub" — layered detection is non-negotiable.
- Committing the scrub key or HMAC secret alongside the manifest in the same repo.
- Replaying auth tokens verbatim — JWTs often have 7-day validity and leak real subjects even if scrubbed from bodies.

## Handoff

**To Voyager:** bundle manifest id + replay config + expected assertion set. Voyager drives staging, does not touch raw capture.
**To Siege:** scrubbed bundle + amplification spec (shuffle / time-warp / rate multiplier). Siege stresses, Mint cleans.
**To Builder:** minimal repro bundle when the replay surfaces an integration bug — smallest subset that reproduces, not the full capture.
**To `pii`:** escalation when capture contains field shapes the default scrub rules did not cover; `pii` upgrades the ruleset, replay re-runs.
**To Cloak / Oath:** periodic audit evidence — scrub ruleset version, bundle inventory, expiry compliance — for DPIA and audit trail.
