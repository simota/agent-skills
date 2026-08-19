# Codex Built-in Image Generation (`image_gen`)

Alternative engine to the Gemini API path: OpenAI Codex (CLI / desktop / IDE extension) ships a built-in `image_gen` tool backed by `gpt-image-2`. It runs inside a ChatGPT Plus/Pro subscription — ChatGPT account auth only, no `OPENAI_API_KEY`, no per-image billing. Researched 2026-08.

## When to prefer over the Gemini API path

| Signal | Engine |
|--------|--------|
| User wants images without API billing, already pays for ChatGPT Plus/Pro | Codex `image_gen` |
| Reproducible code deliverable, seeds, batch pipelines, metadata (Builder image-generation contract) | Gemini API (default) |
| Assets generated alongside a coding session and saved into the repo | Codex `image_gen` |
| Fine parameter control (resolution tiers, aspect ratios, thinking level, grounding) | Gemini API |

Builder's deliverable stays "code, not images" on the Gemini path; the Codex path is *operating guidance* (commands + config), not Python code.

## Usage

- Inside Codex CLI, request in natural language, or invoke the built-in skill explicitly as `$imagegen`. Outputs are saved under `$CODEX_HOME`.
- Some installs require enabling the feature in `~/.codex/config.toml`:

```toml
[features]
image_generation = true
```

- If saving fails, check the sandbox mode: `--sandbox workspace-write` (read-only sandbox cannot write generated files — community report, unverified).
- Transparent backgrounds: `image_gen` generates via chroma-key + post-process script, or falls back to `gpt-image-1.5` (per the official imagegen SKILL.md).
- Do not confuse with `--image` / `-i`: that flag is image *input* (vision) for mockup-to-code, not generation. Input constraints: no BMP/TIFF/SVG/HEIC, ≤5MB recommended.

## Cost model

- Consumes standard Codex usage limits; an image-generation turn burns the quota **3–5× faster** than a text turn (official docs).
- No extra charge within the subscription. For high volume, switching to the OpenAI Image API (metered, `OPENAI_API_KEY`) is the documented alternative — that path exits the subscription.

## UNVERIFIED (as of 2026-08)

- Whether `image_gen` works in Codex cloud (async tasks; agent phase defaults to network-off sandbox).
- Whether Codex `image_gen` quota is shared with ChatGPT's own image generation.
- "Unlimited on Pro" claims (personal-blog sourced only).
- Full official parameter reference for `$imagegen`.

## Sources

- https://learn.chatgpt.com/docs/image-generation (redirect target of developers.openai.com/codex/image-generation)
- https://community.openai.com/t/introducing-gpt-image-2-available-today-in-the-api-and-codex/1379479 (2026-04-21 announcement)
- https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/imagegen/SKILL.md
- https://github.com/openai/codex/issues/19133 (feature-flag enablement)
