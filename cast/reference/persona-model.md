# Cast Persona Model

Purpose: Define the canonical Echo-compatible persona schema, Cast extension fields, detail levels, and confidence rules.

## Contents

1. Frontmatter schema
2. SPEAK extension
3. Section structure
4. Echo mapping
5. Confidence model
6. Detail levels
7. Backward compatibility

## Frontmatter Schema

### Echo Standard Fields

| Field | Required | Notes |
|---|---|---|
| `name` | Yes | Persona display name |
| `service` | Yes | Service or product identifier |
| `type` | Yes | `user` or `internal` |
| `category` | Yes | Persona family used across the ecosystem |
| `created` | Yes | ISO date |
| `source` | Yes | Primary creation evidence |

### Cast Extension Fields

| Field | Required | Notes |
|---|---|---|
| `version` | No | Default `1.0` |
| `status` | No | `draft`, `active`, `evolved`, `archived` |
| `updated` | No | ISO date |
| `evolution_count` | No | Increment on each accepted evolution |
| `confidence` | No | `0.0-1.0` |
| `tags` | No | Search and grouping tags |
| `echo_base_mapping` | No | Echo persona anchor |
| `cast_managed` | No | Boolean flag for Cast-managed records |

### Cast SPEAK Extension Fields

Use `voice_profile` only when `SPEAK` mode is needed.

| Field | Notes |
|---|---|
| `speaking_style.formality` | `casual`, `neutral`, `formal`, `technical` |
| `speaking_style.vocabulary_level` | `simple`, `moderate`, `advanced` |
| `speaking_style.sentence_length` | `short`, `medium`, `mixed` |
| `speaking_style.emotional_tone` | Persona voice tone |
| `speaking_style.linguistic_markers` | Recurrent phrasing markers |
| `voicevox.*` | Japanese-first TTS settings |
| `say.*` | macOS fallback settings |
| `edge_tts.*` | Cross-platform network fallback |
| `google_tts.*` | Explicit paid engine only |
| `engine_preference` | `auto`, `voicevox`, `say`, `edge-tts`, `google_tts` |

### Key SPEAK Parameter Ranges

| Field | Range / Rule |
|---|---|
| `voicevox.speed` | `0.5-2.0` |
| `voicevox.pitch` | `-0.15-0.15` |
| `voicevox.intonation` | `0.0-2.0` |
| `voicevox.volume` | `0.0-2.0` |
| `say.rate` | `90-300` WPM |
| `google_tts.speaking_rate` | `0.25-4.0` |
| `google_tts.pitch` | `-20.0 to +20.0` semitones |
| `google_tts.volume_gain_db` | `-96.0 to +16.0` |

## Status Values

| Status | Meaning | Typical next state |
|---|---|---|
| `draft` | Generated but not sufficiently validated | `active` |
| `active` | Validated and in use | `evolved`, `archived` |
| `evolved` | Transitional state during accepted change | `active` |
| `archived` | Preserved but no longer active | — |

## Section Structure

### Required Sections

- `## Profile`
- `## Quote`
- `## Goals`
- `## Frustrations`
- `## Key Behaviors`
- `## Emotion Triggers`
- `## Context Scenarios`
- `## JTBD`
- `## Echo Testing Focus`
- `## Source Analysis`
- `## Evolution Log`

### Optional Sections

- `## Demographics`
- `## Psychographics`
- `## Digital Behavior`
- `## Literacy & Experience`
- `## Social Context`
- `## Life Stage`
- `## Internal Profile`
- `## Workflow Context`

## Echo Base Persona Mapping

| Echo mapping | Use when the dominant trait is |
|---|---|
| `Newbie` | Low familiarity, high guidance need |
| `Power User` | High proficiency, shortcut-oriented |
| `Mobile User` | Mobile-primary, context-constrained |
| `Senior` | Deliberate pace, clarity-first |
| `Internal` | Team workflow or operational persona |

Rules:

- Every Cast persona should map to one Echo base persona.
- Keep the mapping aligned with the dominant behavioral trait, not demographics alone.
- Changing `echo_base_mapping` is a significant evolution signal.

## Confidence Model

### Source Contributions

| Source | Contribution |
|---|---|
| Research interview | `+0.30` |
| Session replay / behavioral evidence | `+0.25` |
| Feedback / review evidence | `+0.20` |
| Analytics | `+0.20` |
| Code / workflow evidence | `+0.15` |
| README / static docs | `+0.10` |

### Validation Contributions

| Validation step | Contribution |
|---|---|
| Proto-persona baseline | `0.30` |
| Interview validation | `+0.20` |
| Survey validation | `+0.15` |
| ML clustering validation | `+0.20` |
| Triangulation bonus | `+0.10` |

### Decay Rules

| Age since update | Rule |
|---|---|
| `<30` days | No decay |
| `30-60` days | `-0.05/week` |
| `60-90` days | `-0.10/week` |
| `90+` days | Freeze value and recommend archival review |

### AI Generation Rule

- AI-only generation is capped at `0.50`.
- Raise confidence only after human review and real-data validation.

## Detail Levels

| Level | Use when | Typical sections |
|---|---|---|
| `Minimal` | Sparse evidence, quick generation | Required sections only |
| `Standard` | Normal product persona work | Required + select optional sections |
| `Full` | Rich evidence across multiple dimensions | Required + most optional sections |
| `Internal` | Team / workflow persona | Required + `Internal Profile` + `Workflow Context` |

## Backward Compatibility

- If Cast fields are missing, infer safe defaults:
  - `version: "1.0"`
  - `status: active`
  - `confidence: 0.50`
- Existing non-Cast consumers must still be able to read the persona.
- Preserve Echo-required sections even when Cast extensions are absent.
