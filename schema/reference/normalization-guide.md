# Normalization Guide

Purpose: Use this file when you need the default normalization baseline or a documented reason to denormalize.

Contents:
1. Normal forms
2. Denormalization decision table
3. Denormalization patterns
4. Audit checklist

## Normal Forms

| Form | Rule | Common violation | Preferred fix |
|------|------|------------------|---------------|
| `1NF` | Atomic values, no repeating groups | `tags = 'a,b,c'` | Junction table |
| `2NF` | No partial dependency on part of a composite PK | `product_name` stored in `order_items` | Move to `products` |
| `3NF` | No transitive dependency | `city` depends on `zip_code`, not `user_id` | Separate reference table |

## When To Denormalize

| Factor | Stay normalized | Denormalize |
|--------|-----------------|-------------|
| Write frequency | High | Low |
| Read frequency | Low or mixed | High and repetitive |
| Consistency requirement | Strict | Eventual consistency is acceptable |
| Query complexity | Simple joins are acceptable | Joins are the bottleneck |

## Denormalization Patterns

| Pattern | Use when | Typical implementation |
|---------|----------|------------------------|
| Materialized view | Read-heavy dashboard or summary query | `REFRESH MATERIALIZED VIEW CONCURRENTLY` |
| Snapshot columns | Historical point-in-time values matter | Store price/name at purchase time |
| Counter cache | Count is queried constantly | `comment_count`, `order_count` |
| JSON aggregation | Attribute set is sparse and truly dynamic | `JSONB` column plus `GIN` index |

## Audit Checklist

- No comma-separated values or repeating column groups
- All non-key columns depend on the whole key
- No transitive dependencies remain in core tables
- Every denormalization choice has a documented rationale
- Source-of-truth ownership is explicit for duplicated data
