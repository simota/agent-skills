# Exit Survey Delta

Purpose: Voice churn-survey data and handoff contract. Generic question lists are model-known.

## Collection Rules

- Trigger after cancellation is confirmed; never block cancellation or require free text.
- Keep a short product-specific reason taxonomy plus `other` and `prefer_not_to_say`.
- Randomize reason order when ordering bias matters and version the taxonomy.
- Separate survey response, save-offer behavior, and marketing-contact consent.
- Do not infer the primary churn cause from a selected reason alone; combine with behavior, billing, support, and follow-up evidence.

## Minimal Record

```text
response_id, account/user pseudonymous key, cancellation timestamp,
reason_code, optional verbatim, segment/plan/tenure, touchpoint,
save_offer_shown/accepted, taxonomy_version, consent flags
```

Apply the product's privacy, retention, and access controls. Avoid storing unnecessary personal text.

## Required Output

Report response rate, reason distribution with sample sizes, segment/tenure differences, verbatim themes, save-offer outcomes, missingness, confidence limits, and the distinction between stated and observed causes. Route product themes to Spark, retention mechanisms to Growth, instrumentation gaps to Pulse, and qualitative follow-up to Field.
