# Canon LLM Fix Prompt Generation

**Purpose:** Canon-specific action verbs, suppression cases, template fields for the `## LLM Fix Prompt` block paired with every confirmed standards violation that has actionable, in-scope remediation.
**Read when:** Canon has assessed a requirement as `Partial` or `Non-compliant` and is handing remediation to Builder or an implementation specialist rather than emitting an audit-only gap report.

> Universal authoring rules and prompt structure: `_common/LLM_PROMPT_GENERATION.md`.
> This file documents only Canon-specific verbs, suppression cases, template fields.

## When Canon Emits a Fix Prompt vs Hands Off / Withholds

Canon's primary artifact is the compliance report (standard + version + section + evidence + verdict). The Fix Prompt is paired with each confirmed violation that has actionable in-scope remediation. Canon never implements; the prompt always names a downstream implementer.

| Situation | Action |
|-----------|--------|
| `Partial` / `Non-compliant` finding, generic remediation per the cited standard, scoped fix | Emit `REMEDIATE` prompt → Builder |
| Violation must remain (legacy, contractual, technical constraint) and the standard documents an exemption process | Emit `EXEMPT-WITH-RATIONALE` prompt → Builder + Scribe |
| Remediation requires an API shape, schema, or response-code change | Emit `BREAKING-REMEDIATE` prompt → Builder + Guardian + Launch |
| Underlying remediation blocked but a compensating control closes the risk window | Emit `MITIGATE` prompt → Builder |
| Standard's interpretation ambiguous; need spec authority or domain expert before code changes | Emit `INVESTIGATE-FURTHER` prompt → Domain expert OR Canon re-entry |
| Finding is OWASP/CWE source-level security work | **Suppress** — Sentinel owns the remediation prompt |
| Finding is i18n/CLDR/BCP-47 work | **Suppress** — Polyglot owns the remediation prompt |
| Finding requires privacy, cryptography, detection, monitoring, or delivery implementation | **Suppress** — Cloak, Crypt, Vigil, Beacon, Gear, or Sentinel owns its implementation prompt |
| Engagement is gap-analysis only (audit report without remediation scope) | **Withhold** — note "Fix prompt withheld per scope: gap-analysis only." |

The `CANON_TO_BUILDER` (or `_TO_PALETTE`, `_TO_GATEWAY`, `_TO_ZEN`) handoff carries a `fix_prompt` field; populate it whenever Canon does NOT suppress or withhold per the table above.

---

## Canon Action Verbs

Each fix prompt declares one verb at the top of `# Your task`.

| Verb | When to use | Receiving agent |
|------|-------------|----------------|
| `REMEDIATE` | Violation has clear remediation per the cited standard, scoped fix | Builder (or Polyglot for i18n, Sentinel for security-specific) |
| `EXEMPT-WITH-RATIONALE` | Violation must remain (constraints, legacy); document exemption per standard's exemption process | Builder + Scribe |
| `BREAKING-REMEDIATE` | Remediation requires breaking change (API shape, schema migration) | Builder + Guardian + Launch |
| `MITIGATE` | Compensating control while underlying remediation is blocked | Builder |
| `INVESTIGATE-FURTHER` | Standard interpretation ambiguous; need to consult the spec authority or a domain expert | Domain expert OR Canon re-entry with more standard context |

---

## Verb Selection Heuristic

```
Verdict == Non-compliant ─┬─ remediation per standard is scoped, no API shape change ──→ REMEDIATE
                          ├─ remediation requires API shape / schema / response-code change ──→ BREAKING-REMEDIATE
                          ├─ underlying fix blocked, compensating control available ──→ MITIGATE
                          └─ violation must remain (legacy / contract / hardware) ──→ EXEMPT-WITH-RATIONALE

Verdict == Partial ──────→ REMEDIATE (close the gap to full conformance)

Standard interpretation ambiguous (multiple defensible readings of the same SC / clause) ─→ INVESTIGATE-FURTHER
```

Tiebreakers:
- `REMEDIATE` is the default. Only escalate to `BREAKING-REMEDIATE` when the standard's prescribed remediation cannot be applied without changing a published surface — and always cross-link Launch for release coordination.
- `EXEMPT-WITH-RATIONALE` requires the cited standard to actually document an exemption mechanism (e.g., WCAG conformance scope statement, OpenAPI `x-` extension allowance, ISO 25010 quality-in-use trade-off). If no exemption mechanism exists, do not invent one — escalate to the user as an "Ask First" decision instead.
- `MITIGATE` always names the underlying remediation that is being deferred, with a re-assessment date — otherwise the compensating control becomes permanent debt.
- `INVESTIGATE-FURTHER` routes to the standard's authoritative source (W3C AGWG for WCAG, OpenAPI Initiative for OpenAPI, ISO TC for ISO standards). Do not let the receiving LLM resolve the ambiguity unilaterally.

---

## Canon-Specific Suppression Cases

Universal cases live in `_common/LLM_PROMPT_GENERATION.md`. Canon adds:

| Case | Reason | Note in report |
|------|--------|----------------|
| Canon hands off to Sentinel for security-specific (OWASP/CWE) violations requiring source-level fix | Sentinel owns security remediation prompts (multi-engine consensus, AUTH-FIX cross-link to Probe, etc.) | "Fix prompt suppressed — Sentinel owns security remediation prompt." |
| Canon hands off to Polyglot for i18n-specific (CLDR, BCP-47) violations | Polyglot owns i18n remediation prompts (locale-aware formatting, RTL, plural rules) | "Fix prompt suppressed — Polyglot owns i18n remediation prompt." |
| Canon hands off regulated-domain implementation | Cloak owns privacy engineering, Crypt owns key management, Vigil owns detection rules, Beacon owns monitoring, Gear owns delivery gates, Sentinel owns source-level security | "Fix prompt suppressed — [specialist] owns the implementation prompt." |
| Audit-only mode (gap report without remediation scope) | The engagement explicitly excludes remediation guidance | "Fix prompt withheld per scope: gap-analysis only." |
| Finding rated `Info` (observation only) | Not actionable | "Fix prompt withheld — finding is informational." |
| Standard version itself is unconfirmed (e.g., user did not pin OWASP edition) | Acting on an unpinned standard risks applying wrong criteria | "Fix prompt withheld — pin standard version before remediation." |

In all suppression cases, write a one-line note in the report explaining why the prompt is withheld. Silent omission breaks downstream expectations.

---

## Per-Violation Fix Prompt Template (Canon Fields)

Canon adds these Canon-specific blocks on top of the universal skeleton:

- `Standard cited` — standard name + version + section ID (e.g., "OWASP ASVS 4.0.3 V2.1.1", "WCAG 2.2 SC 1.4.3", "OpenAPI 3.1.0 §4.7.20")
- `Gap classification` — `missing` / `partial` / `non-conforming` / `over-conforming`
- `Remediation per standard` — the standard's prescribed remediation, verbatim if the standard specifies it
- `Exemption process` — for `EXEMPT-WITH-RATIONALE`, the standard's documented exemption mechanism (scope statement, `x-` extension, conformance-claim caveat, etc.)
- For `BREAKING-REMEDIATE` — `User-facing impact` and `Rollback plan`
- For `MITIGATE` — `Underlying remediation deferred` and `Re-assessment date`

````markdown
## LLM Fix Prompt

```text
# Your task
<VERB> the standards violation described below.

# Finding context
- Title: [brief description of the violation]
- Severity: [Critical | High | Medium | Low | Info]
- Confidence: [HIGH | MEDIUM | LOW] (Canon's assessment confidence)
- Standard cited: [standard name + version + section ID, e.g., "WCAG 2.2 SC 1.4.3"]
- Gap classification: [missing | partial | non-conforming | over-conforming]

# Violation
[What the requirement says vs what the codebase does]

Location: `<file>:<line>` in `<component / function>`

# Evidence
Current implementation:
```
[verbatim code / config / markup snippet]
```

Standard requirement (verbatim where possible):
> [exact quote from the cited section]

# Remediation per standard
[The standard's prescribed remediation — verbatim if specified, otherwise the closest in-spec approach]

Approach: [implementation strategy aligned with the standard]
Files to modify: [list with expected change per file]
Constraints:
- [coupling, side effect, or backward-compat note]
- [related sections of the same standard that must remain satisfied]

# [BREAKING-REMEDIATE only — User-facing impact]
- API / surface change: [yes/no — describe]
- Client breaking change: [yes/no — describe]
- Migration steps for clients: [list]

# [BREAKING-REMEDIATE only — Rollback plan]
- How to revert: [git revert SHA, feature flag toggle, etc.]
- Pre-deploy verification: [staging test, canary, etc.]
- Comms required: [release notes, advisory, etc.]

# [EXEMPT-WITH-RATIONALE only — Exemption process]
- Mechanism: [scope statement / x-extension / conformance caveat]
- Documentation location: [where the exemption is recorded]
- Review cadence: [when to re-evaluate the exemption]

# [MITIGATE only — Underlying remediation deferred]
- Underlying status: [why the standard-prescribed fix is blocked]
- Compensating control: [what this prompt actually changes]
- Re-assessment date: [when to revisit the deferred fix]

# Acceptance criteria
- [ ] Cited section now passes its conformance test
- [ ] Evidence (file:line) updated to reflect the fix
- [ ] No regression introduced in adjacent sections of the same standard
- [ ] [BREAKING-REMEDIATE] Migration path documented for clients
- [ ] [EXEMPT-WITH-RATIONALE] Exemption recorded per the standard's mechanism

# Ruled-out alternatives (do not revisit)
- [alternative 1] — eliminated because [evidence, e.g., violates SC X.Y.Z]
- [alternative 2] — eliminated because [evidence]

# What NOT to do
- Do not silence the symptom (suppress the lint rule, override the contrast checker, mark the test xfail)
- Do not invent an exemption the standard does not document
- Do not assess against an unpinned version of the standard
- Do not bundle unrelated standards changes into the same PR
- Do not expand scope beyond the cited files unless evidence demands it
```
````

---
