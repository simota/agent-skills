# Game Accessibility

**Purpose:** Designing accessibility into game UI from the start — color, controls, audio, difficulty, visual, motion.
**Read when:** Designing or auditing game accessibility (`a11y` recipe).

## Contents
- Designed in, not bolted on
- Reference standards
- Color & colorblindness
- Controls & input
- Audio: subtitles & captions
- Difficulty & assists
- Visual & text
- Motion & photosensitivity
- Cognitive & menus
- Tiered checklist
- Pitfalls

---

## Designed in, not bolted on

Accessibility is cheapest and best when designed from the first layout, not patched post-ship. The recurring principle: **never encode critical information in a single channel** — pair color with shape/text, pair audio with visual cues, pair precise input with alternatives. Most accessibility features also improve usability for everyone (subtitles, remapping, scalable text).

---

## Reference standards

- **Game Accessibility Guidelines** (gameaccessibilityguidelines.com) — Basic / Intermediate / Advanced tiers.
- **Xbox Accessibility Guidelines (XAG)** + Accessibility Testing (AGT).
- **Apple/PlayStation** platform accessibility features (system-level — design to cooperate with them).
- **APX** (Able Player Experiences) patterns.

Pick a target tier with the user (`A11Y_SCOPE` trigger): Baseline / Broad (platform AGT) / Comprehensive.

---

## Color & colorblindness

- ~8% of men / ~0.5% of women have color-vision deficiency (deuteranopia most common).
- **Never use color as the only signal** — add shape, icon, pattern, label, or position. (Red enemy / green ally → also use icon shape.)
- Offer **colorblind palettes** (deuteranopia, protanopia, tritanopia) or a customizable color picker for key signifiers.
- Maintain sufficient **contrast** (text and critical UI ≥ WCAG-AA-like ratios as a floor).

---

## Controls & input

- **Full remapping** of every action; alternative control schemes.
- **Toggle vs hold** for aim/crouch/sprint/interact; no required rapid mashing without an alternative.
- **Sensitivity, dead zone, invert-Y, aim assist**; one-handed and adaptive-controller friendliness.
- Avoid mandatory simultaneous multi-button or precise-timing inputs without an assist/alternative.

---

## Audio: subtitles & captions

- **Subtitles** for all dialogue, on by default or prompted at first launch; adjustable size, background opacity, and color.
- **Closed captions** for important non-speech sound (footsteps, reloads, alarms) with **direction** ("[gunfire, left]") and **speaker** labels.
- Separate **volume sliders** (master/music/SFX/voice); visual cues for audio-only signals (off-screen threat indicator).

---

## Difficulty & assists

- Offer **difficulty and assist options** (aim assist, auto-aim, slow-motion, enemy-damage scaling, skip-puzzle/skip-combat) that don't lock the *story* behind reflex/skill walls.
- Make assists **granular and non-judgmental** (no "easy = lesser" framing); allow mid-game changes.
- Separate challenge axes (combat vs puzzle vs platforming) so a player can ease one without easing all.

---

## Visual & text

- **Text scaling** and legible fonts (avoid all-caps body, decorative faces for critical text); minimum readable size floor.
- **HUD scale** and high-contrast mode.
- Don't pack critical text into tight, unscalable boxes — design layouts that tolerate larger text and localization expansion.

---

## Motion & photosensitivity

- **Reduce camera shake / motion / flashing** options; photosensitivity-safe defaults (no rapid full-screen red/white flashes; respect ~3 flashes/sec limits).
- Reduce/disable parallax and aggressive screen effects on request.
- Provide a warning for sequences with intense flashing if unavoidable.

---

## Cognitive & menus

- Clear language, consistent iconography, no time-pressured menus.
- Objective reminders / waypoint assist; reduce reliance on memory.
- For comprehensive tier: screen-reader-navigable menus, full audio menu narration.

---

## Tiered checklist

| Tier | Must include |
|------|-------------|
| **Baseline** | Colorblind-safe encoding, full remap, subtitles, text scaling, separate volume |
| **Broad (AGT)** | Baseline + closed captions w/ direction, difficulty/assist options, motion reduction, photosensitivity-safe, HUD scale |
| **Comprehensive** | Broad + screen-reader menus, audio cues for all key info, granular per-axis difficulty, cognitive-load options |

Deliver this as a checklist with each item marked in-scope or deferred (with reason) — never silently omitted.

---

## Pitfalls

- Color-only state (red/green) with no shape/text backup.
- Subtitles without captions for non-speech, or without speaker/direction.
- Difficulty that gates the story behind reflexes with no assist.
- Unscalable text / tight boxes that break with larger fonts or localization.
- Flashing/shake with no reduce option (photosensitivity risk).
- Treating accessibility as a post-launch backlog item instead of a design input.
