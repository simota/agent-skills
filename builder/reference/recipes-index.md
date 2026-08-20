# Builder Recipe Registry

The full Recipe table for `builder`. `builder/SKILL.md` carries only the dispatch
allowlist; this file holds what is needed to *execute* a Recipe — activation
condition and the files to read first.

**Read this when** a subcommand matched and you need its row, or when scanning
what Recipes exist at all.

---

| Recipe | Subcommand | Default? | When to Use | Read First |
|--------|-----------|---------|-------------|------------|
| Bug Fix | `fix` | ✓ | Scoped fix after Scout handoff, target <50 lines | — |
| CRUD | `crud` | | Single-aggregate CRUD, no invariants, 30-60 lines | `reference/implementation-policy.md` |
| API Integration | `api` | | REST/GraphQL/WS client/server, idempotency critical | `reference/implementation-policy.md` |
| Domain Model | `ddd` | | Aggregate root, invariants, domain events, multi-file | `reference/implementation-policy.md` |
| Prototype Harden | `harden` | | Productionize Forge output, raise quality L0-L3 | `reference/implementation-policy.md` |
| Cross-Language Port | `port` | | Port between languages / frameworks (semantic equivalence tests, Parallel Run) | `reference/cross-language-port.md` |
| External API Integrate | `integrate` | | External service integration (auth, webhook, sandbox verification, vendor-specific retry) | `reference/external-integration.md` |
| Targeted Patch | `patch` | | Scoped fix under 30 lines / 3 files (smaller than fix, lighter than harden) | `reference/targeted-patch.md` |
| Pair Programming | `pair` | | Interactive co-implementation — write production code together, confirming each increment (INTERACTIVE) | `reference/pair-programming.md` |
| Image Generate | `image` | | Gemini text-to-image or grounded-generation Python implementation | `reference/image-generation-prompts.md`, `reference/image-generation-api.md` |
| Image Edit | `image-edit` | | Reference-based or iterative image-editing code | `reference/image-generation-api.md` |
| Image Prompt | `image-prompt` | | JP-to-EN prompt optimization and parameter design | `reference/image-generation-prompts.md` |
| Image Batch | `image-batch` | | Seeded, resumable, rate-limit-aware asset generation | `reference/image-generation-batch.md`, `reference/image-generation-api.md` |
| Image Style | `image-style` | | Reference-style anchoring and reusable style-token extraction | `reference/image-generation-style-transfer.md` |
| Image Postprocess | `image-postprocess` | | Upscale, inpaint, outpaint, artifact checks, and export formats | `reference/image-generation-postprocess.md` |
| Image Cinematic | `image-cinematic` | | Camera, lens, lighting, film-stock, and composition prompt design | `reference/image-generation-cinematic-prompts.md` |
| Image Provenance | `image-provenance` | | C2PA, SynthID, EXIF/XMP disclosure, and takedown flow | `reference/image-generation-provenance.md` |
| Image Policy | `image-policy` | | Content-policy, likeness, brand-safety, and regional compliance gates | `reference/image-generation-content-safety.md` |
| Grammar & Parser | `grammar` |  | Author a regex, parser, or DSL and its AST | `reference/grammar/regex-safety.md`, `reference/grammar/parser-generators.md`, `reference/grammar/dsl-design.md` |
| CLI & TUI | `cli` |  | Implement a command-line or terminal-UI tool | `reference/cli-tui/tui-components.md`, `reference/cli-tui/cli-design-anti-patterns.md`, `reference/cli-tui/cross-platform.md` |
