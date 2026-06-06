# Snort / Suricata Network Detection Reference

Purpose: Author network-layer detection rules in Snort 3 and Suricata dialects, map them to MITRE ATT&CK Network techniques, and wire the resulting EVE JSON alerts into the SIEM. The `snort` Recipe covers rule authoring, profiling, ET Open community rule management, and FP-aware threshold tuning. It does not cover host-process telemetry or incident response triage — those belong to `sigma` and Triage respectively.

For shared Sigma / YARA rule structure, modifiers, and ATT&CK coverage mapping templates, see `detection-patterns.md`. This file covers **network-layer (Snort 3 / Suricata) specifics only** — `fast_pattern` anchoring, EVE JSON event shape, ET Open rule pinning, rule performance profiling, and Snort/Suricata dialect differences.

## Scope Boundary

- **Vigil `snort`**: Network sensor rule authoring (Snort 3 / Suricata), flow / file / dns / tls keyword usage, EVE JSON shape, ET Open management, rule performance.
- **Vigil `sigma`** (adjacent): Host-process / endpoint / cloud-audit detection in Sigma v2.1+. Process creation, registry, file, command-line — not wire traffic.
- **Sentinel** (adjacent): Static code-level security scanning (SAST, secrets, CVE). No packet capture, no runtime traffic inspection.
- **Breach** (adjacent): Red-team attack scenarios and C2 infrastructure design. Breach *generates* the traffic, Vigil `snort` *detects* it.
- **Triage** (adjacent): Incident first response after a Snort alert fires. Triage owns the response playbook execution; `snort` owns the rule that triggered it.

If the question is "what wire-level signature catches this?" → `snort`. If it is "what host artifact catches this?" → `sigma`. If it is "what does the SOC do after it fires?" → `playbook` or Triage.

## Rule Authoring Patterns

| Pattern | Keyword anchors | Use when |
|---------|-----------------|----------|
| Signature match | `content`, `pcre`, `fast_pattern` | Known payload bytes (exploit, C2 beacon, malware string) |
| Flow-aware | `flow:established,to_server`, `flowbits` | Stateful session logic, multi-step exchanges |
| Protocol field | `http.uri`, `http.user_agent`, `dns.query`, `tls.sni`, `tls.cert_subject` | Application-layer field precision |
| File extraction | `file.data`, `file.name`, `filemagic` | Inline malware sample classification, pairs with YARA |
| Rate / threshold | `threshold: type both, track by_src, count N, seconds T` | Scan / brute-force / enumeration patterns |
| Anomaly | Suricata Lua scripts, `luajit`, `datarep` | Baseline deviation, reputation scoring |

### Snort 3 rule skeleton (ATT&CK T1071.001 — Web C2)

```
alert http (
  msg:"ATTACK T1071.001 Suspicious Beacon to Rare TLD";
  flow:established, to_server;
  http.uri; content:"/api/ping"; fast_pattern;
  http.user_agent; content:"python-requests"; nocase;
  http.host; pcre:"/\.(xyz|top|tk)$/i";
  metadata: service http, mitre_attack T1071.001;
  classtype:trojan-activity;
  sid:1000001; rev:1;
)
```

### Suricata dialect (TLS SNI-based C2 detection, ATT&CK T1573.002)

```
alert tls any any -> any any (
  msg:"ATTACK T1573.002 Suspicious TLS SNI to Known C2 Domain";
  tls.sni; content:"badc2"; nocase; endswith;
  flow:established, to_server;
  threshold: type limit, track by_src, count 1, seconds 300;
  metadata: mitre_attack T1573.002;
  sid:2000001; rev:1;
)
```

### DNS tunneling (ATT&CK T1071.004)

```
alert dns any any -> any any (
  msg:"ATTACK T1071.004 DNS Tunneling — Abnormally Long Subdomain";
  dns.query; pcre:"/^[a-zA-Z0-9]{60,}\./";
  threshold: type both, track by_src, count 20, seconds 60;
  metadata: mitre_attack T1071.004;
  sid:3000001; rev:1;
)
```

## EVE JSON Event Shape

Every Suricata alert lands in EVE JSON. Downstream SIEM parsers must expect at least:

```json
{
  "timestamp": "2026-04-24T09:00:00.000Z",
  "event_type": "alert",
  "src_ip": "10.0.0.5", "dest_ip": "203.0.113.42",
  "src_port": 54321, "dest_port": 443,
  "proto": "TCP", "app_proto": "tls",
  "alert": {
    "action": "allowed", "signature_id": 2000001,
    "signature": "ATTACK T1573.002 Suspicious TLS SNI ...",
    "category": "Trojan Activity", "severity": 2,
    "metadata": {"mitre_attack": ["T1573.002"]}
  },
  "tls": {"sni": "badc2.example.xyz", "version": "TLSv1.3"}
}
```

Ingest with Filebeat / Vector / Logstash; normalize to ECS fields (`source.ip`, `destination.ip`, `url.domain`) so downstream Sigma correlation works.

## Rule Profiling and Performance

Noisy or expensive rules kill sensor throughput. Profile before deploying.

| Tool | Output | Action threshold |
|------|--------|------------------|
| `suricata --engine-analysis` | Per-rule inspection cost estimate | Flag rules without `fast_pattern` anchor |
| `suricata -k none --rule-perf` | Per-rule micro-benchmark (ticks, checks, matches) | Refactor if avg ticks > 500 on production traffic sample |
| Snort 3 `profiler` module | Module/rule timing breakdown | Drop rules in top 1% of cost unless TP-critical |
| Suricata stats.log | `detect.alert`, `decoder.drop`, `flow.memuse` | Investigate drops > 0.1% — blind spots |

Always anchor with `fast_pattern` on the most selective content token; never use unanchored `pcre` as the first match.

## ET Open Community Rule Management

ET Open = 40k+ free rules, but pulling them raw causes alert fatigue.

1. **Pin by version**, not `HEAD` — `suricata-update --sources ...` with a locked release tag.
2. **Disable by tag**, not by sid — `suricata-update disable-conf` on `policy-balanced` / unused protocols.
3. **Enable by category, test in staging** — never push `enable-all` to production.
4. **Measure FP per category for 7 days** before production promotion; categories like `ET POLICY`, `ET INFO` are notoriously noisy.
5. **Local overrides live in a separate file** — never edit upstream `.rules` files (will be clobbered by next update).

## Anti-Patterns

- Using unanchored `pcre` as the primary matcher (kills throughput, often unnecessary).
- Omitting `flow:` on TCP rules (matches orphaned packets, inflates FPs).
- Copying ET Open rules without per-environment tuning (asset baselines, internal IP ranges, user agents).
- Skipping MITRE ATT&CK metadata in `metadata:` keyword (breaks coverage mapping with `coverage` Recipe).
- Tuning by raising severity instead of fixing match logic (hides noise, same FP volume).
- Writing rules without sensor placement context (internal-to-internal vs egress vs ingress changes what "suspicious" means).
- Shipping rules without a matching SIEM parser update (EVE JSON schema drift silently breaks downstream correlation).

## Handoff / Next Steps

- **To `coverage`**: submit the new sid + ATT&CK Network technique ID so the coverage matrix updates.
- **To `playbook`**: pair every high-severity sid with a SOC response step (who investigates, what pcap to pull, what containment).
- **To Triage**: supply packet capture (`pcap-log`) path and EVE JSON alert fields for incident scoping.
- **To Beacon**: push sensor throughput / drop metrics to observability so rule-load regressions are caught as SLO burns.
- **To Breach (Purple Team)**: request known-bad pcap replays (e.g., Atomic Red Team network variants) for true-positive validation before production promotion.
