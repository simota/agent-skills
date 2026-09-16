# agy (Antigravity CLI) Orchestration Authoring Protocol

> **Tier:** `orchestration` — activates from the hub, a recipe, or on engine detection. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

Adapt only agy's runtime interfaces; the specialist's role and method do not change. Preserve A1–A9 identifiers for existing consumers. Current documented models, commands, output fields, permissions, and sources are centralized in `_common/CLI_COMPATIBILITY.md`. Gemini CLI is a separate runtime, not an interchangeable binary or config schema.

## Why This Exists

Earlier rules treated one model, maximum effort, permission bypass, a PTY, and file-handoff capture as universal requirements. Those were model/version-specific assumptions. Use documented native capabilities first and enable a workaround only for an observed failure in the installed environment. Neither documentation nor a successful process proves the requested task was performed.

## The Nine Principles

### A1. Single-Model Effort-Tier Routing

Legacy heading retained. Select the stable available authorized model and supported effort via `_common/CLI_COMPATIBILITY.md` §4; do not force a historical model or effort on every step. Inherit explicit user choices. A preview or paid model is not an automatic substitute.

**A1-R — Recipe execution:** preserve recipe acceptance criteria, specialist boundaries, and effort/budget constraints; no extra reasoning directive is required merely because the executor uses agy.

### A2. File-Handoff Capture + Real PTY

Legacy heading retained, **conditional rather than mandatory**. Prefer the documented structured headless result channel and validate process status, parsed result, denied-tool diagnostics, and actual artifacts. Apply the canonical `_common/CLI_COMPATIBILITY.md` §9.2 protocol. Use a scoped file artifact or PTY only after reproducing a capture/terminal failure; record current-run provenance and completeness. Never introduce a permission bypass as part of output capture.

### A3. Session-Scoped Model/Tier — No Per-Agent Switch

Legacy heading retained, not a claim about the current interface. The current documented headless model/effort controls are in Compatibility §4. Discover actual model slugs and agent configuration; do not assume display labels are API IDs, per-agent fields exist, or omitted settings inherit identically across versions. Verify the selected model from runtime output when available.

### A4. Spawn Topology & Fan-Out

Discover native subagent/background capabilities and limits. Keep hub-spoke ownership, disjoint writes, bounded workers, and explicit joins. CLI processes are an alternative only when authorized and their results can be captured and verified. Do not invent another CLI's Agent API or make a paid/preview teamwork feature mandatory.

### A5. @-Path Context Injection

Resolve the specialist's real SKILL.md, source revision, and required paths before delegation. Use the installed interface's documented file-reference mechanism and confirm content was accessible. A path string or an import marker is not proof of a read. Pass only the relevant context delta; preserve the skill-local `_common` resolution and project-local availability gate.

### A6. Sandbox / Permission Posture

Use existing least-privilege grants. Normal headless operation does not require a bypass flag. Distinguish permission denial, missing credentials, quota, and capture failure; do not “fix” any of them by silently widening permissions. Apply Compatibility §5 and §9.1. Respect production, untrusted-workspace, secret, network, and spend restrictions even when a tool exposes an auto-approve option.

### A7. GEMINI.md / AGENTS.md Authority

Verify which instruction files the installed runtime loads. Apply this repository's AGENTS.md and applicable tool-specific deltas without assuming Gemini CLI's historical loading behavior. Rule-class precedence in `_common/OPERATIONAL.md` still protects security, legal, and repository-wide architecture constraints.

### A8. Structured Output via Artifact + Gemini JSON Discipline

Use a documented structured-output/schema facility when available and useful. Parse and validate the expected shape; independently verify the content and artifact/effect. A valid JSON document, non-empty output, sentinel, terminal status, or exit zero alone is insufficient. A soft-denied required tool caps completion unless an authorized alternative provides the same evidence. Keep machine output and diagnostics separate.

### A9. Fast-Model Autonomy & Compensation

Do not infer a reasoning deficit from an engine label. Provide missing inputs, constraints, and objective completion criteria instead of a mandatory number of thoughts, alternatives, micro-steps, or self-checks. Apply `_common/OPUS_5_AUTHORING.md` P5/P9/P12 and the normal Completion Contract. Escalate effort only from task need or observed quality shortfall within authorization.

**A9-D — Deep Reasoning Directive:** retained as a migration identifier, not a prompt block. Replace old forced-thinking text with the task's observable acceptance criteria and evidence requirements. This does not remove executable validation, risk analysis, or independent verification.

## Per-Role Apply Matrix

Orchestrators emphasize A1/A2/A4/A6; workers A5/A8/A9; reviewers A8 and independence; runner authors A2/A3/A6/A7. Read only applicable runtime detail, not every engine's manual. Boundaries remain `_common/BOUNDARIES.md`.

## Validation Hooks

- R-A1: actual model/effort choice follows Compatibility and authorization.
- R-A2: capture uses the documented channel; any workaround has a reproduced trigger.
- R-A3: configured slugs/fields exist in the installed runtime; no display-name guessing.
- R-A4: topology, capacity, writer ownership, and joins are explicit.
- R-A5: required files and contracts are accessible from the specialist's directory.
- R-A6: no automatic permission widening or production/untrusted bypass.
- R-A7: actual instruction loading and repository precedence are respected.
- R-A8: shape, semantics, denied tools, artifact provenance, and completeness are checked.
- R-A9: autonomy is bounded by scope and evidence, not forced internal reasoning.

Report observed results and unavailable runtime checks separately. Passing most items never compensates for a missing safety or completion requirement.

## How to Reference This File

Reference A identifiers from a Compatibility section when agy execution or runner generation is relevant. Keep model IDs and current CLI syntax in `_common/CLI_COMPATIBILITY.md`; do not duplicate them in role contracts.

**Lifecycle:** failure: obsolete agy workarounds become unconditional and weaken permissions; effect: native structured capture with symptom-gated recovery and unchanged task boundaries; owner: compatibility maintainers; removal: when a tested shared runtime adapter covers A1–A9 and all consumers migrate together.
