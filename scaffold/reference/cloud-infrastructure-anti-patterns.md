# Cloud Infrastructure Anti-Patterns

Purpose: Use this file when reviewing network topology, IAM, encryption, HA, or multi-account / multi-cloud guardrails.

Contents:
1. Network anti-patterns
2. IAM and security pitfalls
3. IaC security anti-patterns
4. Multi-account / multi-cloud pitfalls
5. Availability pitfalls

## Network Anti-Patterns

| ID | Anti-pattern | Signal | Safer pattern |
|----|--------------|--------|---------------|
| `NW-01` | Flat Network | everything in one public subnet | public/private split |
| `NW-02` | IP Address Exhaustion | `/24`-style subnets block scale-out | plan generous CIDR ranges such as `/16` VPC and `/20+` subnets where appropriate |
| `NW-03` | `0.0.0.0/0` Security Group | broad ingress or egress by default | narrow CIDR or SG references |
| `NW-04` | No VPC Endpoints | AWS service traffic pays NAT tax | add Gateway / Interface endpoints |
| `NW-05` | Single-AZ Deployment | one AZ outage causes full outage | multi-AZ design |
| `NW-06` | Overlapping CIDRs | future peering / TGW / hybrid links fail | explicit CIDR planning |
| `NW-07` | No Environment Segmentation | dev can reach prod | separate environments |

## IAM And Security Pitfalls

- Wildcard permissions
- Long-lived credentials
- No MFA or equivalent admin guard
- Shared service accounts/roles
- No SCPs or Organization Policies
- IMDSv1 reliance on EC2

## IaC Security Anti-Patterns

| ID | Anti-pattern | Safer pattern |
|----|--------------|---------------|
| `IS-01` | Console Drift | scheduled drift detection + console guardrails |
| `IS-02` | No Encryption Default | account/org-level encryption defaults |
| `IS-03` | Public Storage Buckets | block public access by policy |
| `IS-04` | No Audit Trail | CloudTrail / Audit Logs everywhere |
| `IS-05` | Unscanned IaC | policy checks in CI |

## Multi-Account / Multi-Cloud Pitfalls

- lowest-common-denominator architecture
- no landing-zone structure
- no data perimeter
- region sprawl
- no tagging strategy

## Availability Pitfalls

| ID | Anti-pattern | Safer pattern |
|----|--------------|---------------|
| `HA-01` | No Backup Strategy | automated snapshots and restore tests |
| `HA-02` | Single Point of Failure | multi-AZ NAT, DB, and ingress |
| `HA-03` | No DR Plan | define RPO/RTO and recovery pattern |
| `HA-04` | Hardcoded Resource References | use data sources and variables |
