# Chaos Engineering & Observability Integration

Purpose: Use this file when chaos work needs observability design, CI maturity guidance, Game Day practice rules, or anti-pattern checks.

## Contents

- Observability pillars in chaos experiments
- Monitoring vs observability
- CI/CD maturity levels
- Game Day practices
- Chaos anti-patterns

## Observability Pillars for Chaos

| Pillar | Role in chaos experiments | Data to collect |
| --- | --- | --- |
| Metrics | define steady-state baselines and quantify impact | latency, throughput, error rate, CPU, memory, queue depth |
| Logs | explain failure context and fallback behavior | affected service, error messages, retry/failover events |
| Traces | reveal propagation paths and bottlenecks | cross-service dependencies and request-path damage |

## Monitoring vs Observability

- Monitoring tells you what broke.
- Observability helps explain why it broke.
- Chaos experiments need both, but observability is the deciding capability when failure paths are unknown.

## CI/CD Integration Maturity

| Level | Integration style | Automation | Environment |
| --- | --- | --- | --- |
| `L1` | manual Game Day | none | staging |
| `L2` | pre-release gate | partial | staging |
| `L3` | PR or merge pipeline | automated | test environment |
| `L4` | continuous chaos | fully automated | canary + production |
| `L5` | adaptive chaos | autonomous | multiple environments |

### `L3` Example

```yaml
resilience-gate:
  runs-on: ubuntu-latest
  needs: [unit-tests, integration-tests]
  steps:
    - name: Deploy to test environment
      run: kubectl apply -f k8s/test/
    - name: Wait for healthy state
      run: kubectl wait --for=condition=ready pod -l app=myapp --timeout=120s
    - name: Capture baseline metrics
      run: ./scripts/capture-metrics.sh --duration 300 --output baseline.json
    - name: Inject fault
      run: kubectl delete pod -l app=myapp --wait=false
    - name: Verify recovery
      run: ./scripts/verify-steady-state.sh --baseline baseline.json --tolerance 10%
```

## Game Day Practice Rules

| Rule | Why it matters |
| --- | --- |
| Blameless culture | findings should improve systems, not punish individuals |
| Work in daylight hours | Game Day is for learning, not firefighting at `2AM` |
| Prepare `3-6 months` ahead for mature programs | SLOs, runbooks, and stakeholder alignment take time |
| Escalate gradually | single service -> multi-service -> zone failure |
| Include non-engineering stakeholders | product and business impact matters during failure drills |
| Repeat regularly | monthly or quarterly practice builds muscle memory |
| Record a timeline | postmortems and action tracking need exact sequence data |

### Common Game Day Failures

| Failure | Result | Prevention |
| --- | --- | --- |
| kill switch not tested | injection cannot be stopped | test the kill switch in advance |
| stakeholders not notified | chaos is mistaken for an incident | announce scope beforehand |
| recovery unclear | time lost after the experiment | document rollback steps per scenario |
| insufficient metrics | impact cannot be measured | validate observability before the drill |
| scope too large | accidental cascading incident | start with the smallest blast radius |

## Chaos Anti-Patterns

| ID | Anti-pattern | Fix |
| --- | --- | --- |
| `CA-01` | Blindfolded Chaos | build metrics, logs, and traces first |
| `CA-02` | Big Bang Experiment | expand from staging or canary to production gradually |
| `CA-03` | Chaos without Hypothesis | require a steady-state hypothesis before injection |
| `CA-04` | One-Off Game Day | run recurring Game Days and automate proven scenarios |
| `CA-05` | Findings Without Actions | assign owners and severities to every gap |
| `CA-06` | Copy-Paste Experiments | design faults around your own dependency graph |
| `CA-07` | Chaos as Blame Tool | keep the process blameless and system-focused |
