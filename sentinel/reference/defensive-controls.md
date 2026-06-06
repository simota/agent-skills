# Defensive Controls & False Positive Management

Purpose: Apply established defensive controls during `SECURE`, and manage false positives during `FILTER`. Covers headers, validation, secrets, rate limiting, confidence scoring, delta scanning, and SARIF output.

---

## 1. Security Headers

| Header | Purpose | Priority |
|--------|---------|----------|
| `Content-Security-Policy` | Prevent XSS and injection | Critical |
| `Strict-Transport-Security` | Force HTTPS | Critical |
| `X-Content-Type-Options` | Prevent MIME sniffing | High |
| `X-Frame-Options` | Prevent clickjacking | High |
| `Referrer-Policy` | Control referrer leakage | Medium |
| `Permissions-Policy` | Disable unnecessary browser features | Medium |

Note: `X-XSS-Protection` is deprecated in modern browsers; CSP is the replacement.

### Next.js

```typescript
const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: [
      "default-src 'self'",
      "script-src 'self'", // Avoid 'unsafe-inline' 'unsafe-eval' in production
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: https:",
      "font-src 'self'",
      "connect-src 'self' https://api.example.com",
      "frame-ancestors 'none'",
      "base-uri 'self'",
      "form-action 'self'",
    ].join('; '),
  },
  { key: 'Strict-Transport-Security', value: 'max-age=31536000; includeSubDomains; preload' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'X-Frame-Options', value: 'DENY' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
];

module.exports = {
  async headers() {
    return [{ source: '/:path*', headers: securityHeaders }];
  },
};
```

### Express.js (`helmet`)

```typescript
import helmet from 'helmet';
app.use(helmet());
app.use(
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: ["'self'"], scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"], imgSrc: ["'self'", 'data:', 'https:'],
      connectSrc: ["'self'", 'https://api.example.com'], fontSrc: ["'self'"],
      objectSrc: ["'none'"], frameSrc: ["'none'"], upgradeInsecureRequests: [],
    },
  })
);
```

### CSP Violation Reporting

```typescript
// Use report-only mode during rollout, then switch to enforcing
{ key: 'Content-Security-Policy-Report-Only', value: "default-src 'self'; report-uri /api/csp-report" }
```

---

## 2. Input Validation

Boundary validation is mandatory. Prefer `Zod` when adding runtime schemas.

### Zod Schema Examples

```typescript
import { z } from 'zod';

const emailSchema = z.string().email().max(254);
const passwordSchema = z.string().min(8).max(128)
  .regex(/[A-Z]/).regex(/[a-z]/).regex(/[0-9]/).regex(/[^A-Za-z0-9]/);
const urlSchema = z.string().url().refine((url) => url.startsWith('https://'), 'Must use HTTPS');
const uuidSchema = z.string().uuid();

const userFormSchema = z.object({
  email: emailSchema,
  password: passwordSchema,
  name: z.string().min(1).max(100).trim(),
  age: z.number().int().min(13).max(120).optional(),
});
```

### Express Validation Middleware

```typescript
function validate(schema: ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse({ body: req.body, query: req.query, params: req.params });
    if (!result.success) {
      return res.status(400).json({
        error: 'Validation failed',
        details: result.error.issues.map((i) => ({ path: i.path.join('.'), message: i.message })),
      });
    }
    req.validated = result.data;
    next();
  };
}
```

---

## 3. Secret Management

Never hardcode secrets. Prefer environment variables with schema validation, then move to managed secret stores for production.

### Environment Variables

```typescript
const envSchema = z.object({
  API_KEY: z.string().min(1),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  NODE_ENV: z.enum(['development', 'production', 'test']),
});
const env = envSchema.parse(process.env);
```

### `.env` Hygiene

```bash
# .gitignore
.env
.env.local
.env.*.local
*.pem
*.key
```

### Secret Stores (Production)

- **AWS Secrets Manager**: `GetSecretValueCommand` with region config
- **HashiCorp Vault**: `vault.read('secret/data/path')`
- **Rotation**: Use TTL-based cache (5min default) with lazy refresh

---

## 4. Rate Limiting

Use stricter limits on auth and expensive endpoints.

```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 100, standardHeaders: true, legacyHeaders: false });
app.use(limiter);

const authLimiter = rateLimit({ windowMs: 60 * 60 * 1000, max: 5, skipSuccessfulRequests: true });
app.use('/api/auth/login', authLimiter);
```

For distributed systems, use Redis-backed stores (`rate-limit-redis`).

---

## 5. False Positive Management

Raw SAST alerts contain ~53% false positives. Without filtering, teams stop trusting the tool.

| FP rate | Assessment | Developer trust |
|---------|------------|-----------------|
| `> 40%` | Harmful | Very low |
| `20-40%` | Needs work | Low |
| `10-20%` | Target range | Medium-High |
| `< 10%` | Excellent | High |

### Framework-Aware Suppression

Suppress findings when framework-native protections are in place:

```text
sanitizer_functions: [sanitizeHtml, escapeSQL, purifyInput]
auth_middleware: [requireAuth, requireRole, requireApiKey]
csrf_protection: "Next.js built-in CSRF protection"
rate_limiting: "Handled at API Gateway"
```

### Delta Scanning

| Mode | Scope | Use when |
|------|-------|----------|
| PR-level | Changed files only | Fast review and merge gates |
| Periodic | Full repository | Weekly or explicit full audits |
| Baseline | Existing findings suppressed | New scanner rollout on legacy code |

### Confidence Scoring

| Factor | Weight |
|--------|--------|
| Multi-engine consensus | `+30%` |
| Known pattern match | `+20%` |
| Data-flow reachability | `+25%` |
| Framework mismatch | `-20%` |
| Test or mock location | `-30%` |

Tiers: `HIGH (≥80%)` → include immediately · `MEDIUM (50-79%)` → report with note · `LOW (<50%)` → suppress unless exhaustive

### Hybrid LLM+SAST Filtering

| Approach | Accuracy |
|----------|----------|
| Rules only (SAST) | 35.7% |
| LLM only | 65.5% |
| LLM + SAST (Hybrid) | 89.5% |

LLM excels at: cross-function data-flow reasoning, upstream validation recognition, exploit-feasibility assessment, framework security guarantee recognition.

Semgrep Assistant Memories achieves 85% FP reduction by learning from past triage decisions. SAST-Genius (Semgrep + fine-tuned LLM) achieves 91% FP reduction.

---

## 6. SARIF Output

Use SARIF when CI, GitHub Code Scanning, or IDE tooling needs machine-readable results.

```json
{
  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/main/sarif-2.1/schema/sarif-schema-2.1.0.json",
  "version": "2.1.0",
  "runs": [{
    "tool": { "driver": { "name": "Sentinel", "version": "1.0" } },
    "results": [{
      "ruleId": "SECRET-001",
      "level": "error",
      "message": { "text": "Hardcoded API key detected" },
      "locations": [{
        "physicalLocation": {
          "artifactLocation": { "uri": "src/config.ts" },
          "region": { "startLine": 42 }
        }
      }],
      "properties": { "confidence": 0.92, "owasp": "A07:2025" }
    }]
  }]
}
```

**Source:** [OWASP Top 10:2025](https://owasp.org/Top10/2025/) · [Semgrep Assistant Memories](https://semgrep.dev/blog/2025/why-ai-powered-memories-are-the-future-of-semgrep-sast/) · [SAST-Genius (arXiv)](https://arxiv.org/abs/2509.15433v2) · [InfoWorld: SAST + AI FP Reduction](https://www.infoworld.com/article/4093079/how-pairing-sast-with-ai-dramatically-reduces-false-positives-in-code-security.html)
