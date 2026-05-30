<!--
Paste the block below into the target project's CLAUDE.md (or AGENTS.md).
This is what makes {{RULE_NOUN_PLURAL}} ENFORCED: every agent loads them before domain work.
-->

## {{KIT_NAME}} {{RULE_NOUN_PLURAL}} (enforced)

This project learns {{SIGNAL_NOUN_PLURAL}} into durable {{RULE_NOUN_PLURAL}} under `{{DOMAIN_DIR}}/`. The {{RULE_NOUN}} files are the source of truth.

- **Before any {{DOMAIN_DIR}} work**, scan `{{DOMAIN_DIR}}/rules/INDEX.md` by tag, then read `{{DOMAIN_DIR}}/rules/core.md` + the matching layer file. Treat every `accepted` {{RULE_NOUN}} as a hard constraint (ignore the `## Archive` section). Where a `Check:` is set, satisfy it.
- **When a {{SIGNAL_NOUN}} arrives**, run the loop in `{{DOMAIN_DIR}}/README.md` (CAPTURE → ANALYZE → REVIEW → PROMOTE → ENFORCE). New {{RULE_NOUN_PLURAL}} require **human approval** at REVIEW before binding — never self-promote, even in AUTORUN. `/nexus` orchestrates the chain.
- **PR review gate (mandatory):** verify the diff violates no accepted {{RULE_NOUN}}; a violation blocks merge until fixed or human-waived. `Check:`-backed rules are machine-verifiable; the rest are reviewer judgment. A violation revealing a missing rule → append to `{{DOMAIN_DIR}}/{{SIGNAL_LOG}}` (`source: review`).

Full mechanism: `{{DOMAIN_DIR}}/README.md` · Agent procedure: `{{DOMAIN_DIR}}/AGENT_GUIDE.md`.
