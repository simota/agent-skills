# SARIF Integration

Purpose: Use this file when Probe findings must be exported to SARIF, uploaded to GitHub Security, or enforced through machine-readable gates.

> **Currency note (2026-05)**: **SARIF v2.1.0 with Errata 01** (OASIS Standards Track Work Product, 2023-08-28, `docs.oasis-open.org/sarif/sarif/v2.1.0/errata01/os/`) is still the active OASIS standard — there is no v2.1.1 or v3.0 published. The Errata does not modify conformance, so any v2.1.0 emitter remains valid. GitHub Advanced Security `upload-sarif` accepts only the v2.1.0 schema; the action moniker is now `github/codeql-action/upload-sarif@v3` (the v2 tag is deprecated). CodeQL CLI continues to emit fingerprint data that survives partial path/line drift.

## Contents

- SARIF minimum schema
- Severity mapping
- ZAP to SARIF conversion
- GitHub Actions upload
- Gate rules

## Severity Mapping

| Source severity | SARIF level |
| --- | --- |
| `High` | `error` |
| `Medium` | `warning` |
| `Low` | `note` |
| `Informational` | `note` |

## Minimal SARIF Skeleton

```json
{
  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
  "version": "2.1.0",
  "runs": [
    {
      "tool": {
        "driver": {
          "name": "Probe Security Scanner",
          "version": "1.0.0",
          "rules": []
        }
      },
      "results": []
    }
  ]
}
```

## ZAP To SARIF Conversion

Keep rule IDs stable and severity mapping deterministic.

```python
import json
import sys

SEVERITY_MAP = {
    "High": "error",
    "Medium": "warning",
    "Low": "note",
    "Informational": "note",
}

def convert_zap_to_sarif(zap_json_path, output_path):
    with open(zap_json_path) as f:
        zap_data = json.load(f)

    sarif = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {"driver": {"name": "OWASP ZAP", "version": "2.16.0", "rules": []}},
            "results": [],
        }],
    }

    rules_added = set()
    for site in zap_data.get("site", []):
        for alert in site.get("alerts", []):
            rule_id = f"ZAP-{alert['pluginid']}"
            if rule_id not in rules_added:
                sarif["runs"][0]["tool"]["driver"]["rules"].append({
                    "id": rule_id,
                    "name": alert["name"],
                    "shortDescription": {"text": alert["name"]},
                    "fullDescription": {"text": alert.get("desc", "")},
                    "help": {"text": alert.get("solution", "")},
                })
                rules_added.add(rule_id)

            for instance in alert.get("instances", []):
                sarif["runs"][0]["results"].append({
                    "ruleId": rule_id,
                    "level": SEVERITY_MAP.get(alert["riskdesc"].split()[0], "note"),
                    "message": {"text": f"{alert['name']} at {instance.get('uri', 'unknown')}"},
                    "locations": [{
                        "physicalLocation": {
                            "artifactLocation": {"uri": instance.get("uri", "")},
                            "region": {"startLine": 1},
                        }
                    }],
                })

    with open(output_path, "w") as f:
        json.dump(sarif, f, indent=2)

if __name__ == "__main__":
    convert_zap_to_sarif(sys.argv[1], sys.argv[2])
```

## GitHub Security Upload

```yaml
name: Security Scan with SARIF

on:
  pull_request:
  push:
    branches: [main]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v4
      - name: Upload SARIF to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: security-results.sarif
          category: probe-security-scan
```

## ZAP Rule Gate Example

```tsv
# Rule ID	Action	Description
10010	IGNORE	Cookie No HttpOnly Flag (known false positive)
10020	WARN	X-Frame-Options Header Not Set
10021	FAIL	X-Content-Type-Options Header Missing
40012	FAIL	Cross Site Scripting (Reflected)
40014	FAIL	Cross Site Scripting (Persistent)
40018	FAIL	SQL Injection
90019	FAIL	Server Side Include
```

## Usage Rules

- Export only validated or clearly labeled findings.
- Keep `ZAP-{pluginid}` stable for repeatability.
- Use SARIF for integration, not as a substitute for the human-readable report.
- Store known false-positive suppressions in version-controlled rules, not in ad hoc ignore lists.
