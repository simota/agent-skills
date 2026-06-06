# Migration Strategies Reference

## Strategy Selection Decision Tree

```
Is the system modular with clear boundaries?
├─ Yes → Can old and new run simultaneously?
│        ├─ Yes → Strangler Fig
│        └─ No → Branch by Abstraction
└─ No
   Is the scope small (<50 files) with high test coverage (>80%)?
   ├─ Yes → Big Bang (with feature flag)
   └─ No
      Is correctness critical (financial, medical)?
      ├─ Yes → Parallel Run
      └─ No → Strangler Fig (create boundaries first)
```

## Strangler Fig Pattern

Replace a system incrementally by routing traffic to new implementations while old code remains operational.

### When to use
- System has identifiable entry points (APIs, routes, event handlers)
- New implementation can coexist with old
- Gradual rollout is acceptable

### Implementation steps
1. **Identify boundary** — find the seam where old and new can coexist
2. **Create facade/proxy** — route requests to either old or new implementation
3. **Build new implementation** — implement one feature/route at a time
4. **Route traffic** — shift traffic gradually via feature flags or routing rules
5. **Verify equivalence** — compare outputs of old and new
6. **Remove old code** — only after new is verified in production

### Routing mechanisms
```typescript
// Feature flag-based routing
function handleRequest(req: Request): Response {
  if (featureFlags.isEnabled('new-auth-service', req.userId)) {
    return newAuthService.handle(req);
  }
  return legacyAuthService.handle(req);
}

// Percentage-based rollout
function routeTraffic(req: Request): Response {
  const percentage = featureFlags.getPercentage('new-payment');
  if (hashUserId(req.userId) % 100 < percentage) {
    return newPaymentService.handle(req);
  }
  return legacyPaymentService.handle(req);
}
```

### Risk mitigation
- Start with lowest-risk, highest-value routes
- Monitor error rates per route during cutover
- Keep rollback instant (flip flag, not redeploy)

## Branch by Abstraction

Introduce an abstraction layer over the code to be replaced, then swap the implementation behind it.

### When to use
- Deeply coupled internal code (shared libraries, utility functions)
- No clear request routing boundary
- Need to maintain single deployable artifact

### Implementation steps
1. **Create abstraction** — interface/adapter over the code to be replaced
2. **Adapt existing code** — make old code implement the new interface
3. **Build new implementation** — implement the interface with new technology
4. **Switch implementation** — swap via dependency injection or config
5. **Remove old code** — after new implementation is verified

### Example
```typescript
// Step 1: Create abstraction
interface UserRepository {
  findById(id: string): Promise<User>;
  save(user: User): Promise<void>;
}

// Step 2: Adapt old code
class LegacyUserRepository implements UserRepository {
  async findById(id: string): Promise<User> {
    return this.legacyORM.query(`SELECT * FROM users WHERE id = ?`, [id]);
  }
}

// Step 3: New implementation
class PrismaUserRepository implements UserRepository {
  async findById(id: string): Promise<User> {
    return this.prisma.user.findUnique({ where: { id } });
  }
}

// Step 4: Switch via DI
const userRepo: UserRepository = config.useNewDB
  ? new PrismaUserRepository(prisma)
  : new LegacyUserRepository(legacyORM);
```

## Parallel Run

Run old and new systems simultaneously, compare outputs, use old for production until confidence is high.

### When to use
- Correctness is critical (financial calculations, compliance)
- Need statistical confidence before cutover
- Can afford the computational overhead of running both

### Implementation steps
1. **Instrument both paths** — run old and new for every request
2. **Compare outputs** — log differences, don't fail on mismatch
3. **Analyze discrepancies** — fix new implementation until match rate > threshold
4. **Cutover primary** — switch new to primary, old to shadow
5. **Remove shadow** — after confidence period

### Comparison framework
```typescript
async function parallelRun<T>(
  label: string,
  control: () => Promise<T>,
  candidate: () => Promise<T>,
  compare: (a: T, b: T) => boolean
): Promise<T> {
  const controlResult = await control();

  // Run candidate async, don't block
  candidate().then(candidateResult => {
    const match = compare(controlResult, candidateResult);
    metrics.record('parallel_run', {
      label,
      match,
      control: controlResult,
      candidate: candidateResult,
    });
  }).catch(err => {
    metrics.record('parallel_run_error', { label, error: err.message });
  });

  return controlResult; // Always return control (old) result
}
```

## Big Bang Migration

Replace everything at once. Use only when scope is small and well-understood.

### When to use
- Scope < 50 files
- Test coverage > 80%
- No external API consumers
- Team can dedicate a sprint to the migration

### Risk mitigation
- Feature flag the entire migration behind a single toggle
- Run full test suite against both branches
- Prepare rollback script that reverts in < 5 minutes
- Schedule during low-traffic window

## Risk Assessment Matrix

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Data loss during migration | Low | Critical | Backup before each phase, verify row counts |
| Breaking API consumers | Medium | High | Versioned endpoints, deprecation notices, adapter layer |
| Performance regression | Medium | Medium | Benchmark before/after, set performance budgets |
| Feature parity gap | High | Medium | Checklist per feature, automated comparison tests |
| Rollback failure | Low | Critical | Test rollback procedure before production migration |
| Extended migration stall | Medium | High | Time-box each phase, define go/no-go criteria |

## Migration Plan Template

```markdown
# Migration Plan: [From] → [To]

## 1. Scope
- **Files affected:** [count]
- **Modules affected:** [list]
- **External consumers:** [count and names]
- **Test coverage:** [percentage]

## 2. Strategy
- **Pattern:** [Strangler Fig | Branch by Abstraction | Parallel Run | Big Bang]
- **Rationale:** [why this strategy]

## 3. Phases
| Phase | Scope | Duration | Rollback | Go/No-Go |
|-------|-------|----------|----------|----------|
| 1 | [description] | [estimate] | [mechanism] | [criteria] |
| 2 | [description] | [estimate] | [mechanism] | [criteria] |

## 4. Risk Matrix
| Risk | L | I | Score | Mitigation |
|------|---|---|-------|-----------|

## 5. Verification
- [ ] Before-snapshot tests created
- [ ] After-migration regression suite
- [ ] Performance benchmarks captured
- [ ] Behavioral equivalence verified
- [ ] Rollback tested

## 6. Rollback Plan
- **Trigger:** [when to rollback]
- **Procedure:** [step-by-step]
- **Estimated time:** [duration]
- **Data reversion:** [if applicable]
```

## Monolith Decomposition Guide

### Domain-Driven Boundary Detection
1. Identify bounded contexts via data ownership analysis
2. Map inter-module communication (sync calls, shared DB tables, events)
3. Score coupling: Low (events only) → Medium (API calls) → High (shared state)
4. Prioritize extraction: start with lowest-coupling, highest-value domains

### Extraction Sequence
1. Extract shared data → service with API
2. Add anti-corruption layer at monolith boundary
3. Dual-write during transition (old DB + new service)
4. Verify data consistency
5. Cut over reads to new service
6. Cut over writes to new service
7. Remove monolith code + old DB tables
