# Circular Dependency Remediation Reference

Purpose: Detect strongly connected components (SCCs) in the dependency graph and produce a prioritized break-plan. Each cycle gets a recommended strategy — dependency inversion, interface extraction, module re-layering, or merge.

## Contents

- Why cycles matter
- Detection
- SCC classification
- Break strategies (5 patterns)
- Prioritization
- Command recipes
- Output template

## Why Cycles Matter

- **Build**: parallel compilation blocked, incremental rebuild invalidated
- **Test**: units cannot be mocked independently
- **Deploy**: microservice extraction impossible without breaking
- **Reason**: understanding requires holding entire cycle in mind
- **Change risk**: modification blast radius = entire cycle

Cyclic dependencies are *always* an architectural smell in module-level graphs. Tolerate only in tight intra-module class graphs with clear shared state.

## Detection

| Language | Tool |
|----------|------|
| JS/TS | `madge --circular`, `dpdm`, `eslint-plugin-import (no-cycle)` |
| Python | `pydeps`, `pylint (cyclic-import)`, `import-linter` |
| Go | `go vet`, `golangci-lint (depguard)`, `gomod-graph` |
| Java/Kotlin | `jdeps`, `ArchUnit`, `jQAssistant` |
| Rust | `cargo deps`, `cargo-modules`, compiler (crate-level cycles are errors) |
| C# | NDepend, `dotnet-depends` |
| Ruby | `debride`, `rubycritic` |

Output Tarjan's or Kosaraju's algorithm result — list of SCCs, each SCC size > 1 is a cycle.

## SCC Classification

For each detected SCC, classify:

| Size | Pattern | Typical cause |
|------|---------|---------------|
| 2 | direct cycle | bidirectional helper use, circular imports |
| 3–5 | small clique | missing layer, mis-extracted utility |
| 6–20 | module blob | bounded context leak, missing boundary |
| 20+ | architectural failure | requires `boundary` Recipe before `cycle` |

Additionally, classify by **direction reversibility**:

- **Flippable**: one edge is clearly "wrong-direction" (e.g., upper layer imports lower-layer test)
- **Symmetric**: both directions seem legitimate — requires design change
- **Accidental**: cycle via transitive dep through a utility — often fixable by moving utility

## Break Strategies

### 1. Dependency Inversion (DIP)

```
Before:                       After:
  A → B → A                     A → IPort ← B
                                (B implements IPort)
```

Best for: cross-layer cycles where A is policy, B is mechanism. Introduce an abstraction A owns.

### 2. Interface Extraction

```
Before:                       After:
  A ↔ B                         A → I ← B
                                (I contains shared contract)
```

Best for: symmetric cycles between peers. Extract shared types/contracts to a neutral module.

### 3. Module Merge

```
Before:                       After:
  A ↔ B                         AB (single module)
```

Best for: cycles of size 2 where A and B are tightly coupled and split was artificial. Low effort, reduces module count.

### 4. Event / Message Decoupling

```
Before:                       After:
  A → B → A                     A → Bus ← B
                                (event-driven)
```

Best for: cycles where the feedback edge is notification-like. Use pub/sub or domain events.

### 5. Module Re-layering (split)

```
Before:                       After:
  A ↔ B                         A_core ← B, A_ext → B
                                (split A into what B needs vs consumes)
```

Best for: God-Class-like A that has legitimate bidirectional need — split A along the line B uses vs the line B is used from.

## Prioritization

Score each SCC and attack highest-score first:

```
Score = (SCC_size × 2) + (churn_rate × 5) + (test_failures × 3) + (build_time_impact × 4)
```

| Score | Priority |
|-------|----------|
| > 40 | P0 — block merges to involved files |
| 25–40 | P1 — fix this quarter |
| 10–25 | P2 — fix in next refactor window |
| < 10 | P3 — document and monitor |

## Command Recipes

```bash
# TypeScript/JS
npx madge --circular --extensions ts,tsx src/
npx madge --image deps.svg src/         # visualize

# Python
pip install pydeps
pydeps mypackage --show-cycles --max-bacon 2 --cluster

# Go
go mod graph | <cycle-detector>
# or: github.com/loov/goda
goda graph "reach(./...)" | dot -Tsvg > deps.svg

# Java
jdeps --print-module-deps target/myapp.jar

# Generic: build a graph + use networkx
python -c "
import networkx as nx, json, sys
g = nx.DiGraph()
for line in sys.stdin:
    src, dst = line.strip().split(' -> ')
    g.add_edge(src, dst)
sccs = [s for s in nx.strongly_connected_components(g) if len(s) > 1]
for i, s in enumerate(sccs, 1):
    print(f'SCC #{i} ({len(s)}): {sorted(s)}')
"
```

### Prevent regression

Add a CI fitness function that fails the build on new cycles:

```bash
# Example: dependency-cruiser (JS/TS)
echo '{"forbidden":[{"name":"no-circular","severity":"error","from":{},"to":{"circular":true}}]}' > .dependency-cruiser.json
npx depcruise --config .dependency-cruiser.json src
```

## Output Template

```markdown
## Atlas Circular Dependency Remediation

**Scope**: `src/` (TypeScript, 342 modules)
**Tool**: `madge --circular`
**SCCs detected**: 5 (total cycle edges: 18)

### SCC Inventory

| # | Size | Members | Churn (90d) | Pattern | Priority | Strategy |
|---|------|---------|-------------|---------|----------|----------|
| 1 | 8 | auth/*, user/*, session/* | HIGH | module blob | **P0** | Boundary split (handoff `boundary`) |
| 2 | 3 | order/service, order/events, inventory/hook | MED | symmetric | **P1** | Event decoupling (#4) |
| 3 | 2 | utils/format, utils/parse | LOW | accidental | **P2** | Module merge (#3) |
| 4 | 2 | config/loader, logger | MED | flippable | **P1** | DIP (#1) — logger gets Config interface |
| 5 | 4 | payment/*, billing/* | LOW | small clique | **P2** | Interface extraction (#2) |

### P0: Module Blob `auth/*, user/*, session/*`

**Recommendation**: escalate to `boundary` Recipe first — this SCC indicates a bounded-context leak, not a cycle fix candidate.

### P1: order ↔ events ↔ inventory (Event Decoupling)

**Current**:
```
order/service.ts → inventory/hook.ts → order/events.ts → order/service.ts
```

**Proposed**:
```
order/service.ts → EventBus ← inventory/hook.ts
order/events.ts → EventBus (publish only)
```

**Steps**:
1. Add `EventBus` interface in `shared/events/`
2. `order/events.ts` publishes `OrderConfirmed` event
3. `inventory/hook.ts` subscribes to bus instead of calling service directly
4. Remove `order/service → inventory/hook` import

**Effort**: M (4–6h)
**Risk**: Medium — event ordering must be tested
**Handoff**: Zen (refactor), Radar (subscription test)

### P1: config/loader ↔ logger (DIP)

**Current**: `config` imports `logger` for init logs; `logger` imports `config` to read log level.

**Proposed**:
- Define `ConfigProvider` interface in `logger/`
- `logger` depends on `ConfigProvider`, not `config`
- `config` implements `ConfigProvider`

**Effort**: S (1–2h)
**Handoff**: Zen

### Fitness Function Recommendation

Add to CI:
```yaml
- name: No new cycles
  run: npx madge --circular --exit-code src/
```

### Next Steps

1. Handoff P0 to `/atlas boundary` for bounded-context analysis
2. Implement P1 fixes this sprint (Zen)
3. Add CI fitness function (handoff Gear)
```

## Anti-Patterns

- Breaking one edge of a large SCC (other edges keep cycle alive)
- "Just use lazy import" — hides cycle at runtime, breaks bundling and type checking
- Merging modules to "fix" a cycle that was a real separation of concerns
- Introducing a god-utility module that everyone depends on (creates single point of failure)
- Ignoring SCC size 2 as "not a big deal" — they compound into larger blobs over time
