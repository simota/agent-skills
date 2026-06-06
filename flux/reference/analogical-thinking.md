# Analogical Thinking & Structural Mapping Reference

Purpose: Disciplined cross-domain analogy generation grounded in Dedre Gentner's structural-mapping theory (1983), which distinguishes surface similarity (objects look alike) from structural similarity (relational systems align). Far analogies — those crossing distant domains — yield the most innovation but are the hardest to find. Biomimicry, cross-industry pattern hunting, and engineering analogies all fall under this lens. Analogy fires best when the problem has clear *relational structure* (causes, constraints, flows) that can be mapped to a source domain.

## Scope Boundary

- **flux `analogy`**: structural mapping from a source domain into the target problem. Produces aligned-relations table with novelty, transferability, and breakdown points.
- **flux `reframe` (default)**: full DEEP pipeline — analogy is one optional stage inside COMBINE.
- **flux `cross`**: Bisociation-style cross-domain combine. Cross treats two domains as raw material to fuse; `analogy` aligns *relations* and tests transfer.
- **flux `scamper`**: intra-artifact modification. Lens A (Adapt) is shallow analogy; `analogy` is the deep version.
- **flux `challenge`**: assumption reversal. Use first if the source domain itself encodes hidden assumptions.
- **flux `inversion`**: invert-the-goal. Inversion asks "what guarantees failure"; analogy asks "what shape solved it elsewhere".
- **riff (elsewhere)**: iterative dialogue. Analogy is a single mapping pass; Riff can develop one analogy across turns.
- **field (elsewhere)**: empirical validation. Analogies predict; research confirms transferability.

## Workflow

```
ENTER    →  state target problem as a relational structure
         →  list entities, relations, constraints, flows, goals

DISTANCE →  decide near vs far analogy budget
         →  near = same industry; mid = adjacent; far = distant domain / nature

HUNT     →  search candidate sources (catalog + free-form)
         →  generate ≥5 candidates across the chosen distance

MAP      →  align relations source → target (not objects → objects)
         →  mark which relations transfer cleanly, which break

TEST     →  identify breakdown points — where the analogy lies
         →  rate transferability (high / partial / metaphor-only)

DELIVER  →  hand to Spark (feature ideas), Atlas (architecture
            patterns), Magi (cross-option decision)
```

## Near vs Far Analogy

| Distance | Source | Strength | Risk |
|----------|--------|----------|------|
| **Near** | Same industry, similar product | High transferability, low novelty | Reinforces industry orthodoxy |
| **Mid** | Adjacent industry, different scale | Balanced novelty/transferability | Surface-similar traps |
| **Far** | Distant domain (biology, physics, history, art) | High novelty, hard to transfer | Metaphor masquerading as insight |

Innovation research (Gentner; cross-industry studies of financial-services lateral thinking) shows far analogies yield the most viable novelty when relational alignment is rigorous — and the most empty rhetoric when it is not.

## Biomimicry Catalog (selected starting points)

| Source pattern | Target uses |
|----------------|-------------|
| Termite mound passive cooling | HVAC, datacenter thermal design |
| Gecko foot van der Waals adhesion | Reusable fasteners, climbing surfaces |
| Beehive honeycomb load distribution | Lightweight structural panels, server racks |
| Slime mold network optimization | Logistics routing, network topology |
| Mycorrhizal nutrient exchange | Resource-sharing platforms, federated systems |
| Octopus distributed cognition | Edge computing, decentralized agents |
| Forest succession | Product lifecycle, ecosystem strategy |
| Predator-prey cycles | Auction dynamics, market timing |

## Cross-Industry Pattern Hunting

| Pattern | Origin | Frequently borrowed into |
|---------|--------|--------------------------|
| Subscription economics | Magazines | SaaS, fitness, food |
| Just-in-time inventory | Toyota | Software deployment, content |
| Loyalty stamp cards | Cafés | Apps, B2B retention |
| Hub-and-spoke | Airlines | Logistics, microservices |
| Loss-leader pricing | Retail grocery | Freemium SaaS |
| Apprenticeship | Crafts | Onboarding, mentorship programs |
| Triage | ER medicine | Incident response, support queues |

## Question Bank for Structural Mapping

- What is the *relation* between A and B in the source? Does that relation exist in target?
- Which entities in source map to which in target? Multiple candidates? Pick by relational role.
- What constraint in source is *absent* in target? That absence often invalidates transfer.
- What constraint in target is *absent* in source? That absence often gives the analogy power.
- Where does the analogy break? Naming the breakdown is half the insight.
- Is the surface similarity (looks alike) or structural (works alike)? Surface alone is decoration.

## Anti-Patterns

- Surface-similarity hunting — "this looks like X" without aligning relations. Produces metaphors, not insight.
- One-analogy commitment — locking onto first analogy and forcing fit. Generate ≥5, kill 4.
- Far-analogy theater — citing biomimicry without testing transfer. "Like a beehive" is rhetoric until relations are mapped.
- Ignoring breakdown points — every analogy breaks somewhere. Where it breaks is often the most useful signal.
- Confirming the preferred reframing — searching only for analogies that support the existing hypothesis. Deliberately seek disconfirming analogies.
- Mapping objects instead of relations — Gentner's core insight: align the relational system, not the entities.
- Treating analogy output as evidence — analogy generates *hypotheses*. Validate empirically before betting.
- Skipping near analogies for the glamour of far ones — near analogies often transfer cleanest. Far is high-variance, not always high-EV.

## Handoff

- **To Spark**: high-transferability mappings as feature concept candidates.
- **To Atlas**: structural patterns that map to architecture decisions (hub-and-spoke, succession, mycorrhiza).
- **To Magi**: when multiple analogies suggest competing actions — decision needed.
- **To Riff**: when one analogy looks promising but the mapping is incomplete — iterate.
- **To Omen**: breakdown points as failure-mode candidates for pre-mortem.
- **To `inversion`**: when the analogy suggests a path, run inversion on that path to surface failure modes.
- **To Field**: high-novelty far analogies needing empirical validation before commitment.
