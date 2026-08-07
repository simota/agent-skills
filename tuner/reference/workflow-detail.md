# Tuner Workflow — Phase Detail

Full required-checks detail for each phase of `ANALYZE → DIAGNOSE → OPTIMIZE → VALIDATE → PRESENT`. `SKILL.md` keeps only the one-line focus; this file is the source of truth for the required checks.

| Phase | Focus | Required checks |
|-------|-------|-----------------|
| `ANALYZE` | Collect evidence and lock a baseline | Capture baseline `EXPLAIN (ANALYZE, BUFFERS)`, slow-query sample, and workload context **before any change** — no baseline, no optimization. |
| `DIAGNOSE` | Isolate the bottleneck | Root cause across scan/join/sort/index; flag version-specific wins (PG18 AIO / skip scan / uuidv7 / virtual generated columns). |
| `OPTIMIZE` | Choose the safest improvement | Rewrite, index, config, cache, MV, or partition recommendation; quantify write-amplification and emit `CONCURRENTLY` DDL + rollback SQL for index/migration changes. |
| `VALIDATE` | Prove the change, guard the rest | Side-by-side before/after `EXPLAIN ANALYZE` diff with row-estimate-ratio delta; confirm no plan regression on adjacent reads/writes — revert the recommendation if a secondary query regresses. |
| `PRESENT` | Deliver and hand off | Report before/after P50/P95/P99 + buffer hits/reads; route Schema (migration ownership), Bolt (app caching), Beacon (before/after monitoring). |
