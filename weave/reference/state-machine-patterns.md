# State Machine Patterns

**Purpose:** Pattern catalog and best practices for state machine design.
**Read when:** Designing an FSM, Statechart, or XState machine.

---

## FSM vs Statechart vs XState

> XState v5 source: [stately.ai/docs/actors](https://stately.ai/docs/actors), [stately.ai/docs/machines](https://stately.ai/docs/machines)

| Aspect | FSM | Statechart (Harel) | XState v5 |
|--------|-----|--------------------|----|
| Hierarchy | Flat | Nested (compound states) | Nested |
| Parallelism | None | Orthogonal regions | Parallel states |
| Guards | Manual | Built-in | Built-in (typed via `setup()`) |
| Actions | Manual | Entry/Exit/Transition | Entry/Exit/Transition + Invoke |
| History | None | Shallow/Deep | Shallow/Deep |
| Concurrency | None | Orthogonal regions | Actor model (spawn / `systemId`) |
| Input | None | None | `createActor(machine, { input })` |
| Persistence | None | None | Deep (recursive) actor snapshot |
| Use case | Simple toggle/enum | Complex business logic | UI + Business logic + Actor systems |

### XState v5 Key API Changes (v4 → v5)

| v4 (removed) | v5 replacement |
|---|---|
| `createMachine()` (standalone) | `setup({}).createMachine()` |
| `interpret(machine)` | `createActor(machine)` |
| `service.start()` | `actor.start()` |
| No input support | `createActor(machine, { input })` |
| Shallow actor persistence | Deep (recursive) actor persistence |

> **Migration note:** XState v4 APIs are removed in v5. Always use `setup()` + `createActor()` for new designs.

---

## State Design Principles

### 1. States are Nouns/Adjectives

```yaml
# Good
states: [idle, loading, loaded, error, cancelled]

# Bad - verbs describe events, not states
states: [load, cancel, submit, retry]
```

### 2. Events are Past Tense or Commands

```yaml
# Good
events: [SUBMIT, CANCEL, FETCH_SUCCESS, FETCH_FAILURE, TIMEOUT]

# Bad - ambiguous
events: [data, click, done]
```

### 3. Guard Conditions are Predicates

```yaml
guards:
  isAuthorized: "user.role === 'admin'"
  hasBalance: "account.balance >= amount"
  isRetryable: "retryCount < maxRetries"
```

---

## Common Patterns

### Pattern 1: Request/Response with Retry

```yaml
STATE_MACHINE:
  name: FetchWithRetry
  initial: idle
  context:
    retryCount: 0
    maxRetries: 3
  states:
    idle:
      on:
        FETCH:
          target: loading
          actions: [resetRetry]
    loading:
      invoke:
        src: fetchService
        onDone: { target: success }
        onError:
          - target: retrying
            guard: canRetry
          - target: failure
      on:
        CANCEL: { target: cancelled }
    retrying:
      entry: [incrementRetry, exponentialBackoff]
      after:
        BACKOFF_DELAY: { target: loading }
    success:
      type: final
    failure:
      on:
        RETRY: { target: loading, actions: [resetRetry] }
    cancelled:
      type: final
```

### Pattern 2: Multi-Step Form Wizard

```yaml
STATE_MACHINE:
  name: FormWizard
  initial: step1
  states:
    step1:
      on:
        NEXT:
          target: step2
          guard: step1Valid
        SAVE_DRAFT: { actions: [saveDraft] }
    step2:
      on:
        NEXT:
          target: step3
          guard: step2Valid
        BACK: { target: step1 }
    step3:
      on:
        SUBMIT:
          target: submitting
          guard: step3Valid
        BACK: { target: step2 }
    submitting:
      invoke:
        src: submitForm
        onDone: { target: complete }
        onError: { target: step3, actions: [showError] }
    complete:
      type: final
```

### Pattern 3: Hierarchical State (Compound)

```yaml
STATE_MACHINE:
  name: OrderLifecycle
  initial: draft
  states:
    draft:
      on:
        SUBMIT: { target: "processing.validating" }
    processing:
      initial: validating
      states:
        validating:
          invoke:
            src: validateOrder
            onDone: { target: authorized }
            onError: { target: "#draft", actions: [showValidationError] }
        authorized:
          on:
            PAY: { target: paying }
        paying:
          invoke:
            src: processPayment
            onDone: { target: paid }
            onError: { target: authorized, actions: [showPaymentError] }
        paid:
          type: final
      onDone: { target: fulfillment }
    fulfillment:
      initial: preparing
      states:
        preparing:
          on:
            SHIP: { target: shipped }
        shipped:
          on:
            DELIVER: { target: delivered }
        delivered:
          type: final
      onDone: { target: completed }
    completed:
      type: final
```

### Pattern 4: Parallel States

```yaml
STATE_MACHINE:
  name: DocumentEditor
  type: parallel
  states:
    editing:
      initial: idle
      states:
        idle:
          on:
            EDIT: { target: modified }
        modified:
          on:
            SAVE: { target: idle, actions: [saveDocument] }
    autosave:
      initial: waiting
      states:
        waiting:
          after:
            30000: { target: saving }
        saving:
          invoke:
            src: autoSave
            onDone: { target: waiting }
            onError: { target: waiting }
    collaboration:
      initial: synced
      states:
        synced:
          on:
            REMOTE_CHANGE: { target: merging }
        merging:
          invoke:
            src: mergeChanges
            onDone: { target: synced }
            onError: { target: conflicted }
        conflicted:
          on:
            RESOLVE: { target: synced }
```

---

## Validation Algorithm

### Reachability Check (BFS)

```
function checkReachability(stateMachine):
  visited = {initial}
  queue = [initial]
  while queue not empty:
    state = queue.dequeue()
    for each transition from state:
      if transition.target not in visited:
        visited.add(transition.target)
        queue.enqueue(transition.target)
  unreachable = allStates - visited
  return unreachable == empty
```

### Deadlock Detection

```
function checkDeadlocks(stateMachine):
  deadlocks = []
  for each state in stateMachine.states:
    if state.type != 'final' and state has no outgoing transitions:
      deadlocks.add(state)
  return deadlocks
```

### Determinism Check

```
function checkDeterminism(stateMachine):
  conflicts = []
  for each state in stateMachine.states:
    for each event that state handles:
      transitions = state.transitionsFor(event)
      if transitions.length > 1:
        if not allHaveMutuallyExclusiveGuards(transitions):
          conflicts.add({state, event, transitions})
  return conflicts
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|-------------|---------|----------|
| God State | A single state can transition to every other state | Introduce hierarchy to constrain transitions |
| Boolean Explosion | `isLoading && !isError && isRetrying` | Split into explicit states |
| Implicit State | State encoded in context variables | Define explicit state nodes |
| Missing Error States | No error handling | Define onError for every invoke |
| Orphan State | Unreachable states exist | Detect via reachability check |
