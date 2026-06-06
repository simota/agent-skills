# Narration Localization Reference

Purpose: Adapt a source-language narration / voice-over script to multiple locales with cultural fit, duration budgeting, and voice-talent-ready briefs. Localization is not translation — it is rewriting the narration for the new locale while preserving intent, timing, and lip-sync feasibility.

> **2026 toolchain.** AI dubbing has reached "good enough for the first pass on internal / mid-tier external work" by 2026: **HeyGen** offers lip-sync dubbing in `40+` languages with face-aware mouth re-rendering; **ElevenLabs** ships `~5,000` voices across `32+` languages and one-click captions; **Kling 3.0 Omni** supports multi-shot sequences with a shared audio timeline and native dialogue in five languages. AI dubbing remains a *first pass*, never the shipping deliverable for brand-critical surfaces — native-speaker LQA stays mandatory. For shorts auto-publishing flows (FlowShorts and similar) the entire pipeline is AI-stitched (script + ElevenLabs VO + captions + auto-posting) — those are appropriate for high-volume social, not for the localized brand campaign work this file covers.

## Scope Boundary

- **cue `localize`**: locale-adapted VO / narration script, expansion budgeting, talent brief, pronunciation guide.
- **cue `narration` (elsewhere)**: source-language narration drafting — always run before `localize`.
- **cue `captions` (elsewhere)**: time-coded subtitle files — base captions should be locked before localizing.
- **Polyglot (elsewhere)**: UI string / i18n key translation for in-product copy. Not for narration audio.
- **Tone (elsewhere)**: per-locale TTS voice selection, dubbing mix, LUFS normalization across languages.
- **Warden (elsewhere)**: LQA gate — pass/fail evaluation of delivered locales.

If the hypothesis is "does this sound natural to a Japanese / German / Spanish viewer?" → `localize`. If it's "are the UI strings translated?" → Polyglot.

## Workflow

```
BASELINE   →  confirm source script is LOCKED (no more edits after localization starts)
           →  classify: lip-sync dub / off-camera VO / voice-over-with-subtitles
           →  list target locales with priority (primary vs secondary markets)

BUDGET     →  apply expansion factor per locale to source word count
           →  if timed-to-video: compute per-scene duration budget per locale
           →  flag scenes where target locale will overrun by >15%

ADAPT      →  rewrite (don't literally translate) per locale
           →  replace idioms, currency, units, cultural references, examples
           →  preserve brand voice, product names, numerical claims
           →  build pronunciation guide for any non-native brand terms

BRIEF      →  assemble voice-talent brief per locale (tone, pace, demographic, reference clips)
           →  produce per-scene timing table (source seconds / target seconds / delta)
           →  note lip-sync priority cues for dubbed scenes

LQA        →  native-speaker review pass against checklist
           →  deliver final per-locale script + brief + pronunciation guide
```

## Expansion Factor Table

Approximate character-count or duration expansion from English source. Use as a budgeting signal, not a guarantee.

| Target locale | Expansion vs EN | Notes |
|---------------|-----------------|-------|
| German (DE) | +30% | Compound nouns; longest of the major Western locales |
| French (FR) | +20% | Verbose formal register, shorter informal |
| Spanish (ES) | +25% | Gendered agreement adds syllables |
| Italian (IT) | +20% | Vowel-heavy, reads fast despite length |
| Portuguese (pt-BR) | +25% | Longer than pt-PT |
| Russian (RU) | +15% | Shrinks vs Latin-alphabet expansion, but cyrillic width compensates |
| Dutch (NL) | +25% | Similar to German but slightly less |
| Japanese (JA) | -10% (chars) / +5-10% (duration) | Fewer characters, but mora-timed delivery lengthens audio |
| Korean (KO) | -5% (chars) / +10% (duration) | Particles and honorifics add duration |
| Chinese — Simplified (zh-CN) | -30% (chars) / -10% (duration) | Very dense script, fast delivery |
| Arabic (AR) | +25% | RTL; longer in duration due to article particles |
| Hindi (HI) | +15% | Devanagari conjuncts, moderate expansion |

Budget rule of thumb: design the source VO with ≥15% duration headroom when DE / ES / FR / PT dubs are planned.

## Lip-Sync vs Voice-Over Decisions

| Delivery | When | Cost |
|----------|------|------|
| Full lip-sync dub | On-camera speaker, narrative fiction, premium brand content | Highest — requires per-syllable retiming, senior VO talent |
| Half-sync (phonetic match on close-ups only) | Corporate / explainer with on-camera speaker in some shots | Moderate — sync only close-ups |
| Off-camera VO (UN-style) | Documentary, product demos where speaker is heard but not tight-shot | Low — timing headroom to full scene length |
| Voice-over-with-subtitles | Technical / training content, budget-constrained | Lowest — subtitles absorb overrun |
| Original audio + subtitles only | Content with heavy-accent intimacy value | None — `captions` owns this |

Default for product / explainer video: **off-camera VO**. Default for testimonial with on-camera face: **voice-over-with-subtitles** unless budget justifies half-sync.

## Cultural Adaptation Checklist

Literal translations break in predictable places. Rewrite, don't translate, for each of these:

- **Idioms**: "home run" → locale equivalent for "clear success", not a baseball reference.
- **Currency**: "$99/month" → local currency with realistic price anchor, not arithmetic conversion.
- **Units**: miles / feet / Fahrenheit → metric; US paper sizes → ISO A4.
- **Dates / times**: MM/DD/YYYY → locale format; 12h → 24h for most non-US locales.
- **Examples and names**: "John from Acme" → plausible local name; avoid names that read as foreign.
- **Humor / sarcasm**: replace with locale-appropriate tone or neutralize.
- **Pop culture references**: TV / music / sports references rarely translate; swap or drop.
- **Politeness register**: JA / KO / DE formal vs informal; corporate content usually formal.
- **Number formatting**: decimal and thousands separators (`1,234.56` vs `1.234,56`).
- **Legal / compliance copy**: GDPR vs CCPA wording is locale-specific — consult Clause when in doubt.

## Voice Talent Brief Template

```markdown
### Voice Talent Brief — [Locale: de-DE]

**Project**: [name] — product explainer, 90s
**Voice profile**: Female, 28-40, warm-professional, Hochdeutsch (no regional accent)
**Tone**: Confident, clear, not corporate-flat. Reference: [link to source-language reference clip].
**Pace**: ~145 wpm target; scene-by-scene timing in attached table.
**Brand pronunciation**:
  - "Acme" → /ˈæk.mi/ (English pronunciation; do not Germanize)
  - "Workspace" → /ˈwɜːk.speɪs/ (English loan; do not translate)
**Tricky passages**:
  - Scene 4: "endpoint" — keep English, stress second syllable
  - Scene 7: product tagline MUST be delivered in single breath
**Delivery**: 48kHz/24-bit WAV, mouth noise removed, -23 LUFS integrated, peaks ≤ -1 dBTP
**Deadline**: [date]
```

## LQA Checklist

Linguistic QA, run by a native speaker before release:

- [ ] Meaning preserved — no accidental claim changes or hedging loss.
- [ ] Brand terms / product names pronounced per guide.
- [ ] Numerical claims (percentages, prices, durations) match source.
- [ ] Idioms feel natural to a native listener (not literally translated).
- [ ] Register (formal / informal) consistent across scenes.
- [ ] No rendering artifacts in TTS output (robotic stress, mispronunciations).
- [ ] Per-scene duration within ±10% of source budget.
- [ ] Profanity / taboo language absent (locale-specific; de-DE ≠ en-US thresholds).
- [ ] Cultural references adapted, not imported.
- [ ] Legal / compliance copy locale-appropriate.

A single failure in claim preservation or legal copy is a hard reject; style issues are a soft reject with revision notes.

## Anti-Patterns

- ❌ Starting localization before the source script is locked — every source edit triggers rework on every locale.
- ❌ Machine translation shipped without native LQA — breaks idioms, mis-registers formality, gets compliance copy wrong.
- ❌ Forcing all locales into the source duration budget — DE / ES overrun by design; plan headroom.
- ❌ Using the same voice talent profile across locales without adapting to cultural norms for authority / warmth.
- ❌ Translating product names — "Workspace" stays "Workspace" unless the brand has an approved local form.
- ❌ Skipping pronunciation guide for non-native brand terms — talent guesses, you rework the session.
- ❌ Lip-syncing off-camera narration — waste of budget; off-camera VO doesn't need sync.

## Handoff

On completion, hand off:

- **To Tone**: per-locale final scripts, pronunciation guide, TTS voice selection recommendation per locale, LUFS target and delivery format.
- **To `captions`**: localized script so translated captions can be timed against the dub, not the source.
- **To Warden**: completed LQA checklist per locale for accessibility + quality gate.
- **To user**: per-locale script package (script + brief + pronunciation guide + timing table), and a delta report listing any scenes where source-language intent was adapted rather than translated directly.
