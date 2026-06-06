# Palette Collaboration Patterns

Purpose: Provide the canonical handoff tokens and minimum fields for Palette coordination with Echo, Flow, Muse, Sentinel, Radar, Canvas, and Warden-related checks.

## Contents

- Partner matrix
- Validation loop
- Animation handoff
- Token coordination
- Security review
- Test handoff
- Visualization handoff

## Partner Matrix

| Partner | Palette receives | Palette sends | Token |
|---------|------------------|---------------|-------|
| `Echo` | friction points, persona findings, emotion score | validation request | `ECHO_TO_PALETTE_HANDOFF`, `PALETTE_TO_ECHO_VALIDATION` |
| `Flow` | animation completion | motion spec | `PALETTE_TO_FLOW_HANDOFF`, `FLOW_TO_PALETTE_COMPLETION` |
| `Muse` | token response | token request | `PALETTE_TO_MUSE_TOKEN_REQUEST`, `MUSE_TO_PALETTE_TOKEN_RESPONSE` |
| `Sentinel` | security feedback | review request | `PALETTE_TO_SENTINEL_REVIEW`, `SENTINEL_TO_PALETTE_FEEDBACK` |
| `Radar` | test report | test request | `PALETTE_TO_RADAR_TEST_REQUEST`, `RADAR_TO_PALETTE_TEST_REPORT` |
| `Canvas` | visualization artifacts | diagram request | `PALETTE_TO_CANVAS_VISUALIZATION` |

## Validation Loop

```markdown
## ECHO_TO_PALETTE_HANDOFF

**Friction Point**: [specific issue]
**Persona**: [persona]
**Emotion Score**: [before score: -3 to +3]
**Root Cause**: [mental model gap / cognitive overload / missing feedback]
**User Quote**: "[quote]"
**Affected Heuristics**:
- #X: [name] - [score]/5
**Suggested Focus**: [improvement direction]
```

```markdown
## PALETTE_TO_ECHO_VALIDATION

**Improvement Made**: [change]
**Files Changed**: [files]
**Heuristics Improved**:
- #X: [heuristic] from X/5 to Y/5
**Validation Request**:
- Target Persona: [persona]
- Expected Outcome: [result]
- Focus Points: [checks]
```

## Animation Handoff

```markdown
## PALETTE_TO_FLOW_HANDOFF

**Interaction**: [interaction]
**Trigger**: [onClick / onHover / onLoad / onStateChange]
**Target Element**: [selector or component]
**State Transitions**:
| From | To | Duration | Easing |
|------|----|----------|--------|
| idle | hover | 150ms | ease-out |
**Reduced Motion Requirement**: Required / Not required
**Accessibility Notes**: [focus / motion / announcement notes]
```

```markdown
## FLOW_TO_PALETTE_COMPLETION

**Implemented**: [animation]
**Files Modified**: [files]
**Approach**: [CSS / JS / library]
**Reduced Motion Support**: Implemented / Pending
**Ready for**: Echo validation / Production
```

## Token Coordination

```markdown
## PALETTE_TO_MUSE_TOKEN_REQUEST

**Interaction Pattern**: [pattern]
**Current Issue**: [gap]
**Token Needs**:
| Category | Purpose | Current Value | Suggested |
|----------|---------|---------------|-----------|
| Color | [purpose] | [value] | [target] |
**Accessibility Concern**: [if any]
**Usage Context**: [where]
```

```markdown
## MUSE_TO_PALETTE_TOKEN_RESPONSE

**Tokens Defined**:
| Token Name | Value | Semantic Purpose |
|------------|-------|------------------|
| `--token` | `value` | [purpose] |
**Usage Guidelines**: [how to apply]
**Files Updated**: [files]
```

## Security Review

```markdown
## PALETTE_TO_SENTINEL_REVIEW

**UX Change**: [description]
**Security-Relevant Aspects**:
- [ ] form handling
- [ ] authentication flow
- [ ] data display
- [ ] error message content
- [ ] input handling
**Specific Concerns**: [questions]
**Files Affected**: [files]
```

```markdown
## SENTINEL_TO_PALETTE_FEEDBACK

**Review Status**: APPROVED / NEEDS_CHANGE / BLOCKED
**Findings**:
| Severity | Issue | Location | Recommendation |
|----------|-------|----------|----------------|
| [High/Med/Low] | [issue] | [file:line] | [fix] |
**Required Changes**: [if any]
```

## Test Handoff

```markdown
## PALETTE_TO_RADAR_TEST_REQUEST

**UX Improvement**: [change]
**Component**: [component]
**Files Changed**: [files]
**Interaction Behaviors to Test**:
1. **Behavior**: [behavior]
   - **Trigger**: [action]
   - **Expected Result**: [result]
   - **Accessibility Check**: [ARIA or keyboard expectation]
**Edge Cases**: [edge cases]
```

```markdown
## RADAR_TO_PALETTE_TEST_REPORT

**Tests Added**:
| Test File | Test Name | Coverage |
|-----------|-----------|----------|
| [file] | [name] | [coverage] |
**Coverage Delta**: [+X%]
**Accessibility Tests**: [result]
**Test Commands**: [commands]
```

## Visualization Handoff

```markdown
## PALETTE_TO_CANVAS_VISUALIZATION

**Visualization Type**: Before/After Comparison | Heuristic Score Chart | Interaction Flow
**Audience**: [design / product / engineering / leadership]
**Source Artifacts**: [files or heuristics]
**Key Story**: [what the visualization must show]
```

If a change materially shifts Value, Agency, Identity, Resilience, or Echo, request a Warden pass after Palette’s own review.
