# Multi-Agent Anti-Patterns & Failure Modes

> Purpose: Read this when checking whether Rally is a bad fit, diagnosing coordination failures, or setting safe limits for a team session.

## Table of Contents

1. Failure Taxonomy
2. Over-Parallelization Signals
3. Anti-Patterns
4. Maker-Checker Rules
5. Rally Checklist

## Failure Taxonomy

System design failures are common in multi-agent work. Treat coordination and scope as first-class risks, not prompt-tuning problems.

| Category | Failure mode | Symptom | Rally safeguard |
|----------|--------------|---------|-----------------|
| System design | ambiguous roles | teammates drift into each other's work | clear boundaries + `exclusive_write` |
| System design | bad state management | loops or long stalls | checkpoints + timeouts |
| System design | incompatible outputs | synthesis breaks | shared interfaces in `shared_read` |
| Inter-agent mismatch | context reset | teammate loses assumptions | re-inject context |
| Inter-agent mismatch | wrong assumptions continue | silent divergence | explicit reports + verification |
| Inter-agent mismatch | context drift | contradictory outputs | semantic contracts |
| Verification failure | repeated completed steps | looped execution | mark completion via `TaskUpdate` |
| Verification failure | hallucination propagation | bad upstream facts spread downstream | cross-check and source verification |

## Over-Parallelization Signals

| Signal | Meaning |
|--------|---------|
| Team completion is slower than a single agent | coordination overhead dominates |
| Message count exceeds `3 x` task count | communication is excessive |
| Ownership conflicts recur | partitioning is too weak |
| Integration consumes `> 50%` of total effort | parallelism is too expensive |

Reference impact:
- parallelizable tasks can improve by about `+81%`
- sequentially dependent tasks can degrade by about `-70%`

## Anti-Patterns

### Design Anti-Patterns

| Anti-pattern | Symptom | Countermeasure |
|--------------|---------|----------------|
| Over-agenting | simple work gets too many agents | start with one agent or a smaller team |
| Ambiguous roles | multiple agents act as the same specialist | separate role, scope, and ownership |
| Unlimited autonomy | loops or cost blow-up | set iteration and cost limits |
| Nested teams | recursive `TeamCreate` | enforce one team per session |
| Wrong framework choice | Rally used for non-parallel work | route by requirement, not trend |

### Communication Anti-Patterns

| Anti-pattern | Symptom | Countermeasure |
|--------------|---------|----------------|
| Broadcast overuse | noisy, expensive updates | DM by default |
| Excess context transfer | teammates receive full history | pass only necessary context |
| Hidden decisions | black-box coordination | use `TaskList`, reports, and explicit summaries |
| Human overtrust | recommendations accepted blindly | keep HITL checkpoints |

### Agent Teams-Specific Anti-Patterns

| Anti-pattern | Example | Countermeasure |
|--------------|---------|----------------|
| Ambiguous spawn prompt | "Build the app" | include API, conventions, goal, and ownership |
| Same-file writes | two teammates edit `index.ts` | define `exclusive_write` first |
| Team on sequential work | staged dependency chain | keep it in one session or pipeline |
| Nested team creation | teammate opens another team | one session, one team |
| Idle treated as failure | unnecessary intervention | `idle` is normal waiting |
| `TeamDelete` without shutdown | active members remain | shutdown all teammates first |

## Maker-Checker Rules

1. Give the checker explicit pass or fail criteria.
2. Set a maximum iteration cap.
3. Define a fallback once the cap is reached.
4. Keep the checker simpler and more reliable than the maker.

## Rally Checklist

- [ ] Is the task truly parallelizable?
- [ ] Are there at least `2` independent work units?
- [ ] Is `ownership_map` conflict-free?
- [ ] Is team size minimal (`2-4` preferred)?
- [ ] Does every spawn prompt include enough context?
- [ ] Are timeout or retry limits defined?
- [ ] Are synthesis verification criteria explicit?
