# Rage-Click and Dead-Click Detection Reference

Purpose: Surface user frustration from micro-behaviors — rapid repeated clicks, clicks on non-interactive elements, error-shake mouse tremor, and u-turn navigation loops — with industry-standard thresholds, false-positive filters, and a direct path back to session replay for qualitative confirmation.

## Scope Boundary

- **trace `rageclick`**: detects frustration micro-signals (rage click, dead click, error shake, u-turn / thrash), scores them, and links each signal to anonymized session replay evidence for WHY inference.
- **pulse (elsewhere)**: quantitative KPI tracking and funnel conversion metrics — owns the numeric trend; Trace owns the behavioral cause.
- **echo (elsewhere)**: persona-based predicted friction points before real data exists. Rageclick confirms or refutes those predictions from real sessions.
- **palette (elsewhere)**: UX remediation (touch-target sizing, feedback timing, affordance redesign) once rageclick surfaces the pattern.
- **cloak (elsewhere)**: privacy controls for replay recording — redaction rules, consent gating, GPC handling.

## Workflow

```
DETECT   →  apply rage/dead/shake/thrash thresholds to event stream
         →  filter false positives (intentional double-click, slow UI, drag intent)
         →  cluster signals by element selector + viewport region

SCORE    →  weight each signal type, aggregate per session, normalize per cohort
         →  flag sessions scoring above p90 for qualitative review

REPLAY   →  fetch anonymized replay slices around each flagged signal (±10s)
         →  verify signal is genuine frustration, not instrumentation artifact

REPORT   →  top-N friction hotspots with element + frequency + replay links
         →  hand off to Palette (fix) or Experiment (A/B validate fix)
```

## Signal Definitions (Industry Baselines)

| Signal | Threshold | Notes |
|--------|-----------|-------|
| Rage click | >=3 clicks within 1s on same element, <50px apart (desktop: 30px) | Hotjar/FullStory/PostHog consensus; loosen radius on mobile for touch imprecision |
| Dead click | click with no DOM mutation, navigation, or network call within 600ms | Exclude elements with `role=button` but documented disabled state |
| Error shake | cursor direction reversals >=6 within 2s, travel <100px total | Indicates hesitation/indecision, not always frustration — score lower |
| U-turn / thrash | back navigation within 5s of forward navigation, repeated >=2 times on same page pair | Signals info-scent failure or wrong-page arrival |

Thresholds above follow the dominant session-replay vendors. Calibrate to your baseline — a site with 4.1% rage-click rate in checkout is the published retail median; deviations >1.5x warrant deeper investigation.

## False-Positive Filters

Apply these BEFORE scoring. Raw rage-click counts without filters produce 30-50% noise.

- **Intentional double-click**: common on desktop for text selection, file-manager-style UI, or map zoom — exclude elements where double-click is documented affordance.
- **Slow UI latency**: if INP (Interaction to Next Paint) >500ms at p75 for the element, repeated clicks are rational, not rage. Exclude and escalate the latency to Bolt/Beacon.
- **Drag intent**: if the second click lands >80px from the first within 300ms, classify as drag, not rage.
- **Disabled-but-not-marked**: elements that look interactive but are programmatically disabled generate dead clicks that are designer errors, not user frustration — still flag for Palette, but categorize separately.
- **Framework hydration delay**: SSR apps show dead-click bursts in the first 200-800ms after navigation. Exclude the page's hydration window from dead-click counting.

## Signal Weight Scoring

```
session_frustration_score =
    3.0 * rage_click_count
  + 2.0 * dead_click_count
  + 1.0 * error_shake_count
  + 1.5 * thrash_count

normalized = session_frustration_score / session_duration_minutes
```

Flag sessions with `normalized >= p90` of the cohort. Do not compare scores across cohorts with different session-length distributions without normalization — a 30s bounce session and a 10min task session produce wildly different raw counts.

Weights above are defaults; recalibrate per product. For high-intent flows (checkout, payment) a single rage click should weigh more than three dead clicks in a browse-only session — apply a `flow_criticality` multiplier to each signal scored inside a declared critical flow.

## Rage vs Dead Click Distinction

The two signals look similar in raw data but mean opposite things. Misclassification leads to the wrong fix.

| Dimension | Rage click | Dead click |
|-----------|-----------|------------|
| User belief | "The element should do something, but my click isn't registering" | "This *might* be clickable, let me try" |
| Element | Interactive (button / link / form control) | Non-interactive (text, image, decorative element) |
| Frequency | 3+ rapid clicks on same target | Often just 1-2 clicks before giving up |
| Fix category | Latency, feedback, state | Affordance, visual signaling, content |
| Handoff | Bolt/Beacon (if INP-correlated) or Palette | Palette (affordance) or Prose (copy clarity) |

A rage click on a working button usually means slow response; a rage click on a broken button means a wiring bug; a dead click on a heading that looks like a button means the visual language is lying to the user.

## Session-Replay Tool Feature Comparison

| Tool | Rage click | Dead click | Error shake | U-turn | AI summary |
|------|------------|------------|-------------|--------|------------|
| Hotjar | Native | Native | No | Partial | Limited |
| FullStory | Native (frustration signal) | Native | Native (thrash) | Native | Yes (Story) |
| PostHog | Native (autocapture) | Manual via filters | No | Manual | Beta |
| Microsoft Clarity | Native | Native | No | Partial | No |
| Mixpanel Session Replay | Via integration | Limited | No | Via events | No |
| Contentsquare | Native | Native | Native | Native | Yes (AI Summaries) |

Pick by: (1) does it detect the signal natively, (2) does it expose the signal via API for pipeline aggregation, (3) does it support client-side PII redaction before transmission.

## Anti-Patterns

- Reporting raw rage-click counts without false-positive filtering — inflates the problem and burns stakeholder trust.
- Treating all rage clicks equivalently — 3 rage clicks on a primary CTA is existential, 3 rage clicks on a decorative logo is noise.
- Ignoring INP when rage clicks cluster — slow UI looks identical to broken UI in click logs; check performance first.
- Using desktop pixel thresholds on mobile — touch imprecision generates systematic false positives; use 50px radius and verify 48x48 CSS-pixel touch targets.
- Aggregating across personas without segmenting — power users and new users show opposite rage-click profiles for the same UI.
- Surfacing rage-click sessions without PII redaction — session replay leaks credit card numbers in ~2% of e-commerce sessions without form masking.
- Drawing conclusions from n<30 rage-click sessions per element — small-sample rage clusters are usually one confused user, not a pattern.

## Handoff

- **To Palette**: top-3 friction hotspots with element selector, frustration score, session count, anonymized replay evidence links, and recommended fix category (affordance, feedback, timing, target size).
- **To Experiment**: if frustration score reproduces across >=2 cohorts and the fix is testable, emit `TRACE_TO_EXPERIMENT` with Hypothesis Readiness Score >=7.
- **To Bolt/Beacon**: elements where rage clicks correlate with INP >200ms — treat as predictive performance regression, not UX issue.
- **To Voice**: flagged friction hotspots to place targeted micro-surveys ("What went wrong here?") at the exact moment of frustration detection.
