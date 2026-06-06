# UX Writing and Microcopy Patterns

Purpose: Keep CTA labels, error messages, confirmations, status copy, and helper text specific, actionable, and consistent.

## Contents

- CTA labels
- Error messages
- Empty states
- Confirmations
- Success and progress copy
- Tone and consistency

## CTA Labels

Rules:

- use a verb plus object
- describe the actual outcome
- match the visible state
- avoid generic labels such as `OK`, `Yes`, `Submit`, or `Click here`

Examples:

| Bad | Good |
|-----|------|
| Submit | Save changes |
| OK | Create project |
| Delete | Delete project |
| Click here | View documentation |

Button state labels:

| State | Pattern |
|-------|---------|
| Default | action verb + object |
| Loading | present participle + `...` |
| Success | past tense or completion message |
| Error | say the action failed and allow retry |

## Error Messages

Use `What + Why + How`.

| Weak | Better |
|------|--------|
| Invalid input | Email must include `@` and a domain |
| Error | This file is too large. Max size is 10 MB. |
| Network error | Can't connect right now. Check your connection and try again. |

Rules:

- name the field or action
- avoid raw status-code language
- say how to recover
- if the user cannot fix it, say what they can do next

## Empty States

Always explain:

1. what is missing
2. why the user is seeing this
3. what the best next action is

Use scenario-specific copy for first use, no-results, and cleared/archived states.

## Confirmations

For destructive actions:

- name the object
- say whether the action can be undone
- prefer explicit buttons such as `Delete project` / `Keep project`
- when recovery exists, prefer soft delete plus `Undo`

Pattern:

| Situation | Recommended copy |
|-----------|------------------|
| Hard delete | `Delete project` + `This action cannot be undone.` |
| Soft delete | `Project archived. Undo?` |
| Unsaved changes | `Discard changes` / `Continue editing` |

## Success And Progress Copy

- acknowledge user actions within the correct time window
- say what completed, not just that “something happened”
- use `aria-live="polite"` for toast or status updates when appropriate

| Context | Good pattern |
|---------|--------------|
| Save | `Changes saved.` |
| Delete with recovery | `Item deleted. Undo?` |
| Upload | `Uploading file...` / `Upload complete.` |
| Long task | `Processing your data...` plus progress if available |

## Tone And Consistency

- plain language over jargon
- same concept, same label everywhere
- be calm during failure states
- be direct without sounding robotic
- keep tense and terminology consistent across states
