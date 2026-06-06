# Voice & Tone Framework

ボイス属性定義、トーンスペクトラム、単語選択ガイドのリファレンス。

---

## Voice vs Tone

| Concept | Definition | Analogy |
|---------|-----------|---------|
| **Voice** | Brand personality — consistent across all contexts | Your personality |
| **Tone** | Emotional inflection — adapts to situation | Your mood |

```
Voice is WHO we are (constant).
Tone is HOW we say it (varies by context).

Same voice, different tones:
  Success: "Your order is on its way! 🎉"
  Error:   "We hit a snag with your order. Here's what to do."
  Warning: "Your trial ends in 3 days. Upgrade to keep your data."
```

---

## Voice Attribute Definition

### Template

```markdown
## Voice Attribute: [Name]

### We are:
[Positive description — 1 sentence]

### We are NOT:
[What to avoid — 1 sentence]

### This sounds like:
✅ [Example of this attribute done well]

### This does NOT sound like:
❌ [Example of going too far]
```

### Common Voice Attributes

| Attribute | We Are | We Are Not |
|-----------|--------|-----------|
| **Clear** | Direct and easy to understand | Oversimplified or condescending |
| **Friendly** | Warm and approachable | Overly casual or unprofessional |
| **Confident** | Assured and knowledgeable | Arrogant or dismissive |
| **Helpful** | Proactively guiding the user | Pushy or patronizing |
| **Honest** | Transparent about limitations | Blunt or alarming |

### Voice Definition Worksheet

```markdown
## Our Brand Voice

### Core Attributes (pick 3-4)
1. [Attribute]: [1-sentence definition]
2. [Attribute]: [1-sentence definition]
3. [Attribute]: [1-sentence definition]

### Voice Spectrum
For each attribute, define the range:

[Attribute]: |----◆-----------|
             Too little  Right  Too much

Example:
Friendly:    |--------◆-------|
             Cold     Warm    Goofy

### Voice Don'ts
- Never [specific behavior]
- Avoid [specific pattern]
- Don't [specific language choice]
```

---

## Tone Spectrum

### Context-Based Tone Adjustment

| Context | Tone | Energy | Formality |
|---------|------|--------|-----------|
| **Onboarding** | Welcoming, encouraging | High | Low |
| **Success** | Celebratory, positive | High | Low |
| **Normal operations** | Neutral, clear | Medium | Medium |
| **Warning** | Serious, helpful | Medium | Medium-High |
| **Error** | Empathetic, calm | Low | Medium |
| **Security/Legal** | Serious, precise | Low | High |
| **Billing/Payment** | Clear, trustworthy | Low | High |

### Tone Mapping Template

```markdown
## Situation: [Context]

### Emotional state of user:
[What the user is likely feeling]

### Our tone:
[How we should sound]

### Example copy:
[Actual text in this tone]

### Tone markers:
- Sentence length: [short/medium/long]
- Contractions: [yes/no]
- Emoji: [yes/sparingly/no]
- Exclamation marks: [yes/sparingly/no]
- Humor: [appropriate/avoid]
```

---

## Word Choice Guide

### Preferred Vocabulary

| Instead of | Use | Why |
|-----------|-----|-----|
| "Invalid" | "Not recognized" / specific issue | Less accusatory |
| "Error" | "Problem" / "Issue" | Less technical |
| "Failed" | "Couldn't" / "Wasn't able to" | Softer |
| "Abort" | "Cancel" / "Stop" | Less alarming |
| "Terminate" | "End" / "Close" | More human |
| "Forbidden" | "You don't have access" | Clearer |
| "Deprecated" | "No longer supported" | Plain language |
| "Null/undefined" | "Not set" / "Missing" | Non-technical |

### Inclusive Language

| Avoid | Prefer | Reason |
|-------|--------|--------|
| "Whitelist/Blacklist" | "Allowlist/Blocklist" | Inclusive terminology |
| "Master/Slave" | "Primary/Replica" | Inclusive terminology |
| "Guys" | "Everyone" / "Team" | Gender-neutral |
| "Sanity check" | "Confidence check" / "Verify" | Mental health sensitivity |
| "Dummy" | "Placeholder" / "Sample" | Respectful language |

### Jargon Translation

| Technical | User-Facing |
|-----------|-------------|
| "Authenticate" | "Sign in" |
| "Repository" | "Project" (if non-dev audience) |
| "Payload" | "Data" / "Content" |
| "Latency" | "Response time" / "Speed" |
| "Cache" | "Saved copy" (if non-dev) |

---

## Voice Audit Checklist

```markdown
## Content Review

### Voice Consistency
- [ ] Matches defined voice attributes
- [ ] Doesn't slip into a different brand personality
- [ ] Consistent across this feature/flow

### Tone Appropriateness
- [ ] Matches user's emotional context
- [ ] Not too casual for serious situations
- [ ] Not too formal for casual interactions
- [ ] Energy level matches the moment

### Word Choice
- [ ] No jargon (or jargon is appropriate for audience)
- [ ] Inclusive language used throughout
- [ ] Active voice preferred
- [ ] Consistent terminology (same concept = same word)

### Clarity
- [ ] Scannable (short sentences, clear structure)
- [ ] One idea per sentence
- [ ] No ambiguous pronouns or references
```

---

## Conversational UI & AI Assistant Tone

### Tone Mapping for AI Contexts

| Context | Tone | Key Rules |
|---------|------|-----------|
| **AI assistant greeting** | Neutral, helpful | No "Hi, I'm [Name]!" — state capability |
| **AI-generated result** | Factual, transparent | Label as AI-generated; show confidence |
| **AI error / no result** | Honest, calm | "Couldn't find an answer" — no apology spiral |
| **AI suggestion** | Supportive, non-pushy | "You might try..." not "You should..." |
| **Handoff to human** | Reassuring | "Connecting you with a team member who can help" |

### Chatbot Personality Guidelines

```markdown
## Rules
1. Define bot personality as a subset of brand voice (not a separate character)
2. Personality should be felt, not declared ("I'm friendly!" = wrong)
3. Keep responses brief — conversational UI has less reading tolerance
4. Use "we" (the product/company), not "I" (the bot)
5. Never pretend to be human — disclose AI nature when asked
6. Avoid filler phrases: "Great question!", "Sure thing!", "Absolutely!"

## Escalation Copy
- "I can help with [scope]. For [out-of-scope], let me connect you with our team."
- "This is beyond what I can assist with. Here's how to reach support: [link]"
- Never: "I don't know" without a next step
```

### AI Tone Spectrum

```
Informational ←────────→ Conversational
  "Results for 'query'"    "Here's what I found for 'query'"

Confident ←────────→ Hedging
  "The answer is X"        "Based on available data, X appears likely"

Concise ←────────→ Explanatory
  "3 results found"        "I found 3 results matching your criteria"

Use LEFT side for: dashboards, data, status
Use RIGHT side for: onboarding, help, guidance
Match the context — never default to conversational.
```
