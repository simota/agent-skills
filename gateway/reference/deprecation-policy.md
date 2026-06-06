# API Deprecation Policy Reference

Purpose: Design the contract for sunsetting parts of an API. Cover RFC 8594 (`Sunset` header), RFC 9745 (`Deprecation` header), deprecation timeline, client SDK migration, customer communication, and removal cutover.

> **2026-05 baseline**: **RFC 9745** "The Deprecation HTTP Response Header Field" was published **2025-03** (Standards Track, [datatracker](https://datatracker.ietf.org/doc/html/rfc9745)) — earlier docs in this skill that cited a 2024 date are wrong. The header is an **Item Structured Field** whose value is a `Date` per RFC 9651 (Structured Field Values for HTTP, 2024-09). Example: `Deprecation: @1688169599`. Use RFC 8594 `Sunset` (HTTP-date format) and RFC 8288 `Link; rel="deprecation"` / `rel="successor-version"` in tandem.

## Scope Boundary

- **gateway `deprecation`**: Deprecation policy + signals (this document).
- **gateway `versioning` (elsewhere)**: URL/header versioning strategy.
- **gateway `breaking` (elsewhere)**: Breaking-change detection.
- **Launch (elsewhere)**: Actual rollout / cutover execution.
- **Voice (elsewhere)**: Customer-facing announcements.
- **Comply (elsewhere)**: Regulated APIs may have SLA-bound deprecation rules.
- **horizon `sunset` (elsewhere)**: Internal tech-debt sunset (different concern).

## Deprecation Lifecycle

```
ACTIVE  →  DEPRECATED  →  SUNSET (removal)
                         ↓
                     (response: 410 Gone or redirect)
```

| Stage | Signal | Operation |
|-------|--------|-----------|
| Active | none | Normal usage |
| Deprecated | `Deprecation: true`, `Sunset: <date>`, `Link: <migration-url>; rel="deprecation"` | Still works; clients warned |
| Sunset | `Sunset` date passed; HTTP 410 Gone or 308 redirect | Removed |

## RFC 9745 — `Deprecation` Header

```
Deprecation: @1727136000           # Date (RFC 9651 Structured Field, Unix timestamp with @ sigil)
Deprecation: true                   # legacy boolean form (older drafts; many clients still recognize)
```

RFC 9745 was published **2025-03** (Standards Track). The value is an Item Structured Field of type Date per RFC 9651. Many clients still send the legacy boolean form — accept both on the receive side but emit the Date form for new responses.

## RFC 8594 — `Sunset` Header

```
Sunset: Wed, 11 Nov 2026 23:59:59 GMT
```

HTTP-date format. Indicates when the resource will become unavailable.

## `Link` for Migration Docs

```
Link: <https://api.example.com/docs/migrate-v1-to-v2>; rel="deprecation"
Link: <https://api.example.com/v2/orders>; rel="successor-version"
```

Multiple `Link` headers are allowed. `rel="deprecation"` is RFC-defined; `rel="successor-version"` is conventional.

## Combined Example

```
HTTP/1.1 200 OK
Deprecation: @1727136000
Sunset: Wed, 11 Nov 2026 23:59:59 GMT
Link: <https://api.example.com/docs/migrate-v1-to-v2>; rel="deprecation"
Link: <https://api.example.com/v2/orders>; rel="successor-version"
Content-Type: application/json

{ "orders": [...] }
```

The endpoint still returns 200 with the data; signals are advisory.

## Timeline Standards

| Audience | Typical deprecation window |
|----------|----------------------------|
| Public API (3rd-party consumers) | 12+ months |
| Partner API (B2B integration) | 6-12 months |
| Internal API | 90 days minimum |
| Mobile app API | Span 2 store releases (~6 months) |
| Regulated context (banking) | Per SLA (often 24+ months) |

Shorter windows risk customer surprise + churn. Longer windows accumulate tech debt.

## Communication Cadence

| Time before sunset | Action |
|--------------------|--------|
| Day 0 (announcement) | Headers ON; blog post; email; changelog; in-app banner if applicable |
| Day -90 | Reminder email; SDK release with new endpoint; tutorial |
| Day -30 | Final reminder; in-product warning; reach top consumers directly |
| Day -7 | Brownouts (briefly return 503/429 with sunset hint, opt-out) |
| Day 0 (sunset) | Remove; respond 410 Gone with migration Link |
| Day +30 | Remove 410 stub; cleanup |

Brownouts (intentional, brief outages of the deprecated endpoint near sunset) force migrations of laggards while still allowing a graceful escape.

## What Triggers Deprecation?

| Reason | Approach |
|--------|----------|
| New, better version exists | Standard versioned deprecation |
| Security flaw in old shape | Faster timeline + clear comms |
| Cost / scale issue | Coordinate with Ledger; usually slower |
| Regulatory change | Comply; per-jurisdiction timing |
| Acquired/sunset feature | Customer outreach + custom support |

## Versioning Strategy Interplay

Deprecation maps to versioning style:

| Versioning | Deprecation method |
|-----------|---------------------|
| URL path (`/v1/...`) | Deprecate the prefix; routes are sunset together |
| Accept header (`application/vnd.api+json;version=1`) | Per-media-type sunset |
| Custom header (`X-API-Version: 1`) | Per-version-header sunset |
| Per-endpoint | Granular; per-route headers |
| Single rolling | Avoid; deprecation is about retiring something |

Hand off the version-strategy choice to the `versioning` recipe; this doc handles signaling once chosen.

## Workflow

```
INVENTORY    →  endpoints / fields / params being deprecated
             →  reason classification

TIMELINE     →  per-audience window (public / partner / internal)
             →  events: announce, T-90, T-30, T-7 brownout, T-0 sunset

SUCCESSOR    →  identify replacement (path / version / new endpoint)
             →  migration guide URL
             →  SDK update plan

SIGNALING    →  Deprecation header (NumericDate)
             →  Sunset header (HTTP-date)
             →  Link rel="deprecation" + rel="successor-version"

COMMS        →  blog / email / changelog / in-product
             →  cadence per timeline
             →  hand off to Voice for customer-facing copy

BROWNOUT     →  schedule (T-7 or per-endpoint)
             →  fail-mode (503 with hint vs 200 with louder warning)
             →  opt-out for critical clients

CUTOVER      →  remove endpoint; respond 410 Gone with successor Link
             →  monitor 410 hits; escalate to top callers
             →  hand off to Launch for actual deploy

POST         →  remove 410 stub after grace period
             →  archive deprecation announcement
             →  update version-coverage docs

HANDOFF      →  versioning: strategy alignment
             →  Launch: cutover scheduling
             →  Voice: customer-facing copy
             →  Comply: regulated context check
             →  Beacon: 410 / 503 traffic monitoring
             →  Builder: SDK updates
```

## Output Template

```markdown
## Deprecation Plan: [API / Endpoint]

### Inventory
| Resource | Successor | Reason | Audience |
|----------|-----------|--------|----------|
| GET /v1/orders | GET /v2/orders | Schema improvements | Public |
| POST /v1/payment.refund | POST /v2/refunds | Verb-leaving for resource | Partner |
| ... | ... | ... | ... |

### Timeline
- **Announce date**: [YYYY-MM-DD]
- **Sunset date**: [YYYY-MM-DD] (window: [N months])
- **T-90 reminder**: [date]
- **T-30 reminder**: [date]
- **T-7 brownout**: [schedule]
- **T-0 cutover**: [date + time]
- **+30 cleanup**: [date]

### Signaling
On deprecated responses:
```
Deprecation: @[unix-ts]
Sunset: [HTTP-date]
Link: <[migration-url]>; rel="deprecation"
Link: <[successor-url]>; rel="successor-version"
```

After sunset:
```
HTTP/1.1 410 Gone
Link: <[successor-url]>; rel="successor-version"
Content-Type: application/problem+json

{ "type": "...", "title": "Endpoint sunset", "status": 410, ... }
```

### Communications
| Date | Channel | Audience | Owner |
|------|---------|----------|-------|
| Announce | Blog + email + changelog | All | DevRel + Voice |
| T-90 | Email + SDK release notes | Active callers | Voice |
| T-30 | Email + in-product banner | Top 100 callers | DevRel + CS |
| T-7 | Direct outreach to laggards | Top 10 callers | CS |

### Brownout Plan
- **Window**: [T-7 to T-1, daily 1-hour outage at 14:00 UTC]
- **Failure mode**: [503 + Sunset hint + Retry-After header]
- **Opt-out**: [VIP customers can request exemption via support]

### SDK Migration
- v1.x EOL: [date]
- v2.0 release: [date]
- Compatibility shim: [yes/no, duration]

### Monitoring
- Pre-sunset: 410-rate trend; alert if traffic stays > 1% at T-7
- Post-sunset: 410 traffic; identify stragglers; outreach

### Handoffs
- versioning: ensures URL strategy aligned
- Launch: cutover scheduling + flag
- Voice: customer-facing copy + email templates
- Comply: regulated context check
- Beacon: 410 / 503 dashboards
- Builder: SDK + compatibility shim
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Removing endpoint without deprecation | Always announce + signal first |
| `Deprecation` header without `Sunset` | Pair them — clients need a date |
| Sunset window < 90 days for public API | 12+ months for public; less risks churn |
| No migration guide URL | Mandatory `Link: rel="deprecation"` |
| No brownout test | Stragglers don't migrate without pressure |
| Killing endpoints with 404 | Use 410 Gone; semantic "permanently removed" |
| No Retry-After on brownout 503 | Clients hammer; honor client retry semantics |
| Deprecation announced only in changelog | Email + blog + in-product + headers |
| Cutting off paying customers without outreach | T-30 direct contact for top 100 |
| Headers only on success responses | Include on 4xx too where applicable |
| No SDK compatibility shim | Forces synchronous migration; breaks staggered upgrades |
| Sunset date drift / silent extension | Erodes trust; commit publicly |

## Deliverable Contract

When `deprecation` completes, emit:

- **Inventory** with successor + reason + audience.
- **Timeline** with all milestone dates.
- **Signaling spec** (Deprecation, Sunset, Link headers).
- **Post-sunset response** (410 Gone with Link).
- **Communications plan** with channel + cadence.
- **Brownout plan**.
- **SDK migration plan**.
- **Monitoring plan**.
- **Handoffs**: versioning, Launch, Voice, Comply, Beacon, Builder.

## References

- **RFC 9745 — The Deprecation HTTP Response Header Field (2025-03, Standards Track)** — [datatracker](https://datatracker.ietf.org/doc/html/rfc9745)
- RFC 8594 — The Sunset HTTP Header Field (2019)
- RFC 8288 — Web Linking (Link header + rels)
- RFC 9651 — Structured Field Values for HTTP (2024-09; defines Date type used by Deprecation)
- RFC 9457 — Problem Details for HTTP APIs (2023-07, obsoletes RFC 7807)
- IETF httpbis-deprecation-header — historical drafts
- Google Cloud — API deprecation policy
- AWS — API deprecation patterns and brownouts
- Stripe API versioning + deprecation case study
- Microsoft REST API guidelines — deprecation chapter
- SemVer spec — for SDK version coordination
- "API Versioning and Deprecation" — Phil Sturgeon, *APIs You Won't Hate*
- Heroku — public deprecation post-mortems (good cautionary reading)
