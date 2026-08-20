# Breach Recipe Registry

The full Recipe table for `breach`. `breach/SKILL.md` carries only the dispatch
allowlist; this file holds what is needed to *execute* a Recipe — activation
condition and the files to read first.

**Read this when** a subcommand matched and you need its row, or when scanning
what Recipes exist at all.

---

| Recipe | Subcommand | Default? | When to Use | Read First |
|--------|-----------|---------|-------------|------------|
| Attack Scenario | `scenario` | ✓ | Attack scenario and kill-chain design — signals `attack scenario` / `kill chain` / `pentest plan` / `WAF bypass` / `control validation` | `reference/attack-playbooks.md` |
| Threat Model | `threat-model` | | STRIDE / PASTA / Attack Trees — signals `threat model` / `attack surface` / `entry point` / `exposure`. Per-engagement models; **never reuse templates** | `reference/threat-modeling.md` |
| Purple Team | `purple` | | Red/Blue coordination — signals `purple team` / `detection validation` / `blue team`; outputs exercise plan + detection rules | `reference/attack-playbooks.md` |
| AI/LLM Red Team | `ai-red` | | AI/LLM red team — signals `prompt injection` / `jailbreak` / `agentic risk` / `RAG poisoning` / `prompt leakage` / `MAESTRO` / `agent skill` / `tool registry`. Multi-turn chains against the deployed pipeline (RAG, tools, MCP, plugins) under OWASP LLM + Agentic Top 10, ATLAS, MAESTRO, NIST AI 100-2 E2025; Garak / PyRIT for automation | `reference/ai-red-teaming.md` |
| Phishing Campaign | `phishing` | | Authorized campaign design — pretexting, landing-page clones, MFA fatigue, quishing, OAuth consent phishing, SPF/DKIM/DMARC evasion, awareness-training integration | `reference/phishing-campaign-design.md` |
| Supply Chain Attack | `supply` | | Dependency confusion, typosquatting, build-tool compromise, SBOM analysis, SLSA provenance, in-toto attestation, registry pinning | `reference/supply-chain-attack-design.md` |
| Social Engineering | `social` | | Vishing, smishing, tailgating, OSINT pretexting, insider threat, BEC, deepfake voice/video; behavioral, not code-centric | `reference/social-engineering-design.md` |
