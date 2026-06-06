# Cast Generation Workflows

Purpose: Define the `CONJURE` workflow, source detection order, synthesis rules, validation thresholds, and registration behavior.

## Contents

1. Source detection
2. Input quality
3. Extraction strategy
4. Synthesis rules
5. Validation
6. Registration
7. Auto-triggers
8. Internal personas

## Source Detection

When no explicit path is provided, detect sources in this order.

### External / User Persona Sources

| Priority | Source | Use for | Confidence contribution |
|---|---|---|---|
| `P0` | `.agents/personas/` | Adopt or enrich existing personas | — |
| `P1` | `README.md` | User types, product promise, usage context | `+0.10` |
| `P2` | `docs/**/*.md` | User guides, personas, workflows | `+0.15` |
| `P3` | `src/**/auth*`, `src/**/user*` | Roles, auth, user models | `+0.15` |
| `P4` | `src/**/checkout*`, `src/**/onboard*` | Key journeys, conversion friction | `+0.15` |
| `P5` | `tests/e2e/**` | User stories encoded in tests | `+0.10` |
| `P6` | `package.json`, `*.config.*` | Product metadata and flags | `+0.05` |

### Internal Persona Sources

| Priority | Source | Use for |
|---|---|---|
| `P0` | `CODEOWNERS` | Team structure and responsibility |
| `P1` | `docs/CONTRIBUTING.md` | Development process |
| `P2` | `.vscode/**`, `.idea/**`, `.editorconfig` | Editor/workflow setup |
| `P3` | `docker-compose*.yml` | Local dev context |
| `P4` | `.github/workflows/*` | CI/CD patterns |
| `P5` | `Makefile`, `scripts/**` | Commands and automation |
| `P6` | `docs/runbook*`, `docs/onboarding*` | Operational and onboarding context |

## Input Quality Assessment

| Factor | High | Medium | Low |
|---|---|---|---|
| Explicitness | User type stated directly | Implied | Guessed from filenames |
| Recency | Updated within `30` days | Updated within `90` days | `90+` days stale |
| Specificity | Named user types with details | General user mention | No user mention |
| Breadth | Multiple dimensions covered | Partial coverage | One dimension only |

## Extraction Strategy

| Source type | Extract |
|---|---|
| Documentation | user types, goals, pain points, usage scenarios, language cues |
| Code | roles, flows, permissions, friction points, feature flags |
| Tests | user stories, expected flows, success criteria, fixtures |
| Researcher handoff | quotes, goals, pain points, segment findings |
| Trace handoff | behavior clusters, device mix, drop-off points |
| Voice handoff | feedback themes, promoters/detractors, segment drift |

### Extraction Output

Produce structured extraction output with:

- `service_context`
- `user_types`
- `goals`
- `pain_points`
- `behaviors`
- `contexts`
- `evidence`

## Synthesis Rules

1. Generate at least `3` personas by default: `P0`, `P1`, `P2`.
2. Assign an `echo_base_mapping` to every persona.
3. Record evidence for every non-trivial attribute.
4. Mark unsupported attributes as `[inferred]`.
5. Calculate confidence from source and validation contributions.

### Priority Assignment

| Priority | Criteria |
|---|---|
| `P0` | Most common or strongest evidence |
| `P1` | Second-most common or business-critical |
| `P2` | Edge case, underserved segment, or high-friction segment |
| `P3+` | Only if evidence strongly supports additional segments |

### Detail Level Selection

| Condition | Detail level |
|---|---|
| User explicitly requests a level | Requested level |
| `4+` extended dimensions available | `Full` |
| `2-3` extended dimensions available | `Standard` |
| `type == internal` | `Internal` |
| Otherwise | `Minimal` |

## Validation

### Echo Compatibility

| Check | Rule | Failure action |
|---|---|---|
| Frontmatter | Echo-required fields present | Add safe defaults |
| `Profile` | Includes core role/context fields | Infer cautiously from evidence |
| `Quote` | Non-empty | Compose from goals and frustrations |
| `Goals / Frustrations / Behaviors` | Keep `3` each | Merge or split to reach `3` |
| `Emotion Triggers` | Cover the expected polarity spread | Generate from context |
| `Echo Testing Focus` | At least `3` flows | Derive from JTBD |
| `Source Analysis` | At least one source | Block generation |

### Consistency Checks

- Tech level must fit behaviors.
- Device emphasis must fit context scenarios.
- Goals and frustrations must not contradict each other.
- Echo mapping must match the dominant trait.

### Confidence Thresholds

| Confidence | Status | Action |
|---|---|---|
| `>=0.60` | `active` | Ready for use |
| `0.40-0.59` | `draft` | Usable with enrichment warning |
| `<0.40` | `draft` | Warn and ask before relying on it |

## Registration

### File Operations

1. Create `.agents/personas/{service-name}/` if missing.
2. Write persona file as `{persona-name}.md` in kebab-case.
3. Update `.agents/personas/registry.yaml`.
4. Return a concise registration summary.

### Naming Rules

- Service name: kebab-case.
- Persona name: kebab-case.
- Internal personas stay in the same service directory and are distinguished by `type: internal`.

### Registration Summary

Return:

- service
- personas generated
- detail level
- registry updated
- persona table with `priority / echo mapping / confidence / file`
- analyzed sources
- recommended next command

## Auto-Detection Triggers

Suggest Cast automatically when:

1. Echo has no saved personas.
2. Researcher completes persona creation.
3. Trace delivers behavioral drift data.
4. A new service is added to the project.

## Internal Persona Rules

- Set `type: internal`.
- Include `Internal Profile` and `Workflow Context`.
- Map to an internal Echo base persona.
- Focus emotion triggers and testing focus on workflow and DX concerns.

### Job Type Detection

| Signal | Inferred type |
|---|---|
| `@frontend-team` in `CODEOWNERS` | Frontend Developer |
| `@backend-team` in `CODEOWNERS` | Backend Developer |
| `@infra-team` in `CODEOWNERS` | Infra Engineer |
| `@qa-team` in `CODEOWNERS` | QA Engineer |
| Storybook / Figma references | UI Designer |
| `docs/runbook*` | Ops Manager |
| `admin/` directory | Content Editor / CS |
| `docs/onboarding*` | New Engineer |
