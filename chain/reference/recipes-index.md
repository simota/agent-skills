# Chain Recipe Registry

The full Recipe table for `chain`. `chain/SKILL.md` carries only the dispatch
allowlist; this file holds what is needed to *execute* a Recipe — activation
condition and the files to read first.

**Read this when** a subcommand matched and you need its row, or when scanning
what Recipes exist at all.

---

| Recipe | Subcommand | Default? | When to Use | Read First |
|--------|-----------|---------|-------------|------------|
| Skill Intake Audit | `intake` | ✓ | New third-party skill or plugin requires intake gate | `reference/intake-checklist.md` |
| Drift Detection | `audit` | | Verify pinned `sha256` against current files; detect silent updates | `_common/SECURITY.md` |
| MCP Server Pinning | `mcp` | | First install or session-start re-verification of MCP tool descriptions | `_common/SECURITY.md` |
| Unicode Scan | `scan` | | Standalone scan for Unicode Tag, bidi, or zero-width injection | `reference/unicode-tag-scan.md` |
| Recovery / Quarantine | `recover` | | Confirmed-compromised skill must be quarantined and remediation diff produced | `reference/intake-checklist.md` |
| Live Malware Scan | `malware-scan` | | Full campaign IoC sweep across live environment surfaces | `reference/supply-chain-malware-scan-procedures.md`, `reference/supply-chain-malware-ioc-database.md` |
| Campaign Scan | `campaign-scan` | | Narrow scan for a named npm/PyPI campaign | `reference/supply-chain-malware-ioc-database.md` |
| Lockfile Pin Check | `lockfile` | | Fast, read-only pre-merge check for known-bad versions and resolved URLs | `reference/supply-chain-malware-ioc-database.md` |
| Eradication Runbook | `eradicate` | | Persistence-first removal for a recent `CONFIRMED` finding | `reference/supply-chain-malware-eradication.md` |
| Rotation Runbook | `rotate` | | Dependency-ordered credential rotation after verify-clean | `reference/supply-chain-malware-eradication.md` |
| Supply-Chain Hardening | `harden` | | Lifecycle-script, cooldown, provenance, registry, and Actions controls | `reference/supply-chain-malware-scan-procedures.md` |
| Propagation Audit | `propagation` | | Unauthorized maintainer publishes, OIDC exchange, and provenance review from a clean session | `reference/supply-chain-malware-scan-procedures.md` |
