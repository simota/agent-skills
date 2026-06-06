# Onboarding & Usage Examples

**Purpose:** Concrete examples of Compass interactions for onboarding users.
**Read when:** You need onboarding scenarios, example dialogues, or usage guidance.

---

## Onboarding Guide

### Level 1: First Contact

Convey the big picture of the ecosystem. Emphasize "what's possible" over detail.

**Recommendation script:**

```
This ecosystem includes 100+ specialist skills, organized into five broad areas:

1. Build: Builder (implementation), Forge (prototypes), Artisan (frontend)
2. Fix: Scout (investigation), Zen (refactoring), Bolt (speedups)
3. Defend: Sentinel (security), Radar (testing), Judge (review)
4. Design: Atlas (architecture), Schema (DB), Gateway (API)
5. Operate: Pipe (CI/CD), Scaffold (infrastructure), Beacon (monitoring)

Tell me what you want to do, and I'll suggest the best skill.
```

### Level 2: Category Deep Dive

Give details to a user who has shown interest in a specific category.

**Example: "Tell me about the testing skills"**

```
There are three testing skills:

1. Radar — unit tests, edge cases, flaky-test repair
   How to use: `/radar improve test coverage for this module`

2. Voyager — E2E tests (Playwright / Cypress)
   How to use: `/voyager build an E2E test for the login flow`

3. Siege — load tests, chaos engineering, contract tests
   How to use: `/siege design a load test plan for this API`

How to choose:
- Function or module level → Radar
- Whole user flow → Voyager
- Non-functional requirements → Siege
```

### Level 3: Scenario Matching

Recommend the best skill for a specific task.

**Example: "We're getting 500 errors in production"**

```
## Recommendation: Investigate and fix production 500s

### 1. Scout (top pick)
- **What it does**: Pinpoints the root cause and reports reproduction steps and impact
- **Why this one**: 500 causes are diverse — investigation comes first
- **How to use**: `/scout we're getting 500s on /api/users in prod. Logs: ...`
- **Caveat**: Scout doesn't write code; the fix hands off to Builder

### 2. Triage (alternative)
- **What it does**: Incident first response, impact identification, recovery procedure
- **When to pick this instead**: Many users are affected and urgency is high

### Next step
Use Scout's findings, fix with `/builder`, then add a regression test with `/radar`.
```

---

## FAQ Patterns

### Q: "What's the difference between Nexus and Compass?"

```
- Compass: guides you to the right skill (the navigator).
- Nexus: actually combines skills and runs the task (the orchestrator).

By analogy:
- Compass = travel guidebook (tells you where to go).
- Nexus = tour guide (actually takes you there).

For simple tasks, look at Compass's recommendation and call the skill directly.
For complex tasks, go Compass → Nexus for automated orchestration.
```

### Q: "There are too many similar skills — I can't choose"

```
For common confusion pairs and how to choose, see the "Don't Use" Quick Reference in patterns.md.

When in doubt, ask: "Does this skill change code?"
- Changes code: Builder, Zen, Artisan, Bolt
- Doesn't: Scout, Judge, Atlas, Sentinel
```

### Q: "I want to start a new project"

```
Recommended chain for a new project:

1. Scribe — requirements and technical specifications
2. Atlas — architecture design
3. Schema — DB design (if needed)
4. Gateway — API design (if needed)
5. Grove — repository structure
6. Scaffold — dev environment and infrastructure
7. Forge — prototype
8. Builder — production implementation

You don't need all of them. Adjust to scope:
- Small: Forge → Builder
- Medium: Scribe → Builder → Radar
- Large: Scribe → Atlas → Builder → Radar → Judge
```

---

## Interaction Examples

### Example 1: Direct Skill Question

**User**: "DB queries are slow"
**Compass**:

```
## Recommendation: Improve DB query performance

### 1. Tuner (top pick)
- EXPLAIN ANALYZE, query-plan optimization, index recommendations
- `/tuner optimize this slow query: SELECT ...`

### 2. Bolt (alternative)
- When app-layer caching or N+1 fixes are also in scope
- `/bolt speed up the response of this API endpoint`

DB-only → Tuner. Whole-app → Bolt.
```

### Example 2: Vague Request

**User**: "I want to improve code quality"
**Compass**:

```
"Code quality" has several facets — which fits best?

1. Readability and structure → Zen (refactoring)
2. Add tests → Radar (test coverage)
3. Strengthen security → Sentinel (vulnerability detection)
4. Add documentation → Quill (JSDoc / comments)
5. Remove dead code → Sweep (dead-code removal)
6. All of the above → Nexus combining the above

Tell me which area matters most, and we'll pick from there.
```

### Example 3: Gap Detection

**User**: "I want to build a Slack bot"
**Compass**:

```
## Recommendation: Slack bot development

### 1. Relay (top pick)
- Specialist for messaging integration, bot development, webhook design
- `/relay design the architecture for a Slack bot`

### 2. Builder (implementation phase)
- When implementing based on Relay's design
- `/builder implement the Slack bot per Relay's design`

### Next step
Design with Relay → implement with Builder → test with Radar.
```
