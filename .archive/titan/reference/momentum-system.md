# Momentum System

Purpose: Read this file when Titan must prove forward progress, score cycle output, validate velocity, or decide whether Rally is justified.

## Contents

- Forward progress guarantee
- Weighted progress score
- Velocity metrics
- Parallel execution rules
- Epic prioritization
- Never idle principle
- Phase transition momentum

Velocity tracking and forward progress guarantee for Titan.

---

## Forward Progress Guarantee

Every execution cycle MUST produce at least one tangible artifact:

| Artifact Type | Examples |
|--------------|---------|
| File change | Code, config, test, documentation |
| Test addition | New test case, coverage improvement |
| Decision record | Entry in Decision Log |
| Document generation | Spec, diagram, report, README |

**Zero-Progress Detection**: 2 consecutive zero-artifact cycles → Anti-Stall Engine activates.
**Cycle Definition**: One Nexus AUTORUN_FULL chain execution or one Rally team completion.

### Weighted Progress Score

Not all artifacts contribute equally to forward progress. Use weighted scoring to distinguish meaningful progress from trivial updates.

| Artifact Type | Weight | Examples |
|--------------|--------|---------|
| Core Implementation | 1.0 | Feature code, critical bug fix, API endpoint |
| Test Addition | 0.7 | New test suite, significant coverage improvement |
| Architecture Decision | 0.5 | ADR entry, schema design, API spec |
| Configuration Change | 0.3 | Build config, CI pipeline, environment setup |
| Documentation Update | 0.3 | README, API docs, user guide |
| Decision Log Entry | 0.1 | Decision record, risk assessment |
| Minor Update | 0.1 | Comment addition, formatting, trivial fix |

**Meaningful Progress Threshold**: A cycle's weighted score must reach **≥0.3** to count as progress. Below 0.3, the cycle is treated as zero-progress for Anti-Stall detection purposes.

**Example**: A cycle that only adds a Decision Log entry (0.1) = zero-progress. A cycle that adds a test (0.7) = meaningful progress. A cycle with config change (0.3) = threshold met.

---

## Velocity Metrics

| Metric | Calculation | Healthy | Warning | Critical |
|--------|------------|---------|---------|----------|
| Epic completion rate | completed / planned × 100% | ≥70% | 50-69% | <50% |
| Cycle time per Epic | actual / estimated | ≤1.2x | 1.2-2x | >2x |
| Stall frequency | stalls / total_cycles × 100% | ≤10% | 10-25% | >25% |
| Agent success rate | successful / total_calls × 100% | ≥80% | 60-79% | <60% |

**Actions**: Healthy → continue · Warning → log, increase monitoring · Critical (1 metric) → Sherpa re-decomposition · Critical (2+) → Anti-Stall Engine L2+.

---

## Parallel Execution Rules

### Rally Auto-Launch Conditions

Rally is automatically invoked when:
1. **Independent Epics**: 2+ Epics with no shared file dependencies
2. **Domain separation**: 2+ technical domains (frontend, backend, infra)
3. **Sherpa parallel_group**: Sherpa marks tasks as parallelizable
4. **Phase pattern**: Phase naturally supports parallelism (HARDEN, VALIDATE, LAUNCH)

### Rally Sizing

| Phase | Typical Teams | Reason |
|-------|--------------|--------|
| BUILD | 2-4 | Feature parallelism |
| HARDEN | 3 | Security + Performance + Quality |
| VALIDATE | 2 | E2E tests + Unit tests |
| LAUNCH | 3 | Docs + Demos + CI/CD |

### File Ownership Protocol

When Rally is active, assign explicit file ownership per team. No two teams write to the same file. Shared dependencies resolved before launch. Integration managed by Titan after Rally completion.

---

## Epic Prioritization

| Priority | Criteria | Action |
|----------|----------|--------|
| **1. Impact/Effort** | High impact + Low effort | Schedule first |
| **2. Unblocking** | Completes → unblocks 3+ Epics | Boost priority |
| **3. Risk Reduction** | Addresses highest-risk item or validates critical assumption | Boost priority |
| **4. User Visibility** | Shows tangible user-facing progress | Boost priority |

**Quick Wins**: Schedule ≥1 quick win at phase start (completable in single Nexus chain, 1-3 agents). Builds momentum and provides early validation.

---

## Never Idle Principle

If primary path is blocked: Check other Epics in phase → Pre-work for next phase → Address tech debt (Sweep/Zen) → Update docs/diagrams → Add test coverage. Never report "waiting" without actively working.

---

## Phase Transition Momentum

At phase boundaries: Begin next phase prep while current wraps up · Run exit criteria checklist systematically · Carry barely-missed items to next phase as high-priority · Log 2-3 sentence retrospective to journal.
