# Input Schema

Purpose: Use this file when the request arrives as free text, YAML, JSON, or a table and you need to normalize it into a matrix model.

## Contents

- Natural-language parsing
- YAML schema
- JSON schema
- Table input
- Validation rules
- Priority semantics

## Natural-Language Parsing

Support these patterns directly.

| Expression | Parse result |
|---|---|
| `A/B/C × X/Y` | axis1=`[A,B,C]`, axis2=`[X,Y]` |
| `AとBとCを、XとYで` | axis1=`[A,B,C]`, axis2=`[X,Y]` |
| `AまたはB、XまたはY` | axis1=`[A,B]`, axis2=`[X,Y]` |
| `AはXと組み合わせない` | constraint `exclude {A, X}` |
| `テストしたい` | domain `test` |
| `デプロイしたい` | domain `deploy` |
| `リスク評価したい` | domain `risk` |

Example:

```text
「Chrome/Firefox/Safari を Windows/macOS/Linux で、
  ログイン済み/未ログインの状態でテストしたい。
  ただし Safari は Windows と組み合わせない。」
```

Normalized form:

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
      - {browser: Safari, os: Windows}
  optimization: pairwise
```

## YAML Schema

Recommended format:

```yaml
matrix:
  domain: test | load | deploy | ux | risk | experiment | compat | custom
  name: optional-name
  description: optional-text
  axes:
    - name: axis_name
      values: [value1, value2]
      priority: high | medium | low
      weight: 1-10
  constraints:
    exclude:
      - {axis_name: value, axis_name: value}
    conditional:
      - if: {axis_name: value}
        then: {axis_name: value}
    require:
      - {axis_name: value, axis_name: value}
  optimization: pairwise | orthogonal | cit | full | custom
  t_way: 2 | 3 | 4
  max_combinations: 1
  tags: [tag1, tag2]
```

## JSON Schema

Use the same logical fields as YAML.

```json
{
  "$schema": "matrix-v1",
  "matrix": {
    "domain": "test",
    "axes": [
      {
        "name": "browser",
        "values": ["Chrome", "Firefox", "Safari"],
        "priority": "high"
      }
    ],
    "constraints": {
      "exclude": [{"browser": "Safari", "os": "Windows"}]
    },
    "optimization": "pairwise",
    "max_combinations": 20
  }
}
```

## Table Input

Accept simple tables and normalize them into YAML.

```markdown
| Axis     | Values                     |
|----------|----------------------------|
| browser  | Chrome, Firefox, Safari    |
| os       | Windows, macOS             |
| locale   | Japanese, English, Chinese |
```

## Validation Rules

| Check | Action |
|---|---|
| fewer than `2` axes | stop, ask for more dimensions |
| any axis has fewer than `2` values | stop, require at least two values |
| duplicated axis names | stop, require unique names |
| constraints eliminate every combination | `ON_CONSTRAINT_UNKNOWN` |
| `6+` axes | warn with `ON_AXIS_OVERFLOW` |
| `max_combinations` exceeds the raw space | warn that optimization has no effect |

## Priority Semantics

| Priority | Meaning | Default behavior |
|---|---|---|
| `high` | must be represented strongly | bias coverage and ranking upward |
| `medium` | standard | default |
| `low` | supplementary | cover with minimum acceptable density |
