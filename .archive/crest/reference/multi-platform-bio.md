# Multi-Platform Bio

## Purpose

An engineer needs many bios — GitHub one-line, LinkedIn About, X 160-char, conference 50-word, long 200-word. They must be **coherent** (same person across platforms) yet **calibrated** (each platform's length, tone, and reader expectation). This reference defines the canonical bio family and the platform tuning rules.

## Scope Boundary

- IN scope: bio length budgets per platform, tone calibration, derivation chain (positioning → variants), social-proof placement, photo guidance, refresh cadence.
- OUT of scope: positioning statement / Topic DNA (`topic-dna`), portfolio site IA (`portfolio`), full LinkedIn profile structure (`linkedin` Recipe), GitHub README (`github` Recipe), CFP authoring (`conference` Recipe), microcopy / error strings (delegate to `prose`).

## Core Concepts

### One Canonical Source

All bios derive from one **Master Positioning Statement** (the output of `topic-dna`). Without a single source, bios drift over months and visitors meet a different person on each platform.

```
Master Positioning Statement (one sentence)
   ↓ derive
GitHub one-line  ←  Twitter 160  ←  LinkedIn About 275  ←  Conference 50  ←  Long 200
```

Update the master, propagate to variants. Never hand-edit a single platform without updating master.

### The Bio Family

| Variant | Length | Where | Purpose |
|---------|--------|-------|---------|
| Master positioning | 1 sentence (15–25 words) | Internal canonical | Source of truth |
| GitHub one-line | 60–160 chars | github.com profile bio field | Drive-by visitor signal |
| X / Twitter bio | ≤160 chars | x.com/username | Plus links + location |
| Bluesky bio | ≤256 chars | bsky.app/profile | More room for nuance |
| LinkedIn headline | ≤220 chars | linkedin headline | Search-discoverable role + DNA |
| LinkedIn About | ≤275 chars (mobile fold) + 2,600 max | linkedin About section | Mobile-first first paragraph |
| Conference bio | 50 words | speaker page / program | Talk credibility + warmth |
| Long bio | 200 words | personal site /about, podcast guest forms | Full narrative |
| Press bio | 100 words | journalists / interviews | Distillation for quoting |

### Length Budgets and Why

| Platform | Reason |
|----------|--------|
| GitHub 60–160 chars | UI truncates beyond; readers skim |
| X 160 chars | Hard limit |
| Bluesky 256 chars | Hard limit; more room than X |
| LinkedIn About 275 chars (mobile fold) | First fold on mobile must contain the hook |
| Conference 50 words | Standard speaker-listing length |
| Long bio 200 words | Podcast / press / about-page sweet spot |

Truncated bios with the payoff cut off are the most common bio failure.

### Derivation Chain

Start from master, expand or contract:

```
[15-25 word master]
   ↓ tighten further; drop verbs of being
[60-160 char GitHub one-line]
   ↓ add 1 specific action / interest + emoji optional
[160 char X bio]
   ↓ add geography / role title
[220 char LinkedIn headline]
   ↓ expand: 1 sentence what + 1 sentence why + 1 sentence call
[275 char LinkedIn About first fold]
   ↓ continue: 2 paragraphs of context
[2,600 char LinkedIn About full]
   ↓ shape narratively for speaking voice
[50 word conference]
   ↓ extend with 1-2 anchors (book, talk, project) and humanizing detail
[200 word long bio]
```

### Tone Calibration by Platform

| Platform | Voice |
|----------|-------|
| GitHub | Engineer-peer; technical jargon OK; hobby parens OK |
| X | Sharper; sentence-fragment OK; humor welcomed |
| Bluesky | Warmer than X; technical-craft community |
| LinkedIn | Outcome-and-expertise framed; warmer than corporate-speak; first-person |
| Conference | Third-person ("Sarah Chen is...") + 1 humanizing detail |
| Long bio | Third-person on /about; first-person in pod-cast guest forms |
| Press | Third-person; one credentialing line + one currently-doing line |

The same person should sound consistent in **what they're known for**, but appropriate for the platform's social register.

### Person Voice (1st vs 3rd)

| Use 1st Person | Use 3rd Person |
|----------------|----------------|
| GitHub bio | Conference speaker bio |
| X / Bluesky bio | Press / journalist bios |
| LinkedIn About | Podcast guest descriptions |
| Personal-site /about (modern convention) | Award nominations |
| Long bio for podcast guesting | Wikipedia-style references |

3rd person on /about is older convention — modern engineer sites use 1st person more. Pick one and stay consistent.

### Social Proof Placement

| Tier | Where to put it |
|------|-----------------|
| Award / book / specific recognition | Master + long bio + LinkedIn About |
| Talks / OSS maintainership | Long bio + conference bio |
| Employer (if notable + current) | LinkedIn headline + long bio |
| Newsletter / podcast subscriber count | X / Bluesky bio + long bio |
| Specific outcome metric | Long bio only |

Don't stuff every bio with all proof — looks insecure. Strongest proof front-loaded.

### Photo Pairing

Bios live alongside photos. Coherence rules:

- Same photo across platforms (or 2 max — formal + casual).
- Updated within last 2 years.
- Eye contact.
- Clean background.
- Smiling or focused (not both).
- Square crop for avatars; landscape for hero.
- Consistent color treatment (same tonal grade across platforms).
- Accessibility: alt text describes person + context, not "headshot".

### Refresh Cadence

| Trigger | Update bios |
|---------|-------------|
| Topic DNA evolved | All variants |
| Major recognition (book, award, talk) | Long + LinkedIn + conference |
| Job change | LinkedIn + long + master |
| Photo refresh | All photos |
| Annual review | Re-read all variants for staleness |

Quarterly drive-by reviews catch stale role / recent-talk references.

### Common Failure Modes

| Failure | Fix |
|---------|-----|
| Bio doesn't say what you do | Lead with verb of doing, not state of being |
| Bio lists 5 unrelated interests | Pick the on-DNA ones |
| GitHub bio = corporate title | Replace with Topic DNA |
| LinkedIn About 1st fold buries DNA | Restructure: hook first |
| Conference bio is 200 words | Cut to 50 |
| Long bio has 5 employer logos | Cut to relevant subset |
| Different person across platforms | Audit; align to master |
| "Passionate about" / "rockstar" / "ninja" | Cut all clichés |
| Uses irony in conference bio that doesn't translate | Tone-calibrate per platform |
| Same emoji on every platform | Pick 0–1 per platform |
| No CTA or link in space-permitting bios | Add the most-relevant link |

### Standard Anti-Phrases

Cut on sight:

| Phrase | Why |
|--------|-----|
| "Passionate about ___" | Vague; unverifiable |
| "Rockstar / ninja / wizard / guru" | 2010s cliché |
| "Helping companies achieve ___" | Consultant-speak; vague |
| "Lifelong learner" | Generic |
| "Award-winning" without naming the award | Empty signal |
| "Solving complex problems" | All engineers do this |
| "Synergize / leverage / utilize" | Corporate filler |
| "Passionate" of any kind | Always cut |
| "Coffee enthusiast" | Generic personality stand-in |
| "He/she/they live in ___ with their dog" | Only if it actually informs your work |

### When Personal Detail Helps

A single specific personal detail at the end of a long bio humanizes:

- "She bakes sourdough on weekends."
- "He's slowly learning bouldering and losing badly."
- "When not coding, she's volunteering at a local cat shelter."

Rules:

- 1 detail max in long bio; 0 in short bios.
- Must be specific (not "loves food").
- Must be actually true.
- Should not actively contradict your professional brand.

## Workflow

1. **Get master positioning** from `topic-dna` output.
2. **Derive GitHub one-line** (60–160 chars).
3. **Derive X bio** (160 chars + location + 1 link).
4. **Derive Bluesky bio** (256 chars; warmer).
5. **Derive LinkedIn headline** (≤220 chars; role + DNA).
6. **Derive LinkedIn About first fold** (≤275 chars: hook + DNA + call).
7. **Expand LinkedIn About** to 600–1,500 chars total with narrative.
8. **Derive conference bio** (50 words, 3rd person + 1 humanizing detail).
9. **Derive long bio** (200 words, 1st-or-3rd-person; with social proof).
10. **Derive press bio** (100 words; for journalist quoting).
11. **Audit anti-phrases** — strip clichés.
12. **Verify photo coherence** across platforms.
13. **Set refresh date** (quarterly drive-by).
14. **Document master + variants** in one canonical artifact.

## Output Template

```yaml
multi_platform_bio:
  master_positioning: "I help fintech teams keep Postgres fast and audit-clean at high scale."
  variants:
    github:
      length_chars: 92
      text: "Postgres performance for fintech. Maintainer of pg-bloat-tool. Tokyo. she/her."
    x:
      length_chars: 158
      text: "Postgres perf for fintech. Maintainer of pg-bloat-tool. Conference speaker (PGCon, RubyKaigi). Tokyo. /sarahchen.dev"
      pinned_link: "sarahchen.dev"
    bluesky:
      length_chars: 240
      text: "Postgres performance specialist for fintech systems. Maintainer of pg-bloat-tool. Speaker at PGCon and RubyKaigi. Writing about query plans, replication, compliance, and what it takes to keep a 12 TB cluster honest. Tokyo."
    linkedin_headline:
      length_chars: 188
      text: "Postgres Performance Engineer for Fintech | Maintainer of pg-bloat-tool | PGCon Speaker | I keep multi-TB OLTP clusters fast and audit-ready"
    linkedin_about_fold:
      length_chars: 268
      text: "I help fintech teams keep Postgres fast and audit-clean at high scale. Currently consulting on a 12 TB OLTP migration. I write monthly at sarahchen.dev about query plans, bloat, and compliance. Reach out: hi@sarahchen.dev — I reply within 48h."
    linkedin_about_full:
      length_chars: 1100
      text: "<full text>"
    conference:
      word_count: 50
      voice: third_person
      text: "Sarah Chen is a Postgres performance engineer focused on fintech systems. She maintains the pg-bloat-tool open-source project and has spoken at PGCon, RubyKaigi, and Postgres London. Sarah lives in Tokyo and is slowly losing to her bouldering wall."
    long:
      word_count: 198
      voice: first_person
      text: "<full text>"
    press:
      word_count: 96
      voice: third_person
      text: "<full text>"
  social_proof_distribution:
    awards: [long, linkedin_about_full]
    talks: [long, conference]
    employer: [linkedin_headline, long]
    newsletter_size: not_yet
  photo:
    primary: avatar_v3.jpg
    used_on: [github, x, bluesky, linkedin]
    age_months: 8
    alt_text: "Sarah, mid-30s, smiling, navy sweater, neutral background"
  anti_phrase_audit: PASS
  refresh:
    last_updated: 2026-04-25
    next_review: 2026-07-25
  handoff:
    portfolio: about_page_long_bio
    github: profile_readme
    linkedin: profile_full_optimization
    conference: cfp_authoring_prep
```

## Anti-Patterns

- Different person across platforms — visitors lose trust.
- Hand-editing one platform without updating master — drift.
- Master positioning that's longer than 25 words — collapses every variant.
- "Passionate about" / "rockstar" / "ninja" — cut.
- Award claim without naming the award — empty.
- LinkedIn headline that's just job title without DNA — wastes search-rank.
- LinkedIn About fold that buries the hook past 275 chars on mobile.
- Conference bio over 50 words — gets cut by event organizer.
- Long bio with 4+ humanizing details — looks like over-compensation.
- Same emoji on every platform — homogeneous; doesn't tune.
- Photo more than 2 years old or different on every platform.
- No link / CTA in space-permitting bios.
- All third-person everywhere — feels distant.
- All first-person everywhere — bad for conference / press.
- Bio that mentions an employer no longer current.
- Bios with no refresh in 18+ months.
- Bio that contradicts your portfolio's hire-readiness signal (e.g., bio says "open to consulting", site says "not available").

## Deliverable Contract

A multi-platform bio package is complete when:

- Master positioning is one sentence ≤ 25 words.
- All bio variants derive from master.
- Length budgets respected per platform.
- LinkedIn About first fold ≤ 275 chars.
- Conference bio = 50 words.
- Long bio = 200 words.
- Tone calibrated per platform.
- Voice (1st / 3rd person) consistent within a platform.
- Photo coherent across platforms.
- Anti-phrase audit passes.
- Social proof distributed appropriately.
- Refresh cadence set (quarterly drive-by).

## References

- Patrick McKenzie, *Salary Negotiation* — bio framing for hire-readiness.
- David Heinemeier Hansson — example of consistent multi-platform voice.
- Linus Torvalds — example of curt, on-brand bio.
- Sara Soueidan — example of strong long bio + conference bio coherence.
- LinkedIn 360Brew Topic DNA — About-section length and 80% pillar guidance.
- Jason Fried, *It Doesn't Have to Be Crazy at Work* — calm-brand voice example.
- Maggie Appleton, *Long-form bio reference* on personal site.
- Andy Crestodina, *Orbit Media* — bio length / engagement research.
- Carmine Gallo, *Talk Like TED* — speaker-bio conference conventions.
- AP Stylebook — third-person bio standards.
- Reuters Handbook of Journalism — bio attribution norms for press.
- IndieWeb wiki — h-card bio microformat.
