# AWS CDK Scaffolding Reference

Purpose: Scaffold an AWS CDK app (TypeScript or Python) with construct selection, stack layout, multi-environment pattern (ephemeral / staging / prod), cross-stack references, and CDK Nag integration — so the synthesized CloudFormation is reviewable, environment-safe, and passes a security baseline before the first deploy.

## Scope Boundary

- **Scaffold `cdk`**: AWS-only, code-first IaC in TypeScript / Python (construct choice, stack boundaries, env matrix, Nag integration).
- **Scaffold `terraform`**: provider-agnostic / multi-cloud IaC. Pick `terraform` when the team standardizes on HCL or when non-AWS providers are in play.
- **Scaffold `cloudformation`**: raw CFN YAML / JSON or SAM. Pick when the team does not want a compiler step, or when existing CFN templates dominate.
- **Scaffold `pulumi`**: code-first IaC *across* clouds. Pick when AWS + GCP / Azure must share one codebase.
- **Pipe (elsewhere)**: CI/CD — `cdk diff`, `cdk deploy --require-approval`, approval gates. `cdk` scaffolds the app; `Pipe` wires the pipeline.
- **Sentinel (elsewhere)**: security audit of the synthesized template. `cdk` integrates Nag; `Sentinel` reviews findings and exceptions.

If the request is "AWS only, prefer real code over HCL" → `cdk`. If "multi-cloud code-first" → `pulumi`. If "HCL shop" → `terraform`.

## Construct Level Selection

| Level | Example | When to pick | When to avoid |
|-------|---------|--------------|---------------|
| L1 (Cfn*) | `CfnBucket` | You need a property the L2 doesn't expose yet | Default — L1 leaks CFN boilerplate into app code |
| L2 | `s3.Bucket`, `lambda.Function` | Default. Sane defaults + type safety | Rarely — prefer L2 |
| L3 / Patterns | `apigateway.LambdaRestApi`, `ecs_patterns.ApplicationLoadBalancedFargateService` | Composed pattern matches exactly | Pattern hides a control you need to tune → drop to L2 |

Default to L2. Escape to L1 for single properties via `.node.defaultChild as CfnBucket` escape hatch; never copy the whole L1 into your code.

## Stack Layout

One app, multiple stacks. Split by blast radius and lifecycle — not by file count.

```
bin/
  app.ts                # app entry, instantiates stacks per env
lib/
  network-stack.ts      # VPC, subnets, endpoints      (long-lived, rare change)
  data-stack.ts         # RDS, S3, KMS                 (long-lived, stateful)
  compute-stack.ts      # ECS / Lambda / API Gateway   (frequent change)
  observability-stack.ts# CloudWatch, alarms, dashboards
  stateless-stack.ts    # queues, topics, step functions
test/
  snapshot.test.ts
cdk.json
cdk.context.json
```

Rules:
- Stateful resources (RDS, S3, KMS keys) live in long-lived stacks with `removalPolicy: RETAIN` in prod.
- Compute / stateless stacks can be torn down and recreated; never place a database in one.
- Cross-stack dependencies flow one direction: `network → data → compute → observability`.

## Multi-Environment Pattern

```ts
// bin/app.ts
const app = new cdk.App();

const envs: Record<string, cdk.Environment & { stage: string }> = {
  dev:     { account: '111', region: 'ap-northeast-1', stage: 'dev' },
  staging: { account: '222', region: 'ap-northeast-1', stage: 'staging' },
  prod:    { account: '333', region: 'ap-northeast-1', stage: 'prod' },
};

// Ephemeral per-PR envs share the dev account, distinguished by stage name.
const stage = app.node.tryGetContext('stage') ?? 'dev';
const prNumber = app.node.tryGetContext('pr');
const effectiveStage = prNumber ? `pr-${prNumber}` : stage;
const env = envs[stage];

const net    = new NetworkStack(app, `Net-${effectiveStage}`, { env });
const data   = new DataStack(app,    `Data-${effectiveStage}`, { env, vpc: net.vpc });
const compute = new ComputeStack(app, `App-${effectiveStage}`,  { env, db: data.cluster });
```

| Env | Account | Protection | TTL |
|-----|---------|------------|-----|
| Ephemeral (`pr-*`) | dev | `removalPolicy: DESTROY`, no backups | Auto-destroy on PR close (CI hook) |
| `dev` | dev | `DESTROY` ok | Persistent |
| `staging` | shared / staging | `RETAIN` stateful, synthetic data | Persistent, parity with prod |
| `prod` | prod | `RETAIN` everywhere, `terminationProtection: true` | Permanent |

Never share an account between `dev` and `prod`. Blast-radius isolation is the primary defense against IAM misconfiguration.

## Cross-Stack References

CDK auto-wires `CfnOutput` / `Fn::ImportValue` when you pass a resource between stacks. This is convenient but sticky — the *producing* stack cannot change the exported resource while a consumer imports it.

Guidelines:
- Small, stable surface between stacks: VPC, SG, cluster ARN, secret ARN.
- For anything that churns (Lambda code, container image tag), pass via SSM Parameter Store / Secrets Manager lookup at runtime, not as a stack output.
- Use `ssm.StringParameter.valueForStringParameter(this, '/payments/dev/db-host')` for loose coupling.
- Document every cross-stack reference in the stack header — future-you will thank you when a rename breaks deploys.

## CDK Nag Integration

Add at app construction, not per-stack. Treat findings as blocking.

```ts
import { AwsSolutionsChecks, NagSuppressions } from 'cdk-nag';

cdk.Aspects.of(app).add(new AwsSolutionsChecks({ verbose: true }));

// Explicit, justified suppression — never broad.
NagSuppressions.addResourceSuppressions(bucket, [
  {
    id: 'AwsSolutions-S1',
    reason: 'Access logs are centralized in the audit account; per-bucket logging would duplicate.',
  },
]);
```

Rules:
- Suppressions live next to the resource, with a written reason.
- Never `addStackSuppressions` as a blanket silence — audit trail disappears.
- Run Nag in `cdk synth` in CI; fail on any unsuppressed finding.

## Testing

| Test | Tool | What it catches |
|------|------|-----------------|
| Synthesis | `cdk synth` in CI | Compile errors, Nag findings |
| Snapshot | `@aws-cdk/assertions` + Jest/pytest | Unintended template drift |
| Fine-grained | `Template.fromStack(s).hasResourceProperties(...)` | Specific property invariants (encryption on, public access off) |
| Deploy dry-run | `cdk diff` | Pre-deploy review — what will change |

```ts
test('bucket is encrypted and blocks public access', () => {
  const app = new cdk.App();
  const stack = new DataStack(app, 'T', { env, vpc: mockVpc });
  const tmpl = Template.fromStack(stack);
  tmpl.hasResourceProperties('AWS::S3::Bucket', {
    BucketEncryption: Match.objectLike({ ServerSideEncryptionConfiguration: Match.anyValue() }),
    PublicAccessBlockConfiguration: Match.objectLike({ BlockPublicAcls: true }),
  });
});
```

## Bootstrap & Version Hygiene

- `cdk bootstrap` once per account+region. Pin bootstrap version in CI; mismatches cause cryptic deploy failures.
- Pin `aws-cdk-lib` and `constructs` in lockfile. CDK minor versions introduce quiet defaults changes.
- Keep a single CDK version across the monorepo — construct type mismatches surface as `any` and silently break L2 typing.

## Anti-Patterns

- Using L1 constructs everywhere — you have rebuilt raw CFN in TypeScript without benefiting from L2 defaults.
- One giant stack containing VPC, RDS, and Lambda — any change blocks every deploy and expands blast radius.
- Putting stateful resources in a stack with `removalPolicy: DESTROY` — one `cdk destroy` drops production data.
- Blanket `NagSuppressions.addStackSuppressions` — kills the whole point of Nag.
- Sharing one AWS account across dev / staging / prod — IAM mistakes cascade into production.
- `cdk deploy` from a developer laptop for production — no plan artifact, no approval, no audit trail.
- Output every internal ARN as a `CfnOutput` — creates hidden cross-stack dependencies that freeze refactors.
- Embedding image tags in the stack — use SSM / Secrets Manager lookup to decouple image bumps from stack deploys.
- Skipping `cdk diff` in CI — CloudFormation replacements (vs updates) go unnoticed and cause downtime.
- `new cdk.App()` without `env:` set — CDK synthesizes environment-agnostic templates and several features silently degrade.

## Handoff

When the CDK app is ready:

- **To Pipe**: the pipeline contract — `cdk synth`, `cdk diff` (posted on PR), `cdk deploy --require-approval broadening` for prod, rollback procedure. Share the bootstrap version and the context keys (`stage`, `pr`).
- **To Sentinel**: Nag findings with justified suppressions, IAM policy inventory, KMS key boundary, SG rules, and the secret hydration path.
- **To Beacon**: alarm + dashboard stack outputs, metrics emitted, and SLO defaults baked into the observability stack.
- **To Ledger** (if used): cost-tag taxonomy applied via `cdk.Tags.of(app).add(...)`, high-cost resources flagged (NAT GW, Aurora, Global Tables).
- **To Canvas**: stack graph and cross-stack reference edges for topology diagrams.
- **Escalation path**: if a second cloud enters scope, plan migration to `scaffold pulumi` before the AWS-only abstraction hardens.
