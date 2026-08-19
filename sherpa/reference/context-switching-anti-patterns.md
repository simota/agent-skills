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
## Pacing Modes
| Mode | WIP | Interruptions | Step size | Use when |
| --- | --- | --- | --- | --- |
| Sprint | `1` | blocked | `10-15 min` | deep focus, deadline pressure |
| Cruise | `1-2` | batched | normal | standard work |
| Recovery | `1` | tolerated | `5-10 min` | after blockers or breaks |
| Wind-down | finish only | tolerated | smallest | session end |
