# Session Analysis Methods

Methods and best practices for session replay analysis.

## 2026 Tooling Landscape

| Tool | 2026 strength | Notes |
|------|----------------|-------|
| **FullStory** | Pixel-perfect replay + **StoryAI** (agentic AI agents proactively surface friction/conversion signals, April 2025) + auto rage-click / dead-click detection + **FullStory Anywhere** (stream behavioral data to your own data warehouse) | Default for enterprise teams that need behavioral analytics at scale. Source: globenewswire.com 2025-04-02 |
| **LogRocket** | Replay tightly coupled with console / network / error monitoring + **Ask Galileo** (natural-language chat over sessions + Zendesk + Zoom + Jira, MCP integration for Claude/ChatGPT/Cursor, March 2026) | Default for engineering teams who want a single tool from "user friction" to "stack trace". Permanent free tier launched Aug 2025 (1,000 sessions/mo). Source: globenewswire.com 2026-03-05 |
| **Hotjar** | Lightweight recording + surveys + feedback widgets, no dev setup | Default for marketing / small teams |
| **Mouseflow + Mina AI** | Natural-language query over session data ("show me sessions where users abandoned checkout after seeing the discount banner") | Use when the analyst is non-technical and needs free-text discovery |
| **PostHog** (self-hosted or cloud) | Open-source replay + product analytics + feature flags + **PostHog AI** (per-session summaries, A/B variant comparison, Session Group API `/session_group_summaries`) | Use when data residency or self-host is a hard requirement, or for integrated A/B behavior analysis. Source: posthog.com/docs/posthog-ai/session-summaries |
| **Amplitude / Pendo / UXCam** | Replay layered on product-analytics primary; UXCam covers iOS/Android/React Native/Flutter/Xamarin | Use when product analytics is already the system of record or for mobile-first products |
| **Sentry** | Session Replay for mobile (iOS/Android/React Native/Flutter) in open beta 2025; paired with error monitoring | Use for mobile-first teams that already use Sentry for error tracking. Source: github.com/getsentry/sentry discussions #74322 |
| **New Relic** | Mobile session replay via native SDKs (iOS v7.5.10 Sep 2025, React Native v1.5.10 Sep 2025) | Use in observability-heavy stacks already on New Relic. Source: docs.newrelic.com |
| **Microsoft Clarity** | Free, unlimited sessions + Copilot per-session AI summaries + React Native/Flutter support (v3.19.0+) | Use for budget-constrained teams or to baseline before investing in premium tools |
| **OpenReplay** (OSS self-hosted) | rrweb-based open-source; private-by-default (all text nodes/images redacted pre-transmission); $5-6/mo storage at 100K sessions | Use when full data sovereignty is required and vendor lock-in is not acceptable. Source: openreplay.com |

### 2026 Capability Baselines

- **AI session summaries** are now table stakes. FullStory StoryAI, LogRocket Ask Galileo, PostHog AI, Microsoft Clarity Copilot, and Mouseflow Mina AI all generate natural-language summaries per session — use them as a first-pass filter, never as the ground truth for a finding.
- **Agentic AI** is the next step beyond summaries: FullStory StoryAI and LogRocket Galileo proactively surface friction and conversion signals without waiting to be asked. Verify all proactive signals against raw replays before actioning.
- **MCP integration** (LogRocket Ask Galileo, March 2026) enables querying session insights from external AI assistants (Claude, ChatGPT, Gemini, Cursor) and automating post-release monitoring via Slack/Teams. Source: blog.logrocket.com/introducing-ask-galileo
- **Mobile session replay** has reached mainstream: Sentry (open beta), New Relic, Microsoft Clarity, UXCam, Smartlook, LogRocket, and OpenReplay all support React Native and Flutter as of 2025-2026. Use wireframe-rendering tools (Smartlook) to minimize CPU/battery impact.
- **Auto-masking** is on by default for passwords, payment fields, and most form inputs across the leading tools. Verify the *server-side* masking config before shipping — client-side masking that fires after the keystroke leaves the DOM is not GDPR-safe.
- **Natural-language query over sessions** changes the analyst workflow: filter-then-scrub becomes ask-then-verify. Pair with explicit hypothesis statements to avoid chasing AI-suggested patterns that are statistical noise.
- **EU Digital Omnibus (Nov 2025)**: proposed GDPR Article 88a would require explicit consent for terminal-equipment data access (covering session replay). Enforcement expected 2026+. Design consent flows to the stricter standard now. Source: kennedyslaw.com 2026.

---

## Analysis Types

### 1. Flow Analysis

Analyze a specific user flow (e.g., checkout).

```yaml
FLOW_ANALYSIS:
  scope: "Specific user journey"
  questions:
    - Where do users drop off?
    - What paths do users actually take?
    - How does expected flow differ from actual?

  metrics:
    - completion_rate: "% who finish the flow"
    - drop_off_points: "Where users leave"
    - path_diversity: "How many unique paths exist"
    - time_to_complete: "Duration statistics"
```

### 2. Segment Comparison

Compare behavior across different user segments.

```yaml
SEGMENT_COMPARISON:
  scope: "Compare behavior across groups"
  dimensions:
    - device: [mobile, desktop, tablet]
    - user_type: [new, returning, power_user]
    - persona: [Researcher-defined personas]
    - source: [organic, paid, direct, referral]

  metrics:
    - behavior_patterns: "How groups differ"
    - success_rates: "Completion by segment"
    - friction_points: "Segment-specific problems"
```

### 3. Problem Investigation

Deep-dive analysis into known problem areas.

```yaml
PROBLEM_INVESTIGATION:
  scope: "Deep-dive into known issues"
  triggers:
    - metric_drop: "Conversion decreased"
    - user_complaint: "Feedback about specific area"
    - echo_prediction: "Simulated friction point"

  approach:
    1. Isolate affected sessions
    2. Identify common patterns
    3. Find root cause
    4. Quantify impact
```

### 4. Anomaly Detection

Detect unusual behavior patterns.

```yaml
ANOMALY_DETECTION:
  scope: "Identify unusual behavior"
  types:
    - positive: "Unexpectedly successful sessions"
    - negative: "Unusually high frustration"
    - neutral: "New behavior patterns emerging"

  methods:
    - statistical: "Deviation from baseline"
    - pattern: "Unusual sequence detection"
    - temporal: "Time-based anomalies"
```

---

## Analysis Workflow

```
1. SCOPE DEFINITION
   ├── What flow/area?
   ├── What time period?
   ├── Which user segments?
   └── What questions to answer?

2. DATA COLLECTION
   ├── Pull relevant sessions
   ├── Apply filters
   ├── Check data quality
   └── Note limitations

3. PATTERN EXTRACTION
   ├── Identify common paths
   ├── Calculate frustration signals
   ├── Find drop-off points
   └── Detect anomalies

4. EVIDENCE GATHERING
   ├── Find representative sessions
   ├── Document specific examples
   ├── Quantify findings
   └── Cross-validate

5. SYNTHESIS
   ├── Formulate hypotheses
   ├── Prioritize issues
   ├── Recommend actions
   └── Prepare handoffs
```

---

## Data Sources

### Session Replay Platforms

| Platform | Strengths | Considerations |
|----------|-----------|----------------|
| **Hotjar** | Heatmaps, recordings, surveys | Free tier limited |
| **FullStory** | Advanced search, DX integration | Enterprise pricing |
| **LogRocket** | Redux integration, error tracking | Developer-focused |
| **Smartlook** | Mobile app support | Good for apps |
| **Mouseflow** | Form analytics | Form-focused |

### Data Points to Collect

```yaml
SESSION_DATA:
  identification:
    - session_id: "Anonymized unique ID"
    - user_segment: "Persona/cohort assignment"
    - device_info: "Type, OS, browser"

  behavior:
    - page_views: "Sequence of pages visited"
    - clicks: "Element, timestamp, position"
    - scrolls: "Depth, velocity, direction"
    - forms: "Field interactions, errors"
    - timing: "Time on page, between actions"

  context:
    - entry_point: "Where they came from"
    - exit_point: "Where they left"
    - errors: "JavaScript errors, API failures"
```

---

## Statistical Considerations

### Sample Size Guidelines

| Analysis Type | Minimum Sessions | Recommended |
|---------------|------------------|-------------|
| Flow completion | 100 | 500+ |
| Segment comparison | 50 per segment | 200+ per segment |
| Anomaly detection | 1000 baseline | 5000+ |
| Problem investigation | 30 affected | 100+ |

### Confidence Levels

```yaml
CONFIDENCE_THRESHOLDS:
  high_confidence:
    sample_size: ">500 sessions"
    pattern_frequency: ">30% of sessions"
    statistical_significance: "p < 0.05"

  medium_confidence:
    sample_size: "100-500 sessions"
    pattern_frequency: "15-30% of sessions"
    note: "Directionally useful, verify with more data"

  low_confidence:
    sample_size: "<100 sessions"
    pattern_frequency: "<15% of sessions"
    note: "Hypothesis only, needs validation"
```

---

## Privacy Best Practices

### Must Do

- Anonymize all session identifiers
- Mask PII in replays (emails, names, addresses)
- Respect user consent preferences
- Apply data retention limits
- Aggregate before sharing

### Never Do

- Store raw PII in analysis outputs
- Share individual session recordings externally
- Analyze without proper consent
- Keep data longer than policy allows
- Identify specific individuals

### Anonymization Template

```yaml
SESSION_REFERENCE:
  # Instead of user ID
  reference: "Session #A7B3C (Mobile, New User, US)"

  # Instead of exact timestamps
  timing: "Morning session, 12 minutes total"

  # Instead of specific location
  context: "Entered from product page, exited at payment"
```

---

## Common Analysis Patterns

### Pattern 1: Funnel Drop-off

```yaml
FUNNEL_ANALYSIS:
  flow: [Landing → Product → Cart → Checkout → Payment → Confirmation]

  findings:
    step: "Cart → Checkout"
    drop_rate: "45%"
    frustration_signals:
      - rage_clicks_on_checkout_button: "12%"
      - back_to_cart: "28%"

  hypothesis: "Checkout button visibility issue"
  evidence: "67% of rage clicks on mobile devices"
```

### Pattern 2: Loop Detection

```yaml
LOOP_ANALYSIS:
  definition: "User returns to same page 2+ times within 60s"

  findings:
    location: "Search results page"
    loop_rate: "23% of sessions"
    common_sequence: "Results → Product → Results → Product → Exit"

  hypothesis: "Search results don't match expectations"
  evidence: "Users view average 4.2 products before leaving"
```

### Pattern 3: Dead End Detection

```yaml
DEAD_END_ANALYSIS:
  definition: "High exit rate from non-terminal page"

  findings:
    location: "FAQ page"
    exit_rate: "78%"
    preceding_action: "Help link click"

  hypothesis: "FAQ doesn't answer user questions"
  evidence: "82% scroll to bottom, 45% use search on FAQ page"
```
