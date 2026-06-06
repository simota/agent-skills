# Microcopy Patterns

ボタンラベル、ツールチップ、空状態パターンのリファレンス。

---

## Button Labels

### Action Button Patterns

| Pattern | Good | Bad | Why |
|---------|------|-----|-----|
| **Specific verb** | "Save changes" | "Submit" | User knows what happens |
| **Object included** | "Delete account" | "Delete" | Clear what's affected |
| **Outcome-focused** | "Get started" | "Continue" | Motivates action |
| **Confirm context** | "Yes, cancel order" | "OK" | Prevents mistakes |

### Primary Action Guidelines

```markdown
## Rules
1. Use verb + noun: "Create project", "Send invite"
2. Match the page context: billing page → "Update payment method"
3. Limit to 3-4 words maximum
4. Use sentence case, not Title Case or ALL CAPS
5. Avoid generic labels: "Submit", "OK", "Click here"

## Destructive Actions
- Use specific consequence: "Delete 3 files" not "Delete"
- Pair with confirmation: "This cannot be undone"
- Use warning color (red) + explicit label
```

### Button State Text

| State | Label | Example |
|-------|-------|---------|
| **Default** | Action verb | "Save changes" |
| **Loading** | Progressive verb + ... | "Saving..." |
| **Success** | Past tense + check | "Saved ✓" |
| **Error** | "Try again" or specific | "Retry save" |
| **Disabled** | Same as default (grey) | "Save changes" (greyed) |

---

## Tooltips

### When to Use Tooltips

| Use | Don't Use |
|-----|-----------|
| Icon-only buttons need text labels | Critical information (use inline text) |
| Abbreviated or truncated text | Form field instructions (use help text) |
| Additional context for power users | Mobile-primary interfaces |
| Keyboard shortcut hints | Content that needs to be read fully |

### Tooltip Writing Guidelines

```markdown
1. Keep under 150 characters (1-2 short sentences)
2. Start with a verb for actions: "Edit your profile name"
3. Use noun phrase for info: "Your current subscription plan"
4. No period for single phrases; period for full sentences
5. Don't repeat the visible label
```

### Examples

| Element | Visible | Tooltip |
|---------|---------|---------|
| Icon button | 🔔 | "Notification settings" |
| Truncated text | "Project Al..." | "Project Alpha Release v2.1" |
| Status badge | "Pro" | "Pro plan — 50 GB storage, priority support" |
| Shortcut | "Save" | "Save changes (⌘S)" |

---

## Empty States

### Empty State Structure

```
┌─────────────────────────────────────┐
│          [Illustration]             │
│                                     │
│     Primary message (what)          │
│   Secondary message (why/how)       │
│                                     │
│      [Primary CTA button]          │
│       Secondary action link         │
└─────────────────────────────────────┘
```

### Empty State Types

| Type | Tone | Example |
|------|------|---------|
| **First use** | Welcoming, encouraging | "Create your first project to get started" |
| **No results** | Helpful, suggestive | "No results for 'xyz'. Try different keywords" |
| **Cleared** | Positive, accomplished | "All caught up! No new notifications" |
| **Error** | Empathetic, actionable | "Couldn't load your data. Check your connection" |
| **Permission** | Clear, directing | "You need admin access to view this page" |

### Empty State Copy Template

```markdown
## [Feature] Empty State

### Primary message
[What the user sees — clear, concise statement]

### Secondary message
[Why it's empty OR how to fill it — 1-2 sentences max]

### CTA
[Specific action button: "Create first [item]" / "Import [items]"]

### Example:
Primary: "No team members yet"
Secondary: "Invite your team to collaborate on projects together."
CTA: "Invite team members"
```

---

## Form Labels & Help Text

### Label Patterns

| Pattern | Example | Use |
|---------|---------|-----|
| **Noun label** | "Email address" | Standard form fields |
| **Question label** | "What's your company name?" | Conversational forms |
| **Action label** | "Choose a password" | Onboarding flows |

### Help Text Guidelines

```markdown
## Rules
1. Place below the field, not in placeholder
2. Show before the user needs it (not after error)
3. Keep to one line (under 80 characters)
4. Use specific constraints: "8+ characters with a number"
5. Never duplicate the label

## Examples
✅ "We'll use this to send you order updates"
✅ "Must be at least 8 characters"
❌ "Enter your email" (duplicates label)
❌ "This field is required" (show only on error)
```

### Placeholder Text

| Do | Don't |
|----|-------|
| Show format: "MM/DD/YYYY" | Repeat the label: "Enter email" |
| Show example: "e.g., Acme Corp" | Put instructions in placeholder |
| Keep shorter than the field width | Use placeholder as the only label |

---

## AI-Context Copy Patterns

### AI Output Framing

| Context | Pattern | Example |
|---------|---------|---------|
| **Generated content** | Label AI origin clearly | "AI-generated summary" / "Suggested by AI" |
| **Confidence level** | Show certainty when useful | "High confidence match" / "This may not be accurate" |
| **Limitations** | Disclose what AI cannot do | "Based on available data as of [date]" |
| **Editable output** | Invite user to refine | "Edit this suggestion to fit your needs" |

### AI State Copy

| State | Copy Pattern | Example |
|-------|-------------|---------|
| **Processing** | Functional description (no anthropomorphism) | "Analyzing your data..." not "I'm thinking..." |
| **Partial result** | Set expectations | "Here's what we found so far. Still checking..." |
| **Low confidence** | Transparent hedging | "We're not sure about this. Please verify." |
| **AI error** | Honest + actionable | "Couldn't generate a summary. Try with a shorter input." |
| **No result** | Helpful fallback | "No suggestions available. Try rephrasing your request." |

### Anti-Anthropomorphism Rules

```markdown
## Rules
1. AI does not "think", "feel", "believe", or "understand"
2. Use "we" (the product team) or passive voice, not "I" (the AI)
3. Describe function, not cognition: "Checking..." not "Thinking..."
4. Never imply emotional states: "Ready" not "Happy to help!"
5. Be transparent about AI involvement — don't disguise AI as human

## Word Choice
Instead of          → Use
"I think..."        → "Based on the data..."
"I'm not sure..."   → "This result may not be accurate."
"I learned that..." → "The analysis shows..."
"I can help you..." → "This tool can..."
"I made a mistake"  → "The result was incorrect. Here's an update."
```

### AI Interaction Microcopy

```markdown
## Prompt Suggestions
- Use placeholder text to show expected input format
- Offer example prompts: "Try: 'Summarize this in 3 bullet points'"
- Show character/token limits when relevant

## Feedback Loops
- "Was this helpful?" [Yes / No] — keep binary
- "Report an issue" — for incorrect/harmful output
- Don't ask for feedback on every interaction (fatigue)

## Regeneration
- "Try again" / "Generate another" (not "Regenerate")
- Show that previous output is still available
- If result changes, explain: "Results may vary with each attempt"
```

---

## Conversational UI Copy

### Turn Design Copy Hierarchy

Conversational interfaces have a layered copy structure:

| Level | Definition | Copy Responsibility |
|-------|-----------|---------------------|
| **Utterance** | A single message/response | Immediate copy: labels, prompts, responses |
| **Sequence** | A related series of turns | Flow copy: progress indicators, continuity cues |
| **Activity** | A complete task within the conversation | State copy: confirmation, completion, transition |
| **Dialog** | The full conversation session | Session copy: welcome, session summary, re-entry |

### Escalation Copy Patterns (Bot → Human)

When a conversation needs to transfer from automated to human support:

```markdown
## Planned Escalation
"I'll connect you with our support team who can help with this."
"Let me bring in a specialist for this request."
"This needs a human touch — I'm transferring you now."

## Fallback Escalation (when bot cannot handle request)
"I'm not the right fit for this. Let me connect you with someone who is."
"I want to make sure you get the right help. Here's our support team."
"I've reached the limits of what I can do here. A person will take it from here."

## Rules
1. Never make the user repeat themselves after escalation
2. Pass context: "I've shared your question with the team"
3. Set expectations: "Typical response time is under 2 hours"
4. Provide fallback: offer async channel if live support is unavailable
```

### Fallback Design Principles

Fallback responses are first-class content — treat them with the same priority as the core experience:

| Principle | Application |
|-----------|-------------|
| **Acknowledge the failure** | "I didn't catch that" not silent redirect |
| **Stay in voice** | Fallbacks use the same tone as normal responses |
| **Offer a path forward** | Always provide an alternative action or channel |
| **Limit fallback loops** | After 2 fallbacks, escalate or offer human handoff |
| **Avoid "I don't understand"** | Reframe as "That's outside what I can help with" |

```markdown
## Fallback Copy Patterns
"I'm not sure I understood that. Could you try rephrasing?"
"That's outside what I can help with here. [Alternative action]"
"I didn't get that — want to try one of these options instead?"
[Show 2-3 quick reply suggestions]
```

### Persona Consistency Across Turns

Voice and tone must remain consistent regardless of conversation state:

```markdown
## Rules
1. Define persona traits before writing any turn copy
2. Test persona under stress: error states, confusion, escalation
3. Persona in errors: if the bot is "friendly and direct", errors must be too
4. No personality switching: don't go formal when things go wrong
5. Document persona decisions in the voice framework

## Consistency Checklist
- [ ] Welcome message and error message use the same voice
- [ ] Escalation copy matches the brand tone
- [ ] Fallback copy is not more formal or robotic than normal turns
- [ ] Confirmation messages feel like the same "person" as onboarding
```

### Multimodal Copy Alignment

When copy appears alongside voice, images, or touch:

| Modality | Copy Adaptation |
|----------|----------------|
| **Voice output** | Short sentences; no markdown; numbers spelled out |
| **Image + text** | Alt text must carry the same message as visual |
| **Touch/gesture** | Label alternatives: "Tap or say 'confirm'" |
| **Screen + voice** | Screen text = visual anchor; voice = elaboration |

---

## AI UX Copy

### Uncertainty Expression Patterns

When AI confidence is limited, communicate it without undermining trust:

| Confidence Level | Copy Pattern | Example |
|-----------------|-------------|---------|
| **High** | State directly | "Based on your history, here's what we found." |
| **Medium** | Hedge lightly | "Based on available data, this looks like..." |
| **Low** | Disclose clearly | "This may not be accurate — please verify before acting." |
| **Unknown** | Acknowledge limits | "We don't have enough information to give a confident answer." |

### Confidence Indicators

Adjust tone based on confidence — not just the content:

```markdown
## High Confidence
- Use active voice and present tense
- State findings directly: "Your order ships tomorrow."

## Medium Confidence
- Use "Based on..." or "It appears that..."
- Invite review: "Does this look right to you?"

## Low Confidence
- Lead with the uncertainty: "We're not certain, but..."
- Offer verification path: "Check [source] to confirm"
- Use passive/conditional: "This may be..." / "It's possible that..."
```

### Anti-Anthropomorphism Guidelines

AI systems must not pretend to have human experiences:

```markdown
## Prohibited Framing
"I learned that..." → "The model was trained on..."
"I think..." → "Based on the data..."
"I feel confident..." → "This result has high confidence."
"I made a mistake" → "The output was incorrect."
"I understand how you feel" → "This sounds frustrating."
"I'm happy to help" → "Here's what this tool can do."

## Rules
1. AI does not feel, think, believe, or understand
2. Use "we" (product team) for brand voice, not "I" (AI)
3. Describe what the system does, not what it experiences
4. Never simulate empathy — acknowledge the user's situation instead
```

### Hallucination Disclaimers

For outputs that may contain AI-generated errors:

```markdown
## Standard Disclaimer Pattern
"AI-generated content. Verify important information before acting."
"This was created by AI. Please review for accuracy."
"Generated by AI — may contain errors or outdated information."

## Context-Specific Variants
Medical/Legal: "This is not professional advice. Consult a qualified expert."
Financial: "For reference only. This is not financial advice."
Research: "AI-generated summary. Check original sources for accuracy."

## Placement Rules
- Inline (preferred for short outputs): directly below the content
- Modal (for high-stakes outputs): require acknowledgment before proceeding
- Persistent badge: for interfaces where all content is AI-generated
```

### Attribution and Citation Patterns

When AI draws on sources, attribute clearly:

```markdown
## Patterns
"Source: [Name], accessed [date]"
"Based on [document/data set]"
"This summary references [X] sources — view all"

## Rules
1. Always link to primary source when available
2. Show recency: "Data as of [date]"
3. If source is unavailable: "Based on training data through [date]"
4. Never fabricate citations
```

### Framing Labels

Label AI-generated content clearly without making it feel dangerous:

| Label | When to Use |
|-------|-------------|
| "AI suggestion" | Optional recommendations |
| "AI draft" | Editable generated content |
| "AI summary" | Condensed content |
| "Reference only" | Informational, non-actionable output |
| "Needs review" | High-stakes content requiring human verification |

### Processing State Microcopy

During AI operations, set accurate expectations:

| State | Copy Pattern | Notes |
|-------|-------------|-------|
| **Generating** | "Generating your summary..." | Use progressive verb |
| **Waiting** | "Almost there..." / "Still working..." | Use after 3+ seconds |
| **Processing** | "Analyzing your data..." | Describe the action, not the AI |
| **Partial result** | "Here's what we have so far. Still working..." | Show progress |
| **Error** | "Couldn't generate a result. Try with different input." | Actionable |
| **Timeout** | "This is taking longer than expected. Try again." | Honest + actionable |
