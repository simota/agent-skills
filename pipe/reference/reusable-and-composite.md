# Reusable Workflows and Composite Actions

Purpose: Decide when to keep workflow YAML inline, when to extract a reusable workflow, and when to encapsulate setup steps in a composite action.

## Contents

- Comparison table
- Rule of three
- Reusable workflow rules
- Composite action rules
- Versioning and testing

## Comparison

| Aspect | Reusable Workflow | Composite Action |
|--------|-------------------|------------------|
| Definition | `.github/workflows/*.yml` with `workflow_call` | action metadata under `.github/actions/*/action.yml` or a separate repo |
| Execution unit | whole workflow or job graph | steps inside a single job |
| Runner | declared inside the reusable workflow | inherited from the caller job |
| Secrets | explicit or `secrets: inherit` | passed through caller `env:` or `with:` only |
| Outputs | job/workflow outputs | step outputs |
| Nesting | workflow nesting is limited and should stay shallow | composites can be nested but should stay simple |
| Environment protection | first-class with workflow jobs | inherited from caller |
| SLSA / provenance | supports higher provenance workflows | no workflow-level provenance benefit |

## Rule Of Three

- `3+` copies of the same pipeline shape -> reusable workflow.
- `3+` copies of the same setup steps inside jobs -> composite action.
- `1-2` copies -> keep inline. Copying is cheaper than premature abstraction.

## Reusable Workflow Rules

- Use `workflow_call` for the reusable entry point.
- Add `workflow_dispatch` when direct testing is useful.
- Validate inputs with defaults, `required`, and `if:` guards.
- Prefer reusable workflows when the unit of reuse is a pipeline, deploy flow, or multi-job contract.
- Reusable workflows are the right place for secrets, environments, approval gates, and shared deployment logic.

Minimal pattern:

```yaml
on:
  workflow_call:
    inputs:
      node-version:
        type: string
        default: '20'
```

## Composite Action Rules

- Use composite actions for repeated step sequences such as checkout + setup + cache + install.
- Every `run:` step inside a composite action must declare `shell:`.
- Composite actions cannot directly read repository or environment secrets on their own. Secrets must be passed in from the caller.
- Use composites when the caller should keep control of runner, permissions, and job graph.

## Versioning And Testing

| Topic | Guidance |
|------|----------|
| Version refs | avoid `@main`; prefer semver tags for shared reuse, exact refs or SHAs for tighter control |
| Direct testing | add `workflow_dispatch` to reusable workflows when maintainers need quick verification |
| Local testing | use `act` for fast smoke checks, then validate with `workflow_dispatch` |
| Change rollout | major tag for compatibility line, immutable SHA for production-critical consumers |

Choose a reusable workflow when you are standardizing a pipeline. Choose a composite action when you are standardizing a step bundle.
