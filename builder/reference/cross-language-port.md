# Cross-Language Port Reference

Purpose: Port business logic from one language/framework to another while guaranteeing behavior equivalence. Uses a test-first parallel-run strategy — the source is treated as the authoritative spec and the port must match its outputs.

## Scope Boundary

- **Builder `port`**: implementation execution (writing target-language code, running tests)
- **Shift (elsewhere)**: large-scale migration **planning** (Strangler Fig, Branch by Abstraction, rollout phases)

Use Shift first for anything > 1 module. Use `port` for a single module / function / service being moved.

## Workflow

```
1. INVENTORY the source: public API, inputs, outputs, side effects, exceptions
2. PIN behavior with tests (if missing, write golden tests against source first)
3. PORT target-language tests (same cases, idiomatic to target)
4. IMPLEMENT target code until target tests pass
5. PARALLEL-RUN source + target against shared input set; diff outputs
6. HANDOFF cutover to Shift (rollout phase) or Guardian (merge)
```

## Golden Test Pattern

Before touching the port, capture source behavior:

```python
# test_golden.py
import json
from source import parse_phone  # existing source implementation; str | None in/out

def test_capture_goldens():
    cases = [
        '+1 (555) 123-4567',
        '555-1234',
        '03-1234-5678',
        '',
        None,
        'not-a-phone',
    ]
    goldens = [{"input": c, "expected": parse_phone(c)} for c in cases]
    with open('goldens.json', 'w') as f:
        json.dump(goldens, f)
```

Then run against the port:

```go
// port_test.go
package port

import (
    "encoding/json"
    "os"
    "testing"
)

type Case struct {
    Input    *string `json:"input"`
    Expected *string `json:"expected"`
}

// ParsePhone accepts and returns *string to preserve Python's None values.
func TestPortMatchesGoldens(t *testing.T) {
    data, err := os.ReadFile("goldens.json")
    if err != nil {
        t.Fatal(err)
    }
    var goldens []Case
    if err := json.Unmarshal(data, &goldens); err != nil {
        t.Fatal(err)
    }
    if len(goldens) == 0 {
        t.Fatal("golden cases must not be empty")
    }
    for _, c := range goldens {
        got := ParsePhone(c.Input)
        if (got == nil) != (c.Expected == nil) ||
            (got != nil && c.Expected != nil && *got != *c.Expected) {
            t.Errorf("input=%v got=%v want=%v", c.Input, got, c.Expected)
        }
    }
}
```

## Language-Specific Gotchas

| Pair | Common divergence |
|------|-------------------|
| Python → Go | nil vs None, int overflow, UTF-8 vs unicode, exception → error return |
| JS → TS | implicit any, runtime vs compile-time types, `null` vs `undefined` |
| JS/TS → Rust | ownership / borrowing, `unwrap` vs Option/Result, sync vs async |
| Ruby → Go | missing stdlib features, regex flavor (Ruby: Oniguruma, Go: RE2) |
| Java → Kotlin | nullability, data class default equals, checked exception removal |
| Python → TS | duck typing vs structural types, decimal precision, timezone |
| PHP → Node | weak vs strict equality, associative arrays → objects/maps |

Document each divergence in the port report.

## Parallel-Run Harness

```bash
set -euo pipefail

# Generate random inputs
python gen_inputs.py > inputs.jsonl

# Run both, normalize JSON, and preserve failures from either program or jq.
python -m source < inputs.jsonl > source_out.jsonl
./target < inputs.jsonl > target_out.jsonl
jq -cS . source_out.jsonl > source_normalized.jsonl
jq -cS . target_out.jsonl > target_normalized.jsonl
diff -u source_normalized.jsonl target_normalized.jsonl
```

Property-based testing is ideal (hypothesis, fast-check, QuickCheck).

## When to STOP the Port

- Source has non-deterministic behavior (depends on process memory layout, CPU flags, insertion order of non-ordered collections)
- Source depends on language-specific semantics with no target equivalent (Python `__del__` vs Go GC)
- Test coverage of source is < 60%; risk of silent behavior drift is too high
- Migration plan is actually larger than single module → handoff to **Shift**

## Output

- Port diff against source API (signature changes, nullability shifts)
- Golden test suite in target language
- Parallel-run report (N inputs tested, 0 mismatches)
- Divergence log (intentional behavior changes, idiomatic adjustments)
- Follow-up handoff: Shift (cutover), Guardian (PR), Radar (coverage fill)
