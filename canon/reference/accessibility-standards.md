# Accessibility Standards Reference

## WCAG 2.2 / ISO/IEC 40500:2025

[Source W3C: https://www.w3.org/WAI/news/2025-10-21/wcag22-iso/] [Source ISO: https://www.iso.org/standard/91029.html]

**ISO/IEC 40500:2025** was approved on 21 October 2025 — WCAG 2.2 now carries formal ISO recognition, giving it legal and regulatory weight across borders. This supersedes ISO/IEC 40500:2012 (which was WCAG 2.0). The December 2024 revision of WCAG 2.2 is expected to become ISO/IEC 40500:2026 by late 2026. Always assess against WCAG 2.2 for current compliance; WCAG 3.0 (outcome-based scoring, targeted Recommendation ~late 2029) is track-only.

> **Tool coverage ceiling:** W3C-approved automated rules cover full or partial SC for only 31% of WCAG 2.2 Level A/AA Success Criteria (17/55 SC). Actual detection rates: axe-core ~57%, general range 30–57%. Always require manual expert audit for any compliance determination.

## WCAG 2.2 (Web Content Accessibility Guidelines)

### Conformance Levels

| Level | Description | Target Audience |
|-------|-------------|-----------------|
| **A** | Minimum accessibility | All websites |
| **AA** | Standard accessibility | Government, enterprise (recommended) |
| **AAA** | Enhanced accessibility | Specialized accessibility needs |

### POUR Principles

| Principle | Meaning | Key Requirements |
|-----------|---------|------------------|
| **Perceivable** | Information must be presentable | Text alternatives, captions, contrast |
| **Operable** | UI must be operable | Keyboard access, time limits, seizures |
| **Understandable** | Content must be understandable | Readable, predictable, error prevention |
| **Robust** | Content must be compatible | Valid markup, accessibility API |

---

## Level A Success Criteria (Minimum)

### 1.1 Text Alternatives

#### 1.1.1 Non-text Content (Level A)
**Requirement:** All non-text content has text alternative that serves equivalent purpose.

**Checklist:**
- [ ] Images have descriptive alt text
- [ ] Decorative images have empty alt (`alt=""`)
- [ ] Complex images have detailed descriptions
- [ ] Form images (buttons, icons) have functional labels
- [ ] CAPTCHA provides alternative methods

**Non-Compliant:**
```html
<img src="chart.png">
<button><img src="search-icon.png"></button>
```

**Compliant:**
```html
<img src="chart.png" alt="Sales increased 20% from Q1 to Q2">
<button aria-label="Search"><img src="search-icon.png" alt=""></button>
```

### 1.2 Time-based Media

#### 1.2.1 Audio-only and Video-only (Level A)
**Requirement:** Provide alternatives for pre-recorded audio-only and video-only content.

- Audio-only: Text transcript
- Video-only: Text description or audio track

#### 1.2.2 Captions (Pre-recorded) (Level A)
**Requirement:** Captions provided for all pre-recorded audio content in synchronized media.

#### 1.2.3 Audio Description or Media Alternative (Level A)
**Requirement:** Alternative for time-based media or audio description for pre-recorded video.

### 1.3 Adaptable

#### 1.3.1 Info and Relationships (Level A)
**Requirement:** Information, structure, and relationships can be programmatically determined.

**Checklist:**
- [ ] Use semantic HTML elements
- [ ] Form inputs have associated labels
- [ ] Tables have proper headers
- [ ] Lists use proper list markup
- [ ] Headings reflect document structure

**Non-Compliant:**
```html
<div class="heading">Section Title</div>
<div onclick="submit()">Submit</div>
<table><tr><td>Name</td><td>Age</td></tr></table>
```

**Compliant:**
```html
<h2>Section Title</h2>
<button type="submit">Submit</button>
<table>
  <thead><tr><th>Name</th><th>Age</th></tr></thead>
  <tbody>...</tbody>
</table>
```

#### 1.3.2 Meaningful Sequence (Level A)
**Requirement:** Reading sequence can be programmatically determined.

#### 1.3.3 Sensory Characteristics (Level A)
**Requirement:** Instructions don't rely solely on sensory characteristics (shape, color, size, location, sound).

**Non-Compliant:**
```html
<p>Click the green button to continue.</p>
<p>See the sidebar on the right for more info.</p>
```

**Compliant:**
```html
<p>Click the "Continue" button (green, below the form) to proceed.</p>
<p>See "Additional Resources" section for more info.</p>
```

### 1.4 Distinguishable

#### 1.4.1 Use of Color (Level A)
**Requirement:** Color is not the only visual means of conveying information.

**Non-Compliant:**
```html
<p>Required fields are marked in red.</p>
<span style="color: red">Username</span>
```

**Compliant:**
```html
<p>Required fields are marked with an asterisk (*).</p>
<span style="color: red">Username *</span>
<span class="sr-only">(required)</span>
```

#### 1.4.2 Audio Control (Level A)
**Requirement:** Audio playing for more than 3 seconds can be paused or stopped.

### 2.1 Keyboard Accessible

#### 2.1.1 Keyboard (Level A)
**Requirement:** All functionality available via keyboard.

**Checklist:**
- [ ] All interactive elements focusable
- [ ] Custom widgets support keyboard
- [ ] No keyboard traps
- [ ] Focus order is logical

**Non-Compliant:**
```html
<div onclick="openMenu()">Menu</div>
<span class="link" onclick="navigate()">Click here</span>
```

**Compliant:**
```html
<button onclick="openMenu()">Menu</button>
<a href="/page">Click here</a>
<!-- Or for custom elements: -->
<div role="button" tabindex="0" onkeydown="handleKey(event)" onclick="openMenu()">Menu</div>
```

#### 2.1.2 No Keyboard Trap (Level A)
**Requirement:** Keyboard focus can be moved away from any component using keyboard.

#### 2.1.4 Character Key Shortcuts (Level A - WCAG 2.1)
**Requirement:** Single-character shortcuts can be turned off or remapped.

### 2.2 Enough Time

#### 2.2.1 Timing Adjustable (Level A)
**Requirement:** Time limits can be turned off, adjusted, or extended.

Exceptions: Real-time events, essential timing, more than 20 hours.

#### 2.2.2 Pause, Stop, Hide (Level A)
**Requirement:** Moving, blinking, scrolling content can be paused, stopped, or hidden.

### 2.3 Seizures and Physical Reactions

#### 2.3.1 Three Flashes or Below Threshold (Level A)
**Requirement:** No content flashes more than 3 times per second.

### 2.4 Navigable

#### 2.4.1 Bypass Blocks (Level A)
**Requirement:** Mechanism to bypass repeated content blocks.

**Implementation:**
```html
<a href="#main-content" class="skip-link">Skip to main content</a>
<!-- Header, navigation -->
<main id="main-content">...</main>
```

#### 2.4.2 Page Titled (Level A)
**Requirement:** Pages have titles that describe topic or purpose.

```html
<title>Shopping Cart - My Store</title>
```

#### 2.4.3 Focus Order (Level A)
**Requirement:** Focusable components receive focus in meaning-preserving order.

#### 2.4.4 Link Purpose (In Context) (Level A)
**Requirement:** Purpose of each link can be determined from link text or context.

**Non-Compliant:**
```html
<a href="/products">Click here</a>
<a href="/about">Read more</a>
```

**Compliant:**
```html
<a href="/products">View our products</a>
<a href="/about">Read more about our company</a>
```

### 2.5 Input Modalities (WCAG 2.1)

#### 2.5.1 Pointer Gestures (Level A)
**Requirement:** Multi-point or path-based gestures have single-pointer alternatives.

#### 2.5.2 Pointer Cancellation (Level A)
**Requirement:** For single-pointer operations:
- No down-event trigger (or can abort/undo)
- Up-event completes or reverses

#### 2.5.3 Label in Name (Level A)
**Requirement:** For components with visible text labels, accessible name contains visible text.

#### 2.5.4 Motion Actuation (Level A)
**Requirement:** Functionality triggered by motion can be triggered by UI and can be disabled.

### 3.1 Readable

#### 3.1.1 Language of Page (Level A)
**Requirement:** Default language can be programmatically determined.

```html
<html lang="ja">
<html lang="en">
```

### 3.2 Predictable

#### 3.2.1 On Focus (Level A)
**Requirement:** Receiving focus doesn't initiate change of context.

#### 3.2.2 On Input (Level A)
**Requirement:** Changing a setting doesn't automatically change context unless user is advised.

### 3.3 Input Assistance

#### 3.3.1 Error Identification (Level A)
**Requirement:** If input error is detected, item is identified and error described in text.

```html
<input aria-describedby="email-error" aria-invalid="true">
<span id="email-error" role="alert">Please enter a valid email address</span>
```

#### 3.3.2 Labels or Instructions (Level A)
**Requirement:** Labels or instructions provided when content requires user input.

### 4.1 Compatible

#### 4.1.1 Parsing (Level A) - Deprecated in WCAG 2.2
Previously required valid HTML. Now handled by user agents.

#### 4.1.2 Name, Role, Value (Level A)
**Requirement:** For all UI components, name and role can be programmatically determined.

**Custom Widget Example:**
```html
<div role="button"
     tabindex="0"
     aria-pressed="false"
     aria-label="Toggle dark mode">
  🌙
</div>
```

---

## Level AA Success Criteria (Standard)

### 1.3.4 Orientation (Level AA)
**Requirement:** Content doesn't restrict view to single display orientation.

### 1.3.5 Identify Input Purpose (Level AA)
**Requirement:** Input purpose can be programmatically determined for user data.

```html
<input type="email" autocomplete="email">
<input type="tel" autocomplete="tel">
<input type="text" autocomplete="given-name">
```

### 1.4.3 Contrast (Minimum) (Level AA)
**Requirement:** Text has contrast ratio of at least 4.5:1 (3:1 for large text).

| Text Size | Minimum Contrast |
|-----------|------------------|
| Normal text (<18pt) | 4.5:1 |
| Large text (≥18pt or 14pt bold) | 3:1 |
| UI components, graphics | 3:1 |

**Tools:**
- WebAIM Contrast Checker
- Chrome DevTools Accessibility panel
- axe DevTools

### 1.4.4 Resize Text (Level AA)
**Requirement:** Text can be resized up to 200% without loss of content.

### 1.4.5 Images of Text (Level AA)
**Requirement:** Use real text instead of images of text (with exceptions).

### 1.4.10 Reflow (Level AA - WCAG 2.1)
**Requirement:** Content can reflow without scrolling in two dimensions at 320px width.

### 1.4.11 Non-text Contrast (Level AA - WCAG 2.1)
**Requirement:** UI components and graphics have 3:1 contrast ratio.

### 1.4.12 Text Spacing (Level AA - WCAG 2.1)
**Requirement:** No loss of content when adjusting:
- Line height: 1.5x font size
- Paragraph spacing: 2x font size
- Letter spacing: 0.12x font size
- Word spacing: 0.16x font size

### 1.4.13 Content on Hover or Focus (Level AA - WCAG 2.1)
**Requirement:** Pointer hover or keyboard focus triggers additional content that is:
- Dismissible
- Hoverable
- Persistent

### 2.4.5 Multiple Ways (Level AA)
**Requirement:** More than one way to locate a page (sitemap, search, navigation).

### 2.4.6 Headings and Labels (Level AA)
**Requirement:** Headings and labels describe topic or purpose.

### 2.4.7 Focus Visible (Level AA)
**Requirement:** Keyboard focus indicator is visible.

```css
:focus {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

/* Don't remove focus outline */
:focus { outline: none; } /* BAD */
```

### 2.4.11 Focus Not Obscured (Minimum) (Level AA - WCAG 2.2)
**Requirement:** When a component receives focus, it's not entirely hidden by author-created content.

### 3.1.2 Language of Parts (Level AA)
**Requirement:** Language of passages can be programmatically determined.

```html
<p>The French word <span lang="fr">bonjour</span> means hello.</p>
```

### 3.2.3 Consistent Navigation (Level AA)
**Requirement:** Navigation appears in same relative order on each page.

### 3.2.4 Consistent Identification (Level AA)
**Requirement:** Components with same functionality are identified consistently.

### 3.3.3 Error Suggestion (Level AA)
**Requirement:** If error is detected and suggestions are known, provide them.

### 3.3.4 Error Prevention (Legal, Financial, Data) (Level AA)
**Requirement:** For legal/financial submissions:
- Reversible, or
- Checked and correctable, or
- Confirmed before submission

### 3.3.7 Redundant Entry (Level AA - WCAG 2.2)
**Requirement:** Previously entered information is auto-populated or available to select.

### 3.3.8 Accessible Authentication (Minimum) (Level AA - WCAG 2.2)
**Requirement:** Cognitive function tests are not required unless:
- Alternative method exists, or
- Mechanism to help complete test, or
- Recognition (not recall) of objects

---

## WAI-ARIA

### ARIA Principles

1. **First Rule of ARIA:** Don't use ARIA if native HTML does the job
2. Use correct roles for interactive elements
3. All interactive ARIA controls must be keyboard accessible
4. Don't use `role="presentation"` or `aria-hidden="true"` on focusable elements
5. All interactive elements must have accessible names

### Common ARIA Patterns

#### Accessible Name
```html
<!-- Label association -->
<input aria-labelledby="label-id">

<!-- Direct label -->
<button aria-label="Close dialog">×</button>

<!-- Described by -->
<input aria-describedby="hint-text">
```

#### Live Regions
```html
<!-- Polite - wait for user to pause -->
<div aria-live="polite">Status: Loading...</div>

<!-- Assertive - announce immediately -->
<div aria-live="assertive" role="alert">Error: Form submission failed</div>

<!-- Atomic - announce entire region -->
<div aria-live="polite" aria-atomic="true">Items in cart: 3</div>
```

#### State Management
```html
<!-- Expanded/collapsed -->
<button aria-expanded="false" aria-controls="menu">Menu</button>

<!-- Selected -->
<div role="option" aria-selected="true">Option 1</div>

<!-- Checked -->
<div role="checkbox" aria-checked="true">Remember me</div>

<!-- Disabled -->
<button aria-disabled="true">Submit</button>

<!-- Invalid -->
<input aria-invalid="true" aria-describedby="error-msg">
```

### Common Widget Patterns

#### Modal Dialog
```html
<div role="dialog"
     aria-modal="true"
     aria-labelledby="dialog-title"
     aria-describedby="dialog-desc">
  <h2 id="dialog-title">Confirm Action</h2>
  <p id="dialog-desc">Are you sure you want to delete this item?</p>
  <button>Cancel</button>
  <button>Delete</button>
</div>
```

#### Tabs
```html
<div role="tablist" aria-label="Sample Tabs">
  <button role="tab" aria-selected="true" aria-controls="panel-1" id="tab-1">Tab 1</button>
  <button role="tab" aria-selected="false" aria-controls="panel-2" id="tab-2">Tab 2</button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">Content 1</div>
<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>Content 2</div>
```

#### Combobox (Autocomplete)
```html
<label id="cb-label">City</label>
<div role="combobox" aria-expanded="true" aria-haspopup="listbox" aria-labelledby="cb-label">
  <input type="text" aria-autocomplete="list" aria-controls="listbox-1">
  <ul role="listbox" id="listbox-1">
    <li role="option" aria-selected="true">Tokyo</li>
    <li role="option">Osaka</li>
  </ul>
</div>
```

---

## Testing Tools and Commands

### Automated Testing

```bash
# axe-core (latest: 4.11.x as of May 2026 — ~57% WCAG 2.2 A/AA SC coverage)
# Source: https://github.com/dequelabs/axe-core
npx @axe-core/cli http://localhost:3000

# Pa11y
npx pa11y http://localhost:3000

# Lighthouse
npx lighthouse http://localhost:3000 --only-categories=accessibility
```

> **Important:** No automated tool covers all WCAG 2.2 A/AA SCs. axe-core provides the highest single-tool coverage (~57%) but cannot replace manual expert review for compliance determination.

### Browser DevTools
- Chrome: Accessibility panel, Lighthouse
- Firefox: Accessibility Inspector
- Safari: Accessibility Browser

### Screen Reader Testing
| Platform | Screen Reader |
|----------|---------------|
| Windows | NVDA (free), JAWS |
| macOS | VoiceOver (built-in) |
| iOS | VoiceOver (built-in) |
| Android | TalkBack (built-in) |

---

## JIS X 8341-3:2016 (Japan)

Japanese Industrial Standard for web accessibility, originally based on ISO/IEC 40500:2012 (WCAG 2.0). Note: ISO/IEC 40500:2012 has been superseded by ISO/IEC 40500:2025 (WCAG 2.2, approved October 2025). JIS X 8341-3 has not yet been formally updated to WCAG 2.2 as of 2026 — assess Japanese government procurement against JIS X 8341-3:2016 Level AA, but note the international standard has moved to WCAG 2.2.

### Conformance Requirements

Same as WCAG 2.0 Levels A, AA, AAA with Japanese-specific guidance:
- Ruby text for kanji pronunciation
- Vertical text layout considerations
- Japanese character spacing

### Government Requirement
Japanese government websites must conform to JIS X 8341-3:2016 Level AA.

---

## Quick Reference: WCAG Mapping

| Issue | Success Criterion | Level |
|-------|-------------------|-------|
| Missing alt text | 1.1.1 | A |
| No keyboard access | 2.1.1 | A |
| Missing form labels | 1.3.1, 3.3.2 | A |
| Low contrast | 1.4.3 | AA |
| No skip link | 2.4.1 | A |
| Missing page title | 2.4.2 | A |
| Missing lang attribute | 3.1.1 | A |
| Focus not visible | 2.4.7 | AA |
| Content in images of text | 1.4.5 | AA |
| No error messages | 3.3.1 | A |
