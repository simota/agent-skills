# IoC / Threat-Intelligence Management Reference

Purpose: Manage indicators of compromise and threat intelligence as a first-class, lifecycle-managed asset. The `ioc` Recipe covers STIX 2.1 object shapes, TAXII 2.1 feed consumption, the observe → validate → enrich → expire lifecycle, MISP integration, feed deduplication, and false-positive handling. Detection rules (sigma / yara / snort) consume IoCs as inputs; `ioc` is the pipeline that feeds them cleanly.

For CI/CD pipeline templates (GitHub Actions, syntax lint / TP / FP test stages, OIDC and SHA-pinned actions) that ship IoC-derived detection rules to staging and production SIEMs, see `detection-as-code.md`. This file focuses on **IoC-specific rule input** — STIX/TAXII ingestion, MISP, lifecycle, TTL, dedup, and feed-quality gates that run *before* the DaC pipeline.

## Scope Boundary

- **Vigil `ioc`**: Intelligence ingestion, normalization, lifecycle, expiration, and quality. STIX/TAXII, MISP, feed hygiene.
- **Vigil `sigma` / `snort` / `yara`** (adjacent): Consumers of IoCs. They reference indicator IDs but do not own the feed.
- **Sentinel** (adjacent): Static vulnerability scanning. Consumes CVE data, not adversary indicators. Different intel class.
- **Breach** (adjacent): Red team generates TTPs and simulated IoCs to validate detection — `ioc` ingests those as test fixtures.
- **Triage** (adjacent): During live incident, Triage queries the IoC platform for context (last-seen, first-seen, related actor) but does not maintain the feed.

If the question is "is this hash/domain/IP known bad?" → `ioc` platform lookup. If "does my detection rule match it?" → the rule-authoring Recipes. If "does this CVE affect me?" → Sentinel.

## IoC Lifecycle

```
OBSERVE → VALIDATE → ENRICH → DISTRIBUTE → EXPIRE
   │          │         │          │           │
 ingest    confirm   context    push to     retire or
 raw feed  quality   add        sensors     re-evaluate
```

| Stage | Activity | Gate to next stage |
|-------|----------|--------------------|
| OBSERVE | Pull from TAXII / MISP / vendor feed / internal sighting | Deduplicate against existing indicators |
| VALIDATE | Check feed reputation, cross-source confirmation, allowlist scrub | Minimum 2 independent sources OR 1 tier-1 source |
| ENRICH | Add actor attribution, campaign ref, ATT&CK TTPs, WHOIS, passive DNS | Confidence score ≥ threshold for production push |
| DISTRIBUTE | Push to SIEM watchlists, EDR blocklists, NGFW, DNS RPZ | Per-sensor format conversion succeeded |
| EXPIRE | TTL-based or confidence-decay retirement; re-evaluate on re-sighting | Zero active references in detection rules |

**TTL guidance by IoC type**:

| Type | Default TTL | Rationale |
|------|-------------|-----------|
| IPv4 / IPv6 | 14 days | IP reuse is fast (cloud, residential proxies) |
| Domain | 30–90 days | Slower churn; DGAs need shorter TTL |
| URL | 30 days | Often tied to domain lifecycle |
| File hash (SHA256) | 365 days or indefinite | Hashes do not go stale; binary is the binary |
| Email sender | 30 days | Infrastructure rotates fast |
| TLS cert / JA3 | 180 days | Certificate lifetime bounded |

## STIX 2.1 Object Shapes

STIX 2.1 separates the observation from the interpretation. Use both.

```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--c4f8bb3e-...",
  "created": "2026-04-24T09:00:00.000Z",
  "modified": "2026-04-24T09:00:00.000Z",
  "name": "Malicious SHA256 observed in phishing campaign APT-X-2026-Q2",
  "pattern": "[file:hashes.'SHA-256' = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855']",
  "pattern_type": "stix",
  "valid_from": "2026-04-24T09:00:00.000Z",
  "valid_until": "2027-04-24T09:00:00.000Z",
  "indicator_types": ["malicious-activity"],
  "confidence": 85,
  "labels": ["malicious-activity"],
  "kill_chain_phases": [
    {"kill_chain_name": "mitre-attack", "phase_name": "initial-access"}
  ]
}
```

Relationship objects link indicators to campaigns, threat actors, tools, and attack patterns:

```json
{
  "type": "relationship",
  "spec_version": "2.1",
  "id": "relationship--...",
  "relationship_type": "indicates",
  "source_ref": "indicator--c4f8bb3e-...",
  "target_ref": "attack-pattern--T1566.001"
}
```

Always populate `valid_until` — missing expiry is the #1 cause of stale-IoC alert fatigue.

## TAXII 2.1 Feed Consumption

TAXII 2.1 is the HTTP-based transport for STIX.

```
GET /taxii2/collections/<id>/objects/?added_after=2026-04-23T00:00:00Z
Accept: application/taxii+json;version=2.1
Authorization: Bearer <token>
```

Pagination uses `X-TAXII-Date-Added-First` / `X-TAXII-Date-Added-Last` + `next` cursor — never full-refresh production feeds.

**Feed hygiene rules**:

1. **Pin feed versions / collection IDs** in config; do not auto-subscribe to new collections.
2. **Rate-limit pull cadence** (most production feeds update every 1–24h; polling faster wastes credits and hits TAXII rate limits).
3. **Sign feed trust relationships** — only auto-distribute from tier-1 feeds; tier-2/3 requires analyst approval.
4. **Track provenance** on every indicator — `x_source_feed`, `x_first_seen`, `x_confidence_source`. Needed for audit and FP triage.

## MISP Integration

MISP is the de facto community sharing platform. Integration patterns:

| Direction | Mechanism | Notes |
|-----------|-----------|-------|
| MISP → Vigil | MISP REST API `/events/restSearch` + `to_ids=true` filter | Pull only IDS-flagged attributes to reduce noise |
| MISP → Sensor | PyMISP → STIX 2.1 → SIEM watchlist sync | Map MISP tags to ATT&CK + TLP |
| Vigil → MISP | Push internal sightings via `/attributes/restSearch` + sighting POST | Share back to community under TLP:AMBER+ only with approval |
| Alert context | SOAR enrichment queries MISP event by attribute value | Cache 15 min to avoid hot-path load |

**TLP handling**:
- TLP:RED → never auto-distribute; analyst manual push only.
- TLP:AMBER / AMBER+STRICT → distribute within org, no external share.
- TLP:GREEN → internal + trusted partners.
- TLP:CLEAR → public.

Violating TLP constraints (especially RED/AMBER) is a breach of the sharing trust model and can get your org kicked from ISACs.

## Deduplication and False-Positive Handling

**Dedup key design** — composite across (type, value, feed). Same hash from 3 feeds = 1 logical indicator with provenance list, not 3 separate detections firing.

```python
dedup_key = hashlib.sha256(
    f"{indicator_type}|{normalized_value}".encode()
).hexdigest()
```

Normalize before hashing: lowercase domains, strip `http(s)://` from URLs for certain matches, canonical-form IPv6.

**Allowlist / FP scrub** — every indicator ingested runs against:

1. **Organization allowlist** (owned domains, outbound SaaS FQDNs, corporate IP ranges).
2. **Alexa / Tranco Top 1M** for domains (high-reputation domain as "malicious" is almost always a feed bug).
3. **Public DNS resolver IPs, CDN ranges, CGNAT** — common FP sources.
4. **Previous FP history** — if this value was dispositioned FP in the last 90 days, require re-validation.

Hits against allowlist *do not* silently drop — flag them for feed-quality reporting.

## Anti-Patterns

- Ingesting feeds without `valid_until` — stale IoCs fire forever and drown the SOC.
- No allowlist scrub — Google, Cloudflare, or your own CDN domain gets flagged as malicious and blocks business.
- Treating all feeds as equal confidence — tier-1 commercial + tier-3 OSINT dumped into the same watchlist.
- Pushing raw hash lists to EDR without context — analyst sees hit, has no story, cannot triage.
- Auto-blocking on single-source indicators (feed bug cascades into production outage).
- Missing provenance — cannot answer "why did we flag this?" during FP dispositioning.
- Re-ingesting the same expired indicator endlessly (no decay memory → churn).
- Sharing TLP:AMBER indicators outward without source permission (breaks ISAC trust).

## Handoff / Next Steps

- **To `sigma` / `snort` / `yara`**: indicator IDs + STIX patterns suitable for detection rule reference; rule references indicator-id, not raw value (so expiry cascades cleanly).
- **To `coverage`**: IoC → ATT&CK kill-chain-phase mapping feeds the gap matrix.
- **To `playbook`**: enrichment lookups during IR — actor, campaign, last-seen, related indicators.
- **To Triage**: live incident context — "is this hash/domain/IP known bad, and since when?"
- **To Breach (Purple Team)**: validated IoCs become test fixtures for detection regression testing.
- **To Scribe**: intel report publication — executive summary of campaigns, actors, observed TTPs per quarter.
