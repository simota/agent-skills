# Probing Questions

**Purpose:** Question banks for the PROBE phase. Sage uses these to surface root cause, force ranking, and detect anti-patterns.
**Read when:** You are in PROBE phase or need to break through founder rationalization.

## Tier-1: Bottleneck Probes

These force the founder to name the single most important problem.

- "What's slowing you down most right now?"
- "If you could fix exactly one thing this week, what would it be?"
- "What are you avoiding?"
- "What's the most important thing you should be doing — and are you doing it?"
- "If only one of your current priorities mattered, which one?"
- "What would you tell another founder in your situation to focus on?"

If the founder gives a list, repeat: *"Of those, which one matters most?"* until reduced to one.

If the founder cannot reduce to one after 3 attempts, surface that the inability to choose is itself the bottleneck.

## Tier-2: Reality Probes

Force grounding in observable reality, not narrative.

- "How many users did you talk to this week? Specifically — names."
- "What did they actually say? Quotes, not paraphrases."
- "What's your weekly growth rate? Show the number."
- "What's your runway? In months. Calculate it."
- "When was the last time you used the product yourself?"
- "How long since you last shipped something to production?"
- "What's your activation rate? From sign-up to first valuable action."
- "What's your weekly revenue? Last 4 weeks, week by week."

If numbers can't be produced, that gap is a signal.

## Tier-3: Anti-Pattern Probes

Detection-oriented questions; pair with `founder-anti-patterns.md`.

**Signal carry-over rule (priority above all other Tier-3 picks):** if the founder voluntarily mentioned cofounder conflict (AP-07), runway < 12 months (P-03), or burnout during CHECK-IN, the single most severe of those signals must be probed first before product/metric anti-patterns. Pick exactly one — the Pareto rule still applies. Suggested openers: "You mentioned [signal] earlier — tell me what's actually happening there." Probe one signal deeply, then return to the bottleneck path; do not chase all three.

- "Why aren't you doing the most important thing?" (AP-04 distraction, AP-09 sales avoidance)
- "Tell me about your cofounder relationship right now." (AP-07)
- "Who specifically is the customer? Job title, company size, problem." (AP-08)
- "When was the last cofounder conversation about equity / direction / roles?" (AP-07)
- "Why are you optimizing X before traction?" (AP-02)
- "How many features did you ship this month vs how many user conversations?" (AP-01)
- "What would happen if you fired your worst customer / dropped your worst segment?" (AP-08)
- "If you couldn't raise, what would you do?" (AP-14, AP-16)
- "What did the last 5 churned users say?" (AP-08, P-12)

## Tier-4: Default-Alive Probes

When fundraising or runway comes up.

- "What's your monthly burn?"
- "What's your monthly revenue?"
- "How many months of runway?"
- "If you couldn't raise, when would you run out?"
- "At your current growth rate, would you be cash-flow positive before that?"
- "What's the smallest version of this business that's default-alive?"

If the founder can't answer in 2 minutes, calculating runway is the immediate action.

## Tier-5: Decision Probes

When the founder is paralyzed between options.

- "What does the data say?"
- "What would the highest-velocity version of this look like?"
- "What's the cheapest test that would resolve this in 2 weeks?"
- "What's the worst case if you pick wrong, and is it reversible?"
- "Which option does the customer pull you toward?"
- "If you had to commit by tomorrow morning, which would you pick?"
- **Two-way door check (P-54):** "Is this a two-way door or a one-way door? If two-way, what's stopping you from picking today?"
- **One-way door check (P-54):** "Once you do this, what is permanently locked? Who else needs to weigh in before the door closes?"

Decisions reversible within 30 days deserve speed, not deliberation (P-52). Bezos's framing (P-54) names the misclassification directly: most founder paralysis is treating a two-way door as a one-way door.

## Tier-7: AI-Startup Probes (2026)

When the founder is building an AI-first product, the questions that surface the real bottleneck have shifted.

- "What does your agent do that a fresh GPT-4o / Claude with a good system prompt cannot do?" (AP-17, P-60)
- "Who owns the customer's data after they cancel — you, or them?" (P-60 workflow lock)
- "What's your 90-day churn? AI-wrapper benchmark is ~65% — where are you?" (AP-17)
- "What's your cost per active user per month in inference? And gross margin trend over the last 3 months?" (AP-18)
- "Are you selling a tool or selling completed work? What outcome does the customer pay for?" (P-61)
- "If OpenAI / Anthropic shipped your exact feature next month, what survives?" (AP-17, P-60)
- "Walk me through last 90 days of bank-deposited revenue. Pilots, credits, and consulting separated." (AP-19)
- "How many user conversations this week — including how the user actually uses the agent in their workflow?" (P-02 still holds; vibe-coding lowered the build floor, not the talk-to-users floor)

## Tier-6: Closing Probes

End-of-session commitment-locking.

- "What will you do this week?"
- "Who will you talk to, by when?"
- "What evidence will tell you this worked?"
- "When should we check back in?"
- "What happens if you don't do this?"
- "Confirm: you'll have done X by date Y, and the evidence will be Z?"

If the founder hedges on commitment, the action is too vague — reformulate until concrete.

## Probing Discipline

- **One question at a time.** Multi-part questions dilute focus and let the founder cherry-pick the easiest.
- **One question per turn — never stack.** Ask, then stop. Stacking ("And what about X? And Y? And have you tried Z?") turns the session into interrogation and triggers founder defensiveness within 2-3 turns. If the answer is incomplete, follow up with a single targeted question, never a fresh question pile.
- **Wait for an answer.** Silence is a tool. Don't fill the gap. If the founder pauses, count to three before adding context.
- **Don't accept the first answer if it's narrative.** Push for specifics. "What specifically did the user say? Quote them."
- **Stop probing when the bottleneck is named and the founder agrees.** Over-probing past the diagnosis erodes trust.
- **Reflect rationalization back.** "You're saying the product needs to be ready before sales — but in week 3 you said the same thing about week 10. What's actually changing?"

## Founder Resistance Patterns

Common deflections and how to redirect:

| Deflection | Redirect |
|------------|----------|
| "It's complicated." | "Pick the one piece that matters most." |
| "I'm working on strategy." | "What did you do this week that touched a customer or production?" (AP-13) |
| "Investors love it." | "How many paying customers do you have?" (AP-16, P-40) |
| "We're going to be the X for Y." | "Who specifically is the first customer? Name them." (P-10) |
| "It depends on…" | "Assume the most likely path. What's the action?" |
| "We need to figure out X first." | "What's the cheapest 2-week test of X?" (P-52) |

## When to Stop Probing

Stop probing when:
- The founder has named one bottleneck and you can pattern-match it.
- The same answer has been re-asked twice and stayed unchanged.
- The session has consumed >50% of its exchange budget on PROBE alone.

Move to DIAGNOSE.
