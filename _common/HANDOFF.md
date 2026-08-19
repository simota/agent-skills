# Handoff Protocol (Common Definition)

Standard format for `## NEXUS_HANDOFF` output. Designed for flexibility: include what's relevant, skip what's not.

---

## NEXUS_HANDOFF Format

### Required Fields (always include)

| Field | Description |
|-------|-------------|
| **Summary** | What was accomplished (1-3 sentences) |
| **Next** | Recommended next agent or action |
| **Verified** | Required **whenever the handoff claims something passes, builds, or is done**. One entry per claim, each an evidence object — never a bare `true`. See *Completed vs Verified* below. Omit only when the step made no such claim. |

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
| **Do not repeat** | Approaches already **tried and ruled out**, each with the evidence that ruled it out. Distinct from *Suggested alternatives* (untried options worth considering) — this field exists to stop the next agent from re-running a dead end. Required whenever a handoff follows a failed attempt or a resumed long-running task. |
| **Guardrail Events** | Safety events triggered during execution |
| **Context labels** | For content the handoff *passes forward* rather than merely cites: its label per `_common/CONTEXT_SUFFICIENCY.md` §3b — at minimum `source` and `trust`. **Required whenever anything non-`operator` is forwarded** (a fetched page, a tool result, another agent's output, a summary this step produced). A receiving agent cannot recover the origin of text it is handed, so an unlabeled forward silently promotes external content to the same standing as the user's own words. Content the step produced by summarizing or merging inherits the strictest label of its inputs. |
| **Omitted** | What was deliberately left out and why — identifiers and reasons, never the content. Distinguishes "considered and set aside" from "never seen", which have opposite fixes. |

---

## Completed vs Verified

**"I changed the code" and "the acceptance criteria hold" are different claims.** Collapsing them is how a
chain inherits a false completion: the next step reads `tests passed`, skips its own check, and builds on a
state that was never confirmed. `_common/HARNESS_DEBT.md` names this `HD-STATE`; this section is how it is paid down.

- **Summary / Artifacts** carry what was *done* — edits made, files touched, analysis produced.
- **Verified** carries what was *confirmed*, and only that. A claim with no evidence object does not belong here.

### Evidence object

Each `Verified` entry is a claim plus the observation that supports it:

```yaml
Verified:
  - claim: "auth unit tests pass"
    command: "pytest tests/auth -q"
    exit_code: 0
    verified_at: 2026-08-17T10:31:12Z
    head: 4d2f9c1              # revision the check actually ran against
    log: artifacts/test-auth-447.log
  - claim: "public schema unchanged"
    command: "npm run contract:test"
    result: not_run             # explicit — distinguishes "unverified" from "forgotten"
```

`result: not_run` is a required distinction, not a formality: an absent row and an unrun check look identical
downstream, and only one of them is safe to re-derive. For non-executable work (design, spec, research),
`command` is replaced by the observation that stands in for it — a reviewer, a cited source locator, a
rendered artifact — but the claim/evidence pairing does not change.

### Validator rules (relations, not field presence)

A handoff that has all its fields can still be wrong. Check the relations:

| # | Rule | Fails when |
|---|------|-----------|
| V1 | `head` matches the repository HEAD the handoff reports | The check ran against a different revision than the work |
| V2 | `verified_at` is later than the last change to the files the claim covers | Evidence predates the edit it supposedly covers |
| V3 | `Artifacts` / changed files agree with `git diff --name-only` | The handoff describes work the tree does not contain |
| V4 | Every load-bearing claim in `Summary` appears in `Verified` or is labeled `UNVERIFIED` | Prose asserts more than the evidence supports |
| V5 | `Do not repeat` survived any compaction between attempt and handoff | The next agent re-runs a known dead end |

**Staleness rule:** if HEAD moves after the handoff is written, the handoff is `STALE` — regardless of how
complete it looks. The receiver re-derives rather than trusting it (`_common/OPERATIONAL.md` §
*Post-Handoff Rehydration*).

### Freshness is four clocks, not one

HEAD movement is one trigger of one kind. A handoff can be stale with HEAD untouched, and current with HEAD
moved. Check each clock that applies to the claim:

| Clock | Stale when | Typical trigger |
|-------|-----------|-----------------|
| **Time** | Elapsed since observation exceeds what the claim's impact tolerates | Wall clock |
| **Version** | The claim was made against a different code / spec / API version | `head` mismatch (V1), dependency bump |
| **Event** | A qualifying event occurred and nothing re-verified after it | `deployment_completed`, `feature_flag_changed`, `incident_declared`, `permission_changed` |
| **Authority** | The source that backed the claim no longer holds decision authority | ADR superseded, policy replaced, owner changed |

Declare the triggers a handoff is sensitive to rather than assuming git alone:

```yaml
invalidate_on: [deployment_completed, permission_changed]
max_age: PT1H          # scale to impact: PT24H low · PT1H medium · PT5M high · live-query critical
```

**Staleness is not one verdict.** Pick the response the claim's role warrants, and say which one was taken:

| Behavior | Use when |
|----------|----------|
| `re_fetch` | The source is cheap to re-read and authoritative — default |
| `fallback` | A last-known-good value is usable **and is labeled as such** in the handoff |
| `block` | The claim is load-bearing for an irreversible action |
| `escalate` | Staleness is caused by an authority change, not a clock |
| `degrade_scope` | Proceed read-only / analysis-only until re-verified |

A blanket reject on every stale field costs more than it saves; an unlabeled `fallback` is how a stale value
becomes a fact. Both failures are avoided by naming the behavior, not by picking a stricter default.

**Status ceiling:** a step whose claims carry no evidence reports `PARTIAL`, never `SUCCESS`. Producing the
work and verifying it are separate roles — an agent's own assertion is `E0` on `_common/EVIDENCE_LADDER.md`
and never ships on its own.

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
- Verified:
    - claim: "race reproduces"
      command: "pytest tests/auth/test_refresh_race.py -q"
      exit_code: 1
      head: 9f6c2a1
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
2. **Never state a pass/build/done claim outside `Verified`** — a claim in prose with no evidence object is
   `UNVERIFIED`, and the step's status is capped at `PARTIAL`
3. **Add detail proportional to complexity** — simple tasks need minimal handoff
4. **Be specific in Next** — include what the next agent should do, not just who
5. **Findings should be actionable** — include file paths, line numbers, evidence
6. **Risks should be concrete** — "might break X" is better than "there are risks"
7. **Journal what's worth keeping** — when a step produces a reusable insight, a notable decision, or state needed for recovery/learning, record it in `.agents/{agent}.md` / `.agents/PROJECT.md` per `_common/OPERATIONAL.md` and reference the paths in `Artifacts`. Routine or trivial steps don't need an entry.

---

## Pre-Handoff Journaling

When a handoff carries durable state, a reusable insight, or a notable decision, precede it with:

1. Appending one row to `.agents/PROJECT.md` (or BLOCKED if write fails)
2. Adding a journal entry to `.agents/{agent}.md` when a reusable insight was generated
3. Listing both file paths in the handoff `Artifacts` field

Routine or trivial steps that produce nothing worth persisting don't need an entry.

**Orchestrator handling (Nexus/Rally):** When recovery- or learning-relevant state is clearly missing from a handoff, the orchestrator asks the agent to record it before the chain moves on. Persistent journaling gaps from the same agent are a review signal — surface them rather than silently degrading.

**Why journaling matters:** Session durability (next section) depends on persistent state outside the orchestrator context. A handoff that skips journaling weakens crash recovery and routing learning — see also `_common/EVOLUTION.md` and `reference/routing-learning.md` (Nexus).

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
