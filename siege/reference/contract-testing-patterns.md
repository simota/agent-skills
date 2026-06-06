# Contract Testing Patterns

Purpose: Use this file for consumer-driven contracts, event contracts, CI gates, and breaking-change evaluation in `CONTRACT` mode.

## Contents

- Contract testing types
- Pact CDC patterns
- AsyncAPI and event contracts
- CI integration
- Breaking-change rules

## Contract Testing Overview

| Type | Direction | Tool | Best fit |
| --- | --- | --- | --- |
| Consumer-driven | Consumer -> Provider | Pact | internal HTTP APIs |
| Provider-driven | Provider -> Consumer | OpenAPI + validation | public APIs |
| Bi-directional | both | Pact + schema validation | mixed ownership models |
| Event contract | Publisher -> Subscriber | Pact / AsyncAPI | messaging and event streams |

## Pact CDC

### Consumer Test

```javascript
const { PactV3, MatchersV3 } = require('@pact-foundation/pact');
const { like, string } = MatchersV3;

const provider = new PactV3({
  consumer: 'OrderService',
  provider: 'ProductService',
});

it('returns product details', async () => {
  await provider
    .given('product 123 exists')
    .uponReceiving('a request for product 123')
    .withRequest({ method: 'GET', path: '/api/products/123' })
    .willRespondWith({
      status: 200,
      body: { id: string('123'), name: string('Widget'), price: like(9.99) },
    })
    .executeTest(async (mockServer) => {
      const product = await fetchProduct(mockServer.url, '123');
      expect(product.name).toBe('Widget');
    });
});
```

### Provider Verification

```python
from pact import Verifier

def test_provider():
    verifier = Verifier(
        provider="ProductService",
        provider_base_url="http://localhost:8080",
    )

    output, _ = verifier.verify_pacts(
        pact_url="https://pact-broker.example.com/pacts/provider/ProductService/consumer/OrderService/latest",
        provider_states_setup_url="http://localhost:8080/_pact/setup",
        publish_verification_results=True,
        provider_app_version="1.2.3",
    )

    assert output == 0
```

## AsyncAPI Event Contract

```yaml
asyncapi: '2.6.0'
info:
  title: Order Events
  version: '1.0.0'

channels:
  orders/created:
    publish:
      operationId: orderCreated
      message:
        name: OrderCreated
        payload:
          type: object
          required: [orderId, customerId, totalAmount, createdAt]
```

### Message Pact Test

```javascript
const { MessageConsumerPact } = require('@pact-foundation/pact');

it('processes order created event', () => {
  return new MessageConsumerPact({
    consumer: 'InventoryService',
    provider: 'OrderService',
  })
    .expectsToReceive('an order created event')
    .withContent({ orderId: like('ord-123'), customerId: like('cust-456') })
    .verify(async (message) => {
      const result = await processOrderEvent(message);
      expect(result.inventoryUpdated).toBe(true);
    });
});
```

## CI Integration

### Pact Broker Workflow

```text
Consumer CI:                    Provider CI:
1. Run consumer tests      ->   1. Pull pacts from broker
2. Generate pact files     ->   2. Verify against provider
3. Publish to broker       ->   3. Publish verification results
4. can-i-deploy            ->   4. can-i-deploy
5. Deploy consumer         ->   5. Deploy provider
```

### GitHub Actions

```yaml
contract-test:
  runs-on: ubuntu-latest
  steps:
    - name: Run consumer tests
      run: npm test -- --testPathPattern=pact
    - name: Publish pacts
      run: |
        npx pact-broker publish ./pacts \
          --consumer-app-version=${{ github.sha }} \
          --branch=${{ github.ref_name }} \
          --broker-base-url=${{ secrets.PACT_BROKER_URL }} \
          --broker-token=${{ secrets.PACT_BROKER_TOKEN }}
    - name: Can I Deploy?
      run: |
        npx pact-broker can-i-deploy \
          --pacticipant=OrderService \
          --version=${{ github.sha }} \
          --to-environment=production \
          --broker-base-url=${{ secrets.PACT_BROKER_URL }}
```

## Breaking Change Detection

| Change | Breaking? | Detection |
| --- | --- | --- |
| Add optional field | No | safe |
| Add required field | Yes | provider or consumer verification fails |
| Remove field | Yes if consumed | consumer contract fails |
| Change field type | Yes | both sides fail |
| Change enum values | Maybe | depends on consumer assumptions |
| Change URL path | Yes | consumer contract fails |
| Add new endpoint | No | safe |

## Versioning Strategy

- Run `can-i-deploy` before every deployment.
- Publish pacts with branch and environment metadata.
- Use pending pacts for new interactions.
- Re-verify provider contracts whenever pacts change.
