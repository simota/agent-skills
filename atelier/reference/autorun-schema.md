# Atelier — AUTORUN `_STEP_COMPLETE` Schema

When atelier receives `_AGENT_CONTEXT`, parse `task_type`, `description`, `Constraints`, and any inbound `DESIGN_INTENT_HANDOFF`. Execute `ONBOARDING → INTAKE → PLAN → EXECUTE → HANDOFF → DELIVER` with verbose explanation suppressed. Return `_STEP_COMPLETE`.

### `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: atelier
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: <primary artifact bundle>
    artifact_types: [prototype, production, deck, asset, export, story, diagram]
    Registry_Ref: .agents/design-system/<slug>.json
    delegates_used: [Frame, Muse, Forge, Artisan, Vitrine]
    parameters:
      Vision_Ref: <Vision direction or user-brief>
      operation_layers: [prompt, structured-comment, direct-edit, parametric-slider]
  Validations:
    onboarding: reused | refreshed | first-run
    a11y_check: passed | flagged | skipped
    token_drift: 0 | <count>
    fidelity: <percentage or n/a>
  Next: <recommended next agent or DONE>
  Reason: <why this next step>
```

---

## Phase Detail (SKILL.md excerpt)

Only ONBOARDING and EXECUTE require procedural specifics beyond the Workflow table; the remaining phases follow Core Rules directly.

#### ONBOARDING
On first invocation per project:
- Scan codebase for token references, CSS variables, Tailwind config, Style Dictionary, Tokens Studio output, or DTCG JSON.
- Delegate to `Frame` if Figma file is provided; delegate to `Muse` for token normalization.
- Write consolidated state to `.agents/design-system/{project}.json` using the canonical schema defined in `_common/design-system-registry.md` (fields: `name`, `version`, `scope`, `source`, `color`, `typography`, `spacing`, `radius`, `shadow`, `motion`, `components`, `brand`, `a11y`, `platform`). Do not invent a local variant — the registry document is the single source of truth.
- Populate `source.extracted_by = "atelier"` and `source.extracted_at` on write; bump `version` per the registry's update rules.
- Express parametric ranges inside the registry using `_common/parametric-output.md` syntax (labeled endpoints with a mandatory `base`, 3-5 steps).
- On subsequent runs, compare the registry's `source` file hashes against current on-disk state. Re-extract only on hash change or explicit `--refresh-design-system`.

#### EXECUTE
- Fan out through the advertised host interface under `_common/CLI_COMPATIBILITY.md`; preserve the authorized concurrency and permission limits.
- Pass `_AGENT_CONTEXT` with `DESIGN_INTENT_HANDOFF` embedded.
- Collect `_STEP_COMPLETE` from each delegate; schema-validate output.
- HANDOFF builds per-consumer bundles with provenance (tokens version, Vision direction version, Figma file ID + version, extraction timestamp); DELIVER returns the artifact set and logs to `.agents/atelier.md` and `.agents/PROJECT.md` per Core Rule #12.
