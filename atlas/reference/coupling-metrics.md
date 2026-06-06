# Coupling Metrics Reference

Purpose: Quantitative module coupling assessment using Robert C. Martin's metrics (Ca, Ce, Instability, Abstractness, Distance from Main Sequence). Identifies modules outside the healthy design zone and proposes targeted interventions.

## Contents

- Core metrics
- Main Sequence interpretation
- Zones and classifications
- Per-module targets
- Command recipes
- Output template

## Core Metrics

For each module:

| Metric | Formula | Meaning | Target |
|--------|---------|---------|--------|
| **Ca** (Afferent Coupling) | count of modules that depend on this | "how reused am I" | project-specific |
| **Ce** (Efferent Coupling) | count of modules this depends on | "how many things do I need" | as low as reasonable |
| **I** (Instability) | Ce / (Ca + Ce) | 0 = stable, 1 = unstable | see zones |
| **A** (Abstractness) | abstract_types / total_types | 0 = concrete, 1 = abstract | matches I |
| **D** (Distance) | |A + I − 1| | distance from Main Sequence | < 0.3 |

### Quick Intuitions

- **High Ca, low Ce**: foundational, widely reused → must be stable, prefer abstract (framework / domain model)
- **Low Ca, high Ce**: leaf / consumer → can be unstable and concrete (entry points, CLI, UI adapters)
- **High Ca, high Ce**: central hub, risky to change → God Package candidate
- **Low Ca, low Ce**: orphan or utility → check if actually used

## Main Sequence Interpretation

Plot each module on (A, I). The **Main Sequence** is the line `A + I = 1`.

```
A
1 ●──── Zone of Uselessness
  │ (abstract & stable-not-used)
  │
  │        ╲     Main Sequence
  │         ╲    (A + I = 1)
  │          ╲
  │           ╲
0 └────────────● Zone of Pain
  0           1  (concrete & many depend on it)
                 I
```

### Zones

| Zone | Location | Meaning | Action |
|------|----------|---------|--------|
| **Main Sequence** | D < 0.3 | Balanced | preserve |
| **Zone of Pain** | A low, I low | Concrete + many depend on it | introduce abstractions, freeze API |
| **Zone of Uselessness** | A high, I high | Abstract + unused | delete or promote usage |
| **Acceptable band** | D < 0.5 | Tolerable drift | monitor |
| **Outside band** | D >= 0.5 | Design issue | fix |

## Zones and Classifications

### Critical: Zone of Pain (A < 0.2, I < 0.2)

Stable concrete module. Changes ripple widely, no interfaces to mock.

**Fix**: Extract stable abstractions (interfaces, traits, protocols), make dependents depend on abstraction.

### Critical: Zone of Uselessness (A > 0.8, I > 0.8)

Abstract but nobody uses it. Waste of design.

**Fix**: Either delete (handoff Void) or find the real consumer and shift imports.

### Warning: Unstable foundation (I > 0.7 AND Ca > 5)

High fan-in but module is still unstable — any change breaks many dependents.

**Fix**: Stabilize (reduce Ce), or split into stable core + unstable extension.

### Warning: Over-abstract (A > 0.6 AND Ca < 2)

Lots of interfaces but barely used — premature abstraction.

**Fix**: YAGNI (handoff Void), collapse interfaces back into concrete until real variant emerges.

## Per-Module Targets by Role

| Module role | Target I | Target A | Example |
|-------------|----------|----------|---------|
| Domain model / entities | 0.0–0.2 | 0.6–0.9 | `order.Order`, `user.User` |
| Shared library / SDK | 0.0–0.2 | 0.7–0.9 | `logging`, `validation` |
| Service / application layer | 0.3–0.6 | 0.3–0.5 | `order/service`, `checkout/workflow` |
| Adapter / infra | 0.6–1.0 | 0.0–0.3 | `postgres/repository`, `stripe/client` |
| Entry point / CLI / UI | 0.8–1.0 | 0.0–0.2 | `main.go`, `App.tsx` |

A module whose actual metrics diverge significantly from its role's target is a design smell.

## Command Recipes

### JS/TS

```bash
# dependency-cruiser has metrics output
npx depcruise --output-type metrics src

# jscpd for duplication (related)
npx jscpd src/
```

### Python

```bash
pip install radon
radon mi mypackage/          # Maintainability Index (related)
# No built-in Martin metrics; use pydeps + custom script
```

### Java

```bash
# JDepend computes Ca, Ce, A, I, D natively
java -jar jdepend.jar com.myapp > metrics.txt

# NDepend (.NET) does this out of the box
```

### Go

```bash
# Use go/parser + custom analyzer, or
go get github.com/fzipp/gocyclo
gocyclo -avg .
# For Ca/Ce, use `goda graph` + post-processing
```

### Generic (language-agnostic)

Build the module dep graph, then:

```python
# Compute Ca, Ce, I, A, D per module
import networkx as nx

g = load_dep_graph()  # DiGraph of module-level deps

for module in g.nodes:
    ce = g.out_degree(module)
    ca = g.in_degree(module)
    i = ce / (ca + ce) if (ca + ce) else 0
    # A requires counting abstract types per module (language-specific)
    a = count_abstract(module) / count_total_types(module)
    d = abs(a + i - 1)
    print(f"{module}\tCa={ca}\tCe={ce}\tI={i:.2f}\tA={a:.2f}\tD={d:.2f}")
```

## Output Template

```markdown
## Atlas Coupling Assessment

**Scope**: `internal/` (Go, 58 packages)
**Tool**: `goda graph` + custom metrics script
**Main Sequence health**: 42/58 modules within D < 0.3 (72%)

### Zone Distribution

| Zone | Count | Modules (top offenders) |
|------|-------|-------------------------|
| Main Sequence (D<0.3) | 42 | — |
| Acceptable (0.3–0.5) | 9 | `order/service`, `auth/handler`, ... |
| Zone of Pain | **4** | `db/models`, `util/common`, `errors`, `types` |
| Zone of Uselessness | 3 | `abstract/factory`, `unused/registry`, `proto/v1` |

### 🔴 Zone of Pain: `internal/types`

**Metrics**: Ca=34, Ce=1, I=0.03, A=0.12, D=0.85

**Problem**: 34 modules depend on `types`, but it is 88% concrete struct definitions. Any field addition triggers 34 rebuilds, any breaking change ripples project-wide.

**Fix**:
1. Identify interfaces that 80% of consumers actually need
2. Extract `types/contract` (abstract) separate from `types/impl` (concrete)
3. Point consumers at `types/contract`
4. Target: A → 0.7, D → 0.3

**Effort**: L (~1 week)
**Handoff**: `adr` (record decision), then Zen

### 🟡 Zone of Uselessness: `abstract/factory`

**Metrics**: Ca=1, Ce=0, I=0, A=1.0, D=0.0 (technically on Main Sequence but A=1 + Ca=1 is uselessness indicator)

**Problem**: fully abstract, only one consumer, no implementation variants planned (confirmed via git blame + spec review).

**Fix**: Delete. Inline the one consumer's usage.

**Effort**: S (30 min)
**Handoff**: Void (YAGNI verdict) → Zen (deletion)

### Role-vs-Actual Deviations

| Module | Role | Target (I, A) | Actual | Gap |
|--------|------|---------------|--------|-----|
| `order/service` | service layer | (0.3–0.6, 0.3–0.5) | (0.78, 0.15) | too unstable + too concrete |
| `db/repository/pg` | infra adapter | (0.6–1.0, 0–0.3) | (0.22, 0.0) | should be unstable; too many things depend on it |

### Fitness Function Recommendation

```yaml
- name: Main Sequence compliance
  run: |
    python scripts/coupling_metrics.py internal/ \
      --fail-on "D > 0.5" \
      --ignore-existing
```

### Next Steps

1. `types` split → ADR + Zen (P0)
2. Delete `abstract/factory` → Void + Zen (P2)
3. Install fitness function → Gear
```

## Anti-Patterns

- Minimizing D globally (loses meaningful variation per role)
- Treating all high-Ca modules as problems (some are legitimate foundations)
- Ignoring A when interpreting I (instability is context-dependent on abstractness)
- Optimizing metrics on noise (small modules have volatile numbers; set min-size threshold)
- One-time audit without fitness function (metrics drift within weeks)
