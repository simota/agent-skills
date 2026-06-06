# GCP Infrastructure Specialist Reference

Purpose: Use this file when GCP-specific networking, runtime, database, messaging, IAM, or cost decisions materially affect the design.

Contents:
1. Networking decisions
2. Compute and orchestration choices
3. Database choices
4. Messaging and workflow choices
5. IAM and organization controls
6. GCP-specific cost optimization

## Networking Decisions

| Decision | Preferred choice |
|----------|------------------|
| Centralized network shared across projects | Shared VPC |
| Full team-level isolation | Separate VPCs + peering |
| Regulated data perimeter | VPC Service Controls |
| Private access to Google APIs | Private Google Access |
| Private access to managed services | Private Service Connect |

## Compute And Orchestration Choices

| Use case | Recommended | Alternative | Avoid |
|----------|-------------|-------------|-------|
| Stateless web API | Cloud Run | GKE Autopilot if Kubernetes is required | Compute Engine |
| Batch processing | Cloud Run Jobs | Dataflow for streaming/data workloads | Compute Engine |
| Standard Kubernetes needs | GKE Autopilot | GKE Standard for advanced customization | unmanaged clusters |

Standard vs Autopilot:

| Criteria | Standard | Autopilot |
|----------|----------|-----------|
| Node management | Manual | Automatic |
| Billing | Per node | Per pod |
| Customization | High | Limited |
| Default recommendation | only when required | most use cases |

## Database Choices

| Requirement | Recommended |
|-------------|-------------|
| Standard web app OLTP | Cloud SQL |
| High-performance PostgreSQL / HTAP | AlloyDB |
| Global distribution and very high consistency | Spanner |

Reference cost/availability anchors:
- Cloud SQL: about `$50+`
- AlloyDB: about `$500+`
- Spanner: about `$2,000+`

## Messaging And Workflow Choices

| Need | Recommended |
|------|-------------|
| Event fan-out and notifications | Pub/Sub |
| Rate-limited or scheduled task execution | Cloud Tasks |
| Multi-step orchestration | Workflows |

## IAM And Organization Controls

- Use Organization Policies for region restrictions and storage guardrails.
- Prefer Workload Identity Federation for GitHub Actions over service-account keys.
- Treat public IPs on Cloud SQL as a risk unless explicitly justified.
- Cloud Run error-rate alert example threshold is `>5%` over `300s`.

## GCP-Specific Cost Optimization

- Cloud SQL `REGIONAL` is the production default; use smaller or single-zone options outside prod when safe.
- Cloud Run `min_instances = 0` is a strong default for non-prod.
- GKE Standard can use Spot VMs; Autopilot is simpler but still needs cost review.
- Cloud NAT should be removed or shared in non-prod when possible.
- CUD discounts roughly range from `25-55%` depending on type and term.
