# Channel Templates

**Purpose:** Platform-specific profile and content templates for engineer self-branding.
**Read when:** PROFILE or NARRATIVE mode — user needs optimized content for a specific channel.

---

## GitHub Profile README

### Structure Template

```markdown
# Hi, I'm [Name] 👋

[One-line positioning statement from Tech×Domain×Perspective]

## About Me
- 🔭 Currently working on: [Current focus project/area]
- 🌱 Currently learning: [Active learning area]
- 💬 Ask me about: [Your expertise topics — 3 max]
- 📝 I write at: [Blog/Qiita/Zenn URL]
- 📫 How to reach me: [Preferred contact]

## Tech Stack
[Badges or icons for primary technologies — limit to 8-10 core tools]

## Featured Work
| Project | Description | Tech |
|---------|-------------|------|
| [Repo 1] | [Impact-focused description] | [Stack] |
| [Repo 2] | [Impact-focused description] | [Stack] |

## Recent Articles
- [Title 1](URL) — [One-line summary]
- [Title 2](URL) — [One-line summary]

## Stats
[GitHub stats card — optional, only if metrics are meaningful]
```

### Best Practices
- Pin 4-6 repositories that demonstrate your niche expertise (GitHub supports up to 6 pinned items including external repos)
- Write README for each pinned repo with clear problem→solution→result framing
- Use contribution graph strategically (consistency > volume)
- Add documentation quality to repos (this signals professionalism)
- **Achievements & Badges:** GitHub automatically displays achievement badges (Arctic Code Vault, Galaxy Brain, Starstruck, etc.) based on program participation. Manage visibility in profile settings — you can hide individual achievements. [Source: GitHub Docs — Managing your profile README](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)
- **GitHub Sponsors:** Eligibility requires a public profile. Sponsorship visibility signals that real users value your OSS work — a stronger trust signal than star count alone. [Source: GitHub Docs — About your profile](https://docs.github.com/en/account-and-profile/concepts/personal-profile)

---

## LinkedIn

### Headline Formula

```
[Role/Title] | [Tech×Domain niche] | [Key achievement or perspective]
```

**Examples:**
- "Backend Engineer | FinTech × Rust | 低レイテンシ決済システムの設計・構築"
- "SRE | クラウドインフラ × 可観測性 | 99.99% SLA達成の仕組みづくり"

**Rules:**
- Max 220 characters
- Include primary tech stack keywords (recruiter search optimization)
- Quantify when possible

### About Section Template

```
[Hook — 1 sentence that captures attention]

[What you do — 2-3 sentences on your expertise and domain]

[Key achievements — 3-5 bullet points with quantified results]
• [Achievement 1 with metric]
• [Achievement 2 with metric]
• [Achievement 3 with metric]

[What drives you — 1-2 sentences on perspective/philosophy]

[Current focus — 1 sentence on what you're working on now]

[CTA — how to connect or collaborate]
```

### Featured Section
- Pin top 3-5 items: talks, articles, projects, media appearances
- Use custom thumbnails for visual impact
- Update quarterly

### Experience Section
- Lead each role with impact, not responsibilities
- Format: "[Action verb] + [what] + [quantified result]"
- Include tech stack as skills for each role

### Platform Notes (2024-2026 Changes)
- **Creator Mode** was removed in March 2024 — its features (Follow CTA, analytics, newsletters, standalone articles) are now available to all members by default. Do not instruct users to "enable Creator Mode."
- **Profile hashtags** ("Talks about" section with 5 hashtags) were deprecated in February 2024. LinkedIn now uses the "About" section and semantic analysis for topic classification — no hashtag fields to configure.
- **Newsletters** generate 206% more impressions than regular posts with 4.40% engagement rate. Recommend creating a newsletter for engineers who want consistent long-form distribution with zero external link penalty.
- Algorithm now uses Interest Graph (content you engage with) alongside Connection Graph. Posts aligned with verified professional expertise see 40% higher organic impressions than off-topic content. [Source: Buffer — LinkedIn Algorithm 2026](https://buffer.com/resources/linkedin-algorithm/)

---

## Technical Blog (Personal Domain)

### Article Frameworks

| Type | Structure | Best For |
|------|-----------|----------|
| **Deep Dive** | Problem→Investigation→Solution→Lessons | Technical authority |
| **Tutorial** | Goal→Prerequisites→Steps→Result | SEO + helpfulness |
| **Opinion** | Thesis→Evidence→Counterargument→Conclusion | Thought leadership |
| **Retrospective** | Context→What happened→Analysis→Takeaways | Experience credibility |
| **Comparison** | Criteria→Tool A vs B→Recommendation | Search traffic |

### Blog Post Template

```markdown
# [Headline — specific and benefit-oriented]

[Hook paragraph — why should the reader care?]

## Background / Problem
[Context that establishes your credibility on this topic]

## Approach / Solution
[Technical content — the core value of the article]

## Results / Lessons Learned
[Quantified outcomes or key takeaways]

## Conclusion
[Summary + call to action (follow, subscribe, discuss)]
```

### Platform Recommendations
- **Own domain first** — you own the SEO equity
- **Hashnode** — free custom domain support, developer-focused community; "Headless Hashnode" mode lets you use it as a CMS with your own frontend for maximum control with built-in audience
- **Hugo/Astro/Next.js** — static site for maximum control and performance

---

## Qiita

### Content Strategy
- **High-performing formats:** Beginner guides, cheat sheets, error resolution, new technology reviews, hands-on "I tried X" articles
- **Advent Calendar:** Participate in year-end events for exposure boost (December is peak annual traffic)
- **Tags:** 5 maximum. Combine specialty tags + popular tags

### Article Template

```markdown
# [Specific title — include search keywords]

## Introduction
[Target audience and what they will gain]

## Environment & Prerequisites
[Version info, prerequisite knowledge]

## Main Content
[Technically accurate content — with code examples]

## Summary
[Bulleted key takeaways]

## References
[Official documentation, RFCs, and other reliable sources]
```

### Pitfalls
- Opinion posts without technical evidence are harshly evaluated — always back up with code or official documentation
- Accuracy is paramount — mistakes are immediately called out in comments
- Organization articles also contribute to your employer's tech branding

---

## Zenn

### Content Strategy
- **Articles:** Deep technical explanations, implementation logs
- **Books:** Systematic series (can be monetized) — functions as a technical book with 10+ chapters
- **Scraps:** Casual learning logs, notes — low barrier to writing

### Book Planning Template

```markdown
# [Book Title]

## Overview
[What readers will learn, in 3 lines]

## Target Audience
[Level and prerequisite knowledge]

## Chapter Structure
1. [Introduction — why this topic]
2-8. [Main content — progressively deeper]
9. [Practice — comprehensive hands-on]
10. [Summary — next steps]

## Pricing
[Free / Paid (¥200-1,000) — decide based on depth and originality]
```

### Strengths
- Markdown management via GitHub integration
- Readership with high interest in modern technologies (TypeScript, Rust, Go)
- Monetization via Badge (tips) + paid Book sales

---

## note

### Content Strategy
- **Target:** Reaching non-engineer audiences (HR, executives, PMs)
- **Formats:** Career essays, management insights, behind-the-scenes of tech decisions, architecture decision rationale
- **Monetization:** Paid articles, magazines, membership

### Article Template

```markdown
# [Story-driven title]

[Introduction — scene-setting that resonates with readers]

## [Main topic — experience-based insights]

[Develop in storytelling format]

## Lessons Learned

[Organize as universally applicable takeaways]

## Closing

[Preview of next article or CTA for follows]
```

### Pitfalls
- Code blocks are not optimized for technical articles — deep technical content belongs on Qiita/Zenn
- Story quality and readability are highly valued

---

## X (Twitter)

### Profile Optimization
- **Display name:** Real name or handle + specialty keyword
- **Bio:** Positioning statement + 3 specialty tags + link
- **Pinned tweet:** Representative work, thread, or self-introduction

### Content Formats

| Format | Structure | Purpose |
|--------|-----------|---------|
| **Thread** | Hook → 5-10 tweets → CTA | Technical explainers, knowledge sharing |
| **Quote RT + Opinion** | Quote + your own take | Thought leadership |
| **Today I Learned** | Short discovery + code or screenshot | Daily posting |
| **Announcement** | Achievement report + link | Track record showcase |

### Algorithm Tips
- Replies = 27x weight of likes; conversations = 150x weight
- External links: as of early 2026, X actively boosts links to technical articles (dev.to, Substack, personal blogs) — no longer blanket-penalized. Non-Premium accounts posting links still see suppressed median engagement; Premium accounts get 4x algorithmic boost. Use a 3-5 tweet thread summarizing the article, then link in the thread for best combined reach. [Source: Sprout Social — How the Twitter Algorithm Works in 2026](https://sproutsocial.com/insights/twitter-algorithm/)
- 1-2 niche-relevant hashtags increase engagement ~21%; 3+ hashtags penalized ~40% — keep to minimum and avoid generic popular tags. Algorithm now uses semantic embeddings for topic classification, making hashtags less critical.
- First 30-60 minutes of velocity is critical → optimize posting time
- Allocate 70% of time to engagement, 30% to new posts

---

## YouTube

### Content Formats

| Format | Length | Purpose |
|--------|--------|---------|
| **"X in 100 Seconds"** | 1-2 min | Rapid concept explainer |
| **Code Report** | 5-8 min | Tech news + opinion |
| **Tutorial** | 8-15 min | Step-by-step walkthrough |
| **Shorts** | 15-60 sec | Clips repurposed from long-form |

### Optimization
- Split each long-form video into 3-5 Shorts
- Thumbnails: 3-5 words of text, high contrast, face recommended
- Titles: specific + curiosity ("How [X] works" > "About [X]")

---

## TikTok / Instagram Reels

### Content Formats
- Coding timelapse (Before/After)
- 60-second concept explainer (screen recording + narration)
- Day in the Life of an Engineer
- Tech news flash

### Tips
- First 3 seconds are everything — hook is mandatory
- Authenticity > high production (31% higher engagement)
- Instagram: DM sharing is the most important signal; Carousels are more likely to be saved

---

## Conference CFP

### Talk Proposal Template

```markdown
## Title
[Specific, curiosity-provoking title — 75% of acceptance decisions are based on the title]

## Abstract (200-300 words)
[Paragraph 1: Problem statement — an issue the audience relates to]
[Paragraph 2: Approach — your unique solution]
[Paragraph 3: Audience takeaways — 3 concrete takeaways]

## Target Audience
[Level and prerequisite knowledge]

## Outline
1. [Intro (5 min)]
2-4. [Main content (10 min each)]
5. [Summary + Q&A (5 min)]

## Speaker Bio
[Positioning statement + experience/track record specific to this talk]
```

### Strategy
- Start with small local events → build track record
- 1h talk = 40h preparation (rule of thumb)
- After speaking: publish slides + write blog post + share on social media
- KubeCon CFP policy: submit to no more than 3 sessions (fairness/review workload constraint). Session types: 30-min presentation (1-2 speakers), 30-min panel (3-5 speakers), 5-min lightning talk, 75-min tutorial (1-5 speakers).
- **KubeCon Japan 2026** (Yokohama, July 28-30, 2026) — opportunity for Japanese engineers to speak at a top-tier global cloud native event on home soil. [Source: CNCF — KubeCon Japan 2026](https://events.linuxfoundation.org/kubecon-cloudnativecon-japan/)

---

## Newsletter

### Platform Comparison

| Platform | Strengths | Best For |
|----------|-----------|----------|
| **Substack** | Easy setup, discovery network, 40-50% avg open rate | Early personal brand |
| **beehiiv** | Growth mechanics (referral, Boosts ad network), 35K+ newsletters powered, 2B+ emails/year | Growth phase |
| **Ghost** | Custom domain, full design control, membership/paywall, strong SEO defaults ($18/month) | Self-hosted professional |
| **Resend + React Email** | Full code-level customization | Tech-savvy creators wanting full control |

> Sources: [beehiiv blog — Substack vs Ghost](https://www.beehiiv.com/blog/substack-vs-ghost)

### Newsletter Structure

```
1. [Hook — this week's theme in one sentence]
2. [Main Content — one deep insight or practical finding]
3. [Quick Links — 3-5 curated links + one-line commentary]
4. [CTA — ask for replies or shares]
```
