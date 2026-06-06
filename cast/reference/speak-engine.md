# Cast SPEAK Engine

Purpose: Define TTS engine selection, auto-derivation rules, prompt patterns, output modes, and failure handling for `SPEAK`.

Scope: Persona-driven CLI/local synthesis with `engine_preference: auto` fallback and persona-attribute → voice-name mapping. For streaming-pipeline TTS (TTSAdapter interface, AudioQueue, low-TTFA cloud engines, lip-sync phoneme timing), see `aether/reference/tts-engines.md`.

## Contents

1. Engine architecture
2. Engine selection
3. Availability checks
4. Voice mapping
5. Parameter derivation
6. Prompt patterns
7. Dialogue mode
8. Output modes
9. Error handling
10. Cost management

## Engine Architecture

| Engine | Platform | Quality | Offline | Cost | Use |
|---|---|---|---|---|---|
| `VOICEVOX` | Cross-platform | High | Yes | Free | Primary Japanese engine |
| `say` | macOS | Standard | Yes | Free | Local fallback |
| `edge-tts` | Cross-platform | High | No | Free | Network fallback |
| `google_tts` | Cross-platform | Very High | No | Paid | Explicit opt-in only |

**Engine notes (as of 2026-05):**
- VOICEVOX continues active development; v0.24.x line (released through 2025) added new speakers and styles, and Humming function covers 29+ characters as of mid-2025. Always probe the local engine version via `GET /version` before assuming speaker IDs — speaker numbering is stable but new IDs appear over time.
- For AI-generated voice clips bundled with personas, attach **C2PA Content Credentials 2.2** assertions (`spec.c2pa.org/specifications/specifications/2.2/`) to document AI-use provenance. Required when persona voice output is published externally.

## Engine Selection

### Explicit engine

- If `engine_preference` is explicit, try that engine first.
- If unavailable, trigger `ON_ENGINE_UNAVAILABLE`.
- Fallback order: `voicevox -> edge-tts -> say`

### `engine_preference: auto`

1. Try `VOICEVOX` at `localhost:50021`
2. Else try `edge-tts`
3. Else try macOS `say`
4. Else return text-only output with warning

Rules:

- Do not include `google_tts` in `auto`.
- If all engines fail, continue in text-only mode in AUTORUN.

## Availability Checks

```bash
# VOICEVOX
curl -s -o /dev/null -w "%{http_code}" http://localhost:50021/version 2>/dev/null

# macOS say
which say

# edge-tts
npx --yes edge-tts --list-voices 2>/dev/null | head -1

# Google Cloud TTS
python3 -c "from google.cloud import texttospeech; print('ok')" 2>/dev/null
test -n "$GOOGLE_APPLICATION_CREDENTIALS" && test -f "$GOOGLE_APPLICATION_CREDENTIALS"
```

## Voice Mapping

### Japanese Defaults

| Persona attribute | VOICEVOX | say | edge-tts | google_tts |
|---|---|---|---|---|
| Young female | `四国めたん:ノーマル (2)` | `Kyoko` | `ja-JP-NanamiNeural` | `ja-JP-Neural2-B` |
| Young male | `剣崎雌雄:ノーマル (46)` | `Eddy` | `ja-JP-KeitaNeural` | `ja-JP-Neural2-C` |
| Mid-age female | `九州そら:ノーマル (16)` | `Flo` | `ja-JP-NanamiNeural` | `ja-JP-Neural2-B` |
| Mid-age male | `玄野武宏:ノーマル (11)` | `Reed` | `ja-JP-KeitaNeural` | `ja-JP-Neural2-D` |
| Senior | slow rate variants | senior voice if available | slower rate | slower rate |

### English Defaults

| Persona attribute | say | edge-tts | google_tts |
|---|---|---|---|
| Young female | `Samantha` | `en-US-JennyNeural` | `en-US-Neural2-F` |
| Young male | `Alex` | `en-US-GuyNeural` | `en-US-Neural2-D` |
| Mid-age female | `Fiona` | `en-US-AriaNeural` | `en-US-Neural2-C` |
| Mid-age male | `Daniel` | `en-US-DavisNeural` | `en-US-Neural2-A` |

## Parameter Derivation

### Rate / Speed Defaults

| Signal | VOICEVOX | say | edge-tts | google_tts |
|---|---|---|---|---|
| Senior | `0.85` | `150` | `-15%` | `0.85` |
| Default | `1.00` | `180` | `+0%` | `1.00` |
| Youth / fast persona | `1.10` | `200` | `+10%` | `1.10` |

### Emotion Mapping

| Emotion | Example parameter bias |
|---|---|
| Enthusiastic / cheerful | higher pitch, higher intonation |
| Neutral | baseline values |
| Reserved / frustrated | lower pitch, lower intonation |

### `speaking_style` Derivation

| Target | Source |
|---|---|
| `formality` | category + tech level |
| `vocabulary_level` | tech level |
| `sentence_length` | Echo mapping |
| `emotional_tone` | emotion triggers |
| `linguistic_markers` | quote + source analysis |

## Prompt Patterns

### Base prompt

Use:

- persona sketch
- current context
- concise instruction
- anti-AI rule: do not sound generic, do not narrate persona metadata, do not contradict persona goals/frustrations

### Topic prompt

Use when the persona should speak about a topic.

### Reaction prompt

Use when the persona should react to a situation.

### Dialogue prompt

Use when two personas should respond to the same topic with tension and contrast.

## Dialogue Mode

### Tension Design Rules

- Contrast goals or frustrations.
- Keep each turn persona-specific.
- Avoid collapsing two personas into one voice.

### Turn Count

| Persona count | Rule |
|---|---|
| `2-3` | Normal dialogue mode |
| `4+` | Trigger `ON_DIALOGUE_COMPLEXITY` |

## Output Modes

| Mode | Result |
|---|---|
| Text only | Transcript only |
| Audio file | File output |
| Playback | Immediate playback if supported |
| Dialogue package | Multi-segment transcript/audio set |

### Transcript Format

Use exact heading:

`## SPEAK Transcript`

Then include:

- `Generated Text`
- `Voice Parameters Used`
- `Engine`
- output path when generated

## Error Handling

| Failure | Action |
|---|---|
| VOICEVOX unavailable | Fall back to `edge-tts`, then `say` |
| Synthesis timeout | Retry once, then fall back |
| Engine unavailable | Trigger `ON_ENGINE_UNAVAILABLE`, continue with fallback or text-only |
| Network timeout | Retry once, then local fallback or text-only |
| Google credentials missing | Recommend fallback instead of auto-failing |
| Quota exceeded | Warn and fall back |

## Cost Management

Rules for `google_tts`:

- Never use in `auto`.
- Use only when explicitly selected.
- Warn when the engine is unavailable or credentials/quota are missing.
- Prefer free engines unless the user explicitly requests premium quality.
