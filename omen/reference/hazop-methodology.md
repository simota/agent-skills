# HAZOP Methodology Reference

Purpose: HAZOP (Hazard and Operability study, IEC 61882) is a systematic deviation analysis originally from process safety. At each process node, a facilitated team walks a matrix of Parameters × Guidewords, asking "what if this parameter deviates from design intent in this way?" — producing a catalogue of deviations, causes, consequences, existing safeguards, and recommended actions. HAZOP adapts cleanly to software systems where nodes become integration boundaries, parameters become throughput / latency / ordering / volume, and guidewords flex to data-flow deviations.

## Scope Boundary

- **omen `hazop`**: node-by-node parameter × guideword deviation study. Systematic, team-facilitated, report-driven. Best for data pipelines, message brokers, control flows, integration boundaries.
- **omen `mode` / `premortem` (elsewhere)**: FMEA / pre-mortem — broader and less structured than HAZOP. Use HAZOP when the system is a clearly decomposable flow; use FMEA when modes cut across many components.
- **omen `faulttree` (elsewhere)**: deductive analysis of one undesired outcome. Complementary — HAZOP deviations often seed fault-tree top events.
- **siege concurrency (elsewhere)**: concurrency and async edge cases. A HAZOP on a message broker surfaces "REVERSE flow" and "AS WELL AS" deviations that siege concurrency then investigates at runtime.
- **STPA (elsewhere in literature)**: Systems-Theoretic Process Analysis — better than HAZOP for software-heavy, tightly-coupled control systems with emergent behavior. When control loops dominate, prefer STPA.
- **Magi (elsewhere)**: trade-off arbitration when HAZOP recommendations compete.

## Workflow

```
1. PREP          assemble design intent: architecture diagram, data contract,
                 SLO / SLA targets, operational envelope.
2. NODES         decompose the system into study nodes: each node is a
                 pipe/queue/call/stream with explicit inputs and outputs.
3. PARAMETERS    pick the parameter set that governs the node's design intent
                 (see Parameter Mapping below).
4. GUIDEWORDS    apply the guideword set to each parameter at each node.
5. DEVIATION     for each (node, parameter, guideword) cell, state the
                 deviation in one sentence. Skip meaningless cells.
6. C-C-S-A       for each kept deviation, record:
                   - Cause(s)
                   - Consequence(s)
                   - Safeguards (existing)
                   - Action(s) recommended (owner + by-when)
7. RECONVENE     review deviations crossing node boundaries; close the loop.
8. REPORT        publish HAZOP worksheet; escalate critical deviations to
                 `faulttree` (deep dive) and `bowtie` (stakeholder view).
```

## Parameter Mapping (process → software)

| Process-safety parameter | Software / system equivalent |
|--------------------------|------------------------------|
| Flow | Throughput (req/s, msg/s, rows/s) |
| Pressure | Backpressure, queue depth, buffer pressure |
| Temperature | Resource heat: CPU %, memory %, GC pause |
| Level | Storage fill: disk %, quota consumption |
| Composition | Payload schema, field set, content-type |
| Time | Latency, freshness, TTL, age of message |
| Sequence | Ordering, causality, commit order |
| Identity | Tenant / user / key correlation |
| Quantity | Batch size, fan-out, message volume |

## Guideword Set

| Guideword | Meaning | Software example |
|-----------|---------|------------------|
| NO / NONE | Complete negation | Zero messages delivered |
| MORE | Quantitative increase | Throughput exceeds SLA 5× |
| LESS | Quantitative decrease | Retrieval returns <1% of expected rows |
| AS WELL AS | Qualitative addition | Extra unexpected fields in payload |
| PART OF | Qualitative decrease | Truncated payload, missing fields |
| REVERSE | Opposite direction | Events replayed out of order |
| OTHER THAN | Complete substitution | Wrong tenant's data routed in |
| EARLY / LATE | Timing deviation | Message arrives after TTL |
| BEFORE / AFTER | Ordering deviation | DB commit precedes validation |

Keep the EARLY/LATE/BEFORE/AFTER extensions for any system with temporal semantics — they catch ordering bugs that NO/MORE/LESS miss.

## Parameter × Guideword Grid (example)

Node: *Kafka topic `orders.v1` — producer → broker → consumer*.

| Parameter | Guideword | Deviation | Cause | Consequence | Safeguard | Action |
|-----------|-----------|-----------|-------|-------------|-----------|--------|
| Throughput | MORE | Producer spikes 10× baseline | Black-Friday campaign | Broker disk pressure, consumer lag | Quota per producer | Load-test producer at 10× |
| Ordering | REVERSE | Consumer re-processes older offsets | Bad consumer reset on deploy | Duplicate side effects | Idempotency key | Add idempotency-key test in CI |
| Composition | AS WELL AS | New optional field added upstream | Schema evolution | Consumer ignores field silently | Schema registry | Enforce consumer compat check |
| Identity | OTHER THAN | Wrong tenant id in key | Bug in producer | Cross-tenant leak | None today | Add tenant-id assertion in serializer |
| Time | LATE | Message age > 5 min | Consumer pause, GC | Downstream SLO miss | Lag alert | Tighten lag threshold to 60s |

A meaningful HAZOP produces 20-80 deviation rows per node for non-trivial systems. Cells that are "N/A / not credible" should be marked explicitly rather than erased — the blank cell is indistinguishable from an oversight in review.

## Study Team Composition

Minimum team of four, ideally five to seven:

| Role | Contribution |
|------|--------------|
| Facilitator (trained) | Drives guideword sweep, keeps pace, owns the minutes |
| Scribe | Captures C-C-S-A per row verbatim |
| Designer / architect | Defends design intent, proposes safeguards |
| Operator / SRE | Grounds deviations in observed reality |
| Domain / product owner | Judges business consequence severity |
| Security (optional) | Flags threats requiring Sentinel / Breach handoff |

A HAZOP without an operator is a design review; a HAZOP without a facilitator drifts. Sessions cap at 3 hours — longer and the team misses deviations.

## Report Template

```
HAZOP Study: <system / release>
Date: <yyyy-mm-dd>   Facilitator: <name>   Attendees: <roles>

Design intent reference: <link>
Node list: <N1, N2, …>

Per-node worksheets: (Parameter / Guideword / Deviation / Cause /
Consequence / Safeguard / Action / Owner / Due)

Cross-node observations: <deviations that traverse nodes>
Escalations: <deviations handed to faulttree / bowtie / sentinel>
Action tracker: <open / closed / deferred, owner, due>
Next review: <date>
```

## HAZOP vs STPA

| Dimension | HAZOP | STPA |
|-----------|-------|------|
| Origin | Process safety (ICI, 1960s) | Systems theory (Leveson, 2010s) |
| Unit of study | Node + parameters | Control loops + unsafe control actions |
| Best fit | Data pipelines, message flows, transport | Autonomy, control systems, emergent behavior |
| Strength | Exhaustive at node level | Captures system-level emergent hazards |
| Weakness | Weak at emergent / cross-node behavior | Heavier ramp-up, fewer practitioners |
| Software fit | Good for flow-dominant systems | Better for control-dominant systems |

Rule of thumb: if the architecture diagram looks like a DAG of flows, start with HAZOP. If it looks like a controller with feedback, start with STPA.

## Anti-Patterns

- Running HAZOP without a design-intent document — deviations have nothing to deviate from.
- Skipping "N/A" cells instead of marking them — review cannot distinguish skip from miss.
- Letting the designer facilitate — they will unconsciously defend rather than challenge.
- Collapsing Consequence and Safeguard into one column — loses the gap between "what would happen" and "what stops it today".
- Leaving actions without owner + due date — the worksheet becomes a museum piece.
- Using HAZOP where STPA fits better (tight control loops, emergent hazards).
- Running a 6-hour marathon session — quality collapses after hour three; split across days.

## Handoff

- **To `faulttree`**: deviations with severe consequences become top events for deductive analysis.
- **To `bowtie`**: each critical deviation maps to a threat on the bowtie left side with its safeguards as preventive barriers.
- **To Triage**: HAZOP actions for runtime deviations seed runbook entries.
- **To Beacon**: deviations detectable only via telemetry define new SLIs and alerts.
- **To Radar**: each kept deviation row becomes a test scenario candidate.
- **To Sentinel / Breach**: deviations with adversarial causes escalate to security review.
- **To Magi**: when two safeguard actions compete for the same budget, hand the deviation rows + cost to Magi for trade-off arbitration.
