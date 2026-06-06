# Rehearsal and Delivery

## Purpose

Design a rehearsal protocol and delivery checklist so a speaker arrives at the stage with the talk in muscle memory, not in PowerPoint memory. Slides do not give a talk — humans do.

## Scope Boundary

- IN scope: rehearsal cadence, breathing and voice technique, pacing, pause discipline, eye-contact routing, Q&A handling, contingency plans.
- OUT of scope: narrative design (`narrative`), visual design (`visual`), slide-framework syntax (`marp`/`reveal`/`slidev`), live recording (delegate to `director`).

## Core Concepts

### The 7-2-1 Rehearsal Rule

A reliable cadence for a 20–30 minute talk:

| Pass | Goal | Format |
|------|------|--------|
| 7 | Solo, full talk, no interruption — even when you forget a line, keep going. Builds resilience. |
| 2 | Live audience of 1–3 trusted peers. Take notes after, not during. |
| 1 | Tech check + final solo run on the actual stage / equipment 60 minutes before showtime. |

Fewer than 7 solo passes correlates strongly with on-stage stumbles in the opening (the highest-attention window). Source: Patricia Fripp's coaching practice; Carmine Gallo's analysis of TED speakers' rehearsal counts.

### Speaking Pace

| Style | WPM | Use Case |
|-------|-----|----------|
| Slow / weighty | 110–130 | Keynotes, emotional moments, non-native audience |
| Conversational default | 140–160 | Most conference talks (125 was the long-standing rule; modern conference recordings cluster higher) |
| Fast / energetic | 180+ | Lightning talks, demo moments — use sparingly |

Verify pace by recording yourself reading 200 words; at 125 WPM you finish in 96 seconds, at 150 WPM in 80 seconds. Do not trust subjective feel — speakers consistently underestimate their pace under stage adrenaline.

TED2026 (Vancouver, 2026-04-13/17, theme "All of Us") again clustered its 80+ talks around 130–150 WPM despite the 18-minute hard cap; the Apple keynote pacing remains slower (~110–125 WPM) by design to let translation tracks keep up. Match the target venue's house pace, not your office rehearsal pace.

### Breathing

- **Diaphragmatic breathing** before going on: 4-second inhale through nose, 4-second hold, 6-second exhale through mouth. Three cycles. Lowers heart rate by 10–15 BPM.
- **Mid-talk breathing**: every 8–12 seconds of speech, take a half-second through the nose at a sentence break. Mouth-breathing dries the throat by minute 4 and produces the "uhmm" filler reflex.

### Pause Discipline

Pauses do four jobs: emphasis, transition, audience comprehension, speaker re-oxygenation. Rules:

- After a key sentence, pause 2 seconds. (Feels like 8 to the speaker. Audience experiences it as confidence.)
- Between major sections, pause 3 seconds and physically move on stage.
- Never fill a pause with "um", "uh", "so", "right". Track filler-word frequency in rehearsal recordings; aim for ≤ 1 per minute.

### Eye-Contact Routing

For in-person audiences, segment the room into 5 zones (front-left, front-right, center, back-left, back-right). Rotate eye contact through zones every 10–15 seconds, holding 3–5 seconds per zone. This is the "lighthouse pattern" used by Kennedy speech coaches.

For online (Zoom, YouTube live): look directly into the camera, not at the gallery. Place a small sticker beside the lens as a target.

For hybrid: alternate every 30 seconds — in-room zones, then camera, then back.

### Filler-Word Reduction

Common fillers: "um", "uh", "like", "so", "right", "you know", "kind of", "actually", "basically".

Reduction technique:

1. Record a rehearsal, transcribe with Whisper or Otter.
2. Highlight every filler. Count.
3. Replace each filler in your script with either silence (preferred) or an intentional bridge ("Now, …", "Here's why …").
4. Re-record. Compare counts. Aim for < 1 / minute by the 5th pass.

### Q&A Handling

Q&A failure modes and responses:

| Failure | Response |
|---------|----------|
| Question is unclear | Restate it: "If I'm hearing you right, you're asking …" |
| You don't know the answer | "I don't know — let me follow up by email." Honesty is high-trust. |
| Hostile / leading question | Acknowledge the underlying concern, then redirect: "I think the deeper concern is X, and on X my view is …" |
| Multi-part question | Answer one part well, defer the rest: "Two parts there. I'll take the first now and the second after." |
| Long monologue posing as a question | Wait for breath, then: "What's the question I can help with?" |
| Silence / no questions | Have one self-Q&A in the back pocket: "A common question I get is …" |

### Contingency Plans

| Failure | Plan |
|---------|------|
| Slides won't load | Have a PDF on your phone. Have a 90-second version of the talk you can deliver from memory with no slides. |
| Demo fails | Have a video backup, pre-recorded with your own narration. |
| Mic dies | Project from the diaphragm, walk closer to the front row. |
| You blank | Drink water — buys 4 seconds. Check notes. Move on. |
| Time gets cut | Have pre-marked "skip" sections in your speaker notes. Cut content, never speed up — fast talkers lose audiences. |
| Q&A goes silent | Pre-loaded self-question (above). |

### Voice Care

- Hydrate with room-temperature water; avoid ice, dairy, and coffee 2 hours pre-talk. Dairy and ice constrict the larynx; coffee dries it.
- Vocal warm-up: lip trills, humming up and down a 5-note scale, tongue twisters ("red leather, yellow leather"). 10 minutes total.
- Avoid throat-clearing — use a swallow instead. Throat-clearing is friction trauma to the vocal folds.

### Stage Movement

- Anchor moments (key sentences, demos): plant feet, no movement.
- Transition moments: walk 2–4 steps to a new spot. Treats new sections as new "scenes."
- Avoid: pacing in tight loops (signals anxiety), turning your back to the audience to read your slides, hiding behind the podium.

### Self-Recording Protocol

For every rehearsal:

- Audio: smartphone in voice-memo mode, 1 m from speaker.
- Video: locked tripod, full-body framing.
- Review with 2× speed for pacing audit, 1× for content audit.
- Note: filler counts, pause counts, energy dips, time per section.

### Teleprompter and Prompter Tools (2026-05)

For remote / hybrid talks where eye contact with the lens is critical, prompter tools allow reading notes without breaking gaze:

| Tool | Platform | Key Feature | Source |
|------|----------|-------------|--------|
| Teleprompter Pro | iOS/macOS (free) | 150K+ ratings; AirPlay mirror | https://teleprompterpro.com/ |
| PromptSmart | iOS/Android | VoiceTrack — auto-scrolls to your pace via speech recognition | https://promptsmart.com/ |
| BIGVU | iOS/Android/Web | AI Script Writer + live scroll; best for video creators | https://bigvu.tv/ |
| Teleprompter.com | Web + app | Three scroll modes, 4K recording, remote control | https://www.teleprompter.com/ |
| Presentation Prompter | macOS | Dedicated app for Keynote/PowerPoint speaker notes | https://presentationprompter.com/ |

For in-person conference talks: use Slidev's built-in presenter view (double-window mode at `/presenter`) or reveal.js speaker notes view (`S` key). Marp does not have a built-in presenter view; export to PDF for Keynote/PowerPoint presenter mode.

## Workflow

1. **Print speaker notes** with timing markers per beat.
2. **Solo Pass 1–3** — content first; do not stop for stumbles.
3. **Solo Pass 4–7** — refine pacing, mark pause locations explicitly.
4. **Record Pass 5** — measure WPM, filler count, pause count.
5. **Live Pass 8 and 9** — friendly audience; collect questions.
6. **Tech check + Pass 10** — actual venue, 60 minutes before showtime.
7. **Pre-talk routine** — hydrate, breathe (4-4-6 × 3 cycles), vocal warm-up.
8. **Stage** — execute, anchor on key beats, route eye contact, defend pauses.
9. **Post-talk** — write down 3 things that worked, 3 to fix. Within 24 hours.

## Output Template

```yaml
rehearsal_plan:
  talk_duration_min: 25
  target_wpm: 125
  passes_solo: 7
  passes_live: 2
  passes_stage: 1
  recordings:
    - pass: 5
      wpm: 132          # too fast — slow down
      filler_per_min: 3.2  # target <1
      pause_count: 8       # target ≥10 (one every ~2 min)
  pause_markers: [slide_3_after_stat, slide_7_section_break, slide_14_post_demo]
  eye_routing: lighthouse_5_zone | camera_only | hybrid_30s_alt
  qa_prep:
    self_qa_backup: "A common question is whether this scales beyond 100 agents..."
    known_hard_questions:
      - "How does this compare with [competitor]?"
      - "What about the cost?"
  contingencies:
    slides_fail: "PDF on phone + 90-sec memorized version"
    demo_fails: "Pre-recorded narrated video at /demos/fallback.mp4"
    time_cut: "Skip slides 18–22 (case study); keep 23 (CTA)"
  pre_talk_routine:
    - hydrate_room_temp_water
    - breathing_4_4_6_x3
    - vocal_warmup_10min
    - no_dairy_no_coffee_2h_before
```

## Anti-Patterns

- "I'll wing it — I know this material." Subject-matter expertise does not equal stage performance. Rehearsal is muscle memory, not knowledge.
- Reading off slides — destroys eye contact, signals unpreparedness.
- Memorizing word-for-word — the first stumble derails the whole talk. Memorize beats, not sentences (except hook and CTA).
- Rehearsing only in your head — silent practice misses 80% of real-talk variables (breath, pace, filler, voice fatigue).
- Stopping every time you stumble — trains the brain to expect breaks; you'll stumble live too.
- Skipping the tech check — projector resolution, click-advance behavior, and audio levels are highest variance failure surfaces.
- Drinking ice water on stage — vocal folds tighten under cold.
- "Any questions?" with crossed arms — body language closes the room.

## Deliverable Contract

A rehearsal plan is complete when:

- Pass cadence is documented (target: 7 solo + 2 live + 1 venue).
- WPM is measured against target ± 5 from a real recording.
- Filler frequency is measured and < 1 / minute.
- Pause locations are explicitly marked in speaker notes.
- Eye-contact routing is chosen for the venue type.
- Q&A backup self-question is written.
- At least 3 contingency plans documented.
- Pre-talk routine is written as a checklist.

## References

- Carmine Gallo, *Talk Like TED* (2014) — TED speaker rehearsal patterns.
- Patricia Fripp, *Get Yourself Promoted* and FrippVT coaching method.
- Chris Anderson, *TED Talks* (2016) — Q&A and stage presence chapters.
- Nancy Duarte, *HBR Guide to Persuasive Presentations* (2012).
- Jerry Weissman, *Presenting to Win* (2008).
- The Voice Foundation — vocal hygiene best practices for public speakers.
- University of Edinburgh study on speech rate and retention — listeners at 190+ WPM retain ~30% less than at 150 WPM; cited in https://aiaudioexpert.com/tools/speech-pace.
- TED2026, Vancouver 2026-04-13/17 ("All of Us"), 80+ talks: cluster at 130–150 WPM — https://conferences.ted.com/ted2026.
