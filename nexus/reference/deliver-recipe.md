# Deliver Recipe — Scope-Adaptive Product Delivery

**Purpose:** Build and ship a product or MVP through the minimum viable specialist chain, sizing discovery, implementation, verification, and release work to the actual scope.

**Read when:** `deliver` matches, the user asks to build a product from scratch, or an MVP/product-lifecycle request is broader than one `feature` but does not justify the fixed high-investment `apex` shape.

---

## Recipe Admission Record

| Gate | Result | Evidence |
|------|--------|----------|
| Cross-boundary | PASS | Product delivery crosses discovery, implementation, verification, and release ownership. |
| Reusable orchestration value | PASS | The absorbed delivery workflow carried independent `small`, `medium`, and `epic` request shapes; all need the same scope-classification and anti-stall contract with different chain sizes. |
| No ownership overlap | PASS | `feature` owns one bounded capability; `apex` owns a high-investment discovery-to-ship run; `deliver` owns scope-adaptive product/MVP delivery. |
| Closed execution contract | PASS | Nexus owns orchestration; specialists own phase artifacts; Radar/Attest/Guardian are independent verification oracles; termination and residual routes are defined below. |

## Parameters

```yaml
scope: auto | small | medium | epic
target: <product, MVP, or release objective>
mode: build | plan-and-build | resume
release: true | false
checkpoint: .agents/nexus-delivery-state.md
```

`scope=auto` is the default. Classify with evidence from repository shape, requested outcomes, public-interface impact, and dependency breadth:

| Scope | Typical surface | Chain posture |
|-------|-----------------|---------------|
| `small` | 1-5 files, one dominant domain, no architecture migration | 3-5 specialists; skip optional discovery artifacts when evidence already exists |
| `medium` | 6-15 files or 2-3 domains, integration or public-interface change | 5-9 specialists; explicit specification and impact gates |
| `epic` | More than 15 files, multiple workstreams, migration/release coordination | 8-18 specialists; Sherpa decomposition and parallel hub-spoke branches |

File counts are evidence, not automatic permission. Safety and blast radius can raise the scope tier.

## Phase Contract

`CLASSIFY → PREFLIGHT → SHAPE → BUILD → VERIFY → RELEASE? → DELIVER`

| Phase | Nexus responsibility | Specialist ownership | Exit evidence |
|-------|----------------------|----------------------|---------------|
| CLASSIFY | Freeze target, non-goals, scope tier, and success signals | Lens/PDM may inspect current state | Delivery Intent + declared tier |
| PREFLIGHT | Reuse existing artifacts and expose blockers before implementation | Lens, Ripple, Schema/Gateway/Atlas as needed | Reuse Map + Impact Notes |
| SHAPE | Select only the chain required by the tier | Scribe/Sherpa for ACs and decomposition | Traceable ACs + bounded work packages |
| BUILD | Execute work packages through hub-spoke delegation | Builder/Artisan/Native/Scaffold and domain owners | Working artifacts; no placeholder residue |
| VERIFY | Keep producer and verifier separate | Radar, Attest, Sentinel, Voyager as applicable | Build/test/lint evidence + AC disposition |
| RELEASE | Prepare or execute release only when `release=true` and authorized | Guardian, Launch, Gear | Release evidence or an explicit release-ready handoff |
| DELIVER | Aggregate evidence and residuals | Nexus | `NEXUS_COMPLETE` + Delivery Report |

Checkpoint-resume applies: persist phase outputs to `.agents/nexus-delivery-state.md` at every boundary. `mode=resume` continues from the last valid checkpoint after revalidating repository state and permissions.

## Chain Selection

- `small`: `Lens?[reuse] → Builder/Artisan → Radar → Guardian?`
- `medium`: `Lens → Scribe/Sherpa → Ripple? → domain implementer(s) → Radar/Attest → Guardian → Launch?`
- `epic`: `Lens → Sherpa → (domain branches in parallel) → Radar/Attest/Sentinel → Guardian → Launch?`

The hub may omit an optional step only with a recorded reason and equivalent evidence. Domain methodology remains in the owning skill; this recipe owns order, handoffs, termination, and verification only.

## Anti-Stall and Recovery

Use the bounded recovery ladder from `reference/delivery-anti-stall-engine.md`: retry only after diagnosis, then narrow the work package, switch to the documented alternate owner/tool, or mark a typed residual. Two identical failures trigger diagnosis rather than a third blind retry. Do not lower acceptance criteria to preserve momentum.

Exit reasons are `ACCEPT`, `target-met`, `BLOCK`, `denied`, `invalid-state`, or `cancelled`. This is a non-loop recipe; **Termination bound: N/A** — every work package reaches a terminal state exactly once. Any non-`ACCEPT` exit reports best-so-far, the residual gap, and the named route.

## Confirm / Safety Gate

Default tier is **announce-and-proceed (no objection window)** for reversible in-scope delivery. Use **Ask First** for L4 security, destructive data work, `PUBLIC_API`/`DATA` blast radius, production release, or 10+ files when the repository rules require it. A denied gate yields `denied`; no side effect is attempted after refusal.

## Scale

3-18 specialists; relative cost Low-High by classified scope.

**Range derivation:** small `3-5`; medium `5-9`; epic `8-18`; global floor/ceiling = `min(3,5,8)` / `max(5,9,18)` = `3-18`.

## Delivery Report

Emit the base `## Nexus Execution Report` plus a named **Delivery Report**:

```markdown
## Delivery Report
- Target: <frozen target>
- Scope: <small|medium|epic> — <evidence>
- Shipped: <artifacts and behavior>
- Acceptance: <AC-ID → PASS|FAIL|UNVERIFIED + evidence>
- Verification: <commands, tests, review oracles>
- Release: <released|release-ready|not-requested|blocked>
- Exit reason: <canonical exit reason>
- Residual Ledger:
  - RES-<n>: <typed residual> → <owner/recipe> — <why it remains>
```

Done means the requested product slice works at the frozen acceptance bar, verification evidence is attached, no in-scope placeholder/TODO residue remains, and each residual has an owner and route. Implementation residuals route to `feature` or the relevant specialist; verification gaps route to Radar/Attest; release gaps route to Guardian/Launch.

## Boundaries and Decision Tree

- One bounded capability in an existing product → `feature`.
- A product/MVP build needing a chain that grows with scope → `deliver`.
- A high-investment discovery-to-ship run with a fixed deep quality loop → `apex`.
- A reusable team/work plan already exists → `enact`.

## Failure Modes Prevented

| Failure mode | Prevention |
|--------------|------------|
| Fixed heavyweight chain for a small build | Scope classification and minimum-chain selection |
| Coding before target/AC freeze | CLASSIFY and SHAPE exits |
| Orchestrator absorbing domain work | Explicit specialist ownership per phase |
| False completion after partial progress | Independent VERIFY phase and typed Residual Ledger |
| Retry loops that burn time without new evidence | Bounded anti-stall recovery ladder |
| Release side effects without authority | Ask First gate and `release` parameter |

## Shared Protocols and References

- `reference/autonomy-quality-protocol.md` — completion integrity, producer≠verifier, residual discipline.
- `_common/HANDOFF.md` — structured phase handoffs.
- `_common/PARALLEL.md` — epic hub-spoke branch ownership and merge.
- `reference/delivery-decision-matrix.md` — scope and agent-selection evidence.
- `reference/delivery-exit-criteria-validation.md` — phase exit validation.
- `reference/delivery-momentum-system.md` — momentum signals without lowering the bar.
- `reference/delivery-product-lifecycle.md` — lifecycle phase detail loaded only when the selected scope needs it.
