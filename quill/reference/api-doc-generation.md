# API Documentation Generation

Purpose: Read this when Quill must document or generate API reference material for TypeScript libraries, REST APIs, or GraphQL schemas.

Contents:
- `TypeDoc (TypeScript)`: setup, config, and generation flow — current stable is **0.28.x** (requires TypeScript ≥ 5.0)
- `swagger-jsdoc (REST API)`: OpenAPI annotations and server wiring
- `GraphQL Schema Documentation`: schema descriptions and examples

Source: [TypeDoc Changelog](https://typedoc.org/documents/Changelog.html) · [TypeDoc 0.28 Tags](https://typedoc.org/documents/Tags.html)

## TypeDoc (TypeScript)

**Installation:**
```bash
npm install typedoc --save-dev
# TypeDoc 0.28+ requires TypeScript ≥ 5.0; dropped legacy TypeScript <5.0 support
```

**Configuration (typedoc.json):**
```json
{
  "entryPoints": ["src/index.ts"],
  "out": "docs",
  "exclude": ["**/*.test.ts", "**/node_modules/**"],
  "excludePrivate": true,
  "excludeProtected": true,
  "includeVersion": true,
  "readme": "README.md"
}
```

**Generate:**
```bash
npx typedoc
```

### TypeDoc 0.28 Key Tags

| Tag | Purpose |
|-----|---------|
| `@expand` | Inline the type's members wherever it is referenced (good for React prop interfaces) |
| `@inline` | Resolve type alias at the point of use |
| `@preventExpand` / `@preventInline` | Override inherited expansion on a per-symbol basis |
| `@disableGroups` | Disable grouping for a given reflection; use `@group none` / `@category none` to suppress headings |

**@expand example (React component props):**
```typescript
/**
 * @expand
 */
export interface ButtonProps {
  /** Accessible label */
  label: string;
  /** Click handler */
  onClick: () => void;
}
```

Source: [TypeDoc @expand](https://typedoc.org/documents/Tags._expand.html) · [TypeDoc @inline](https://typedoc.org/documents/Tags._inline.html)

### basePath and displayBasePath (0.28+)

- `basePath` — affects both relative link resolution and rendered source paths.
- `displayBasePath` — changes rendered base path for sources only, leaving link resolution untouched.

### ESM-only (0.28 breaking change)

TypeDoc 0.28 converted to ESM. If your `typedoc.json` plugins use CommonJS, migrate them to ESM or use dynamic `import()` wrappers.

## swagger-jsdoc (REST API)

**Installation:**
```bash
npm install swagger-jsdoc swagger-ui-express --save
```

**Configuration:**
```javascript
const swaggerJsdoc = require('swagger-jsdoc');

const options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'My API',
      version: '1.0.0',
      description: 'API documentation'
    },
    servers: [
      { url: 'http://localhost:3000' }
    ]
  },
  apis: ['./src/routes/*.ts']
};

const specs = swaggerJsdoc(options);
```

**Route Documentation:**
```typescript
/**
 * @openapi
 * /users/{id}:
 *   get:
 *     summary: Get user by ID
 *     tags: [Users]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: User found
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/User'
 *       404:
 *         description: User not found
 */
router.get('/users/:id', getUser);
```

## GraphQL Schema Documentation

```graphql
"""
A user in the system.
Users must verify their email before accessing protected resources.
"""
type User {
  "Unique identifier (UUID v4)"
  id: ID!

  "Display name (1-50 characters)"
  name: String!

  "User's email address (unique)"
  email: String!

  "Account creation timestamp"
  createdAt: DateTime!
}

"""
Input for creating a new user.
"""
input CreateUserInput {
  "Display name (required, 1-50 chars)"
  name: String!

  "Email address (required, must be unique)"
  email: String!
}
```
