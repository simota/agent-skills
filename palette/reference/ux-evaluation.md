# UX Evaluation Reference

Purpose: Provide the canonical heuristic, SUS, and before/after report formats for Palette.

## Contents

Note: See also `wcag22-inclusive-design.md` for WCAG 3.0 preview, Popover API patterns, and Calm UI evaluation.

### Inclusive Design Beyond WCAG

| Dimension | Need | Design Response |
|-----------|------|----------------|
| Neurodivergent (ADHD) | Focus fragmentation, executive function load | Reduce parallel stimuli, single-task flows, clear next-action indicators |
| Neurodivergent (Autism) | Sensory overwhelm, routine disruption | Predictable layouts, muted palettes, explicit state changes (not implied) |
| Aging (65+) | Reduced contrast sensitivity, motor precision | 48px+ touch targets, high contrast, larger body text (18px+), simple navigation |
| Low Literacy | Reading difficulty | Icon-led UI, short sentences (grade 6 reading level), progressive disclosure |
| Cultural | Left-to-right assumption, color meaning variance | RTL-ready, culturally neutral color choices (red ≠ danger everywhere) |
| Situational | Bright sunlight, one-handed, noisy environment | High contrast mode, large touch areas, visual + haptic feedback |

### Dynamic Island UX Pattern (Contextual Persistent UI)

| State | Form | Use |
|-------|------|-----|
| Compact | Pill-shaped ambient indicator | Timer, delivery tracking, playing media |
| Expanded | Tap to reveal controls | Player controls, navigation ETA, order status |
| Glanceable | <1 second readable | No interaction required for status |

**Rule**: Non-intrusive notifications should use compact→expanded pattern. Never require full attention for status updates.

### Ethical Gamification Evaluation

| Pattern | Ethical | Manipulative |
|---------|---------|-------------|
| Progress | Toward user's goal completion | Toward platform engagement metrics |
| Rewards | Skill mastery, knowledge gained | Streaks that punish absence |
| Social | Collaboration, shared achievement | Shame-based leaderboards |
| Urgency | Real deadlines (sale ends) | Fabricated scarcity ("only 2 left!") |

**Rule**: Gamification should reinforce user goals, not platform goals. Ask: "Would the user thank us for this mechanic?"

### Form Validation Best Practices (2025)

| Timing | When | Example |
|--------|------|---------|
| On blur | Most fields | Email format, required fields |
| Real-time (debounced) | Critical uniqueness checks | Username availability (400-700ms debounce) |
| On submit | Fallback for all | Show all errors at once as safety net |

**Rules**:
- Never validate empty required fields before user types (premature validation causes 22% more errors — Baymard)
- Never disable the submit button — keep active, show errors on submit
- Use `aria-invalid`, `aria-describedby`, `aria-live="polite"` for accessibility
- Debounce: 300-500ms for format, 400-700ms for network

### Empty States That Guide Action

```
┌─────────────────────────┐
│        [Icon]           │
│  "No projects yet"      │  ← Concise headline
│  Create your first      │  ← Supporting description
│  project to get started │
│  [Create Project]       │  ← Primary CTA (1-2 options max)
└─────────────────────────┘
```

**Rule**: Never blame the user. Use encouraging tone. Match visual style of populated state. 1-2 actions max (Hick's Law). Products: Slack, GitHub, Notion, Linear.

### Error Recovery Pattern

Every error message needs 3 elements:
1. **What happened** — plain language ("Your changes couldn't be saved")
2. **Why** — brief cause ("The server is temporarily unavailable")
3. **What to do** — actionable buttons: Retry / Save Draft / Undo

**Rules**: Auto-save to localStorage/IndexedDB always. Persistent banner for connection issues (not modal). 2-3 recovery options. Never "Error 500" with no guidance.

### Undo Toast Pattern

```
┌────────────────────────────────────────┐
│  Message deleted          [Undo]       │  ← 5-6 second timer
└────────────────────────────────────────┘
```

**Rule**: Defer actual deletion until toast expires. `aria-live="polite"`. Stack vertically. Place bottom-center. 5-6s for actionable, 3s for informational. Products: Gmail, Slack, Notion.

### Infinite Scroll vs Pagination Decision

| Pattern | Use When |
|---------|----------|
| Infinite scroll | Content discovery, social feeds, entertainment |
| Pagination | Goal-oriented search, data tables, SEO-critical pages |
| Load More button | Hybrid — user-controlled, reachable footer |

**Rule**: Infinite scroll requires virtual scrolling (`@tanstack/virtual`) for >100 items, "Back to top" button, scroll position preservation on back navigation. Never hide the footer.

### Expandable Cards vs Modal Decision

| Pattern | Use When |
|---------|----------|
| Expand in-place | Quick detail view, retains list context |
| Side panel (peek) | Detailed view + list visible simultaneously |
| Modal/dialog | Focused task, form submission, confirmation |
| Full page | Complex content, SEO-important pages |

- Heuristic report template
- Score definitions
- UX metrics
- SUS quick version
- Before/after template

## Heuristic Report Template

```markdown
### UX Heuristic Evaluation: [Component/Flow Name]

| # | Heuristic | Score | Issues | Priority |
|---|-----------|-------|--------|----------|
| 1 | Visibility of System Status | X/5 | [issue] | High/Med/Low |
| 2 | Match User's Mental Model | X/5 | [issue] | High/Med/Low |
| 3 | User Control & Freedom | X/5 | [issue] | High/Med/Low |
| 4 | Consistency & Standards | X/5 | [issue] | High/Med/Low |
| 5 | Error Prevention | X/5 | [issue] | High/Med/Low |
| 6 | Recognition over Recall | X/5 | [issue] | High/Med/Low |
| 7 | Flexibility & Efficiency | X/5 | [issue] | High/Med/Low |
| 8 | Minimalist Design | X/5 | [issue] | High/Med/Low |
| 9 | Error Recovery | X/5 | [issue] | High/Med/Low |
| 10 | Contextual Help | X/5 | [issue] | High/Med/Low |

**Overall Score**: X.X/5
**Critical Areas**: #X, #X (scores <= 2)
**Quick Wins**: [low-effort, high-impact improvements]
```

## Score Definitions

| Score | Meaning |
|-------|---------|
| `5` | excellent |
| `4` | good |
| `3` | acceptable but should improve |
| `2` | poor |
| `1` | critical |

Priority guideline:

- High: scores `1-2` on critical flows
- Medium: score `3`
- Low: score `4`

## UX Metrics

| Metric | Target |
|--------|--------|
| Task Success Rate | `>95%` on critical flows |
| Error Rate | `<5%` on common flows |
| Abandonment Rate | `<10%` on critical flows |

Measure before and after when instrumentation is available.

## SUS Quick Version

Rate each `1-5`:

1. I can complete my task without help.
2. The interface feels consistent.
3. Error messages help me fix problems.
4. I always know what is happening.
5. I can undo mistakes easily.

`SUS Score = sum * 4`

| Range | Interpretation |
|-------|----------------|
| `80+` | Excellent |
| `68-79` | Good |
| `51-67` | Needs improvement |
| `<51` | Poor |

## Before/After Template

```markdown
### UX Improvement: [Title]

#### Before
**Problem**: [user friction]
**Evidence**: [file:line or flow]

#### After
**Solution**: [change]
**Benefit**: [UX impact]

#### Impact Assessment
| Metric | Before | After (Expected) |
|--------|--------|------------------|
| Task completion | X% | Y% |
| Error rate | X% | <Y% |
| User confidence | Low/Med/High | Low/Med/High |

#### Heuristics Improved
- [#X: Heuristic] from X/5 to Y/5

#### Implementation
- **Files**: [files]
- **Effort**: S / M / L
- **Risk**: Low / Medium / High
```
