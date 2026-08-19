# Recipe Design

**Purpose:** How to design a repo-tailored task playbook as a subcommand-driven recipe.
**Read when:** You are in the `recipe` mode or designing the recipe set inside a blueprint.

## Contents
- What a recipe is (and is not)
- Recipe anatomy
- Signal keywords
- Worked examples
- Anti-patterns

---

## What a recipe is (and is not)

A **recipe** is a named, repeatable playbook for one recurring multi-step task in the repo. It chains existing skills and ecosystem agents in a fixed order with decision points. It is the project-scoped analogue of the `Recipe` tables that ecosystem skills (Architect, Sigil) carry internally.

| A recipe IS | A recipe is NOT |
|-------------|-----------------|
| A fixed flow for a repeatable task | A single methodology (→ that is a skill) |
| A chain of skills/agents with a subcommand | Runtime per-request routing (→ that is Nexus) |
| Design-time, persistent, repo-local | An autonomous loop (→ that is Orbit) |
| Deterministic enough to name and document | A one-off ad-hoc sequence |

A recipe earns existence only when SURVEY found the task happening repeatedly. If it happens once, do not encode it.

---

## Recipe anatomy

Every designed recipe specifies these fields (handed to Nexus to register, and to Sigil if any step needs a new skill):

```yaml
recipe:
  subcommand: ship-feature          # first-token trigger
  task: "Take a described feature from scaffold to an opened PR"
  signal_keywords: [ship, "build the feature", "implement and open PR"]
  preconditions: [clean working tree, feature spec exists]
  chain:                            # ordered steps, each with an owner
    - step: scaffold structure       owner: scaffold       gate: none
    - step: implement logic          owner: builder        gate: tests-green
    - step: add edge-case tests      owner: radar          gate: coverage>=target
    - step: prepare PR               owner: guardian       gate: user-confirm
  decision_points:
    - at: implement logic
      if: "ambiguous requirement"
      then: ask user, do not guess
  output: "Opened PR with passing tests"
  rollback: "Abandon branch; no merge performed"
```

The discriminator is **shape, not step count**: a straight chain is a recipe regardless of length; any genuine branching, fan-out, or convergence makes it a **workflow** — design it with `workflow-design.md` and a formal topology instead, even below 5 steps. Keep recipe chains short for readability, but length alone never forces promotion.

---

## Signal keywords

Recipes activate by subcommand (first token) or by natural-language signal. For each recipe, define both so Nexus can route. Make signals concrete and non-overlapping with other recipes in the suite — two recipes that fire on the same phrase is a routing fault caught in VERIFY.

```
| Subcommand   | Signal keywords                          |
|--------------|------------------------------------------|
| ship-feature | "ship", "build and open PR", "implement X"|
| cut-release  | "release", "tag a version", "ship to prod"|
| onboard      | "set up dev env", "onboard", "first run" |
```

---

## Worked examples

### ship-feature (chain over skills + agents)
SURVEY found: features routinely go scaffold → implement → test → PR, done inconsistently. Mechanism: recipe (repeatable multi-step, no heavy coordination). Chain: `scaffold → builder → radar → guardian`, gate on tests-green before PR. Owner: Nexus registers it; no new skill needed.

### cut-release (chain with a confirmation gate)
SURVEY found: monthly release with changelog + notes + tag. If it needs `≤ 5` linear steps → recipe; if it fans out (collect across packages, parallel verify, then converge) → promote to workflow. Decision point: ask user before tagging. Owner: Nexus; defer changelog/notes to `Launch` if that ecosystem agent owns it (route, don't duplicate).

### add-migration (recipe that needs a new project skill)
SURVEY found: schema changes need a migration + model update + test, repo-specific. Mechanism: recipe whose first step calls a **new** project skill `new-prisma-migration`. DELEGATE: Sigil authors the skill body; Sigil[blueprint] registers the recipe with Nexus referencing it.

---

## Anti-patterns

- **Recipe that is really one skill.** A single methodology with no chaining belongs in a skill (Sigil), not a recipe.
- **Recipe that is really a workflow.** Heavy multi-agent coordination with branching needs a formal topology — promote it.
- **Overlapping signals.** Two recipes firing on the same phrase. Disambiguate or merge.
- **Encoding a one-off.** No observed repetition in SURVEY → do not create the recipe.
- **Embedding step logic Sigil[blueprint] should delegate.** Sigil[blueprint] names the step and its owner; the owning skill/agent holds the how.
