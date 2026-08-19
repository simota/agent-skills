# Delegation Handoffs

**Purpose:** Per-component handoff specs and the project routing-map format. Sigil[blueprint] designs; these specs hand each piece to its owner.
**Read when:** You are in `DELEGATE`, building the routing map (`map` mode), or finalizing a blueprint.

## Contents
- Principle
- Routing map format
- Handoff payloads by owner
- Escalation to Architect
- Completeness rule

---

## Principle

Sigil[blueprint]'s output is a design plus a set of handoffs — never an installed artifact. Every component of the blueprint (each skill, recipe, workflow, hook, placement decision) must name exactly one owning agent and the payload that agent needs to execute. A component with no owner is an incomplete design and fails VERIFY.

Use the canonical envelope in `_common/HANDOFF.md`; the fields below are the Sigil[blueprint]-specific payload each owner receives.

---

## Routing map format

The routing map answers "which agent or skill owns which repo task domain" and is consumed by Nexus. Every task domain has exactly **one** primary owner. Ecosystem-owned domains point at the existing agent (defer, never duplicate).

```yaml
routing_map:
  # task domain        : owner (project skill or ecosystem agent)
  "db schema design"   : schema            # ecosystem
  "db query tuning"    : tuner             # ecosystem
  "trpc procedure"     : new-trpc-procedure  # project-local (Sigil authors)
  "app route"          : new-app-route       # project-local
  "security review"    : judge             # ecosystem — deferred
  "ship a feature"     : recipe:ship-feature
  "cut a release"      : workflow:release-train
```

Conflict rule: if two owners claim one domain, narrow scope until each domain is singly owned, or merge. Surface unresolved conflicts as VERIFY failures.

---

## Handoff payloads by owner

### Sigil[blueprint] → Sigil (`SIGIL_BLUEPRINT_TO_SIGIL_HANDOFF`) — author skill bodies
```yaml
skill_specs:
  - name: new-trpc-procedure
    responsibility: "Generate a tRPC procedure with Zod input + colocated test"
    conventions: [import-alias "@/", zod-in src/schemas, vitest]
    type_hint: Micro | Full
    description_requirements:
      - third person, gerund-form name
      - include negative triggers ("Don't use when…")
    install_target: project (.claude/skills + .agents/skills)
```
Sigil[blueprint] states *what* the skill must do and *which conventions* to mirror; Sigil decides Micro/Full and writes the body, scores it, and installs.

### Sigil[blueprint] → Nexus (`SIGIL_BLUEPRINT_TO_NEXUS_HANDOFF`) — register routing + chains
```yaml
nexus_registration:
  routing_map: <the map above>
  recipes:   [<recipe definitions from recipe-design.md>]
  workflows: [<workflow definitions with topology + phases>]
```

### Sigil[blueprint] → Orbit (`SIGIL_BLUEPRINT_TO_ORBIT_HANDOFF`) — autonomous loop specs
```yaml
loop_spec:
  workflow: release-nightly
  goal: "nightly release if main is green"
  stop_condition: "no merged PRs since last run"
  operation_contract: <inputs, success check, recovery>
```

### Sigil[blueprint] → Hone (`SIGIL_BLUEPRINT_TO_HONE_HANDOFF`) — enforcement hooks
```yaml
hook_specs:
  - event: PreToolUse
    matcher: "git commit"
    enforce: "block direct commits to main"
    rationale: "every-time guard — not a skill"
```

### Sigil[blueprint] → Grove (`SIGIL_BLUEPRINT_TO_GROVE_HANDOFF`) — placement
```yaml
placement:
  recipes_doc: docs/recipes/ or CLAUDE.md section
  monorepo_scope: per-package paths if applicable
  # skill install dirs (.claude/skills/ + .agents/skills/) are owned by Sigil, not Grove —
  # never route them here; doing so creates an L6 double-owner on the install path
```

---

## Escalation to Architect

When SURVEY/MAP surfaces a gap that is **not** project-specific — a capability that would help many repositories — escalate to `Architect` for a global ecosystem agent instead of designing a project-local one. Require evidence it generalizes (the same need would recur across unrelated repos); otherwise keep it project-local.

```yaml
SIGIL_BLUEPRINT_TO_ARCHITECT_HANDOFF:
  gap: "<capability>"
  why_global: "<evidence it generalizes beyond this repo>"
  project_workaround: "<what the project-local layer does meanwhile>"
```

---

## Completeness rule

Before emitting `_STEP_COMPLETE`, confirm:
- every skill in the suite plan → a Sigil spec,
- every recipe and workflow → a Nexus registration entry,
- every enforcement point → a Hone hook spec,
- every loop → an Orbit loop spec,
- every task domain → exactly one routing-map owner.

Any unowned component blocks delivery.
