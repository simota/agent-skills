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

### To Director (Script → Recording)

```yaml
CUE_TO_DIRECTOR_HANDOFF:
  source: Cue
  destination: Director
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

### To Reel (CLI Demo Segment)

```yaml
CUE_TO_REEL_HANDOFF:
  source: Cue
  destination: Reel
  content:
    cli_segment:
      scene: [N]
      commands:
        - command: "[shell command]"
          pause_after: "[seconds]"
          comment: "[what to highlight]"
      terminal_config:
        theme: "[dark | light]"
        font_size: [N]
        width: [columns]
      duration: "[target seconds]"
  request: "Record terminal demo segment"
```

### To Tone (Audio Specifications)

```yaml
CUE_TO_TONE_HANDOFF:
  source: Cue
  destination: Tone
  content:
    audio_needs:
      bgm:
        mood: "[upbeat | calm | corporate | energetic]"
        duration: "[seconds]"
        fade_points: ["[timestamp:fade-type]"]
      sfx:
        - trigger: "[scene transition | button click | success]"
          timing: "[timestamp]"
          style: "[subtle | prominent]"
    video_context: "[brief description of video content]"
  request: "Design BGM and sound effects for video"
```
