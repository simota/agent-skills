# Field — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Field-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Field
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Interview Guide | Usability Test Plan | Research Report | Persona Set | Journey Map | Calibration Report | Tri-Engine Combined Plan | Tri-Engine Portfolio]"
    parameters:
      study_mode: "[Study design | Analysis & synthesis | Continuous program | AI-assisted review | Calibration & impact]"
      research_questions: "[primary research questions]"
      methodology: "[interview | usability test | survey | diary study | mixed methods]"
      sample_size: "[participant count]"
      confidence_level: "[high | medium | low]"
    tri_engine:                                  # present only when `multi` Recipe ran
      engines_run: [codex, agy, claude]
      engines_failed: [list or none]
      merge_strategy: "[Combined Plan | Portfolio]"
      concurrence_distribution:
        UNIVERSAL: [count]
        LIKELY: [count]
        VERIFIED-DIVERGENT: [count]
      coverage_matrix:                           # qual/quant × generative/evaluative cell counts
        qual_generative: [count]
        qual_evaluative: [count]
        qual_descriptive: [count]
        quant_generative: [count]
        quant_evaluative: [count]
        quant_descriptive: [count]
        mixed: [count]
      rejected: [count + top categories — duplicate / hallucination / ethics-gap / under-powered / WEIRD-bias / synthetic-misuse]
  Validations:
    - "[research questions defined before study design]"
    - "[bias checklist applied]"
    - "[evidence strength documented]"
    - "[limitations and segment scope stated]"
  Next: Cast | Echo | Spark | Vision | Palette | Canvas | Echo[demand] | DONE
  Reason: [Why this next step]
```
