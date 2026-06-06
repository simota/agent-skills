# Managed Agents — Pattern Mapping

Anthropic's **Claude Managed Agents** (announced Code w/ Claude SF 2026) bundles four features that map closely to existing Nexus patterns. Use this reference to align local routing with the official vocabulary, and to surface upgrade paths when a chain would benefit from the managed-platform equivalent.

[Source: Anthropic — *Code with Claude SF 2026* and *New in Claude: Managed Agents* (2026)](https://claude.com/blog/new-in-claude-managed-agents)
[Source: Anthropic — *Introducing Dynamic Workflows in Claude Code* (2026)](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code) — see §5.

---

## 1. The Four Features

| Managed Agents feature | What it is | Nexus equivalent | Where in Nexus |
|--------------------------|-----------|-----------------|----------------|
| **Multiagent Orchestration** | Lead agent decomposes the job and delegates each piece to a specialist; specialists can have different models, prompts, and tools; they coordinate over a shared filesystem. | Hub-and-spoke routing with `_AGENT_CONTEXT` / `_STEP_COMPLETE`; Recipe-driven chains; Rally for parallel branches. | `Core Contract`, `Recipes`, `reference/orchestration-patterns.md`, `_common/PARALLEL.md` |
| **Outcomes** | Rubric-based automatic output evaluation and iterative improvement. Each spec defines what "done" looks like; the platform scores against it and loops until the rubric passes. | Evaluator-Loop pattern; Sprint Contract; Rubric System; Judge as quality gate. | `reference/evaluator-loop-protocol.md` (merged: loop + contract + rubric) |
| **Dreaming** | Off-line analysis of past sessions to curate memories and propagate distilled knowledge across future runs. | Lore — cross-agent pattern extraction, METAPATTERNS.md curation, freshness scoring, organizational unlearning. | Delegate to Lore; see `lore/SKILL.md` |
| **Webhooks** | Completion / state-change notifications to external systems (CI, Slack, dashboards). | PushNotification + Mend handoffs; Beacon for production alerting; explicit `_STEP_COMPLETE` schema. | `reference/output-formats.md`, route via Mend/Beacon |

## 2. Selection Rules

Use the Nexus-local equivalent (default) when:
- The work runs inside a single Claude Code or Codex CLI session.
- All specialists are local skill agents under `~/.claude/skills/`.
- Coordination overhead is contained within a single user session.

Recommend escalating to the **managed platform** (and surface the recommendation in `NEXUS_COMPLETE`) when:
- The chain runs unattended over hours or days (Webhooks > local polling).
- A team-wide knowledge base must persist across many users' sessions (Dreaming > per-user Lore).
- The Outcome rubric must be enforced across many concurrent invocations with platform-level audit (Managed Outcomes > Evaluator-Loop in-session).
- The customer needs Anthropic Console audit trails for compliance (every step durably logged with the agent's identity, order, and reasoning).

Otherwise stay on the local hub-and-spoke chain. Adopting the managed platform for short-lived single-user tasks pays only coordination cost without unlocking its differentiators.

## 3. Anti-Pattern: Reinventing the Feature

When a request describes one of the four features in disguise, prefer the official feature in vocabulary even if implemented locally:

- "Score my output against criteria and rerun until it passes" → call this **Outcomes / Evaluator Loop**, not "validation chain".
- "Remember what worked across past projects" → call this **Dreaming**, route to Lore.
- "Tell my dashboard when it's done" → call this **Webhooks**, route to Mend / PushNotification.
- "Split this between specialists" → call this **Multiagent Orchestration**, route as a Nexus chain.

Shared vocabulary with the platform reduces translation cost when chains later migrate to managed agents.

## 4. Cited Deployment Patterns

Public reference deployments documented by Anthropic at SF 2026:
- **Harvey** (legal document drafting): completion rate ≈6× higher under Multiagent Orchestration vs single-agent baseline.
- **Netflix**: log-analysis lead agent fans out across multiple log sources in parallel; aggregates findings.
- **Spiral**: combines Multiagent Orchestration with Outcomes to enforce editorial-quality bars on generated long-form writing.
- **Wisedocs**: document verification 50% faster after migrating to managed agents with shared filesystem coordination.

Use these as evidence when proposing local chain patterns of the same shape (e.g., "we are using the Netflix pattern: lead agent fans out across N independent investigators").

---

## 5. Dynamic Workflows (Claude Code-native, research preview 2026)

**What it is.** A Claude Code feature where Claude "dynamically writes orchestration scripts that run tens to hundreds of parallel subagents in a single session, checking its work before anything reaches you." It is the native, in-session delivery of Multiagent Orchestration (§1) + Outcomes-style verification + automatic checkpointing, combined into one mechanism. "Progress is saved as the run goes, so a job that's interrupted picks up where it left off instead of starting over." High-stakes runs add **adversarial review** (agents attempt to refute findings before delivery).

| Property | Dynamic Workflows | Nexus equivalent |
|----------|-------------------|------------------|
| Fan-out scale | tens–hundreds of parallel subagents | L2 Parallel Spawn / Rally (L3) — typically 2–8 branches before hierarchical decomposition (Core Rule #9) |
| Verification | independent verification + adversarial review before integration | Evaluator-Loop / `acceptance` Code+Design adversaries |
| Resume | native checkpoint-resume across interruptions | Checkpoint-resume for 4+ step chains (Safety Contract) |
| Orchestration logic | Claude writes the orchestration script on the fly | Recipe + routing-matrix (pre-designed chains) |

**Why isolation + adversarial review (the failure modes DW exists to fix).** A single agent working a complex task in one context window degrades in three specific ways — these are the canonical justification for spawning isolated subagents (Core Rule #3) and for the adversarial-verification stage, not just a performance optimization:
1. **Agentic laziness** — the agent declares the task complete after partial progress (e.g. addressing 35 of 50 items in a security review). Mitigation: one isolated subagent per item with a narrow, checkable goal, so "done" is verified per-item, not self-asserted over the whole set.
2. **Self-preferential bias** — when asked to verify or judge its own output, the agent favors its own prior findings. Mitigation: a *separate* agent (ideally a different model) performs verification — the generator-evaluator separation Judge also enforces against self-grade inflation.
3. **Goal drift** — the original objective loses fidelity through successive summarization steps. Mitigation: each subagent receives the original goal directly in its own context rather than a summary-of-a-summary.
[Source: claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code]

**Activation (Claude Code).** Two paths:
1. Ask directly: "Create a dynamic workflow".
2. Enable the **`ultracode`** setting (effort menu) — sets effort to `xhigh` and lets Claude auto-decide when to deploy a workflow. Auto mode is recommended. `ultracode` ≈ AUTORUN_FULL + Opus 4.8 P6 (`xhigh` baseline).

**Availability.** Research preview across Claude Code CLI, Desktop, VS Code extension, and the Claude API (incl. Amazon Bedrock, Vertex AI, Microsoft Foundry).

**Selection rule — native Dynamic Workflows vs Nexus manual orchestration:**
- Prefer **native Dynamic Workflows** as the *execution substrate* for large homogeneous fan-outs on Claude Code: codebase-wide bug hunts / security audits, large migrations or framework modernization spanning thousands of files, and critical work needing independent verification. Native DW scales fan-out and checkpointing further than Nexus can manually spawn.
- Keep **Nexus** as the *routing/recipe layer*: task classification, minimum-viable-chain design, cross-domain specialist selection (Recipes), and hub-spoke guardrails. Nexus's value is *which* specialists and *what shape*, not raw parallel throughput.
- Composition: a Nexus Recipe step whose work is a large parallel sweep (e.g. `acceptance` Code Oracles, `apex` Loop) may **delegate execution to a native dynamic workflow** when available, rather than Nexus issuing dozens of individual `Agent(...)` calls. Surface this in `NEXUS_COMPLETE` when the workload matches a DW use case.
- When DW is unavailable (Codex CLI / agy, or older Claude Code), fall back to L2/L3 spawn + Core Rule #9 hierarchical decomposition.

**Anti-pattern vocabulary (extends §3):** "run hundreds of agents in parallel and self-check until it converges" → call this **Dynamic Workflows**, not "big parallel chain".

---

## When to Read This File

- During `CLASSIFY` when the user explicitly mentions Managed Agents, Outcomes, Dreaming, Webhooks, **Dynamic Workflows, or `ultracode`**.
- During `CHAIN_SELECT` when a request describes a managed-agents feature in plain English, **or when a Recipe step is a large parallel sweep that native Dynamic Workflows could execute**.
- During `DELIVER` to surface an escalation recommendation in `NEXUS_COMPLETE` if the local hub-and-spoke is not the right long-term home for the workload.
