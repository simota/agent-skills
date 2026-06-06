# Skill Packs

Skill membership matrix for selective enablement across the 124-skill ecosystem.

## Why this exists

Anthropic guidance is **8-12 skills** before "context tax" (token overhead per turn) starts to dominate; routing degradation begins in the **dozens**, and a **15,000-character cap** on the available skills list is a hard ceiling. This repository's 124 skills exceed all three thresholds.

This file defines **10 Packs** (overlapping subsets of the ecosystem) so that any single workstream can enable ~20-30 skills instead of the full 134. Selective enablement is driven by the Claude Code `skills` filter in `~/.claude/settings.json` (`"all"` / `[list]` / `[]`); Codex CLI and agy use equivalent allowlist mechanisms when available.

**Sources:**
- claude.com/blog/lessons-from-building-claude-code-how-we-use-skills (8-12 sweet spot, context tax)
- platform.claude.com/docs/agents-and-tools/agent-skills/overview (skill filter spec)
- platform.claude.com/docs/agents-and-tools/agent-skills/best-practices (vague descriptions + dozens of skills → wrong selection)
- claudefa.st/blog/guide/mechanics/skill-listing-budget (`skillListingBudgetFraction`, `skillListingMaxDescChars`, `/skills` picker)

## Pack design rules

1. **Overlapping membership is allowed.** A skill may belong to multiple packs; union when multiple packs are enabled.
2. **`core` is always-on.** Loaded regardless of which other packs are active.
3. **Pack size target: 20-30 skills.** A single pack must stay under the Anthropic guidance for "dozens" — keep the working set narrow.
4. **Domain trigger words.** Each pack lists English anchor keywords so Nexus CLASSIFY can auto-suggest a pack from a free-form request.
5. **No silent demotion.** If the active packs do not cover a request, Nexus must surface "pack mismatch" rather than route to a fallback skill.

## Active-pack profiles

Each profile sets the Claude Code `skills` field. Use one at a time per workspace; switch with `/nexus pack <name>` (planned subcommand) or by editing `settings.json` directly.

| Profile | Packs active | Total skills (approx) |
|---------|-------------|----------------------|
| `web-dev` | `core + web + design` | ~50 |
| `mobile-dev` | `core + mobile + design` | ~30 |
| `security` | `core + security` | ~25 |
| `growth` | `core + growth + research` | ~50 |
| `infra-ops` | `core + infra` | ~40 |
| `research` | `core + research` | ~35 |
| `package-author` | `core + package-gen + design + research` | ~75 |
| `all` | `"all"` (no filter) | 124 (debugging / discovery only) |

---

## Packs

### `core` (always-on, ~11 skills)

**Purpose:** orchestration + universal investigation/implementation/review primitives + skill-meta governance required for any workstream.

**Members:** `nexus`, `sherpa`, `scout`, `builder`, `radar`, `zen`, `guardian`, `compass`, `architect`, `gauge`, `prune`, `sigil`, `titan`

**Triggers:** loaded unconditionally.

---

### `web` (web frontend + backend, ~22 skills)

**Purpose:** browser-tier feature work — React/Vue/Svelte/Next.js, API design, perf, E2E.

**Members:** `voyager`, `pixel`, `palette`, `frame`, `forge`, `artisan`, `atelier`, `flow`, `bolt`, `atlas`, `gateway`, `prose`, `funnel`, `bazaar`, `growth`, `ink`, `dot`, `vector`, `canvas`, `muse`, `vision`, `vitrine`, `polyglot`, `relay`

**Triggers:** `react`, `vue`, `svelte`, `next.js`, `frontend`, `web`, `landing page`, `e2e`, `playwright`, `cypress`, `webdriver`, `css`, `html`, `tailwind`, `api design`, `openapi`, `rest`, `graphql`, `i18n`, `l10n`, `internationalization`, `localization`, `intl api`, `translation key`, `bot framework`

---

### `mobile` (iOS/Android native + cross-platform, ~7 skills)

**Purpose:** pure-native (Swift/SwiftUI, Kotlin/Compose) + cross-platform (RN/Flutter/KMP/CMP) + store release.

**Members:** `native`, `port`, `snap`, `voyager`, `forge`, `frame`

**Triggers:** `ios`, `android`, `swift`, `swiftui`, `kotlin`, `jetpack compose`, `xcuitest`, `appium`, `detox`, `maestro`, `react native`, `flutter`, `kmp`, `cmp`, `liquid glass`, `material 3`, `app store`, `play store`

---

### `security` (SAST + DAST + crypto + compliance, ~12 skills)

**Purpose:** static + dynamic security analysis, threat modeling, crypto, privacy, compliance, supply-chain.

**Members:** `sentinel`, `probe`, `attest`, `crypt`, `cloak`, `vigil`, `breach`, `cull`, `chain`, `canon`, `oath`, `clause`

**Triggers:** `security`, `cve`, `owasp`, `sast`, `dast`, `pentest`, `threat model`, `red team`, `purple team`, `mitre`, `sigma`, `yara`, `cryptography`, `tls`, `kms`, `pii`, `gdpr`, `ccpa`, `soc2`, `pci-dss`, `hipaa`, `iso 27001`, `supply chain`, `npm worm`, `malware`

---

### `ai-eval` (LLM eval + observability + multi-engine review, ~12 skills)

**Purpose:** LLM/agent evaluation, multi-engine review, observability, reliability eng, failure mode analysis.

**Members:** `judge`, `magi`, `attest`, `oracle`, `beacon`, `mend`, `siege`, `omen`, `ripple`, `void`, `matrix`, `mint`

**Triggers:** `llm`, `rag`, `prompt engineering`, `ai safety`, `evaluation`, `eval`, `slo`, `sli`, `observability`, `tracing`, `incident`, `chaos`, `mutation testing`, `load test`, `pre-mortem`, `race condition`, `memory leak`, `deadlock`, `multi-engine review`, `manual qa`, `testrail`, `zephyr`, `xray`, `qase`, `bva`, `equivalence class`, `combinatorial`, `coverage matrix`, `test data`, `fixture`, `factory pattern`

---

### `growth` (product growth + analytics + LP, ~18 skills)

**Purpose:** funnel/LP optimization, A/B testing, retention, KPI design, persona-driven UX validation.

**Members:** `pulse`, `experiment`, `funnel`, `bazaar`, `ledger`, `compete`, `voice`, `echo`, `plea`, `cast`, `field`, `trace`, `bond`, `saga`, `spark`, `rank`, `helm`, `sage`, `growth`

**Triggers:** `kpi`, `a/b test`, `experiment`, `funnel`, `landing page`, `cro`, `seo`, `geo`, `retention`, `churn`, `nps`, `cohort`, `session replay`, `persona`, `cognitive walkthrough`, `user feedback`, `cost optimization`, `finops`, `competitive analysis`, `prioritization`, `ice`, `rice`, `wsjf`, `moscow`

---

### `infra` (DevOps + DB + scheduling + repo ops, ~25 skills)

**Purpose:** infrastructure provisioning, CI/CD, observability, DB design, scheduling, repo health.

**Members:** `beacon`, `mend`, `latch`, `gear`, `pipe`, `scaffold`, `triage`, `trail`, `launch`, `hearth`, `tempo`, `schema`, `tuner`, `shard`, `seek`, `stream`, `weave`, `shift`, `grok`, `grove`, `nest`, `hone`, `sweep`, `harvest`, `rally`, `darwin`, `lore`, `orbit`, `anvil`, `relay`

**Triggers:** `terraform`, `cloudformation`, `pulumi`, `docker`, `kubernetes`, `gha`, `github actions`, `ci/cd`, `pipeline`, `dotfiles`, `zsh`, `tmux`, `neovim`, `cron`, `timezone`, `dst`, `retry`, `backoff`, `db schema`, `migration`, `index`, `slow query`, `etl`, `kafka`, `airflow`, `dbt`, `multi-tenant`, `search engine`, `vector db`, `state machine`, `saga`, `regex`, `dsl`, `parser`, `repo structure`, `dead code`, `cli config`, `cli dev`, `tui`, `linter`, `test runner`, `build tool`, `slack bot`, `discord bot`, `webhook`, `websocket`, `c4 model`, `structurizr`

---

### `design` (design system + visual + media, ~28 skills)

**Purpose:** design system construction, visual asset generation, slide/video production, brand work.

**Members:** `muse`, `vision`, `atelier`, `canvas`, `frame`, `vitrine`, `palette`, `prose`, `flow`, `pixel`, `forge`, `artisan`, `ink`, `dot`, `sketch`, `saga`, `cue`, `director`, `stage`

**Triggers:** `design system`, `design tokens`, `figma`, `figjam`, `figma make`, `storybook`, `mermaid`, `draw.io`, `ascii diagram`, `svg`, `icon`, `pixel art`, `3d`, `meshy`, `tripo`, `slide`, `marp`, `reveal.js`, `slidev`, `keynote`, `presentation`, `notebooklm`, `video`, `screencast`, `cli demo`, `vhs`, `terminalizer`, `asciinema`, `audio`, `bgm`, `sfx`, `voice synthesis`, `aituber`, `vtuber`, `game design`, `gdd`

---

### `research` (user research + discovery + brainstorming + career, ~32 skills)

**Purpose:** discovery-side work — user research, brainstorming, strategic decisions, career/learning/hiring content generation, prose authoring.

**Members:** `field`, `plea`, `lens`, `cast`, `voice`, `echo`, `trace`, `compete`, `spark`, `riff`, `flux`, `omen`, `magi`, `rank`, `ascent`, `crest`, `agora`, `guild`, `sage`, `helm`, `harvest`, `tome`, `scribe`, `accord`, `void`, `quill`, `zine`, `saga`

**Triggers:** `user research`, `interview`, `usability test`, `persona`, `journey map`, `jtbd`, `brainstorm`, `ideate`, `reframe`, `assumption challenge`, `pre-mortem`, `deliberation`, `prioritization`, `career`, `job change`, `side business`, `learning`, `curriculum`, `hiring`, `interview rubric`, `local government`, `civic`, `side project idea`, `office hours`, `advisory`, `strategy simulation`, `yagni`, `scope cut`, `documentation`, `jsdoc`, `tsdoc`, `tech blog`, `note`, `zenn`, `qiita`, `tax filing`, `tome`

---

### `package-gen` (document-package generation, ~30 skills)

**Purpose:** end-to-end document package production via the `package` Recipe (12 domain presets — startup / career / learning / hiring / local-gov / etc.). Heavy union with `research`, `design`, and `core`.

**Members:** `accord`, `scribe`, `tome`, `quill`, `rank`, `spark`, `magi`, `void`, `morph`, `canon`, `prose`, `saga`, `pulse`, `cast`, `field`, `plea`, `echo`, `voice`, `compete`, `attest`, `judge`, `clause`, `oath`, `cloak`, `vigil`, `ascent`, `agora`, `guild`, `trawl`, `stage`, `cue`, `vitrine`, `pixel`, `artisan`, `frame`, `muse`, `palette`, `vision`

**Triggers:** `business plan`, `venture`, `mvp dossier`, `pitch package`, `documentation package`, `package`, `startup dossier`, `domain preset`, `traceability matrix`, `feature_id`, `f-001`

---

## Routing protocol (Nexus CLASSIFY integration)

When `/nexus pack` is invoked or when a user request arrives:

1. **Extract domain anchors** from input (English trigger keywords above).
2. **Score packs** by trigger-keyword overlap (highest match wins; ties broken by `core + most-specific-pack`).
3. **Recommend profile** matching `## Active-pack profiles` table.
4. **Surface to user** as `Recommended profile: <name> (covers <N>/<total> matched anchors). Switch? [Y/n/customize]`.
5. **On Y** → write to `~/.claude/settings.json` `skills` array (union of pack members), reload Claude Code, log to `.agents/PROJECT.md`.

If 0 anchors match → fall through to `all` profile with `skillListingBudgetFraction: 0.02` and let Claude's built-in priority-drop handle the listing.

## Update policy

When a new skill is added (e.g. via `architect`):
1. Architect updates `CAPABILITIES_SUMMARY` for routing partners.
2. Architect adds the skill to **at least one** pack here and emits `ARCHITECT_TO_NEXUS_HANDOFF` so Nexus's CLASSIFY can adapt.
3. If a pack would grow beyond 30 members, split it (e.g. `infra` → `infra-build` + `infra-data` + `infra-ops`).

When a skill is removed or merged:
- Remove from every pack listing here in the same commit.

## Anti-patterns to avoid

- **Loading `all` as the default.** Negates the entire point of this file. `all` is for discovery sessions only.
- **Pack-by-feature instead of pack-by-domain.** Packs are domains (web, mobile, security…), not features (auth, payment, search). A feature spans multiple packs by design.
- **Duplicating description prose across packs.** Each skill's `description:` lives in its `SKILL.md`; this file only records membership.
- **Skipping `core`.** Disabling `nexus` or `sherpa` breaks orchestration. Always include `core`.

## Status

This file is **v0.1 (draft membership)**. Membership was derived from each skill's `description:` field — review and revise per workstream evidence. Track corrections in `.agents/PROJECT.md` and propagate to this file.
