# LENS Framework Reference

## SCOPE → SURVEY → TRACE → CONNECT → REPORT

---

## 1. SCOPE Phase (Understand the Question)

Decompose the question and identify the investigation type.

```yaml
INVESTIGATION_SCOPE:
  original_question: "[User's exact question]"
  investigation_type:
    - EXISTENCE: "Does X exist in this codebase?"
    - FLOW: "How does X work from A to B?"
    - STRUCTURE: "What is the architecture of X?"
    - DATA: "Where does data X originate and go?"
    - CONVENTION: "What patterns/tools does this project use?"
  search_targets:
    keywords: ["[domain terms]", "[technical terms]"]
    file_patterns: ["[likely file patterns]"]
    entry_points: ["[routes, handlers, main files]"]
  scope_boundary:
    include: ["[directories/modules to search]"]
    exclude: ["[node_modules, build, etc.]"]
  expected_output:
    format: "[existence_check | flow_diagram | structure_map | data_trace]"
    depth: "[surface | moderate | deep]"
```

---

## 2. SURVEY Phase (Get the Lay of the Land)

### Step 2.1: Project Structure Scan
```bash
# Directory structure overview
ls -la
cat package.json  # or equivalent manifest
cat README.md     # if exists

# Identify framework/patterns
# Look for: src/, app/, lib/, routes/, controllers/, services/
```

### Step 2.2: Entry Point Identification

| Entry Point Type | How to Find |
|-----------------|-------------|
| HTTP Routes | `grep -r "router\|app.get\|app.post\|@Get\|@Post"` |
| CLI Commands | `grep -r "command\|program\|yargs\|commander"` |
| Event Handlers | `grep -r "on(\|addEventListener\|subscribe\|@EventHandler"` |
| Cron/Batch | `grep -r "cron\|schedule\|@Scheduled"` |
| Exports (Library) | Entry in `package.json` main/exports |
| UI Components | `grep -r "export default function\|export const.*=.*=>"` in components/ |

### Step 2.3: Technology Stack Detection
```yaml
TECH_STACK:
  language: "[TypeScript/Python/Go/etc.]"
  framework: "[Next.js/Express/Django/etc.]"
  orm_db: "[Prisma/TypeORM/SQLAlchemy/etc.]"
  test_framework: "[Jest/Vitest/pytest/etc.]"
  build_tool: "[webpack/vite/turbopack/etc.]"
  package_manager: "[npm/yarn/pnpm/etc.]"
  key_dependencies:
    - name: "[package]"
      purpose: "[what it does]"
```

---

## 3. TRACE Phase (Follow the Flow)

### Pattern A: Execution Flow Trace

```yaml
EXECUTION_FLOW:
  trigger: "[HTTP request / CLI command / Event / etc.]"
  steps:
    - step: 1
      location: "src/routes/auth.ts:15"
      action: "POST /api/auth/login received"
      next: "src/controllers/authController.ts:42"

    - step: 2
      location: "src/controllers/authController.ts:42"
      action: "Validate request body"
      next: "src/services/authService.ts:28"

    - step: 3
      location: "src/services/authService.ts:28"
      action: "Check credentials against DB"
      calls:
        - "src/repositories/userRepo.ts:15"
        - "src/utils/hash.ts:8"
      next: "src/services/authService.ts:45"

    - step: 4
      location: "src/services/authService.ts:45"
      action: "Generate JWT token"
      output: "{ token: string, expiresIn: number }"

  error_paths:
    - condition: "Invalid credentials"
      location: "src/services/authService.ts:35"
      action: "Throw UnauthorizedError"
      handler: "src/middleware/errorHandler.ts:20"
```

### Pattern B: Data Flow Trace

```yaml
DATA_FLOW:
  data_entity: "[e.g., User, Order, Payment]"
  lifecycle:
    creation:
      location: "src/services/userService.ts:12"
      input: "[form data, API payload]"
      validation: "src/validators/userValidator.ts:5"

    storage:
      location: "src/repositories/userRepo.ts:20"
      target: "[PostgreSQL via Prisma]"
      schema: "prisma/schema.prisma:45"

    retrieval:
      locations:
        - "src/repositories/userRepo.ts:35 (findById)"
        - "src/repositories/userRepo.ts:50 (findByEmail)"

    transformation:
      - location: "src/mappers/userMapper.ts:8"
        input_type: "UserEntity"
        output_type: "UserDTO"
        purpose: "Strip sensitive fields for API response"

    output:
      - "API response (src/controllers/userController.ts:30)"
      - "Email service (src/services/emailService.ts:15)"
```

### Pattern C: Dependency Trace

```yaml
DEPENDENCY_TRACE:
  target: "[module/file/function]"
  depends_on:
    - "src/utils/config.ts (configuration)"
    - "src/db/connection.ts (database)"
  depended_by:
    - "src/controllers/authController.ts"
    - "src/middleware/authMiddleware.ts"
  external:
    - "jsonwebtoken (JWT generation)"
    - "bcrypt (password hashing)"
```

---

## 4. CONNECT Phase (Build the Big Picture)

```yaml
CONNECTION_MAP:
  modules:
    - name: "Authentication"
      files: ["src/auth/*"]
      responsibility: "User identity verification and token management"
      interfaces:
        exposed: ["login(), logout(), verifyToken()"]
        consumed: ["UserRepository.findByEmail()"]

    - name: "Authorization"
      files: ["src/middleware/auth*"]
      responsibility: "Route protection and permission checking"
      interfaces:
        exposed: ["authMiddleware(), requireRole()"]
        consumed: ["AuthService.verifyToken()"]

  relationships:
    - from: "Authentication"
      to: "Authorization"
      type: "provides token verification"

  boundaries:
    - "Authentication ↔ Database: via UserRepository"
    - "Authentication ↔ External: JWT library"

  conventions_found:
    - pattern: "Repository pattern for DB access"
      evidence: "src/repositories/*.ts"
    - pattern: "Service layer for business logic"
      evidence: "src/services/*.ts"
    - pattern: "DTO mapping for API responses"
      evidence: "src/mappers/*.ts"
```

---

## 5. REPORT Phase (Deliver Understanding)

Output investigation results as a structured report. Use the appropriate output format from `output-formats.md` based on investigation type:
- Simple existence checks → Quick Answer
- Flow/structure questions → Investigation Report
- Onboarding requests → Onboarding Report
