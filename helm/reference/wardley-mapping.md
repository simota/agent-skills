# Wardley Mapping Reference

Purpose: Apply Simon Wardley's value-chain and evolution mapping to visualize the strategic landscape. A Wardley Map plots components on two axes — anchored at user needs (value) and charted across evolution (genesis → custom → product → commodity) — to expose strategic choices, inertia, and climatic patterns.

## Scope Boundary

- **helm `wardley`**: Simon Wardley value-chain + evolution mapping (this document).
- **helm `porter` (elsewhere)**: Industry structure analysis. Porter is static; Wardley is evolutionary.
- **helm `jtbd` (elsewhere)**: Customer-job reframing. Wardley starts with user needs and traces the chain backwards.
- **helm `blue-ocean` (elsewhere)**: New market creation. Wardley reveals *where* on the map to create new space.
- **Atlas (elsewhere)**: Software architecture. Wardley is strategic; Atlas is structural.
- **Magi (elsewhere)**: Go/No-Go decision. Wardley provides the terrain for Magi's deliberation.

## Core Concepts

### Map vs Graph

A map has **position** and **direction**. A typical "architecture diagram" is a graph — nodes and edges without meaningful position. Wardley Maps add two axes:

- **Y-axis (value chain)**: visible to user at top; supporting components at bottom. Anchored at user need.
- **X-axis (evolution)**: Genesis → Custom → Product (+ rental) → Commodity (+ utility). Direction of evolution is left-to-right.

```
   Value      User Need
   (visible)  ┼─────────────── A  (visible component)
              │               ╱│
              │              ╱ │
              │             B  │  (custom-built)
              │            ╱│  │
              │           C │ D│  (products / rental)
   Invisible  │          ╱  │  │
              ┼──────────E──F──G── (commodity / utility)
                        │   │  │
                        ▼   ▼  ▼
         Genesis    Custom  Product  Commodity
              ←──── Evolution ────→
```

Each component's position encodes its evolutionary stage; each dependency encodes the value chain.

### Four Evolution Stages

| Stage | Definition | Examples | Characteristics |
|-------|-----------|----------|-----------------|
| **Genesis** | Novel, chaotic, rare, uncertain | Early research, new invention | Wonder, gamble, high cost, high variance |
| **Custom-built** | Unique per user, bespoke, limited copies | Early product attempts, consulting builds | Emerging understanding, high labor, learning phase |
| **Product (+ rental)** | Repeatable product / service with multiple vendors | Off-the-shelf software, subscriptions | Feature comparison, competition on differentiation |
| **Commodity (+ utility)** | Undifferentiated, cost-of-doing-business | Electricity, S3 storage, HTTP | Competition on cost/operational excellence, standardized |

Direction of evolution is one-way: components move right, not left. Attempting to "reinvent" a commodity as custom is usually strategic suicide.

### Characteristics by Stage

| Characteristic | Genesis | Custom | Product | Commodity |
|----------------|---------|--------|---------|-----------|
| Ubiquity | rare | uncommon | common | ubiquitous |
| Certainty | uncertain | emerging | stable | standard |
| Customer-perceived value | variable | high | moderate | low (assumed) |
| Failure mode | fatal / breakthrough | feature miss | losing race | commodity margin squeeze |
| Appropriate methodology | experimental | agile | lean / continuous improvement | Six Sigma / Ops |
| Appropriate structure | Pioneer | Settler | Town Planner | Town Planner |
| Culture | speculative | value-creation | efficient delivery | extreme efficiency |

Wardley's **Pioneer / Settler / Town Planner (PST)** organizational model maps which teams own which stage.

## Climatic Patterns

The map reveals universal patterns. Use these to interrogate any position.

### Core patterns

- **Everything evolves**: all components drift rightward over time.
- **Efficiency enables innovation**: commoditizing one layer liberates investment higher up.
- **Inertia grows with ubiquity**: users and organizations resist commoditization of familiar products.
- **Higher-order systems create new sources of worth**: once X commoditizes, Y built on top of X becomes a new genesis.
- **Past success breeds inertia**: the winning custom-build position becomes the chain to break.
- **Red Queen effect**: standing still = losing ground (competitors evolve).
- **No component is static**: if you don't migrate, someone will eat your position.

## Doctrine (Universal Principles)

Irrespective of context, good strategy applies these:

1. Focus on user needs.
2. Use a common language (maps).
3. Be transparent — share the map.
4. Challenge assumptions — is the component really at that stage?
5. Remove duplication — multiple teams building the same custom thing.
6. Use appropriate methodology per stage.
7. Think small (teams, contracts, services).
8. Use standards where appropriate — especially for commodities.
9. Design for constant evolution — every commodity was once a genesis.

## Gameplay / Strategic Moves

Wardley catalogs dozens of "gameplays." Key families:

| Family | Examples | When appropriate |
|--------|----------|------------------|
| Accelerator | Open source a component, sponsor competition | Force commoditization of adjacent component |
| Decelerator | FUD, patents, licensing, regulation | Slow competitor evolution |
| Market | Pricing, differentiation, geography | Shape demand |
| Ecosystem | Platform + third-party innovation (ILC: innovate-leverage-commoditize) | Extract signal from the edge |
| Defensive | Exit, retirement, sunset | Recognize when a position is indefensible |
| Attack | Fool's mate (attack an inert competitor) | When competitor has inertia |

### ILC loop (classic Wardley pattern)

> **Innovate** internally → **Leverage** the ecosystem that forms around you → **Commoditize** the successful piece, freeing the next layer.

AWS did this: launched S3/EC2 → ecosystem built products on top → AWS folded successful abstractions (Lambda, Aurora) back down to commodity.

## Workflow

```
ANCHOR      →  identify the user need (who + what job)
            →  not "customer" (internal user, admin, ops are users too)

CHAIN       →  list components required to deliver that need
            →  include tech + data + people + processes

POSITION    →  place each component at the right evolutionary stage
            →  consider: ubiquity, certainty, comparable-market evidence

DRAW        →  plot value chain vertically (user at top)
            →  plot evolution horizontally
            →  draw dependencies (chain edges)

SCAN-CLIMATE→  identify inertia, duplication, stage mismatches
            →  spot higher-order-system opportunities
            →  note competitor positions on same map

APPLY       →  apply doctrine (focus, remove duplication, right methodology per stage)
            →  select gameplays (accelerator/decelerator/ecosystem/attack)

DECIDE      →  make strategic choices with the map as evidence
            →  assign Pioneer/Settler/Town Planner ownership
            →  hand off to Magi for arbitration if trade-offs exist
```

## Common Strategic Mistakes (the map makes visible)

| Mistake | Signal on the map | Correction |
|---------|-------------------|------------|
| Building custom what is commodity | Component in Custom but industry-wide has it in Commodity | Buy/rent, reassign team |
| Managing commodity with Pioneer methodology | Genesis methodology applied to known commodity | Switch to operational excellence (Town Planner) |
| Standardizing too early | Standard applied to Genesis component | Delay; let variants explore |
| Ignoring higher-order opportunity | Commoditized layer sits dormant, no new genesis above | Invest in genesis above the commoditized base |
| Relying on a single vendor for commodity | No second source | Encourage utility / multi-vendor |
| Pioneer team reassigned to Town Planner work | Wrong structure for stage | Rotate people; use PST |

## Output Template

```markdown
## Wardley Map: [Anchor user need]

### Anchor
- **User**: [who]
- **Need**: [what job — not a feature]

### Value Chain (top → bottom = visible → invisible)
1. [Component A] — visible to user
2. [Component B] — supports A
3. [Component C] — supports B
4. ...

### Evolution Positions
| Component | Stage | Evidence |
|-----------|-------|----------|
| A | Custom | [market signal, competitor analysis] |
| B | Product | [multiple vendors exist] |
| C | Commodity | [utility / price competition] |
| ... | ... | ... |

### Map Sketch (ASCII or image)
```
[user need]──[A: Custom]──[B: Product]──[C: Commodity]
                          [D: Custom]─────┘
```

### Climate & Inertia Findings
- [ ] Component X has inertia — [why]
- [ ] Component Y is positioned wrong (we custom-build but industry-commoditized)
- [ ] Duplication: team α and β both build [Z] — consolidate
- [ ] Higher-order opportunity: commoditized [C] enables new genesis [N]

### Strategic Moves
| Move | Component | Rationale |
|------|-----------|-----------|
| Accelerator: open-source | [X] | force [Y] to commodity |
| Ecosystem: ILC | [platform] | leverage third-parties, fold back |
| Defensive: sunset | [Z] | indefensible position |

### Pioneer / Settler / Town Planner
- **Pioneer team** owns: [genesis components]
- **Settler team** owns: [custom → product transition]
- **Town Planner team** owns: [product → commodity, ops]

### Doctrine Check
- [ ] Anchored at user need
- [ ] Map shared with stakeholders
- [ ] Appropriate methodology per stage
- [ ] Duplication removed
- [ ] Standards applied where appropriate

### Handoffs
- Atlas: architecture follow-through on commoditized / standardized layers
- Shift (`detect`/`modernize`/`radar`): modernization plan for components that must evolve (absorbed from horizon)
- Magi: Go/No-Go on strategic moves
- Spark: genesis opportunities for new features
- Ledger: cost implications of commodity vs custom
- Scribe: written strategy document
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Drawing a graph, not a map | Enforce Y=value, X=evolution; position must mean something |
| Not anchoring at user need | Start with user + job, not technology |
| Mixing evolution with maturity | Evolution = industry-wide stage, not how mature *your* implementation is |
| Static map (draw once, forget) | Re-map when competitor moves or new commoditization hits |
| Ignoring inertia | Name it explicitly; plan against it |
| Custom-building commodities | Buy/rent; reserve engineers for genesis |
| Same methodology everywhere | Apply experimental / agile / lean / Six Sigma by stage |
| PST ownership mismatch | Rotate Pioneer/Settler/Town Planner by component stage |

## Deliverable Contract

When `wardley` completes, emit:

- **Anchor** with user and need.
- **Value chain** from visible (user-facing) to invisible (supporting).
- **Evolution positions** for every component with evidence.
- **Map sketch** (ASCII or image).
- **Climate & inertia findings**.
- **Strategic moves** chosen with rationale.
- **Pioneer / Settler / Town Planner** ownership assignments.
- **Doctrine checklist**.
- **Handoffs**: Atlas, Shift (`detect`/`modernize`/`radar`), Magi, Spark, Ledger, Scribe.

## References

- Simon Wardley — *Wardley Maps* (CC-licensed book, Medium series)
- Learn Wardley Mapping — learnwardleymapping.com (tutorial)
- Ben Mosior — *Hired Thought* blog and YouTube
- onlinewardleymaps.com — free browser-based mapping tool. The **June 2025 modernisation release** ([docs.onlinewardleymaps.com 2025-06-15](https://docs.onlinewardleymaps.com/blog/2025-06-15-release-note/)) ships a TypeScript rewrite, a resizable split-pane editor, and a simplified DSL with new decorator syntax (legacy maps still parse).
- *Topographical Intelligence for Your Business* — HBR write-up of the framework
- LEF (Leading Edge Forum) — Wardley's original research
- "Crossing the River by Feeling the Stones" — Wardley's essay on the doctrine
- Mark Craddock — *Learn Wardley Mapping* (Medium, Apr 2026) — Claude Code skill benchmarked blind against 25 of Wardley's own published maps; documents the OWM-DSL-as-LLM-target pattern.
- Mermaid Wardley Map support — community PR landed 2025; LLMs can now emit Wardley diagrams directly into Mermaid blocks for inline rendering.
- Simon Wardley — *Craft Conference 2025* (Budapest, May 2025) keynote on mapping the AI value chain; also `Agile Meets Architecture 2025` speaker billing.

## 2025-2026 AI Tooling for Wardley Maps

Three classes of AI tooling now coexist; treat them as Tier 4 defaults, never as truth:

| Class | Examples | Use | Risk |
|-------|----------|-----|------|
| Claude / GPT skills emitting OWM-DSL | `haberlah/wardley-mapping` (Claude Code skill, 2026), `IanSimon23/wardley_maps` | First-draft maps from a scenario description; export to onlinewardleymaps.com | LLM may collapse Custom and Product when the industry signal is ambiguous — always demand an evidence column |
| LLM-in-Mermaid | community Mermaid plugin (2025) | Inline maps in chat or PR comments | No interactive editing; positions are not stable across regenerations |
| Drag-and-drop with AI coach | `IanSimon23/wardley_maps`, MCP-market "Wardley Strategy Mapping" skill (2026) | Workshops and reviews | Coach text reflects training-set bias toward AWS / SaaS exemplars; sanity-check on non-software domains |

Always require the AI to attach an **Evidence** column per component (per the Output Template) and to name the inertia it sees — otherwise the map is graph, not map.
