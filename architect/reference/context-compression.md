# Context Compression

Read for the `compress` recipe or after a structural improvement. Measure the baseline before editing; preserve a reversible diff. Shared delivery rules are in `_common/OPERATIONAL.md`; structure is owned by `_templates/SKILL_TEMPLATE.md`.

## Token Estimation Guidelines

Prefer the actual host tokenizer. Without one, label estimates as heuristics: English ~4 chars/token, Japanese ~1.5, code/YAML ~3.5, mixed ~2.5. Use the same method before and after; file totals are not per-run consumption.

```yaml
TOKEN_ESTIMATE:
  agent: "[name]"
  date: "[YYYY-MM-DD]"
  sections:
    - name: "[section]"
      lines: 0
      estimated_tokens: 0
      category: core | standard | boilerplate | integration
      compression_potential: low | medium | high
  totals:
    total_lines: 0
    estimated_tokens: 0
    boilerplate_ratio: "[measured %]"
    compression_target: "[evidence-based proposal, not a quota]"
```

## Compression Strategies

Inventory required decisions, live constraints, rejected alternatives and output fields **before** removing text; then remove statements that cannot change an action. Inspect sections individually.

| Candidate | Action | Preservation check |
|-----------|--------|--------------------|
| Existing shared contract repeated locally | Link to its existing canonical source | The skill-local symlink resolves; the source loads at the required phase, not merely through an unopened reference |
| General knowledge, obsolete workaround, unused example | Delete | No unique rule, live dependency, schema or failure-prone format is removed |
| Repeated explanation of one rule | Keep the most precise expression | Preserve conditions, thresholds and exceptions |
| Heavy checklist/schema needed only on one path | Keep in an on-demand reference | SKILL.md names that path and when to load it |
| References always used together | Merge the useful content | No unrelated task must load the merged material |
| Repeated output envelope | Use `_common/AUTORUN.md` or `_common/HANDOFF.md` as applicable | Preserve skill-specific payloads; do not invent `$schema` files |
| Inferable operational steps | Replace with the outcome and constraints | Loose-prompt compression is limited to established Grade A skills and non-critical steps; never apply it to boundaries, safety, integration formats or experimental behavior |

Do not create a shared contract just to remove prose duplication. Do not require a minimum reference count, example count or line count. Do not move heavy references into SKILL.md to make the reference census smaller.

## Ma Design Principles

Use the authoring template's ordering; front-load the task's authority, constraints and completion condition. Layout is not evidence of behavioral equivalence. Cache economics and model-generation benchmarks are not compression gates; verify actual runtime dependencies through `_common/CLI_COMPATIBILITY.md` only when the task needs them.

## Equivalence Verification

| Axis | Required evidence |
|------|-------------------|
| Behavioral | Exercise 3 representative prompts, including an edge/negative case; compare required actions and outputs, not wording |
| Structural | Validate against `_templates/SKILL_TEMPLATE.md` and the repository's existing checks |
| Integration | Preserve exact AUTORUN/Nexus/handoff fields, enums and skill-specific payloads; verify shared-contract delivery from the skill's own directory |
| Routing | Preserve CAPABILITIES_SUMMARY, triggers, owned artifact and role boundaries; check inbound/outbound routing |

Run applicable repository checks and reread the diff. Unexecuted behavioral checks remain **unverified**, not PASS. Preserve the existing Boundaries and CAPABILITIES_SUMMARY contract; do not compress away its conditions. Repair broken links and remove active mentions of deleted files. Keep intentional project-local mirrors synchronized.

```yaml
EQUIVALENCE_REPORT:
  agent: "[name]"
  date: "[YYYY-MM-DD]"
  compression_applied:
    strategies: ["dedup", "density", "hierarchy"]
    lines_before: 0
    lines_after: 0
    reduction: "[measured %]"
  verification:
    behavioral:
      status: "[PASS or FAIL only when exercised]"
      test_prompts: 0
      issues: ["[missing evidence / observed mismatch]"]
    structural:
      status: "[PASS or FAIL only when exercised]"
```

Report all four axes even when the compact envelope above is extended. A missing live result is a delivery limitation, not a successful equivalence test.

## COMPRESSION_PROPOSAL Output Template

```yaml
COMPRESSION_PROPOSAL:
  agent: "[name]"
  date: "[YYYY-MM-DD]"
  analysis:
    current_lines: 0
    estimated_tokens: 0
    boilerplate_lines: 0
    boilerplate_ratio: "[measured %]"
    ma_compliance:
      zone1_identity: true
      zone4_actionable: true
      separator_frequency: "[observed; not a required interval]"
      density_rhythm: "[observed]"
  proposals:
    - id: 1
```

Name each affected section, its DELETE/MERGE/TRIM decision, retained behavior, destination when merged, and verification evidence. Apply the approval thresholds in SKILL.md; a projected savings percentage never overrides a boundary.
