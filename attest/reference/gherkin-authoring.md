# Gherkin Authoring Reference

Purpose: Author production-quality Gherkin `.feature` files with framework-aware step-definition mapping. Cover Cucumber-JVM, Cucumber-JS, Reqnroll (.NET, the active fork of SpecFlow), Behave (Python), pytest-bdd, and Godog (Go). Translate ACs into executable BDD specifications.

## Scope Boundary

- **attest `gherkin`**: Gherkin authoring + step-definition mapping (this document).
- **attest `bdd` (elsewhere)**: Generic Given/When/Then scenario shapes from spec.
- **Voyager (elsewhere)**: E2E execution layer (Playwright/Cypress).
- **Radar (elsewhere)**: Test code authoring beyond BDD scaffolding.
- **Builder (elsewhere)**: Step-definition body implementation.

## Gherkin Anatomy

```gherkin
@billing @critical
Feature: Refund processing
  As a customer
  I want to request a refund
  So that I receive my money back when goods are defective

  Background:
    Given the customer "alice@example.com" has order "ORD-001" totaling $50

  Scenario: Full refund within 30 days
    When the customer requests a full refund
    Then the order status becomes "refunded"
    And $50 is credited back to the original payment method

  Scenario Outline: Refund window enforcement
    Given the order was placed <days_ago> days ago
    When the customer requests a refund
    Then the system responds with "<outcome>"

    Examples:
      | days_ago | outcome   |
      | 1        | accepted  |
      | 30       | accepted  |
      | 31       | rejected  |
      | 365      | rejected  |
```

Components:
- **Feature**: One per file; describes capability + role narrative.
- **Background**: Steps that precede every scenario in the file.
- **Scenario**: One concrete example.
- **Scenario Outline + Examples**: Parameterized scenarios.
- **Tags**: `@<name>` for grouping, filtering, hooks.
- **Steps**: `Given` / `When` / `Then` / `And` / `But`.
- **Doc strings** (`"""`) and **data tables** (`|`).

## Step Quality Rules

| Rule | Example |
|------|---------|
| Declarative not imperative | `Given the user is logged in` (not "click email field, type x, click password...") |
| One subject per step | `Then the order is shipped` (not "the order is shipped and email sent") |
| User language, not UI | `When the customer requests a refund` (not "when GET /api/refunds returns 200") |
| Domain ubiquitous language | Use the same nouns as the spec |
| Avoid conjunctions inside a step | Use `And` to chain instead |
| No assertions in `Given`/`When` | Reserve assertions for `Then` |

## Framework-Specific Step-Definition Mapping

### Cucumber-JS (TypeScript)

```typescript
import { Given, When, Then } from '@cucumber/cucumber';

Given('the customer {string} has order {string} totaling ${int}',
  async function (email: string, orderId: string, amount: number) {
    this.customer = await createCustomer(email);
    this.order = await createOrder(orderId, this.customer.id, amount);
  }
);

When('the customer requests a full refund', async function () {
  this.response = await refundService.processFull(this.order.id);
});

Then('the order status becomes {string}', async function (status: string) {
  const order = await getOrder(this.order.id);
  expect(order.status).toBe(status);
});
```

Cucumber expressions: `{string}`, `{int}`, `{float}`, `{word}`, `{}` plus custom parameter types.

### Cucumber-JVM (Java)

```java
import io.cucumber.java.en.*;

public class RefundSteps {
    @Given("the customer {string} has order {string} totaling ${int}")
    public void customer_has_order(String email, String orderId, int amount) {
        this.order = orderFactory.create(email, orderId, amount);
    }

    @When("the customer requests a full refund")
    public void customer_requests_refund() {
        this.response = refundService.processFull(this.order.getId());
    }

    @Then("the order status becomes {string}")
    public void order_status_becomes(String status) {
        assertThat(orderRepo.find(order.getId()).getStatus()).isEqualTo(status);
    }
}
```

### SpecFlow / Reqnroll (.NET)

```csharp
[Binding]
public class RefundSteps {
    [Given(@"the customer ""(.+)"" has order ""(.+)"" totaling \$(\d+)")]
    public void GivenCustomerHasOrder(string email, string orderId, int amount) {
        order = orderFactory.Create(email, orderId, amount);
    }

    [When(@"the customer requests a full refund")]
    public void WhenCustomerRequestsFullRefund() {
        response = refundService.ProcessFull(order.Id);
    }

    [Then(@"the order status becomes ""(.+)""")]
    public void ThenOrderStatusBecomes(string status) {
        Assert.Equal(status, orderRepo.Find(order.Id).Status);
    }
}
```

Note: Reqnroll is the maintained successor to SpecFlow. SpecFlow has been stagnant since 2022; new .NET BDD projects should adopt Reqnroll directly. Existing SpecFlow projects can migrate via Reqnroll's compatibility shim — Gherkin syntax is preserved, and step-definition method signatures map 1:1.

### Behave (Python)

```python
from behave import given, when, then

@given('the customer "{email}" has order "{order_id}" totaling ${amount:d}')
def step_customer_has_order(context, email, order_id, amount):
    context.order = order_factory.create(email, order_id, amount)

@when('the customer requests a full refund')
def step_request_full_refund(context):
    context.response = refund_service.process_full(context.order.id)

@then('the order status becomes "{status}"')
def step_order_status(context, status):
    order = order_repo.find(context.order.id)
    assert order.status == status
```

### pytest-bdd

```python
from pytest_bdd import given, when, then, parsers, scenarios

scenarios('../features/refund.feature')

@given(parsers.parse('the customer "{email}" has order "{order_id}" totaling ${amount:d}'),
       target_fixture='order')
def order_setup(email, order_id, amount):
    return order_factory.create(email, order_id, amount)

@when('the customer requests a full refund', target_fixture='response')
def request_refund(order):
    return refund_service.process_full(order.id)

@then(parsers.parse('the order status becomes "{status}"'))
def assert_status(order, status):
    assert order_repo.find(order.id).status == status
```

### Godog (Go)

```go
func iHaveOrderTotaling(email, orderID string, amount int) error {
    order = orderFactory.Create(email, orderID, amount)
    return nil
}

func iRequestFullRefund() error {
    response = refundService.ProcessFull(order.ID)
    return nil
}

func InitializeScenario(ctx *godog.ScenarioContext) {
    ctx.Step(`^the customer "([^"]*)" has order "([^"]*)" totaling \$(\d+)$`, iHaveOrderTotaling)
    ctx.Step(`^the customer requests a full refund$`, iRequestFullRefund)
}
```

## Tag Strategy

```gherkin
@critical                 # Priority: must pass for release
@billing                  # Domain area
@regression               # Add to nightly suite
@flaky                    # Known unstable; quarantined
@wip                      # Work in progress; excluded from CI
@manual                   # Cannot be automated; doc-only
@requires-feature-flag    # Conditional execution
@slow                     # Excluded from PR runs
```

CI patterns:
- PR run: `--tags "@critical and not @slow and not @wip"`
- Nightly: `--tags "not @manual and not @wip"`
- Smoke: `--tags "@smoke"`

## Hook Patterns

```typescript
import { Before, After, BeforeAll, AfterAll } from '@cucumber/cucumber';

BeforeAll(async () => { await db.migrate(); });
Before({ tags: '@billing' }, async function () { this.billing = await setupBillingFixture(); });
After(async function (scenario) {
  if (scenario.result?.status === 'FAILED') {
    await captureScreenshot(scenario);
  }
});
```

## Data Tables

```gherkin
Given the following users exist:
  | name  | email             | role  |
  | Alice | alice@example.com | admin |
  | Bob   | bob@example.com   | user  |
```

```typescript
Given('the following users exist:', async function (table: DataTable) {
  for (const row of table.hashes()) {
    await createUser(row);
  }
});
```

## AC → Gherkin Translation

| AC pattern | Gherkin pattern |
|------------|-----------------|
| "When X happens, Y must be true" | `When X` / `Then Y` |
| "If precondition P, then Y" | `Given P` / `When X` / `Then Y` |
| "Y must hold for all values [...]" | `Scenario Outline` + `Examples` |
| "Within N days/seconds" | Boundary tests at N-1, N, N+1 in Examples |
| "Otherwise reject" | Negative scenario with explicit error message |
| "Atomically" | `Then ... And ...` chained Then steps |

## Workflow

```
EXTRACT     →  pull ACs from spec (one feature file per capability)
            →  identify role narrative (As a / I want / So that)

DECOMPOSE   →  one scenario per concrete behavior
            →  outline + examples for parameterized rules
            →  background for shared setup

WRITE       →  declarative steps in domain language
            →  data tables for repeated structures
            →  doc strings for payloads

TAG         →  priority + domain + execution lane
            →  feature-flag conditional tags

MAP         →  emit step-definition stubs for target framework
            →  cucumber expressions or regex
            →  parameter type definitions

INTEGRATE   →  hook setup (Before/After/BeforeAll)
            →  CI tag filters
            →  reporting (cucumber-html-reporter, allure)

HANDOFF     →  Builder: step body implementation
            →  Voyager: E2E orchestration if browser-driven
            →  Radar: complementary unit/integration tests
```

## Output Template

```markdown
## Gherkin Package: [Feature]

### Feature File
[full .feature content]

### Step Definition Stubs
- **Framework**: [Cucumber-JS / Cucumber-JVM / Reqnroll (.NET) / Behave / pytest-bdd / Godog]
- **File**: [path]
- [code stubs]

### Tag Plan
| Tag | Purpose | CI lane |
|-----|---------|---------|
| @critical | Release blocker | PR + nightly |
| @billing | Domain | Nightly |
| @smoke | Sanity | Pre-deploy |

### Hooks
- BeforeAll: [setup]
- Before(@billing): [fixture]
- After: [teardown + screenshot on failure]

### Data Strategy
- Fixtures from: [Mint / factory / fixtures.json]
- Cleanup: [transaction rollback / explicit teardown]

### CI Integration
- PR command: `[test runner cmd] --tags "@critical and not @slow"`
- Nightly: `--tags "not @manual and not @wip"`

### Coverage
- ACs covered: [N/M]
- Outline branches: [list]
- Negative paths: [list]

### Handoffs
- Builder: implement step bodies
- Voyager: browser orchestration if needed
- Radar: complementary unit tests
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| UI-driven steps ("click button X") | Declarative behavior ("submits the order") |
| Multiple Given/When/Then in one step via `and` text | Split with `And` step keyword |
| Background with too many steps (>3) | Move to fixture / hook |
| Scenario without `Then` | Every scenario must have an assertion |
| Hard-coded data without Examples | Use Scenario Outline + Examples for variants |
| Implementation leaking into step text (URLs, SQL) | Hide in step-definition body |
| Sharing mutable state via globals | Use scenario context / DI |
| Tags applied at scenario but never to feature | Inherit at feature for cross-scenario rules |
| One mega-feature file | Split per capability |
| Step ambiguity (two definitions match same text) | Use unique cucumber expressions / regex anchors |
| Conditional logic in steps (if/else) | One step = one behavior; split scenarios |
| `Then` that performs an action | `Then` is read-only; move action to `When` |
| Using `Given` for assertion | Use `Then`; `Given` is precondition only |

## Deliverable Contract

When `gherkin` completes, emit:

- **Feature files** with Background, Scenarios, Outlines, Tags.
- **Step-definition stubs** for the target framework.
- **Tag taxonomy** with CI lane mapping.
- **Hook configuration**.
- **Data fixtures** plan.
- **CI tag filters** per lane.
- **Coverage report**: ACs covered, missing.
- **Handoffs**: Builder, Voyager, Radar.

## References

- Cucumber — Gherkin Reference (cucumber.io/docs/gherkin)
- Cucumber Expressions — github.com/cucumber/cucumber-expressions
- Cucumber-JVM, Cucumber-JS, Godog official documentation
- Reqnroll (formerly SpecFlow) — reqnroll.net
- Behave — behave.readthedocs.io
- pytest-bdd — pytest-bdd.readthedocs.io
- Aslak Hellesøy, *The Cucumber Book* (2nd ed.)
- Liz Keogh — "Step away from the tools" (BDD vs tooling)
- Dan North — original BDD essay
- Matt Wynne, Aslak Hellesøy — *BDD in Action*
- Gojko Adzic — *Specification by Example*
- ISO/IEC/IEEE 29119-1 — software testing concepts
