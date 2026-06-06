# Policy as Code Reference

## Overview

Policy as Code (PaC) translates compliance requirements into machine-executable policies that can be tested, versioned, and enforced automatically in CI/CD pipelines and runtime environments.

---

## Tool Landscape

| Tool | Language | Use Case | Integration |
|------|----------|----------|-------------|
| **OPA (Open Policy Agent)** | Rego | General-purpose policy engine | Kubernetes, Terraform, CI/CD, API gateways |
| **Conftest** | Rego (via OPA) | Configuration file testing | Terraform, Kubernetes YAML, Dockerfile |
| **Checkov** | Python/YAML | IaC security scanning | Terraform, CloudFormation, Kubernetes, ARM |
| **Sentinel** (HashiCorp) | Sentinel | Terraform policy enforcement | Terraform Cloud/Enterprise |
| **Kyverno** | YAML | Kubernetes-native policies | Kubernetes admission controller |
| **AWS Cedar** | Cedar | Fine-grained authorization (ABAC/RBAC) | Amazon Verified Permissions, API gateways; deny-by-default semantics |
| **AWS Config Rules** | Python/JSON | AWS resource compliance | AWS native |
| **AWS Audit Manager** | Console/API | Evidence collection automation | AWS native; maps to SOC2/PCI-DSS/HIPAA/ISO 27001 |
| **Azure Policy** | JSON | Azure resource compliance | Azure native |
| **GCP Organization Policy / Policy Controller** | YAML/Rego | GCP resource constraints + Kubernetes | GCP native + Anthos |

Sources: [OPA docs](https://www.openpolicyagent.org/docs/latest/) | [Cedar policy language](https://docs.cedarpolicy.com/) | [Amazon Verified Permissions (Cedar 4.5)](https://aws.amazon.com/about-aws/whats-new/2025/08/amazon-verified-permissions-cedar-4-5/) | [Kyverno docs](https://kyverno.io/docs/)

---

## OPA/Rego Patterns for Compliance

### Access Control Policy (SOC2 CC6.1, PCI-DSS Req 7)

```rego
package compliance.access_control

# Deny if user lacks required role for resource
deny[msg] {
    input.action == "access"
    not has_required_role(input.user, input.resource)
    msg := sprintf("User %s lacks required role for %s", [input.user.id, input.resource.type])
}

has_required_role(user, resource) {
    required := role_requirements[resource.type]
    user.roles[_] == required[_]
}

role_requirements := {
    "cardholder_data": ["pci_admin", "payment_processor"],
    "ephi": ["hipaa_authorized", "healthcare_admin"],
    "audit_logs": ["security_admin"],
}
```

### Encryption Enforcement (PCI-DSS Req 3.4, HIPAA §164.312)

```rego
package compliance.encryption

# Terraform: Deny unencrypted storage
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket"
    not has_encryption(resource)
    msg := sprintf("S3 bucket %s must have encryption enabled (PCI-DSS Req 3.4)", [resource.name])
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_rds_instance"
    not resource.change.after.storage_encrypted
    msg := sprintf("RDS instance %s must have storage encryption (HIPAA §164.312(a)(2)(iv))", [resource.name])
}

has_encryption(resource) {
    resource.change.after.server_side_encryption_configuration[_].rule[_].apply_server_side_encryption_by_default[_].sse_algorithm
}
```

### Logging Requirements (PCI-DSS Req 10, SOC2 CC7.2)

```rego
package compliance.logging

# Ensure CloudTrail is enabled and configured
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_cloudtrail"
    not resource.change.after.enable_logging
    msg := "CloudTrail logging must be enabled (PCI-DSS Req 10)"
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_cloudtrail"
    not resource.change.after.is_multi_region_trail
    msg := "CloudTrail must be multi-region (SOC2 CC7.2)"
}
```

---

## CI/CD Integration

### Pipeline Architecture

```
Code Commit
    |
    v
[Static Analysis] -> Sentinel/Conftest (IaC policies)
    |
    v
[Build]
    |
    v
[Test] -> OPA unit tests for policies
    |
    v
[Compliance Gate] -> OPA/Conftest evaluation against compliance policies
    |                 PASS -> continue
    |                 FAIL -> block + notify
    v
[Deploy] -> Kubernetes admission (OPA Gatekeeper / Kyverno)
    |
    v
[Runtime] -> Continuous compliance monitoring
```

### Conftest in CI Example

```yaml
# .github/workflows/compliance.yml
compliance-check:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Install conftest
      run: |
        wget -qO- https://github.com/open-policy-agent/conftest/releases/download/v0.50.0/conftest_0.50.0_Linux_x86_64.tar.gz | tar xz
        sudo mv conftest /usr/local/bin/
    - name: Run compliance policies
      run: |
        conftest test terraform/ --policy policy/compliance/ --output json
        conftest test kubernetes/ --policy policy/compliance/ --output json
```

---

## Policy Testing

```rego
# policy/compliance/access_control_test.rego
package compliance.access_control

test_deny_unauthorized_access {
    deny["User user123 lacks required role for cardholder_data"] with input as {
        "action": "access",
        "user": {"id": "user123", "roles": ["viewer"]},
        "resource": {"type": "cardholder_data"}
    }
}

test_allow_authorized_access {
    count(deny) == 0 with input as {
        "action": "access",
        "user": {"id": "admin1", "roles": ["pci_admin"]},
        "resource": {"type": "cardholder_data"}
    }
}
```

---

## Continuous Compliance Monitoring

| Component | Purpose | Tools |
|-----------|---------|-------|
| Drift detection | Detect configuration changes that break compliance | AWS Config, OPA + periodic scan |
| Evidence collection | Automated compliance evidence gathering | Custom scripts, cloud-native tools |
| Dashboard | Real-time compliance posture visualization | Grafana, cloud-native dashboards |
| Alerting | Notify on compliance violations | PagerDuty, Slack, OpsGenie |
| Reporting | Scheduled compliance status reports | Custom reporting + Scribe agent |

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Policies only in CI, not runtime | Drift goes undetected | Add runtime enforcement (OPA Gatekeeper, cloud-native policies) |
| Policies without tests | False positives/negatives go unnoticed | Test every policy with positive and negative cases |
| Manual exception process | Exceptions are undocumented | Codify exceptions as policy rules with expiry dates |
| Overly broad policies | Too many false positives, developers ignore | Scope policies to specific resource types and environments |
| No policy versioning | Can't track policy changes over time | Store policies in git with conventional commits |
