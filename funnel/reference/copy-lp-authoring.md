# LP Copy Authoring Reference

Purpose: Author LP copy that converts — headline, hero body, value prop, benefit blocks, microcopy. Copy is the LP's load-bearing element; layout is scaffolding for words. This reference covers headline formulas (PAS / BAB / 4U), hero-section copy anatomy, value-prop clarity tests, microcopy patterns (button text, tooltips, helper text), readability targets, and LP-context tone and voice.

> **2026 traffic mix: LPs are read by AI agents, not only humans.** A meaningful share of LP visits comes from generative engines (ChatGPT, Perplexity, Claude, Gemini, Google AI Overviews) summarising the page to answer a user query elsewhere. Published 2025–2026 retail data shows AI-driven traffic up `~693%` YoY and ChatGPT referrals converting `~31%` higher than non-branded organic. Two implications for LP copy:
>
> 1. **Lead with the answer.** The headline + sub-head + first benefit block must be self-contained enough to be quoted verbatim by an AI engine without context. PAS / BAB / 4U formulas still apply; the cut-off for "summarisable answer" is the first 80–120 visible words.
> 2. **Attribute every claim.** Statistics need a named source, testimonials need a real name + title + company. Unsourced claims are silently demoted by AI summarisers and never make it into the citation. See `trust-signal-placement.md` for the source-attribution rules.

## Scope Boundary

- **Funnel `copy`**: LP headline, sub-head, hero body, benefit-block copy, section-level framing, CTA label drafting, and microcopy shells authored to conversion goals.
- **Prose (elsewhere)**: authoritative microcopy voice/tone system, design-system-wide error/empty/success copy, exact final wording polished to brand-voice guidelines.
- **Growth (elsewhere)**: copy frameworks applied across funnel stages (ads → LP → email nurture), SEO-driven headline formulas, keyword integration, GEO/AI-citation copy optimization.
- **Muse (elsewhere)**: typographic tokens (font size, weight, line-height, `text-wrap: balance`) — not the words themselves.
- **Vision (elsewhere)**: brand positioning, master-narrative, category framing upstream of any LP copy.

If the question is "what does the headline need to do?" → `copy`. If it's "what is our brand voice across every surface?" → Prose. If it's "how do we say this same benefit in the Google Ad and nurture email?" → Growth.

## Headline Formulas

Pick one formula. Generate 5+ candidates before selecting. The winner is the one that passes the 5-second test: can a stranger restate the value prop after 5 seconds of exposure?

### PAS — Problem · Agitate · Solution

Use when audience is problem-aware (knows the pain, searching for relief).

```
[Problem statement] → [Consequence / urgency] → [Solution framing]
```

Example:

- Problem: `Your team is still chasing invoices in spreadsheets.`
- Agitate: `Every lost invoice is revenue that walks away.`
- Solution: `[Product] automates collections so you get paid on time.`

Headline candidate: **"Stop losing revenue to lost invoices."**

### BAB — Before · After · Bridge

Use when transformation is tangible and demonstrable (before-state and after-state are visually or numerically different).

```
[Before — current painful state] → [After — desired state] → [Bridge — the product]
```

Example:

- Before: 4 hours of weekly reporting.
- After: Reports auto-generated in 3 minutes.
- Bridge: AI-driven reporting that learns your metrics.

Headline candidate: **"From 4-hour reports to 3 minutes."**

### 4U — Urgent · Unique · Useful · Ultra-specific

Use when competing in a crowded category and differentiation is the blocker.

| Dimension | Test |
|-----------|------|
| Urgent | Is there a time element? |
| Unique | Can a competitor say the same sentence? (If yes, rewrite.) |
| Useful | Does the reader get a concrete outcome? |
| Ultra-specific | Is there a number, name, or timeframe? |

Headline candidate: **"Ship a production Stripe integration in 30 minutes — without touching webhooks."**

### Formula Selection by Audience State

| Audience state | Best formula |
|---------------|--------------|
| Unaware | Curiosity hook or stat (PAS / BAB assume existing pain) |
| Problem-aware | PAS |
| Solution-aware | BAB |
| Product-aware | 4U |
| Most-aware | Offer-led ("50% off until Friday") |

## Hero-Section Copy Anatomy

```
┌─────────────────────────────────────────────┐
│ [Eyebrow]  ← optional category / social proof│
│ [Headline] ← main value prop, ≤ 8 words      │
│ [Sub-head] ← expansion, ≤ 20 words, who + how│
│ [CTA copy] ← value-restating action          │
│ [Trust line] ← optional, "no credit card" etc│
└─────────────────────────────────────────────┘
```

**Headline constraints:**

- ≤ 8 words / ≤ 44 characters (forces clarity, removes jargon).
- Answers "What's in it for me?" in one pass.
- No brand name in the headline unless the brand itself is the value (e.g., "Notion for teams" only works when Notion is already known).
- Use `text-wrap: balance` in CSS so line breaks favor readability.

**Sub-head constraints:**

- ≤ 20 words, one sentence.
- Completes the picture: **who** it's for + **how** it works + **why** it's different.
- Do not restate the headline — expand it.

Example pairing:

- Headline: "Ship Stripe in 30 minutes."
- Sub-head: "For indie devs and 2-person startups who need payments live today — no webhook handling, no compliance tickets, one SDK call."

## Value-Prop Clarity Tests

Run the draft through all four before committing.

| Test | Method | Fail condition |
|------|--------|----------------|
| 5-second test | Show a stranger for 5s, remove, ask "what does it do?" | Cannot restate core value |
| Grandma test | Read to a non-domain reader | Any jargon unexplained |
| Competitor-swap test | Replace your product with a competitor's — does the copy still fit? | If yes, it's not differentiated |
| So-what test | After every benefit claim, ask "so what?" recursively until you hit an outcome | Ends at a feature, not an outcome |

## Benefit vs Feature Conversion

Every feature statement must be rewritten as a benefit. A feature describes the product; a benefit describes the reader's post-purchase life.

| Feature (what it has) | Benefit (what the reader gets) |
|----------------------|-------------------------------|
| "256-bit SSL encryption" | "Bank-level data protection for your customers" |
| "OAuth 2.0 support" | "Users log in with Google — one less password to forget" |
| "99.99% uptime SLA" | "Your store stays open even when we push updates" |
| "10M-row data exports" | "Export an entire year of analytics to a CSV — without chunking" |
| "Realtime sync" | "Your team sees the same data at the same time, no refresh" |

**Rule:** Feature is fine as a supporting detail under the benefit, never as the benefit itself.

## Microcopy Patterns

### Button text

- State the value, not the mechanism. "Get my report" beats "Submit form".
- Possessive framing ("my") outperforms neutral ("your" / none) by ~10% in LP A/B.
- Under 5 words; verb-first.

### Helper text (under input labels)

- Tell the reader what format to use before they guess.
- Example: `We'll send your receipt here. Use a work email for team access.`
- Never duplicate the label. If the label is "Email", do not also write "Enter your email".

### Tooltip copy

- One sentence. If it needs two, redesign the UI.
- Start with the answer, not context. `Annual billing saves 20%` beats `About annual billing: you save 20%`.

### Trust-line copy (near CTA / form)

- Remove specific risk objections: `No credit card required · Cancel anytime · We never share your email`.
- Keep to 3 items max, pipe-separated. More reads as defensive.

### Error-message shells

Funnel drafts the shell. Prose polishes the final wording.

| Context | Shell pattern |
|---------|--------------|
| Field-level validation | `[Field] [what's wrong]. [How to fix it].` |
| Server-side failure | `We couldn't [verb]. [Likely cause]. [Next action].` |
| Network / retry | `Something went wrong on our end. [Retry action].` |

## Readability Targets

LP copy is skimmed, not read.

| Metric | LP target |
|--------|-----------|
| Flesch Reading Ease | 60-70 (8th-grade level) |
| Average sentence length | 12-18 words |
| Paragraph length | 1-3 sentences |
| Passive voice | < 10% |

**Rule:** If the headline Flesch score is below 50, rewrite. Technical LPs (dev tools, finance) may reach 50-60, but never below.

## Tone and Voice for LP Context

LPs live on a compressed trust timeline — every word must earn the next. Default LP tone:

| Dimension | LP default | Why |
|-----------|-----------|-----|
| Formality | Mid-casual | Too formal reads as corporate fluff; too casual reads as unserious for B2B |
| Confidence | High, unhedged | "Ship in 30 minutes" beats "Helps you potentially ship faster" |
| Specificity | Numbers and names | "Join 1,247 teams" beats "Join thousands" |
| Perspective | Second person ("you") | First-person ("we help") centers the company, not the reader |
| Certainty | Declarative | Avoid "may" / "might" / "can help" — they leak into every weak headline |

**Voice shifts by LP type:**

- B2B SaaS → confident, data-specific, outcome-framed.
- Consumer product → warmer, sensory, story-adjacent.
- Developer tool → precise, code-literate, jargon-OK when accurate.
- Enterprise → measured, compliance-aware, risk-reducing.

## Anti-Patterns

- ❌ Headline with two value props connected by "and" — forces the reader to choose what matters.
- ❌ Starting the headline with the company name.
- ❌ Adjective-stacked benefits: "revolutionary, innovative, best-in-class platform" (all three words do zero work).
- ❌ "The [category] for [audience]" as the only positioning. Copies every competitor.
- ❌ Sub-head that repeats the headline with different words.
- ❌ Feature-listing where benefits are required (pricing page is fine; LP hero is not).
- ❌ "We" / "our" dominance — count pronouns; if "we" > "you", rewrite.
- ❌ Passive-voice testimonials: "This product was found useful" → "I cut my close time in half."
- ❌ CTA copy as a direction ("Click here", "Scroll down") — direction is the UI's job, not the copy's.
- ❌ Jargon in the first paragraph of the LP. Jargon in paragraph 3 under a features heading is acceptable.

## Handoff

**To Prose** (voice polish):

- Draft copy with section-by-section rationale (what each block must accomplish).
- Tone calibration notes (B2B SaaS / consumer / dev-tool / enterprise).
- Terms deliberately chosen vs brand-voice defaults (flag for review).
- Error/empty/success shells needing final wording.

**To Growth** (cross-stage framework):

- Headline formula selected (PAS / BAB / 4U) and the one-sentence value prop.
- Primary benefit list ranked by importance — Growth reuses in Google Ads, social, nurture email.
- SEO-target keywords that must appear in H1 / H2 (if constrained).

**To Artisan** (implementation):

- Final copy with section anchors (`#hero`, `#benefits`, `#cta-final`).
- Character-count budget per field (for responsive truncation handling).
- `text-wrap: balance` flag on headline and sub-head.
