# Handoff Templates

**Purpose:** Standard handoff formats for inter-agent communication.
**Read when:** Receiving or sending data to partner agents.

---

## Incoming Handoffs

### SCHEMA_TO_MINT_HANDOFF

Received from Schema when table definitions are ready for data generation.

```yaml
SCHEMA_TO_MINT_HANDOFF:
  tables:
    - name: users
      columns:
        - { name: id, type: serial, pk: true }
        - { name: email, type: varchar(255), unique: true, not_null: true }
        - { name: name, type: varchar(100), not_null: true }
        - { name: role, type: enum(user,admin,moderator), default: user }
        - { name: created_at, type: timestamp, not_null: true }
        - { name: deleted_at, type: timestamp, nullable: true }
      indexes:
        - { columns: [email], unique: true }
    - name: orders
      columns:
        - { name: id, type: serial, pk: true }
        - { name: user_id, type: integer, fk: users.id, not_null: true }
        - { name: total, type: decimal(10,2), not_null: true }
        - { name: status, type: enum(pending,paid,shipped,cancelled), default: pending }
  relationships:
    - { from: orders.user_id, to: users.id, type: many-to-one }
  enums:
    - { name: user_role, values: [user, admin, moderator] }
    - { name: order_status, values: [pending, paid, shipped, cancelled] }
```

### RADAR_TO_MINT_HANDOFF

Received from Radar when specific test data is needed for coverage.

```yaml
RADAR_TO_MINT_HANDOFF:
  test_context:
    module: "order-processing"
    coverage_gaps:
      - "Edge case: order with zero items"
      - "Edge case: user with expired subscription placing order"
      - "Boundary: maximum cart size (100 items)"
  data_requirements:
    - entity: Order
      scenarios:
        - { name: empty_order, items_count: 0 }
        - { name: max_items, items_count: 100 }
        - { name: expired_user, user_trait: expired_subscription }
  constraints:
    - "Must use existing userFactory if available"
    - "Fixtures must be importable from test files"
```

### SIEGE_TO_MINT_HANDOFF

Received from Siege when volume data is needed for load testing.

```yaml
SIEGE_TO_MINT_HANDOFF:
  load_profile:
    target: "order-service"
    scenario: "Black Friday simulation"
  volume_requirements:
    users: 100000
    orders: 500000
    order_items: 1500000
    products: 5000
  data_distribution:
    - "80% orders in 'paid' status"
    - "15% orders in 'pending' status"
    - "5% orders in 'cancelled' status"
  constraints:
    - "Must generate in batches of 10000"
    - "Output as CSV for bulk import"
    - "Include realistic timestamps over 30-day window"
```

### ATTEST_TO_MINT_HANDOFF

Received from Attest when acceptance criteria drive data scenarios.

```yaml
ATTEST_TO_MINT_HANDOFF:
  acceptance_criteria:
    - id: AC-001
      description: "User can checkout with valid coupon"
      data_needs:
        - valid_coupon: { discount: 20, expiry: future }
        - user_with_cart: { items: 3, total: 15000 }
    - id: AC-002
      description: "System rejects expired coupon"
      data_needs:
        - expired_coupon: { discount: 20, expiry: past }
```

### CLOAK_TO_MINT_HANDOFF

Received from Cloak with PII masking rules.

```yaml
CLOAK_TO_MINT_HANDOFF:
  masking_rules:
    - field: "users.email"
      technique: faker_replacement
      locale: ja
    - field: "users.name"
      technique: faker_replacement
      locale: ja
    - field: "users.phone"
      technique: format_preserving_mask
    - field: "payments.card_number"
      technique: remove_entirely
    - field: "users.ssn"
      technique: remove_entirely
  compliance:
    standard: GDPR
    retention: "Test data expires after 30 days"
```

---

## Outgoing Handoffs

### MINT_TO_RADAR_HANDOFF

Sent to Radar with generated factories and fixtures.

```yaml
MINT_TO_RADAR_HANDOFF:
  factories:
    - path: "tests/factories/userFactory.ts"
      entity: User
      traits: [admin, deleted, unverified]
      edge_cases: [empty_name, max_length_email, unicode_name]
    - path: "tests/factories/orderFactory.ts"
      entity: Order
      traits: [empty, max_items, cancelled]
  fixtures:
    - path: "tests/fixtures/checkout-scenario.ts"
      description: "Complete checkout flow data"
  usage:
    import: "import { userFactory, orderFactory } from '@test/factories'"
    build: "userFactory.build({ transientParams: { admin: true } })"
    buildList: "orderFactory.buildList(5)"
  edge_cases_covered:
    - "Empty string fields"
    - "Max-length fields"
    - "Unicode/emoji in text fields"
    - "Zero and negative numbers"
    - "Null optional fields"
```

### MINT_TO_VOYAGER_HANDOFF

Sent to Voyager with E2E seed data.

```yaml
MINT_TO_VOYAGER_HANDOFF:
  seed_scripts:
    - path: "tests/e2e/seeds/setup.ts"
      description: "Base E2E environment seed"
      run_command: "npx tsx tests/e2e/seeds/setup.ts"
  test_accounts:
    - { email: "admin@test.example.com", password: "Test1234!", role: admin }
    - { email: "user@test.example.com", password: "Test1234!", role: user }
  preconditions:
    - "3 products in catalog"
    - "1 active coupon code: TESTCOUPON"
    - "Admin user has 2 existing orders"
  cleanup:
    command: "npx tsx tests/e2e/seeds/teardown.ts"
```

### MINT_TO_SIEGE_HANDOFF

Sent to Siege with volume datasets.

```yaml
MINT_TO_SIEGE_HANDOFF:
  datasets:
    - path: "load-test/data/users.csv"
      records: 100000
      format: CSV
    - path: "load-test/data/orders.csv"
      records: 500000
      format: CSV
  import_script: "load-test/scripts/bulk-import.sh"
  generation_time: "~15 minutes"
  data_distribution:
    order_status: { paid: 80%, pending: 15%, cancelled: 5% }
  notes:
    - "Timestamps distributed over 30-day window"
    - "Deterministic seed: 42 (reproducible)"
```

### MINT_TO_BUILDER_HANDOFF

Sent to Builder with test data utilities for integration tests.

```yaml
MINT_TO_BUILDER_HANDOFF:
  utilities:
    - path: "src/test-utils/factories/index.ts"
      exports: [userFactory, orderFactory, productFactory]
    - path: "src/test-utils/seed.ts"
      description: "Integration test seed runner"
  usage_example: |
    import { userFactory } from '@/test-utils/factories';
    const user = userFactory.build({ role: 'admin' });
  dependencies_added:
    - { name: "fishery", version: "^2.2.0", dev: true }
    - { name: "@faker-js/faker", version: "^9.0.0", dev: true }
```
