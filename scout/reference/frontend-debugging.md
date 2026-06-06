# Frontend Debugging Reference

Browser and frontend-framework-specific bug investigation patterns.

## Browser DevTools Strategy

### Console Patterns
- Unhandled Promise rejection → missing async error handling
- `[Violation]` warnings → forced reflow, long task, passive event listener
- CORS errors → API endpoint misconfiguration or proxy setup missing

### Network Tab Investigation
- Identify slow requests in waterfall → resource dependency chain issue
- Response diff (expected vs actual) → API contract violation
- Preflight (OPTIONS) failure → caused by CORS misconfiguration

### Performance Tab
- Long Task (>50ms) → main thread blocking
- Layout Shift → root cause of CLS issue (missing image dimensions, dynamic content insertion)
- Memory timeline → leak detection (Specter escalation candidate)

## React-Specific Patterns

### Hydration Mismatch
- Symptom: `Text content does not match server-rendered HTML`
- Cause: divergent output between SSR and CSR (Date, Math.random, window references)
- Investigation: check for inappropriate use of `suppressHydrationWarning`
- Root fix: isolate client-only logic inside `useEffect`

### Stale Closure
- Symptom: event handler reads outdated state
- Cause: missing dependencies in useCallback/useEffect dependency array
- Investigation: check for ESLint `exhaustive-deps` warnings
- Pattern: verify whether functional update `setState(prev => ...)` can prevent the issue

### useEffect Cleanup Missing
- Symptom: state update after unmount (memory leak)
- Cause: forgotten cleanup for subscription, timer, or AbortController
- Investigation: `Can't perform a React state update on an unmounted component` warning
- Specter escalation: if memory leak suspected, use SCOUT_TO_SPECTER_HANDOFF

### Infinite Re-render Loop
- Symptom: `Maximum update depth exceeded`
- Cause: unconditional setState inside useEffect, object literals in dependency array
- Investigation: check re-render count with React DevTools Profiler

## Vue-Specific Patterns

### Reactivity Lost
- Symptom: data change not reflected in UI
- Cause: direct array index assignment in Vue 2, missing ref in Vue 3
- Investigation: track reactive state with Vue Devtools

### Computed Cache Invalidation
- Symptom: computed property not recalculated
- Cause: getter references a non-reactive property
- Investigation: verify reactive state of properties referenced inside computed getter

## State Management Bugs

### Redux Selector Memoization Failure
- Symptom: unnecessary re-renders
- Cause: createSelector input selector returns a new object on every call
- Investigation: check per-action state diff in Redux DevTools
- Pattern: `===` reference comparison — beware of array/object re-creation

### Zustand Stale State
- Symptom: stale state read inside subscribe
- Cause: closure capture issue
- Investigation: compare `getState()` value with the state inside the subscribe callback

## CSS Layout Bug Patterns

### Z-index Stacking Context
- Symptom: element hidden beneath another element
- Cause: implicit stacking context created by transform, opacity, or will-change
- Investigation: visualize stacking contexts with DevTools Layers panel

### Flexbox/Grid Overflow
- Symptom: content overflows the container
- Cause: `min-width: auto` (Flexbox default), text wrapping not set
- Investigation: apply `overflow: hidden` to isolate the problem → fix with `min-width: 0`

### Container Query / @layer Issues
- Symptom: styles not applied only under specific conditions
- Cause: container query size condition mismatch, @layer precedence
- Investigation: check applied/overridden rules in DevTools Styles panel

## Mobile-Specific Patterns

### Touch Event vs Click Delay
- Symptom: 300ms delay after tap
- Cause: waiting for double-tap zoom detection
- Investigation: check whether `touch-action: manipulation` is set

### Viewport Bug
- Symptom: layout breaks on iOS Safari when address bar shows/hides
- Cause: `100vh` does not account for dynamic viewport height
- Investigation: check usage of `dvh` (dynamic viewport height)

## AI-Generated Frontend Code Patterns

Common frontend bugs in AI-generated code:
- Incomplete dependency array specification (casual use of ESLint suppressions)
- Missing error boundaries (happy-path-only implementation)
- Missing accessibility attributes (aria-label, role, keyboard navigation)
- Incomplete responsive design (only specific breakpoints considered)
