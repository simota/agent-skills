# Antigravity CLI Review Usage

Review-specific adapter for the optional third engine. Claude + Codex remains Judge's normal dual-engine baseline; agy participates only when available and authorized. `tri-engine-review.md` owns independent fan-out and integration, `codex-integration.md` owns severity/filtering, and `_common/CLI_COMPATIBILITY.md` owns runtime facts. Gemini CLI and Antigravity CLI are distinct products; installing one is not an upgrade of the other.

## Prerequisites

Verify the installed binary/version, supported headless interface, existing account authorization and required read tools. Resolve the target revision/diff before dispatch. No new plugin, MCP server, paid model or permission expansion is implied. An optional third-party review plugin requires the supply-chain gate in `_common/SECURITY.md`; built-in file/diff analysis does not require it.

### Robust availability detection

Probe the current host PATH and documented fallback executable locations without reading credential stores. A missing binary differs from authentication, quota or tool-permission failure. Record the observed category; never silently relabel a failed engine as a clean review. CLI discovery does not prove its account can execute a request.

## Command Reference

### Syntax

Use the documented `agy -p` headless entry under existing scoped grants. Resolve model identifiers, output options and schemas through `_common/CLI_COMPATIBILITY.md` §3–§5 and §9.2. Do not append permission-bypass flags or assume TUI plugin commands exist in a headless session.

### Flag Matrix (verified against `agy --help` v1.0.2 + official DEV.to examples, 2026-05)

Legacy heading retained for links; that old matrix is superseded by the compatibility layer's dated official sources. Current documented structured output and model selection must not be disabled by historical workarounds. Installed help is the final capability check.

### Canonical Commands

Prepare a review brief containing goal, target revision/base, relevant rules, read-only authority, ACs and the expected findings schema. Invoke it through the verified interface and capture process status, structured result, diagnostics and current-run artifacts. A review prompt forbidding writes is **not** a sandbox; restrict the actual grant where supported.

## Use Case Cookbook

Use the following scope deltas with the same bounded review brief. These are review tasks, not additional top-level Recipes or copyable plugin invocations.

### 1. Current-Branch Review (PR-equivalent)

Resolve the actual comparison base and current HEAD; inspect that diff and relevant unchanged callers. Do not assume the base branch is named main.

### 2. Pre-Commit / Uncommitted Changes

Distinguish staged, unstaged and requested untracked changes. Preserve the working tree and report which snapshot was reviewed.

### 3. Specific Commit Review

Resolve the supplied SHA and review its introduced changes against the correct parent; do not broaden into unrelated history.

### 4. Pull Request Review (GitHub MCP-backed)

Use an available authorized GitHub interface to resolve PR/base/head/diff. Review tools do not authorize posting, merging or branch checkout over user changes. Without connector access, use an available local diff and disclose the coverage gap.

### 5. Security-Focused Review

Ground exploitable findings in code paths and evidence; route CRITICAL/HIGH findings to Sentinel. Keep this review read-only and within authorized targets.

### 6. Intent-Alignment Review

Compare the diff with the supplied intent and frozen ACs. Separate missing behavior, unintended scope and unverified assumptions.

### 7. AI-Generated Code Scrutiny

Verify referenced symbols, imports and APIs against repository/package evidence; inspect error paths and security shortcuts without assuming generated code is correct or incorrect.

### 8. Framework-Specific Review

Load only the matching sections of `framework-reviews.md` after detecting the installed stack. Do not impose a newer framework or architecture as a review fix.

### 9. Consistency Audit

Report concrete outliers against evidenced repository conventions; style differences alone are not correctness defects.

### 10. Test Quality Review

Inspect isolation, boundary coverage, mock fidelity and dependencies on ordering/time/network. Distinguish inspection from tests actually run.

### 11. Project-Guideline-Gated Review

Read applicable repository instructions and any supplied REVIEW.md. Verify loaded rule scope instead of assuming every CLI discovers every filename.

### 12. Cross-Engine Verification

Run independent read-only reviews concurrently when inputs and budgets permit. Hide peer conclusions until independent findings are recorded. Engine agreement is corroboration, not proof.

### 13. Structured JSON Output for CI

Use supported structured output with the findings schema: severity, file, line, issue, evidence and suggested_fix. Parse and validate content before integration; malformed/missing output is incomplete, not zero findings.

## Prompt Structure (Recommended)

Supply **Goal / Context / Constraints / Done when** with revision and read-only authority. Request evidence-bound findings rather than private reasoning. The downstream brief must carry actual safety constraints even when loose prompts preserve methodological independence.

## Interactive Slash Commands

Use only commands advertised by the installed runtime or an audited plugin. Plugin-specific slash commands are optional; do not guess their names, arguments or environment variables.

## Decision Flow

Resolve requested engine and target → verify capability/authority → execute bounded review → validate output → integrate through `tri-engine-review.md`. Apply its declared degraded mode on a real unavailable/broken engine; do not silently substitute an explicitly requested provider.

## Do / Don't

### Do

Keep authentication in the existing authorized tool/session, enforce read-only effects, bind findings to a revision and report actual checks. Use current supported output capture and disclose missing independent coverage.

### Don't

Do not expose credentials, auto-install plugins, globally allowlist shell commands, disable permissions for convenience, infer success from exit zero, harvest unrelated transcripts or fabricate engine concurrence. Never route around a safety refusal.

## Troubleshooting

Separate missing binary, unavailable account/model, denied required tool, quota/transport failure, schema failure and missing evidence. Diagnose once, use a permitted bounded repair when justified, and otherwise return the precise limitation. Do not alter review criteria to make a failed run pass.

### Silent Failure Detection

Apply `_common/MULTI_ENGINE_RECIPE.md` §3.5. Record actual process/tool status and structured result plus required artifacts and diagnostics. A timeout, stale artifact or denied required read is not a successful review even if some prose was returned. Legacy PTY/file-handoff applies only after reproducing an installed-version defect under `_common/CLI_COMPATIBILITY.md` §9.2.

## Cross-References

- Codex CLI review (default engine): `codex-review-usage.md`.
- Claude Code CLI review (alternative engine, subagent/plan-mode required): `claude-review-usage.md`.
- Output interpretation, severity mapping, override rules, false-positive filtering (engine-agnostic): `codex-integration.md`.
- Framework-specific review prompts: `framework-reviews.md`.
- PR size cognitive-load thresholds: `review-effectiveness.md`.

### Official Sources (2026)

Current primary-source snapshot and recheck procedure → `_common/CLI_COMPATIBILITY.md`. Antigravity's CLI documentation, not Gemini CLI extension documentation, governs agy commands.
