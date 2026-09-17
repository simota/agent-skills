# Rehearsal Plan Contract

Load for `rehearsal`, not slide generation. The SKILL owns initial pacing defaults; use measured speaker/venue timing to evaluate the rehearsal. Narrative and visual design remain separate recipes; Cue owns recording execution.

## Plan and Measurement

For a 20–30 minute talk, the local planning target is 7 solo + 2 peer-audience + 1 venue pass; it is not an empirical guarantee. Record any venue/speaker-specific adjustment. Use early passes for content, later passes for timing, a recorded pass for measurement, peer passes for questions, and a final check on the actual equipment (target: 60 minutes before showtime).

Measure WPM, fillers/minute, pause count and section duration from a real recording. Completion targets: WPM within ±5 of the chosen target and fillers <1/minute. With no recording, report these as unverified goals, not achieved results. Mark pauses in speaker notes (defaults: 2 seconds after key claims, 3 seconds between sections). Budget pauses, demos, transitions and Q&A inside the hard clock.

Select venue-appropriate eye routing: `lighthouse_5_zone` (front-left/right, center, back-left/right; planned rotation), `camera_only`, or `hybrid_30s_alt`. These are plan choices, not proof of audience attention. Rehearse recovery without restarting from the beginning whenever a line is missed.

## Q&A and Contingencies

Prepare known hard questions, an honest unknown-answer response and a backup self-question. Restate unclear questions; keep multipart/hostile exchanges within the Q&A budget rather than inventing an answer.

Document at least three fallback plans: slides unavailable (offline copy/no-slide summary), demo failure (recorded fallback), and reduced time (pre-marked cuts retaining the governing idea and CTA). Check microphone, clicker, display, sound and presenter view on actual equipment. Include recover-from-blank steps and a pre-talk routine suited to the speaker. Do not prescribe dietary/breath-holding rules or guaranteed physiological effects as slide-delivery requirements.

## Output Schema

Placeholders are targets or measurements as labeled, never sample observations:

```yaml
rehearsal_plan:
  talk_duration_min: 0
  target_wpm: 0
  passes_solo: 7
  passes_live: 2
  passes_stage: 1
  recordings:
    - pass: 0
      wpm: 0
      filler_per_min: 0
      pause_count: 0
  pause_markers: []
  eye_routing: "lighthouse_5_zone | camera_only | hybrid_30s_alt"
  qa_prep:
    self_qa_backup: "<prepared question>"
    known_hard_questions: []
  contingencies:
    slides_fail: "<tested fallback>"
    demo_fails: "<artifact/path and playback check>"
    time_cut: "<explicit cuts and retained ending>"
  pre_talk_routine: []
```

Use `recordings: []` until a recording exists; populate measurements only from evidence. Accompany the plan with measured-vs-target status, explicit pause locations, Q&A backup, ≥3 contingencies and the equipment-check result. Within 24 hours of delivery, record three successes and three changes. Resolve presenter/teleprompter features from the installed renderer or chosen product; no cached app catalog or medical claims are needed.
