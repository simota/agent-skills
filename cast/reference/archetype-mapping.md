# Archetype Mapping Reference

Purpose: Tag personas with brand and behavioral archetypes so downstream agents (Echo, Spark, Voice, Bond) inherit consistent narrative DNA. Cover Jung 12 brand archetypes, Jobs-To-Be-Done archetype model, persona-archetype mapping, and brand consistency validation.

## Scope Boundary

- **cast `archetype`**: Brand + JTBD archetype tagging on personas (this document).
- **cast `generate` (elsewhere)**: Persona generation from sources.
- **Saga (elsewhere)**: Customer story narratives (uses archetypes downstream).
- **Vision (elsewhere)**: Brand identity direction.
- **Field (elsewhere)**: Foundational user research.

## Two Archetype Layers

| Layer | Purpose | Source |
|-------|---------|--------|
| **Brand Archetype** | Persona's emotional / aspirational identity (who they want to be) | Carl Jung / Margaret Mark + Carol Pearson |
| **JTBD Archetype** | Persona's job-when-they-hire-the-product (functional / emotional / social) | Clayton Christensen / Bob Moesta |

A persona ideally maps to both: **Brand archetype** for tone of voice, **JTBD archetype** for feature priority.

## The 12 Jung Brand Archetypes

| # | Archetype | Core desire | Voice | Example brands |
|---|-----------|-------------|-------|----------------|
| 1 | **Innocent** | Safety, simplicity | Optimistic, sincere | Coca-Cola, Dove |
| 2 | **Sage** | Truth, understanding | Authoritative, thoughtful | Google, BBC |
| 3 | **Explorer** | Freedom, discovery | Adventurous, restless | Patagonia, Jeep |
| 4 | **Outlaw** | Liberation, disruption | Rebellious, blunt | Harley-Davidson, Virgin |
| 5 | **Magician** | Transformation, vision | Mystical, inspiring | Apple, Tesla, Disney |
| 6 | **Hero** | Mastery, achievement | Bold, confident | Nike, BMW |
| 7 | **Lover** | Intimacy, beauty | Sensual, warm | Chanel, Häagen-Dazs |
| 8 | **Jester** | Joy, playfulness | Funny, irreverent | Old Spice, M&M's |
| 9 | **Everyman** | Belonging, fairness | Friendly, down-to-earth | IKEA, Levi's |
| 10 | **Caregiver** | Service, compassion | Nurturing, supportive | Johnson & Johnson, Volvo |
| 11 | **Ruler** | Control, status | Refined, commanding | Rolex, Mercedes |
| 12 | **Creator** | Innovation, expression | Visionary, expressive | Adobe, LEGO |

Three motivational families:
- **Order**: Caregiver, Ruler, Creator (provide structure)
- **Belonging**: Lover, Jester, Everyman (foster connection)
- **Change**: Hero, Outlaw, Magician (mastery + transformation)
- **Meaning**: Innocent, Sage, Explorer (independence + truth)

## JTBD Archetypes

```
            FUNCTIONAL
                |
                |  "Help me get this job done"
                |
EMOTIONAL ──────┼────── SOCIAL
                |
"Help me feel"  |  "Help me be seen as..."
```

Per Christensen, every "hire" of a product satisfies a mix of:
- **Functional**: solve a tangible task ("file taxes correctly")
- **Emotional**: feel a way ("feel competent, not anxious")
- **Social**: be seen a way ("be seen as responsible")

JTBD archetype categorizes the *dominant* dimension. A persona may have multiple jobs; identify the primary one for product positioning.

## Persona ↔ Archetype Mapping

```yaml
persona:
  id: P-042
  name: Aoi Mori
  brand_archetype:
    primary: Sage
    secondary: Caregiver
    rationale: |
      Wants accurate information first, then to share it with others.
      Quotes: "I read 3 reviews before any purchase" / "I always tell my colleagues."
  jtbd_archetype:
    job_dimension: emotional
    job_statement: "When I'm evaluating a complex tool, I want to feel confident that I haven't missed anything, so I can recommend it without reservation."
    functional_aspect: thorough comparison
    emotional_aspect: confidence, low regret
    social_aspect: trusted advisor
```

## Selection Heuristics

```
RAW PERSONA EVIDENCE  →  ARCHETYPE TAG
──────────────────────────────────────
"I research extensively"           → Sage
"I want to feel free / explore"    → Explorer
"I need to look successful"        → Ruler / Hero (depending on tone)
"I want simple, no surprises"      → Innocent / Everyman
"I love clever / playful brands"   → Jester / Creator
"I take care of others"            → Caregiver
"I disrupt the status quo"         → Outlaw
"I want transformation"            → Magician
```

Use evidence quotes from interviews / reviews / support tickets — never assign by intuition alone.

## Brand-Archetype Consistency Check

For multi-persona sets, validate that the *brand* the personas serve has a coherent archetype mix:

| Brand archetype | Dominant persona archetypes |
|-----------------|----------------------------|
| Apple (Magician) | Magician + Creator + Explorer |
| Patagonia (Explorer) | Explorer + Caregiver |
| Stripe (Sage) | Sage + Creator |

If the persona set has ≥3 dominant archetypes that don't ladder up to a coherent brand, the segmentation is wrong.

## Workflow

```
EVIDENCE     →  collect quotes / behaviors per persona
             →  tag each behavior with motivational family

JUNG-MAP     →  primary brand archetype (single)
             →  secondary archetype (modifier)
             →  rationale with ≥3 evidence citations

JTBD-MAP     →  identify job statement (When __, I want __, so I can __)
             →  classify dominant dimension (F/E/S)
             →  enumerate F + E + S aspects

CONSISTENCY  →  brand-level archetype coherence
             →  flag personas that don't ladder up
             →  brand archetype = mode of persona archetypes

VALIDATE     →  evidence-cited quotes per archetype
             →  no archetype assigned without ≥3 quotes
             →  archetype + JTBD compatibility (e.g., Sage+Functional ✓; Outlaw+Innocent ✗)

DELIVER      →  registry update with archetype + jtbd fields
             →  tone-of-voice guide per archetype
             →  feature-priority hint from JTBD dimension

HANDOFF      →  Saga: narrative voice
             →  Spark: feature priority via JTBD
             →  Voice: tone-of-voice copy
             →  Echo: archetype-aligned cognitive walkthrough
             →  Bond: emotional retention triggers
```

## Output Template

```markdown
## Archetype Mapping: [Persona Set]

### Persona Archetype Table
| ID | Name | Brand Primary | Brand Secondary | JTBD Dim | Job Statement (compact) |
|----|------|---------------|-----------------|----------|--------------------------|
| P-001 | Aoi | Sage | Caregiver | Emotional | feel confident before recommending |
| P-002 | Ren | Hero | Ruler | Social | be seen as the high-performer |
| P-003 | Hana | Caregiver | Innocent | Functional | protect family from financial risk |

### Evidence per Persona
- **P-001 / Sage**:
  - "I always read 3 reviews before buying" (interview T-12)
  - "I keep a Notion of every decision rationale" (behavior log)
  - "I recommend tools to my team on Slack" (Slack mining)
- **P-002 / Hero**: ...

### JTBD Statements
- P-001: "When evaluating a complex tool, I want to feel confident I haven't missed anything, so I can recommend it without reservation."
- P-002: ...

### Brand-Level Coherence
- Modal archetype across personas: [Sage]
- Implied brand archetype: [Sage] — matches stated brand: [yes / no]
- Outliers: [persona IDs that don't ladder up + recommendation]

### Tone-of-Voice Hints
- Sage: authoritative, thoughtful, evidence-led — avoid casual or playful
- Hero: confident, achievement-framed — quantify impact

### JTBD-Driven Feature Priority
- Functional dim → tools, data, integrations
- Emotional dim → reassurance UX, tooltips, undo, confirmation
- Social dim → sharing, badges, public profiles

### Handoffs
- Saga: narrative voice + character sheet
- Spark: feature priority by JTBD dimension
- Voice: per-archetype copy guide
- Echo: walkthrough with archetype-consistent reactions
- Bond: emotional retention triggers per archetype
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Picking archetype by gut without evidence | Require ≥3 evidence quotes per assignment |
| Multiple primary archetypes per persona | One primary + one optional secondary (modifier) |
| Brand archetype != mode of persona archetypes | Re-segment; personas serving different brands shouldn't share a set |
| JTBD with all three F/E/S equally weighted | Pick the *dominant* dimension; secondary aspects are context |
| Job statement missing one of the When/Want/So-that clauses | Use full template; partial JTBDs are aspirational, not actionable |
| Stereotyping (Sage = nerdy male, Lover = young female) | Bias-audit: representation matrix; archetypes are universal |
| Archetype + JTBD incompatibility (Outlaw + Functional only) | Outlaw is emotional/social; check archetype × JTBD compatibility |
| Tagging only personas, never the brand | Brand archetype enables consistency at portfolio level |
| Reapplying archetype as a persona name (Persona "The Sage") | Archetype is a tag; persona has a real-life-resembling name |
| Static archetype with no review cadence | Re-validate during evolve; market shifts drift archetypes |
| Using archetypes as creative shortcut without behavior | Archetype must trace to evidence; otherwise persona drifts |
| Forcing Jung 12 onto B2B-only personas | Adapt for B2B: Sage / Ruler / Caregiver / Hero are typically dominant |

## Deliverable Contract

When `archetype` completes, emit:

- **Per-persona archetype** (primary + secondary, JTBD dimension).
- **Evidence citations** (≥3 quotes per archetype).
- **Job statement** (When / Want / So-that template).
- **Brand-level coherence check**.
- **Tone-of-voice hints** per archetype.
- **JTBD-driven feature priority** hint.
- **Handoffs**: Saga, Spark, Voice, Echo, Bond.

## References

- *The Hero and the Outlaw* — Margaret Mark + Carol Pearson (12 archetype framework, 2001)
- Carl Jung — *Archetypes and the Collective Unconscious* (1959)
- *Competing Against Luck* — Clayton Christensen + Karen Dillon + David Duncan + Taddy Hall (2016) — JTBD framework
- *Jobs to be Done* — Tony Ulwick (Outcome-Driven Innovation)
- *Demand-Side Sales 101* — Bob Moesta + Greg Engle (JTBD interview techniques)
- JTBD Pyramid™ — AIM Institute (2025) — addresses five common JTBD practitioner challenges
- *Building a StoryBrand* — Donald Miller (brand archetypes for narrative)
- *Designing Brand Identity* — Alina Wheeler
- *About Face* — Alan Cooper (persona origins)
- *The Persona Lifecycle* — Pruitt + Adlin
- "Brand Archetypes: A Practical Framework" — Iconic Fox / IDEO white papers
- Jung typology test resources (note: MBTI continues to face significant academic-validity criticism — use only as a creative prompt, not as evidence)
- ISO 9241-210 — Human-centered design (persona context)
- *Lean UX* — Jeff Gothelf + Josh Seiden (proto-personas)
- Microsoft Inclusive Design — Persona Spectrum approach (`inclusive.microsoft.design`, refreshed 2024-2025) as a complementary lens to archetype tagging
