# Ripple Analysis Template

Combined analysis report including both vertical impact and horizontal consistency checks.

## Usage

Use this template (default) for comprehensive change analysis:
- "Analyze the impact of this change"
- "What should I know before implementing?"
- "Is this change safe to proceed?"

## Template

```markdown
# Ripple Analysis Report

## Executive Summary

**Change:** [Brief description of the proposed change]
**Requested By:** [Source - user request, Nexus chain, Scout investigation, etc.]
**Analysis Date:** YYYY-MM-DD

### Quick Assessment

| Metric | Value | Status |
|--------|-------|--------|
| **Risk Score** | X.X / 10 | 🟢 LOW / 🟡 MEDIUM / 🟠 HIGH / 🔴 CRITICAL |
| **Direct Impact** | X files | |
| **Transitive Impact** | Y files | |
| **Breaking Changes** | N | |
| **Pattern Violations** | M | |
| **Test Coverage** | P% | 🟢 Good / 🟡 Moderate / 🔴 Poor |

### Recommendation

**Verdict:** ✅ GO / ⚠️ CONDITIONAL GO / 🛑 NO-GO

**Rationale:** [1-2 sentences explaining the recommendation]

**Conditions (if CONDITIONAL GO):**
- [ ] [Condition 1]
- [ ] [Condition 2]

---

## 1. Change Scope

### What is Being Changed

| Aspect | Description |
|--------|-------------|
| **Target File(s)** | `src/path/to/file.ts` |
| **Change Type** | [New Feature / Modification / Refactoring / Deletion / Rename] |
| **Change Description** | [Detailed description] |

### Proposed Modification

```typescript
// Current State
[existing code or "N/A for new files"]

// Proposed State
[proposed code or description]
```

### Key Changes

1. **[Change 1]:** [Description]
2. **[Change 2]:** [Description]
3. **[Change 3]:** [Description]

---

## 2. Vertical Impact Analysis

### Dependency Overview

```
[Changed File]
       │
       ├──► [Direct 1] ──► [Trans 1.1]
       │
       ├──► [Direct 2] ──► [Trans 2.1]
       │                    └──► [Trans 2.2]
       │
       └──► [Direct 3]
```

### Affected Files Summary

| Level | Count | Files |
|-------|-------|-------|
| **0: Source** | 1 | `target-file.ts` |
| **1: Direct** | X | `dep1.ts`, `dep2.ts`, ... |
| **2: Transitive** | Y | `trans1.ts`, `trans2.ts`, ... |
| **Tests** | Z | `*.test.ts` files |

### Direct Dependents (Level 1)

| File | Import | Impact Type | Risk |
|------|--------|-------------|------|
| `src/dep1.ts` | `import { X }` | Function | Medium |
| `src/dep2.ts` | `import type { Y }` | Type | Low |
| `src/dep3.ts` | `import { Z }` | Function | High |

### Breaking Changes

| Export | Change | Affected Files | Severity |
|--------|--------|----------------|----------|
| `functionA` | Signature change | 5 | HIGH |
| `TypeB` | Property rename | 3 | MEDIUM |

**Breaking Change Details:**

#### Breaking Change 1: `functionA`

- **Current:** `functionA(param: string): Result`
- **Proposed:** `functionA(param: string, options?: Options): Result`
- **Impact:** All callers need review
- **Migration:** Non-breaking (new param is optional)

#### Breaking Change 2: `TypeB`

- **Current:** `{ oldProp: string }`
- **Proposed:** `{ newProp: string }`
- **Impact:** All type usages break
- **Migration:** Find-replace required

### Cascade Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Type errors | High | Medium | TypeScript will catch |
| Runtime errors | Low | High | Add tests |
| Build failure | Medium | High | CI will catch |

---

## 3. Horizontal Consistency Analysis

### Pattern Compliance Overview

| Category | Status | Issues |
|----------|--------|--------|
| Naming Conventions | ✅ | 0 |
| File Structure | ⚠️ | 1 |
| Code Patterns | ✅ | 0 |
| Type Definitions | ⚠️ | 2 |
| Error Handling | ✅ | 0 |

### Naming Convention Check

| Element | Convention | Proposed | Status |
|---------|------------|----------|--------|
| Function name | camelCase | `getData` | ✅ |
| Component name | PascalCase | `UserCard` | ✅ |
| Type name | PascalCase | `UserType` | ✅ |
| File name | kebab-case | `user-card.tsx` | ✅ |

### Pattern Compliance

#### Established Patterns

**1. Error Handling**
- **Codebase Pattern:** Try-catch with custom error class
- **Proposed:** ✅ Follows pattern
- **Reference:** `src/services/baseService.ts`

**2. Data Fetching**
- **Codebase Pattern:** React Query with standardized options
- **Proposed:** ✅ Follows pattern
- **Reference:** `src/hooks/useUser.ts`

**3. State Management**
- **Codebase Pattern:** Zustand with typed slices
- **Proposed:** ✅ Follows pattern
- **Reference:** `src/store/userStore.ts`

### Style Violations

| Location | Issue | Severity | Recommendation |
|----------|-------|----------|----------------|
| `file:23` | Missing return type | Low | Add explicit type |
| `file:45` | Unused import | Low | Remove import |

### Similar Files for Reference

| Purpose | File | Use For |
|---------|------|---------|
| Component structure | `src/components/Similar.tsx` | Layout, props pattern |
| Hook pattern | `src/hooks/useSimilar.ts` | Return type, errors |
| Service pattern | `src/services/similar.ts` | API integration |

---

## 4. Risk Assessment Matrix

### Risk Dimensions

| Dimension | Score (1-10) | Weight | Weighted | Justification |
|-----------|--------------|--------|----------|---------------|
| **Impact Scope** | X | 30% | X×0.3 | [N] files affected |
| **Breaking Potential** | Y | 25% | Y×0.25 | [N] breaking changes |
| **Pattern Deviation** | Z | 20% | Z×0.2 | [N] violations |
| **Test Coverage** | W | 15% | W×0.15 | [P]% covered |
| **Reversibility** | V | 10% | V×0.1 | [Easy/Moderate/Hard] |

### Calculation

```
Risk Score = (X×0.30) + (Y×0.25) + (Z×0.20) + (W×0.15) + (V×0.10)
           = [calculation]
           = X.X / 10
```

### Risk Level

| Score | Level | Meaning |
|-------|-------|---------|
| 1-3 | 🟢 LOW | Safe to proceed |
| 4-6 | 🟡 MEDIUM | Proceed with caution |
| 7-8 | 🟠 HIGH | Requires careful planning |
| 9-10 | 🔴 CRITICAL | Significant risk, consider alternatives |

**This Change:** [X.X] - [LEVEL]

---

## 5. Test Coverage Analysis

### Affected Code Coverage

| File | Current Coverage | Status |
|------|-----------------|--------|
| `target.ts` | 85% | 🟢 Good |
| `dependent1.ts` | 45% | 🟡 Moderate |
| `dependent2.ts` | 20% | 🔴 Poor |

### Tests Requiring Updates

| Test File | Reason | Priority |
|-----------|--------|----------|
| `target.test.ts` | Direct change | High |
| `dependent1.test.ts` | Uses changed function | Medium |
| `integration.test.ts` | End-to-end flow | High |

### Suggested New Tests

| Test Case | Why | Priority |
|-----------|-----|----------|
| `should handle null input` | New edge case | High |
| `should work with new options` | New functionality | High |
| `should maintain backward compat` | Breaking change guard | Medium |

---

## 6. Recommendations

### Action Items

#### Before Implementation

- [ ] Review breaking change migration paths
- [ ] Add tests for uncovered dependent code (via Radar)
- [ ] Confirm pattern compliance for [specific area]

#### During Implementation

- [ ] Follow patterns in `src/reference/similar.ts`
- [ ] Update all direct dependents
- [ ] Maintain backward compatibility where marked

#### After Implementation

- [ ] Run full test suite
- [ ] Verify type checking passes
- [ ] Update affected documentation

### Suggested Implementation Order

1. **Phase 1:** Update type definitions
2. **Phase 2:** Update core implementation
3. **Phase 3:** Update direct dependents
4. **Phase 4:** Run tests and verify
5. **Phase 5:** Update documentation

### Risk Mitigations

| Risk | Mitigation |
|------|------------|
| Breaking changes | Add compatibility layer |
| Low test coverage | Add tests via Radar first |
| Pattern deviation | Follow reference files |

---

## 7. Next Steps

### Recommended Agent Chain

| Step | Agent | Task |
|------|-------|------|
| 1 | **Radar** | Add tests for low-coverage areas |
| 2 | **Builder** | Implement changes with impact awareness |
| 3 | **Guardian** | Plan PR strategy |
| 4 | **Judge** | Review implementation |

### Handoff Information

**For Builder:**
- Direct files to modify: [list]
- Patterns to follow: [references]
- Breaking changes to handle: [list]
- Tests to update: [list]

**For Guardian:**
- Suggested PR scope: [description]
- Logical groupings: [groups]
- Breaking change notes: [for changelog]

---

## Appendix: Commands Used

```bash
# Dependency analysis
grep -rl "from.*target-module" src --include="*.ts"
npx madge --depends-on src/target.ts src/

# Pattern analysis
grep -E "pattern" src/**/*.ts
find src -name "*.ts" -exec grep -l "pattern" {} \;

# Coverage check
npx jest --coverage --collectCoverageFrom="src/target.ts"
```
```

## Quick Reference Checklist

### Completeness

- [ ] Executive summary with clear verdict
- [ ] Change scope clearly defined
- [ ] All direct dependents identified
- [ ] Transitive dependencies traced
- [ ] Breaking changes documented
- [ ] Pattern compliance checked
- [ ] Risk score calculated with evidence
- [ ] Test coverage gaps identified
- [ ] Recommendations are actionable
- [ ] Next steps defined

### Quality Gates

- [ ] Risk score justified with evidence
- [ ] All 5 risk dimensions scored
- [ ] Pattern violations have file:line references
- [ ] Recommendations include specific actions
- [ ] Handoff information is complete
