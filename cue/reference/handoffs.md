# Cue Handoff Templates

## Receiving Handoffs

### From Saga (Narrative → Video)

```yaml
SAGA_TO_CUE_HANDOFF:
  source: Saga
  content:
    narrative: "[story or use case narrative]"
    key_moments: ["[emotional beats or turning points]"]
    characters: ["[personas involved]"]
  request: "Adapt narrative into video script"
```

### From Scribe (Specification → Tutorial Video)

```yaml
SCRIBE_TO_CUE_HANDOFF:
  source: Scribe
  content:
    specification: "[spec document path or summary]"
    target_features: ["[features to demonstrate]"]
    audience: "[technical level]"
  request: "Create tutorial video script from specification"
```

## Sending Handoffs

### To Cue Production (Script → Recording)

```yaml
CUE_TO_DEMO_HANDOFF:
  source: Cue
  destination: Cue
  content:
    script: "[path to script document]"
    recording_segments:
      - scene: [N]
        type: "[screen-recording | UI-demo]"
        url: "[starting URL]"
        actions: ["[user actions to record]"]
        duration: "[seconds]"
    resolution: "[1920x1080 | 1280x720]"
    browser_state: "[logged in | fresh | specific state]"
  request: "Record screen segments for video production"
```
