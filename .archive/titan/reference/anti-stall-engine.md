# Anti-Stall Engine

Purpose: Read this file when Titan detects stalled execution, needs the full `L1-L5` recovery ladder, or must account for stall budgets and guardrail interactions.

## Contents

- Stall detection
- Recovery cascade
- Budget tracking
- Recovery flowchart
- Guardrail integration

13-level recovery cascade ensuring Titan never stops before exhausting all options.

---

## Stall Detection

A stall is detected when a phase cycle produces **zero progress artifacts** (no file changes, no test additions, no decisions recorded, no documents generated).

**Detection threshold**: 2 consecutive zero-progress cycles trigger the Anti-Stall Engine.

### Stall Classification

| Type | Symptom | Typical Cause |
|------|---------|---------------|
| **Agent Failure** | Agent returns error or empty result | Wrong agent, missing context |
| **Dependency Block** | Waiting on external input | Missing API key, unreachable service |
| **Complexity Block** | Task too large for single agent | Insufficient decomposition |
| **Approach Block** | Current method not working | Wrong methodology |
| **Scope Block** | Requirements exceed capabilities | Feature too ambitious |
| **Technology Block** | Library/framework limitation | Tool doesn't support needed feature |

---

## Recovery Cascade

### L1: Tactical Recovery (stay within current approach)

**Budget**: 5 attempts per phase, 10 per project.

#### 1.1 Retry with Context (on first failure)
- Inject error message and failure context into agent prompt
- Add relevant code snippets, specify exact expected output format

#### 1.2 Agent Swap (same agent fails twice)
- Switch to alternative agent: Builder↔Artisan · Sentinel↔Canon · Forge↔Builder · Scout↔Lens · Radar↔Voyager

#### 1.3 Decompose Further (agent succeeds partially)
- Invoke Sherpa to break failing task into smaller pieces
- Target: each sub-task completable in a single agent call

### L2: Operational Recovery (change methodology, same goal)

**Budget**: 3 attempts per phase, 5 per project.

#### 2.1 Alternative Approach (L1 exhausted)
- Switch: TDD↔Prototype-first · Top-down↔Bottom-up · Monolithic↔Modular · REST↔GraphQL

#### 2.2 Skip and Return (other non-blocked work exists)
- Mark blocked item as DEFERRED, continue with other items
- Return after other phase work completes (context may resolve block)

#### 2.3 Scope Reduction (feature partially implementable)
- Reduce to MVP version, cut non-essential requirements
- Document cuts and add to backlog for future iteration

### L3: Strategic Recovery (change direction)

**Budget**: 1 attempt per phase, 3 per project.

#### 3.1 Phase Reorder (other phases can proceed)
- Postpone stuck phase, advance to non-blocked phase, return with more context

#### 3.2 Scope Cut (feature blocking critical path)
- Remove entire features from roadmap (preserve core value proposition)
- Update SUCCESS_CRITERIA to reflect reduced scope

#### 3.3 Architecture Pivot (architecture is root cause)
- Fundamental change: Monolith↔Microservices · SSR↔SPA · SQL↔NoSQL · Sync↔Event-driven
- Requires re-running ARCHITECT phase for affected components

#### 3.4 Technology Swap (specific technology is bottleneck)
- Replace problematic library/framework via Magi evaluation + Forge prototype

### L4: Degradation Recovery (deliver what's possible)

**Budget**: No limit (graceful degradation always acceptable).

#### 4.1 Partial Delivery (most features work)
- Ship working parts, create detailed TODO docs for unfinished parts

#### 4.2 Stub Implementation (architecture clear, implementation blocked)
- Create interfaces/stubs with TODO annotations, full type definitions, tests against stubs

#### 4.3 Documentation-Only (implementation not feasible)
- Comprehensive design document, implementation guide, all decisions documented

### L5: User Escalation (last resort)

**Budget**: 1 per project per L1-L4 cycle.

#### 5.1 Single Focused Question
- Must be: Specific · Actionable · Minimal (one question) · Options-based (2-4 choices)

---

## Budget Tracking

```markdown
## Stall Budget Status
| Level | Phase Budget | Phase Used | Project Budget | Project Used |
|-------|-------------|------------|----------------|--------------|
| L1 Tactical | 5 | [N] | 10 | [N] |
| L2 Operational | 3 | [N] | 5 | [N] |
| L3 Strategic | 1 | [N] | 3 | [N] |
| L4 Degradation | ∞ | [N] | ∞ | [N] |
| L5 User | — | — | 1 | [N] |
```

Budget resets per phase for L1-L3. Project budget is cumulative across all phases.

---

## Recovery Flowchart

```
Stall Detected → L1.1 Retry → L1.2 Swap → L1.3 Decompose
  → L2.1 Alt approach → L2.2 Skip+return → L2.3 Scope reduce
  → L3.1 Phase reorder → L3.2 Scope cut → L3.3 Arch pivot → L3.4 Tech swap
  → L4.1 Partial delivery → L4.2 Stub impl → L4.3 Docs-only
  → L5.1 Ask user ONE question → Response → Restart cascade
Each step: Success? → Continue. Fail? → Next level.
```

---

## Guardrail Integration

Guardrail events (`_common/AUTORUN.md` § Guardrail Protocol L1-L4) map to Anti-Stall levels: L2 recovery failure → Anti-Stall L1, L3 pause → Anti-Stall L1-L2, L4 abort → immediate halt + rollback. Guardrail auto-recoveries do NOT consume Anti-Stall budget; only failures escalated to Titan do.
