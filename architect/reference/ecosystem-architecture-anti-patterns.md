# Ecosystem Architecture Review

Read during ANALYZE. Use actual skill ownership from `_common/BOUNDARIES.md`, the authoritative scaffold `_templates/SKILL_TEMPLATE.md`, and orchestration contracts `_common/SUBAGENT.md` / `_common/PARALLEL.md`. Do not maintain a copied roster or a second category registry.

## Evidence → Decision

| Evidence | Review action |
|----------|---------------|
| One agent can satisfy the acceptance criteria | Do not add coordination; improve the existing owner |
| Three prompt-only revisions fail on the same behavior | Inspect missing context, ownership and orchestration before another wording change |
| 10+ declared capabilities | Check for a God Agent; propose a responsibility split only for independently owned outputs |
| Two agents always change together | Test whether the boundary is artificial; compare a merged design before recommending one |
| A new agent has fewer than three concrete product needs | Recheck whether an extension of an existing owner suffices |
| Usage below 10% of relevant opportunities | Investigate phantom scope; a review signal is not authorization to retire an agent |
| Cyclic dependencies or recurring handoff bounces | Define the hub-owned dependency order, join and finite stop condition |
| Context grows through raw history or repeated handoffs | Identify the state actually needed at the next action; preserve evidence and contract delivery |
| More workers but no independent work/owned artifacts | Remove speculative parallelism; use measured coordination cost and task dependencies |
| More than eight agents in one category | Check whether ownership is clear; do not split a category just to meet a count |

Do not resolve a supervisor bottleneck by bypassing Nexus. Use bounded fan-out/gather or a justified hierarchy with explicit ownership and joins. Flat peer-to-peer or swarm examples are not repository authorization.

## Health Review Signals

| Signal | Existing review threshold |
|--------|---------------------------|
| Agents used monthly | At least 80% |
| Functional overlap | Under 30%; approval/rejection bands in `reference/overlap-detection.md` |
| Average Health Score | At least 80; name the rubric used |
| Routing/agent-definition drift | Reconcile within one sprint |
| Category population | Review outside 2–8, not an automatic restructure |
| Orphan agents | Zero |
| Individual Health Score | Below 70: evaluate an improvement proposal |

Record observations, denominators and the proposed action. Missing activity evidence is unknown, not zero. Retirement, replacement or routing changes still follow their owning skill and approval gates; these heuristics never authorize deletion on their own.
