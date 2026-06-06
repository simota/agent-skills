# Motion Design Anti-Patterns

Purpose: Use this file when you need to judge whether motion is meaningful, proportional, and cognitively appropriate.

## Contents
- `MD-01` to `MD-07`
- Functional vs decorative decision test
- Timing guidance
- Motion hierarchy

## Anti-Patterns

| ID | Failure | Required Fix |
|----|---------|--------------|
| `MD-01` | Purpose-free animation | Define feedback, guidance, or state purpose, or remove it |
| `MD-02` | Visual overload | Keep simultaneous prominent motion to `2-3` items |
| `MD-03` | Cognitive fatigue | Remove repeated decorative motion |
| `MD-04` | Attention hijack | Match motion strength to content importance |
| `MD-05` | Bad timing | Use the correct duration band for the surface |
| `MD-06` | Wrong easing for the context | Use entry=`ease-out`, exit=`ease-in`, state=`ease-in-out` |
| `MD-07` | UI depends on animation to make sense | Keep full meaning in static states |

## Functional vs Decorative Decision Test

Ask:
1. If this animation disappears, does the user lose information?
2. Does it explain spatial or causal change?
3. Does it respond to user action or system state?

If all answers are `No`, the motion is decorative and should be optional.

## Timing Bands

| Use | Duration |
|-----|----------|
| Micro interaction | `100-200ms` |
| UI entry/exit | `150-300ms` |
| Panel or modal | `200-350ms` |
| Page transition | `200-500ms` |
| Complex sequence | `300-700ms` |
| Loading / skeleton | `1000ms+` |

Rules:
- `<100ms` is usually too fast for meaningful motion
- `>500ms` for basic UI often feels slow
- Exit duration is usually `60-80%` of entry duration

## Motion Hierarchy

| Level | Intensity | Typical Use |
|-------|-----------|-------------|
| `1` | subtle | color, opacity, focus |
| `2` | light | press, hover, small state change |
| `3` | standard | modal, dropdown, content transition |
| `4` | strong | page transition, major emphasis |

Keep simultaneous level-4 motion to one focal surface at a time.
