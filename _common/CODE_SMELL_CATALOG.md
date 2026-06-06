# Code Smell Catalog (Master Reference)

Centralized taxonomy of structural code smells shared across skills.
Each entry is a smell **name + definition + recognition pattern + canonical example + severity hint**.

Consumers:
- `zen/reference/code-smells-metrics.md` — refactor mechanic + complexity metrics per smell.
- `judge/reference/code-smell-detection.md` — detection-during-review heuristic + severity weighting.

Severity hint is a baseline for review reports; individual skills may re-weight based on context.

---

## 1. Bloaters (Overly Large Code)

### BLOAT-001: Long Method / Function
- **Definition:** A single function carries too much logic to read or test in one breath.
- **Recognition:** > 50 LOC, > 5 parameters, or > 3 distinct processing steps.
- **Severity hint:** LOW.
- **Example:**
  ```typescript
  function processOrder(userId, productId, quantity, price, currency, discount, ...) {
    // validation + pricing + persistence + notification — all inline
  }
  ```

### BLOAT-002: Large Class / God Class
- **Definition:** A class/module that owns many unrelated responsibilities.
- **Recognition:** Methods > 20, LOC > 500, or fan-out (collaborators) > 10.
- **Severity hint:** MEDIUM.
- **Example:**
  ```typescript
  class UserManager {
    createUser(); deleteUser();
    sendEmail();         // mail concern
    generateReport();    // reporting concern
    processPayment();    // payment concern
  }
  ```

### BLOAT-003: Long Parameter List
- **Definition:** Function signature with too many positional parameters.
- **Recognition:** > 4 parameters, or 3+ params of the same primitive type.
- **Severity hint:** LOW.

### BLOAT-004: Data Clumps
- **Definition:** The same group of fields appears together in many places.
- **Recognition:** Same 3+ fields co-occurring in multiple classes/signatures.
- **Severity hint:** LOW.

### BLOAT-005: Primitive Obsession
- **Definition:** Domain concepts represented by raw primitives (string/number).
- **Recognition:** 3+ same-type parameters, or domain ids/amounts kept as `string`/`number`.
- **Severity hint:** LOW.
- **Example:**
  ```typescript
  function createOrder(userId: string, productId: string, price: number, currency: string)
  // vs createOrder(userId: UserId, productId: ProductId, price: Money)
  ```

---

## 2. Object-Orientation Abusers

### OOA-001: Switch Statements (Type Switching)
- **Definition:** `switch`/`if-else` chains keyed on a type discriminator.
- **Recognition:** Same dispatching switch appearing in multiple call sites.
- **Severity hint:** LOW.

### OOA-002: Refused Bequest
- **Definition:** Subclass inherits but ignores or overrides most of the parent.
- **Recognition:** Subclass uses < 30% of inherited surface.
- **Severity hint:** LOW.

### OOA-003: Alternative Classes with Different Interfaces
- **Definition:** Two classes do similar things but expose unlike APIs.
- **Recognition:** Parallel behaviors with differing method names/shapes.
- **Severity hint:** LOW.

### OOA-004: Temporary Field
- **Definition:** Fields only populated in certain code paths.
- **Recognition:** Field is `null`/`undefined` for most of an instance's lifetime.
- **Severity hint:** LOW.

---

## 3. Change Preventers

### CHG-001: Divergent Change
- **Definition:** A single class changes for many unrelated reasons.
- **Recognition:** Commits touching the same class span unrelated feature areas.
- **Severity hint:** MEDIUM.

### CHG-002: Shotgun Surgery
- **Definition:** One conceptual change requires edits across many files.
- **Recognition:** Same modification repeated in 5+ files per change.
- **Severity hint:** MEDIUM.

### CHG-003: Parallel Inheritance Hierarchies
- **Definition:** Adding a subclass to one hierarchy forces a mirror subclass elsewhere.
- **Severity hint:** LOW.

---

## 4. Dispensables (Unnecessary Code)

### DISP-001: Dead Code
- **Definition:** Code that is never executed or reached.
- **Recognition:** Unused functions/variables/imports, commented-out blocks without issue link.
- **Severity hint:** INFO.

### DISP-002: Speculative Generality
- **Definition:** Abstractions added "for future flexibility" with no current consumer.
- **Recognition:** Interfaces with one implementor, unused extension points.
- **Severity hint:** LOW.

### DISP-003: Comments Masking Bad Code
- **Definition:** Comments compensating for unclear naming or structure.
- **Severity hint:** INFO.

### DISP-004: Duplicate Code
- **Definition:** Same or near-same logic in multiple places.
- **Recognition:** Similar block of 3+ LOC repeated in 2+ sites.
- **Severity hint:** LOW.

### DISP-005: Lazy Class
- **Definition:** Class that no longer earns its keep.
- **Severity hint:** INFO.

### DISP-006: Magic Numbers / Strings
- **Definition:** Literal values whose meaning is not self-evident.
- **Recognition:** Numeric/string literals other than `0`, `1`, `-1`, `""` used in logic.
- **Severity hint:** INFO.

### DISP-007: Defensive Excess
- **Definition:** Fallbacks/validation for scenarios that cannot occur.
- **Severity hint:** LOW. (See `zen/reference/defensive-excess.md`.)

---

## 5. Couplers (Excessive Coupling)

### CPL-001: Feature Envy
- **Definition:** Method uses another object's data more than its own.
- **Recognition:** Chains like `a.b.c.d` or many getters from one external object.
- **Severity hint:** LOW.

### CPL-002: Inappropriate Intimacy
- **Definition:** Classes know too much about each other's internals.
- **Recognition:** Access to private members of a "friend", circular references.
- **Severity hint:** MEDIUM.

### CPL-003: Message Chains
- **Definition:** `a.getB().getC().getD()`-style traversal.
- **Severity hint:** LOW.

### CPL-004: Middle Man
- **Definition:** A class whose methods only delegate to another object.
- **Severity hint:** LOW.

---

## 6. Control-Flow Smells

### CTRL-001: Spaghetti Code
- **Definition:** Tangled control flow that is hard to follow.
- **Recognition:** Cyclomatic complexity > 15, nesting depth > 4, or heavy `break`/`continue`/`goto`.
- **Severity hint:** MEDIUM.

---

## 7. Test Code Smells

| ID | Smell | Recognition | Severity hint |
|----|-------|-------------|---------------|
| TST-001 | Duplicated Setup | Same `beforeEach`/setup in > 3 test files | LOW |
| TST-002 | Helper Sprawl | > 10 helpers in one test utility file | LOW |
| TST-003 | Assertion Roulette | > 3 unlabeled assertions in one test | LOW |
| TST-004 | Mystery Guest | Test depends on external file/DB/env without explicit setup | MEDIUM |
| TST-005 | Eager Test | Single test verifies > 5 distinct behaviors | LOW |
| TST-006 | Obscure Test | Test name does not describe behavior | INFO |
| TST-007 | Test Duplication | Same assertion pattern in > 3 test cases | LOW |
| TST-008 | Hard-Coded Data | Magic strings/numbers inside assertions | INFO |
| TST-009 | Conditional Logic in Test | `if`/`else`/`switch` inside a test body | LOW |
| TST-010 | Dead Test | Skipped/commented-out test with no issue link | INFO |

---

## 8. Framework-Specific Hints

These are non-canonical but commonly surface during review.

- **React:** Prop drilling 3+ layers; component LOC > 300; `useEffect` deps drift (escalate as a bug pattern, not a smell).
- **Express / API:** Fat controller (business logic in route handler); inconsistent error handling; over-chained middleware.
- **TypeScript:** Overuse of `any`; over-reliance on `as` assertions; mixed `enum` / union-type style.

---

## Severity Hint Legend

| Severity | Meaning |
|----------|---------|
| MEDIUM | Should be addressed in current change scope; structural risk. |
| LOW | Worth tracking; queue for refactor pass. |
| INFO | Cosmetic / cleanup; bundle with other work. |

Consumers MAY upgrade/downgrade severity based on call-site criticality, blast radius, or repository conventions.
