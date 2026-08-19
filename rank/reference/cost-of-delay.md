# Cost of Delay Delta

Purpose: Rank `cod` scope, uncertainty, and routing contract. General CoD/CD3 theory is model-known.

## Scope

- Use `cod` when value loss per unit time and calendar duration can be defended economically.
- Use WSJF for relative backlog scoring when monetary inputs are unreliable.
- Do not mix currency-valued and Fibonacci-valued items in one ordering.

## Calculation Contract

```text
CoD = user/business value loss + time-criticality loss + risk/opportunity loss
CD3 = CoD per time unit / calendar duration to value
```

- Classify the value curve before ranking: linear, urgent/front-loaded, fixed-deadline cliff, or uncertain/intangible.
- Fixed-deadline items are scheduled backward from the cliff, not blindly sorted by linear CD3.
- Duration includes dependencies, queue time, and time until value realization; it is not effort hours.
- Show ranges or sensitivity bands for weak inputs. Never present a single-point estimate as measured fact.

## Required Output

| Item | CoD range / week | Curve | Duration range | CD3 range | Confidence | Evidence |
|---|---:|---|---:|---:|---|---|

Also include the ordered queue, assumptions, dependency notes, executive overrides, and the condition that would change the order.

## Handoff

- Highest-ranked item -> Sherpa with duration and dependencies.
- Contested value lens or curve -> Magi.
- Strategic market-window input -> Helm.
- Audit trail -> Scribe with assumptions and sources.
