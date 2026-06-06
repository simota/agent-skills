# AWS Infrastructure Specialist Reference

Purpose: Use this file when AWS-specific networking, compute, database, messaging, IAM, or cost decisions materially affect the design.

Contents:
1. Networking decisions
2. Compute service selection
3. Database and storage choices
4. Messaging and orchestration
5. IAM and account strategy
6. AWS-specific cost optimization

## Networking Decisions

| Decision | Preferred choice |
|----------|------------------|
| `3` or fewer VPCs | VPC Peering |
| `4+` VPCs or on-prem integration | Transit Gateway |
| S3 / DynamoDB private access | Gateway Endpoint (free) |
| Other private AWS service access | Interface Endpoint (`~$7.5/month + transfer`) |

## Compute Service Selection

| Use case | Recommended | Alternative | Avoid |
|----------|-------------|-------------|-------|
| Always-on web API | ECS Fargate | EKS if Kubernetes is required | Direct EC2 management |
| Low-traffic API | Lambda or App Runner | Fargate | EC2 |
| Short batch jobs | Lambda | Step Functions + Lambda | EC2 |
| Long-running batch | ECS Tasks | Step Functions + ECS | Lambda |
| Existing Kubernetes platform | EKS | Fargate for simpler services | unmanaged clusters |

## Database And Storage Choices

| Need | Recommended choice |
|------|--------------------|
| General relational DB | Aurora Serverless v2 or RDS |
| Unpredictable key-value workload | DynamoDB On-Demand |
| Stable predictable DynamoDB workload | Provisioned + Auto Scaling |
| Lifecycle-based object storage savings | S3 lifecycle + Intelligent Tiering / IA / Glacier |
| CDN + static/private origin | CloudFront + OAC |

## Messaging And Orchestration

| Need | Recommended |
|------|-------------|
| General async queue | SQS Standard |
| Strict ordering / dedupe | SQS FIFO |
| Event routing | EventBridge |
| Workflow with `3+` steps and branching/retry | Step Functions |

## IAM And Account Strategy

- Prefer multi-account separation for management, security, logs, shared services, and workloads.
- Use permission boundaries for delegated administration.
- Use cross-account roles with `ExternalId`.
- Enforce region boundaries with SCPs where appropriate.
- No `0.0.0.0/0` ingress by default.

## AWS-Specific Cost Optimization

- Prefer `Compute Savings Plans` before stricter EC2-only commitments.
- Graviton can reduce compute cost by about `20%`.
- Monitor CPU and memory for at least `2+ weeks`.
- Average utilization under `40%` is a strong downsizing signal.
- Consider scheduled shutdowns for `dev` and `staging`.
- Use VPC endpoints to reduce NAT Gateway cost.
