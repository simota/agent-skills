# Director — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Director-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Director
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    demo_type: "[product demo | onboarding | stakeholder | comparison | persona | vision-stream | multi-aspect]"
    feature: "[feature name]"
    archetype: "[30s social | 60s producthunt | 90s linkedin | 180s walkthrough | 3x45s series]"
    aspect_variants: ["16:9", "9:16", "4:5", "1:1"]   # actually produced
    video_paths:
      master: "[path to 1920×1080 master .webm]"
      "16:9": "[path or null]"
      "9:16": "[path or null]"
      "4:5": "[path or null]"
      "1:1": "[path or null]"
    duration: "[seconds]"
    resolution: "[WxH]"
    captions:
      closed_vtt: "[path]"
      burned_in_mp4: "[path or null]"
      languages: ["en", "ja", ...]
    transcript: "[plaintext path]"
    videoobject_jsonld: "[path]"
    quality:
      scorecard: "[X / 97]"
      vmaf: "[≥ 90]"
      psnr_db: "[≥ 40]"
      ssim: "[≥ 0.95]"
      lufs: "[-14 | -16]"
      wcag: "1.2.2 ✓ / 1.2.4 N/A / 1.2.5 ✓"
      verdict: "ship | ship-with-fixes | reshoot"
  Artifacts: [scenario, master video, aspect variants, captions, transcript, JSON-LD, thumbnail set, checklist, quality report, or NONE]
  Next: Vitrine | Quill | Growth | VERIFY | DONE
  Reason: [blocking issue or packaging justification]
```
