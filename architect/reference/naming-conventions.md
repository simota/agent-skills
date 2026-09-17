# Agent Naming

Run after the primary action, output and domain are known. Use 1–2 syllables where possible; 3 is acceptable, 4+ is avoided. Do not use numbers or special characters. Repository file/display conventions remain authoritative.

## Candidate Score

Rate each dimension 1–5; multiply by its weight and sum. Select the highest-scoring candidate that passes conflict checks.

| Dimension | Weight |
|-----------|--------|
| Brevity | 20% |
| Evocativeness | 30% |
| Memorability | 20% |
| Uniqueness | 15% |
| Typeability | 15% |

## Required Records

```yaml
FUNCTION_ANALYSIS:
  primary_action: "[what the agent does]"
  primary_output: "[owned deliverable]"
  primary_domain: "[scope]"
CONFLICT_CHECK:
  exact_match: "[current skill names checked]"
  phonetic_similar: "[confusable names]"
  abbreviation_conflict: "[confusable short forms]"
  semantic_conflict: "[roles the name could misroute to]"
```

Check the actual global and available project-local skill definitions, not a copied name bank. Reject exact conflicts; explain remaining ambiguity before selection. Avoid culturally offensive or misleading names and unsupported claims of trademark clearance.

Return the selected name, syllable count, weighted score and the conflict evidence. Do not retain illustrative names as a list of available names: installation and roster changes invalidate that assumption.
