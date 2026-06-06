# Context Switching & Flow State Anti-Patterns

Purpose: Use this file when Sherpa needs hard rules for WIP limits, focus protection, pacing, or context-switch cost.

## Contents

- `CS-01` to `CS-07`
- switch-cost statistics
- flow protection
- WIP limits
- pacing-mode integration

## Anti-Patterns

| ID | Anti-pattern | Symptom | Preferred fix |
| --- | --- | --- | --- |
| `CS-01` | No WIP Limit | many in-progress tasks, few completions | keep WIP at `1-2` tasks/person |
| `CS-02` | Interrupt Culture | constant chat, mentions, or meetings | use asynchronous communication and focus blocks |
| `CS-03` | Multi-Project Juggling | `3+` projects in parallel destroy throughput | prefer one project, cap at two when possible |
| `CS-04` | Review Delay Loop | review wait time spawns unrelated new work | reserve review blocks and return quickly |
| `CS-05` | Tool Fragmentation | heavy app switching and search time | consolidate context and colocate docs |
| `CS-06` | Firefighting Addiction | frequent incidents kill planned work | use rotations and invest in root-cause fixes |
| `CS-07` | Meeting Fragmentation | no uninterrupted block remains | batch meetings and protect meeting-free time |

## Switch-Cost Data

```text
Reference costs (human deep-focus recovery):
- full recovery to deep focus: ~23m 15s
- cognitive hit per switch: ~20%
- same codebase switch: ~5-10 min
- different-domain switch: ~30-60 min
Note: For AI-agent practical switch costs (~3-12 min), see emergency-protocols.md.

Project load impact:
1 project -> 100% productive time
2 projects -> 80%
3 projects -> 55%
4 projects -> 35%
5 projects -> 15%
```

## Flow Protection

```text
Protect flow with:
1. a 2-hour focus block
2. notification control
3. urgency-based communication channels
4. visible "in focus" signals
5. batched message handling
```

## WIP Limit Rules

```text
Principle:
Lead time = WIP / Throughput

Practical limits:
- individual: 1-2 in-progress tasks
- team columns: explicit WIP caps
- expedite lane: reserve 1 slot for real emergencies
```

## Pacing Modes

| Mode | WIP | Interruptions | Step size | Use when |
| --- | --- | --- | --- | --- |
| Sprint | `1` | blocked | `10-15 min` | deep focus, deadline pressure |
| Cruise | `1-2` | batched | normal | standard work |
| Recovery | `1` | tolerated | `5-10 min` | after blockers or breaks |
| Wind-down | finish only | tolerated | smallest | session end |

## Quality Gates

```text
- multiple concurrent steps -> apply WIP limit
- interruption-driven drift -> use Parking Lot
- 3+ projects in parallel -> move to Base Camp prioritization
- session > 3h -> suggest break or Wind-down
```
