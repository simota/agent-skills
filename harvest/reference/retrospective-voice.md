# Retrospective Voice

Purpose: Use this mode when Harvest should turn PR and release data into a human, developer-friendly narrative without changing the underlying facts.

## Contents

- When to apply
- Voice styles
- Output lengths
- Event-to-narrative mapping

## When To Apply

Use when the report should feel like a retrospective, release commentary, internal newsletter, or culture note rather than a pure metric dump.

## Voice Styles

| Style | Tone | Best for |
|------|------|----------|
| Pragmatic | Grounded, direct, practical | Sprint retros, refactoring, hard weeks |
| Passionate | High-energy, celebratory | Feature launches, morale posts |
| Analytical | Structured, data-forward | Metrics reviews, trend commentary |

## Output Lengths

| Length | Use when | Shape |
|--------|----------|-------|
| Short | Slack or chat update | `1-2` sentences plus one metric |
| Medium | Team update | short narrative + numbers + wins + next |
| Long | Retrospective document | full story + lessons learned + forward look |

## Event-To-Narrative Mapping

| Git event | Narrative angle |
|----------|-----------------|
| Large refactor | "The Cleanup" |
| Many small PRs | "The Machine" |
| Hotfix after release | "The Save" |
| First-time contributor | "The New Voice" |
| Long-lived branch merged | "The Marathon" |
| Dependency major upgrade | "The Migration" |

## Guardrails

- Do not invent sentiment that the data cannot support.
- Keep the facts, dates, and metrics accurate.
- Use narrative to explain, not to mask weak signals.

## Retrospective Framework Catalogue (2026)

| Framework | Lens | Best fit |
|-----------|------|----------|
| Start / Stop / Continue (Keep/Drop/Start variant) | Behavior change | Default low-friction sprint retro; every note maps to a commitment |
| Mad / Sad / Glad | Emotion | Surfacing morale and frustration after intense sprints |
| 4Ls (Liked / Learned / Lacked / Longed for) | Positive-framed learning | Project end, milestone, or onboarding retro |
| Plus / Delta | Lightweight pair lens | Quick post-meeting or release-checkpoint review |
| Sailboat (Wind / Anchor / Rocks / Island) | Goal-and-blocker narrative | Cross-functional or quarterly retros |
| Speed Boat | Hazard-focused variant of Sailboat | Identifying drag and risks before a launch |

Selection guidance: per agile-coach surveys for 2025, Keep/Drop/Start, Mad/Sad/Glad, and Speed Boat remain the most-cited defaults (`kollabe.com/posts/retrospective-formats-compared`, retroteam.ai 2025). When narrative voice is layered onto Harvest data, pick the framework that matches what the PR record actually shows: a heavy-refactor week pairs with Sailboat (rocks), a launch week pairs with Plus/Delta, and a high-defect-rate week pairs with Mad/Sad/Glad.
