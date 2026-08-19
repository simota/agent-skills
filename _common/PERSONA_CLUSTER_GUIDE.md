# Persona Cluster Guide

Five persona agents form a lifecycle. This guide helps route to the right agent and navigate the cluster.

## Persona Lifecycle

```
Field → Cast → Echo / Trace / Echo[demand]
 (research)   (generate/manage)   (consume/validate/advocate)
```

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| **Field** | Design and conduct user research | Research questions | Findings, persona data |
| **Cast** | Generate, register, evolve, audit personas | Evidence from any source | Registered personas |
| **Echo** | Persona-based cognitive walkthrough | Existing UI/flow + persona | Friction report, emotion scores |
| **Trace** | Session replay behavioral analysis | Real session data + persona | Behavior patterns, validation data |
| **Echo[demand]** | Synthetic user advocate | Product context + persona | Feature requests, unmet needs |

## Echo vs Echo[demand] Decision Tree

```
What is your goal?
|
+-- "Evaluate an existing UI/flow for friction"
|   -> Echo (cognitive walkthrough, emotion scoring)
|
+-- "Discover what users want but haven't been built"
|   -> Echo[demand] (demand generation, blind spot discovery)
|
+-- "Detect dark patterns or bias in a UI"
|   -> Echo
|
+-- "Challenge team assumptions or roadmap"
|   -> Echo[demand] (CHALLENGE mode)
|
+-- "Understand user emotion during a specific flow"
|   -> Echo
|
+-- "Hear competitive frustration from users"
|   -> Echo[demand] (COMPETE mode)
|
+-- "Generate A/B test hypotheses"
|   -> Echo (friction -> hypothesis)
|
+-- "Write user-voice section for PRD/spec"
|   -> Echo[demand] -> Scribe[unified]/Scribe
|
+-- "Both / Unclear"
|   -> Echo[demand] (explore demands) -> Echo (validate in existing flow)
```

### Core Distinction

| Dimension | Echo | Echo[demand] |
|-----------|------|------|
| Input | Existing UI/flow/screenshots | Product context/roadmap/feature area |
| Output | Friction points, emotion scores, improvements | Feature requests, unmet needs, assumption challenges |
| Perspective | "How does this UI feel?" | "What is missing from this product?" |
| Timing | Post-design / post-implementation validation | Planning stage / roadmap review |
| Persona usage | Walk through UI as persona | Speak demands as persona |

## Migration Note

Echo's persona generation and persona templates are managed by Cast (the canonical source). See:
- Persona schema: `cast/reference/persona-model.md`
- Generation workflows: `cast/reference/generation-workflows.md`

Synthetic persona risks and guardrails: `_common/AI_PERSONA_RISKS.md`
