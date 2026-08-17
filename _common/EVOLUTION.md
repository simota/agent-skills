# Evolution Shared Protocol

Shared specification for ecosystem self-evolution. All agents may reference this protocol when contributing to or consuming evolution data.

---

## EVOLUTION_SIGNAL Format

When any agent discovers an insight worth propagating to the ecosystem, it can emit an EVOLUTION_SIGNAL in its journal entry or output:

```markdown
<!-- EVOLUTION_SIGNAL
type: [INSIGHT | PATTERN | DRIFT | GAP | FEEDBACK]
source: [agent name]
date: YYYY-MM-DD
summary: [1-2 sentence description]
affects: [list of agent names or "ecosystem"]
priority: HIGH | MEDIUM | LOW
reusable: true | false
-->
```

### Signal Types

| Type | When to emit | Example |
|------|-------------|---------|
| INSIGHT | Agent discovers a reusable lesson | "Caching improves Builder chain by 40%" |
| PATTERN | Recurring theme detected across tasks | "Auth bugs always involve token expiry" |
| DRIFT | Convention or strategy deviation noticed | "Team shifted from REST to GraphQL" |
| GAP | Unserved need identified | "No agent handles WebSocket testing" |
| FEEDBACK | Quality signal about the ecosystem | "Judge→Architect chain has 90% success" |

### Usage Guidelines

- Emit signals only for findings that affect multiple agents or future tasks
- Do NOT emit signals for task-specific details that won't recur
- Signals are collected by Darwin during Journal Synthesis (ET-04)
- Agents do NOT need Darwin to be invoked to emit signals — they are stored in journals for later collection

---

## ECOSYSTEM.md Reading Rules

When an agent reads `.agents/ECOSYSTEM.md`, follow these rules:

### What to Read

| Section | Who should read | When |
|---------|----------------|------|
| Project Lifecycle | All agents | To understand current phase context |
| Dynamic Affinity Override | Nexus | During routing decisions |
| Ecosystem Fitness Dashboard | Nexus (Proactive Mode) | To display health summary |
| Agent Relevance Scores | Individual agents | To understand own relevance |
| Cross-Agent Discoveries | All agents | When starting a task in a known pattern area |
| Staleness Report | Architect, Void | When reviewing agent fitness |

### Reading Protocol

1. **Check existence**: ECOSYSTEM.md may not exist yet. If absent, proceed normally — Darwin will create it on first invocation.
2. **Read selectively**: Only read sections relevant to your current task. Do not process the entire file.
3. **Freshness check**: Check `Last Evolution Check` date. If >30 days old, data may be stale — still use it but note staleness.
4. **Do not modify**: Only Darwin writes to ECOSYSTEM.md. Other agents read only.

---

## Dynamic AFFINITY Override Application

### For Nexus (Routing)

When routing a task:

1. Read `.agents/ECOSYSTEM.md` → Dynamic Affinity Override section
2. For each agent in the proposed chain:
   - If an override exists and is not expired (< 90 days old):
     - Use override value instead of base PROJECT_AFFINITY
   - Else:
     - Use base PROJECT_AFFINITY as normal
3. Log override application: `_AFFINITY_OVERRIDE: [agent] [base] → [override]`

### Override Precedence

```
1. User explicit override (always highest)
2. Darwin Dynamic AFFINITY Override (from ECOSYSTEM.md)
3. PROJECT_AFFINITY.md base affinity
```

### Override Expiry

- Overrides carry a **removal condition**, not only a date: the state of the world that made the override necessary, and what would make it unnecessary.
- Overrides are reviewed 90 days after their `Date` field. Review means re-checking the condition — an override whose condition still holds is renewed with a new `Date`, not dropped.
- Only an override whose condition no longer holds, or which carries no condition at all, is retired. Expiring on the date alone would silently drop a control that is still load-bearing (`_common/HARNESS_DEBT.md` § Complexity Budget).
- Darwin refreshes overrides on ET-01 (phase transition) and periodic checks

---

## Journal Recording Recommendations

When recording journal entries, agents are encouraged to:

### Tag Reusable Insights

Add `reusable: true` or `reusable: false` to journal entries:

```markdown
## 2026-02-19 - Cache Strategy Insight

**Chain:** Scout → Builder → Radar
**Insight:** Redis caching for session data reduced response time by 60%.
**Apply when:** Session-heavy SaaS applications with >1000 concurrent users.
**reusable:** true
```

### Include EVOLUTION_SIGNAL When Appropriate

Embed signals in journal entries for Darwin to collect:

```markdown
## 2026-02-19 - Auth Pattern Discovery

**Chain:** Sentinel → Builder → Radar
**Insight:** JWT refresh token rotation prevents 95% of token theft attacks.
**Apply when:** Any application using JWT authentication.
**reusable:** true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Sentinel
date: 2026-02-19
summary: JWT refresh token rotation is a critical security pattern
affects: [Builder, Gateway, Sentinel]
priority: HIGH
reusable: true
-->
```

### Benefits

- Agents that tag reusable insights contribute to ecosystem knowledge
- Darwin's Journal Synthesizer (ET-04) processes these tags efficiently
- Cross-agent discoveries improve over time as more agents participate
- No agent is required to participate — tagging is recommended, not mandatory
