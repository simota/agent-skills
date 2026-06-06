# Process Guide, Examples & Decision Templates

> Builder's working process, Forge conversion, TDD templates, anti-pattern examples, and decision-point question templates

---

## 1. Ambiguity Detection & Resolution

Trigger `ON_AMBIGUOUS_SPEC` (§7) if any apply:

| Check Item | Ambiguous Example | Clarification Needed |
|------------|-------------------|---------------------|
| "appropriately", "as needed" | "Display appropriate error message" | Specific message content |
| Undefined numeric range | "Large amount of data" | Specific count (100? 100,000?) |
| Undefined edge cases | "Delete user" | How to handle related data? |
| Undefined error behavior | "Call API" | Timeout, retry strategy? |
| Multiple interpretations | "Latest data" | Created date? Updated date? |

---

## 2. Forge → Builder Conversion

### Spec Analysis Template

```markdown
### Clear Requirements
- [ ] Requirement 1: [Specific content]

### Inferred Requirements (Confirmation Recommended)
- [ ] Inference 1: [Content] → Rationale: [Why inferred]

### Undefined Requirements (Confirmation Required)
- [ ] Unknown 1: [Content] → Impact: [Implementation impact]
```

### Forge Handoff Parser

```yaml
FORGE_HANDOFF_PARSER:
  inputs:
    - components/prototypes/*.tsx    # UI implementation
    - types.ts                       # Type definitions
    - mocks/handlers.ts              # API mocks
    - .agents/forge-insights.md      # Domain knowledge
  outputs:
    value_objects:   # Extract VO candidates from mock data
    entities:        # Extract Entity candidates from data with IDs
    api_endpoints:   # Extract API list from MSW handlers
    error_cases:     # Extract DomainError list from error mocks
```

### Conversion Patterns with Code

```typescript
// Mock Data → Value Object
class Email extends ValueObject<{ value: string }> {
  private static readonly PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  static create(email: string): Result<Email, ValidationError> {
    if (!this.PATTERN.test(email)) return err(new ValidationError('Invalid email format'));
    return ok(new Email(email.toLowerCase().trim()));
  }
}

// MSW Handler → API Client
class UserApiClient extends ApiClient {
  async getUser(id: UserId): Promise<Result<User, ApiError>> {
    return this.request<UserDto>({ method: 'GET', url: `/api/users/${id.value}` })
      .then(result => result.map(UserMapper.toDomain));
  }
}

// Error Mock → DomainError
class EmailRequiredError extends DomainError {
  constructor() { super('EMAIL_REQUIRED', 'Email is required'); }
}
```

---

## 3. TDD Templates

### Test Design Document

```markdown
### Happy Path
| Given | When | Then |
|-------|------|------|
| Valid user data | Call create() | User entity is generated |

### Edge Cases
| Case | Input | Expected Result |
|------|-------|-----------------|
| Empty email | `{ email: '' }` | ValidationError |

### Boundary Values
| Item | Minimum | Maximum | Boundary Tests |
|------|---------|---------|----------------|
| Name length | 1 char | 100 chars | 0, 1, 100, 101 |

### Error Recovery
| Error | Recovery | Verification Method |
|-------|----------|---------------------|
| API timeout | 3 retries | Inject delay with mock |
```

### Test Skeleton (AAA Pattern)

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid data', async () => {
      // Arrange: Valid user data
      // Act: Call createUser()
      // Assert: User entity is returned
    });
    it('should return ValidationError for empty email', async () => {
      // TODO: Radar implements
    });
    // Boundary values: Radar extends with it.each for min/max
  });
});
```

---

## 4. Code Standards

### Naming Conventions
- Value Objects: noun (`Email`, `UserId`, `Money`)
- Entities: noun with identity (`User`, `Order`)
- Services: noun + Service (`AuthService`, `CartService`)
- Error classes: description + Error (`InvalidCredentialsError`)

### Error Handling Patterns
- Use `Result<T, E>` for expected failures (validation, not found)
- Use `throw` for unexpected failures (invariant violations, programmer errors)
- Never swallow errors — log + rethrow or handle explicitly

### Logging Standards
- Log with context: `logger.error('Failed to save', { payload, error: e })`
- Never log secrets, tokens, passwords, or personal data

### AI-Generated Code Quality Checks
- Run linter/type-checker after each generation step
- Self-critique: review generated code in fresh context
- No new `any` types without justification comment
- Function length ≤ 20 lines; extract if longer
- No dead code or unused imports
- Prefer composition over inheritance
- YAGNI: don't generate abstract base classes unless 3+ concrete implementations exist

---

## 5. Seven Deadly Sins

> Every sin here has burned a production system.

### 1. Magic Numbers
```typescript
// ❌  if (items.length > 100) { paginate(items); }
// ✅
const PAGINATION_THRESHOLD = 100; // UX研究: 100件超で描画が遅延
if (items.length > PAGINATION_THRESHOLD) { paginate(items); }
```

### 2. God Function
```typescript
// ❌  200+ line function — untestable, unmaintainable
// ✅  Split into pure functions ≤ 20 lines each
function validateInput(data: DataPayload): Result<ValidData, ValidationError> { ... }
function processCore(data: ValidData): ProcessedResult { ... }
```

### 3. Swallowed Errors
```typescript
// ❌
try { await saveData(payload); } catch (e) { /* silence */ }
// ✅
try { await saveData(payload); } catch (e) {
  logger.error('Failed to save data', { payload, error: e });
  throw new DataPersistenceError('Save failed', { cause: e });
}
```

### 4. Direct DB in Handler / Leaky Abstraction
```typescript
// ❌  fetch('/api/users') directly inside a React component
// ✅
function useUsers() { return useQuery(['users'], () => userService.getAll()); }
function UserList() { const { data } = useUsers(); ... }
```

### 5. Missing Input Validation / Happy Path Trap
```typescript
// ❌
async function loadUser(id: string) { return (await api.getUser(id)).profile.displayName; }
// ✅
async function loadUser(id: string): Promise<Result<string, UserError>> {
  const result = await api.getUser(id);
  if (result.isErr()) return err(new UserNotFoundError(id));
  return ok(result.value.profile?.displayName ?? 'Anonymous');
}
```

### 6. Hardcoded Config / `any` Abuse
```typescript
// ❌
function processData(data: any) { return data.items.map(item => item.value); }
// ✅
interface DataPayload { items: Array<{ value: number }>; }
function processData(data: DataPayload) { return data.items.map(item => item.value); }
```

### 7. Async Void
```typescript
// ❌  load(); // Promise ignored inside useEffect
// ✅
useEffect(() => {
  let cancelled = false;
  fetchData()
    .then(data => { if (!cancelled) setData(data); })
    .catch(err => { if (!cancelled) setError(err); });
  return () => { cancelled = true; };
}, []);
```

---

## 6. Warning Signs

### General Signals

| Warning Sign | What It Means | Action |
|--------------|---------------|--------|
| Copy-pasting error handler 3+ times | Missing abstraction | Extract to utility/middleware |
| Function approaching 100 lines | God function forming | Split into pure functions |
| Reaching for `any` | Types are fighting you | Redesign interface, use generics |
| "This is hard to test" | Coupling is too tight | Inject dependencies, use interfaces |
| Adding a flag parameter | Function doing two things | Split into two functions |
| "I'll fix this later" | Technical debt incoming | Fix now or create tracked TODO |

### AI-Specific Warning Signs

| Warning Sign | Root Cause | Action |
|--------------|------------|--------|
| Abstraction bloat: 1000 lines for a 100-line problem | Over-engineering | Strip to MVP; add complexity only when needed |
| Assumption propagation: first misunderstanding spreads to all layers | Unchecked premise | Re-read spec; invalidate downstream before continuing |
| Dead code accumulation: unused implementations left behind | Incomplete refactor | Delete before committing |
| Wrong language idiom: Java-style OOP in Go code | Model habit leak | Audit against project conventions |

### Stop and Ask Moments

If encountered, invoke the relevant template from §7:
1. Two reasonable approaches with different trade-offs
2. Hard-to-reverse decisions (DB schema, public API shape)
3. Performance vs readability conflict — measure first
4. Security-sensitive code — invoke Sentinel review

---

## 7. Decision-Point Question Templates

### ON_AMBIGUOUS_SPEC
```yaml
questions:
  - question: "There are ambiguities in the specification. How should they be interpreted?"
    header: "Specification"
    options:
      - label: "Option A: [Specific interpretation] (Recommended)"
        description: "[Rationale and impact]"
      - label: "Option B: [Alternative interpretation]"
        description: "[Rationale and impact]"
      - label: "Support both"
        description: "Make it switchable via configuration or flag"
      - label: "Clarify specification before implementation"
        description: "Pause and confirm detailed specification"
    multiSelect: false
```

### ON_PERFORMANCE_DECISION
```yaml
questions:
  - question: "There are design decisions affecting performance. How should we proceed?"
    header: "Performance"
    options:
      - label: "Implement optimization upfront (Recommended)"
        description: "Build in N+1 prevention, indexes, caching from the start"
      - label: "Simple implementation + optimize later"
        description: "Make it work first, improve after confirming bottlenecks"
      - label: "Request analysis from Tuner"
        description: "Delegate optimization to DB performance specialist agent"
    multiSelect: false
```

### ON_DB_MIGRATION
```yaml
questions:
  - question: "Introduce a new database migration?"
    header: "DB Migration"
    options:
      - label: "Review migration plan (Recommended)"
        description: "Confirm changes and rollback procedures"
      - label: "Execute as-is"
        description: "Apply migration directly"
      - label: "Defer this change"
        description: "Skip schema change and consider alternative approach"
    multiSelect: false
```

### ON_CORE_REFACTORING
```yaml
questions:
  - question: "Refactor a core utility used by the entire app?"
    header: "Core Change"
    options:
      - label: "Analyze impact first (Recommended)"
        description: "List all dependent locations for review"
      - label: "Refactor incrementally"
        description: "Split small changes across multiple PRs"
      - label: "Maintain current state"
        description: "Skip core utility changes"
    multiSelect: false
```

### ON_PATTERN_CHOICE
```yaml
questions:
  - question: "Which DDD pattern should be applied?"
    header: "DDD Pattern"
    options:
      - label: "Entity (Recommended)"
        description: "Persistent object identified by ID"
      - label: "Value Object"
        description: "Immutable object compared by value"
      - label: "Aggregate Root"
        description: "Boundary grouping related entities"
      - label: "Domain Service"
        description: "Logic not belonging to a single entity"
    multiSelect: false
```

---

## 8. Case Studies

### Case Study 1: Forge → Builder Handoff (User Authentication)

**Scenario**: Forge delivered a working login prototype with MSW mocks. Builder transforms it into production-ready authentication.

```
BLUEPRINT: Value Objects (Email, Password, SessionToken), Entity (User),
           error types (InvalidCredentials, AccountLocked, RateLimited)
FORGE:     Email VO with validation, AuthService with error handling,
           httpOnly cookie token storage, rate limiting awareness
TEMPER:    Handle 401/403/429, retry with exponential backoff for 5xx
```

```typescript
// Forge mock type
interface LoginResponse { token: string; user: any; }  // 🔴 any!

// Builder production type
interface AuthResult {
  sessionToken: SessionToken;  // Value Object
  user: AuthenticatedUser;     // Entity
  expiresAt: Date;
}
type LoginError = InvalidCredentialsError | AccountLockedError | RateLimitedError;
```

### Case Study 2: Scout → Builder Handoff (Race Condition Fix)

**Scenario**: Scout found a race condition in cart quantity updates. Fast clicks caused non-deterministic inventory state.

**Root Cause**: `updateQuantity()` fired API calls without waiting; response order determined final state.

**Builder's Solution**: Optimistic locking with abort-on-new-request.

```typescript
// Before
async function updateQuantity(itemId: string, quantity: number) {
  await api.patch(`/cart/${itemId}`, { quantity });
}

// After
class CartService {
  private pendingUpdates = new Map<string, AbortController>();

  async updateQuantity(
    itemId: CartItemId, quantity: Quantity, version: number
  ): Promise<Result<CartItem, CartError>> {
    this.pendingUpdates.get(itemId.value)?.abort();
    const controller = new AbortController();
    this.pendingUpdates.set(itemId.value, controller);
    // ... optimistic lock implementation with version check
  }
}
```
