# AI-Generated Code Scrutiny (Judge)

> Elevated review playbook for AI-authored code: detection signals, defect catalog, FP-rate ceilings, and Judge-side enforcement rules.

Read this when reviewing PRs where ≥50% of LOC is AI-generated (Copilot/Cursor/Claude artifacts) or when the user invokes the `AI code review` flow.

---

## 1. Why Elevated Scrutiny

Empirical 2025–2026 data justify treating AI-generated code as junior-developer work requiring supervision:

| Signal | Magnitude | Source |
|--------|-----------|--------|
| AI code total issue rate vs human | **1.7x** | CodeRabbit 470-PR study |
| Logic errors | **+75%** (1.75x) | CodeRabbit |
| Security vulnerabilities | **+2.74x** | Veracode 2025 (100+ LLMs) |
| Performance inefficiencies | **+8x** | Veracode 2025 |
| OWASP Top 10 failure rate | **45%** | Veracode 2025 |
| Secret leak rate (AI commits vs baseline) | **3.2% vs 1.5%** | Industry benchmark |
| Commit velocity (AI-assisted dev vs baseline) | **3-4x** | Fortune 50 enterprise data |
| Security finding intro rate | **10x** | Fortune 50 enterprise data |
| Review time penalty above 40% AI ratio | **+91%** | Industry analysis |
| Bug rate above 40% AI ratio | **+9%** | Industry analysis |
| AI-attributable CVEs (single month) | **35 (Mar 2026)** | Georgia Tech Vibe Security Radar |

**Sustainable AI-code ratio: 25–40%.** Above 40%, flag the repo and require additional review depth.

---

## 2. AI Defect Top 8 (canonical detector list)

Run all 8 on any PR whose author is an AI agent or whose AI-generated LOC ≥50%.

1. **Hallucinated imports / slopsquatting** — module names that look real but don't exist in the registry.
2. **Missing null/undefined checks at boundaries** — absent guards on external input.
3. **Over-broad type assertions** — `as any`, `# type: ignore`, blanket `unknown` casts.
4. **Absent edge-case handling** — happy path only; empty list, zero, max, negative ignored.
5. **N+1 query patterns** — AI's natural for-loop style hides DB round-trips.
6. **Repeated near-identical code blocks** — anti-DRY, copy-paste-with-tweak.
7. **try/catch wrapping every call** — defensive blanket catches that swallow errors.
8. **Tests asserting `called()` not `contract holds`** — mock-shape tests with no behavioral assertion.

Source: arxiv.org/html/2512.05239v1 ; coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report.

---

## 3. AI-Generated Code Indicators (detection signals)

When any of these appear during NORMALIZE/CLUSTER, escalate review depth and cross-reference `ai-review-patterns.md`.

- Repetitive boilerplate without variation
- Missing edge cases and error boundaries
- Overly verbose null checks (every call defensively wrapped)
- Generic variable names (`data`, `result`, `temp`)
- Lack of domain-specific validation
- Security shortcuts — hardcoded values, permissive CORS, credential exposure
- Performance anti-patterns — N+1, missing pagination, synchronous blocking
- Unnecessary abstractions / wrong pattern selection
- **Absent defenses** — missing input validation, missing sanitization, missing parameterized queries
- **Plausible Hallucination** — real-looking API calls / imports / internal classes that don't exist in the codebase

Top AI vulnerability categories:
- XSS — **86% failure rate**
- Log injection — **88% failure rate**
- Injection-class weaknesses — **33.1%** of all confirmed AI-code vulnerabilities (SSRF/CWE-918 leading; AppSec Santa 2026, 534 samples across 6 LLMs)

---

## 4. Absence Detection

LLMs systematically miss **absent** defenses (vs present-code issues). At GROUND, explicitly verify the presence of:
- Input validation at every external boundary
- Output encoding / parameterized queries
- URL scheme allowlists for redirects
- Error handling on all I/O paths

Absent-defense findings get severity bump (MEDIUM → HIGH) when in auth / payments / data-access paths.

---

## 5. Hallucination Verification

For every AI-generated import, API call, or class reference:
1. Verify module exists in the lockfile / package registry.
2. Verify symbol exists in the imported module.
3. Verify internal class exists in the codebase via `grep` / `Glob`.

If any check fails → finding class = `hallucination` → severity HIGH → suppress LLM Fix Prompt and route to Builder with "verify before fixing" note.

---

## 6. FP-Rate Ceilings (category-specific, 2026 targets)

Industry-converging ceilings the FILTER stage must enforce. Drop any class whose recent FP rate exceeds the ceiling for **3 consecutive runs** and surface a category-degradation warning instead of silently emitting noise.

| Category | FP-Rate Ceiling |
|----------|-----------------|
| Security | < 3% |
| Bug-risk | < 3% |
| Maintainability | < 5% |
| Style | < 2% |

Public benchmark spread (operating points, not ceilings):
- Greptile: 82% catch rate / 11 FP per run.
- CodeRabbit: 44% catch rate / 2 FP per run.

Source: codeant.ai/blogs/ai-code-review-false-positives ; greptile.com/benchmarks.

---

## 7. Post-Merge Follow-Up

AI-generated code creates hidden technical debt that surfaces 30–90 days post-merge. For AI-heavy PRs (>50% AI-generated LOC), recommend a scheduled follow-up review at the **30-day mark**.

For safety-critical domains (medical, autonomous vehicle, critical infrastructure), EU AI Act high-risk transparency rules apply — flag for compliance review.
