# Type Improvement Strategies

Purpose: Read this when Quill must replace `any`, add safer types, introduce type guards, or report type-coverage improvements.

Contents:
- `any → Proper Type Migration Path`: audit, categorize, and replace workflow
- `Type Guard Patterns`: narrowing techniques for uncertain values
- `Union & Intersection Types`: expressive replacement patterns
- `Type Coverage Score`: target thresholds and interpretation
- `Any Type Audit Report`: reusable audit output structure
- `Utility Type Cheat Sheet`: reusable helpers for safer API surfaces

## any → Proper Type Migration Path

### Step 1: Audit

```bash
# Find all any types
grep -rn ': any\|: any\[\]\|as any\|<any>' src/ --include='*.ts' --include='*.tsx'

# Count by file
grep -rnl ': any' src/ --include='*.ts' | while read f; do
  echo "$(grep -c ': any' "$f") $f"
done | sort -rn
```

### Step 2: Categorize

| Category | Example | Strategy |
|----------|---------|----------|
| API Response | `fetch().then(r => r.json() as any)` | Define response interface |
| Function param | `function process(data: any)` | Use generics or specific type |
| Library type | `thirdPartyLib.method() as any` | Check @types package or use `unknown` |
| Legacy code | `const x: any = legacyFunction()` | Wrap with typed adapter |
| Quick hack | `(window as any).customProp` | Extend global types |

### Step 3: Replace Patterns

#### Pattern: API Response
```typescript
// Before
const data: any = await response.json();

// After
interface UserResponse {
  id: string;
  name: string;
  email: string;
}
const data: UserResponse = await response.json();
```

#### Pattern: Generic Function
```typescript
// Before
function first(arr: any[]): any {
  return arr[0];
}

// After
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}
```

#### Pattern: Event Handler
```typescript
// Before
function handleChange(e: any) {
  setValue(e.target.value);
}

// After
function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
  setValue(e.target.value);
}
```

#### Pattern: Dynamic Object
```typescript
// Before
const config: any = {};

// After
interface AppConfig {
  apiUrl: string;
  timeout: number;
  debug?: boolean;
}
const config: AppConfig = {
  apiUrl: 'https://api.example.com',
  timeout: 5000,
};
```

#### Pattern: Third-Party Library
```typescript
// Before
const result: any = externalLib.process(data);

// After (Option A: Install types)
// npm install -D @types/external-lib

// After (Option B: Declare module)
declare module 'external-lib' {
  export function process(data: InputType): OutputType;
}

// After (Option C: Wrap with adapter)
function processData(data: InputType): OutputType {
  return externalLib.process(data) as OutputType;
}
```

## Type Guard Patterns

### Basic Type Guard
```typescript
function isString(value: unknown): value is string {
  return typeof value === 'string';
}
```

### Object Type Guard
```typescript
interface User {
  id: string;
  name: string;
}

function isUser(obj: unknown): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'name' in obj &&
    typeof (obj as User).id === 'string' &&
    typeof (obj as User).name === 'string'
  );
}
```

### Discriminated Union Guard
```typescript
type Result<T> =
  | { status: 'success'; data: T }
  | { status: 'error'; error: string };

function isSuccess<T>(result: Result<T>): result is { status: 'success'; data: T } {
  return result.status === 'success';
}
```

## Union & Intersection Types

```typescript
// Union: Either type
type Result<T> = Success<T> | Failure;

// Intersection: Combined type
type AdminUser = User & { permissions: string[] };

// Discriminated Union (recommended)
type ApiResult<T> =
  | { status: 'success'; data: T }
  | { status: 'error'; error: string };
```

## Type Coverage Score

```
Type Coverage = (Typed Symbols / Total Symbols) × 100

Target: 95%+ for production code
```

## Any Type Audit Report

```markdown
### Type Audit: [Module Name]

**Current Coverage**: X.X%
**Target**: 95%

| File | `any` Count | Severity | Notes |
|------|-------------|----------|-------|
| api/client.ts | 5 | High | API response types |
| utils/helpers.ts | 2 | Medium | Legacy code |
| types/legacy.ts | 8 | Low | Deprecated, to be removed |

**Total `any` types**: 15
**Estimated effort**: 2-3 hours

**Priority Replacements**:
1. `api/client.ts:42` - `response: any` → `ApiResponse<User>`
2. `api/client.ts:56` - `data: any` → `RequestPayload`
3. `utils/helpers.ts:12` - `config: any` → `AppConfig`

**Blocked Items**:
- `types/legacy.ts` - Depends on deprecated API, defer until migration
```

## Utility Type Cheat Sheet

| Utility | Purpose | Example |
|---------|---------|---------|
| `Partial<T>` | All props optional | `Partial<User>` for updates |
| `Required<T>` | All props required | `Required<Config>` for validation |
| `Pick<T, K>` | Select specific props | `Pick<User, 'id' \| 'name'>` |
| `Omit<T, K>` | Exclude specific props | `Omit<User, 'password'>` |
| `Record<K, V>` | Key-value map | `Record<string, User>` |
| `Readonly<T>` | Immutable | `Readonly<Config>` |
| `NonNullable<T>` | Remove null/undefined | `NonNullable<string \| null>` |
| `ReturnType<F>` | Function return type | `ReturnType<typeof fetch>` |
| `Parameters<F>` | Function param types | `Parameters<typeof handler>` |
| `Awaited<T>` | Unwrap Promise | `Awaited<Promise<User>>` → `User` |
| `NoInfer<T>` | Block inference at call site (TS 5.4+) | Prevent secondary params from widening the inferred type |

Source: [TypeScript Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html) · [NoInfer — TS 5.4](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-4.html)

## satisfies Operator (TS 4.9+)

Use `satisfies` to validate structure while preserving literal types. Prefer it over `as` casts for config objects, route maps, and theme tokens:

```typescript
// Before (as cast erases literal types)
const routes = {
  home: '/',
  about: '/about',
} as Record<string, string>;

// After (satisfies validates structure; literals preserved)
const routes = {
  home: '/',
  about: '/about',
} satisfies Record<string, string>;

// routes.home is still '/' not string
```

Source: [TypeScript 4.9 — satisfies operator](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html)

## Branded Types (Nominal Typing)

Use branded types to prevent accidental value mix-ups at the type level without runtime overhead:

```typescript
type UserId = string & { __brand: 'UserId' };
type OrderId = string & { __brand: 'OrderId' };

function assertUserId(id: string): UserId {
  // validate here
  return id as UserId;
}

// Compiler rejects passing OrderId where UserId is expected
function getUser(id: UserId): User { ... }
```

Source: [TypeScript Do's and Don'ts](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html)
