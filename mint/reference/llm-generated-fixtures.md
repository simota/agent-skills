# LLM-Generated Test Data with Guardrails

**Purpose:** Use an LLM to synthesize test fixtures (free-text fields, realistic product descriptions, dialogue, long-tail categorical values) while keeping the output deterministic, schema-valid, bias-audited, and cost-capped. Mint owns the fixture contract; the LLM is a generator behind a strict validation layer.

## Scope Boundary

- **Mint `llm`**: LLM as a fixture generator with schema post-validation, deterministic seeding, bias sampling, and cost ceiling.
- **Oracle (elsewhere)**: production LLM feature design — prompt engineering, RAG pipelines, eval framework, AI safety architecture, MLOps.
- **Forge (elsewhere)**: throwaway mocked LLM data for UX prototypes (no validation, no eval, single-session).
- **Siege (elsewhere)**: adversarial / red-team inputs for load and resilience testing; `llm` produces typical data, Siege produces abusive data.

If the hypothesis is "do realistic-but-fake fixtures expose a bug?" → `llm`. If it is "is our production prompt correct?" → Oracle.

## When LLM Beats Faker

| Field type | Faker | LLM |
|------------|-------|-----|
| Name / email / address | ✓ (faster, deterministic) | ✗ (overkill) |
| Short categorical (status, role) | ✓ | ✗ |
| Realistic product review (50–200 words, topic-consistent) | ✗ (template-y) | ✓ |
| Multi-turn dialogue with topic drift | ✗ | ✓ |
| Long-tail SKU / description variants that look like a real catalog | ✗ | ✓ |
| Domain-specific error messages (medical, legal, technical) | ✗ | ✓ |

Rule: if the field needs **semantic coherence with adjacent fields** or **domain authenticity**, LLM earns its cost. Otherwise Faker wins.

## Prompt Template Contract

Every Mint-owned generator prompt must include:

```
SYSTEM:
  You are a test-fixture generator. Output ONLY valid JSON matching the schema below.
  Do not invent fields. Do not add commentary. Do not use real personal names
  from training data — use obviously synthetic names.

SCHEMA:
  { "id": "uuid", "title": "string<=60", "body": "string<=500",
    "sentiment": "positive|neutral|negative", "locale": "en|ja|de" }

CONSTRAINTS:
  - count: 25
  - sentiment distribution: positive=10, neutral=8, negative=7
  - locale distribution: en=15, ja=5, de=5
  - diversity: no two titles sharing a 5-gram

USER:
  Generate now.
```

Keys: explicit schema, explicit distribution targets (for bias control), explicit diversity constraint (to prevent mode collapse), explicit "no real PII from training data".

## Hallucination Detection (Schema Validation After Generation)

LLM output is untrusted. Validate every record, discard invalid ones, retry with budget cap.

```python
from pydantic import BaseModel, ValidationError

class Fixture(BaseModel):
    id: str
    title: str
    body: str
    sentiment: str
    locale: str

def generate_batch(prompt: str, target: int, max_retries: int = 3) -> list[Fixture]:
    fixtures, attempts = [], 0
    while len(fixtures) < target and attempts < max_retries:
        raw = llm_call(prompt)          # returns list[dict]
        for record in raw:
            try:
                fixtures.append(Fixture.model_validate(record))
            except ValidationError:
                continue                # silently drop, count against attempts
        attempts += 1
    if len(fixtures) < target:
        raise RuntimeError(f"Only {len(fixtures)}/{target} valid after {attempts} attempts")
    return fixtures[:target]
```

Reject rate > 20% is a prompt-quality signal — tighten the schema in the prompt before adding retries.

## Bias Audit on Generated Data

LLM output reflects training-data skew. Audit every batch before it ships to fixtures.

| Axis | Check | Threshold |
|------|-------|-----------|
| Gender (names / pronouns) | distribution across male / female / neutral | no class > 60% |
| Locale / script | character-class histogram | matches target distribution ± 10% |
| Sentiment | classifier agreement with prompt label | ≥ 90% |
| Length | token-count std / mean | ≥ 0.3 (reject suspiciously uniform batches) |
| Duplication | near-dup via embedding cosine > 0.9 | < 5% of batch |
| Topic coverage | keyword histogram | no single topic > 40% |

Fail the batch on any red axis — do not "fix" by re-prompting five times; re-design the prompt.

## Deterministic Seeding and Cache

LLMs are non-deterministic by default. Mint fixtures must reproduce.

```python
# temperature=0 is necessary but not sufficient (providers still vary across weeks)
# Real determinism = cache the output keyed by (prompt_hash, model, schema_version)

import hashlib, json, pathlib

def cache_key(prompt: str, model: str, schema_version: str) -> str:
    return hashlib.sha256(f"{model}|{schema_version}|{prompt}".encode()).hexdigest()

def generate_cached(prompt, model, schema_version, cache_dir="fixtures/cache"):
    key = cache_key(prompt, model, schema_version)
    path = pathlib.Path(cache_dir) / f"{key}.json"
    if path.exists():
        return json.loads(path.read_text())
    result = llm_call(prompt, model=model, temperature=0, seed=42)
    path.write_text(json.dumps(result))
    return result
```

Commit the cache directory. CI reads from cache; only a `--regenerate` flag triggers live calls.

## Eval Pipeline for Generator Quality

A generator prompt is itself testable. Run nightly against a held-out spec:

```
input:   prompt template + sample constraints
eval 1:  schema-validity rate   >= 95%
eval 2:  bias-audit pass        == 100%
eval 3:  diversity (dup rate)   <  5%
eval 4:  human-spot-check score >= 4/5 on 10 samples weekly
output:  red / amber / green per template, trend chart
```

Amber / red triggers a prompt-review PR — generator prompts are code and rot like code.

## Cost Control

Before generating:

```
budget = batch_count × records_per_batch × tokens_per_record × model_price
```

| Control | Rule |
|---------|------|
| Hard daily cap | per-generator env var, reject call above cap |
| Batch size | prefer 20–50 records per prompt call over 1-by-1 |
| Model tier | cheapest model that passes eval — don't default to the flagship |
| Cache first | CI must hit cache 99% of runs; regen is a deliberate act |
| Alert | cost > 2× trailing 7-day mean → page the Mint owner |

Typical fixture-generation cost target: ≤ $5 per full regen across all fixtures in a repo.

## Anti-Patterns

- Calling the LLM at test time — tests must not depend on network or provider availability.
- Skipping schema validation because "it looked fine" — one malformed record breaks the whole fixture load.
- Using `temperature > 0` for fixture generation then committing the output — non-reproducible CI.
- Letting the LLM invent PII-shaped strings (real-looking emails, phone numbers) without a PII scrub pass — hand off to `pii`.
- No cost cap — a regen loop can burn hundreds of dollars silently.
- Re-running the prompt five times until the bias audit passes by luck — the audit has been overfit, not solved.
- Using LLM output as both generator and validator (self-grading) — confirmation bias. Validate with schema + classifier + Faker-based smoke checks instead.
- Prompt-as-code without version tracking — record `prompt_hash` + `model` + `schema_version` in the fixture header.

## Handoff

**To Radar:** generated fixture set + generator prompt hash + eval report (schema-valid rate, bias pass, dup rate). Radar trusts Mint's contract, not the LLM.
**To `pii`:** raw LLM output before commit, for a scrub pass if any free-text could have leaked training-data PII.
**To Oracle:** prompt-engineering learnings if the generator was expensive to make correct — Oracle can upgrade the prompt for production LLM features.
**To Siege:** adversarial variants of the generator prompt if stress / red-team coverage is also desired; Siege owns the abuse side.
