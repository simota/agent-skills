# Video Bug Report Analysis Reference

**Purpose:** Pipeline and contracts for analyzing screen-recording bug reports. Local frame extraction (Python) feeds key frames to Codex CLI for VLM-based bug detection, then normalizes results into Scout's standard investigation report.
**Read when:** The bug report includes a screen recording (MP4 / MOV / WebM) and the `video` Recipe is active, or `vague-report-handling.md` `P06` was inferred and the input is a video.

## Contents

- Pipeline overview
- Codex CLI integration
- JSON output schema
- Prompt template
- Frame extraction module (Python spec)
- Confidence scoring (visual evidence)
- Failure modes and recovery
- Privacy and compliance
- Scout workflow integration

## Pipeline Overview

```
[1] PREPROCESS    →  [2] EXTRACT      →  [3] ANALYZE       →  [4] VALIDATE      →  [5] REPORT
    Python local      Python local        Codex CLI            Python local         Scout phase
    ─────────────     ─────────────       ─────────────        ─────────────        ─────────────
    resize 1280px     PySceneDetect       codex exec           JSON Schema          Investigation
    PII mask          + absdiff           --image *.jpg        + evidence_frames    Report
    ffprobe PTS       + pHash dedup       --output-schema      sanity check         + Fix Prompt
                      → 8-15 frames       --sandbox read-only  + confidence ≥ 0.7
                      + metadata.json     --ephemeral
```

| Stage | Owner | Output | Failure → |
|-------|-------|--------|-----------|
| `1 PREPROCESS` | Python | normalized.mp4 + meta | Skip if dimensions already ≤ 1280px; record actual values |
| `2 EXTRACT` | Python | `frames/frame_NNN.jpg` + `metadata.json` | If `0` frames extracted → escalate to `vague-report-handling.md` |
| `3 ANALYZE` | Codex CLI | `analysis.json` (stdout) | Schema violation → 1 retry → human review queue |
| `4 VALIDATE` | Python | validated.json | `confidence < 0.7` → human review queue |
| `5 REPORT` | Scout | Investigation Report | Standard Scout output contract |

## Codex CLI Integration

### Preflight

Run before stage 3. If preflight fails, suppress LLM Fix Prompt and emit a `Codex CLI unavailable` note in the Scout report.

```bash
codex --version || { echo "codex CLI missing"; exit 1; }
codex auth status >/dev/null 2>&1 || { echo "codex auth required"; exit 1; }
```

### Call Pattern

Model selection is intentionally **not** specified. The active model follows `~/.codex/config.toml` or the CLI's default. This keeps Scout decoupled from model lifecycle changes and respects user / CI profile settings.

```bash
codex exec \
  -i frames/frame_001.jpg \
  -i frames/frame_002.jpg \
  ...
  -i frames/frame_NNN.jpg \
  --output-schema scout/schemas/video-bug-detection.schema.json \
  --sandbox read-only \
  --ephemeral \
  --skip-git-repo-check \
  --add-dir frames/ \
  "$(cat scout/prompts/video-bug-detection.md)"
```

### Required Flags

| Flag | Purpose | Why |
|------|---------|-----|
| `-i <FILE>` (repeated) | Attach frames | One per key frame, in time order |
| `--output-schema <FILE>` | Force JSON output | Downstream parsing depends on schema; free-form text breaks the pipeline |
| `--sandbox read-only` | Restrict FS writes | Analyzer must not modify the workspace |
| `--ephemeral` | No session persistence | Each video is independent; no context carryover |
| `--skip-git-repo-check` | Allow non-repo dirs | Frames may live in temp dirs outside any git repo |
| `--add-dir frames/` | Allow read of frame dir | Sandbox needs explicit read permission for the frame directory |

### Optional Flags

| Flag | When |
|------|------|
| `--profile <name>` | CI / test environments needing a non-default model |
| `-c "key=value"` | Override single config (e.g. `-c sandbox_permissions=...`) |
| `--oss --local-provider lmstudio` | Local provider fallback (offline / privacy-strict envs) |

## JSON Output Schema

Place at `scout/schemas/video-bug-detection.schema.json`. Loaded by `--output-schema`.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "VideoBugDetection",
  "type": "object",
  "required": ["verdict", "evidence_frames", "confidence"],
  "properties": {
    "verdict": {
      "type": "string",
      "enum": ["bug", "no_bug", "uncertain"]
    },
    "screen_id": {
      "type": ["string", "null"],
      "description": "Identifier of the screen / view if recognizable; null otherwise."
    },
    "bug_type": {
      "type": ["string", "null"],
      "enum": [
        "layout_break",
        "error_dialog",
        "freeze_or_blank",
        "wrong_state",
        "ocr_or_text_error",
        "navigation_error",
        "other",
        null
      ]
    },
    "evidence_frames": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["frame", "timestamp_ms", "observation"],
        "properties": {
          "frame": {"type": "integer", "minimum": 0},
          "timestamp_ms": {"type": "integer", "minimum": 0},
          "region": {
            "type": ["array", "null"],
            "items": {"type": "integer"},
            "minItems": 4,
            "maxItems": 4,
            "description": "[x, y, w, h] in pixels of the affected region; null if whole frame."
          },
          "observation": {"type": "string", "minLength": 5}
        }
      }
    },
    "reproduction_steps": {
      "type": "array",
      "items": {"type": "string"}
    },
    "root_cause_hypothesis": {
      "type": ["string", "null"]
    },
    "confidence": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "uncertain_reason": {
      "type": ["string", "null"],
      "description": "Required when verdict is 'uncertain' or confidence < 0.7."
    }
  }
}
```

### Field Contracts

| Field | Rule |
|-------|------|
| `verdict` | `bug` only when at least 1 evidence frame has a concrete observation |
| `evidence_frames[].frame` | Must be a valid index in `metadata.json` |
| `evidence_frames[].timestamp_ms` | Must come from `metadata.json[frame].timestamp_ms`, not invented |
| `confidence` | `< 0.7` → human review queue; suppress `LLM Fix Prompt` |
| `uncertain_reason` | Mandatory if `verdict = uncertain` |

## Prompt Template

Place at `scout/prompts/video-bug-detection.md`. The body below is the full prompt — do not add the schema inline; `--output-schema` enforces it.

````markdown
You are a senior QA engineer analyzing a screen recording submitted as a bug report.

# Inputs

- A sequence of key frames extracted from a screen recording, attached in time order.
- Each frame is identified by its position in the attachment list (frame 0 = first attached image).
- Frame metadata (timestamps, motion scores) is provided in the user message as JSON.

# Task

1. Inspect each frame and identify the screen / view if possible.
2. Compare frames in temporal order to detect anomalies: layout breakage, error dialogs, frozen or blank screens, wrong navigation, text or OCR errors, unexpected state.
3. Cite **only visual evidence**. Every claim must reference a specific frame index and, when applicable, an `[x, y, w, h]` region.
4. If you cannot determine a bug from the frames, return `verdict: "uncertain"` with `uncertain_reason`. Do not invent observations.
5. If the frames clearly show normal behavior, return `verdict: "no_bug"`.

# Constraints

- Do not speculate beyond visible evidence.
- Do not assume application logic that is not observable.
- Use frame indices and timestamps verbatim from the metadata; do not invent values.
- `reproduction_steps` should be derived from observed user actions only.
- If the screen contains text in a non-English language, transcribe it as-is in `observation`.

# Output

Emit a single JSON object conforming to the attached schema (`video-bug-detection.schema.json`). No prose outside the JSON.
````

### Few-Shot Strategy

Inline few-shot examples are intentionally omitted from the prompt to keep the token budget for the actual frames. If recall regresses on a golden set, inject 1 positive (`bug`) + 1 negative (`no_bug`) example as additional `--image` attachments preceded by labeled metadata in the user message.

## Frame Extraction Module (Python Spec)

Implementation lives in the consuming project, **not** in this skill repo. The contract below is what Scout assumes.

### Module Layout

```
video_bug_analysis/
├── __init__.py
├── extractor.py          # main entry
├── preprocess.py         # resize, PII mask, ffprobe
├── scene_detect.py       # PySceneDetect AdaptiveDetector wrapper
├── motion_sample.py      # absdiff sampling within scenes
├── dedup.py              # pHash deduplication
└── schema.py             # metadata.json model
```

### Entry Point

```python
def extract_frames(
    video_path: str,
    output_dir: str,
    *,
    max_frames: int = 15,
    min_frames: int = 5,
    target_long_edge: int = 1280,
    pii_mask: bool = True,
) -> ExtractionResult: ...
```

### Result Type

```python
@dataclass
class FrameMetadata:
    frame: int                   # 0-based index in the output list
    path: str                    # absolute path to JPEG
    timestamp_ms: int            # PTS-derived; never frame-number derived
    motion_score: float          # 0.0-1.0, scene transition magnitude
    is_forced: bool              # True for first / last / long-static center

@dataclass
class ExtractionResult:
    frames: list[FrameMetadata]  # length: min_frames..max_frames
    duration_ms: int
    source_resolution: tuple[int, int]
    normalized_resolution: tuple[int, int]
    pii_masked: bool
    metadata_json_path: str      # serialized FrameMetadata list
```

### Algorithm

1. **Preprocess**: Probe with `ffprobe -show_streams` for resolution, FPS, duration. Resize long edge to `target_long_edge` (Lanczos). If `pii_mask=True`, run OCR + redact regions matching PII patterns before further processing.
2. **Scene detect**: Run `PySceneDetect` with `AdaptiveDetector` (defaults). Collect scene boundaries as candidate frames.
3. **Motion sample**: Within each scene longer than 0.5s, compute `absdiff` between adjacent frames; pick local maxima up to 1-3 per scene.
4. **Force include**: First frame, last frame, and the midpoint of any static region longer than 2s (catches static-state bugs like layout break).
5. **Dedup**: Compute `pHash` for all candidates; remove near-duplicates (Hamming distance ≤ 5).
6. **Cap**: Trim to `max_frames`, prioritizing forced frames + highest motion_score. Floor at `min_frames` if less candidates exist (use raw scene boundaries).
7. **Serialize**: Write JPEGs (quality 90) and `metadata.json` to `output_dir`.

### Dependencies

```
scenedetect>=0.7
opencv-python
numpy
imagehash
ffmpeg-python
pillow
# optional for PII mask:
pytesseract  # or paddleocr
```

### Performance Target

| Input | Target | Hardware |
|-------|--------|----------|
| 30s @ 720p | ≤ 8s | M1/M2 CPU, no GPU |
| 60s @ 1080p | ≤ 15s | same |
| 5min @ 1080p | ≤ 60s | same |

If exceeded, switch `AdaptiveDetector` → `ContentDetector` and skip Optical Flow paths.

## Confidence Scoring

Map the LLM's `confidence` field plus visual-evidence strength to Scout's standard scale.

| LLM `confidence` | Evidence Frames | Region Coordinates | Scout Confidence |
|------------------|-----------------|--------------------|------------------|
| ≥ 0.85 | ≥ 2 frames | present in ≥ 1 frame | `HIGH` |
| 0.7 – 0.84 | ≥ 2 frames | optional | `MEDIUM` |
| 0.5 – 0.69 | ≥ 1 frame | optional | `LOW` |
| < 0.5 | any | any | `LOW` (or `uncertain`) |

`HIGH` is required to emit a `LLM Fix Prompt` block. `MEDIUM` may emit `INVESTIGATE-FURTHER`. `LOW` and `uncertain` route to human review queue.

## Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| `codex` not in `PATH` | preflight | Emit "Codex CLI unavailable" note, suppress Fix Prompt, recommend manual review |
| `codex auth` not configured | preflight | Same as above |
| Rate limit (429 / equivalent stderr) | parse stderr | Exponential backoff: 5s, 15s, 45s; max 3 attempts |
| Schema violation in stdout | JSON Schema validate | 1 retry with same input; if still invalid → human review queue |
| `confidence < 0.7` | post-validate | Human review queue; do not emit Fix Prompt |
| Sandbox denies frame read | stderr `permission denied` | Add `--add-dir frames/` if missing; otherwise fail loud |
| Zero frames extracted | extractor result | Treat as `vague-report-handling.md` `P06` with reduced confidence |
| Codec / container unsupported | ffprobe failure | Emit "Unsupported video format" with detected format; ask reporter for re-export |
| Frames exceed CLI image limit | exec stderr | Halve `max_frames` and retry once; otherwise batch-split per scene |

## Privacy and Compliance

| Concern | Mitigation |
|---------|------------|
| PII in screen content (names, emails, tokens) | OCR-based redaction in **PREPROCESS**, before any LLM call |
| Recording uploaded to OpenAI | Document in user-facing privacy notice; offer `--oss` local-provider path for strict environments |
| Session metadata leakage | `--ephemeral` ensures no Codex CLI session file is written |
| Frame retention | Pipeline caller is responsible for retention policy on `frames/` and `analysis.json`; default recommendation: delete within 24h of report closure |

Cross-reference: `_common/BOUNDARIES.md` for cross-skill privacy norms; cross-team consent / DPA handled by Cloak when applicable.

## Scout Workflow Integration

Map of standard Scout phases to video-specific actions when Recipe `video` is active.

| Phase | Standard Action | Video Recipe Addition |
|-------|----------------|------------------------|
| `TRIAGE` | 3 hypotheses | Add hypothesis `H0`: "video may not actually contain the bug" |
| `RECEIVE` | Normalize report | Probe video metadata; record duration, resolution, codec |
| `REPRODUCE` | Build minimal repro | **Run frame extractor → invoke Codex CLI → parse analysis.json** |
| `TRACE` | Narrow search space | Map `evidence_frames` observations to candidate code paths |
| `LOCATE` | Pinpoint cause | Confirm with at least 2 visual evidence points + 1 code-side trace |
| `ASSESS` | Severity / scope | Use `bug_type` to seed severity; verify against `reference/output-format.md` table |
| `REPORT` | Investigation Report | Embed `evidence_frames` references in `Reproduction Steps`; gate Fix Prompt on `HIGH` confidence |

### Handoff Notes

- `SCOUT_TO_BUILDER_HANDOFF`: include `video_analysis_artifact: <path/to/analysis.json>` in the handoff payload so Builder can replay observations.
- `SCOUT_TO_RADAR_HANDOFF`: surface `bug_type` so Radar can pick a matching regression-test template.
- `SCOUT_TO_SENTINEL_HANDOFF`: when `bug_type = ocr_or_text_error` exposes credentials/PII, escalate before any Fix Prompt is emitted.

## See Also

- `reference/vague-report-handling.md` — `P06 Image Only` parent pattern; this reference is the deeper specialization for video.
- `reference/reproduction-templates.md` — for non-video reproduction templates that frame the broader REPRODUCE contract.
- `reference/output-format.md` — the canonical investigation report shape this pipeline must produce.
- `reference/fix-prompt-generation.md` — verbs and suppression rules for the Fix Prompt block.
