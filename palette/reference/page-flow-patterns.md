# Page and Flow UX Patterns

Purpose: Guide page-state design, navigation, search and filter UX, onboarding, and dashboard layouts with explicit recovery and wayfinding rules.

## Contents

- Page states
- Navigation and progress
- Search, filter, and tables
- Onboarding and first use
- Dashboard layouts
- Accessibility notes

## Page States

| State | Must include | Typical next action |
|-------|--------------|---------------------|
| Empty | explanation, reason, and CTA | create, import, explore, or clear filters |
| Error | plain-language cause, safe retry, recovery path | retry, go back, or contact support |
| Loading | stable layout, progress cue, no blank screen | skeleton for structured content, spinner for short actions |
| Offline | current status, cached-content note if any, retry/reconnect cue | retry after reconnect |
| First use | purpose, first milestone, small next step | start setup or guided action |

Rules:

- never show a blank state without a next step
- customize empty states by scenario, not by a single generic message
- use `role="status"` or `aria-live="polite"` for dynamic result or connectivity updates

## Navigation And Progress

| Pattern | Use it when | Rule |
|---------|-------------|------|
| Breadcrumbs | hierarchy is deeper than a single page jump | show current location without forcing recall |
| Dead-end prevention | a user can finish a task and get stuck | always offer a next valid action |
| Step progress | multi-step tasks | show current step, remaining steps, and back/exit options |

If a journey needs more than a small structural fix, treat it as Macro and route to `Vision`.

## Search, Filter, And Tables

| Problem | Pattern |
|---------|---------|
| `20+` items and no fast find path | add search |
| multiple filters with unclear active state | show active filter chips or clear state |
| dense tables with scanning pain | improve hierarchy, column labels, and row actions |
| long result sets | use pagination or infinite scroll only when the task model supports it |
| search/filter updates feel silent | announce result count changes with `aria-live="polite"` |

## Onboarding And First Use

| Pattern | Use it when | Rule |
|---------|-------------|------|
| Progressive disclosure | the product has more than one maturity level | reveal basics first, advanced controls later |
| Setup wizard | onboarding has unavoidable sequential steps | show progress and allow safe return |
| Feature discovery | new capabilities need lightweight teaching | keep it contextual, dismissible, and non-blocking |

Anti-patterns:

- showing all options on first load
- hiding common actions too deeply
- forcing re-learning through inconsistent labels or patterns

## Dashboard Layouts

- keep one primary CTA per area
- make metric cards scannable in seconds
- use status indicators consistently
- reserve quick actions for frequent, low-risk tasks

## Accessibility Notes

- empty, error, and result-count messages should be announced
- offline/reconnect banners need clear semantics
- progress indicators must be understandable without color alone
- first-use flows must support keyboard and screen-reader navigation
