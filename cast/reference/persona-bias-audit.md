# Persona Bias Audit Reference

Purpose: Detect and remediate bias in persona sets. Cover representation matrix, intersectionality coverage, stereotyping detection, the Inclusive Persona Checklist, name/photo bias, ableism, ageism, and locale bias. Personas with embedded bias propagate downstream into Echo walkthroughs, Spark feature priorities, and Voice copy.

## Scope Boundary

- **cast `bias-audit`**: Persona representation + ethical audit (this document).
- **cast `archetype` (elsewhere)**: Brand / JTBD archetype tagging.
- **Cloak (elsewhere)**: Privacy / consent / PII handling.
- **Comply (elsewhere)**: Regulated context (e.g., insurance non-discrimination).
- **Plea (elsewhere)**: Synthetic user voice (separate concern, but shares ethics surface).

## Why Bias Audits

Personas are reasoning shortcuts — they shape *every* downstream decision. Biased personas produce:

- Excluded users (features that don't fit)
- Stereotyped UX ("women want pink", "elders need huge fonts")
- Discriminatory pricing or eligibility
- Hostile design (assuming all users speak English, have stable WiFi, hold a credit card)
- Reinforcement of marketing tropes

## The Five Bias Lenses

| Lens | Question | Tool |
|------|----------|------|
| **Representation** | "Who's missing?" | Representation matrix |
| **Intersectionality** | "Who exists at the cross of multiple identities?" | Crenshaw-style intersection grid |
| **Stereotype** | "Are attributes stuck together by tradition not data?" | Attribute-correlation audit |
| **Power** | "Who designed this — and whose lens is encoded?" | Designer reflexivity statement |
| **Harm** | "What harm does this persona enable / prevent?" | Inclusive Persona Checklist |

## Representation Matrix

```
                Age
        18-24  25-34  35-44  45-54  55-64  65+
Gender ┌──────┬──────┬──────┬──────┬──────┬─────┐
F      │  1   │  2   │  1   │      │      │     │
M      │      │  3   │  1   │      │  1   │     │
NB     │      │      │      │      │      │     │
       └──────┴──────┴──────┴──────┴──────┴─────┘
```

Generate per dimension: gender × age, ability × locale, income × education, etc. Empty cells = potentially unserved.

Compare against:
- Customer base (who actually uses the product)
- Total addressable market (who could)
- Census / domain norms (sanity check)

Flag dimensions where persona set ≠ population. "We have 5 personas, all male, all 25-34" is a red flag even for a B2B dev tool.

## Intersectionality Grid

A persona at one identity (woman) is not the same as at the intersection (woman + Black + lower-income + rural + non-native English). Crenshaw 1989: discrimination is multiplicative, not additive.

| Persona | Gender | Race | Income | Ability | Locale | Native lang |
|---------|--------|------|--------|---------|--------|-------------|
| P-001 Aoi | F | Asian | mid | none | Tokyo | JA |
| P-002 Marcus | M | Black | low | dyslexia | rural US | EN |
| P-003 Priya | F | South Asian | high | colorblind | London | EN |

Empty intersections = blind spots. Personas at unexpected intersections often reveal the strongest UX gaps.

## Stereotype Detection

Run an attribute-correlation audit: do attributes cluster by tradition rather than data?

Smell tests:
- All female personas are caregivers / nurturing
- All male personas are technical / decisive
- Older personas described as "tech-averse" without evidence
- Lower-income personas described as "price-sensitive" only
- Disabled personas defined by their disability
- Non-Western personas described in exotic / othering tone
- LGBTQ+ identity treated as personality

Per attribute, ask: *Is this trait evidenced in data, or imported from cliché?*

## Inclusive Persona Checklist

Adapted from Microsoft Inclusive Design Toolkit + W3C Accessible Personas guidance:

```
[ ] Persona attributes have provenance citations (interview, survey, log)
[ ] Demographic doesn't predict role (e.g., not all "young" = "tech-savvy")
[ ] Photo / name doesn't reinforce stereotypes (or photo is omitted)
[ ] Disability represented in ≥20% of persona set
[ ] At least 1 persona has a temporary or situational impairment
[ ] Income range spans free-to-paid users
[ ] Locale / language diversity beyond default
[ ] Naming reflects intended market diversity
[ ] Goals / pains in user's own words where possible
[ ] No persona reduced to a single identity attribute
[ ] LGBTQ+ identity (if relevant) treated as context, not center
[ ] Ableism, ageism, classism flags clear (zero-tolerance items)
[ ] Test of Time check: would this persona embarrass us in 5 years?
[ ] Stress-case persona present (denied, abandoned, hostile context)
[ ] Designer reflexivity statement: who built this and whose blind spots?
```

Required: ≥ 13/15 pass. Disability + stress-case items are mandatory (block on fail).

## Name + Photo Bias

Names and photos encode identity quickly — and lazily.

```
Anti-pattern    →  Fix
"Jessica, 24, F"           →  Real-feeling name + clear cultural origin
Stock photo of smiling woman →  Diverse photo set OR omit photo entirely
Anglo-only name pool        →  Match target market diversity
"Tech-savvy millennial"     →  Specific behaviors, not generation labels
```

If photo can't be diverse, omit. A name + role + behaviors carries more weight than a photo.

## Ableism, Ageism, Classism Pitfalls

| Bias | Example | Fix |
|------|---------|-----|
| Ableism | "Power user with no impairment" | Include disabilities (vision, motor, cognitive); include situational (loud train, one-handed) |
| Ageism | "Old user struggles with tech" | Older users may be expert; specify behavior, not age |
| Classism | "Premium users are sophisticated" | Income ≠ taste; describe needs, not aesthetics |
| Westernism | Default = US/UK | Test names, holidays, currencies, RTL languages |
| Cisheteronormativity | Assume gender binary, opposite-sex pairing | Use NB; pronoun fields; decouple identity from product use |
| Neurotypicalism | All personas plan, focus, respond similarly | Include ADHD, autism, dyslexia patterns |

## Stress-Case Personas

Eric Meyer + Sara Wachter-Boettcher (*Design for Real Life*): every persona set must include people in crisis or hostile contexts.

- Recently divorced / bereaved (sensitive copy)
- Domestic abuse victim (privacy, escape buttons)
- Refugee / asylum seeker (trust, language barrier)
- Recently disabled (re-learning the interface)
- Identity theft victim (low trust)
- Burned out professional (low cognitive load)

These reveal where the product fails the most vulnerable.

## Workflow

```
COLLECT     →  load all personas in registry
            →  list every demographic + behavioral attribute

REPRESENT   →  build representation matrix per pair (gender×age, ability×locale, ...)
            →  flag empty cells vs target market
            →  sanity-check against census / domain norms

INTERSECT   →  intersectionality grid: identify unmet intersections
            →  add ≥1 persona per critical empty intersection

STEREOTYPE  →  attribute-correlation audit
            →  flag clichéd pairings; require evidence per pair

POWER       →  who designed the persona set?
            →  reflexivity statement: known blind spots
            →  external review by underrepresented voice if possible

CHECKLIST   →  apply Inclusive Persona Checklist (13/15 minimum)
            →  disability + stress-case mandatory

NAME-PHOTO  →  name pool diversity
            →  photo diversity or omission

REMEDIATE   →  add missing personas
            →  rewrite stereotyped attributes with evidence
            →  flag personas that fail checklist with severity

REPORT      →  bias audit report with severity tiers
            →  recommended additions / rewrites

HANDOFF     →  back to cast `generate` for missing personas
            →  Cloak: privacy review of new attributes
            →  Comply: regulated-context check
            →  Voice / Echo / Spark: re-run downstream with debiased set
```

## Output Template

```markdown
## Bias Audit: [Persona Set]

### Representation Matrices
**Gender × Age**
[matrix]
- Empty cells: [list]
- vs market base: [delta]
- Severity: [low / med / high]

**Ability × Locale**
[matrix]
- ...

### Intersectionality Grid
[grid showing personas at intersections]
- Critical missing intersections: [list]

### Stereotype Audit
| Attribute pair | Personas | Evidence? | Verdict |
|---------------|----------|-----------|---------|
| Female + caregiving | P-002, P-003 | weak (assumption) | REWRITE |
| Older + tech-averse | P-005 | none | DROP |
| Premium + sophisticated | P-001 | none | DROP |

### Inclusive Persona Checklist Score
- [N/15] passed
- Mandatory items (disability, stress-case): [PASS / FAIL]
- Severity if FAIL: [block]

### Name + Photo
- Name diversity: [pool stats]
- Photo: [diverse / omitted / homogeneous → recommend change]

### Reflexivity
- Persona set authored by: [team profile]
- Known blind spots: [list]
- External review: [yes / no, by whom]

### Stress-Case Coverage
- [list of stress-case personas; recommend add if missing]

### Severity-Tiered Findings
**BLOCK** (must fix before downstream use):
- [item]

**WARN**:
- [item]

**INFO**:
- [item]

### Recommended Additions
- New persona: [profile sketch] — fills [intersection]

### Recommended Rewrites
- P-002: drop "nurturing by default" → replace with evidence-cited behavior

### Handoffs
- cast `generate`: produce additions
- Cloak: privacy review
- Comply: regulated check (if applicable)
- Echo / Spark / Voice: re-run downstream after fix
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Audit done by the same team that authored the personas | External or rotated reviewer |
| Demographic diversity treated as token (1 disabled persona) | ≥20% disability representation |
| Stress cases excluded as edge case | Stress cases reveal mainstream design failures |
| "Cultural sensitivity" approximated by name change | Validate behaviors, holidays, payment methods, language |
| Photo diversity without behavioral diversity | Behaviors carry the weight; photos are secondary |
| Persona reduced to one identity ("the disabled user") | Disability is context; persona has goals + jobs + values |
| Audit at end of process | Audit during persona design, not after |
| Anti-stereotype overcorrection ("now all female personas are CEOs") | Variation, not flipped stereotypes |
| Skipping reflexivity statement | Designer blind spots are the source of bias |
| Treating audit as one-time | Re-audit on every persona evolve cycle |
| Conflating bias with statistical fairness in ML | Persona bias ≠ ML fairness; both matter, separately |
| Photo of Western face for "global" persona | Match the actual market or omit |
| Ignoring locale / RTL / non-Latin scripts | Test name + content rendering across scripts |
| Assuming intersectional users are "edge" | They're often majority in real markets |

## Deliverable Contract

When `bias-audit` completes, emit:

- **Representation matrices** with empty-cell flags.
- **Intersectionality grid** with critical missing intersections.
- **Stereotype audit table** with verdicts.
- **Inclusive Persona Checklist** (15-item) score with mandatory-pass status.
- **Name + photo** diversity assessment.
- **Reflexivity statement** + external review status.
- **Stress-case coverage** check.
- **Severity-tiered findings** (BLOCK / WARN / INFO).
- **Remediation list** (additions + rewrites).
- **Handoffs**: cast generate, Cloak, Comply, downstream re-run.

## Regulatory & Standards Context (as of 2026-05)

Persona bias work increasingly intersects with formal AI-governance obligations. Cast bias audits should reference applicable frameworks rather than ad-hoc rules:

| Framework | Status (2026-05) | Relevance to persona bias |
|-----------|------------------|---------------------------|
| **ISO/IEC 42001:2023** (AI Management System) | Published Dec 2023; certifiable; major vendors (SAP, Cornerstone Galaxy, etc.) certified through 2025 | Persona artifacts feeding AI systems fall under AIMS scope — Annex A controls cover bias mitigation, human oversight, lifecycle management |
| **ISO/IEC 23894:2023** (AI Risk Management) | Published Feb 2023; companion to ISO 31000 + ISO/IEC 42001 | Adds AI-specific risk categories: algorithmic transparency, fairness/bias, robustness, human-AI interaction risks — apply to AI-generated personas |
| **NIST AI RMF 1.0** + **AI 600-1 Generative AI Profile** | RMF Jan 2023; GenAI Profile published 2024-07-26 (NIST.AI.600-1) | Profile enumerates 12 GenAI-specific risks with 200+ suggested actions across Governance, Content Provenance, Pre-deployment Testing, Incident Disclosure |
| **EU AI Act** (Regulation 2024/1689) | Published 2024-07; GPAI obligations + AI Office operational from 2025-08-02; GPAI penalties from 2026-08-02; pre-existing GPAI models full compliance by 2027-08-02 | Personas used to train or evaluate GPAI models become AI-Act-relevant artifacts — bias audit evidence is part of conformity assessment |
| **IEEE 7000-2021** (Value-Based Engineering) | Published Sep 2021; technology-agnostic ethical-design methodology | Translates ethical values into measurable requirements — pair with bias audit checklist for traceability |
| **C2PA Content Credentials 2.2** | Spec released 2025-04-22 / 2025-05-01 | If persona artifacts include AI-generated photos, attach C2PA assertions for provenance (origin, AI-use, edits) |
| **APPI Amendment Bill (Japan)** | Cabinet-approved 2026-04-07; Diet review in progress; enforcement within 2 years of promulgation (by 2028) | New statistical-processing exemption permits AI-training use of personal data with transparency safeguards; strengthens biometric + children's-data protections; introduces administrative fines under expanded PPC powers |

For AI-generated personas, Cast bias audits should at minimum align with NIST AI 600-1 actions and ISO/IEC 23894 risk categories.

## References

- Kimberlé Crenshaw, "Demarginalizing the Intersection of Race and Sex" (1989)
- *Design for Real Life* — Eric Meyer + Sara Wachter-Boettcher (stress cases)
- *Mismatch* — Kat Holmes (inclusive design at Microsoft)
- *Technically Wrong* — Sara Wachter-Boettcher (bias in tech)
- *Algorithms of Oppression* — Safiya Noble
- Microsoft Inclusive Design Toolkit — `inclusive.microsoft.design` (refreshed 2024-2025 around 10-year anniversary; Persona Spectrum concept; Fluent 2 design system)
- W3C Accessible Personas — `w3.org/WAI/planning/personas/`
- *Lean UX* — Gothelf + Seiden (proto-persona ethics)
- *Just Enough Research* — Erika Hall (interview rigor)
- POUR principles — WCAG (Perceivable, Operable, Understandable, Robust)
- ISO 9241-220 — Human-centered design processes
- ISO/IEC 42001:2023 — AI Management System (`iso.org/standard/42001`)
- ISO/IEC 23894:2023 — Guidance on risk management for AI (`iso.org/standard/77304.html`)
- NIST AI RMF 1.0 + AI 600-1 Generative AI Profile (2024-07; `doi.org/10.6028/NIST.AI.600-1`)
- EU AI Act — Regulation (EU) 2024/1689 (`artificialintelligenceact.eu/implementation-timeline/`)
- IEEE 7000-2021 — Model Process for Addressing Ethical Concerns During System Design
- C2PA Content Credentials Technical Specification 2.2 (`spec.c2pa.org/specifications/specifications/2.2/`)
- Japan APPI Amendment Bill 2026 — `ppc.go.jp` (Personal Information Protection Commission)
- Geert Hofstede — *Cultures and Organizations* (locale dimensions)
- *Sorting Things Out* — Bowker + Star (categorization politics)
- Ruha Benjamin, *Race After Technology*
- Joy Buolamwini, "Gender Shades" (algorithmic bias parallel)
