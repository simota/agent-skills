# Chaos Engineering Guide

Purpose: Use this file for steady-state hypotheses, fault-injection scope, tool selection, and Game Day execution in `CHAOS` mode.

## Contents

- Chaos principles
- Steady-state hypothesis template
- Failure-injection scenarios
- Tool selection
- Game Day checklist and maturity model

## Chaos Principles

| Principle | Operational meaning |
| --- | --- |
| Steady state first | define normal behavior before injecting failure |
| Realistic faults | vary conditions that match real incidents |
| Minimal blast radius | start with canary scope or single-service failure |
| Automation after safety | automate only after manual safety checks are proven |
| Recovery matters | every experiment must include stop and restore conditions |

## Steady-State Hypothesis Template

```markdown
## Steady-State Hypothesis

### System Under Test
[Service/component]

### Normal Behavior
- Error rate: < [X]%
- Latency p99: < [X]ms
- Throughput: > [X] requests/sec
- Success rate: > [X]%

### Experiment
- Action: [fault to inject]
- Expected: [maintain steady state or degrade gracefully]
- Not expected: [cascading failure, data loss, stuck recovery]

### Abort Conditions
- Error rate exceeds [X]%
- Latency exceeds [X]ms
- Data corruption appears
- Kill switch is triggered
```

## Metrics to Observe

| Layer | Metrics |
| --- | --- |
| User-facing | error rate, latency, success rate |
| Application | exceptions, queue depth, worker/thread count |
| Infrastructure | CPU, memory, disk, network |
| Dependencies | latency and error rate per dependency |

## Failure Injection Scenarios

| Scenario | Tool | Example |
| --- | --- | --- |
| Kill pod | `kubectl` | `kubectl delete pod <name> -n <ns>` |
| CPU stress | `stress-ng` | `stress-ng --cpu 4 --timeout 60s` |
| Memory pressure | `stress-ng` | `stress-ng --vm 2 --vm-bytes 80% --timeout 60s` |
| Network latency | `tc` | `tc qdisc add dev eth0 root netem delay 200ms 50ms` |
| Packet loss | `tc` | `tc qdisc add dev eth0 root netem loss 10%` |
| DNS failure | `iptables` | `iptables -A OUTPUT -p udp --dport 53 -j DROP` |
| Disk full | `fallocate` | `fallocate -l 10G /tmp/fill-disk` |
| Dependency timeout | service stub or proxy | validate timeout, retry, and circuit behavior |
| Pool exhaustion | workload + limits | validate backpressure and rejection |

## Chaos Tools

| Tool | Scope | Complexity | Recommended use |
| --- | --- | --- | --- |
| Chaos Monkey | instance kill | low | simple production-safe failure drills |
| Litmus Chaos | Kubernetes | medium | cluster-native experiments |
| Gremlin | platform-wide | low | managed enterprise chaos |
| Chaos Mesh | Kubernetes | medium | open-source K8s chaos |
| Toxiproxy | network in dev/test | low | local or CI dependency faulting |
| `tc` / `netem` | Linux network | medium | controlled latency/loss injection |

### Toxiproxy Example

```python
toxiproxy.create_proxy("redis", "localhost:26379", "redis:6379")
toxiproxy.proxy("redis").add_toxic("latency", {
    "type": "latency",
    "attributes": {"latency": 1000, "jitter": 500}
})
toxiproxy.proxy("redis").add_toxic("reset", {
    "type": "reset_peer",
    "attributes": {"timeout": 0}
})
```

## Game Day Checklist

```markdown
## Pre-Game (about 1 week before)
- [ ] Hypothesis documented and reviewed
- [ ] Dashboards prepared
- [ ] Abort criteria defined
- [ ] Blast radius limited
- [ ] Participants briefed
- [ ] Stakeholders notified
- [ ] Rollback/kill switch tested

## During Game
- [ ] Baseline metrics captured (15 min steady state)
- [ ] Injection started at [time]
- [ ] Monitoring active
- [ ] Timeline recorded
- [ ] Abort criteria checked continuously

## Post-Game
- [ ] Injection stopped and system recovered
- [ ] Results compared with hypothesis
- [ ] Gaps identified
- [ ] Action items created with owners
- [ ] Findings shared
```

## Maturity Model

| Level | Practice | Example |
| --- | --- | --- |
| `1` | Ad hoc | manual experiments in staging |
| `2` | Planned | scheduled Game Days |
| `3` | Automated | chaos inside CI/CD |
| `4` | Continuous | controlled production chaos |
| `5` | Advanced | multi-failure and cascading scenarios |
