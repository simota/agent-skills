# PostgreSQL 19 Preview (2026-05)

Purpose: Use this file when planning the PG18 → PG19 migration window or evaluating PG19 Beta features in non-production. **PG19 is not yet GA** as of 2026-05-22 — do not deploy to production.

> Production target as of 2026-05 is **PostgreSQL 18** (currently 18.4). See `postgresql-18-performance.md` for the supported feature set.

Contents:
- Release timeline
- Notable features for query tuning
- What to evaluate in Beta
- Migration posture

---

## Release Timeline

| Milestone | Date | Source |
|-----------|------|--------|
| Feature freeze | 2026-04-08 | `https://www.postgresql.org/developer/roadmap/` |
| Beta 1 (scheduled) | **2026-06-04** | `https://www.postgresql.org/message-id/3a3283b1-5f4b-4f11-bae8-56f998454a01@postgresql.org` |
| GA (planned) | September 2026 | `https://pgpedia.info/postgresql-versions/postgresql-19.html` |

The project's normal cadence ships GA in late September; treat any earlier date as speculative.

## Notable Features for Query Tuning

These are the features most relevant to Tuner workflow once PG19 is GA (`https://thebuild.com/blog/2026/05/18/postgresql-19-beta-the-four-features-youll-actually-feel/`, `https://neon.com/postgresql/postgresql-19-new-features`, `https://www.bytebase.com/blog/postgres-19-features-im-excited-about/`):

| Area | Change | Why Tuner cares |
|------|--------|-----------------|
| SQL/PGQ graph queries (SQL:2023) | Expose relational tables as property graphs with pattern-matching syntax | Removes the need to bolt on a separate graph DB for moderate graph workloads; new plan node types to interpret |
| `ON CONFLICT DO SELECT` | Atomic get-or-create semantics | Replaces 2-round-trip get-or-insert patterns that drive lock contention |
| `FOR PORTION OF` (SQL:2011 temporal) | Range-bounded UPDATE/DELETE | New planner path for bitemporal / SCD workloads |
| `GROUP BY ALL`, `IGNORE NULLS` | Convenience syntax | Cosmetic; no plan impact |
| MultiXactOffset widened 32 → 64-bit | Eliminates ~4B-member wraparound limit | Removes an old "emergency vacuum required" failure mode on high-row-lock workloads |
| Online checksum enable/disable | Can be toggled on a running cluster | Lets ops add data checksums without dump/restore |
| `pg_stat_wal` extra detail | Finer WAL accounting | New tuning levers for WAL-pressure diagnosis |
| Per-process-type logging | Verbosity per `autovacuum` / `archiver` / etc. | Stops "I turned on debug logging and the log volume exploded" |
| Logical replication publications gain sequence support | `REFRESH SEQUENCES` + sequencesync worker | Closes a long-standing gap in logical replication migrations |

## What to Evaluate in Beta

Before any production cutover plan, run these checks against PG19 Beta in staging:

1. **Re-run top-10 slow queries** from PG18 production through PG19 Beta with `EXPLAIN (ANALYZE, BUFFERS)`. Look for plan-shape regressions (new sort, lost skip scan, hash → merge swap).
2. **Test `ON CONFLICT DO SELECT`** for any pattern currently using two round-trips for get-or-create. Quantify the round-trip elimination.
3. **Audit logical replication** if you depend on sequence values — the sequencesync worker is new and the migration path is `REFRESH SEQUENCES`.
4. **Confirm extension availability**: check that pgvector, PostGIS, pg_partman, pg_repack, TimescaleDB, etc., have PG19-compatible builds before counting on the upgrade window.
5. **Verify `pg_upgrade` from PG18 → PG19** preserves planner statistics and that any `CREATE STATISTICS` objects rebuild correctly post-upgrade (this is the PG18 behavior — verify it carries to 19).

## Migration Posture (Tuner)

| Phase | Tuner action |
|-------|--------------|
| 2026-05 to GA | Stay on PG18. Use this file only for forward planning. |
| Beta period | Run staging benchmarks; do not promote PG19 recommendations into production fix prompts. |
| GA + ~1 quarter | Wait for the first minor (`19.1`) before any production roll. The 18.0 release also shipped the first minor (18.1) two months later. |
| Production cutover | Treat PG18 → PG19 like PG17 → PG18: re-EXPLAIN top queries, rebuild extended statistics, validate logical replication, verify extension versions. |

Until PG19 is GA, every actionable `## LLM Fix Prompt` block stays anchored to PG18 (current production) or the user's actual deployed major.
