# JSDoc/TSDoc Style Guide

Purpose: Read this when Quill is writing JSDoc/TSDoc tags, examples, interface docs, or checking code-comment style quality.

Contents:
- `Essential Tags`: canonical `@param`, `@returns`, `@throws`, `@example`, `@deprecated`, and `@see` usage
- `Good vs Bad Examples`: signal-to-noise examples for API docs
- `Interface Documentation`: interface-level documentation patterns
- `Quill's Code Standards`: concise style constraints for durable comments

## Essential Tags

### @param - Document parameters
```typescript
/**
 * @param name - User's display name (max 50 chars)
 * @param options - Configuration options
 * @param options.timeout - Request timeout in ms (default: 5000)
 */
function createUser(name: string, options?: CreateOptions): User
```

### @returns - Document return value
```typescript
/**
 * @returns The created user object, or null if creation failed
 */
function createUser(name: string): User | null
```

### @throws - Document exceptions
```typescript
/**
 * @throws {ValidationError} When name is empty or too long
 * @throws {NetworkError} When API is unreachable
 */
function createUser(name: string): User
```

### @example - Show usage
```typescript
/**
 * @example
 * // Basic usage
 * const user = createUser('John');
 *
 * @example
 * // With options
 * const user = createUser('John', { timeout: 10000 });
 */
```

### @deprecated - Mark obsolete code
```typescript
/**
 * @deprecated Use `createUserV2` instead. Will be removed in v3.0.
 */
function createUser(name: string): User
```

### @see - Reference related items
```typescript
/**
 * @see {@link createUserV2} for the new API
 * @see https://docs.example.com/users for full documentation
 */
```

## Good vs Bad Examples

### BAD: Noise comment
```typescript
/**
 * Creates a user
 * @param name - the name
 * @returns user
 */
function createUser(name: string): User
```

### GOOD: Meaningful documentation
```typescript
/**
 * Creates a new user account and sends verification email.
 *
 * @param name - Display name (1-50 characters, no special chars)
 * @returns Newly created user with pending verification status
 * @throws {ValidationError} If name doesn't meet requirements
 *
 * @example
 * const user = await createUser('John Doe');
 * console.log(user.status); // 'pending_verification'
 */
function createUser(name: string): Promise<User>
```

## Interface Documentation

```typescript
/**
 * Represents a user in the system.
 *
 * @remarks
 * Users are created via {@link createUser} and must verify
 * their email before accessing protected resources.
 */
interface User {
  /** Unique identifier (UUID v4) */
  id: string;

  /** Display name (1-50 characters) */
  name: string;

  /**
   * Account status
   * - `pending`: Email not verified
   * - `active`: Full access
   * - `suspended`: Account disabled by admin
   */
  status: 'pending' | 'active' | 'suspended';

  /** ISO 8601 timestamp of account creation */
  createdAt: string;
}
```

## Quill's Code Standards

### Good Quill Code
```typescript
// GOOD: Explains the business rule (The WHY)
/**
 * Calculates tax using the regional rate table (updated annually).
 * Falls back to the standard rate when region is unrecognized.
 * @see https://example.com/docs/tax-rates for the rate table source
 */
const tax = calculateTax(amount, region);

// GOOD: Detailed TSDoc for library consumers
interface UserProps {
  /** unique ID from Auth0 (not database ID) */
  authId: string;
}
```

### Bad Quill Code
```typescript
// BAD: Explains the obvious (Noise)
const tax = calculateTax(amount); // calculates tax

// BAD: Vague or lying comment
// Todo: fix this later
const data = getData();
```

## TSDoc for AI Consumers (2026)

In 2026 the primary reader of an exported library symbol is **as often an AI coding agent as a human developer** — Cursor / Claude Code / Copilot / Windsurf pull TSDoc straight into the agent context when the user types the symbol. Two additions to the style guide:

1. **`@example` blocks earn their token cost.** The agent reproduces examples verbatim into the user's code — bias the example toward the common path, never an edge case. If a function has two genuinely common usage shapes, write two examples; if it has one, write one.
2. **Put the *return-value-on-failure* contract in `@returns` or `@throws`, not in prose.** The agent will pattern-match on `@returns`/`@throws` first when picking error-handling code. A README paragraph saying "may return null" without a structured tag is invisible to the agent.

```typescript
/**
 * Fetch a user by ID. Returns null when the user does not exist;
 * throws on network / auth failure.
 *
 * @param id - User UUID (validated client-side; rejects empty string)
 * @returns The user, or `null` if no user with that ID exists
 * @throws {NetworkError} On transport failure (retryable)
 * @throws {AuthError} When the caller's session is invalid (not retryable)
 *
 * @example
 * // Canonical usage
 * const user = await fetchUser(id);
 * if (user == null) return notFound();
 */
async function fetchUser(id: string): Promise<User | null>
```

The pattern above is **also** what `llms.txt` will surface to retrieval pipelines — keep the contract structured so both the IDE and the agent can act on it without re-parsing prose.
