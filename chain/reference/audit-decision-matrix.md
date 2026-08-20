# Chain Audit Decision Matrix

Moved out of `chain/SKILL.md` so it loads when it is needed rather than on
every invocation. The text is unchanged.

---

## Audit Decision Matrix

| Finding | Severity | Default action | Escalate to |
|---------|----------|----------------|-------------|
| Unicode Tag codepoint in any file | `P0` | `REJECT` + `QUARANTINE` | triage |
| `curl ... | bash`, `wget ... | sh`, `eval $(...)` in bundled script | `P0` | `REJECT` | triage |
| `~/.ssh`, `~/.aws`, `~/.npmrc`, `~/.netrc` read without declaration | `P0` | `REJECT` | triage |
| `settings.json` mutation that changes `permissions` | `P0` | `REJECT` + `QUARANTINE` | triage |
| Project-local `.claude/settings.json` `hooks` parsed or executed **before** the trust prompt is answered | `P0` | `REJECT` | triage |
| Path containment checked **before** symlinks are resolved (validation sees the link, not its target) | `P0` | `REJECT` | triage |
| Frontmatter contains custom keys outside `name` / `description` | `P1` | `REJECT` (forward-compat) | maintainer |
| Bundled binary without provenance attestation | `P1` | `REJECT` until provenance provided | sentinel |
| Outbound HTTP to non-allowlisted host | `P1` | `REJECT` until network allowlist updated | maintainer |
| `sha256` mismatch vs pinned manifest | `P1` | `BLOCK` + investigate diff | maintainer |
| MCP tool description changed since pin | `P1` | `BLOCK` tool until reviewed | maintainer |
| Capability declared in body but tool calls observed go beyond | `P2` | `FLAG` + require capability update | maintainer |
| External URL in SKILL.md resolves to executable content | `P2` | `FLAG` + require static replacement | maintainer |
| Bidi-override codepoint outside allowlisted i18n context | `P2` | `FLAG` | maintainer |

Severity rules:
- `P0` always rejects and quarantines.
- `P1` rejects until remediated by maintainer.
- `P2` flags but may pass with explicit override and journaled rationale.
