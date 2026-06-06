# Crypt Handoff Templates

## Receiving Handoffs

### From Sentinel (Vulnerability Report)

```yaml
SENTINEL_TO_CRYPT_HANDOFF:
  source: Sentinel
  content:
    vulnerabilities:
      - type: "[crypto anti-pattern | weak algorithm | key management]"
        location: "[file:line]"
        severity: "[critical | high | medium]"
        description: "[what was found]"
    scan_scope: "[files or modules scanned]"
  request: "Design crypto fix for identified vulnerabilities"
```

### From Comply (Regulatory Requirements)

```yaml
COMPLY_TO_CRYPT_HANDOFF:
  source: Comply
  content:
    regulation: "[FIPS 140-2 | PCI-DSS | HIPAA | GDPR]"
    crypto_requirements:
      - requirement: "[specific crypto requirement]"
        section: "[regulation section reference]"
    current_compliance: "[compliant | non-compliant | partial]"
  request: "Select algorithms meeting regulatory requirements"
```

### From Gateway (API Auth Design)

```yaml
GATEWAY_TO_CRYPT_HANDOFF:
  source: Gateway
  content:
    api_design: "[OpenAPI spec or summary]"
    auth_requirements:
      type: "[JWT | API key | mTLS | OAuth2]"
      sensitivity: "[public | internal | confidential]"
    current_auth: "[existing auth mechanism if any]"
  request: "Design cryptographic auth scheme for API"
```

## Sending Handoffs

### To Builder (Implementation Spec)

```yaml
CRYPT_TO_BUILDER_HANDOFF:
  source: Crypt
  destination: Builder
  content:
    crypto_spec:
      algorithms: ["[algorithm selections with parameters]"]
      libraries: ["[recommended libraries with versions]"]
      key_management:
        generation: "[how to generate keys]"
        storage: "[where to store keys]"
        rotation: "[rotation schedule and procedure]"
      code_examples: ["[reference implementations]"]
    anti_patterns_to_avoid: ["[specific anti-patterns for this context]"]
    test_vectors: ["[known-answer test vectors for verification]"]
  request: "Implement cryptographic design"
```

### To Sentinel (Design Verification)

```yaml
CRYPT_TO_SENTINEL_HANDOFF:
  source: Crypt
  destination: Sentinel
  content:
    crypto_design: "[architecture summary]"
    algorithms_used: ["[algorithm list with parameters]"]
    key_management: "[key lifecycle design]"
    threat_model: "[what attacks this defends against]"
    verification_points:
      - check: "[what to verify]"
        expected: "[expected result]"
  request: "Verify cryptographic design for security"
```

### To Cloak (Privacy Layer)

```yaml
CRYPT_TO_CLOAK_HANDOFF:
  source: Crypt
  destination: Cloak
  content:
    encryption_layer:
      algorithm: "[selected algorithm]"
      scope: "[what data is encrypted]"
      key_hierarchy: "[key management structure]"
    searchable_encryption: "[blind index or other searchable scheme if applicable]"
    data_retention: "[crypto-based deletion capability]"
  request: "Integrate encryption layer into privacy architecture"
```
