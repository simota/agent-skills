# Zen Refactoring Recipes

Purpose: Use this file when you need a concrete refactoring recipe with ordered steps and before/after examples.

## Contents
- [Core Recipes](#extract-method)
- [Advanced Recipes](#replace-conditional-with-polymorphism)
- [Canonical Report Template](#beforeafter-report-template)

Step-by-step guides for common refactorings.

---

## Extract Method

**When**: Long method, duplicated code, code needing explanation

**Steps**:
1. Identify code fragment to extract
2. Check for local variables used (read and modified)
3. Create new method with intention-revealing name
4. Copy code to new method
5. Replace original code with method call
6. Pass read variables as parameters
7. Return modified variables (or use out parameters)
8. Run tests to verify behavior unchanged

**Before**:
```javascript
function printOwing() {
  // print banner
  console.log("***********************");
  console.log("**** Customer Owes ****");
  console.log("***********************");

  // calculate outstanding
  let outstanding = 0;
  for (const o of orders) {
    outstanding += o.amount;
  }

  // print details
  console.log(`name: ${name}`);
  console.log(`amount: ${outstanding}`);
// ...
```

**After**:
```javascript
function printOwing() {
  printBanner();
  const outstanding = calculateOutstanding();
  printDetails(outstanding);
}

function printBanner() {
  console.log("***********************");
  console.log("**** Customer Owes ****");
  console.log("***********************");
}

function calculateOutstanding() {
  return orders.reduce((sum, o) => sum + o.amount, 0);
}
// ...
```

---

## Replace Conditional with Guard Clauses

**When**: Deeply nested conditionals, special cases mixed with main logic

**Steps**:
1. Identify special case conditions
2. Convert each to early return (guard clause)
3. Remove unnecessary else branches
4. Flatten remaining main logic
5. Run tests

**Before**:
```javascript
function getPayAmount() {
  let result;
  if (isDead) {
    result = deadAmount();
  } else {
    if (isSeparated) {
      result = separatedAmount();
    } else {
      if (isRetired) {
        result = retiredAmount();
      } else {
        result = normalPayAmount();
      }
    }
  }
// ...
```

**After**:
```javascript
function getPayAmount() {
  if (isDead) return deadAmount();
  if (isSeparated) return separatedAmount();
  if (isRetired) return retiredAmount();
  return normalPayAmount();
}
```

---

## Introduce Explaining Variable

**When**: Complex expressions that are hard to understand

**Steps**:
1. Identify complex expression
2. Create well-named variable
3. Replace expression with variable
4. Run tests

**Before**:
```javascript
if (platform.toUpperCase().indexOf("MAC") > -1 &&
    browser.toUpperCase().indexOf("IE") > -1 &&
    wasInitialized() && resize > 0) {
  // do something
}
```

**After**:
```javascript
const isMacOS = platform.toUpperCase().indexOf("MAC") > -1;
const isIE = browser.toUpperCase().indexOf("IE") > -1;
const wasResized = wasInitialized() && resize > 0;

if (isMacOS && isIE && wasResized) {
  // do something
}
```

---

## Introduce Constant

**When**: Magic numbers or strings appear in code

**Steps**:
1. Identify magic value
2. Create descriptively named constant
3. Replace all occurrences
4. Run tests

**Before**:
```javascript
if (age >= 18) { /* ... */ }
if (status === 'pending') { /* ... */ }
const timeout = 86400000;
```

**After**:
```javascript
const LEGAL_ADULT_AGE = 18;
const STATUS_PENDING = 'pending';
const ONE_DAY_MS = 24 * 60 * 60 * 1000;

if (age >= LEGAL_ADULT_AGE) { /* ... */ }
if (status === STATUS_PENDING) { /* ... */ }
const timeout = ONE_DAY_MS;
```

### Naming Guidelines

- Use SCREAMING_SNAKE_CASE for constants
- Name should explain the meaning, not the value
- Group related constants together

```javascript
// ❌ Bad: Name describes value
const THIRTY_DAYS = 30;
const ONE_HUNDRED = 100;

// ✅ Good: Name describes meaning
const PASSWORD_EXPIRY_DAYS = 30;
const MAX_LOGIN_ATTEMPTS = 100;
```

---

## Replace Conditional with Polymorphism

**When**: Switch/if-else chains that dispatch based on type or status

**Steps**:
1. Identify the condition that selects behavior
2. Create interface/base class for the common behavior
3. Create subclass/implementation for each case
4. Replace conditional with polymorphic dispatch
5. Run tests

**Before**:
```typescript
function calculateArea(shape: Shape): number {
  switch (shape.type) {
    case 'circle':
      return Math.PI * shape.radius ** 2;
    case 'rectangle':
      return shape.width * shape.height;
    case 'triangle':
      return 0.5 * shape.base * shape.height;
    default:
      throw new Error(`Unknown shape: ${shape.type}`);
  }
}
```

**After**:
```typescript
interface Shape {
  area(): number;
}

class Circle implements Shape {
  constructor(private radius: number) {}
  area(): number { return Math.PI * this.radius ** 2; }
}

class Rectangle implements Shape {
  constructor(private width: number, private height: number) {}
  area(): number { return this.width * this.height; }
}

class Triangle implements Shape {
// ...
```

---

## Introduce Parameter Object

**When**: 3+ parameters frequently travel together, or function signatures are growing

**Steps**:
1. Identify parameters that logically group together
2. Create a class/interface for the group
3. Replace parameter list with the new object
4. Move related behavior into the object if applicable
5. Run tests

**Before**:
```typescript
function createEvent(
  title: string,
  startDate: Date,
  endDate: Date,
  location: string,
  isRecurring: boolean,
  recurrencePattern?: string
) { ... }

createEvent("Meeting", start, end, "Room A", true, "weekly");
```

**After**:
```typescript
interface EventConfig {
  title: string;
  dateRange: DateRange;
  location: string;
  recurrence?: RecurrenceConfig;
}

interface DateRange {
  start: Date;
  end: Date;
}

interface RecurrenceConfig {
  pattern: string;
}
// ...
```

---

## Decompose Conditional

**When**: Complex boolean expressions that are hard to read at a glance

**Steps**:
1. Identify the complex conditional
2. Extract each clause into a named function or variable
3. Replace original expression with named parts
4. Run tests

**Before**:
```typescript
if (
  user.subscription !== 'free' &&
  user.lastLogin > thirtyDaysAgo &&
  user.purchaseCount > 0 &&
  !user.isDeactivated
) {
  sendPromoEmail(user);
}
```

**After**:
```typescript
const isPaidUser = user.subscription !== 'free';
const isRecentlyActive = user.lastLogin > thirtyDaysAgo;
const hasPurchaseHistory = user.purchaseCount > 0;
const isActiveAccount = !user.isDeactivated;

const isEligibleForPromo = isPaidUser && isRecentlyActive && hasPurchaseHistory && isActiveAccount;

if (isEligibleForPromo) {
  sendPromoEmail(user);
}
```

---

## Replace Nested Conditional with Pipeline

**When**: Data transformation with multiple filter/map/reduce steps tangled in loops

**Steps**:
1. Identify the collection being processed
2. Convert loop body into chained operations (filter, map, reduce)
3. Give each step a meaningful name if complex
4. Run tests

**Before**:
```typescript
function getActiveUserEmails(users: User[]): string[] {
  const result: string[] = [];
  for (const user of users) {
    if (user.isActive) {
      if (user.email) {
        if (user.emailVerified) {
          result.push(user.email.toLowerCase());
        }
      }
    }
  }
  return result;
}
```

**After**:
```typescript
function getActiveUserEmails(users: User[]): string[] {
  return users
    .filter(user => user.isActive)
    .filter(user => user.email && user.emailVerified)
    .map(user => user.email!.toLowerCase());
}
```

---

## Extract Interface

**When**: Class has multiple responsibilities, or you need to improve testability

**Steps**:
1. Identify the subset of methods that represent a cohesive contract
2. Create an interface with those method signatures
3. Have the class implement the interface
4. Update consumers to depend on the interface
5. Run tests

**Before**:
```typescript
class PaymentService {
  async charge(amount: number, card: Card): Promise<Receipt> { ... }
  async refund(receiptId: string): Promise<void> { ... }
  getTransactionHistory(): Transaction[] { ... }
}

// Test requires a real PaymentService
function processOrder(service: PaymentService, order: Order) { ... }
```

**After**:
```typescript
interface PaymentGateway {
  charge(amount: number, card: Card): Promise<Receipt>;
  refund(receiptId: string): Promise<void>;
}

class StripePaymentService implements PaymentGateway {
  async charge(amount: number, card: Card): Promise<Receipt> { ... }
  async refund(receiptId: string): Promise<void> { ... }
  getTransactionHistory(): Transaction[] { ... }
}

// Now testable with mock
function processOrder(gateway: PaymentGateway, order: Order) { ... }
```

---

## Consolidate Duplicate Fragments

**When**: Same code appears in both branches of a conditional

**Steps**:
1. Identify identical code in if/else branches
2. Move common code before or after the conditional
3. Simplify the conditional to contain only differences
4. Run tests

**Before**:
```typescript
if (isSpecialDeal) {
  total = price * quantity * 0.95;
  sendConfirmation(total);
  logTransaction(total);
} else {
  total = price * quantity;
  sendConfirmation(total);
  logTransaction(total);
}
```

**After**:
```typescript
total = isSpecialDeal
  ? price * quantity * 0.95
  : price * quantity;
sendConfirmation(total);
logTransaction(total);
```

---

## Recipe 11: Introduce Strategy Pattern

**When**: Long if/else or switch chains dispatching behavior based on type or mode

**Steps**:
1. Identify the conditional that selects behavior
2. Define a Strategy interface with the varying behavior
3. Create concrete Strategy implementations for each branch
4. Replace conditional with strategy lookup/injection
5. Run tests

**Before**:
```typescript
function calculateShipping(order: Order): number {
  if (order.shippingMethod === 'standard') {
    return order.weight * 0.5;
  } else if (order.shippingMethod === 'express') {
    return order.weight * 1.5 + 5.0;
  } else if (order.shippingMethod === 'overnight') {
    return order.weight * 3.0 + 15.0;
  } else if (order.shippingMethod === 'international') {
    const zoneFactor = getZoneFactor(order.destination);
    return order.weight * 2.0 * zoneFactor + 20.0;
  }
  throw new Error(`Unknown method: ${order.shippingMethod}`);
}
```

**After**:
```typescript
interface ShippingStrategy {
  calculate(order: Order): number;
}

class StandardShipping implements ShippingStrategy {
  calculate(order: Order): number {
    return order.weight * 0.5;
  }
}

class ExpressShipping implements ShippingStrategy {
  calculate(order: Order): number {
    return order.weight * 1.5 + 5.0;
  }
}
// ...
```

---

## Recipe 12: Introduce Observer/Event

**When**: Tight coupling via direct method calls across modules; one action triggers multiple side effects

**Steps**:
1. Identify the trigger action and its side effects
2. Create an EventEmitter or pub/sub mechanism
3. Replace direct calls with event emission
4. Register side effects as event listeners
5. Run tests

**Before**:
```typescript
class OrderService {
  constructor(
    private emailService: EmailService,
    private inventoryService: InventoryService,
    private analyticsService: AnalyticsService,
    private loyaltyService: LoyaltyService,
  ) {}

  async placeOrder(order: Order): Promise<void> {
    await this.saveOrder(order);
    // Tightly coupled side effects
    await this.emailService.sendConfirmation(order);
    await this.inventoryService.reserveItems(order.items);
    await this.analyticsService.trackPurchase(order);
    await this.loyaltyService.addPoints(order.customerId, order.total);
// ...
```

**After**:
```typescript
class OrderService {
  constructor(private eventBus: EventEmitter) {}

  async placeOrder(order: Order): Promise<void> {
    await this.saveOrder(order);
    this.eventBus.emit('order.placed', order);
  }
}

// Listeners registered separately (loose coupling)
eventBus.on('order.placed', (order) => emailService.sendConfirmation(order));
eventBus.on('order.placed', (order) => inventoryService.reserveItems(order.items));
eventBus.on('order.placed', (order) => analyticsService.trackPurchase(order));
eventBus.on('order.placed', (order) => loyaltyService.addPoints(order.customerId, order.total));
```

---

## Recipe 13: Introduce Factory/Builder

**When**: Complex object construction with many optional parameters, conditional initialization, or multi-step setup

**Steps**:
1. Identify complex constructor or creation logic
2. Create a Builder class with fluent methods
3. Move construction logic into the builder
4. Replace direct construction with builder calls
5. Run tests

**Before**:
```typescript
// Complex construction scattered across callers
const config = new ServerConfig();
config.host = process.env.HOST || 'localhost';
config.port = parseInt(process.env.PORT || '3000');
config.ssl = process.env.NODE_ENV === 'production';
if (config.ssl) {
  config.sslCert = fs.readFileSync(process.env.SSL_CERT!);
  config.sslKey = fs.readFileSync(process.env.SSL_KEY!);
}
config.cors = process.env.NODE_ENV === 'development';
config.rateLimit = process.env.NODE_ENV === 'production' ? 100 : 0;
config.logging = process.env.LOG_LEVEL || 'info';
```

**After**:
```typescript
class ServerConfigBuilder {
  private config: Partial<ServerConfig> = {};

  host(host: string): this { this.config.host = host; return this; }
  port(port: number): this { this.config.port = port; return this; }
  withSSL(cert: Buffer, key: Buffer): this {
    this.config.ssl = true;
    this.config.sslCert = cert;
    this.config.sslKey = key;
    return this;
  }
  withCORS(): this { this.config.cors = true; return this; }
  rateLimit(limit: number): this { this.config.rateLimit = limit; return this; }
  logLevel(level: string): this { this.config.logging = level; return this; }

// ...
```

---

## Before/After Report Template

Use the canonical `## Refactoring Report: [Component/File]` template in `reference/review-report-templates.md`.
