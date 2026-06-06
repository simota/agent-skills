# Emergency Protocols & Base Camp

Purpose: Use this file when work is slipping into emergency conditions, when multi-Epic coordination is needed, or when context-switch cost must be made explicit.

## Contents

- Emergency levels
- Yellow, Red, and Evacuation protocols
- Recovery checkpoint
- Base Camp dashboard
- Context-switch protocol

## Emergency Levels

| Level | Condition | Response |
| --- | --- | --- |
| Yellow Alert | `1-2` major blockers, falling behind | reassess plan, cut scope, or add support |
| Red Alert | critical path blocked, deadline at risk | stop and invoke `Triage` |
| Evacuation | cascading failures, project integrity at risk | full stop, stabilize first |

## Yellow Alert

```markdown
## Yellow Alert

**Triggered by**:
- velocity ~40% below estimate
- 2 blockers identified
- projected completion ~2x original estimate

### Options
1. Scope Cut (Recommended)
2. Request Reinforcements
3. Extend Timeline
4. Push Through

### Immediate Actions
1. Commit current progress
2. Document blockers
3. Choose the response strategy
```

## Red Alert

```markdown
## Red Alert

**Triggered by**: critical blocker, cannot proceed

### Emergency Actions
1. Stop dependent work
2. Document current state
3. Commit all progress clearly
4. Communicate to stakeholders
5. Pivot to valid unblocked work if available

### Invoking Triage
/Triage assess current situation
Context: [Epic] blocked by [blocker]
Impact: [N] steps blocked
Need: prioritized recovery options
```

## Evacuation Protocol

```markdown
## Evacuation Protocol

### Immediate Actions
1. STOP ALL WORK
2. SECURE CURRENT STATE
   git stash
   git status
   git log -5
3. DOCUMENT EVERYTHING
4. INVOKE TRIAGE
5. COMMUNICATE

### Do NOT
- make hasty fixes
- delete anything
- hide the problem
- continue other work until stable
```

## Recovery Checkpoint

```markdown
## Recovery Checkpoint

**Emergency**: [Description]
**Resolution**: [What fixed it]
**Duration**: [How long it took]

### Post-Mortem Notes
- Root cause
- Warning signs missed
- Prevention

### Plan Adjustments
- [ ] Re-estimate remaining steps
- [ ] Update risk assessments
- [ ] Add monitoring or checks
- [ ] Document in project journal
```

## Base Camp

```markdown
## Base Camp

**Date**: YYYY-MM-DD
**Session Duration**: Xh Ym
**Total Steps Today**: N completed

### Active Expeditions
| Epic | Progress | Status | Priority | Last Touch |
|------|----------|--------|----------|------------|
| Payment Flow | 40% | Active | P0 | Now |
| User Settings | 25% | Paused | P1 | 2h ago |
| Bug #123 | 0% | Queued | P2 | - |
```

### Priority Matrix

| Priority | Meaning |
| --- | --- |
| `P0 - Summit` | blocking others or due today |
| `P1 - High Camp` | important this week |
| `P2 - Base Camp` | useful, flexible timing |
| `P3 - Queue` | nice to have |

## Context-Switch Protocol

```markdown
## Context Switch Request

**Current**: [Epic A] (Step X/Y, Z% complete)
**Target**: [Epic B]

### Switch Assessment
| Factor | Value |
|--------|-------|
| Current step completion | 60% |
| Context switch cost | ~8 minutes |
| Priority comparison | P0 -> P1 |
| Momentum loss | High |

### Recommendation
Finish the current step first when possible.
```

### Context-Switch Cost Reference

These are practical AI-agent context-switch costs. For human deep-focus recovery costs (~23 min), see `context-switching-anti-patterns.md`.

| From -> To | Estimated cost | Why |
| --- | --- | --- |
| Same domain | `~3 min` | context is still warm |
| Different domain | `~8 min` | mental model rebuild needed |
| After a long break | `~12 min` | review required |
