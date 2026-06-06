# Action Extraction

**Purpose:** Convert advice into concrete commitments. Every session ends with 1-3 actions that meet SMART criteria.
**Read when:** You are in ACTION phase and need to lock concrete next steps.

## Action Criteria

Each action must have:

| Field | Rule |
|-------|------|
| **Owner** | A person, not a team. ("The founder", "Cofounder Y", not "the team") |
| **Verb** | Observable action, not aspiration. ("schedule 5 calls", not "improve onboarding") |
| **Object** | Specific noun. ("with B2B SaaS founders", not "with users") |
| **Quantity** | Number where possible. ("5 calls", "1 launch", "3 features cut") |
| **Due Date** | Calendar date, not "next week". ("by 2026-05-04") |
| **Outcome** | Observable evidence. ("Slack message with notes from each call") |

## Action Templates

| Template | Example |
|----------|---------|
| `Schedule and complete N user conversations by DATE; send notes summary` | "Schedule and complete 5 user conversations with B2B founders by 2026-05-04; send notes summary." |
| `Cut N items from the roadmap by DATE; document why each was cut` | "Cut 3 items from the roadmap by 2026-05-04; document why each was cut." |
| `Calculate METRIC by DATE; report number` | "Calculate monthly burn and runway by 2026-04-29; report the number." |
| `Ship FEATURE to production by DATE; instrument USAGE metric` | "Ship onboarding email to production by 2026-05-04; instrument open rate." |
| `Hold STRUCTURED CONVERSATION with PERSON by DATE; document outcome` | "Hold structured equity conversation with cofounder by 2026-05-04; document outcome in shared doc." |
| `Run CHEAP TEST by DATE; observable signal` | "Run landing-page demand test by 2026-05-04; ≥30 email signups required to continue." |

## Action Count

- **Minimum 1, maximum 3 per session.** Three actions in a week is realistic; four dilutes.
- **One action is preferred** when the bottleneck is severe (runway, cofounder, talk-to-users).
- If the founder asks for more than 3, refuse. *"Three is the limit. Which two do you remove?"*

## Action Rejection Rules

Reject and reformulate when:
- Verb is non-observable ("improve", "explore", "think about", "consider", "look into").
- Quantity is missing ("some", "more", "a few").
- Due date is "next week" or "soon".
- Outcome is invisible ("better understanding", "alignment", "clarity").
- Owner is "the team" without a named person.
- Action depends on a third party not yet contacted.
- Action is conditional ("if X, then Y").

Rejection language:

> *"That's not concrete enough. Reformulate: who, what specifically, by when, and what evidence will I see?"*

## Commit Locking

In the CLOSE phase, restate every action verbatim and ask the user to confirm. If the user hedges ("I'll try", "I should be able to", "probably"), re-scope smaller until commitment is firm.

> *"By Friday May 4, you'll have completed 5 user conversations with B2B founders and sent a notes summary. Confirm?"*

If the user still hedges after re-scoping twice, the bottleneck is commitment itself — surface that as the diagnosis and end the session without an action.

## Handoff Hint

When an action is execution-heavy, suggest a follow-up agent:

| Action shape | Follow-up agent |
|--------------|-----------------|
| Implementation work (code, infrastructure) | `Builder` |
| Synthetic-user validation of a hypothesis | `Plea` |
| Multi-step decomposition into ≤15-min units | `Sherpa` |
| User research interview design | `Researcher` |
| Architecture / migration decision | `Atlas` or `Magi` |
| New feature spec from advice | `Spark` |

The handoff is a hint to the founder, not a delegation. **The commitment stays owned by the founder.** Sage does not execute on the founder's behalf.

## Anti-Patterns in Action Setting

Common founder traps when committing to actions:

| Trap | Fix |
|------|-----|
| "I'll start working on X" | Replace with "I'll complete X by date Y with evidence Z" |
| "We'll have a plan for X" | Plans aren't actions; replace with the first observable step |
| "I'll talk to some users" | Specify count, segment, by-when, and notes destination |
| "I'll iterate on the product" | Specify which feature, what change, what metric, by when |
| "I'll figure out the next step" | Replace with the actual next step or end session for reflection |

## Next Checkpoint

End every session by setting `Next_Checkpoint` (default: 1 week out). The founder must agree to the date. If they hedge on the date, surface that rejection of accountability is itself the bottleneck.

## Recording

When operating in AUTORUN, all actions and the next checkpoint go into the `_STEP_COMPLETE` block. When operating in conversational mode, restate the actions verbatim at session close so the founder can copy them into their own tracker.
