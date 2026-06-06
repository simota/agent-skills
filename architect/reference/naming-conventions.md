# Naming Conventions

**Purpose:** Naming rules for new agents.
**Read when:** You need a short, distinctive, role-evocative agent name.

## Contents
- Core Principles
- Naming Categories
- Naming Process
- Existing Agent Names (Reference)
- Anti-Patterns
- Name Validation Checklist
- Name Ideas by Domain
- Cultural Considerations
- Naming Decision Tree

---

## Core Principles

### 1. Short and Memorable

| Preference | Syllables | Examples |
|------------|-----------|----------|
| Ideal | 1-2 | Scout, Zen, Forge, Bolt |
| Acceptable | 3 | Sentinel, Voyager, Guardian |
| Avoid | 4+ | ❌ Authenticator, ❌ Orchestrator |

### 2. Evocative of Role

The name should immediately suggest what the agent does:

| Name | Evokes | Actual Role |
|------|--------|-------------|
| Scout | Explorer, pathfinder | Bug investigator |
| Forge | Blacksmith, creation | Rapid prototyper |
| Sentinel | Guard, watchman | Security analyst |
| Zen | Calm, simplicity | Code clarity |
| Bolt | Speed, lightning | Performance optimizer |

### 3. Easy to Type

- No special characters
- No numbers
- Standard English keyboard
- Avoid similar-looking letters (l/1, O/0)

### 4. Unique in Ecosystem

- Check all current agent names
- No phonetic duplicates
- No confusing abbreviations

---

## Naming Categories

### Action-Based Names

Names that suggest what the agent does:

| Name | Action | Agent |
|------|--------|-------|
| Scout | Scouting/investigating | Bug investigator |
| Forge | Forging/creating | Prototyper |
| Sweep | Sweeping/cleaning | Dead code remover |
| Harvest | Harvesting/gathering | PR collector |

**Pattern**: `[Verb stem as noun]`

### Role-Based Names

Names that suggest a profession or role:

| Name | Role | Agent |
|------|------|-------|
| Sentinel | Guard | Security analyst |
| Guardian | Protector | PR manager |
| Sherpa | Mountain guide | Task decomposer |
| Artisan | Craftsman | Frontend specialist |

**Pattern**: `[Professional title]`

### Quality-Based Names

Names that suggest a quality or attribute:

| Name | Quality | Agent |
|------|---------|-------|
| Zen | Calm, clarity | Refactoring |
| Bolt | Speed | Performance |
| Vision | Sight, direction | Creative direction |

**Pattern**: `[Abstract quality noun]`

### Tool-Based Names

Names that suggest a tool or instrument:

| Name | Tool | Agent |
|------|------|-------|
| Radar | Detection device | Test coverage |
| Canvas | Artist's surface | Visualization |
| Anvil | Blacksmith's tool | CLI builder |
| Probe | Investigation tool | Dynamic security |

**Pattern**: `[Tool/instrument name]`

### Location-Based Names

Names that suggest a place or destination:

| Name | Location | Agent |
|------|----------|-------|
| Gateway | Entry point | API design |
| Atlas | World map | Architecture |
| Nexus | Connection hub | Orchestrator |
| Arena | Battle ground | Multi-AI |

**Pattern**: `[Place/landmark name]`

---

## Naming Process

### Step 1: Identify Core Function

```yaml
FUNCTION_ANALYSIS:
  primary_action: "[What does it DO?]"
  primary_output: "[What does it PRODUCE?]"
  primary_domain: "[What AREA does it cover?]"
```

### Step 2: Brainstorm Candidates

Generate 5-10 candidate names across categories:

```yaml
CANDIDATES:
  action_based:
    - "[Name 1]"
    - "[Name 2]"
  role_based:
    - "[Name 3]"
    - "[Name 4]"
  quality_based:
    - "[Name 5]"
    - "[Name 6]"
  tool_based:
    - "[Name 7]"
    - "[Name 8]"
```

### Step 3: Evaluate Candidates

Score each candidate:

| Criterion | Weight | Score (1-5) |
|-----------|--------|-------------|
| Brevity (syllables) | 20% | |
| Evocative power | 30% | |
| Memorability | 20% | |
| Uniqueness | 15% | |
| Typeability | 15% | |

### Step 4: Conflict Check

Verify against existing names:

```yaml
CONFLICT_CHECK:
  exact_match: [Check all current names]
  phonetic_similar: [Sounds like existing?]
  abbreviation_conflict: [Same abbreviation?]
  semantic_conflict: [Similar meaning?]
```

### Step 5: Final Selection

Select the highest-scoring name without conflicts.

---

## Existing Agent Names (Reference)

### Single Syllable (9)
- Zen, Flow, Bolt, Spark, Scout, Forge, Probe, Judge, Sweep

### Two Syllables (32)
- Nexus, Sherpa, Builder, Artisan, Radar, Voyager
- Sentinel, Guardian, Harvest, Palette, Muse, Echo
- Canvas, Atlas, Gateway, Scaffold, Anvil, Gear
- Polyglot, Growth, Bond, Pulse
- Ripple, Trail, Morph, Accord, Helm
- Stream, Launch, Grove

### Three Syllables (15)
- Experiment, Field, Vector, Triage, Compete
- Vitrine, Schema, Arena, Vision, Quill, Scribe
- Director, Architect, Frontend-Design (hyphenated)

---

## Anti-Patterns

### Names to Avoid

| Anti-Pattern | Example | Problem |
|--------------|---------|---------|
| Generic | Helper, Manager | No identity |
| Descriptive | CodeFormatter | Too literal |
| Technical | JSONParser | Implementation detail |
| Long | SecurityAuditor | Hard to type |
| Abbreviation | SecAudit | Unclear |
| Numbers | Agent1 | Meaningless |
| Version | AgentV2 | Confusing |

### Confusing Names

Avoid names that could be confused with:
- Programming concepts (Class, Function, Module)
- Common tools (Git, Docker, npm)
- Other products (Claude, Cursor, Copilot)
- Generic terms (AI, Bot, Assistant)

---

## Name Validation Checklist

Before finalizing a name:

- [ ] **Length**: 1-3 syllables
- [ ] **Spelling**: Standard English
- [ ] **Pronunciation**: Unambiguous
- [ ] **Meaning**: Evokes the role
- [ ] **Uniqueness**: No existing conflicts
- [ ] **Keyboard**: Easy to type
- [ ] **Memory**: Easy to recall
- [ ] **Context**: Works in sentences

Example validation:

```markdown
## Name Validation: Weave

- [x] Length: 1 syllable ✓
- [x] Spelling: Standard English ✓
- [x] Pronunciation: Clear (/wiːv/) ✓
- [x] Meaning: Suggests combining/integrating ✓
- [x] Uniqueness: No conflicts ✓
- [x] Keyboard: Easy (5 letters) ✓
- [x] Memory: Common word ✓
- [x] Context: "Ask Weave to integrate" ✓

**Result**: APPROVED
```

---

## Name Ideas by Domain

### Investigation Domain
- Trace, Seek, Find, Hunt, Track
- Sleuth, Detective (too long)

### Creation Domain
- Forge, Craft, Make, Build, Shape
- Sculptor, Potter (role-based alternatives)

### Security Domain
- Guard, Shield, Ward, Watch, Vigil
- Warden, Knight (role-based alternatives)

### Performance Domain
- Bolt, Flash, Swift, Quick, Rush
- Turbo, Nitro (brand associations)

### Quality Domain
- Zen, Pure, Clean, Clear, Refine
- Polish, Shine (action-based alternatives)

### Documentation Domain
- Quill, Ink, Scribe, Pen, Write
- Chronicle, Record (too formal)

### Testing Domain
- Radar, Check, Verify, Test, Prove
- Inspector (role-based alternative)

---

## Cultural Considerations

### Positive Associations
- Greek/Roman mythology (Atlas, Nexus)
- Nature (Flow, Grove)
- Crafts (Forge, Anvil, Canvas)
- Exploration (Scout, Voyager, Vector)

### Neutral Associations
- Tools (Radar, Probe)
- Roles (Guardian, Sentinel)
- Abstract concepts (Zen, Vision)

### Avoid
- Violent connotations
- Religious terms
- Culturally specific references
- Trademark conflicts

---

## Naming Decision Tree

```
START
  │
  ├─ What does the agent DO primarily?
  │   ├─ Creates things → Action-based (Forge, Build)
  │   ├─ Analyzes things → Tool-based (Radar, Probe)
  │   ├─ Guards things → Role-based (Sentinel, Guardian)
  │   └─ Improves things → Quality-based (Zen, Polish)
  │
  ├─ How long is the best candidate?
  │   ├─ 1 syllable → Ideal, use it
  │   ├─ 2 syllables → Good, use it
  │   ├─ 3 syllables → Acceptable if evocative
  │   └─ 4+ syllables → Find alternative
  │
  ├─ Is there a conflict?
  │   ├─ Yes → Find alternative
  │   └─ No → Proceed
  │
  └─ Final check: Does it pass validation?
      ├─ Yes → APPROVED
      └─ No → Revise
```
