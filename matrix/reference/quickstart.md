# Quickstart Templates

Purpose: Use this file when you need a fast, copy-pasteable starter matrix without reading the full methodology.

## Contents

- Test matrix
- Deploy matrix
- Risk matrix
- Usage notes

## Test Matrix

Use this when planning browser, OS, auth, or locale coverage.

```yaml
matrix:
  domain: test
  axes:
    - name: browser
      values: [Chrome, Firefox, Safari]
    - name: os
      values: [Windows, macOS, Linux]
    - name: auth
      values: [logged_in, anonymous]
  constraints:
    exclude:
      - { browser: Safari, os: Windows }
      - { browser: Safari, os: Linux }
  optimization: pairwise
  priority_axis: browser
```

Expected outcome:

- Original combinations: `18`
- Optimized set: about `6`
- Coverage guarantee: `2-way 100%`
- Suggested next agent: `Voyager` or `Radar`

## Deploy Matrix

Use this when rollout order depends on environment, region, or traffic.

```yaml
matrix:
  domain: deploy
  axes:
    - name: environment
      values: [production, staging]
    - name: region
      values: [us-east, ap-northeast, eu-west]
    - name: traffic
      values: ["100%", "50%", "10%"]
  constraints:
    conditional:
      - if: { environment: staging }
        then: { traffic: "100%" }
  optimization: pairwise
  priority_axis: region
```

Expected outcome:

- Original combinations: `18`
- Optimized set: about `6`
- Coverage guarantee: `2-way 100%`
- Suggested next agent: `Scaffold` or `Gear`

## Risk Matrix

Use this when threat, surface, and privilege combinations need prioritization.

```yaml
matrix:
  domain: risk
  axes:
    - name: threat
      values: [XSS, SQLi, CSRF, RCE]
    - name: surface
      values: [API, Web, Mobile]
    - name: auth_level
      values: [admin, user, anonymous]
  optimization: pairwise
  priority_axis: threat
```

Expected outcome:

- Original combinations: `36`
- Optimized set: about `9`
- Coverage guarantee: `2-way 100%`
- Suggested next agent: `Triage`, `Sentinel`, or `Scout`

## Usage Notes

1. Start here when the user needs a matrix quickly.
2. Move to [input-schema.md](~/.claude/skills/matrix/reference/input-schema.md) when constraints, weights, or metadata become more complex.
3. Move to [output-templates.md](~/.claude/skills/matrix/reference/output-templates.md) when the result must be handed off formally.
