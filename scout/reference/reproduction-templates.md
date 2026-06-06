# Scout Reproduction Templates Reference

**Purpose:** Reusable reproduction templates for UI, API, state, async, and general failures.
**Read when:** You need a consistent reproduction record instead of writing ad hoc repro notes.

## Contents

- UI bug template
- API bug template
- State bug template
- Async bug template
- General bug report template

## UI Bug Template

```markdown
## UI Bug Reproduction

**Environment:**
- Browser: [Chrome 120 / Firefox 121 / Safari 17]
- OS: [macOS 14 / Windows 11 / Ubuntu 22]
- Screen size: [1920x1080 / Mobile 375x667]
- User role: [Admin / Regular / Guest]

**Setup State:**
- [ ] Fresh login
- [ ] Specific data exists: [describe]
- [ ] Feature flags: [list]

**Steps:**
1. Navigate to [URL/page]
2. [User action]
3. [User action]
4. Observe [element/area]

**Expected:** [What should happen]
**Actual:** [What actually happens]
**Visual Evidence:** [Screenshot or recording link]
**Reproducibility:** [Always / 80% / Specific conditions]
```

## API Bug Template

```markdown
## API Bug Reproduction

**Endpoint:** [METHOD /api/path]

**Request:**
```json
{
  "headers": {
    "Authorization": "Bearer [token type]",
    "Content-Type": "application/json"
  },
  "body": {}
}
```

**Expected Response:** [status/body]
**Actual Response:** [status/body]

**cURL Command:**
```bash
curl -X POST https://api.example.com/endpoint \
  -H "Authorization: Bearer xxx" \
  -H "Content-Type: application/json" \
  -d '{"key":"value"}'
```

**Reproducibility:** [Always / Specific conditions]
```

## State Bug Template

```markdown
## State Bug Reproduction

**State Location:** [Redux store / React Context / component state]
**State Path:** [store.user.profile / context.theme]

**Initial State:** [json]
**Action/Trigger:** [what changes the state]
**Expected State:** [json]
**Actual State:** [json]

**State Timeline:**
1. [T0] Initial state
2. [T1] Action dispatched
3. [T2] Unexpected state

**DevTools Evidence:** [Redux DevTools / React DevTools]
```

## Async Bug Template

```markdown
## Async Bug Reproduction

**Async Operation:** [API call / timer / event listener]

**Sequence:**
User -> Component -> Service -> API

**Timing Information:**
- Operation start: [timestamp]
- Expected completion: [duration]
- Actual completion: [duration]
- Error occurred at: [timestamp]

**Race Condition Factors:**
- [ ] Rapid user interaction
- [ ] Slow network
- [ ] Component unmount
- [ ] Multiple concurrent requests

**Console Logs:**
[timestamped logs]
```

## General Bug Report Template

```markdown
## Bug Report

**Title:** [Brief description]
**Severity:** Critical / High / Medium / Low
**Reproducibility:** Always / Sometimes / Rare

**Environment:**
- [Browser/OS/Node version]
- [Dev/Staging/Prod]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Behavior:** [What should happen]
**Actual Behavior:** [What actually happens]

**Error Messages:**
[exact error text]

**Additional Context:**
- Recent changes: [if known]
- Affected users: [scope]
- Workaround: [if any]
```

## Template Selection Guide

| Bug Type | Template | Focus |
|----------|----------|-------|
| Visual / UI | UI Bug | screenshot, viewport, role |
| API | API Bug | request/response, `curl` |
| State | State Bug | snapshots, timeline |
| Timing | Async Bug | sequence, timestamps |
| Mixed or unclear | General Bug Report | common baseline |
