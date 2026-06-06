# Schema Design Anti-Patterns

Purpose: Use this file when reviewing table structure, naming, constraints, or data-type choices.

Contents:
1. Core anti-patterns
2. Data-type selection
3. Constraint strategy
4. Naming rules
5. Design gates

## Core Anti-Patterns

| ID | Anti-pattern | Signal | Safer pattern |
|----|--------------|--------|---------------|
| `SD-01` | God Table | `200+` columns, full scans dominate, many unrelated domains mixed together | Split by domain or lifecycle |
| `SD-02` | Missing Primary Key | Rows cannot be uniquely updated/deleted, ORM support breaks | Add UUID or BIGINT surrogate PK |
| `SD-03` | FK Orphans | `*_id` columns without FK constraints, ghost records remain | Add FK plus deliberate `ON DELETE` strategy |
| `SD-04` | Wrong Data Type | Date, money, boolean, or UUID stored as text | Use semantic DB-native types |
| `SD-05` | Wide Table | `150+` columns or many sparse attributes | Vertical split, move sparse fields to `JSONB` only if justified |
| `SD-06` | Constraint Desert | No `CHECK`, `NOT NULL`, or `UNIQUE`; app-only validation | Enforce invariants in the DB |
| `SD-07` | Reserved Word Collision | `user`, `order`, `group`, or other reserved names require quoting | Use plural or scoped names |

## Data-Type Selection

| Data kind | Avoid | Prefer |
|-----------|-------|--------|
| Money | `FLOAT`, `DOUBLE` | `NUMERIC` / `DECIMAL` |
| Date/time | `VARCHAR` | `DATE`, `TIMESTAMP`, `TIMESTAMPTZ` |
| Boolean | `INT`, `CHAR('Y'/'N')` | `BOOLEAN` |
| UUID | `VARCHAR(36)` | Native `UUID` |
| Status | Free-form `VARCHAR` | `ENUM` or `CHECK` |
| JSON payload | `TEXT` | `JSON` / `JSONB` |

## Constraint Strategy

- DB constraints are the final integrity boundary.
- App validation improves UX; it does not replace DB validation.
- Name constraints explicitly so failure messages are actionable.
- Use `ON DELETE CASCADE` only when bulk child deletion is intentional and bounded.

## Naming Rules

| Area | Preferred | Avoid |
|------|-----------|-------|
| Tables | plural `snake_case` | singular, camelCase, reserved words |
| FKs | `{table_singular}_id` | ambiguous names like `user` or `ref` |
| Booleans | `is_*`, `has_*` | vague flags |
| Timestamps | `*_at` | mixed naming styles |
| Indexes | `idx_{table}_{columns}` | auto-generated opaque names |
| Constraints | `pk_`, `fk_`, `chk_`, `uniq_` prefixes | unnamed or opaque defaults |

## Design Gates

- `50+` columns in one table -> review for vertical split
- Missing PK -> block the design
- `*_id` without FK -> propose a FK or explain why the link is intentionally soft
- Date/money/boolean stored as text -> propose a type migration
- No `CHECK` / `NOT NULL` where business invariants exist -> add DB constraints
- Reserved-word identifier -> rename before migration generation
