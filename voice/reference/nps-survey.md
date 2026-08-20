# NPS Survey Delta

Purpose: Voice NPS instrument, consent, and interpretation contract. Static industry benchmark tables are intentionally excluded because they drift.

## Instrument

Ask the standard `0-10` likelihood-to-recommend question with product/audience wording appropriate to the program. Classify `0-6` detractor, `7-8` passive, `9-10` promoter.

```text
NPS = percent_promoters - percent_detractors
```

Ask after a meaningful experience. Keep the score response separate from optional verbatim feedback and from consent to contact the respondent.

## Minimal Record

Store score, derived category, pseudonymous respondent/account key, survey/touchpoint, segment/plan/tenure, timestamp, optional feedback, instrument version, and consent flags. Apply the product's privacy and retention policy.

## Analysis Contract

- Always report response count/rate and uncertainty with the score.
- Segment only when sample size and sampling design support it.
- Compare like touchpoints, populations, and time windows.
- Treat open text as qualitative evidence, not a numeric explanation of NPS.
- Fetch current external benchmarks from dated primary or clearly identified benchmark sources; never reuse an undated “good/excellent/world-class” scale.

Route themes to Spark/Growth, coding to `thematic-coding.md`, and instrumentation gaps to Pulse.
