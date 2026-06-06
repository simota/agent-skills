# Intent Clarification (absorbed from Cipher)

**Purpose:** Interpretation method for ambiguous user requests.
**Read when:** The request is vague and routing depends on resolving intent first.
**See also:** After resolving intent, see `routing-explanation.md` for how to present the chosen chain (and alternatives) back to the user.

Methodology for decoding ambiguous user intent before agent routing. Previously a standalone agent (Cipher), now integrated as a Nexus capability.

---

## The Three Laws

1. **No Interpretation Without Context**: git log → .agents/PROJECT.md → conversation history. Context reveals intent. Words are noise.
2. **Ambiguity is Sin, Over-Questioning Also Sin**: Context clear → Proceed. 2+ valid paths → Ask. Safe default → Proceed. Don't block flow.
3. **Never Hide Assumptions**: Always state "I interpreted this as..." "I'm assuming that..." Hidden assumptions are time bombs.

---

## Process: GATHER → READ → DECIDE → OUTPUT

| Phase | Actions |
|-------|---------|
| **GATHER** | git log · .agents/PROJECT.md · conversation history · resolve pronouns ("it", "that", "this") |
| **READ** | Interpret tone, scope, urgency (see patterns below) |
| **DECIDE** | Single interpretation → Proceed · Multiple valid → Ask · Safe default → Proceed |
| **OUTPUT** | Structured clarification with assumptions documented |

---

## Tone & Scope Interpretation Patterns

| Signal | Interpretation | Action |
|--------|---------------|--------|
| "Fix this" / "Please fix it" | Bug fix, specific target | Check git diff/status for context |
| "Improve" / "Enhance it" | Enhancement, broad scope | Narrow scope via recent activity |
| "Something is wrong" | Vague bug report | Investigate before interpreting |
| "Make it better" | Quality improvement | Check recent Judge feedback |
| Frustrated tone | User wants action, not questions | Use safest default, proceed |
| Technical terms used | User knows domain | Match precision level |
| Vague keywords | Scope ambiguity | Check .agents/PROJECT.md context |

### Scope Detection

| Keyword | Likely Scope | Example |
|---------|-------------|---------|
| "the button" / "this component" | Minimal (1 file) | Specific element fix |
| "the auth flow" / "login" | Moderate (feature) | Feature-level change |
| "the whole app" / "overall" | Extensive (system) | System-wide concern |
| "everything" / "all of it" | Over-scope → narrow down | Ask one clarifying question |

---

## CIPHER_GATE Integration

The following rules apply as an internal Nexus capability (previously the Cipher integration protocol):

- Trigger: context_confidence < 0.60, multiple valid interpretations, or missing critical context
- Auto-clarification: Nexus attempts to resolve using gathered context
- Single question: If still ambiguous, ask ONE focused question with options
- Confidence boost: +0.20 on successful clarification

---

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Better |
|-------------|---------------|--------|
| Asking what user already said | Wastes trust | Re-read conversation |
| Multiple questions in sequence | Blocks flow | One question max |
| "What do you mean?" (open-ended) | Too vague | Offer specific options |
| Interpreting without any context | Guessing | Always gather first |
| Assuming domain expertise | May confuse user | Match user's language level |

---

## Learning Loop

Record interpretation patterns in `.agents/nexus.md`:

```yaml
vocabulary_corrections:
  - phrase: "[User's phrase]"
    means: "[Actual meaning in this project]"
    context: "[When this applies]"
```
