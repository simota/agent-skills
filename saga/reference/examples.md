# Narrative Examples

**Purpose:** Concrete finished examples of the narratives Saga generates.
**Read when:** You want to check the quality bar and finished form of a narrative.

---

## Example 1: Use Case Story (Pixar Story Spine)

### Meta Info
- **Product:** Cloud invoice management SaaS
- **Persona:** Freelance designer Misaki Sato (32)
- **Framework:** Pixar Story Spine + JTBD
- **Target Audience:** Development team

### Story

**Misaki Sato's daily life**

Misaki Sato is a freelance web designer. She works five days a week at a coworking space in the city. Her skills are solid, and clients speak well of her.

At the end of every month, Misaki's expression clouds over. She fills out invoices for five clients one by one in an Excel template, converts them to PDF, and attaches them to emails. She spends thirty minutes every time double-checking whether the withholding tax calculation is correct and whether the bank details are right. "I went independent because I love design work — so why am I spending four hours a month on bookkeeping?"

**Turning point**

One Friday night, while doing month-end invoicing, Misaki realized she had missed a client's company name change. She corrected it and resent the invoice. Embarrassment and exhaustion hit her at once. "I can't keep doing this."

That weekend, a friend from the same coworking space mentioned, "I automated my invoicing, you know."

**Chain of change**

After registering client information in [Product Name], monthly invoices were generated automatically from transaction history. Withholding tax was calculated automatically too. The PDF design was polished and even included her own logo.

Thanks to that, the four hours at month-end became twenty minutes. On top of that, reminders for unpaid invoices started going out automatically, and missed collections dropped to zero.

**New daily life**

Now Misaki treats month-end not as "invoice day" but as "the day I plan next month's projects." Her self-image of "bad with numbers" changed to "leave the numbers to the tool, I focus on design."

### Job Story
> **When** I need to create invoices for multiple clients at month-end,
> **I want to** automatically generate invoices from transaction data,
> **so I can** reduce the time and psychological burden of bookkeeping and focus on my core work.

### Anti-Pattern Check
All items PASS (criteria in `reference/anti-patterns.md`). Reasons this example passes:
- AP-1 has a story arc / AP-2 Misaki is the protagonist / AP-3 depicts the month-end pain
- AP-4 clear Before→After / AP-5 concrete persona / AP-6 no assumptions
- AP-7 plain language / AP-8 depicts a failure (missed company name change) / AP-9 no promotional tone

---

## Example 2: Product Narrative (StoryBrand SB7)

### Meta Info
- **Product:** Task management tool for teams
- **Framework:** StoryBrand SB7
- **Target Audience:** Landing page / Marketing

### BrandScript

#### 1. Hero
A startup team lead wants everyone on the team to move a project forward in the same direction.

#### 2. Problem
- **External:** Tasks are scattered across Slack, email, and spreadsheets, and it's unclear what's current
- **Internal:** Anxiety that "maybe my management is bad." Frustration at not knowing who's doing what
- **Philosophical:** When a team works together, everyone should know what to do right now without hesitation — that should be a given
- **Villain:** "Scattered information" and "a culture of unspoken assumptions"

#### 3. Guide
- **Empathy:** "Once you cross ten people, you lose track of what's happening. You're not alone in that."
- **Authority:** Adopted by 1,200+ teams cumulatively. Average meeting time reduced by 32%

#### 4. Plan
1. **Invite your team** — Setup complete in 3 minutes
2. **Visualize the project** — Organize tasks with drag and drop
3. **Share progress in real time** — Zero more "what's the status?" questions

#### 5. Call to Action
- **Direct CTA:** Start for free
- **Transitional CTA:** Watch a 3-minute demo video

#### 6. Failure
If information stays scattered like this, important tasks will slip through, deadlines will be missed, and team frustration will build up. A day may come when a top performer says, "I want to work somewhere more organized."

#### 7. Success
A team where everyone understands their role and acts autonomously. No one asks "what should I do now?" anymore. The lead is freed from management overhead and can focus on strategy. Team members feel glad they work on this team.

---

### One-liner
> To the team drowning in scattered tasks with no idea what's current: with [Product Name], become a team that runs from the same map.

---

## Example 3: Pitch Story (Pixar + Numbers)

### Meta Info
- **Product:** AI-powered customer support tool
- **Framework:** Pixar Story Spine + Numbers
- **Target Audience:** Investors

### Story

Japan's e-commerce market is worth 23 trillion yen. Of that, 70% of merchants cite "balancing customer support quality and efficiency" as their biggest challenge.

Every day, support teams answer the same questions dozens of times, and complex inquiries take an average of 3.2 exchanges to resolve. Agent turnover runs at 40% annually.

We realized: the problem wasn't "not enough people" — it was "people not being free to focus on the things only people can do."

[Product Name] has AI instantly handle routine responses and routes only "cases that require judgment" to human agents.

At companies that adopted it, first-contact resolution rose from 67% to 89%. Cases handled per agent increased 2.3x. And turnover improved from 40% to 18%.

What we're aiming for is a world where the act of "having to ask a question" disappears altogether — where AI resolves issues before the customer is even troubled by them.

---

## Example 4: Scenario Narrative (JTBD + Context Depiction)

### Meta Info
- **Product:** Household budgeting app
- **Persona:** Dual-income couple, the Yamada family (husband 34, wife 32, one child)
- **Framework:** JTBD + Scene Depiction
- **Target Audience:** Development team

### Scene Setup
**When:** Sunday night, 9 PM, after putting the child to bed
**Where:** Living room sofa
**What's happening:** The couple is discussing next month's expenses

### Narrative

Sunday, 9 PM. The Yamadas sit side by side on the living room sofa. They've just finally gotten their one-year-old son to sleep. On the table sit both their phones and a list of next month's big expenses — daycare fees, car insurance renewal, a wedding gift for the wife's friend.

"How much did we spend this month?" the husband asks. The wife opens her banking app, checks the credit card statement, and compares it against a rough food-spending estimate she'd jotted in a separate notes app. "Maybe around 280,000 yen... but I'm not sure exactly."

They're both tired. This "maybe" is the source of their stress. Every month they have this same conversation, one of them says "we really need to manage this better," and yet nothing ever changes.

They open [App Name]. Since their accounts and cards are already linked, this month's spending is automatically categorized. Food: 187,000 yen. Fixed costs: 82,000 yen. Hobbies and social spending: 41,000 yen. A bar chart shows the comparison with last month.

"Oh, food spending is up 20,000 yen from last month. Probably because we ate out a lot." The wife taps the screen, and a list of dining-out expenses appears. "Five weekend lunches at 18,000 yen total... let's watch that a bit."

Together they adjust next month's budget. With daycare fees and insurance pushing fixed costs up by 30,000 yen, they decide to trim hobbies and social spending slightly. It's done in five minutes.

"We used to spend thirty minutes and still not really know," the husband laughs. The wife sets her phone down on the table, finally looking relaxed.

### Job Story
> **When** the couple discusses next month's household budget at month-end,
> **I want to** see this month's spending accurately broken down by category,
> **so I can** have a short, constructive conversation grounded in facts instead of "maybe."

### Tension Points
| # | Point | Content | Resolution |
|---|---------|------|------|
| 1 | Vague grasp of spending | "Maybe around 280,000 yen" | Precise automatic categorization |
| 2 | Time drain | 30 minutes of unproductive checking each month | Done in 5 minutes |
| 3 | Emotional friction | Repeated "we should manage this better" | Objective, data-driven conversation |
