# Product Lifecycle — L/XL Phase Reference

Purpose: Read this file when Nexus[deliver] classifies work as `L` or `XL`, chooses lifecycle phases, or needs the exact phase chain and shortcut rules.

## Contents

- Scope detection
- Quick reference
- L scope phases
- XL scope additions
- Phase execution pattern
- Nexus chain format
- Agent justification shortcuts

```
DISCOVER → DEFINE → ARCHITECT → BUILD → HARDEN → VALIDATE → LAUNCH → GROW → EVOLVE
```

**S/M scopes use single chains defined in SKILL.md. This file covers L/XL scope phase execution only.**

---

## Scope Detection

```
file_count = estimated files to create/modify
  1-5   → S (just build — see SKILL.md)
  6-15  → M (understand then build — see SKILL.md)
  16-30 → L (phased delivery — this file)
  31+   → XL (full lifecycle — this file)
confidence < 0.60 → Lens codebase analysis first, then re-evaluate
```

## Quick Reference

| Scope | DISCOVER | DEFINE | ARCHITECT | BUILD | HARDEN | VALIDATE | LAUNCH | GROW | EVOLVE |
|-------|----------|--------|-----------|-------|--------|----------|--------|------|--------|
| **L** | Nexus→Lens→Scribe[unified] | Spark→Scribe | Magi→Atlas→Schema→Grove | Sherpa→Rally→Radar | Full | Full | Full | SKIP | SKIP |
| **XL** | Full 8-agent | Full 6-agent | Full 7-agent | Full Rally | Full | Full | Full | Full | Full |

---

## L Scope Phases

### DISCOVER (L)
```
Chain: Nexus → Lens → Scribe[unified]
Acceptance: Product definition with features, constraints, integration points
Artifacts: `docs/product-definition.md`
```

### DEFINE (L)
```
Chain: Spark → Scribe
Acceptance: Roadmap with prioritized features, SUCCESS_CRITERIA defined
Artifacts: `docs/roadmap.md`
```

### ARCHITECT (L)
```
Chain: Magi → Atlas → Schema → Grove
Acceptance: ADR for key decisions, DB schema, repo structure
Artifacts: ADRs, schema files
```

### BUILD (L) — Core Phase
```
Chain: Sherpa → Rally{feature teams} → Radar
Rally: Team{ Feature A: Builder→Radar | Feature B: Artisan→Radar | ... }
Acceptance: All features implemented, integration tests passing
Artifacts: Source code + test files
```

### HARDEN (L)
```
Chain: Rally{Sentinel+Probe} → Judge → Zen → Bolt
Acceptance: Security audit pass, code quality ≥B, perf targets met
```

### VALIDATE (L)
```
Chain: Rally{Voyager+Radar} → Echo
Acceptance: E2E passing, UX validated, quality gate approved
```

### LAUNCH (L)
```
Chain: Quill → Guardian → Launch → Gear
Acceptance: Docs updated, PR ready, CHANGELOG written, CI configured
```

---

## XL Scope Additions

XL scope includes all L phases plus GROW and EVOLVE, and expands each phase with additional agents. **Apply Agent Justification Gate from SKILL.md before deploying any additional agent.**

### DISCOVER (XL additions)
Add: Field (personas), Compete (SWOT), Voice (feedback), Scout (issues), Triage (incidents)
```
Chain: Nexus → Scribe[unified] → Field → Compete → Voice → Lens
```

### DEFINE (XL additions)
Add: Pulse (KPIs), Magi (Go/No-Go), Canon (standards), Ripple (impact)
```
Chain: Spark → Scribe → Pulse → Magi → Canon
```

### ARCHITECT (XL additions)
Add: Gateway (API), Scaffold (infra), Canvas (diagrams)
```
Chain: Magi → Atlas → Gateway → Schema → Grove → Scaffold → Canvas
```

### BUILD (XL additions)
Add: Forge (prototypes), Stream (data), Builder (CLI)
```
Rally teams by domain: Frontend(Artisan) | Backend(Builder) | Data(Stream) | CLI(Builder)
```

### HARDEN (XL additions)
Add: Tuner (DB perf), Judge (PDCA), Canon (compliance)
```
Chain: Rally{Sentinel+Probe} → Judge → Zen → Rally{Bolt+Tuner} → Judge → Canon
```

### VALIDATE (XL additions)
Add: Trace (session analysis), Experiment (A/B), Vector (browser)
```
Chain: Rally{Voyager+Radar} → Echo → Trace → Experiment → Vector
```

### LAUNCH (XL additions)
Add: Canvas (diagrams), Scribe (conversion), Rally{Vitrine+Cue} (demos)
```
Chain: Quill → Canvas → Guardian → Launch → Rally{Vitrine+Cue} → Gear
```

### GROW (XL only)
```
Chain: Growth → Pulse → Stream → Experiment
Purpose: SEO/CRO, retention, i18n, analytics, growth experiments
```

### EVOLVE (XL only)
```
Chain: Voice → Ripple → Sweep → Shift (`detect`/`radar`) → Gear → Trail
Purpose: Feedback-driven improvement, feeds back to DISCOVER
```

---

## Phase Execution Pattern

```
Phase N:
  1. Generate Epics from this document + scope
  2. Run Agent Justification Gate per agent
  3. Independent Epics → Rally (parallel) · Sequential → Nexus AUTORUN_FULL
  4. Update NEXUS_DELIVERY_STATE on each completion
  5. Exit ≥80% → next phase · 60-79% → reduce scope + proceed · <60% → Anti-Stall
```

## Nexus Chain Format

```
## NEXUS_AUTORUN_FULL
Task: [Phase objective]
Chain: [Agent chain]
Context: [What agents need to know]
Acceptance: [Measurable criteria]
```

On `NEXUS_COMPLETE`: SUCCESS → next Epic · PARTIAL → L1 retry · BLOCKED → L2 skip · FAILED → L1 agent swap

## Agent Justification Shortcuts (L scope)

| Phase | Often Skipped | Reason |
|-------|--------------|--------|
| DISCOVER | Field, Compete, Voice | L scope knows its users |
| DEFINE | Pulse, Canon | KPIs and standards optional at L |
| ARCHITECT | Scaffold, Canvas | Infra and diagrams are XL concerns |
| VALIDATE | Trace, Experiment | Session analysis/A/B are XL |
| LAUNCH | Scribe, Vitrine, Cue | Multiple demo formats are XL |

Full agent × phase deployment map → `reference/delivery-agent-deployment-matrix.md`
Phase exit checklists → `reference/delivery-exit-criteria-validation.md`
