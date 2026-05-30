# Learning-Loop Kit — Instance Registry

Tracks every kit instantiated from this base. One row per instance.

## Rendered (shipped)

| # | Kit | Slug | Signal → Rule | Config | Status |
|---|-----|------|---------------|--------|--------|
| 1 | Design Feedback | `design-feedback` | UI/UX feedback → design principles (core + frontend/ios/android) | `instances/design-feedback.config.md` | **shipped — predecessor / non-strict render** (`_templates/design-feedback-kit/`; uses `Scope:`/`Token:` instead of base `Layer:`/`Check:` — see config) |

## Proposed (candidate domains — not yet rendered)

Ranked by fit with the loop pattern. Render on demand via `README.md` → "Instantiate".

| Kit | Slug | Signal → Rule | ANALYZE / ENFORCE / GATE skills | Machine encoding | Fit |
|-----|------|---------------|----------------------------------|------------------|-----|
| Review Knowledge | `review-knowledge` | PR review comments → coding conventions | judge, zen / artisan, builder / guardian, judge | lint rule (Semgrep/ESLint) | ★★★ |
| Incident Learning | `incident-learning` | incidents / postmortems → reliability rules + runbook | beacon, triage, omen / beacon, builder / guardian, beacon | alert rule + SLO | ★★★ |
| Secure-Coding Rules | `secure-coding` | vuln / CVE / audit findings → banned patterns + secure-impl rules | sentinel, chain, vigil / sentinel, builder / guardian, sentinel | lint rule (Semgrep) | ★★★ |
| Voice & Tone | `voice-tone` | copy feedback → UX-writing / brand-voice rules | prose, canon, tone / prose, artisan / guardian, canon | none (reviewer judgment) | ★★★ |
| AI-Eval | `ai-eval` | LLM-output feedback → prompt rules + eval rubric + regression cases | oracle / oracle, builder / guardian, oracle | eval harness (regression set) | ★★☆ |
| API Convention | `api-convention` | API review feedback → naming/versioning/error-shape rules | gateway / gateway, builder / guardian, gateway | OpenAPI lint (spectral) | ★★☆ |
| Architecture Decision | `arch-decision` | design decisions → architectural constraints | atlas, stratum / atlas, builder / guardian, atlas | fitness function / dep-cruiser | ★★☆ |
| Test Strategy | `test-strategy` | flaky / recurring failures → testing principles + quarantine rules | radar, vista / radar / guardian, radar | quarantine list + CI rule | ★☆☆ |

> Adding a row to "Proposed" is cheap — it just records intent. Rendering is the work; do it when a real signal stream for that domain exists (don't render speculative kits with no signals to feed them — they become dead docs).
