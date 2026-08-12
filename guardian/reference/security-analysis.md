# Security-Aware Change Analysis Reference

Purpose: Classify security impact, trigger Sentinel or Probe when required, and surface dangerous change patterns early.

## Contents

- Security categories
- Classification criteria
- Escalation flow
- Sentinel protocol
- Probe integration
- Dangerous patterns
- Report template
- AI-generated code checks

## Security Impact Categories

| Category | Description | Action |
|----------|-------------|--------|
| `CRITICAL` | auth, crypto, secrets, permissions | immediate Sentinel handoff |
| `SENSITIVE` | user data, session, API keys | Sentinel review recommended |
| `ADJACENT` | code near security boundaries | monitor closely |
| `NEUTRAL` | no obvious security implications | standard review |

## Classification Criteria

### `CRITICAL`

Blocking Sentinel handoff is required for patterns such as:
- `**/auth/**`
- `**/security/**`
- `**/crypto/**`
- `**/permissions/**`
- `**/rbac/**`
- `.env*`
- `**/*.key`
- `**/*.pem`
- `**/secrets/**`

### `SENSITIVE`

Typical examples:
- `**/api/**`
- `**/middleware/**`
- `**/session/**`
- `**/payment/**`
- user-data processing, validation, session or cookie handling

### `ADJACENT`

Typical examples:
- `**/config/**`
- `**/database/**`
- migrations that affect auth or user-data behavior

## Escalation Flow

1. classify file and code patterns
2. mark blocking vs non-blocking
3. hand off to Sentinel when required
4. hand off to Probe for runtime API/auth validation when needed
5. fold returned findings into Guardian risk and PR strategy

## Sentinel Auto-Link Protocol

Trigger Sentinel when:
- `security_classification == CRITICAL`
- `SENSITIVE` change affects auth or permissions
- dangerous pattern count `> 0`
- secret exposure risk exists

## Probe Integration

Use Probe for:
- API changes
- auth or token flow changes
- validation or runtime exploit verification

Template:

```markdown
## GUARDIAN_TO_PROBE_HANDOFF

**Reason**: API/auth/runtime security verification needed
**Changed areas**:
- ...
```

## Dangerous Code Patterns

High-signal examples:
- secret or key material in source
- unsafe auth/permission handling
- insecure crypto usage
- missing validation on exposed endpoints
- unsafe AI-generated code near security boundaries

## Report Template

```markdown
## Security Impact Assessment

### Classification
- Security category: ...

### Critical Changes (Sentinel Handoff Required)
- ...

### Dangerous Patterns Detected
- ...

### Recommendation
- ...
```

## AI-Generated Code Detection

Code-based categories:
- `Verified`
- `Suspected`
- `Untested`
- `Human`

Use AI-code status to raise caution, not to replace direct security evidence.

### AI-Generated Code Risk Stats

- AI code introduces 2.74x more security vulnerabilities, 1.75x more logic errors, and 322% more privilege-escalation paths than human-written code (Veracode 2025: 45% of LLM samples failed OWASP Top 10).
- AI-generated CVEs rose from 6 (Jan 2026) to 35 (Mar 2026); estimated real count 5-10x higher given underreporting.
- 42% of all code is now AI-generated, making it the majority threat vector.
- DORA 2025: 31% more PRs merge unreviewed under AI adoption — automated AI-review-tool approval alone is insufficient for merge.
- AI co-authored commits leak secrets at ~2x baseline rate; 64% of leaked secrets from 2022 remain unrevoked in 2026 due to governance gaps (GitGuardian 2026).
