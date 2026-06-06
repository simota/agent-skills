# Software Quality Standards Reference

## ISO/IEC 25010:2023 — Product Quality Model (supersedes 2011)

[Source: https://www.iso.org/standard/78176.html]

The 2023 revision expands from 8 to **9 characteristics** and renames several top-level items. **Do not assess against the 2011 model** — its 8-characteristic structure (Portability, Usability) is superseded.

**Key changes from 2011:** Usability → **Interaction Capability** (adds Inclusivity, Self-descriptiveness); Portability → **Flexibility** (adds Scalability); **Safety** added as 9th characteristic; Reliability/Maturity → Faultlessness; User Interface Aesthetics → User Engagement; Security adds **Resistance** sub-characteristic.

### Quality Characteristics (2023 — 9 characteristics)

| Characteristic | Definition | Sub-characteristics (2023) |
|----------------|------------|---------------------------|
| **Functional Suitability** | Meets stated and implied needs | Completeness, Correctness, Appropriateness |
| **Performance Efficiency** | Performance relative to resources | Time behavior, Resource utilization, Capacity |
| **Compatibility** | Works with other systems | Co-existence, Interoperability |
| **Interaction Capability** | Can be used effectively (was: Usability) | Appropriateness recognizability, Learnability, Operability, User error protection, User engagement, Inclusivity, User assistance, Self-descriptiveness, Accessibility |
| **Reliability** | Performs under conditions | Faultlessness, Availability, Fault tolerance, Recoverability |
| **Security** | Protects information | Confidentiality, Integrity, Non-repudiation, Accountability, Authenticity, **Resistance** |
| **Maintainability** | Can be modified effectively | Modularity, Reusability, Analysability, Modifiability, Testability |
| **Flexibility** | Can be transferred/adapted (was: Portability) | Adaptability, **Scalability**, Installability, Replaceability |
| **Safety** | Avoids unacceptable risk (new in 2023) | Operational constraint, Risk identification, Fail safe, Hazard warning, Safe integration |

### ISO/IEC 25019:2023 — Quality-in-Use Model

[Source: https://www.iso.org/standard/78177.html]

Companion standard published November 2023 (Edition 1). Defines the Quality-in-Use model covering three characteristics: Effectiveness, Efficiency, Satisfaction (with sub-characteristics Context coverage and Flexibility-in-use). Use ISO 25019 when assessing from the end-user / operational perspective; use ISO 25010 for intrinsic product quality. Both are part of the SQuaRE family.

### Quality Metrics

#### Functional Suitability
| Metric | Formula | Target |
|--------|---------|--------|
| Functional completeness | Implemented / Required functions | ≥ 100% |
| Functional correctness | Correct outputs / Total outputs | ≥ 99% |
| Functional appropriateness | Used functions / Provided functions | ≥ 80% |

#### Performance Efficiency
| Metric | Formula | Target |
|--------|---------|--------|
| Response time | Measured time for operation | Depends on SLA |
| Throughput | Requests processed / Time unit | Depends on requirements |
| Resource utilization | Resources used / Available resources | < 80% |

#### Reliability
| Metric | Formula | Target |
|--------|---------|--------|
| MTBF | Total uptime / Number of failures | Depends on criticality |
| Availability | Uptime / (Uptime + Downtime) | ≥ 99.9% (three nines) |
| Fault density | Faults / Size (KLOC) | < 1 per KLOC |

#### Maintainability
| Metric | Formula | Target |
|--------|---------|--------|
| Cyclomatic complexity | Decision points + 1 | ≤ 10 per function |
| Coupling | Dependencies between modules | Low |
| Cohesion | Related functions in module | High |
| Code duplication | Duplicated lines / Total lines | < 5% |

#### Security
| Metric | Formula | Target |
|--------|---------|--------|
| Vulnerability density | Vulnerabilities / KLOC | 0 for critical/high |
| Security test coverage | Security tests / Security requirements | ≥ 100% |
| Time to patch | Discovery to deployment | < 24h critical |

### Quality Assessment Template

```markdown
## ISO 25010 Quality Assessment: [System Name]

### Assessment Date: YYYY-MM-DD
### Scope: [What was assessed]

### Quality Scores

| Characteristic | Weight | Score (1-5) | Weighted Score |
|----------------|--------|-------------|----------------|
| Functional Suitability | 15% | | |
| Performance Efficiency | 15% | | |
| Compatibility | 10% | | |
| Usability | 15% | | |
| Reliability | 15% | | |
| Security | 15% | | |
...
```

---

## Clean Code Principles

### Naming Standards

#### Variables and Functions
| Rule | Bad | Good |
|------|-----|------|
| Use intention-revealing names | `d` | `elapsedDays` |
| Avoid disinformation | `accountList` (if not List) | `accounts` or `accountList` (if List) |
| Make meaningful distinctions | `a1`, `a2` | `source`, `destination` |
| Use pronounceable names | `genymdhms` | `generationTimestamp` |
| Use searchable names | `7` | `MAX_RETRY_COUNT = 7` |

#### Classes
| Rule | Bad | Good |
|------|-----|------|
| Noun or noun phrase | `ProcessData` | `DataProcessor` |
| Avoid generic names | `Manager`, `Processor`, `Data` | `PaymentGateway`, `OrderValidator` |
| Single responsibility | `UserManagerAndValidator` | `UserManager`, `UserValidator` |

#### Functions
| Rule | Bad | Good |
|------|-----|------|
| Verb or verb phrase | `password` | `validatePassword` |
| Small and focused | 100+ lines | < 20 lines |
| One level of abstraction | Mixed levels | Single level |
| Minimal arguments | 5+ arguments | 0-3 arguments |

### Function Rules

#### Size
```javascript
// BAD: Too long, multiple responsibilities
function processOrder(order) {
  // 100+ lines of validation, calculation, database, email...
}

// GOOD: Small, single responsibility
function processOrder(order) {
  validateOrder(order);
  const total = calculateTotal(order);
  await saveOrder(order, total);
  await sendConfirmation(order);
}
```

#### Arguments
```typescript
// BAD: Too many arguments
function createUser(name, email, age, address, phone, status) {...}

// GOOD: Use object parameter
function createUser(params: CreateUserParams) {...}

interface CreateUserParams {
  name: string;
  email: string;
  age?: number;
  address?: Address;
  phone?: string;
  status?: UserStatus;
}
```

#### Side Effects
```typescript
// BAD: Hidden side effect
function checkPassword(password: string): boolean {
  const valid = validate(password);
  if (valid) {
    Session.initialize(); // Hidden side effect!
  }
  return valid;
}

// GOOD: No side effects, or clearly named
function validatePassword(password: string): boolean {
  return validate(password);
}

function validatePasswordAndInitSession(password: string): boolean {
// ...
```

### Comments Standards

#### Good Comments
```typescript
// Explains WHY (not what)
// We use setTimeout instead of requestAnimationFrame because
// this needs to run even when the tab is hidden
setTimeout(updatePosition, 16);

// Warns of consequences
// WARNING: Running this on production will delete all user data
async function resetDatabase() {...}

// Legal/copyright
// Copyright (c) 2024 Company Name. MIT License.

// TODO for known issues
// TODO(user): Refactor when TypeScript supports decorators
```

#### Bad Comments
```typescript
// BAD: Redundant comment
// Increment i by 1
i++;

// BAD: Noise comment
// Default constructor
constructor() {}

// BAD: Commented out code
// function oldImplementation() {
//   return x + y;
// }

// BAD: Journal comment
// 2024-01-15: Added by John
// ...
```

### Error Handling

#### Exceptions over Error Codes
```typescript
// BAD: Error codes
function divide(a: number, b: number): { result?: number; error?: string } {
  if (b === 0) return { error: 'Division by zero' };
  return { result: a / b };
}

// GOOD: Exceptions
function divide(a: number, b: number): number {
  if (b === 0) throw new DivisionByZeroError();
  return a / b;
}
```

#### Specific Exceptions
```typescript
// BAD: Generic exception
throw new Error('Something went wrong');

// GOOD: Specific exception
throw new InvalidInputError('Email format is invalid', { field: 'email' });
throw new ResourceNotFoundError('User', userId);
throw new AuthenticationError('Invalid credentials');
```

#### Don't Return Null
```typescript
// BAD: Returns null
function findUser(id: string): User | null {
  return users.get(id) || null;
}

// GOOD: Use Optional/Maybe or throw
function findUser(id: string): User {
  const user = users.get(id);
  if (!user) throw new UserNotFoundError(id);
  return user;
}

// GOOD: Use Option type
function findUser(id: string): Option<User> {
  return Option.fromNullable(users.get(id));
// ...
```

---

## SOLID Principles

### S - Single Responsibility Principle

**Definition:** A class should have only one reason to change.

```typescript
// BAD: Multiple responsibilities
class UserService {
  createUser(data: UserData) {...}
  validateEmail(email: string) {...}
  sendWelcomeEmail(user: User) {...}
  generateReport(userId: string) {...}
  hashPassword(password: string) {...}
}

// GOOD: Single responsibility each
class UserService {
  constructor(
    private validator: UserValidator,
    private notifier: UserNotifier,
    private repository: UserRepository
// ...
```

### O - Open/Closed Principle

**Definition:** Open for extension, closed for modification.

```typescript
// BAD: Requires modification to add new type
class PaymentProcessor {
  process(payment: Payment) {
    if (payment.type === 'credit') {
      // process credit
    } else if (payment.type === 'paypal') {
      // process paypal
    } else if (payment.type === 'crypto') {
      // process crypto - NEW CODE ADDED
    }
  }
}

// GOOD: Open for extension
interface PaymentHandler {
// ...
```

### L - Liskov Substitution Principle

**Definition:** Subtypes must be substitutable for their base types.

```typescript
// BAD: Violates LSP
class Rectangle {
  setWidth(width: number) { this.width = width; }
  setHeight(height: number) { this.height = height; }
  area() { return this.width * this.height; }
}

class Square extends Rectangle {
  setWidth(width: number) {
    this.width = width;
    this.height = width; // Unexpected behavior!
  }
}

// GOOD: Separate types
// ...
```

### I - Interface Segregation Principle

**Definition:** Clients shouldn't depend on interfaces they don't use.

```typescript
// BAD: Fat interface
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
}

class Robot implements Worker {
  work() { /* OK */ }
  eat() { throw new Error('Robots do not eat'); } // Violation!
  sleep() { throw new Error('Robots do not sleep'); } // Violation!
}

// GOOD: Segregated interfaces
interface Workable {
// ...
```

### D - Dependency Inversion Principle

**Definition:** Depend on abstractions, not concretions.

```typescript
// BAD: Depends on concrete class
class OrderService {
  private database = new MySQLDatabase();

  save(order: Order) {
    this.database.query('INSERT INTO orders...');
  }
}

// GOOD: Depends on abstraction
interface OrderRepository {
  save(order: Order): Promise<void>;
}

class OrderService {
// ...
```

---

## 12-Factor App

### The 12 Factors

| Factor | Principle | Compliance Check |
|--------|-----------|------------------|
| 1. Codebase | One codebase tracked in version control | Single repo, many deploys |
| 2. Dependencies | Explicitly declare and isolate | package.json/requirements.txt |
| 3. Config | Store config in environment | No hardcoded config |
| 4. Backing Services | Treat as attached resources | Connection via URL/credentials |
| 5. Build, Release, Run | Strictly separate stages | CI/CD pipeline |
| 6. Processes | Execute app as stateless processes | No local state |
| 7. Port Binding | Export services via port binding | Self-contained HTTP server |
| 8. Concurrency | Scale out via process model | Horizontal scaling |
| 9. Disposability | Fast startup and graceful shutdown | Quick boot, SIGTERM handling |
| 10. Dev/Prod Parity | Keep environments similar | Same services, tools |
| 11. Logs | Treat logs as event streams | stdout/stderr, not files |
| 12. Admin Processes | Run admin tasks as one-off processes | Same codebase, separate run |

### Compliance Checklist

#### Factor 1: Codebase
- [ ] Single repository per application
- [ ] Multiple deploys from same codebase
- [ ] No code sharing via copy-paste (use packages)

#### Factor 2: Dependencies
- [ ] All dependencies explicitly declared
- [ ] No reliance on system-wide packages
- [ ] Dependency isolation (node_modules, venv)
- [ ] Lock file committed (package-lock.json, yarn.lock)

#### Factor 3: Config
- [ ] No hardcoded configuration values
- [ ] Configuration via environment variables
- [ ] Sensitive data not in codebase
- [ ] Config validation at startup

```typescript
// BAD
const DATABASE_URL = 'postgres://localhost:5432/db';

// GOOD
const DATABASE_URL = process.env.DATABASE_URL;
if (!DATABASE_URL) throw new Error('DATABASE_URL required');
```

#### Factor 4: Backing Services
- [ ] Database, cache, queue as attached resources
- [ ] Connection via environment URL
- [ ] No distinction between local and third-party services
- [ ] Can swap services without code changes

#### Factor 5: Build, Release, Run
- [ ] Separate build stage (compile, bundle)
- [ ] Separate release stage (build + config)
- [ ] Separate run stage (execute processes)
- [ ] Immutable releases

#### Factor 6: Processes
- [ ] Stateless processes
- [ ] No sticky sessions
- [ ] State in backing services (database, cache)
- [ ] File uploads to object storage

```typescript
// BAD: Local state
const sessions = new Map(); // Lost on restart/scale

// GOOD: External state
const sessions = new RedisSessionStore();
```

#### Factor 7: Port Binding
- [ ] Self-contained web server
- [ ] Export HTTP via port binding
- [ ] No external web server dependency

```typescript
// App binds to port
const port = process.env.PORT || 3000;
app.listen(port);
```

#### Factor 8: Concurrency
- [ ] Horizontal scaling capability
- [ ] Process types defined (web, worker, scheduler)
- [ ] No shared memory between processes
- [ ] Workload distribution via process manager

#### Factor 9: Disposability
- [ ] Fast startup time (seconds, not minutes)
- [ ] Graceful shutdown on SIGTERM
- [ ] Crash-only design (safe restart)
- [ ] Idempotent operations

```typescript
// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('Shutting down...');
  await server.close();
  await database.disconnect();
  process.exit(0);
});
```

#### Factor 10: Dev/Prod Parity
- [ ] Same backing services in dev and prod
- [ ] Same deployment process
- [ ] Minimize time gap (CI/CD)
- [ ] Minimize personnel gap (developers deploy)

#### Factor 11: Logs
- [ ] Logs to stdout/stderr
- [ ] No file writing in application
- [ ] Structured logging (JSON)
- [ ] Log aggregation external to app

```typescript
// BAD
fs.appendFileSync('app.log', message);

// GOOD
console.log(JSON.stringify({ level: 'info', message, timestamp: new Date() }));
```

#### Factor 12: Admin Processes
- [ ] Admin tasks run in identical environment
- [ ] Same codebase and config
- [ ] Run as one-off processes
- [ ] REPL available for inspection

---

## Code Metrics Standards

### Complexity Metrics

| Metric | Target | Tool |
|--------|--------|------|
| Cyclomatic Complexity | ≤ 10 per function | ESLint, SonarQube |
| Cognitive Complexity | ≤ 15 per function | SonarQube |
| Nesting Depth | ≤ 4 levels | ESLint |
| Function Length | ≤ 50 lines | ESLint |
| File Length | ≤ 500 lines | Custom |
| Parameters | ≤ 4 per function | ESLint |

### ESLint Rules

```json
{
  "rules": {
    "complexity": ["error", 10],
    "max-depth": ["error", 4],
    "max-lines": ["error", 500],
    "max-lines-per-function": ["error", 50],
    "max-params": ["error", 4],
    "max-nested-callbacks": ["error", 3]
  }
}
```

### SonarQube Quality Gates

| Metric | Threshold |
|--------|-----------|
| Coverage | ≥ 80% |
| Duplicated Lines | < 3% |
| Maintainability Rating | A |
| Reliability Rating | A |
| Security Rating | A |
| Blocker Issues | 0 |
| Critical Issues | 0 |

---

## Testing Standards

### Test Pyramid

```
         /\
        /  \     E2E Tests (few)
       /----\
      /      \   Integration Tests (some)
     /--------\
    /          \ Unit Tests (many)
   /------------\
```

### Coverage Guidelines

| Type | Minimum | Target |
|------|---------|--------|
| Line Coverage | 70% | 80%+ |
| Branch Coverage | 60% | 70%+ |
| Function Coverage | 80% | 90%+ |
| Critical Paths | 100% | 100% |

### Test Naming Convention

```typescript
// Pattern: describe > context > expected behavior
describe('UserService', () => {
  describe('createUser', () => {
    it('should create a user with valid data', async () => {...});
    it('should throw ValidationError when email is invalid', async () => {...});
    it('should throw ConflictError when email already exists', async () => {...});
  });
});
```

### Test Quality Checklist

- [ ] Tests are independent (no order dependency)
- [ ] Tests are repeatable (no flakiness)
- [ ] Tests are self-validating (pass/fail clear)
- [ ] Tests are timely (written with code)
- [ ] Tests cover edge cases
- [ ] Tests have single assertion focus
- [ ] Tests use meaningful names
- [ ] Tests mock external dependencies
