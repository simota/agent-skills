# Workflow Engine Selection Guide

**Purpose:** Selection guide for workflow engines.
**Read when:** Picking the right workflow engine for a project.

---

## Engine Comparison Matrix

| Engine | Type | Language | Hosting | Durability | Complexity | Cost Model |
|--------|------|----------|---------|------------|------------|------------|
| Temporal | General | Go/Java/TS/Python | Self/Cloud | High | Medium-High | Self: infra, Cloud: per-action |
| AWS Step Functions | Serverless | ASL (JSON) | AWS | High | Medium | Per transition |
| Inngest | Event-driven | TS/Go/Python | Cloud/Self | High | Low-Medium | Per run |
| Restate | General | TS/Java/Go/Rust | Self/Cloud | High | Low-Medium | Infra only |
| DBOS Transact | General | TS/Python/Java/Go | Self/Cloud | High (Postgres-backed) | Low | Per execution |
| XState | Client-side / Node | TS/JS | N/A (in-process) | None (stateless) | Low-Medium | Free |
| Apache Airflow | Data pipeline | Python | Self/Cloud | Medium | Medium | Infra only |
| Prefect | Data pipeline | Python | Self/Cloud | Medium | Low-Medium | Per task |

> **Note:** Cadence (Uber's predecessor to Temporal) is effectively superseded by Temporal for new projects. Source: [temporal.io](https://temporal.io/blog/what-is-durable-execution)

---

## Selection Decision Tree

```
What kind of workflow is it?
├── Frontend / in-process state management
│   └── XState v5 (Actor model, createActor)
├── Data pipeline / ETL
│   ├── Python-heavy → Airflow or Prefect
│   └── Stream integration → Kafka Streams (see Stream agent)
├── Serverless / event-driven
│   ├── AWS-only → Step Functions
│   └── Multi-cloud / Next.js → Inngest or Trigger.dev
├── AI agent workflows (durable execution)
│   ├── LangGraph — stateful graph-based agents, human-in-the-loop
│   ├── Temporal + OpenAI Agents SDK — durable long-running agents
│   └── DBOS + OpenAI Agents SDK — Postgres-backed durable agents
└── General business workflow
    ├── Already on AWS → Step Functions
    ├── Want minimal infra overhead + Postgres only → DBOS Transact
    ├── Want durable async/await with service-boundary isolation → Restate
    ├── Multi-cloud / high availability
    │   ├── Want managed service → Temporal Cloud
    │   └── Self-hosting OK → Temporal OSS
    └── Simple event chain → Inngest
```

---

## Temporal

### Strengths
- Language-native workflow definitions (code is the workflow)
- Strong durability guarantees (replay-safe execution)
- Signal/Query/Update for external interaction with workflow state
- Child Workflow and Continue-as-new support long-running workflows

### Best For
- Long-running business processes (days to months)
- Complex compensation and retry logic
- Microservice-to-microservice orchestration

### Template

```yaml
TEMPORAL_WORKFLOW:
  name: "[WorkflowName]"
  task_queue: "[queue-name]"
  workflow_execution_timeout: "30d"
  activities:
    - name: "[ActivityName]"
      start_to_close_timeout: "30s"
      retry_policy:
        initial_interval: "1s"
        backoff_coefficient: 2.0
        maximum_attempts: 5
        non_retryable_error_types: ["BusinessError"]
  signals:
    - name: "[SignalName]"
      description: "[External trigger]"
  queries:
    - name: "[QueryName]"
      description: "[State inspection]"
```

---

## AWS Step Functions

> Source: [aws.amazon.com — Distributed Map Feb 2025](https://aws.amazon.com/about-aws/whats-new/2025/02/aws-step-functions-data-source-output-option-distributed-map/), [aws.amazon.com — Distributed Map Sep 2025](https://aws.amazon.com/about-aws/whats-new/2025/09/aws-step-functions-data-source-options-observability-distributed-map/)

### Strengths
- Native integration with AWS services (Lambda, SQS, DynamoDB, etc.)
- Declarative workflow definitions via ASL
- Two execution modes: Express (high-volume, at-least-once) and Standard (long-running, exactly-once)
- Distributed Map for large-scale parallel data processing:
  - Feb 2025: JSONL, semicolon/tab-delimited formats, output transformations
  - Sep 2025: Athena manifest, Parquet, S3ListObjectsV2 prefix iteration, JSON array extraction, observability metrics (`Approximate Open Map Runs Count`)
- Built-in error handling and retries

### Best For
- AWS-centric architectures
- Serverless workflows
- Orchestrating Lambda functions
- Large-scale parallel data processing (Distributed Map)

### Template

```json
{
  "Comment": "[WorkflowDescription]",
  "StartAt": "[FirstState]",
  "States": {
    "[StateName]": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...",
      "Retry": [{
        "ErrorEquals": ["States.TaskFailed"],
        "IntervalSeconds": 2,
        "MaxAttempts": 3,
        "BackoffRate": 2.0
      }],
      "Catch": [{
        "ErrorEquals": ["States.ALL"],
        "Next": "[ErrorHandler]"
      }],
      "Next": "[NextState]"
    }
  }
}
```

---

## Restate

> Source: [restate.dev](https://restate.dev), [pkgpulse.com — inngest-vs-trigger-dev-v3-vs-restate-2026](https://www.pkgpulse.com/guides/inngest-vs-trigger-dev-v3-vs-restate-2026)

### Strengths
- Durable async/await baked into service boundaries via an opt-in SDK — developers choose which code paths are durable
- Strongly-typed RPC between services with built-in retry and exactly-once semantics
- Lightweight compared to Temporal: no external orchestrator cluster required

### Best For
- Microservice orchestration where workflow correctness must be enforced at service boundaries
- TypeScript, Java, Go, and Rust backends
- Teams wanting Temporal-class durability without the operational overhead

---

## DBOS Transact

> Source: [dbos.dev/dbos-transact](https://www.dbos.dev/dbos-transact), [dbos.dev — March 2026 updates](https://www.dbos.dev/blog/dbos-new-features-march-2026)

### Strengths
- Postgres-backed durable execution: workflow state is checkpointed in Postgres — no separate orchestration cluster
- Minimal integration footprint: a 110-LoC app requires only ~7 lines of change vs. >100 for Temporal
- Supports TypeScript, Python, Java, Go, and Kotlin (as of March 2026)
- Workflow patching (March 2026): upgrade workflow code while existing workflow executions are in-flight
- Parent/child workflow relationships are indexed for navigating complex nested workflows
- Integrates with OpenAI Agents SDK for durable AI agent execution

### Best For
- Teams that already run Postgres and want durability without a new cluster
- Background jobs, scheduled workflows, AI agent pipelines
- Lightweight durable execution in serverless and container environments

### Template (TypeScript)

```typescript
import { DBOS } from '@dbos-inc/dbos-sdk';

class OrderWorkflow {
  @DBOS.workflow()
  static async processOrder(orderId: string) {
    await OrderWorkflow.reserveInventory(orderId);
    await OrderWorkflow.chargePayment(orderId);
    await OrderWorkflow.dispatchShipment(orderId);
  }

  @DBOS.step()
  static async reserveInventory(orderId: string) { /* ... */ }

  @DBOS.step()
  static async chargePayment(orderId: string) { /* ... */ }

  @DBOS.step()
  static async dispatchShipment(orderId: string) { /* ... */ }
}
```

---

## Inngest

### Strengths
- Event-driven with a simple API
- Serverless-first (integrates with Vercel, Cloudflare, and others)
- Built-in step functions, sleep, and wait-for-event
- Great local development experience (Dev Server)

### Best For
- Next.js / Vercel-based projects
- Event-driven workflows
- Background jobs

### Template (TypeScript)

```typescript
// Inngest function definition
const workflow = inngest.createFunction(
  { id: "[function-id]", retries: 3 },
  { event: "[trigger/event]" },
  async ({ event, step }) => {
    const result1 = await step.run("[step-1]", async () => {
      // Step 1 logic
    });

    await step.sleep("wait-period", "1h");

    const result2 = await step.run("[step-2]", async () => {
      // Step 2 logic using result1
    });

    return { result1, result2 };
  }
);
```

---

## XState (v5)

> Source: [stately.ai/docs/actors](https://stately.ai/docs/actors), [stately.ai/docs/setup](https://stately.ai/docs/setup), [stately.ai/blog/2023-12-01-xstate-v5](https://stately.ai/blog/2023-12-01-xstate-v5)

### Strengths
- Full Actor model: `createActor()` creates an implicit actor system where the root actor can spawn and communicate with child actors via the receptionist pattern (`systemId`)
- `setup({ ... })` function provides type-bound action helpers, strongly typed guards, actors, delays, and context — reducing boilerplate and enabling robust type inference
- Deep (recursive) persistence: invoked/spawned actors are persisted along with their descendants
- `input` support: pass initial data to machines via `createActor(machine, { input })`
- Works in browser and Node.js; visual editor via Stately Studio

### Best For
- Frontend and server-side state management
- Form wizards and UI flows
- Actor-based concurrency patterns

### Template (v5 — setup + createActor)

```typescript
import { setup, createActor } from 'xstate';

const machine = setup({
  types: {
    context: {} as { count: number },
    events: {} as { type: 'INCREMENT' } | { type: 'RESET' },
  },
  actions: {
    increment: ({ context }) => ({ count: context.count + 1 }),
  },
}).createMachine({
  id: '[machineName]',
  initial: '[initialState]',
  context: { count: 0 },
  states: {
    // state definitions
  },
});

const actor = createActor(machine, { input: { /* initial input */ } });
actor.subscribe(snapshot => console.log(snapshot.value));
actor.start();
```

> **Migration note:** XState v4 APIs (`Machine()`, `interpret()`) are removed in v5. Use `setup().createMachine()` + `createActor()` instead.

---

## BPMN 2.0 Engines (Camunda 8 / Zeebe)

> Source: [camunda.com/platform/zeebe](https://camunda.com/platform/zeebe/), [camunda.com — migrate from Camunda 7 to 8 (2025)](https://camunda.com/blog/2025/07/migrate-from-camunda-7-to-camunda-8/)

### Camunda 8 (Zeebe engine)

| Feature | Details |
|---------|---------|
| Engine | Zeebe — distributed, event-driven (replaces Camunda 7 monolith) |
| Standard | BPMN 2.0 + ad-hoc subprocesses (exception handling, human-in-the-loop) |
| Testing | Camunda Process Test (CPT) with reusable test scenario files (GA 2025) |
| AI | BPMN Copilot (SaaS): generate process diagrams from natural language |
| Migration | Camunda 7 → 8 migration is recommended; Zeebe Java client replaces Zeebe Java client v8.8+ |
| Client | Camunda Java client (unified, replaces Zeebe Java client from 8.8.0) |

> **Removed guidance:** Camunda 7 (Activiti-based) is in maintenance mode. New projects should use Camunda 8. Use BPMN boundary timer + escalation events for timeouts — not BPMN error events.

---

## AI Agent Workflow Engines

> Source: [LangGraph v1 adoption — fordelstudios.com (2026)](https://fordelstudios.com/research/state-of-ai-agent-frameworks-2026), [Temporal + OpenAI Agents SDK — temporal.io (Aug 2025)](https://temporal.io/blog/durable-digest-august-2025)

| Engine | Approach | Best For |
|--------|---------|---------|
| LangGraph | Graph-based state machine; nodes = agents/tools/checkpoints; edges = conditional transitions | Stateful multi-agent workflows, audit trails, rollback |
| Temporal + OpenAI Agents SDK | Durable workflow wrapping LLM agent execution | Long-running agents that must survive crashes |
| DBOS + OpenAI Agents SDK | Postgres-backed durable agent execution | Lightweight durable agents without a separate cluster |

---

## Non-Functional Requirements Checklist

Non-functional requirements to verify during selection:

| Requirement | Question |
|-------------|----------|
| Durability | Can a workflow resume if the process crashes mid-execution? |
| Scalability | What is the concurrency ceiling? Does it scale out? |
| Observability | Are execution-state visibility, logs, and metrics sufficient? |
| Cost | Cost projection based on execution count and transition count |
| Latency | Latency requirements between steps |
| Vendor lock-in | Degree of dependency on a specific cloud vendor |
| Team skill | Fit with the team's existing skill set |
| Community | Community activity and documentation quality |
