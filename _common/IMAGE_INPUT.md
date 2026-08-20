# Image Input Protocol

> **Tier:** `domain` — activates when the task's subject matches. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

Canonical protocol for **any image supplied as input** to any agent — screenshot, Figma frame, photograph, diagram, chart, UI mockup, log capture, whiteboard sketch, or generated asset — when that image informs a decision, design, implementation, or response.

This is a cross-cutting protocol: it is not owned by one specialist. Whichever skill receives the image runs this pipeline, then either acts or hands off the **structured reading** (never the raw pixels) to the owner skill identified in Stage 1.

Core stance (inherited from Web Fetch Safety, `_common/WEB_FETCH_SAFETY.md`): **do not let speculation fill a visual gap.** Image interpretation has wider semantic latitude than text; a misread propagates silently through every downstream agent.

---

## The Pipeline

`RECOGNIZE → PARSE → ANALYZE → HYPOTHESIZE → PROPOSE`

Run every stage for evidence-bearing or ambiguous images. Collapse to a lightweight pass only when the image is self-evident for the task.

| Depth | When | Stages run |
|-------|------|-----------|
| Lightweight | Single self-evident image whose content *is* the entire input (e.g., one legible error-message screenshot) | RECOGNIZE + PARSE, state the reading, proceed |
| Full | Bug reports, design comps, multi-element frames, diagrams, anything driving downstream work | All five stages |

Full-depth runs execute the stages as **layered passes** (global → regional → detail → reconcile, plus an optional independent blind re-read) — see **§ Multi-Layer Analysis** below for the layer table, depth selection, and reconciliation rules.

### Stage 1 — RECOGNIZE (classify the image)

Identify the image type first; type determines what to extract and who owns the follow-up.

| Image type | Recognition signals | Parse focus | Likely owner skill |
|------------|--------------------|-------------|--------------------|
| UI mockup / design comp | Polished layout, design grid, no browser chrome | Components, spacing, tokens, states | `pixel` (→code), `vision` (direction), `frame` (Figma), `forge` |
| Running-app screenshot / error screen | Browser/OS chrome, real data, toasts, modals | UI state, error text, env indicators | `scout` (bug), `echo` (UX) |
| Wireframe / sketch | Low fidelity, boxes, placeholder text | Structure, flow, intent | `forge`, `vision` |
| Chart / graph / data viz | Axes, legend, series, units | Values, trends, axis labels, outliers | `pulse`, `oracle` |
| Architecture / system diagram | Nodes, boundaries, layered boxes | Components, dependencies, direction | `atlas`, `canvas` |
| ER diagram | Entities, cardinality crow's-feet | Tables, relations, keys | `schema` |
| Flowchart / sequence / state diagram | Arrows, decision diamonds, lifelines | Nodes, transitions, conditions | `canvas`, `weave` |
| Log / terminal capture | Monospace, stack traces, timestamps | Errors, codes, ordering | `scout`, `triage` |
| Spreadsheet / table capture | Grid, headers, rows | Headers, cell values, units | data extraction → owner |
| Whiteboard / handwriting | Photo of board/paper, hand-drawn | Best-effort transcription, intent | parse then route |
| Photograph (physical/real-world) | Real environment, hardware, paper | Context-dependent | route by request |

If the type is itself ambiguous, name the candidates and treat it as a Stage 3 ambiguity (ask before assuming).

**Accuracy — preprocess before you trust a reading:**
- Correct orientation/skew first; a rotated or warped frame degrades every downstream read.
- Pre-crop to the region of interest rather than reasoning over a downscaled whole — automatic downscaling silently destroys small text and fine detail. For a large or multi-region image, tile it (overlapping crops + one global thumbnail), read each tile, then merge — but skip tiling for pure scene-level questions where global context matters more than local detail.
- Treat dense text, tiny labels, and low-contrast scans as high-risk for misread; obtain a higher-resolution or lossless version before relying on the text rather than guessing through compression artifacts.

### Stage 2 — PARSE (extract content systematically)

Extract verbatim, zone by zone — do not summarize away signal:
- **Text** — all legible text (error messages, labels, status codes, stack traces, copy). Quote exactly; mark unreadable spans as `[unreadable]`, never guess.
- **Layout** — structural arrangement, regions, z-order (modals/toasts over content), hierarchy.
- **Annotations** — reporter-added marks: red boxes, arrows, circles, callouts, highlights. These encode where the human wants attention.
- **Numbers & units** — values with their units/axes/scale. Flag any number whose unit or scale is missing.
- **State & environment** — focus/hover/error/disabled states, cursor position, timestamps, OS/browser/device frame, viewport size.

**Accuracy — high-entropy content needs deliberate extraction (a single glance hallucinates here):**
- Dense tables (≈20+ cells), multi-column layouts, and data-dense charts: extract cell-by-cell / series-by-series, not as one summarizing pass. If a separate OCR/text-extraction step is available, pair it with the visual read for numeric and tabular content rather than trusting one look.
- For charts/graphs, read the **axis labels, scales, and legend first**, then interpret the data — reading the trend before pinning the axes is a top failure mode.

### Stage 3 — ANALYZE (separate observed from inferred)

Partition every image-derived statement into two zones and keep them visibly separate:
- **(a) Observed** — literally present in the image.
- **(b) Inferred** — reasonably implied but not literally shown (e.g., "checkout step 2, per the breadcrumb"). Mark each as inferred.

**Accuracy — how to read before splitting observed/inferred:**
- **Describe first, then answer.** For any non-trivial reasoning question, produce a full literal description of the image *first*, then reason from that description — it anchors the analysis to pixels and sharply cuts hallucination. Do not jump straight to the conclusion.
- **Enumerate regions.** For a multi-element image, number the distinct regions and refer to them by index while reasoning, instead of reasoning over the whole frame at once.
- **State the task frame.** Fix the role / domain / intent ("reading a checkout error for a payments bug") before analyzing — a generic "what is this" read is measurably noisier.
- **Anchor spatial / quantitative judgments** (size, distance, count, relative position) on a known-size reference object in the frame; do not estimate from raw impression. If counting, parse systematically (row by row / left to right), not at a glance.

**Ambiguity Ask-First triggers** — stop and ask via `AskUserQuestion` before proceeding when any hold:
- Text is unreadable (resolution, occlusion, glare, truncation).
- Symbols/arrows/lines/connections admit more than one plausible reading.
- Multiple elements / screens / variants present and the target is unstated.
- Numbers, units, or scale are ambiguous (axis labels missing, bare "12").
- The image references off-screen context the agent cannot see.
- The request and the visible content disagree, with no clear resolution.

This Ask-First gate applies in **AUTORUN and AUTORUN_FULL** — image ambiguity overrides the default no-confirmation policy. When asking, quote the specific region ("the value next to the orange arrow"), not a generic "please clarify the image".

### Stage 4 — HYPOTHESIZE (candidate explanations + confidence)

Go beyond passive description: enumerate the candidate explanations for *what the image shows* or *what produced the observed state*, and rank them.

For each hypothesis state:
- **Claim** — the candidate explanation.
- **Confidence** — High / Medium / Low, grounded in observed evidence (not vibes).
- **Discriminating evidence** — what would confirm or refute it (a log line, a repro step, an API response, a second screenshot).

Prefer 2–4 competing hypotheses over a single premature conclusion. A Low-confidence hypothesis with a cheap discriminating test is more useful than a confident guess.

**Abstention is a valid outcome.** When the visible evidence cannot support any hypothesis above Low confidence, the correct output is "cannot determine from the image" plus the discriminating evidence still needed — never upgrade a guess to a confident claim to appear decisive. This is the active-voice counterpart of the Stage 3 observed/inferred split.

### Stage 5 — PROPOSE (next action / routing)

Convert the analysis into action:
- **Next action** — concrete step(s): code area to investigate, fix direction, data to gather, confirmation to request.
- **Crop-and-rerun before escalating** — when a specific region drove a Low-confidence read, the cheapest next action is usually to re-examine a tighter crop of just that region (Stage 1 preprocessing on a focused area), not to ask the user yet.
- **Routing** — the owner skill from Stage 1, handed the structured reading.
- **Primary vs incidental** — keep the requested item separate from incidental issues the image surfaced. Never let an incidental finding silently expand scope; list it separately and let the user decide whether to bundle.

---

## Multi-Layer Analysis (accuracy discipline)

A single glance at a whole image hallucinates on dense, small, or low-contrast content — and the misread is invisible because the reader *feels* confident. For evidence-bearing images, execute the pipeline as **layered passes**, each anchored to the one before it:

| Layer | Pass over | Produces |
|-------|-----------|----------|
| **L1 Global** | the whole image (or thumbnail) | image type (Stage 1), overall layout, numbered region enumeration — scene-level claims only |
| **L2 Regional** | one crop per L1 region | zone-by-zone verbatim extraction (Stage 2) on the tight crop, never the downscaled whole |
| **L3 Detail** | high-risk crops (dense tables, small labels, stack traces, axis numbers, low-contrast text) | cell-by-cell / line-by-line extraction; pair with OCR/text-extraction when available |
| **L4 Reconcile** | all layer outputs | one merged reading; every claim tagged with its source layer and region index |
| **L5 Blind re-read** | the original image, by an **independent reader** | a second reading produced without seeing the first one's conclusions (fresh subagent or second engine, prompt carries the task frame but no hypotheses); discrepancies vs L4 listed explicitly |

**Depth selection** (extends the Lightweight/Full table above):
- Lightweight images → L1 only.
- Full-pipeline images (bug evidence, comps, diagrams, data) → **L1–L4 minimum**.
- Add **L5** when: a number/unit read drives an irreversible or costly decision, the evidence is contested ("the log says X" vs user says Y), or a load-bearing claim came out of L1–L4 at Low confidence.

**Reconciliation rules (L4):**
- For **local detail** (text, values, labels), lower layers win: L3 > L2 > L1. A claim about small text sourced only from L1 is presumptively unreliable — re-read at L2/L3 before using it.
- For **scene-level structure** (what kind of screen, overall flow), L1 wins — tiling loses global context (Stage 1 caveat).
- A conflict between layers is a **signal, not noise**: re-crop and re-read the conflicting region once; still conflicting → treat as a Stage 3 ambiguity (Ask-First triggers apply).
- L5 discrepancies: resolve by targeted re-crop where possible; otherwise downgrade the claim to Low confidence and surface it in Open questions / abstention — never silently pick one reading.

**Execution mechanics:** produce crops as real files and `Read` each one — do not "mentally crop". macOS: `sips -c <h> <w> --cropOffset <y> <x>` (or `-z` to upscale a small region); alternatives: ImageMagick `magick input.png -crop WxH+X+Y crop.png`, Python PIL `Image.open(p).crop((l,t,r,b))`. Write crops to the scratchpad, never the repo. Obtain a lossless/original-resolution source before L3 when the input is visibly compressed.

---

## Specialization: Bug Report Images (mandatory full analysis)

When the user attaches an image to a bug report, defect report, or "this is broken" request, a one-line description is **not** sufficient. The image is primary evidence — read it at **L1–L4 minimum** (§ Multi-Layer Analysis), adding **L5** when error text, codes, or numeric evidence is contested or load-bearing. Produce the full five-section analysis before proposing a fix or routing downstream. The sections below follow **report order** (how the analysis reads to a human), not pipeline order — the parenthetical stage tags show which pipeline stage produces each:

1. **Observations** (Stage 2) — verbatim: error text, status codes, stack traces, UI state, highlighted regions, cursor, timestamps, environment indicators, reporter annotations.
2. **Inferred context** (Stage 3b) — implied-but-not-shown facts, each marked inferred.
3. **Problem points** (Stage 3) — each distinct problem, primary defect separated from incidental issues in the same frame. Never collapse into "the screen is broken".
4. **Improvement proposals** (Stage 5) — concrete remediation per problem; distinguish "fix the reported defect" from "incidental improvements surfaced".
5. **Open questions** (Stage 4) — what the image alone cannot resolve (repro steps, exact API response, prior actions, account state).

Skipping this on a bug-report image is a `PARTIAL` outcome, not `SUCCESS`. If the image is genuinely under-determined, produce the partial analysis from what *is* observable and push the rest into Open questions — never skip the analysis entirely.

---

## Specialization: Visual Fix Loop (screenshot-driven fix / improvement)

When a chain **executes a fix or improvement** for a problem identified from a screenshot, the reading pipeline alone is not the finish line — a visually-reported defect demands **visual re-verification**. Tests passing does not prove the pixels changed; the loop closes only when an after-capture of the same screen is compared against the reported screenshot.

`STRUCTURED READING → FIX → RE-CAPTURE → COMPARE → VERDICT`

- **RE-CAPTURE** — after the fix, capture the same screen/state the reported screenshot shows, matching route, viewport, theme, and data state as closely as reproducible (note any unavoidable deltas). Capture executor by platform:
  - Web (local app) — `run` skill to launch + screenshot, or `vector` (Playwright capture), or Claude-in-Chrome tools.
  - Web (component-level) — `vitrine` (Storybook/VRT) when the surface is catalogued.
  - iOS — `voyager[ios]` (XCUITest screenshot); native mobile screen iteration → `native` `visualloop` (`native/reference/agent-visual-loop.md`).
- **COMPARE** — walk the **Problem points list from the five-section analysis** item by item against the after-capture. Verdict per item: `resolved` / `unresolved` / `regressed` / `not-capturable`. Never issue a single global "looks fixed".
- **VERDICT** — deliverable carries before/after evidence (or paths to both captures) and the per-item verdict table. If no capture path is available (no runnable app, auth-walled screen, device-only state), mark the visual claim `UNVERIFIED` explicitly — a visual fix without an after-capture is asserted, not verified.
- **Incidental items** — improvements the user did not bundle into scope are not fixed, but the COMPARE step still checks the fix did not *regress* them.

This loop is mandatory whenever the defect or improvement is visually observable and a capture path exists; skipping RE-CAPTURE on a capturable surface downgrades the outcome to `PARTIAL`.

---

## Handoff Rule

When delegating to any downstream agent (Scout, Sherpa, Builder, Radar, Pixel, …), pass the **structured reading** (the stage outputs), not the raw image alone. Downstream agents inherit a verified reading instead of re-interpreting pixels or guessing. Log image-derived decisions and ambiguity resolutions in the agent journal so the verified reading — not the raw image — is what propagates.

---

## Rationale

Images encode high-signal evidence the user often could not or did not put into text. A shallow read ("looks like a UI bug") loses error codes, annotations, and incidental problems, forcing downstream agents to re-derive or guess — and a speculative reading is invisible once it propagates. The five-stage pipeline converts pixels into durable, machine-and-human-readable findings once, so the whole chain acts on one verified interpretation. One confirmation question costs far less than building on a misread visual.
