# Bolt Database Query Optimization

Query optimization patterns, N+1 fixes, and index strategies.

---

## EXPLAIN ANALYZE Reading Guide

```sql
-- PostgreSQL EXPLAIN ANALYZE
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE user_id = 123 AND status = 'pending';

-- Key metrics to watch:
-- 1. Seq Scan vs Index Scan (Seq Scan on large tables = problem)
-- 2. Rows vs Actual Rows (big difference = stale statistics)
-- 3. Loops (high number in nested loop = N+1 potential)
-- 4. Buffers: shared hit vs read (low hit ratio = need more cache)
```

---

## Index Strategies

```sql
-- B-tree: Default, good for equality and range queries
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_orders_user_status ON orders(user_id, status); -- Composite

-- Partial index: Index only relevant rows
CREATE INDEX idx_orders_pending ON orders(user_id)
  WHERE status = 'pending';

-- Covering index: Include columns to avoid table lookup
CREATE INDEX idx_orders_covering ON orders(user_id)
  INCLUDE (total, created_at);

-- GIN: For array/JSONB containment queries
CREATE INDEX idx_products_tags ON products USING GIN(tags);

-- Expression index: For computed queries
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
```

---

## N+1 Detection and Fixes

### Prisma

```typescript
// ❌ N+1 Problem: 1 query for orders + N queries for users
const orders = await prisma.order.findMany();
for (const order of orders) {
  const user = await prisma.user.findUnique({ where: { id: order.userId } });
}

// ✅ Fix with include (Prisma)
const orders = await prisma.order.findMany({
  include: { user: true }
});

// ✅ Fix with select for specific fields
const orders = await prisma.order.findMany({
  include: {
    user: {
      select: { id: true, name: true, email: true }
    }
  }
});
```

### TypeORM

```typescript
// ❌ Bad: Lazy loading causes N+1
@Entity()
class Order {
  @ManyToOne(() => User)
  user: User;
}

// ✅ Fix with eager loading
const orders = await orderRepository.find({
  relations: ['user', 'items']
});

// ✅ Fix with query builder for complex queries
const orders = await orderRepository
  .createQueryBuilder('order')
  .leftJoinAndSelect('order.user', 'user')
  .leftJoinAndSelect('order.items', 'items')
  .where('order.status = :status', { status: 'pending' })
  .getMany();
```

### Drizzle

```typescript
// ✅ Using with clause
const orders = await db.query.orders.findMany({
  with: {
    user: true,
    items: true
  }
});

// ✅ Using select with joins
const orders = await db
  .select()
  .from(ordersTable)
  .leftJoin(usersTable, eq(ordersTable.userId, usersTable.id))
  .where(eq(ordersTable.status, 'pending'));
```

---

## Query Rewriting Techniques

```sql
-- ❌ Slow: Correlated subquery
SELECT * FROM orders o
WHERE (SELECT COUNT(*) FROM order_items oi WHERE oi.order_id = o.id) > 5;

-- ✅ Fast: JOIN with GROUP BY
SELECT o.* FROM orders o
JOIN order_items oi ON oi.order_id = o.id
GROUP BY o.id
HAVING COUNT(oi.id) > 5;

-- ❌ Slow: OR with different columns
SELECT * FROM users WHERE email = 'a@b.com' OR phone = '123';

-- ✅ Fast: UNION (uses indexes on both columns)
SELECT * FROM users WHERE email = 'a@b.com'
UNION
SELECT * FROM users WHERE phone = '123';

-- ❌ Slow: NOT IN with subquery
SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM banned_users);

-- ✅ Fast: LEFT JOIN IS NULL
SELECT u.* FROM users u
LEFT JOIN banned_users b ON u.id = b.user_id
WHERE b.user_id IS NULL;

-- ❌ Slow: LIKE with leading wildcard (no index)
SELECT * FROM products WHERE name LIKE '%phone%';

-- ✅ Fast: Full-text search
SELECT * FROM products WHERE to_tsvector('english', name) @@ to_tsquery('phone');
```

---

## Batch Operations

```typescript
// ❌ Slow: Individual inserts
for (const item of items) {
  await prisma.item.create({ data: item });
}

// ✅ Fast: Batch insert
await prisma.item.createMany({
  data: items,
  skipDuplicates: true,
});

// ❌ Slow: Individual updates
for (const item of items) {
  await prisma.item.update({
    where: { id: item.id },
    data: { status: 'processed' }
  });
}

// ✅ Fast: Batch update with transaction
await prisma.$transaction(
  items.map(item =>
    prisma.item.update({
      where: { id: item.id },
      data: { status: 'processed' }
    })
  )
);

// ✅ Fastest: Raw SQL for bulk updates
await prisma.$executeRaw`
  UPDATE items SET status = 'processed'
  WHERE id = ANY(${ids})
`;
```
