# Technology Adoption Anti-Patterns

> Failure patterns in technology selection, Hype Cycle traps, evaluation frameworks, and avoiding Resume Driven Development

## 1. The 7 Major Technology Adoption Anti-Patterns

| # | Anti-Pattern | Problem | Symptoms | Countermeasure |
|---|-------------|------|------|------|
| **TA-01** | **Resume Driven Development** | Choosing a technology for the engineer's career goals | "Let's rewrite it in Rust," "let's add Kubernetes" (even when unneeded) | Base decisions on business requirements, team capability, and project scale |
| **TA-02** | **Hype Driven Adoption** | Adopting a technology purely because it's trendy or buzzworthy | The justification is "everyone's using it" or "it's popular on Hacker News" | Check its position on the Gartner Hype Cycle; wait until past the Trough of Disillusionment |
| **TA-03** | **FAANG Cargo Cult** | Copying a big-company case study while ignoring your own context | Adopting Google-scale technology for a 10-person team, excessive complexity | Choose technology that fits your own scale, constraints, and team capability |
| **TA-04** | **Shiny Object Syndrome** | Always jumping to the newest technology, abandoning what already works | Changing frameworks every six months, projects that never ship | Don't change "good enough" technology; quantify the cost of change |
| **TA-05** | **Premature Optimization** | Investing preemptively in technology for future problems | Going microservices at 100 users, unnecessary scalability work | Follow YAGNI, focus on the present problem, deal with the future later |
| **TA-06** | **Innovator's Dilemma** | Clinging to existing technology and missing disruptive change | "jQuery is good enough" for 5 years straight, team skills stagnate | Build a regular technology radar, reserve 20% exploration time |
| **TA-07** | **AI Hype Trap** | Over-trusting AI/LLMs as a cure-all and applying them inappropriately | Insufficient accuracy in text-to-SQL, unverified quality of AI-generated code | Understand AI's limits, require human review, limit the scope of application |

---

## 2. Technology Evaluation Framework

```
Tech Maturity Matrix (2×2 evaluation):

  Technology maturity (X axis):
    Research → Proof of Concept → Early Adoption → Full Adoption

  Business applicability (Y axis):
    Low → Medium → High

  Decision logic:
    High maturity × High applicability → Adopt aggressively
    High maturity × Low applicability → Watch
    Low maturity × High applicability → Trial
    Low maturity × Low applicability → Avoid

Gartner Hype Cycle's 5 stages:
  1. Innovation Trigger
  2. Peak of Inflated Expectations
  3. Trough of Disillusionment → most dropouts happen here
  4. Slope of Enlightenment
  5. Plateau of Productivity → production adoption belongs here

  ⚠️ Note: only about 20% of technologies actually make it through the Hype Cycle
  → most die out at Stage 3

Adoption Curve and the Chasm:
  Innovators (2.5%) → Early Adopters (13.5%)
    → [CHASM] →
  Early Majority (34%) → Late Majority (34%) → Laggards (16%)
  → Technology that doesn't cross the chasm is risky for the enterprise
```

---

## 3. Criteria for Telling Substance from Hype

```
5 indicators for judging a technology's "substance":

  1. User readiness:
     → Is the team's learning cost within an acceptable range?
     → Do case studies from adopting companies exist?

  2. Business model sustainability:
     → What funds the OSS project? What's the risk of single-company dependency?
     → Any precedent of license changes? (Redis, Elasticsearch, etc.)

  3. Infrastructure maturity:
     → Is the toolchain (CI/CD, monitoring, debugging) in place?
     → Are there enough hosting/deployment options?

  4. Regulatory/ethical feasibility:
     → Can compliance requirements be met?
     → Are there data-privacy concerns?

  5. Ecosystem health:
     → Number of Stack Overflow questions and answer rate
     → Trend in npm weekly downloads
     → GitHub stars growth rate (a spike followed by a crash is a warning sign)
     → Contributor count and commit frequency

  Lessons from failed technologies:
    → Google Glass: privacy concerns + cost
    → Segway: mismatch with user behavior
    → Deno (early on): insufficient ecosystem
    → text-to-SQL: accuracy falling short of expectations
```

---

## 4. How to Use the Thoughtworks Technology Radar

```
Technology Radar's 4 rings:

  Adopt:
    → Widely proven across the industry, recommended for production use
    → `radar`: actively consider adoption in existing projects

  Trial:
    → Use experimentally on projects where risk can be managed
    → `radar`: a suitable target for building a PoC

  Assess:
    → Worth exploring how it would impact you
    → `radar`: an investigation target during the ASSESS phase

  Hold:
    → Adoption in new projects is not recommended
    → `radar`: consider replacing existing usage

  How to use it:
    → Review the Technology Radar every six months
    → Cross-check against the project's tech stack
    → Add investigation of alternatives to ASSESS for anything that moves into Hold
```

---

## 5. Integration with `radar`

```
Usage within `radar`:
  1. Screen for TA-01 through TA-07 during the ASSESS phase
  2. Cross-check regularly against the Technology Radar
  3. Apply the Tech Maturity Matrix evaluation during the PREPARE phase
  4. Present the rationale for the adoption decision during the COMPLETE phase

Quality gates:
  - "Everyone's using it" as the justification → Hype Cycle position check required (prevents TA-02)
  - Copying a FAANG case study → verify fit to your own scale (prevents TA-03)
  - Frequent framework changes → change cost must be quantified (prevents TA-04)
  - Unneeded upfront investment → YAGNI check (prevents TA-05)
  - No technology change in 5 years → check the technology radar (prevents TA-06)
  - "AI can do anything" thinking → limit scope of application + require review (prevents TA-07)
```

**Source:** [Product Leadership: Emerging Technologies - Adopt or Avoid](https://www.productleadership.com/blog/emerging-technologies-adopt-or-avoid/) · [Thoughtworks Technology Radar](https://www.thoughtworks.com/radar) · [Gartner Hype Cycle Methodology](https://www.gartner.com/en/research/methodologies/gartner-hype-cycle)
