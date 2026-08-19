# Scope Creep & Execution Anti-Patterns
Purpose: Use this file when active execution is expanding, interruptions are piling up, or pace is becoming unsustainable.
## Contents
- `SC-01` to `SC-07`
- execution-phase traps
- sustainable pace rules
- scope defense checklist
- interruption classes
## Scope-Creep Anti-Patterns
| ID | Anti-pattern | Symptom | Preferred fix |
| --- | --- | --- | --- |
| `SC-01` | Maverick Addition | work enters the sprint without team agreement | require explicit plan update or backlog entry |
| `SC-02` | Scope Creep via "Quick Fix" | “small” extras appear repeatedly | apply the `2 min` rule and Parking Lot |
| `SC-03` | Stakeholder Bypass | work is requested directly to developers | route requests through the backlog or owner |
| `SC-04` | Gold-Plating | work exceeds acceptance criteria | enforce Definition of Done |
| `SC-05` | Emergency Inflation | routine work abuses the urgent lane | classify interrupts strictly |
| `SC-06` | Acceptance Criteria Drift | success criteria change mid-execution | require agreement plus re-estimation |
| `SC-07` | Perfectionism Trap | work never reaches “done” | use MVP / good-enough criteria |
## Execution-Phase Traps
| Trap | Symptom | Response |
| --- | --- | --- |
| Board Out-of-Date | board does not reflect real status | update the board continuously |
| No Flow to Done | everything stays open until the end | finish one slice at a time |
| Absent Owner | needed decisions go unanswered | secure owner availability or decision rules |
| Delayed Feedback | review happens too late | review completed work immediately |
| Lack of Support | silent struggle lasts `30+ min` | trigger stalled detection |
| Team Reassignment | members are moved mid-stream | protect team continuity during the timebox |
## Interruption Classes
| Priority | Meaning | Response |
| --- | --- | --- |
| `P0` | production incident or data-loss risk | interrupt immediately, trigger `Triage` |
| `P1` | serious bug, same-day response needed | finish current step, then switch |
| `P2` | improvement or debt | Parking Lot / backlog |
| `P3` | information or FYI | batch asynchronously |
