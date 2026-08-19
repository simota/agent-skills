# Fishbone Delta

Purpose: Scout `fishbone` breadth, evidence, and anti-blame contract. Ishikawa notation is model-known.

## Software/Ops Categories

Use the 6M labels only as prompts, adapting names when the domain fits better:

- Machine: infrastructure, runtime, hardware, platform
- Method: code, procedure, workflow, controls
- Material: inputs, data, dependencies
- Measurement: telemetry, alerts, thresholds
- Environment: external service, load, regulation, operating condition
- People/organization: staffing, knowledge flow, incentives, handoffs

People is never a terminal blame bucket; trace the system condition that made individual action decisive.

## Workflow Contract

1. State one factual effect without embedding a suspected cause.
2. Generate candidate causes across applicable categories before convergence.
3. Weight candidates using an agreed probability/impact scale.
4. Mark each top candidate `confirmed`, `ruled out`, or `uncertain` with evidence.
5. Identify primary and contributing causes and explain their interaction.

## Required Output

Provide the effect, categorized cause map, weighted top causes, evidence/verdict table, primary-plus-contributor narrative, corrective action, detection improvement, owners, and handoffs to Builder/Triage/Lore as appropriate.
