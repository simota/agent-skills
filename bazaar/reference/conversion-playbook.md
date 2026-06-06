# Conversion Playbook

Industry-calibrated CVR baselines, copy frameworks, CTA strategy, and per-section heuristics. The playbook drives Strategy-stage CVR target setting and Structure-stage copy framework choice.

This is a reference, not a script. `bazaar` uses it to brief Funnel / Prose / Growth — those agents own the craft.

---

## CVR Baselines by LP Type

Source: synthesis of public benchmarks (Unbounce, WordStream, HubSpot, Databox 2024–2025) + practitioner calibration. Numbers assume **warm or mixed traffic** unless noted; cold paid traffic typically halves the median. Use as a starting point and calibrate against the client's own baseline.

| LP Type | Median CVR | Top Quartile | Top Decile | Traffic Qualifier | Friction Profile |
|---------|-----------|--------------|------------|-------------------|------------------|
| **SaaS Free Trial** | 2.0% | 4–5% | 7%+ | warm/mixed | Email-only signup (lowest friction trial path) |
| **SaaS Demo Request** | 1.5–3% | 5% | 8%+ | warm/mixed | 5–7 form fields, qualification gate |
| **SaaS Freemium Signup** | 4–8% | 12% | 18%+ | warm/mixed | Email + password, immediate product access |
| **E-com Product** | 1.5% | 3% | 5%+ | mixed | Trust + reviews + scarcity dominant |
| **E-com Cart Recovery LP** | 8–15% of recovery clickers | 20% | 30%+ | warm | Reminder + incentive (clarify denominator: % of clickers, NOT % of cart abandoners) |
| **Lead Magnet — warm traffic** | 20–30% | 40% | 50%+ | warm (email/retargeting) | Email-for-content, very low friction |
| **Lead Magnet — cold paid** | 5–10% | 15% | 25%+ | cold paid | Same form, lower intent |
| **Webinar / Event Registration** | 10–20% | 25% | 35%+ | warm/mixed | Urgency + speaker authority |
| **Newsletter Signup** | 1–3% | 5% | 8%+ | mixed | Value preview + frequency clarity |
| **B2B Contact / Enterprise — warm** | 2–4% | 5% | 8%+ | warm | Trust badges + case studies + named accounts |
| **B2B Contact / Enterprise — cold** | 1–2% | 3% | 5%+ | cold | Same with longer trust-build |
| **App Install (mobile web → app)** | 1–2% | 4% | 6%+ | mixed | Smart App Banner + value-first hero |
| **Course / Education Signup** | 3–6% | 10% | 15%+ | warm/mixed | Outcome promise + syllabus preview |
| **Real-Estate Lead** | 2–5% | 8% | 12%+ | mixed | Geo-specific + virtual tour |
| **Pricing Page** | 3–6% (next-step click) | 9% | 15%+ | warm | Plan-tier psychology + anchor pricing + comparison clarity |
| **Service / Consulting** | 2–4% | 6% | 10%+ | mixed | Case studies + trust + clear scope |

**Use**: lock the CVR target during Strategy stage. Communicate it to Funnel (structure decisions), Growth (CRO priority), Experiment (variant hypothesis).

---

## Copy Framework Choice

| Framework | When it fits | Section Order |
|-----------|--------------|---------------|
| **AIDA** (Attention / Interest / Desire / Action) | Default for consumer LPs, broad funnels | Hook hero → benefit interest → desire (proof) → CTA |
| **PAS** (Problem / Agitate / Solve) | B2B pain-driven products, security, compliance | Name pain → amplify cost → present solve |
| **BAB** (Before / After / Bridge) | Transformational products (fitness, productivity, education) | State before → show after → bridge = product |
| **4Ps** (Promise / Picture / Proof / Push) | High-CVR direct response, lead magnets, sales pages | Bold promise → vivid picture → social/numeric proof → strong push |
| **StoryBrand SB7** | Brand-driven B2B with hero-arc fit | Customer = hero, brand = guide, plan, call, success vs. failure |
| **JTBD-first** | Product-led SaaS where job is well-defined | Name the job → friction of current solutions → product as new way → proof |

**Rule**: choose ONE framework per LP. Mixing dilutes. Magi can arbitrate when two frameworks tie.

### Recipe → Framework Default Map

When the Recipe is known but the framework is ambiguous, default to this map (override only with Magi arbitration logged):

| Recipe | Default framework | Why |
|---|---|---|
| `premium` | Magi arbitration required (no default — brand-defining surface) | Stakes too high for default |
| `lead-gen` | **PAS** (Problem / Agitate / Solve) | B2B pain-driven decision |
| `saas` (free trial) | **JTBD-first** | Product-led; job is the wedge |
| `saas` (demo request) | **PAS** or **StoryBrand SB7** | Sales-assisted; objection-heavy |
| `ecom` | **AIDA** with strong proof block | Consumer impulse + trust |
| `event` | **4Ps** (Promise / Picture / Proof / Push) | Time-boxed; urgency + speaker authority |
| `magnet` | **4Ps** with stripped Push | Email-for-content; low friction |

---

## Section Sequence Heuristics

### High-converting default (consumer, ~1500 words)

1. **Hero**: headline + sub + primary CTA + hero asset (image/video/illustration) + optional trust strip (logos or numbers)
2. **Benefit block 1**: top benefit framed as outcome
3. **Benefit block 2**: second benefit framed as outcome
4. **Social proof block**: testimonials, case studies, numbers ("10,000+ teams")
5. **Objection handling**: FAQ-style or comparison table
6. **Benefit block 3**: third benefit (often "how it works" mini-explainer)
7. **Final CTA**: stronger close, urgency or risk-reversal
8. **FAQ**: 3–5 Q/A, scannable
9. **Footer with trust signals**: privacy, terms, contact, security badges

### B2B / Enterprise

1. Hero with named-account logo wall in trust strip
2. Pain framing (PAS) + cost of inaction
3. Solution overview with 3 capability pillars
4. Case study spotlight (specific customer, named numbers)
5. ROI / value calculator (if applicable)
6. Integration / security / compliance section
7. Demo request CTA
8. Resources (whitepapers, analyst reports)

### E-com Product

1. Hero with main product image + add-to-cart sticky
2. Key benefits + key specs (above the fold for mobile)
3. Image gallery + variant selector
4. Customer reviews + ratings (verified)
5. Use-case storytelling
6. FAQ
7. Cross-sell / related products
8. Trust footer (returns, shipping, warranty)

### Lead Magnet

1. Hero: cover image + title + email form (above the fold)
2. What's inside (3–5 bullet points)
3. Author credibility / brand authority
4. Sample preview (1–2 page snippets)
5. Final email form (repeat CTA)

### Event / Webinar

1. Hero: title + date + speakers + register CTA + countdown
2. Agenda
3. Speaker bios with social proof
4. Why attend (3 takeaways)
5. Past-event highlights or testimonials
6. Repeat register CTA + add-to-calendar

---

## CTA Strategy

| Decision | Heuristic |
|----------|-----------|
| **Primary CTA count above fold** | 1 (one). Decision fatigue is real. |
| **Repeat CTA frequency** | Every ~2 sections after benefit blocks; absolutely after social proof and after FAQ |
| **CTA microcopy** | Verb + outcome ("Start free trial", "Get the playbook", "Book a demo"). Avoid "Submit", "Click here". |
| **CTA button color** | High contrast vs. surrounding palette; aligned with brand accent. Test color in Experiment, not Strategy. |
| **Secondary CTA** | Single low-commitment option (e.g., "Watch a 2-min demo") if primary is high-friction |
| **Sticky CTA** | Mobile: yes for E-com and lead-gen. Desktop: optional for very long pages (>2500 words). |
| **Exit-intent CTA** | Lead-magnet downgrade or discount; A/B test before adopting (can hurt brand) |

---

## Form Design

| Decision | Heuristic |
|----------|-----------|
| **Field count** | Lead magnet: 1 (email). Free trial: 1–2. Demo request: 5–7 with qualification. Enterprise: 7–10. |
| **Progressive disclosure** | If >3 fields, break into 2–3 steps with progress indicator. Step 1 ≤ 2 fields. |
| **Label position** | Top-aligned (faster scan, accessibility friendly) |
| **Validation** | Inline, on blur; success-state microcopy |
| **Required-field marking** | Mark optional fields, not required (when most are required) |
| **Error microcopy** | Specific ("Email format looks off — example: name@company.com"), never "Invalid input" |
| **CAPTCHA** | Avoid unless bot traffic is verified pain. Bot Manager or invisible reCAPTCHA preferred. |

---

## Social Proof Hierarchy

In order of impact (highest first):

1. **Specific outcome from named customer**: "Acme cut onboarding time 67% in 30 days"
2. **Named-account logo wall**: well-known logos > unknown logos
3. **Numbers**: "10,000+ teams", "$1B+ processed", "4.8/5 from 12,000 reviews"
4. **Recognizable awards / press**: G2 Leader, Gartner Magic Quadrant, TechCrunch coverage
5. **Star-rating block** with review snippets
6. **Founder / leadership credibility**: when brand is early, founder authority can substitute
7. **Open-source / community signals**: GitHub stars, npm downloads, Discord member count (B2D)

**Anti-pattern**: avatar grid with no names ("our happy customers"). Reads as stock photo bingo.

---

## Trust Mechanics

Pick AT LEAST ONE trust mechanic per LP:

- Named-account social proof
- Money-back guarantee
- Free trial / no credit card
- Open-source / transparency
- Security badges (SOC 2, ISO 27001, GDPR)
- Press logos (only if Tier-1)
- Verified review platforms (G2, Capterra, Trustpilot, ProductHunt)
- Founder authority (B2D / B2SMB)
- Industry endorsement (when applicable)

---

## Urgency vs. Clarity Trade-off

| Approach | When it works | When it backfires |
|----------|---------------|-------------------|
| **Time scarcity** ("Offer ends Friday") | Real deadlines, events, launches | Manufactured urgency hurts brand long-term |
| **Quantity scarcity** ("3 spots left") | Cohort-based products, services with capacity | Visible-only-on-some-pages reads as dark pattern |
| **Loss framing** ("Stop losing X") | Cost-of-inaction is concrete and measurable | Generic loss framing reads as fearmongering |
| **Clarity ("Calm UI")** | Premium / trust-driven / B2B-enterprise | When CVR target is high and audience is action-ready, can underperform |

Magi arbitrates urgency vs. clarity during Strategy stage when persona signals are mixed.

---

## Common LP Failure Modes

| Symptom | Likely root cause | Repair |
|---------|------------------|--------|
| **Dual-promise drift** (hero says one thing, section 5 says another) | Two unrelated value props leaked past UNDERSTAND | Stop chain; return to UNDERSTAND; lock one promise; second promise becomes a separate LP |
| Low CVR + high bounce | Hero fails 5-second test (Hero-Contract Legibility ≤ 1/3) | Re-write hero in Structure stage |
| Low CVR + low bounce | Trust gap (Trust-Signal Density ≤ 1/4) | Strengthen social proof + guarantee + author authority |
| High click-through + low form submit | Form friction | Reduce field count, progressive disclosure |
| Inconsistent mobile | Above-fold breaks on common viewports / tap targets < 44px | Bolt + Voyager regression sweep |
| AI search not citing the page | GEO weakness; check per-platform tactic table | Growth — structured data, AI-friendly headings, citation-ready facts, AI bot crawl policy |
| Strong CVR but low quality leads | Targeting / qualification mismatch | Add qualification fields; tighten persona in Audience stage |
| Strong CVR + high refund/churn | Qualification gap (separate from low-quality leads) | Move qualification upstream; add deselect-friendly copy in objection block |
| Spike CVR then collapse | Burnt audience / scarcity overuse / FTC dark-pattern risk | Rotate creative, restore clarity-led variant; audit per FTC dark-pattern guidance |

---

## Calibration Workflow

1. **Read the brief**: identify LP type → look up baseline.
2. **Adjust for context**: brand maturity, traffic source, audience temperature.
3. **Set Strategy CVR target**: usually median × 1.5 → top-quartile range.
4. **Communicate to Funnel + Prose**: target drives copy aggression (calm vs. direct response).
5. **Lock in handoff bundle**: `CVR_Target` field in `LURE_STAGE_BUNDLE`.
6. **Validate post-launch in Beacon dashboard**: actual CVR vs. target; feedback loop to next iteration.
