# Modern Verification Tooling

**Purpose:** Tooling guidance for spec-vs-implementation conformance, internal-behaviour ACs, contract-test maintenance, and .NET BDD framework selection. Cite these recommendations in compliance reports when the target stack matches.
**Read when:** Authoring verification reports that recommend specific frameworks beyond hand-authored BDD scenarios.

---

## Schemathesis — Stateful API Conformance

Drive verification from the OpenAPI / GraphQL spec. The property-based engine explores state transitions and surfaces conformance gaps that human-authored BDD scenarios miss.

- Treat Schemathesis output as evidence of **spec-vs-implementation** conformance.
- Treat hand-authored BDD as evidence of **intent-vs-implementation** conformance.
- Both are required for a full verdict on REST/GraphQL services.

Source: schemathesis.io

---

## Tracetest — Internal-Behaviour ACs

When an AC says "on submit, the audit log records the event AND the cache is invalidated AND no PII is logged", an HTTP-only verifier cannot prove it.

- Tracetest asserts on individual OpenTelemetry spans, making internal-behaviour ACs first-class verifiable.
- Add Tracetest assertions to the BDD step library for distributed-system ACs.

Source: tracetest.io

---

## PactFlow HaloAI — AI-Augmented Contract Derivation

Generate Pact contracts from OpenAPI specs and observed traffic; HaloAI maintains them as the spec evolves.

- Reduces contract-test maintenance overhead by ~60% in published deployments.
- Recommend on consumer-driven contract programmes where AC drift between provider and consumer specs is the bottleneck.

Source: pactflow.io/ai/

---

## Reqnroll over SpecFlow — .NET BDD

SpecFlow has been stagnant since 2022; Reqnroll is the active fork.

- Same Gherkin syntax, .NET 10 and Cucumber Messages v30 compatible.
- Verification reports targeting .NET stacks must call out the migration explicitly rather than continuing to cite SpecFlow.

Source: reqnroll.net; reqnroll.net/news/2024/02/from-specflow-to-reqnroll-why-and-how/

---

## Supply-Chain Provenance (v6 fold-in)

Capability-gated optional evidence-package fields for SLSA-style conformance.

| Field | Format |
|-------|--------|
| `sbom_ref` | CycloneDX / SPDX URI |
| `signature_ref` | Cosign bundle digest |
| `provenance_attestation` | SLSA v1.2 in-toto statement |

**Policy:**
- Advisory by default when Sigstore / Cosign / SBOM-generator infra is available.
- Downgrade to `supply_chain_provenance: skipped (org capability missing)` when any of (Fulcio reachable / Rekor v2 reachable / SBOM generator wired into CI) is missing.
- Mandatory only when the Tier policy declares it (Enterprise Tier-S regulated domains).
- Never block merge for absent supply-chain fields on orgs without infra (reproduces the SLSA/Cosign prerequisite tyranny anti-pattern — omen v6 FM-7, RPN 252).

---

## Citation Form Discipline (v5 fold-in)

When emitting `@source:` citations for documentation Claim-Binding or traceability evidence:

| Preferred | Example |
|-----------|---------|
| Symbol-based | `@source:billing-service::createInvoice` |
| Content-hash | `@source:openapi.yaml#sha256:abc...` |
| Line-number (only with content-hash anchor) | `@source:src/api.ts#L12-45#sha256:...` |

Raw line-number references silently drift on refactor and can point to unrelated code while still passing existence checks (omen v5 FM-D-2, RPN 648). Line-number-only citations are forbidden.

---

## BDD Anti-Pattern Sources

Reference list for the Boundaries Never rules in SKILL.md.

| Anti-pattern | Sources |
|--------------|---------|
| BDD as post-implementation test scripts | cucumber.io; thoughtworks.com |
| Implementation details in scenario steps | cucumber.io; johnfergusonsmart.com |
| Multi-outcome scenarios | cucumber.io |
| Abstract scenarios without concrete data | cucumber.io anti-patterns |
| Scenario Outline overuse / test explosion | cucumber.io |
| Imperative (vs declarative) scenarios | cucumber.io; johnfergusonsmart.com |
| Mixed precondition/action in Given | cucumber.io; thoughtworks.com |
| LLM scenario hallucination (~5% rate) | arxiv.org/abs/2508.20744 |

---

## ISO/IEC/IEEE 29148 Quality Attributes — Source Notes

The Complete attribute requires criteria to be self-contained so verification can proceed without chasing cross-references (Source: ISO/IEC/IEEE 29148:2018 individual requirement characteristics).
