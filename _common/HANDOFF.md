# Handoff Protocol (Common Definition)

Standard format for `## NEXUS_HANDOFF` output. Designed for flexibility: include what's relevant, skip what's not.

---

## NEXUS_HANDOFF Format

### Required Fields (always include)

| Field | Description |
|-------|-------------|
| **Summary** | What was accomplished (1-3 sentences) |
| **Next** | Recommended next agent or action |

### Recommended Fields (include for complex tasks)

| Field | Description |
|-------|-------------|
| **Findings** | Key discoveries, root causes, analysis results |
| **Risks** | Identified risks, concerns, potential issues |
| **Open questions** | Unresolved items that need attention |

### Optional Fields (include when applicable)

| Field | Description |
|-------|-------------|
| **Step** | Step number in chain (e.g., 2/5) |
| **Agent** | Current agent name |
| **Artifacts** | Files created or modified |
| **Contract_Ref** | Sprint Contract ID (e.g., SC-login-feature-20260325) when Evaluator Loop is active |
| **Pending Confirmations** | Decisions awaiting user input |
| **User Confirmations** | Decisions already confirmed by user |
| **Suggested alternatives** | Alternative approaches considered |
| **Guardrail Events** | Safety events triggered during execution |

---

## Examples

### Minimal (simple task)

```
## NEXUS_HANDOFF
- Summary: Root cause identified — null check missing in `auth.ts:42`
- Next: Builder (implement fix)
```

### Standard (typical task)

```
## NEXUS_HANDOFF
- Step: 2/4
- Agent: Scout
- Summary: Investigated login failure. Root cause: token refresh race condition in `auth/refresh.ts:87`
- Findings: Two concurrent refresh calls invalidate each other's tokens
- Artifacts: Investigation notes in `.agents/scout.md`
- Risks: Fix may affect session handling in other flows
- Next: Builder (implement mutex-based refresh)
```

### Full (complex/high-risk task)

```
## NEXUS_HANDOFF
- Step: 3/7
- Agent: Sentinel
- Summary: Security audit complete. 2 critical, 1 medium vulnerability found
- Findings: SQL injection in search endpoint, XSS in comment rendering, weak CSRF token
- Artifacts: `reports/security-audit.md`
- Risks: SQL injection is exploitable in production
- Pending Confirmations: Deploy hotfix vs scheduled release?
- User Confirmations: "Prioritize security over feature work" (confirmed 2024-01-15)
- Open questions: Third-party dependency CVE-2024-XXXX — vendor patch ETA unknown
- Suggested alternatives: WAF rule as interim mitigation
- Guardrail Events: L3 triggered (critical security), auto-paused for review
- Next: Builder (implement fixes, priority: SQL injection first)
```

---

## Rules

1. **Always include Summary + Next** — these are the minimum for any handoff
2. **Add detail proportional to complexity** — simple tasks need minimal handoff
3. **Be specific in Next** — include what the next agent should do, not just who
4. **Findings should be actionable** — include file paths, line numbers, evidence
5. **Risks should be concrete** — "might break X" is better than "there are risks"
6. **Journaling is a hard gate** — before emitting handoff, confirm `.agents/{agent}.md` and `.agents/PROJECT.md` writes per `_common/OPERATIONAL.md` → *Pre-Handoff Checklist*. Reference both paths in `Artifacts`.

---

## Pre-Handoff Journaling Gate

Every `## NEXUS_HANDOFF` and `_STEP_COMPLETE` **MUST** be preceded by:

1. Appending one row to `.agents/PROJECT.md` (or BLOCKED if write fails)
2. Adding a journal entry to `.agents/{agent}.md` when a reusable insight was generated (or noting "no novel insight" in the PROJECT.md row)
3. Listing both file paths in the handoff `Artifacts` field

**Orchestrator enforcement (Nexus/Rally):** A handoff returned without journaling evidence is treated as `PARTIAL`. The orchestrator reroutes the agent to complete the logging step before chain progression. After 2 consecutive journaling-gate failures from the same agent, escalate to the user.

**Why this is a gate, not a suggestion:** Session durability (next section) depends on persistent state outside the orchestrator context. A handoff that skips journaling breaks crash recovery and routing learning — see also `_common/EVOLUTION.md` and `reference/routing-learning.md` (Nexus).

---

## Session Durability Principle

> Handoff data is the session log. It must survive orchestrator interruption.

Based on the Managed Agents virtualization pattern (Anthropic), session state (the append-only record of what happened) must live outside the orchestrator so that:

- **Crash recovery**: If the orchestrator (Nexus/Rally) is interrupted mid-chain, the last `_STEP_COMPLETE` + `NEXUS_HANDOFF` in `.agents/PROJECT.md` and agent journals enables any new orchestrator instance to resume from the last successful step.
- **Debuggability**: All handoff data is inspectable in persistent files (`.agents/*.md`), not trapped in a transient context window.
- **Checkpoint-resume**: For chains with 4+ steps, each `_STEP_COMPLETE` acts as a durable checkpoint. A `wake(sessionId)` equivalent is: read `.agents/PROJECT.md` → find last completed step → reconstruct handoff context → spawn next agent.

### Practical Implications

| Situation | Action |
|-----------|--------|
| Chain interrupted mid-step | Read `.agents/PROJECT.md` for last `_STEP_COMPLETE`; resume from that point |
| Handoff context too large for prompt | Store in `.agents/{agent}.md` journal; pass file path reference instead |
| Need to replay or debug a chain | All steps are traceable via `PROJECT.md` activity log + individual journals |

### What to Persist vs. What to Pass Inline

| Data | Persist (journal/PROJECT.md) | Pass inline (prompt) |
|------|------------------------------|---------------------|
| Step completion status | Always | Always |
| File paths modified | Always | Always |
| Detailed investigation notes | Always | Summary only |
| Full error traces | Always | Key error + file:line only |
| Acceptance criteria | Always (at chain start) | Reference only |

---

## DESIGN_INTENT_HANDOFF Format

**Purpose**: Specialized handoff schema for design-to-implementation pipelines (inspired by Claude Design by Anthropic Labs, 2026-04-17). Use this when atelier/Vision/Frame/Muse hand off to implementation agents (Forge/Artisan/Pixel/Vitrine) or to Claude Code.

**When to use**:
- atelier orchestrating design → code loops
- Vision passing direction to Muse/Frame/Forge
- Forge/Pixel producing prototypes to hand off to Artisan
- Any chain where design intent must survive handoff without lossy re-interpretation

### Required Fields

| Field | Description |
|-------|-------------|
| **Intent** | Design direction in natural language (from Vision or user). What feel, what audience, what emotional register |
| **Tokens** | Current design-system tokens as `{color, typography, spacing, radius, shadow, motion}`. Reference to `.agents/design-system/{project}.json` when loaded |
| **Constraints** | Platform (web/mobile/desktop), brand rules, a11y targets (WCAG level), regulatory (cookie/ADA/EU AI Act), performance budgets |
| **Acceptance** | Measurable criteria — contrast ratio, bundle size, responsive breakpoints, browser matrix |

### Recommended Fields

| Field | Description |
|-------|-------------|
| **Assets** | References to images, icons, fonts, existing components (file paths or URLs) |
| **References** | Inspiration sources — screenshots, competitor UIs, Figma URLs, web captures |
| **Variants** | Parametric options if the caller wants multiple explorations (see `_common/parametric-output.md`) |
| **Code_Instructions** | When next agent is Claude Code / Artisan / Builder: explicit "what file, what framework, what test" directives |

### Optional Fields

| Field | Description |
|-------|-------------|
| **Registry_Ref** | Path to persisted design system (e.g., `.agents/design-system/marketing-2026.json`) |
| **Vision_Ref** | Path to Vision direction document (e.g., `.agents/vision/direction.md`) |
| **Handoff_Bundle** | Path to structured bundle (see `_templates/handoff-bundle.template.json`) |
| **Do_Not** | Explicit anti-patterns — colors/layouts/words that must be avoided |

### Example (Minimal)

```yaml
DESIGN_INTENT_HANDOFF:
  Intent: "Calm, trustworthy landing page for B2B fintech — reduce perceived risk"
  Tokens: { color: "registry:marketing-2026", typography: "Inter/Fraunces", spacing: "base-8" }
  Constraints: "Web only, WCAG 2.2 AA, LCP < 2.5s"
  Acceptance: "Hero + 3 feature blocks + CTA; contrast ≥ 4.5:1"
  Next: Forge (prototype)
```

### Example (Full)

```yaml
DESIGN_INTENT_HANDOFF:
  Intent: |
    Ship-ready dashboard for on-call engineers. Tone: calm under pressure,
    dense but scannable. No marketing gloss. Dark-mode first.
  Tokens:
    color: ".agents/design-system/observability-2026.json"
    typography: "Inter (UI) / JetBrains Mono (metrics)"
    spacing: "dense-4"
    radius: "sharp"
  Constraints:
    platform: "web + Electron"
    a11y: "WCAG 2.2 AA, keyboard-first, screen-reader for alert states"
    perf: "TTI < 1.5s on mid-range laptop; update cadence 2s"
    brand: "no emojis in UI copy; no gradients; use our logo monochrome"
  Acceptance:
    - "Incident list + timeline + drill-down modal"
    - "Contrast ≥ 7:1 for critical status indicators"
    - "Keyboard shortcut overlay (?-key)"
  Assets:
    - "assets/icons/severity-*.svg"
    - "fonts/Inter-Variable.woff2"
  References:
    - "https://linear.app/inbox"
    - ".agents/web-capture/datadog-dashboard-2026-04.png"
  Variants:
    density: [compact=3 / base=4 / relaxed=6]
    accent: [cyan=#06b6d4 / amber=#f59e0b]
  Code_Instructions:
    framework: "Next.js 15 / React Server Components"
    files: ["app/dashboard/page.tsx", "components/incident-*"]
    test: "Playwright a11y + visual regression"
  Registry_Ref: ".agents/design-system/observability-2026.json"
  Vision_Ref: ".agents/vision/direction-2026-04.md"
  Handoff_Bundle: ".agents/atelier/bundle-dashboard-2026-04.json"
  Do_Not:
    - "Pastel colors"
    - "Illustrations or hero images"
    - '"Delightful" / "magical" / "powerful" in copy'
  Next: Artisan (implement) → Vitrine (catalog)
```

### Rules

1. **Intent is mandatory** — a handoff without explicit design intent is a handoff that will drift
2. **Tokens must be referenceable** — either inline or a registry path. Never free-form color names
3. **Constraints include a11y by default** — WCAG level must be declared, not assumed
4. **Code_Instructions are explicit when crossing the design→code boundary** — frameworks, file paths, test expectations
5. **Do_Not is as important as Intent** — negative space prevents regression to generic outputs
6. **Registry_Ref persists across sessions** — the design system outlives any single chain; refer to it, don't re-derive it
