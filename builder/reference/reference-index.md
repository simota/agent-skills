# Builder Reference Index

Every `reference/` file `builder` owns, and the condition that makes it worth
reading. `builder/SKILL.md` keeps only the shared-contract rows and a pointer here.

**Read this when** you need a reference and the Recipe registry did not already
name it, or when scanning what this skill can consult at all.

---

| Reference | Read this when |
|-----------|----------------|
| `reference/core-contract-rationale.md` | A Core Contract rule needs its reasoning, tuning number, or source. |
| `reference/implementation-policy.md` | Repository-first architecture selection, language/toolchain grounding, implementation boundaries, and frontend state ownership. |
| `reference/cross-language-port.md` | `port` recipe — parallel-run black-box comparison, semantic equivalence tests. |
| `reference/external-integration.md` | `integrate` recipe — sandbox-first, secret handling, vendor retry, webhook signatures. |
| `reference/targeted-patch.md` | `patch` recipe — scoped patch with regression coupling and clear rollback. |
| `reference/pair-programming.md` | `pair` recipe — driver/navigator roles, SETUP -> LOOP -> CLOSE, gates, termination bounds. |
| `reference/recipe-verify-gates.md` | The per-recipe acceptance gate for the active subcommand. |
| `reference/autorun-nexus.md` | Exact AUTORUN or Nexus Hub mode compatibility details. |
| `reference/autorun-schema.md` | Emitting the AUTORUN `_STEP_COMPLETE` block — Builder-specific Output/Next schema. |
| `reference/image-generation-api.md` | Gemini SDK/auth/model/request/response/error/rate/cost rules and grounded or reference-based generation. |
| `reference/image-generation-prompts.md` | Prompt architecture, JP-to-EN mapping, presets, templates, policy-safe phrasing, and quality checks. |
| `reference/image-generation-batch.md` | Seed strategy, style anchors, bounded concurrency, checkpoints, naming, and pHash deduplication. |
| `reference/image-generation-style-transfer.md` | Reference-image prompting, style-token extraction, leakage controls, and model-choice boundaries. |
| `reference/image-generation-postprocess.md` | Native-resolution regeneration, upscale, masks, inpaint/outpaint, artifact checks, and export formats. |
| `reference/image-generation-cinematic-prompts.md` | Shot, camera, lens, aperture, lighting, color science, film stock, and composition vocabulary. |
| `reference/image-generation-provenance.md` | C2PA, SynthID, EXIF/XMP disclosure, distribution records, and takedown/appeal response. |
| `reference/image-generation-content-safety.md` | Layered policy filtering, likeness/minor/brand safety, regional compliance, refusal UX, and red-team tests. |
| `reference/image-generation-codex.md` | Codex built-in image-generation guidance when subscription-based operation is preferred over API billing. |
| `reference/grammar/` | Authoring a regex, parser, DSL, or AST transform (absorbed from `grok`) |
| `reference/cli-tui/` | Implementing a CLI or terminal UI (absorbed from `anvil`) |
| `_common/OPUS_5_AUTHORING.md` | Sizing the report, effort-level for codegen, front-loading constraints at PLAN. Critical: P3, P6. |
