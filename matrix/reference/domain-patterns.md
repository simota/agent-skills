# Domain Patterns

Purpose: Use this file when the domain is known and you need default axes, common constraints, scoring hints, and downstream routing.

## Contents

- Test
- Load
- Deploy
- UX
- Risk
- Experiment
- Compatibility
- AI/ML
- Custom

## Test

Typical axes:

| Axis | Common values | Priority |
|---|---|---|
| browser | Chrome, Firefox, Safari, Edge | high |
| os | Windows, macOS, Linux, iOS, Android | high |
| viewport | desktop, tablet, mobile | medium |
| auth_state | logged_in, anonymous, expired_session | high |
| data_state | empty, populated, edge_case | medium |
| network | wifi, cellular, slow_3g, offline | low |
| locale | ja, en, zh-TW, ko | low |

Common constraints:

```yaml
constraints:
  exclude:
    - {browser: Safari, os: Windows}
    - {browser: Chrome, os: iOS}
  conditional:
    - if: {network: offline}
      then: {auth_state: logged_in}
```

Suggested next agent: `Voyager`, `Radar`, or `Siege`.

## Load

Typical axes:

| Axis | Common values | Priority |
|---|---|---|
| concurrent_users | 10, 100, 500, 1000, 5000 | high |
| data_volume | small, medium, large | high |
| endpoint | /api/users, /api/search, /api/checkout | high |
| duration | 1min, 5min, 30min, 1hour | medium |
| ramp_pattern | constant, gradual, spike, wave | medium |
| region | ap-northeast-1, us-east-1, eu-west-1 | low |

Common constraints:

```yaml
constraints:
  conditional:
    - if: {concurrent_users: 5000}
      then: {duration: "1min"}
  exclude:
    - {data_volume: large, concurrent_users: 5000}
```

Suggested next agent: `Siege`, `Beacon`, or `Bolt`.

## Deploy

Typical axes:

| Axis | Common values | Priority |
|---|---|---|
| environment | dev, staging, production | high |
| region | ap-northeast-1, us-east-1, eu-west-1 | high |
| version | current, next, rollback | high |
| traffic_split | 0%, 1%, 10%, 50%, 100% | medium |
| rollout_strategy | blue-green, canary, rolling | medium |
| feature_flags | enabled, disabled | low |

Default ordering:

1. `dev -> staging -> production`
2. nearest region first
3. `1% -> 10% -> 50% -> 100%`

Suggested next agent: `Scaffold`, `Gear`, or `Beacon`.

## UX

Typical axes:

| Axis | Common values | Priority |
|---|---|---|
| persona | beginner, intermediate, expert, senior, accessibility_user | high |
| device | desktop, tablet, mobile | high |
| scenario | first_visit, return_visit, task_completion, error_recovery | high |
| locale | ja, en, zh, ko, ar | medium |
| accessibility | none, screen_reader, keyboard_only, high_contrast | medium |
| connection | fast, slow, offline | low |

Suggested next agent: `Cast`, `Echo`, or `Field`.

## Risk

Typical axes:

| Axis | Common values | Priority |
|---|---|---|
| threat | XSS, SQLi, CSRF, SSRF, XXE, RCE, PathTraversal | high |
| attack_surface | Web_UI, REST_API, GraphQL, WebSocket, File_Upload | high |
| auth_level | anonymous, authenticated, privileged, admin | high |
| data_sensitivity | public, internal, confidential, restricted, PII | high |
| impact | low, medium, high, critical | medium |

Default risk tiers:

| Score | Priority |
|---|---|
| `7.0-10.0` | `P0 / Critical` |
| `4.0-6.9` | `P1 / High` |
| `2.0-3.9` | `P2 / Medium` |
| `0.0-1.9` | `P3 / Low` |

Suggested next agent: `Triage`, `Sentinel`, `Probe`, or `Scout`.

## Experiment

Typical axes:

| Axis | Common values | Priority |
|---|---|---|
| variable | button_color, cta_text, layout, price_display | high |
| user_segment | new_users, returning_users, premium, free | high |
| exposure_rate | 1%, 5%, 10%, 50% | medium |
| duration | 1week, 2weeks, 1month | medium |
| metric | CTR, CVR, retention, ARPU | high |

Suggested next agent: `Experiment` or `Pulse`.

## Compatibility

Typical axes:

| Axis | Common values | Priority |
|---|---|---|
| runtime_version | Node.js 20, 22, 24 (Node 18 reached EOL 2025-04) / Python 3.11, 3.12, 3.13 (Python 3.9 EOL 2025-10, 3.10 EOL 2026-10) | high |
| dependency_version | react@18, react@19 (react@17 is two majors behind; only include for legacy migration matrices) | high |
| os | ubuntu-22.04, ubuntu-24.04, macos-14, macos-15 | medium |
| architecture | x86_64, arm64 | medium |
| feature | core, experimental, deprecated | medium |

Suggested next agent: `Shift` (`detect`/`radar`) or `Builder`.

## AI/ML

Typical axes:

| Axis | Common values | Priority |
|---|---|---|
| model_type | classification, regression, generative, recommendation | high |
| input_dimension | text, image, tabular, multimodal | high |
| fairness_group | gender, age, ethnicity, disability | high |
| dataset_split | train, validation, test, out-of-distribution | medium |
| hyperparameter | learning_rate, batch_size, epochs, dropout | medium |
| deployment_target | edge, cloud, on-premise | low |

Common constraints:

```yaml
constraints:
  conditional:
    - if: {input_dimension: multimodal}
      then: {model_type: generative}
  exclude:
    - {deployment_target: edge, model_type: generative}
```

Notes:

- Use NIST CT for AI-Enabled Systems guidance for input space modeling.
- Fairness axes require at least 3-way strength to cover intersectional bias (e.g., gender × age × ethnicity).
- Dataset coverage uses combinatorial coverage difference (NIST CSWP 19) to compare train vs. test distribution.
- For training data quality, use data frequency coverage instead of simple tuple presence — measure how often each feature interaction appears, not just whether it appears. Skewed frequency distributions degrade model performance even when all tuples are nominally covered (NIST 2025). Use CoDEX (Coverage of Data Explorer) for frequency analysis.
- Key finding: performance may increase or decrease with data skew, feature importance methods do not reliably predict skew impact, and adding more data may not mitigate skew effects — frequency rebalancing of specific interactions is needed.

Suggested next agent: `Oracle`, `Radar`, or `Experiment`.

## Custom

Use `custom` when none of the built-in domains fit. In that case:

- preserve the generic matrix model
- do not invent a downstream specialist
- ask only if domain ambiguity changes the outcome materially
