# Codex Orchestration Authoring Protocol

> **Tier:** `orchestration` — activates from the hub, a recipe, or on engine detection. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

Codex-specific adaptation of the shared `_common/OPUS_5_AUTHORING.md` principles. Current model IDs, CLI features, permission guidance, and official sources live in `_common/CLI_COMPATIBILITY.md`. Preserve C1–C9 identifiers for existing consumers; do not copy this protocol into spawn prompts.

## Why This Exists

A host's native tools, configuration, and result channels differ from another CLI's. Adapt those interfaces without replacing the specialist's method or importing another model's prompting workarounds. A Codex worker in a multi-engine review also follows `_common/MULTI_ENGINE_RECIPE.md` and `_common/SUBAGENT.md`.

## The Nine Principles

### C1. Spawn Capacity and Depth Budget

Before fan-out, discover the actual native delegation interface and effective capacity/depth limits. Respect the lower of runtime limits, recipe limits, and authorized budget. Do not assume a fixed thread count or an old config key. Verify a capability through advertised tools, runtime help/configuration, or a harmless supported probe. Record concrete unavailable/denied capability evidence before using the fallback in `nexus/reference/execution-layers.md`.

### C2. Concurrent Fan-Out / Join

Launch independent tasks together when the host supports it. Give each writer disjoint files or an isolated worktree; identify the merge owner and join required results before dependent work. A running child is not a completed result. Use sequential execution for real data dependencies, shared mutable state, or an explicit recipe gate—not merely because calls appear in a numbered plan.

### C3. Reasoning-Effort Routing

**C3.0 — Runtime selection:** use `_common/CLI_COMPATIBILITY.md` §4. The previous fixed-generation/variant mandate is retired. Preserve explicit user model choices and the approved cost envelope; select a current stable available model when a selection is needed. Do not silently fall back across unavailable models or providers.

Configure effort only through supported model/runtime settings. Choose it from task difficulty and measured quality, not a copied enum or the number of files. Stronger reasoning does not establish permission, guarantee correctness, or replace required tests.

### C4. Loose-Prompt Spawning

Pass the goal, source paths/revision, constraints, owned write surface, acceptance criteria, and result shape. The specialist reads its own SKILL.md and applicable contracts; do not repeat its framework, chain-of-thought instructions, or a second checklist. Keep independent reviewers free of the producer's verdict while giving them the actual task and evidence needed to verify it.

### C5. Lazy Tool Visibility

A shortened tool list is not proof of absence. Use the runtime's discovery mechanism when available, then call only the returned schema. If no discovery/spawn mechanism is exposed, say exactly that; do not invent `spawn_agent` parameters or a wait/resume tool. Distinguish not installed, not exposed, denied, and failed.

### C6. Checkpoint-Resume via Session Tools

Continue a matching existing worker when its role and context remain valid, using the runtime's advertised session lifecycle tools. Rehydrate repository state and pass deltas; do not reuse stale claims after a revision changes. Independent verification still needs independence, not a resumed producer recast as a critic. Release finished workers where supported and persist evidence-bound checkpoints for long work.

### C7. Sandbox / Approval Posture

Inherit the user's effective sandbox, approval, network, and managed policy. AUTORUN does not authorize editing global configuration, setting approval to never, enabling network, or removing isolation. Plan work within the grant; obtain only genuinely missing authorization for required effects. Denied work remains blocked/partial unless an authorized alternative succeeds. Apply `_common/CLI_COMPATIBILITY.md` §5; never use a bypass as an automatic retry strategy.

### C8. AGENTS.md Authority

Use Codex's applicable AGENTS.md chain and the repository's precedence rules, rather than assuming CLAUDE.md is auto-loaded. Respect nested scope and managed controls. Keep cross-tool rules in the common repository entry point and portable skill contracts.

### C9. Autonomy / Self-Driving Maximization

For an implementation assignment, execute and validate the requested result within scope. Resolve reversible uncertainty from evidence or a safe documented default; ask only for unresolved consequential choices. Follow the Completion Contract in `_common/OPERATIONAL.md`; do not append repetitive persistence/self-verification directives to every spawn. Communicate material progress and blockers proportionally—there is no universal ban on plans or status updates. After a concrete failed check, repair or diagnose; do not merely announce a follow-up.

## Per-Role Apply Matrix

Orchestrators emphasize C1/C2/C6/C7; implementation workers C4/C7/C9; independent reviewers C4/C6; skill authors C3/C5/C8. These select relevant checks, not extra workflow phases. Role boundaries remain `_common/BOUNDARIES.md`.

## Validation Hooks

- R-C1: capacity and fallback claims have actual runtime evidence.
- R-C2: independent branches can run concurrently; required results are joined and writes isolated.
- R-C3: model/effort selection uses the current Compatibility contract, available interfaces, and authorization.
- R-C4: handoffs contain the task and evidence, not duplicated methodology.
- R-C5: tool discovery precedes an absence claim where supported; no fabricated API.
- R-C6: resume preserves state validity and verification independence.
- R-C7: permission boundaries are inherited, not widened by AUTORUN.
- R-C8: applicable AGENTS.md scope and rule classes are respected.
- R-C9: implementation reaches objective validation or a concrete unresolved blocker.

Apply relevant checks and report their evidence. A tally such as “7/9” is not proof that a missing security or completion requirement is acceptable. Static review cannot certify a live Codex run.

## How to Reference This File

Reference C identifiers from a Compatibility section only when the skill actually delegates or generates a Codex runner. Shared behavior remains in the spine; vendor facts remain in `_common/CLI_COMPATIBILITY.md`.

**Lifecycle:** failure: Claude-specific tools or stale model/approval mandates leak into Codex execution; effect: evidence-based interface adaptation without relaxing boundaries; owner: compatibility maintainers; removal: when a tested shared runtime adapter supplies all C1–C9 guarantees and consumers migrate together.
