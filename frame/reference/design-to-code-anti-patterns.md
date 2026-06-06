# Design-to-Code Anti-Patterns & Quality Guardrails

Purpose: load this when validating extraction quality, documenting known gaps, or preventing design-to-code failure modes before handoff.

## Contents

- [The 70% Problem](#the-70-problem)
- [Anti-Patterns](#anti-patterns)
- [Quality Guardrails for Frame](#quality-guardrails-for-frame)
- [Component-First Extraction Principle](#component-first-extraction-principle)
- [W3C Design Tokens (DTCG) Standard](#w3c-design-tokens-dtcg-standard)
- [Sources](#sources)

## The 70% Problem

AI-generated code from design input typically reaches ~70% fidelity. The remaining 30% — which consumes 80% of effort — includes:
- Responsive behavior and breakpoints
- Dynamic state management (hover, loading, error, empty)
- Interactive elements (animations, transitions, drag-and-drop)
- Accessibility (ARIA roles, focus management, keyboard navigation)
- Performance optimization (lazy loading, code splitting)

**Frame implication:** Extraction output must explicitly flag what the 30% gap contains for downstream agents. Don't promise pixel-perfect; promise structured context that enables human-quality implementation.

---

## Anti-Patterns

### AP-1: Screenshot-Only Handoff

| Aspect | Detail |
|--------|--------|
| **What happens** | Passing only screenshots without structured context |
| **Result** | Downstream agents guess layout rules, hardcode pixel values, miss component boundaries |
| **Mitigation** | Always include `get_design_context` as primary; screenshots as supplementary visual reference |

### AP-2: Ignoring Code Connect Mappings

| Aspect | Detail |
|--------|--------|
| **What happens** | Extracting design data without checking existing Code Connect mappings |
| **Result** | Downstream agents create new components instead of reusing existing ones; drift and duplication |
| **Mitigation** | Always run `get_code_connect_map` in SURVEY phase; include snippets in PACKAGE output |

### AP-3: Flat Context Dump

| Aspect | Detail |
|--------|--------|
| **What happens** | Extracting everything from a Figma file without filtering or scoping |
| **Result** | Noisy payload exceeds context limits; downstream agents hallucinate components |
| **Mitigation** | Scope to specific pages/frames in SURVEY; structure per downstream agent using handoff templates |

### AP-4: Hardcoded Values Over Tokens

| Aspect | Detail |
|--------|--------|
| **What happens** | Extracting raw hex colors, pixel values instead of Figma Variable references |
| **Result** | Generated code uses magic numbers; no connection to design system; breaks on theme changes |
| **Mitigation** | Extract variables via `get_variable_defs`; map raw values to token names in handoff |

### AP-5: Silent Mapping Drift

| Aspect | Detail |
|--------|--------|
| **What happens** | Code Connect mappings go stale as designs or code evolve; no detection |
| **Result** | Outdated code snippets in PACKAGE output; wrong implementations |
| **Mitigation** | Check staleness in MAINTAIN phase; compare current props against mappings; flag >30-day-old mappings |

### AP-6: Ignoring Rate Budget

| Aspect | Detail |
|--------|--------|
| **What happens** | Calling high-cost tools without budget planning; especially on Professional/Organization (200/day) |
| **Result** | Extraction fails partway; incomplete handoff packages |
| **Mitigation** | Calculate budget in SURVEY; reserve 10% buffer; stop gracefully when budget < 10% |

---

## Quality Guardrails for Frame

### Pre-Extraction Checklist (SURVEY phase)

- [ ] MCP connection verified (`whoami`)
- [ ] Rate budget calculated for task scope
- [ ] Code Connect mappings checked (existing coverage known)
- [ ] Extraction scope bounded to specific pages/frames
- [ ] Downstream agent(s) identified → handoff format selected

### Pre-Handoff Validation (between PACKAGE and DELIVER)

- [ ] **Naming consistency**: Figma component names match Code Connect mapping names
- [ ] **Token coverage**: Raw values mapped to Figma Variables where available
- [ ] **Completeness**: No critical components missing from extraction
- [ ] **Code Connect inclusion**: Existing mappings included in handoff
- [ ] **Rate budget report**: Usage tracked and reported
- [ ] **Gap documentation**: Missing or incomplete data explicitly noted

### Post-Handoff Quality Signals

| Signal | Indicates |
|--------|-----------|
| Downstream agent asks for Figma URL | Insufficient structural context in handoff |
| Generated code uses hardcoded colors/spacing | Token extraction missing or not included in handoff |
| Duplicate components created | Code Connect mappings not checked or not included |
| Responsive issues in implementation | Auto Layout / constraints not extracted or poorly structured |

---

## Component-First Extraction Principle

**Key insight:** Map Figma components to existing codebase components rather than enabling generation of new code.

```
WRONG: Figma design → extract visuals → generate new component code
RIGHT: Figma design → check Code Connect → reuse existing component → fill props from design
```

When Code Connect mappings exist, Frame's handoff should emphasize:
1. Which existing component to use
2. What props to set (from Figma variant/property values)
3. What tokens to apply (from Figma Variables)
4. What's NOT mapped (new components that need creation)

---

## W3C Design Tokens (DTCG) Standard

The W3C Design Tokens Community Group spec reached first stable version (2025.10):
- Media type: `application/design-tokens+json`
- File extension: `.tokens` or `.tokens.json`
- Figma Variables supports native import/export in this format

**Frame implication:** When extracting variables for Muse handoff, note DTCG compatibility. Figma Variables → DTCG JSON is a supported export path for standards-compliant token pipelines.

---

## Sources

- The New Stack: "How a Component-First Approach Fixes Figma-to-Code" (2025)
- TFIR: "AI Code Quality in 2026: Guardrails" (2026)
- W3C DTCG: "Design Tokens Specification 1.0" (2025.10)
- Smashing Magazine: "Automating Design Systems" (2025)
- Supernova: "AI-Ready Design Systems" (2025)
- LogRocket: "How to Structure Figma Files for MCP" (2025)
- Builder.io: "AI Automation in Design Systems" (2025)
