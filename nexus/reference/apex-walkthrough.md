# Nexus Apex Walkthrough — Visualising the Workflow and What Happens

**Purpose:** Human-facing document that illustrates, phase by phase, what happens when `/nexus apex` runs — which agent produces what, where the workflow stops or branches, and how to read the topology.
**Read when:** First-time apex users, when explaining the recipe to a team, when reviewing per-phase responsibilities, or when locating "where am I now?" during trouble.
**Companion:** The technical contract is in `apex-recipe.md`; this document is its narrative visualisation.

---

## 1. End-to-end Overview

```mermaid
flowchart TD
    USER([👤 User])
    USER -->|goal supplied| P1
    USER -->|no args / goal=auto| P0
    P0[Phase 0<br/>Bootstrap — autonomous goal discovery<br/>project_scan + spark + rank<br/>+ voice/pulse/compete/sage/magi]
    P0 --> CONFIRM{🚦 Boundary Confirm<br/>AUTORUN_FULL: 60s objection window<br/>others: explicit confirm}
    CONFIRM -->|approve or 60s timeout| P1
    CONFIRM -->|reject| ABORT[❌ Abort or<br/>suggest re-launch with explicit goal]
    P1[Phase 1<br/>Discovery<br/>plea + field + echo?] --> P2
    P2[Phase 2<br/>Ideate<br/>riff] --> P3
    P3{Phase 3<br/>Verdict<br/>magi}
    P3 -->|Go| P4
    P3 -->|Split 1-1-1| HUMAN1[👤 Human Review]
    HUMAN1 --> P3
    P4[Phase 4<br/>Spec<br/>accord +void? +scribe?] --> P5
    P5[Phase 5<br/>Design + Risk Gate<br/>parallel: Tech ‖ UX]
    P5 --> GATE{Risk Gate<br/>omen + ripple + echo}
    GATE -->|Go| P6
    GATE -->|No-Go| P4
    P6[Phase 6<br/>Implementation Loop<br/>orbit drives builder/artisan/judge/radar/voyager] --> SHIP
    P6 -->|Stuck/Budget| TRIAGE[🚨 Triage]
    SHIP[Ship<br/>guardian → launch] --> DONE([✅ Feature released])

    style USER fill:#e1f5ff
    style DONE fill:#d4edda
    style HUMAN1 fill:#fff3cd
    style TRIAGE fill:#f8d7da
    style GATE fill:#fff3cd
    style P3 fill:#fff3cd
```

**Colour legend**: 🟦 entry / 🟩 done / 🟨 decision gate / 🟥 escalation

---

## 3. Failure and Rollback Flow

```mermaid
stateDiagram-v2
    [*] --> Phase1
    Phase1 --> Phase2
    Phase2 --> Phase3
    Phase3 --> Phase4: Verdict OK
    Phase3 --> HumanReview: Split decision
    HumanReview --> Phase3
    Phase4 --> Phase5
    Phase5 --> Phase6: Risk Gate Pass
    Phase5 --> Phase4: traceability < threshold
    Phase5 --> Phase4: fatal plea-echo divergence
    Phase5 --> Phase5_UX: echo NG
    Phase5_UX: in-Phase 5 UX fix
    Phase5_UX --> Phase5
    Phase6 --> Ship: all AC satisfied
    Phase6 --> Triage: Stuck Loop
    Phase6 --> HumanBudget: Budget exceeded
    HumanBudget --> Phase6: continue approved
    HumanBudget --> [*]: abort
    Triage --> Phase4: spec-rooted cause
    Triage --> Phase6: implementation-rooted cause
    Ship --> [*]
```

---

## 4. Two-tier Hub Topology

```mermaid
flowchart TB
    USER([👤 User]) --> NEXUS

    subgraph TOP[Top hub: Nexus]
        NEXUS{Nexus}
    end

    NEXUS -.Phase 1.-> PL[plea]
    NEXUS -.Phase 1.-> RE[field]
    NEXUS -.Phase 1.-> EC[echo]
    NEXUS -.Phase 2.-> RI[riff]
    NEXUS -.Phase 3.-> MA[magi]
    NEXUS -.Phase 4.-> AC[accord]
    NEXUS -.Phase 5 Tech.-> AT[atlas]
    NEXUS -.Phase 5 UX.-> VISION
    NEXUS -.Phase 5 Gate.-> GATE[omen+ripple+echo]
    NEXUS -.Phase 6.-> ORBIT
    NEXUS -.Ship.-> GU[guardian]
    NEXUS -.Ship.-> LA[launch]

    subgraph UXHUB[UX sub-hub: Vision]
        VISION{Vision}
        VISION --> MU[muse]
        VISION --> PA[palette]
        VISION --> PR[prose]
        VISION --> FL[flow]
        VISION --> FR[frame]
        VISION --> FO[forge]
        VISION --> EC2[echo<br/>walkthrough]
    end

    subgraph LOOPHUB[Loop sub-hub: Orbit — engine = Codex CLI]
        ORBIT{Orbit<br/>spawn parent}
        ORBIT -.spawn_agent.-> BU[builder]
        ORBIT -.spawn_agent.-> AR[artisan]
        ORBIT -.spawn_agent.-> SH[vitrine]
        ORBIT -.spawn_agent.-> JU[judge]
        ORBIT -.spawn_agent.-> RA[radar]
        ORBIT -.spawn_agent.-> VO[voyager]
    end

    style NEXUS fill:#cfe2ff
    style VISION fill:#f8d7da
    style ORBIT fill:#d1ecf1
    style LOOPHUB fill:#fef3e8
```

**Design rationale**: top-level Nexus directly fans out to ~10 agents only; the 9 UX agents hide under Vision and the 6 loop agents hide under Orbit. This preserves the "specialists ≤ 7-10 per orchestrator" principle. **Furthermore, LOOPHUB executes on Codex CLI and is fully isolated from the Claude Code session's context budget.**

---

## 5. Time and Cost Profile

| Profile | Agent count | Time estimate | Cost estimate | Use case |
|---|---|---|---|---|
| **Lite** | 8-10 | 60-90 min | Low | Backend-only feature, accord=Lite |
| **Standard** | 14-18 | 2-3 hours | Medium | Typical UI-bearing feature |
| **Full** | 20-25 | 3-5 hours | High | Greenfield, accord=Full, Figma integration, multi-locale |
| **+Phase 0 (autonomous mode)** | +4-8 | +15-25 min | +10-20% | Goal also auto-selected when launched with no args |

> Note: times depend on network and model latency. Each phase has a verification gate, so this is **total elapsed time**, not the bandwidth of parallel processing.

---

## 6. What Remains as Artefacts

```mermaid
flowchart LR
    subgraph PHASES[Per-phase artefacts]
        D1[Phase 1<br/>demand list +<br/>persona evidence]
        D2[Phase 2<br/>session summary]
        D3[Phase 3<br/>verdict +<br/>AC seed]
        D4[Phase 4<br/>L0-L3 spec +<br/>traceability]
        D5[Phase 5<br/>ADR + OpenAPI +<br/>schema + tokens +<br/>prototype + walkthrough]
        D6[Phase 6<br/>working code +<br/>tests + stories]
        D7[Ship<br/>PR + CHANGELOG +<br/>rollback plan]
    end
    USER([User]) --> ALL[All artefacts<br/>retained in auditable form]
    PHASES --> ALL
```

**Primary artefacts that persist after implementation**:
- `docs/specs/<feature>.md` (accord)
- `docs/adr/ADR-NNNN.md` (atlas)
- `docs/api/openapi.yaml` (gateway)
- `docs/design/tokens.json` (muse)
- Storybook (vitrine)
- E2E persona scenarios (voyager)
- Release notes + rollback procedure (launch)

All of these are auto-generated as apex by-products, so what remains is not just **"working code"** but **"explainable functionality"**.

---

## 7. Invocation Examples (copy-pasteable)

> Invocation forms (autonomous no-args, goal-supplied, mode overrides) are listed in `apex-recipe.md` / `nexus/SKILL.md` § Subcommand Dispatch. This section keeps only the interruption-handling demo, which is walkthrough-specific.

### Stopping mid-flight

```bash
# In autonomous mode, any input within the 60s window stops immediately
> /nexus apex
... Proposal: "fine-grained notification controls" ... stop within 60s by typing anything
> stop                    # ← any input aborts
Aborted. To choose differently:
  /nexus apex specify a different goal directly
```

After execution, Nexus returns a `## Nexus Execution Report` with the Phase 0 selection log plus Status / Output / Handoff for Phases 1-6. In autonomous mode, the rationale for `auto_selected_goal` and its `rejected_alternatives` are also persisted, so "why we did not pick a different feature" remains auditable.
