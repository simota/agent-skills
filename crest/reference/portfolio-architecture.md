# Portfolio Architecture

## Purpose

A personal site is the only channel an engineer fully controls. SNS algorithms, employer branding, and platform changes can erase visibility overnight; a personal portfolio doesn't. This reference defines the information architecture, hire-readiness signals, and content cadence for a portfolio that compounds over years.

## Scope Boundary

- IN scope: site IA, page-level content blueprint, hire-readiness checklist (CTA, contact, response time, availability), case-study structure, "now" page, writing/talks/projects organization, technology stack guidance.
- OUT of scope: visual design (delegate to `vision`), full design-system tokens (`muse`), animation (`flow`), per-platform bios (`bio`), Topic DNA / positioning (`topic-dna`), conversion funnel for paid offers (`funnel`), SEO meta (`growth`).

## Core Concepts

### What a Portfolio Is For

| Audience | Goal |
|----------|------|
| Recruiter / hiring manager | Quickly verify competence, fit, contact path |
| Peer engineer | Find your work, technique, point of view |
| Client / collaborator | Decide whether to hire / partner |
| Journalist / podcaster | Find a quotable expert |
| Future-you | Track what you've shipped, said, learned |

A portfolio that serves all five reads cleanly to each. Designed for one audience, it fails the others.

### Information Architecture

| Page | Purpose |
|------|---------|
| `/` (home) | Hero + Topic DNA + 3–5 latest signals (project, post, talk) + CTA |
| `/about` | Long-form bio + photo + values + timeline |
| `/projects` | Curated case studies with outcomes |
| `/writing` (or `/blog`) | Articles, ordered by date, tagged by pillar |
| `/talks` | Conference talks with video / slides / transcripts |
| `/now` | What you're working on right now (Derek Sivers' /now convention) |
| `/uses` | Tools / setup (engineer-community convention) |
| `/contact` | Email + booking calendar + availability signal |
| `/feed.xml` | RSS feed (essential — many engineers still subscribe) |

Optional pages, only when there's content:

- `/podcasts` — guest appearances
- `/teaching` — courses, workshops
- `/oss` — open-source contributions
- `/talks/upcoming` — upcoming events

### The Hero Block

The first 600 px of the home page. Must answer in under 3 seconds:

1. **Who are you?** (Name + Topic DNA in one sentence)
2. **What can I do here?** (Read / hire / contact)
3. **Why should I trust you?** (1–2 social proof signals)

Anti-patterns:

- "Hi I'm [name]" with no Topic DNA.
- Multiple equal-weight CTAs ("Read my blog | See my projects | Hire me | Subscribe | Twitter").
- Stock illustrations or generic abstract art.
- Hero video / autoplay — kills page weight without payoff.

### Hire-Readiness Checklist

Even if you're employed, your portfolio should signal hire-readiness state explicitly:

| Element | Signal |
|---------|--------|
| Availability indicator | "Open to consulting Q3 2026" / "Not available for contract" / "Hiring me as advisor: yes" |
| Response time | "I reply within 48h on weekdays" |
| Contact path | One primary (email) + one secondary (calendar booking) |
| Engagement model | "Consulting / advisory / part-time / FTE" — pick one or list explicitly |
| Rate band (optional) | "Day-rate: $X / project from $Y" — filters tire-kickers |
| Geography | "Remote, EU/UK overlap preferred" |
| References | 2–3 quotable testimonials with name + company |
| Recent work | Last 3 case studies / projects |

Missing any of these on a hire-seeking portfolio cuts response rates ~50%.

### Case Study Structure

A portfolio's defining content. Each case study:

| Section | Length | Purpose |
|---------|--------|---------|
| Title | 1 line | Name the project + outcome |
| Context | 2–3 sentences | Who / when / why |
| Role | 1 line | What you specifically did vs the team |
| Constraints | 2–3 bullets | Real limits (budget, time, tech) |
| Approach | 2–4 paragraphs | How you tackled it; trade-offs |
| Outcome | 2–3 bullets with numbers | "Reduced p95 by 60%" / "Shipped 6 weeks early" |
| Learnings | 1–2 paragraphs | What you'd do differently |
| Visual | 1–3 images / GIFs | Concrete artifacts |
| Stack | One-liner | Technologies used |
| Links | Optional | Live, repo, paper |

5–10 case studies > 50 thin project listings.

### The "Now" Page

Pioneered by Derek Sivers (nownownow.com). One paragraph + bullet list of:

- What you're working on
- What you're learning
- What you're not doing
- Date last updated

Updates every 1–3 months. Most-clicked page after `/about` for engineer portfolios.

### The "Uses" Page

Convention site: uses.tech. Lists:

- Hardware (laptop, monitor, keyboard, mic)
- Editor / IDE / terminal
- Daily software
- Browser extensions

Generates traffic from peer engineers and signals taste.

### Writing / Blog Architecture

| Decision | Recommendation |
|----------|---------------|
| URL structure | `/writing/<slug>` flat or `/writing/<year>/<slug>` |
| Date in URL | Optional; helps signal currency |
| Categories vs tags | Tags by pillar (3–5) — derived from Topic DNA |
| RSS / Atom feed | Mandatory |
| Newsletter signup | If you publish, yes; otherwise no |
| Comments | Off (Webmentions or external links acceptable) |
| Reading time | Show |
| Estimated date | Show |
| Last updated | Show if you maintain evergreen content |

Fewer, deeper posts > frequent thin posts.

### Talks Page

For each talk:

| Element | Notes |
|---------|-------|
| Title | Same on slide / title-page / event listing |
| Event + date | Conference name, location, year |
| Length | Lightning / regular / keynote |
| Video link | YouTube / conference site |
| Slides link | Speakerdeck / Slideshare / hosted PDF |
| Transcript | If available — accessibility + SEO |
| Description | 2–3 sentence summary |
| Tags | Pillar derived from Topic DNA |

Talks are the highest-credibility evidence a portfolio can carry.

### Tech Stack Choices

| Choice | When |
|--------|------|
| Astro | Content-heavy + low maintenance + fast |
| Eleventy | Lighter Astro alternative; great for writers |
| Next.js | If you genuinely want SPA features (rare for personal sites) |
| Hugo | Pure-content site, very fast builds |
| Plain HTML + CSS | Long-term durable; respect for the medium |

Avoid: heavy SPA frameworks for content sites; CMS-coupled (drupal/WP) without strong reason.

Performance budget: LCP ≤ 1.5s, INP ≤ 100ms, total transfer ≤ 200 KB on mobile 3G. A slow personal site signals indifference.

### IndieWeb Conventions

For credibility with the engineer / web-craft community:

- `rel="me"` on social links.
- `h-card` microformat on /about.
- `h-entry` microformat on posts.
- Webmentions endpoint.
- IndieAuth-friendly.

Optional but signals craft.

### Content Cadence

| Frequency | What |
|-----------|------|
| Daily | Nothing — it's not a journal |
| Weekly | Optional — only sustainable if writing is the job |
| Monthly | A realistic article cadence |
| Quarterly | Case study or major project |
| Annually | Year-in-review post; /now refresh |

Burnout from over-publishing kills more portfolios than under-publishing.

### Domain and Branding

- Use a personal domain (yourname.com or yourname.dev), not username.medium.com.
- Domain is a long-term asset; transfer it across employers.
- Email at the domain (you@yourname.com) — signals seriousness.
- Subdomains for experiments (lab.yourname.com, talks.yourname.com).

### Accessibility

A portfolio that fails a11y is professionally embarrassing for an engineer:

- Color contrast WCAG AA (4.5:1 body, 3:1 large).
- Keyboard navigation through all pages.
- Skip-to-content link.
- Focus indicators visible.
- Alt text on all images.
- Captions / transcripts on videos.
- Document language (`lang="ja"` / `"en"`).

### Privacy

Don't ship analytics that track visitors aggressively:

- Plausible / Simple Analytics / Fathom > Google Analytics.
- No third-party fonts — host them or use system stack.
- No social-share buttons that load tracking scripts.
- Cookie banner only if actually using cookies.
- DNT honored.

## Workflow

1. **Audit current state** — what pages exist, what content lives where.
2. **Set hero block** — Topic DNA + CTA + social proof.
3. **Decide IA pages** — / + /about + /projects + /writing + /talks + /now + /uses + /contact.
4. **Build hire-readiness block** — availability, contact, response time, references.
5. **Author 3–5 case studies** with outcome numbers.
6. **Set up writing IA** — feed, tags, reading time.
7. **Populate talks page** with video + slides + transcripts.
8. **Write `/now` and `/uses`**.
9. **Pick tech stack** — content-first, fast, durable.
10. **Add IndieWeb microformats** if community-relevant.
11. **Set content cadence** — monthly articles, quarterly case studies.
12. **Run a11y + perf audit** — LCP / INP / CLS targets.
13. **Verify privacy** — Plausible / no aggressive tracking.
14. **Set quarterly /now-update reminder**.

## Output Template

```yaml
portfolio_architecture:
  domain: example.dev
  topic_dna_handoff: yes  # consumed from topic-dna output
  pages:
    - path: /
      hero:
        name_and_dna: "Engineer for Postgres-heavy fintech systems"
        primary_cta: "Read latest case study"
        secondary_cta: "See availability"
        social_proof:
          - "Speaker at PGCon 2025"
          - "Maintainer of pg-bloat-tool"
    - path: /about
      contains: [bio_long, photo, values, timeline]
    - path: /projects
      case_studies:
        - title: "Cut p95 query latency 60% on a 12 TB OLTP cluster"
          outcome_numbers: ["p95: 320ms → 128ms", "AWS bill: -$8K/mo"]
        - ...
      target_count: 5_to_10
    - path: /writing
      pillars_from_topic_dna: yes
      feed: /feed.xml
      reading_time: yes
    - path: /talks
      with_video: yes
      with_slides: yes
      with_transcript: yes
    - path: /now
      update_cadence_months: 3
    - path: /uses
      sections: [hardware, editor, software, browser]
    - path: /contact
      hire_readiness:
        availability: "Open to advisory work Q3 2026"
        response_time: "48h weekdays"
        engagement_models: [advisory, consulting]
        rate_band: visible
        geography: "Remote, JP/EU overlap"
        references: 3
  tech_stack: astro
  performance_targets:
    lcp_ms: 1500
    inp_ms: 100
    transfer_kb_mobile_3g: 200
  a11y:
    wcag_aa: yes
    keyboard_navigable: yes
    skip_to_content: yes
    alt_text_audit: yes
  privacy:
    analytics: plausible
    third_party_fonts: no
    tracking_scripts: none
  indieweb:
    rel_me_on_socials: yes
    h_card_about: yes
    h_entry_posts: yes
    webmentions: yes
  cadence:
    article_per_month: 1
    case_study_per_quarter: 1
    now_page_update_per_quarter: 1
  handoff:
    vision: visual_design_brief
    muse: token_audit
    bio: about_page_long_bio
    growth: seo_meta + structured_data
```

## Anti-Patterns

- Hero with no Topic DNA — visitors don't know what you're for.
- 5+ equal-weight CTAs — choice paralysis.
- "Hi I'm [name]" without context — friendly, useless.
- Heavy SPA for static content — slow, ungoogleable, brittle.
- Carousel of 50 thin "projects" without case studies — quantity, no signal.
- Resume timeline as the only project evidence — no outcomes.
- /blog full of "Hello world" / "trying something new" posts — noise floor.
- No /contact or contact buried 3 clicks deep — kills opportunities.
- Availability + response time absent — recruiters move on.
- No case study with numbers — no proof of competence.
- No /now page — visitors can't tell if you're active.
- Stock illustrations on hero — generic, forgettable.
- Autoplay video on hero — page weight + UX violation.
- Custom-loaded fonts blocking render — perf failure.
- Aggressive analytics + cookie banner — distrust signal.
- No RSS feed — engineer audience explicitly notices.
- A11y failures (low contrast, no focus, no alt) — professional credibility crater.
- Unmaintained — last post 18+ months ago with no /now update.
- Newsletter signup popup interstitial — anti-pattern; convert from value, not interruption.
- Mobile-broken layout — most traffic is mobile.

## Deliverable Contract

A portfolio architecture spec is complete when:

- Pages defined with purpose per page.
- Hero block has Topic DNA + CTA + social proof.
- Hire-readiness signals all present.
- Case-study target count set with structure.
- Writing IA includes feed + tags + reading time.
- Talks page has video + slides + transcript columns.
- /now and /uses defined.
- Tech stack chosen for content-first + fast + durable.
- Performance + a11y + privacy targets stated.
- Cadence plan documented (monthly / quarterly).
- Handoff briefs prepared for `vision`, `muse`, `bio`, `growth`.

## References

- Derek Sivers — *nownownow.com* and the /now-page convention.
- uses.tech — engineer /uses convention.
- IndieWeb wiki — microformats, h-card, h-entry, Webmentions.
- Brad Frost, *Atomic Design* (2016) — IA components.
- Sara Soueidan, sarasoueidan.com — case-study masterclass.
- Sara Wachter-Boettcher, *Design for Real Life* — accessibility-first content design.
- Maggie Appleton, maggieappleton.com — durable content site reference.
- Astro / Eleventy / Hugo official documentation.
- Plausible / Fathom / Simple Analytics — privacy-respecting analytics.
- WebAIM Million 2025 — accessibility baseline data.
- Patrick McKenzie, *Salary Negotiation* / *Don't Call Yourself a Programmer* — hire-readiness framing.
- Tania Rascia, taniarascia.com — content-first portfolio reference.
- Josh Comeau, joshwcomeau.com — interactive portfolio reference (note: heavier; learn the IA, not the JS).
- Robin Rendle, robinrendle.com — writing-first reference.
