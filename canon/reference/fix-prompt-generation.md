# Canon LLM Fix Prompt Generation

**Purpose:** Canon-specific action verbs, suppression cases, template fields, and worked example for the `## LLM Fix Prompt` block paired with every confirmed standards violation that has actionable, in-scope remediation.
**Read when:** Canon has assessed a requirement as `Partial` or `Non-compliant` and is handing the remediation off to Builder (or Polyglot / Sentinel / Oath for domain-owned cases) rather than emitting an audit-only gap report.

> Universal authoring rules and prompt structure: `_common/LLM_PROMPT_GENERATION.md`.
> This file documents only Canon-specific verbs, suppression cases, template fields, and an example.

## Contents

- When Canon emits a Fix Prompt vs hands off / withholds
- Canon action verbs
- Verb selection heuristic
- Canon-specific suppression cases
- Per-violation fix prompt template (Canon-specific fields)
- Worked example

---

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
| Finding is GDPR/HIPAA/SOC2 compliance work | **Suppress** — Oath (or Sentinel for security-overlap) owns the remediation prompt |
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
| Canon hands off to Sentinel/Oath for compliance-mandated changes (GDPR/HIPAA) | Oath owns regulatory remediation prompts; Sentinel for security-overlap | "Fix prompt suppressed — [Oath/Sentinel] owns compliance remediation prompt." |
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

## Worked Example (REMEDIATE)

**Scenario:** A primary call-to-action button uses light-grey text (`#999`) on a white background (`#fff`), giving a contrast ratio of 2.85:1 — failing WCAG 2.2 SC 1.4.3 (Contrast Minimum, Level AA, requires ≥ 4.5:1 for normal text).

````markdown
## LLM Fix Prompt

```text
# Your task
REMEDIATE the standards violation described below.

# Finding context
- Title: Primary CTA button text fails WCAG 2.2 contrast minimum
- Severity: High
- Confidence: HIGH (measured contrast ratio, deterministic)
- Standard cited: WCAG 2.2 SC 1.4.3 Contrast (Minimum), Level AA
- Gap classification: non-conforming

# Violation
SC 1.4.3 requires a contrast ratio of at least 4.5:1 for normal text against
its background. The primary CTA button renders text `#999999` on background
`#ffffff`, producing a measured ratio of 2.85:1 — below the AA threshold.

Location: `src/components/PrimaryButton.tsx:18` in `<PrimaryButton>` (token
`color.text.muted` consumed at line 18; token defined at
`src/styles/tokens.css:42`)

# Evidence
Current implementation:
```
.primary-button {
  color: var(--color-text-muted); /* #999999 */
  background: var(--color-bg-default); /* #ffffff */
}
```

Standard requirement (verbatim):
> "The visual presentation of text and images of text has a contrast ratio of
> at least 4.5:1, except for the following: Large Text … Incidental … Logotypes."
> — WCAG 2.2, Success Criterion 1.4.3

The button text is normal-weight 14px — none of the exceptions (Large Text,
Incidental, Logotypes) apply.

# Remediation per standard
Approach: Raise the foreground color until the measured contrast against the
button background is ≥ 4.5:1. The design system already defines
`color.text.default` (`#1a1a1a`) which yields 17.4:1 against `#ffffff`. Replace
the muted token usage on the primary CTA with the default text token; keep the
muted token for genuinely de-emphasized contexts where SC 1.4.3 exceptions
apply (large text ≥ 18pt, incidental UI).

Files to modify:
- src/components/PrimaryButton.tsx — swap `color.text.muted` for `color.text.default` at line 18
- src/components/PrimaryButton.test.tsx — add an axe-core assertion that the rendered button has no SC 1.4.3 violations
- src/styles/tokens.css — add an inline comment on `color.text.muted` warning that it must not be used for SC 1.4.3-bound text

Constraints:
- Do NOT lower the contrast threshold or switch the assertion to AAA (7:1) —
  the fix must satisfy AA without overshooting and constraining the design system.
- Adjacent SCs (1.4.11 Non-Text Contrast, 2.4.7 Focus Visible) must remain
  satisfied — verify focus ring and border still meet 3:1 against background.
- Do not change the button background; the design system reserves white
  backgrounds for primary surfaces.

# Acceptance criteria
- [ ] Rendered primary CTA measures contrast ≥ 4.5:1 (verify with axe-core or @adobe/leonardo-contrast-colors)
- [ ] PrimaryButton.test.tsx asserts no SC 1.4.3 violations via axe-core
- [ ] SC 1.4.11 (Non-Text Contrast) and SC 2.4.7 (Focus Visible) still pass on the same component
- [ ] Token `color.text.muted` carries an inline comment restricting its use
- [ ] No new test failures in src/components/

# Ruled-out alternatives (do not revisit)
- Adding a darker background to the button — eliminated: the design system
  reserves white backgrounds for primary surfaces; changing it cascades to
  other components.
- Marking the text as "Large Text" by upsizing to 18pt — eliminated: the
  visual hierarchy treats this as a body-weight CTA; upsizing would conflict
  with the design system's type scale.
- Suppressing the axe-core rule for this component — eliminated: SC 1.4.3 is a
  Level AA conformance requirement; suppression would be a false-conformance
  claim under WCAG 2.2 §5 Conformance Requirements.
- Switching to AAA (7:1) for everything — eliminated: out of scope; the
  engagement targets AA conformance, and AAA imposes design constraints the
  user has not opted into.

# What NOT to do
- Do not silence the symptom by suppressing the axe-core rule, lowering the
  threshold in the test, or marking the test xfail
- Do not invent a "decorative text" exemption — WCAG 2.2 SC 1.4.3 lists its
  exceptions exhaustively (Large Text, Incidental, Logotypes); this button
  text is none of those
- Do not assess against an unpinned WCAG version — the cited fix is bound to
  WCAG 2.2 SC 1.4.3 specifically
- Do not bundle unrelated a11y changes (focus order, alt text, ARIA labels)
  into the same PR
- Do not expand scope to other components unless they share the same token
  usage and same conformance gap
```
````

This prompt is self-contained: a coding LLM (or Palette, if the design-system token itself needs revisiting) can act on it without seeing the rest of the Canon report.
