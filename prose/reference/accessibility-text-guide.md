# Accessibility Text Guide

Alt text rules, ARIA label patterns, screen reader text. Aligned with WCAG 2.2 (ISO/IEC 40500:2025).

> **Compliance context**: WCAG 2.2 is the current W3C standard (Oct 2023). The European Accessibility Act (EAA) has been enforceable since June 28, 2025, making Level AA compliance a legal requirement in the EU. ADA litigation in the U.S. continues to reference WCAG 2.2.

---

## Alt Text

### Decision Tree

```
Is the image decorative?
  → Yes: alt="" (empty alt, NOT missing alt)
  → No: Does it contain text?
    → Yes: Include the text in alt
    → No: Does it convey information?
      → Yes: Describe the information, not the image
      → No: alt="" (decorative)
```

### Alt Text Rules

| Rule | Good | Bad |
|------|------|-----|
| **Describe function, not appearance** | "Search" (for search icon) | "Magnifying glass icon" |
| **Be concise** | "Sales chart showing 20% growth in Q4" | "A bar chart with blue bars..." |
| **Skip "image of"** | "Team photo at company retreat" | "Image of team at retreat" |
| **Include text in images** | "Banner: 50% off all items" | "Promotional banner" |
| **Context matters** | "Error: form has 2 invalid fields" | "Red circle with X" |

### Alt Text by Image Type

| Type | Pattern | Example |
|------|---------|---------|
| **Logo** | "[Company name] logo" | "Acme Corp logo" |
| **Icon button** | Action description | "Close dialog" |
| **Avatar** | "[Name]'s profile photo" | "Jane Smith's profile photo" |
| **Chart** | Summary + key data | "Monthly revenue: $50K avg, trending up" |
| **Screenshot** | What it demonstrates | "Settings page showing dark mode toggle" |
| **Decorative** | Empty alt: `alt=""` | (background patterns, dividers) |
| **Complex diagram** | Brief alt + long description | alt + `aria-describedby` |

---

## ARIA Labels

### Common ARIA Patterns

| Element | ARIA | Example |
|---------|------|---------|
| **Icon button** | `aria-label` | `<button aria-label="Close dialog">×</button>` |
| **Navigation** | `aria-label` on `<nav>` | `<nav aria-label="Main navigation">` |
| **Search** | `aria-label` on form | `<form role="search" aria-label="Site search">` |
| **Status** | `aria-live` | `<div aria-live="polite">3 results found</div>` |
| **Toggle** | `aria-pressed` | `<button aria-pressed="true">Dark mode</button>` |
| **Expandable** | `aria-expanded` | `<button aria-expanded="false">Show details</button>` |
| **Tab panel** | `aria-selected` | `<button role="tab" aria-selected="true">` |
| **Progress** | `aria-valuenow` | `<progress aria-valuenow="75" aria-valuemax="100">` |

### ARIA Label Writing Rules

```markdown
1. Use visible text first (aria-label is a last resort)
2. Start with a verb for actions: "Close", "Open", "Search"
3. Include context: "Delete item 'Project Alpha'" not just "Delete"
4. Match the visual context: if text says "Learn more", aria-label says
   "Learn more about pricing plans"
5. Don't include the role: "Close" not "Close button"
   (screen reader already announces "button")
```

### When to Use Which ARIA

| ARIA Attribute | Use When |
|---------------|----------|
| `aria-label` | No visible text, need to provide accessible name |
| `aria-labelledby` | Visible text exists elsewhere, reference it by ID |
| `aria-describedby` | Additional description beyond the label |
| `aria-live="polite"` | Dynamic content updates (search results, notifications) |
| `aria-live="assertive"` | Urgent updates (errors, time-sensitive alerts) |
| `aria-hidden="true"` | Decorative elements screen readers should skip |

---

## Screen Reader Text

### Visually Hidden Text Pattern

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

### Common Screen Reader Announcements

| Scenario | Announcement | Implementation |
|----------|-------------|---------------|
| **Form error** | "Error: Email is required" | `aria-live="assertive"` on error region |
| **Loading** | "Loading results..." | `aria-live="polite"` + sr-only text |
| **Results count** | "15 results found" | `aria-live="polite"` on results region |
| **Success** | "Changes saved successfully" | `role="status"` with `aria-live="polite"` |
| **New content** | "3 new notifications" | `aria-live="polite"` on counter |
| **Page change** | Document title update | `<title>New Page - App Name</title>` |

---

## Accessible Content Patterns

### Link Text

| Bad | Good | Why |
|-----|------|-----|
| "Click here" | "View pricing plans" | Context without surrounding text |
| "Read more" | "Read more about our API" | Unique, descriptive |
| "Link" | "Documentation" | Meaningful destination |
| URL as text | Descriptive text | Readable by screen readers |

### Heading Structure

```markdown
## Rules
1. One <h1> per page (page title)
2. Don't skip levels (h1 → h3 without h2)
3. Headings describe the section content
4. Use headings for structure, not styling

## Example
h1: "Account Settings"
  h2: "Profile"
    h3: "Personal Information"
    h3: "Profile Photo"
  h2: "Security"
    h3: "Password"
    h3: "Two-Factor Authentication"
  h2: "Notifications"
```

### Table Accessibility

```html
<table>
  <caption>Monthly sales by region</caption>
  <thead>
    <tr>
      <th scope="col">Region</th>
      <th scope="col">Q1</th>
      <th scope="col">Q2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">North</th>
      <td>$50K</td>
      <td>$62K</td>
    </tr>
  </tbody>
</table>
```

---

## WCAG 2.2 New Criteria (Text-Relevant)

| Criterion | Level | Text Impact |
|-----------|-------|-------------|
| **2.4.11 Focus Appearance** | AA | Ensure focused elements have visible labels and sufficient contrast |
| **2.5.7 Dragging Movements** | AA | Provide text instructions for non-drag alternatives |
| **2.5.8 Target Size (Minimum)** | AA | Tap/click targets must be at least 24x24 CSS px; label text must fit |
| **3.2.6 Consistent Help** | A | Help mechanisms (contact, FAQ links) must appear in consistent locations |
| **3.3.7 Redundant Entry** | A | Don't ask users to re-enter information; pre-fill and label clearly |
| **3.3.8 Accessible Authentication** | AA | Avoid cognitive function tests; provide clear text alternatives for CAPTCHA |

---

## Accessibility Text Checklist

```markdown
- [ ] All images have appropriate alt text (or empty alt for decorative)
- [ ] Icon buttons have aria-labels
- [ ] Links have descriptive text (no "click here")
- [ ] Form fields have visible labels (not just placeholders)
- [ ] Error messages are announced to screen readers
- [ ] Dynamic content uses aria-live regions
- [ ] Heading hierarchy is logical (no skipped levels)
- [ ] Tables have captions and scope attributes
- [ ] Color is not the sole indicator of meaning
- [ ] Focus order matches visual order
- [ ] WCAG 2.2: Help mechanisms are consistently placed and labeled
- [ ] WCAG 2.2: Authentication steps have clear text instructions
- [ ] WCAG 2.2: Pre-filled fields are labeled to explain auto-populated data
```

---

## WCAG 2.2 Detailed Implementation Guide

### 2.5.7 Dragging Movements — Text Alternatives

For any UI where users drag to perform an action, provide a text-based alternative:

```markdown
## Patterns
- Drag handle: "Drag to reorder, or use the up/down buttons"
- Slider: "Drag to adjust, or type a value in the field below"
- Sortable list: "Drag items to reorder, or use arrow keys when focused"
- Range control: "Slide to set range. Use keyboard: Left/Right arrows to adjust"

## Implementation Notes
- Provide the alternative in visible help text OR in aria-describedby
- Keyboard alternative must be functional, not just documented
- Touch: swipe alternatives must also exist (tap to select, then move)
```

### 3.2.6 Consistent Help — Copy Standards

Help mechanisms must appear in consistent locations across multiple pages:

```markdown
## Rules
1. If a help link appears in the header on page A, it must appear in the header on all pages
2. Help copy must use consistent labels: "Help" not "Help" on one page and "Support" on another
3. Contact information copy must be identical wherever it appears
4. FAQ links must use the same label across all pages

## Consistent Help Labels
✅ "Help" (consistent across all pages)
✅ "Contact support" (consistent across all pages)
❌ "Help" on homepage, "Get help" on checkout, "Support" on settings

## Placement Consistency Checklist
- [ ] Help mechanism appears at the same position across all pages
- [ ] Help label text is identical across all pages
- [ ] Contact copy is verbatim consistent
```

### 3.3.7 Redundant Entry — Pre-fill Copy Patterns

Do not ask users to re-enter information they have already provided:

```markdown
## Pre-fill Announcement Patterns
"Using your saved address: [address]. Change"
"Pre-filled from your profile. Update if needed."
"We found your previous entry: [value]. Confirm or update."

## Suggestion Copy
"Same as your billing address — use it? [Yes / No]"
"Your name from step 1: [name]. Use this? [Confirm / Change]"
"Last used: [value]. Use again?"

## Rules
1. Label pre-filled fields clearly — don't silently populate without notification
2. Always provide an edit path: "Change" or "Update"
3. For auto-populated values from session: "Based on what you told us earlier"
4. Never pre-fill sensitive data (passwords, payment CVV) silently
```

### 3.3.3 Error Suggestion — Specific Recovery Text

Error messages must suggest how to correct the input:

```markdown
## Templates
"[Field] must be [requirement]. Example: [concrete example]"
"Enter a valid [format]. Example: name@company.com"
"[Field] is too [long/short]. Use [X] to [Y] characters."

## High-Quality Error Suggestion Examples
✅ "Password must be 8–64 characters and include at least one number."
✅ "Enter a date in MM/DD/YYYY format. Example: 03/15/2025"
✅ "Phone number must include country code. Example: +1 555 000 0000"
❌ "Invalid input"
❌ "Error in field"
❌ "Please try again"
```

### 3.3.4 Error Prevention — Confirmation Copy for Irreversible Actions

For legal, financial, or data-deletion actions, provide review and confirmation:

```markdown
## Review Step Copy
"Review your order before confirming."
"Check the details below. This action cannot be undone."
"You are about to [action]. Please confirm."

## Confirmation Dialog Patterns
### Destructive Action (e.g., delete)
Title: "Delete [item name]?"
Body: "This will permanently delete [item]. You can't undo this."
Confirm CTA: "Delete [item name]"  ← be specific
Cancel CTA: "Keep [item name]"

### High-Stakes Action (e.g., submit legal form)
Title: "Submit your application?"
Body: "Once submitted, you won't be able to edit your responses."
Confirm CTA: "Submit application"
Cancel CTA: "Go back and review"

## Rules
1. Confirm buttons must name the specific action: "Delete account" not "OK"
2. Never use "OK/Cancel" for destructive actions
3. The cancel action should be the safe default (visually prominent)
4. For financial transactions: show amount and recipient in the confirmation copy
```
