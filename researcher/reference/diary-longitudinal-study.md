# Diary Study & Longitudinal Research Reference

Purpose: Design diary / longitudinal behavioral studies that capture in-context behavior unfolding over days or weeks. Covers study-length trade-offs, prompt frequency, self-report bias mitigation, Experience Sampling Method (ESM), participant fatigue management, and multi-modal capture (photo, video, voice).

## Scope Boundary

- **Researcher `diary`**: Longitudinal self-report study design — diary protocols, ESM schedule, prompt authoring, fatigue thresholds, media-capture instructions, analysis of time-series qualitative data.
- **vs Echo**: Echo simulates personas walking through a UI in a single session; it does not observe real behavior over time. In-situ longitudinal observation → `diary`; synthetic single-session walkthrough → Echo.
- **vs Pulse**: Pulse captures passive behavioral telemetry via in-product events. Passive telemetry at scale → Pulse; prompted self-report with reflection → `diary`. Best paired: telemetry gives "what", diary gives "why".
- **vs Voice**: Voice collects feedback after the fact (reviews, support tickets, post-hoc NPS). Retrospective feedback → Voice; real-time or near-real-time in-context capture → `diary`.

## Study-Length Trade-Offs

| Length | Captures | Fatigue risk | Use when |
|--------|----------|--------------|----------|
| 3–5 days | Acute decisions, weekly rhythms | Low | Purchase journeys, onboarding, habit trials |
| 1–2 weeks | Weekly cycles, novelty decay | Medium | Feature adoption, learning curves |
| 3–4 weeks | Habit formation, month-end patterns | High | Retention, behavior change studies |
| 6–12 weeks | Habit stabilization, life-event triggers | Very high | Long-term behavior shifts, chronic contexts |

Default: **2 weeks** — long enough to see novelty effects fade, short enough to retain 80%+ participants with adequate incentive.

## Prompt Frequency & ESM Schedule

Experience Sampling Method (ESM) prompts participants at semi-random intervals to capture in-the-moment state without recall bias.

| Cadence | Prompts/day | Fatigue | Use when |
|---------|-------------|---------|----------|
| Event-contingent | Variable (triggered by event) | Low | Behavior is discrete and self-reportable |
| Signal-contingent (ESM) | 3–6 randomized | Medium | Mood, context, in-situ usage patterns |
| Interval-contingent | 1–2 fixed | Low | End-of-day reflection, summary diary |
| Combined (ESM + EoD) | 3–5 ESM + 1 summary | Medium | Rich multi-granularity picture |

Cap ESM at **6 prompts/day**. Response window per prompt: **15–30 minutes**. Quiet hours (no prompts): typically 22:00–08:00 local.

## Self-Report Bias Mitigation

| Bias | Mechanism | Mitigation |
|------|-----------|-----------|
| Recall | Gaps between event and report distort detail | ESM within 30 min of event; end-of-day diary same day |
| Social desirability | Participant reports the "right" answer | Emphasize anonymized reporting, no right/wrong framing |
| Hawthorne | Being observed changes behavior | Baseline first 1–2 days as "settling"; analyze from day 3 |
| Demand characteristics | Participant guesses study hypothesis | Cover story; multiple plausible purposes in brief |
| Selection | Who agrees to diary ≠ population | Screen for diverse contexts; over-recruit marginal segments |
| Attrition | Dropouts differ from completers | Report dropout rate; analyze sensitivity by days-completed |

## Participant Fatigue Management

Fatigue manifests as declining response length, straight-line answers, missed prompts, and dropout.

- **Front-load key prompts**: days 1–3 typically have highest engagement.
- **Rotate prompt types**: alternate short (2 items) and medium (5 items) days.
- **Incentive structure**: completion bonus (e.g. +50% for ≥80% of prompts answered) outperforms flat payment.
- **Check-in touchpoint**: researcher message at day 3 and day 7 reduces dropout by 15–25%.
- **Completion threshold**: accept data from participants who answered ≥70% of prompts; flag below for sensitivity analysis.
- **Target 10–15 participants** per segment to survive 20–30% attrition and still analyze ≥8 complete logs.

## Media Capture

| Modality | Strength | Limit | Prompt design |
|----------|----------|-------|---------------|
| Text | Fastest, lowest friction | Shallow on emotion | 1–3 items, ≤60 words expected |
| Photo | Context, environment, object-of-use | PII risk | "Show the thing you just used / the space you're in" |
| Short video (15–30s) | Behavior + verbal reflection | Upload friction on mobile data | "Record what happened, why it mattered" |
| Voice note (30–60s) | Emotion, tone, richer than text | Transcription cost | "Talk for 30 seconds about how that went" |
| Screenshot | In-app moment | Needs OS permission guidance | "Capture the screen where you got stuck" |

Always include a **"no-response" option with reason code** (busy / forgot / not applicable). Silence is data.

## Tool Selection

| Tool | Strength | Use when |
|------|----------|----------|
| Indeemo | Mobile-first, media-rich, ESM | Consumer mobile behavior |
| dscout | Strong panel + diary workflow | Need recruitment bundled |
| Ethnio + custom form | Flexible, low cost | Internal panel, simple text/photo |
| Gmail/SMS + Airtable | DIY, zero tool cost | Tiny study (n<10), text-only |
| Day One / private Notion | Participant-preferred journaling | Sensitive / personal topics |

## Anti-Patterns

- Running a 4-week diary when 1 week would answer the question — attrition wastes data.
- ESM with >6 prompts/day — dropout after day 3 exceeds 40%.
- Asking participants to re-explain context every prompt — use short-form checkboxes for recurring context.
- Treating diary entries as interview substitutes — diaries give breadth over time; interviews give depth at a moment. Use both.
- Skipping the baseline settling period — Hawthorne effect inflates early-day data.
- No dropout reporting — readers cannot assess bias.
- Requiring desktop uploads for mobile behavior — forces context-switch that kills in-the-moment capture.
- Analyzing as aggregated means — lose the within-person trajectory that is the point of longitudinal data.

## Analysis Approach

Diary data is **multi-level** (observations nested within participants nested within time).

- **Within-person**: chart each participant's trajectory; identify turning points and triggers.
- **Cross-person**: cluster trajectories (e.g. steady adopters vs. frustrated dropouts).
- **Temporal patterns**: day-of-week effects, novelty decay curves, habit-formation thresholds (typically 21–66 days for new habits).
- **Triangulate** with telemetry from Pulse where available — diary "why" plus telemetry "what" is the strongest combination.

## Handoff

- **To Pulse**: telemetry instrumentation needs derived from observed moments (e.g. "add event for the stuck-step participants described on day 4").
- **To Cast**: behavior-trajectory clusters for persona refinement.
- **To Echo**: specific stuck moments to run cognitive walkthroughs on.
- **To Voice**: recurring pain themes that should enter the operational feedback loop.
- **Always include** in handoff: participant count, completion rate, dropout pattern, media-capture gaps, within-person variance notes, confidence limitations.
