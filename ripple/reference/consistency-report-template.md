# Consistency Report Template

Horizontal consistency analysis report focusing on pattern compliance and naming conventions.

## Usage

Use this template when the focus is on:
- "Does this follow our patterns?"
- "Check consistency before implementing"
- "What conventions should this follow?"

## Template

```markdown
# Consistency Analysis Report

## Change Summary

**Proposed Change:** [Brief description]
**Scope:** [File(s) or module(s) being analyzed]
**Analysis Date:** YYYY-MM-DD

---

## Pattern Compliance Matrix

### Overall Status

| Category | Status | Issues |
|----------|--------|--------|
| Naming Conventions | ✅ / ⚠️ / ❌ | X issues |
| File Structure | ✅ / ⚠️ / ❌ | X issues |
| Code Patterns | ✅ / ⚠️ / ❌ | X issues |
| Type Definitions | ✅ / ⚠️ / ❌ | X issues |
| Error Handling | ✅ / ⚠️ / ❌ | X issues |

**Legend:**
- ✅ Compliant - Follows established patterns
- ⚠️ Minor Deviation - Acceptable with documentation
- ❌ Non-Compliant - Requires correction

---

## Naming Convention Analysis

### File Naming

| Pattern | Expected | Actual | Status |
|---------|----------|--------|--------|
| Components | PascalCase.tsx | [actual] | ✅/❌ |
| Hooks | use{Name}.ts | [actual] | ✅/❌ |
| Utils | camelCase.ts | [actual] | ✅/❌ |
| Types | {name}.types.ts | [actual] | ✅/❌ |
| Tests | {name}.test.ts | [actual] | ✅/❌ |

### Variable/Function Naming

| Pattern | Convention | Examples in Codebase | Proposed | Status |
|---------|------------|---------------------|----------|--------|
| Functions | camelCase | `fetchUser`, `handleClick` | [proposed] | ✅/❌ |
| Components | PascalCase | `UserProfile`, `LoginForm` | [proposed] | ✅/❌ |
| Constants | SCREAMING_SNAKE | `MAX_RETRIES`, `API_URL` | [proposed] | ✅/❌ |
| Interfaces | PascalCase (I-prefix?) | `User`, `IUserRepository` | [proposed] | ✅/❌ |
| Types | PascalCase | `UserDTO`, `ApiResponse` | [proposed] | ✅/❌ |
| Enums | PascalCase | `UserStatus`, `OrderState` | [proposed] | ✅/❌ |

### Naming Issues Found

| Location | Current | Expected | Severity |
|----------|---------|----------|----------|
| `file.ts:23` | `getData` | `fetchUserData` | Medium |
| `file.ts:45` | `IUser` | `User` (no I-prefix) | Low |

---

## File Structure Analysis

### Directory Pattern Compliance

**Expected Structure:**
```
src/
├── components/          # UI components
│   └── {ComponentName}/
│       ├── index.ts
│       ├── {ComponentName}.tsx
│       ├── {ComponentName}.test.tsx
│       └── {ComponentName}.styles.ts
├── hooks/               # Custom hooks
├── services/            # API services
├── types/               # Type definitions
└── utils/               # Utility functions
```

**Proposed Placement:**
```
[Where the new code should go]
```

**Compliance:** ✅ / ⚠️ / ❌

### Structure Issues

| Issue | Current | Expected | Action Required |
|-------|---------|----------|-----------------|
| [issue] | [current location] | [expected location] | [action] |

---

## Code Pattern Analysis

### Established Patterns in Codebase

#### 1. Error Handling Pattern

**Codebase Standard:**
```typescript
// Pattern found in: src/services/*.ts
try {
  const result = await operation();
  return { success: true, data: result };
} catch (error) {
  logger.error('Operation failed', { error });
  throw new CustomError('OPERATION_FAILED', error);
}
```

**Proposed Code:**
```typescript
[proposed error handling]
```

**Compliance:** ✅ / ⚠️ / ❌
**Notes:** [explanation if deviation]

#### 2. Data Fetching Pattern

**Codebase Standard:**
```typescript
// Pattern found in: src/hooks/use*.ts
const useData = () => {
  return useQuery({
    queryKey: ['key'],
    queryFn: fetchData,
    staleTime: 5 * 60 * 1000,
  });
};
```

**Proposed Code:**
```typescript
[proposed data fetching]
```

**Compliance:** ✅ / ⚠️ / ❌

#### 3. State Management Pattern

**Codebase Standard:**
```typescript
// Pattern found in: src/store/*.ts
[existing pattern]
```

**Proposed Code:**
```typescript
[proposed state management]
```

**Compliance:** ✅ / ⚠️ / ❌

#### 4. Component Structure Pattern

**Codebase Standard:**
```typescript
// Pattern found in: src/components/**/*.tsx
interface Props {
  // Props definition
}

export const Component: FC<Props> = ({ prop1, prop2 }) => {
  // Hooks at top
  const [state, setState] = useState();

  // Handlers
  const handleAction = () => {};

  // Effects
  useEffect(() => {}, []);

  // Render
  return <div />;
};
```

**Proposed Code Follows Pattern:** ✅ / ⚠️ / ❌

---

## Type Definition Analysis

### Type Pattern Compliance

| Aspect | Convention | Status |
|--------|------------|--------|
| Interface vs Type | Use `interface` for objects, `type` for unions/primitives | ✅/❌ |
| Optional Properties | Use `?` not `| undefined` | ✅/❌ |
| Readonly | Use `readonly` for immutable properties | ✅/❌ |
| Generics | Use descriptive names (T → TData) | ✅/❌ |
| Export Location | Types in dedicated files or colocated | ✅/❌ |

### Type Issues Found

| Location | Issue | Recommendation |
|----------|-------|----------------|
| `file.ts:12` | `any` type used | Define proper type |
| `file.ts:34` | Missing return type | Add explicit return type |

---

## Similar Implementations Reference

### Existing Code to Follow

| Feature | Reference File | Key Patterns |
|---------|---------------|--------------|
| Similar component | `src/components/Similar/Similar.tsx` | Structure, props pattern |
| Similar hook | `src/hooks/useSimilar.ts` | Return type, error handling |
| Similar service | `src/services/similarService.ts` | API pattern, types |

### Code Samples from Codebase

**Most Relevant Example:**
```typescript
// From: src/components/Example/Example.tsx
// This is the pattern to follow for [your change]

[relevant code snippet]
```

---

## Consistency Score (Horizontal)

| Factor | Score (1-10) | Justification |
|--------|--------------|---------------|
| **Naming Compliance** | X | [N violations found] |
| **Structure Compliance** | Y | [placement issues] |
| **Pattern Compliance** | Z | [N pattern deviations] |
| **Type Compliance** | W | [N type issues] |

**Horizontal Consistency Score:** X.X / 10

---

## Violations Summary

### Critical (Must Fix Before Implementation)

| # | Location | Issue | Required Action |
|---|----------|-------|-----------------|
| 1 | `file:line` | [description] | [action] |

### Warning (Should Fix)

| # | Location | Issue | Recommended Action |
|---|----------|-------|-------------------|
| 1 | `file:line` | [description] | [action] |

### Info (Consider Fixing)

| # | Location | Issue | Suggestion |
|---|----------|-------|------------|
| 1 | `file:line` | [description] | [suggestion] |

---

## Recommendations

### Pattern Alignment Actions

1. **Naming:**
   - [ ] Rename [X] to follow [convention]

2. **Structure:**
   - [ ] Move [file] to [location]

3. **Code Patterns:**
   - [ ] Apply [pattern] from [reference file]

4. **Types:**
   - [ ] Define proper types for [X]

### Reference Files to Study

Before implementing, review these files for consistency:
1. `src/path/to/similar1.ts` - For [pattern]
2. `src/path/to/similar2.ts` - For [pattern]

---

## Commands Used

```bash
# Check naming patterns
grep -E "function [A-Z]" src/ -r --include="*.ts"

# Find similar implementations
grep -rl "similar pattern" src --include="*.ts" | head -5

# Count pattern usage
grep -c "pattern" src/**/*.ts | sort -t: -k2 -rn | head -10
```
```

## Quick Reference Checklist

- [ ] Naming conventions verified against codebase
- [ ] File structure matches project organization
- [ ] Code patterns compared to existing similar files
- [ ] Type definitions follow project standards
- [ ] All violations documented with severity
- [ ] Reference files identified for guidance
