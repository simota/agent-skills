# Circular Dependency Remediation

Load for `cycle`. Build a directed graph of the declared module/package boundary using the target's configured dependency analyzer. Record source, tool/version, ignored edges, and scope; a text import count or dependency-version duplication is not cycle detection.

## Detect and Classify

Compute strongly connected components (Tarjan or Kosaraju); inspect every SCC with more than one node and any genuine self-loop. Distinguish a module's legitimate internal references from a self-dependency at the chosen boundary. Re-run detection after each proposed cut: removing one edge does not prove an SCC is acyclic.

| SCC size | Classification / planning scope |
|----------|---------------------------------|
| 2 | Direct pair; identify which direction should own the contract. |
| 3–5 | Clique; identify a shared concept or dependency inversion seam. |
| 6–20 | Blob; boundary analysis before local edge cutting. |
| >20 | Architecture-wide issue; propose a boundary redesign first. |

Classify the relationship as direction-flippable, symmetric co-evolution, or accidental imports/re-exports. Check actual runtime initialization and shared state; hiding an import behind a lazy/dynamic import is not structural remediation.

## Select the Cut

| Evidence | Strategy |
|----------|----------|
| Stable dependency points into an unstable implementation | Dependency inversion: stable side owns the interface; composition root wires implementation. |
| Both modules use the same independent concept | Extract that concept into a lower shared module with no back-edge. |
| Both sides are one responsibility and co-change together | Merge, provided distinct bounded contexts are not being collapsed. |
| Cross-domain notifications need not be synchronous | Event/message decoupling with explicit ordering, consistency and failure semantics. |
| Responsibilities sit in the wrong layer | Re-layer modules and validate the whole resulting graph. |

Do not create a God `utils` module, merge distinct contexts merely to hide an SCC, or ignore a two-node cycle because it is small. Boundary evidence: `reference/module-boundary-evaluation.md`.

## Prioritization

The existing Atlas ranking is:

`score = SCC_size*2 + churn_rate*5 + test_failures*3 + build_time_impact*4`

Its input units/normalization are not specified by the formula. Declare them with the observation window before using a score; without comparable inputs, report the underlying evidence and leave the score uncomputed. Do not fabricate a CI-blocking classification from arbitrary units.

| Existing score band | Planning priority |
|---------------------|-------------------|
| >40 | P0 — recommend a merge gate under the project's authorized policy |
| 25–40 | P1 — this quarter |
| 10–25 | P2 — next refactor |
| <10 | P3 — monitor |

The original bands overlap at 25. Report that boundary ambiguity for owner resolution rather than silently assigning a new policy. These are proposals; Atlas does not change code, CI or merge protection.

## Deliverable and Verification

Report scope/tool, SCC inventory (size, members, churn, relationship pattern, priority and selected strategy), the exact edges to remove/add, effort, risks, compatibility/migration order, implementation handoff and prevention plan. For each proposed fitness function, name its baseline and expected violating case. Use the existing configuration; never overwrite an architecture rules file with a sample.

VERIFY: a complete graph after the proposed changes has no targeted cycle; the replacement interface/event does not introduce a new SCC; tests cover ordering/initialization effects; and claimed measurements come from actual evidence. Hand visualization data to Canvas and the approved refactor to Zen/Builder through `reference/handoffs.md` and `_common/HANDOFF.md`.
