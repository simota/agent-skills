# Handoff Templates

**Purpose:** Handoff templates between Tome and other agents.
**Read when:** Confirming inter-agent collaboration formats.

---

## Incoming Handoffs

### From User (Direct Request)

```yaml
USER_TO_TOME:
  target:
    type: "[commit | pr | branch | file_range]"
    ref: "[specific reference]"
  audience:
    level: "[beginner | intermediate | advanced | auto]"
  output:
    format: "[learning_doc | glossary | decision_record | tutorial | learning_series | incremental_doc]"
  mode: "[standard | incremental | batch]"
  prev_doc: "[path to previous learning doc, if incremental]"
  notes: "[additional requests or focus areas]"
```

### From Agent (Generic Handoff)

Used by Trail, Harvest, Lens, Scout, and any other upstream agent.

```yaml
AGENT_TO_TOME_HANDOFF:
  source_agent: "[Trail | Harvest | Lens | Scout | ...]"
  investigation:
    target: "[investigation subject]"
    findings: "[key findings or data]"
    commits: "[key commit list, if applicable]"
    root_cause: "[root cause, if applicable]"
    timeline: "[change timeline, if applicable]"
  request:
    focus: "[documentation focus]"
    audience: "[target audience level or auto]"
    format: "[output format]"
```

---

## Outgoing Handoffs

### To Quill (Inline Documentation)

```yaml
TOME_TO_QUILL_HANDOFF:
  source:
    learning_doc: "[path to generated learning document]"
    key_insights: "[key insights]"
  request:
    action: "[inline comments / JSDoc / README updates]"
    target_files: "[target file list]"
    priority_items:
      - "[most important annotation point 1]"
      - "[most important annotation point 2]"
```

### To Scribe (Specification Documents)

```yaml
TOME_TO_SCRIBE_HANDOFF:
  source:
    learning_doc: "[path to generated learning document]"
    decisions: "[recorded design decision list]"
  request:
    action: "[spec/design document promotion]"
    format: "[ADR | HLD | design doc]"
    spec_candidates:
      - item: "[item to promote to spec]"
        rationale: "[why it should become a spec]"
```

### To Canvas (Visualization + Knowledge Graph)

```yaml
TOME_TO_CANVAS_HANDOFF:
  source:
    learning_doc: "[path to generated learning document]"
    flows: "[flows to visualize]"
    knowledge_graph: "[concept relationships as structured data]"
  request:
    action: "[Mermaid/ASCII diagram generation]"
    diagram_types:
      - type: "[sequence | flowchart | state | class | concept_map]"
        scope: "[diagram scope]"
        highlight: "[change portion highlight instructions]"
```

### To Lore (Knowledge Catalog)

```yaml
TOME_TO_LORE_HANDOFF:
  source:
    learning_doc: "[path to generated learning document]"
    patterns: "[extracted general patterns]"
    quality_scorecard: "[A/B/C per axis]"
  request:
    action: "[knowledge catalog registration]"
    insights:
      - pattern: "[pattern name]"
        description: "[pattern description]"
        applicability: "[applicability scope]"
```

### To Prism (Audio Learning via NotebookLM)

```yaml
TOME_TO_PRISM_HANDOFF:
  source:
    learning_doc: "[path to generated learning document]"
    audience_level: "[beginner | intermediate | advanced]"
  request:
    action: "[NotebookLM steering prompt generation]"
    focus: "[key topics for audio overview]"
    tone: "[educational | conversational | technical]"
```

### To Director (Demo Narration Scripts)

```yaml
TOME_TO_DIRECTOR_HANDOFF:
  source:
    learning_doc: "[path to generated learning document]"
    change_walkthrough: "[step-by-step change flow]"
  request:
    action: "[demo narration script generation]"
    scenes:
      - scene: "[scene description]"
        screen_capture: "[what to show on screen]"
        narration_focus: "[key teaching point]"
```
