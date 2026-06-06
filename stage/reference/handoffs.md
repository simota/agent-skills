# Stage Handoff Templates

## Receiving Handoffs

### From Scribe (Specification → Slides)

```yaml
SCRIBE_TO_STAGE_HANDOFF:
  source: Scribe
  content:
    document_type: "[PRD | SRS | HLD | LLD]"
    key_sections: ["[section summaries]"]
    audience: "[target audience for presentation]"
    duration: "[target duration]"
  request: "Convert specification into presentation slides"
```

### From Canvas (Diagrams → Slide Embedding)

```yaml
CANVAS_TO_STAGE_HANDOFF:
  source: Canvas
  content:
    diagrams: ["[diagram paths or inline]"]
    diagram_types: ["[flowchart | sequence | ER | class]"]
    context: "[where in the presentation these belong]"
  request: "Embed diagrams into slide deck"
```

### From Tome (Learning Material → Slides)

```yaml
TOME_TO_STAGE_HANDOFF:
  source: Tome
  content:
    learning_document: "[path or inline]"
    key_concepts: ["[concept list]"]
    audience_level: "[beginner | intermediate | advanced]"
    duration: "[target duration]"
  request: "Convert learning material into presentation"
```

## Sending Handoffs

### To Director (Slides → Recording)

```yaml
STAGE_TO_DIRECTOR_HANDOFF:
  source: Stage
  destination: Director
  content:
    slide_deck: "[path to slide file]"
    framework: "[Marp | reveal.js | Slidev]"
    preview_command: "[command to launch slides]"
    recording_notes:
      - slide: [N]
        action: "[what to demonstrate on this slide]"
        duration: "[seconds]"
    total_duration: "[target video duration]"
  request: "Record presentation as demo video"
```

### To Reel (CLI Demo Segment)

```yaml
STAGE_TO_REEL_HANDOFF:
  source: Stage
  destination: Reel
  content:
    cli_segment:
      context: "[which slide this demo supports]"
      commands: ["[command sequence]"]
      expected_output: "[what the audience should see]"
      duration: "[seconds for this segment]"
  request: "Record CLI demo for presentation"
```
