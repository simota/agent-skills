# Workflow Design

**Purpose:** How to design a project workflow/chain that coordinates multiple agents under a formal topology.
**Read when:** You are in the `workflow` mode or designing the workflow set inside a blueprint.

## Contents
- Recipe vs Workflow
- Formal topology (mandatory)
- The 5-phase ceiling
- Parallelism layer choice
- Boundaries: Orbit, Weave, Nexus
- Worked example
- Anti-patterns

---

## Recipe vs Workflow

| | Recipe | Workflow |
|--|--------|----------|
| Coordination | Linear chain, light | Multi-agent, may fan out/converge |
| Topology | Implicit sequence | **Explicit & formal** (required) |
| Branching | A few decision points | Genuine branching / parallelism |
| When | Straight chain, no fan-out (any length) | Any branching, fan-out, or convergence |

The discriminator is **shape, not step count**. If the task is a straight chain, design it as a recipe (`recipe-design.md`) regardless of length. Promote to a workflow the moment coordination, branching, or fan-out is real — even below 5 steps.

---

## Formal topology (mandatory)

Every workflow Sigil[blueprint] designs MUST declare one topology. Unstructured flat peer networks ("Bag of Agents") amplify errors and never ship.

| Topology | Shape | Use when |
|----------|-------|----------|
| Hub-and-spoke | One orchestrator delegates to specialists, gathers results | Default; most project workflows. `≤ 7` spokes per hub |
| Pipeline | Output of stage N feeds stage N+1 | Linear transformation with clear stage boundaries |
| Hierarchy | Orchestrator → sub-orchestrators → specialists | `> 7` specialists, or grouped sub-domains |

Scaling rules:
- Beyond `4` coordinating agents, coordination tax dominates without structure — use hierarchy or pipeline, not flat peers.
- Beyond `7` spokes on one hub, split into a two-level hierarchy.
- Justify multi-agent at all: only when single-agent performance is `< 45%` on the task. Above that, sharpen the single skill first (note this in the blueprint).

In this ecosystem the runtime hub is `Nexus`. A project workflow Sigil[blueprint] designs is registered with Nexus, which acts as the hub at execution time. Sigil[blueprint] declares the topology; Nexus runs it.

---

## The 5-phase ceiling

Cap every workflow at `≤ 5` sequential phases. Per-step accuracy compounds: `0.85^10 ≈ 0.20` end-to-end. Each phase boundary should carry a verification checkpoint that resets the accuracy baseline.

If a workflow needs more than 5 phases:
- Split it into two workflows with a handoff, or
- Collapse adjacent phases owned by the same agent, or
- Move detail down into the owning skill so the phase count drops.

Declare `phases: <int>` for every workflow; VERIFY rejects `> 5`.

---

## Parallelism layer choice

Refer to `_common/SUBAGENT.md`. Summary:

| Need | Layer |
|------|-------|
| 2-3 independent subtasks in one session, read-mostly | Skill-internal subagents (spawn in one turn) |
| 4+ workers, cross-session, file-ownership isolation, parallel writes | Agent Teams |

State the parallelism layer in the workflow spec. For independent subtasks, spell out the explicit "spawn N subagents in the same turn when…" trigger so the runtime fans out instead of serializing.

---

## Boundaries: Orbit, Weave, Nexus

- **Loop needed** (the workflow runs itself repeatedly toward a goal until a condition): Sigil[blueprint] specs the loop and hands it to `Orbit`. Sigil[blueprint] does not build the runner.
- **Code-level state machine / saga** (states, transitions, compensation in the application): that is `Weave`'s domain. Sigil[blueprint] does not design state machines; it may reference one a workflow depends on.
- **Runtime routing** of the workflow per request: `Nexus`. Sigil[blueprint] designs the persistent definition; Nexus executes.

---

## Worked example

`release-train` workflow. SURVEY found a monthly release that fans out across packages then converges.

```yaml
workflow:
  name: release-train
  outcome: "Tagged release with changelog and notes across all packages"
  topology: hub-spoke           # Nexus is the hub at runtime
  parallelism: agent-teams      # parallel per-package collection, isolated
  phases:                       # 4 <= 5
    - collect:  owner: launch    # gather merged PRs per package (parallel spokes)
    - version:  owner: launch     # compute version bumps; checkpoint: semver valid
    - changelog: owner: launch    # generate changelog + notes; checkpoint: user-confirm
    - verify:   owner: guardian   # tag + final gate; checkpoint: clean tree
  loop: none                    # one-shot; if "release nightly" → defer to Orbit
  delegations:
    - to: Nexus   payload: workflow definition + topology
    - to: Launch  payload: versioning + changelog ownership (ecosystem agent — route, don't duplicate)
```

---

## Anti-patterns

- **No topology.** A workflow without a declared hub-spoke/pipeline/hierarchy is a Bag of Agents — rejected.
- **> 5 phases.** Accuracy collapse; split or collapse.
- **Multi-agent for a `> 45%` single-agent task.** Coordination overhead unjustified; improve the single skill.
- **Building the loop/state-machine inline.** Defer loops to Orbit, state machines to Weave.
- **Flat peer network beyond 4 agents.** Use hierarchy or pipeline.
