# Skill Validation

Read before delivering a generated or improved skill. `_templates/SKILL_TEMPLATE.md` and the current repository checks own syntax and required sections; do not implement a competing YAML linter or require obsolete 400–1400-line scaffolds.

**Pass criteria:** all applicable REQUIRED checks pass; at least 80% of applicable RECOMMENDED checks pass; record skipped OPTIONAL checks. Unexecuted runtime behavior is unverified. Derive check totals from the checks actually exercised.

## 1. Structure Validation (REQUIRED)

Run `make check` in the repository root. Inspect frontmatter (`name` and `description` only), CAPABILITIES_SUMMARY/COLLABORATION_PATTERNS/BIDIRECTIONAL_PARTNERS formatting, required headings and current size rules through the existing checker rather than copied numerical quotas.

- **S1.7 / S1.8:** mandatory actions, approval gates and prohibitions are explicit. INTERACTION_TRIGGERS is optional; every actual confirmation requirement must still be represented.
- **S1.14:** operational logging is delivered; a fictional log example is not required.
- **S1.15 / S1.16:** AUTORUN and Nexus Hub Mode use the applicable `_common/AUTORUN.md` and `_common/HANDOFF.md` envelopes plus any unique skill payload.
- Resolve every shared path from the skill's own directory. `_common/` does not load automatically. Preserve its symlink and the required loading depth; verify both project-local mirrors when affected.

## 2. Content Quality Validation

Check the owned artifact and completion evidence, executable decisions and exceptions, valid required schemas, reciprocal partner expectations, and specificity beyond general model knowledge. Required safety/decision rules must survive removal of prose. An unused example, closing slogan or diagram is not a completeness requirement.

## 3. Overlap Check Validation

| ID | Check |
|----|-------|
| O3.1 | Scan the current ecosystem and calculate overlap from actual capabilities |
| O3.2 | Reject a new agent with overlap ≥50%; propose an existing-owner alternative |
| O3.3 | For overlap ≥30% and <50%, obtain confirmation and document differentiation |
| O3.4 | State the unique outcome an existing agent cannot deliver |
| O3.5 | Report the top 3 overlaps and shared/unique capabilities |

Full algorithm: `reference/overlap-detection.md`. For a reference-only edit, do not invent a new-agent overlap finding; confirm unchanged ownership instead.

## 4. Nexus Compatibility Validation

| ID | Check |
|----|-------|
| N4.1 | `_AGENT_CONTEXT` required fields and Role are correct |
| N4.2 | `_STEP_COMPLETE` preserves the explicitly declared skill-specific schema; otherwise use the default statuses `SUCCESS \| PARTIAL \| BLOCKED \| FAILED` and payload from `_common/AUTORUN.md` |
| N4.3 | `NEXUS_HANDOFF` preserves the canonical required fields, including pending/user confirmations |
| N4.4 | Work returns to the hub; no direct specialist-to-specialist invocation |
| N4.5 | Primary-output ownership agrees with `_common/BOUNDARIES.md` |
| N4.6 | New/changed routing has a task type, primary chain and optional additions |
| N4.7 | Partner handoffs can be orchestrated without hidden shared state |
| N4.8 | Trigger and negative-routing cases select the intended owner |

## 5. Style & Conventions Validation

Use repository language/naming rules and `_common/GIT_GUIDELINES.md`. Validate Markdown and internal paths, including reference-to-reference links. A link that exists only from the repository root is not evidence it works in the installed skill. No minimum file, example or line count applies.

## 6. Context Efficiency Validation (OPTIONAL)

For COMPRESS, this becomes a required delivery check: measure the baseline, review section-level duplication and loading cost, and complete all four equivalence axes in `reference/context-compression.md`. Preserve routing, boundaries, exact output fields and on-demand reference delivery. A lower token estimate alone is not a pass.

## 7. Opus 5 Readiness Validation (RECOMMENDED)

Legacy heading retained for links. Apply model-agnostic P1–P12 from `_common/OPUS_5_AUTHORING.md`; use `_common/CLI_COMPATIBILITY.md` only for an actual runtime dependency. Verify authority, observable completion, independent verification, disjoint parallel ownership and authentic runtime capability. Label behavior that was not exercised as unverified.

## 8. Output Density Protocol Validation (REQUIRED)

| ID | Check |
|----|-------|
| R8.1 | An absent Output Contract correctly inherits `M`; a present contract must add a real override or domain ban |
| R8.2 | Present default is `S/M/L/XL`; `L/XL` is for a long response artifact, not merely many written files |
| R8.3 | `_common/OUTPUT_STYLE.md` is referenced, not copied |
| R8.4 | Task types that require different tiers declare the differences |

A missing/invalid tier, a redundant default-only `M` contract, file-output `L/XL`, copied banned-pattern list or missing differing-tier override fails this gate. AUTORUN/handoff envelopes are separate from response tiers.

## Runtime Evaluation — Separate from Artifact Lint

Exercise representative real tasks, negative routing and failure/edge cases against a documented simple baseline. A plausible sample response in SKILL.md is not an executed test. Preserve actual tool-call and outcome evidence; do not infer success from the final prose alone.

During execution, check instruction/source grounding, untrusted-input boundaries, required confirmation for consequential actions and output format/privacy constraints. After execution, inspect the trace for wrong tools, instruction failures, missing state or orchestration errors. An unsupported citation or unevidenced outcome is a finding, not successful validation.

Use `reference/review-loop.md` for review scheduling and priority windows; do not copy a second remediation calendar here. Keep expected/observed evidence and the defect's owner in the feedback.

## Validation Report

Report each exercised gate with PASS/FAIL and evidence, separately list unverified/skipped checks and reasons, and give derived totals. Include repository command/exit results and semantic limitations; neither a score nor a syntactically valid file proves runtime quality.
