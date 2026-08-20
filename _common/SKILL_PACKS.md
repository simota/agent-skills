# Skill Packs

> **Tier:** `authoring` — activates when creating or auditing skills, not during user work. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

Skill membership matrix for selective enablement across the 90-skill global ecosystem. This repository also carries three project-local extensions (`orbit`, `lore`, `darwin`) registered in `_common/PROJECT_LOCAL_SKILLS.md`.

## Why this exists

Anthropic guidance is **8-12 skills** before "context tax" (token overhead per turn) starts to dominate; routing degradation begins in the **dozens**, and a **15,000-character cap** on the available skills list is a hard ceiling. This repository's 93 packages (90 global + 3 project-local) exceed all three thresholds when loaded together.

This file defines **11 Packs** (overlapping subsets of the ecosystem) so that any single workstream can enable ~20-30 skills instead of the full 90 global skills. Selective enablement is driven by the Claude Code `skills` filter in `~/.claude/settings.json` (`"all"` / `[list]` / `[]`); Codex CLI and agy use equivalent allowlist mechanisms when available.

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
| `web-dev` | `core + web + design` | 33 |
| `mobile-dev` | `core + mobile + design` | 27 |
| `security` | `core + security` | 17 |
| `growth` | `core + growth + research` | 34 |
| `infra-ops` | `core + infra` | 28 |
| `research` | `core + research` | 28 |
| `package-author` | `core + package-gen + design + research` | 51 |
| `skill-meta` | `core + skill-meta` | 12 |
| `incident-response` | `core + chain` | 9 |
| `legal-jp` | `core + canon` | 9 |
| `personal-env` | `core + hone` | 9 |
| `ai-cli-admin` | `core + hone` | 9 |
| `all` | `"all"` (no filter) | 90 global; this repository additionally discovers 3 project-local skills |

---

## Packs

### `core` (always-on, 8 skills)

**Purpose:** orchestration + universal investigation/implementation/review primitives required for any workstream.

**Members:** `nexus`, `sherpa`, `scout`, `builder`, `radar`, `zen`, `guardian`, `compass`

**Triggers:** loaded unconditionally.

### `skill-meta` (ecosystem authoring and governance, 4 skills)

**Purpose:** explicit maintenance of skill packages, project-local operating layers, format compliance, and portfolio retention. This Pack is not loaded for ordinary product work.

**Members:** `architect`, `gauge`, `prune`, `sigil`

**Triggers:** `create skill`, `design skill`, `skill audit`, `skill compliance`, `skill ecosystem`, `merge skill`, `sunset skill`, `project-local skill`, `skill routing`.

---

### `web` (web frontend + backend, 21 skills)

**Purpose:** browser-tier feature work — React/Vue/Svelte/Next.js, API design, perf, E2E.

**Members:** `voyager`, `pixel`, `palette`, `frame`, `forge`, `artisan`, `atelier`, `flow`, `bolt`, `atlas`, `gateway`, `prose`, `funnel`, `growth`, `ink`, `vector`, `canvas`, `muse`, `vision`, `vitrine`, `polyglot`

**Triggers:** `react`, `vue`, `svelte`, `next.js`, `frontend`, `web`, `landing page`, `e2e`, `playwright`, `cypress`, `webdriver`, `css`, `html`, `tailwind`, `api design`, `openapi`, `rest`, `graphql`, `i18n`, `l10n`, `internationalization`, `localization`, `intl api`, `translation key`, `bot framework`

---

### `mobile` (iOS/Android/macOS native + cross-platform, 5 skills)

**Purpose:** pure-native app development — iOS/Android mobile (Swift/SwiftUI, Kotlin/Compose) **and macOS desktop** (SwiftUI for Mac / AppKit) — plus cross-platform (RN/Flutter/KMP/CMP) and store/direct release. Named `mobile` for backward compatibility with the `mobile-dev` profile; scope is native-app, not mobile-only.

**Members:** `native`, `port`, `voyager`, `forge`, `frame`

**Triggers:** `ios`, `android`, `macos`, `mac app`, `swift`, `swiftui`, `appkit`, `kotlin`, `jetpack compose`, `xcuitest`, `appium`, `detox`, `maestro`, `react native`, `flutter`, `kmp`, `cmp`, `liquid glass`, `material 3`, `app store`, `mac app store`, `play store`, `notarization`, `developer id`, `sparkle`, `menu bar app`, `entitlements`, `xpc`

---

### `security` (SAST + DAST + crypto + compliance, 9 skills)

**Purpose:** static + dynamic security analysis, threat modeling, crypto, privacy, compliance, supply-chain.

**Members:** `sentinel`, `probe`, `attest`, `crypt`, `cloak`, `vigil`, `breach`, `chain`, `canon`

**Triggers:** `security`, `cve`, `owasp`, `sast`, `dast`, `pentest`, `threat model`, `red team`, `purple team`, `mitre`, `sigma`, `yara`, `cryptography`, `tls`, `kms`, `pii`, `gdpr`, `ccpa`, `soc2`, `pci-dss`, `hipaa`, `iso 27001`, `supply chain audit`

---

### `ai-eval` (LLM eval + observability + multi-engine review, 12 skills)

**Purpose:** LLM/agent evaluation, multi-engine review, observability, reliability eng, failure mode analysis.

**Members:** `judge`, `magi`, `attest`, `oracle`, `chisel`, `beacon`, `mend`, `siege`, `omen`, `ripple`, `void`, `matrix`

**Triggers:** `llm`, `rag`, `prompt engineering`, `prompt specification`, `vague prompt`, `ai safety`, `evaluation`, `eval`, `slo`, `sli`, `observability`, `tracing`, `incident`, `chaos`, `mutation testing`, `load test`, `pre-mortem`, `race condition`, `memory leak`, `deadlock`, `multi-engine review`, `manual qa`, `testrail`, `zephyr`, `xray`, `qase`, `bva`, `equivalence class`, `combinatorial`, `coverage matrix`, `test data`, `fixture`, `factory pattern`

---

### `growth` (product growth + analytics + LP, 14 skills)

**Purpose:** funnel/LP optimization, A/B testing, retention, KPI design, persona-driven UX validation.

**Members:** `pulse`, `experiment`, `funnel`, `ledger`, `compete`, `voice`, `echo`, `cast`, `field`, `trace`, `saga`, `spark`, `rank`, `growth`

**Triggers:** `kpi`, `a/b test`, `experiment`, `funnel`, `landing page`, `cro`, `seo`, `geo`, `retention`, `churn`, `nps`, `cohort`, `session replay`, `persona`, `cognitive walkthrough`, `user feedback`, `cost optimization`, `finops`, `competitive analysis`, `prioritization`, `ice`, `rice`, `wsjf`, `moscow`

---

### `infra` (DevOps + DB + scheduling + repo ops, 16 skills)

**Purpose:** infrastructure provisioning, CI/CD, observability, DB design, scheduling, repo health.

**Members:** `beacon`, `mend`, `gear`, `scaffold`, `triage`, `trail`, `launch`, `schema`, `tuner`, `seek`, `stream`, `weave`, `shift`, `grove`, `sweep`, `rally`

**Triggers:** `terraform`, `cloudformation`, `pulumi`, `docker`, `kubernetes`, `gha`, `github actions`, `ci/cd`, `pipeline`, `cron`, `timezone`, `dst`, `retry`, `backoff`, `db schema`, `migration`, `index`, `slow query`, `etl`, `kafka`, `airflow`, `dbt`, `multi-tenant`, `search engine`, `vector db`, `state machine`, `saga`, `regex`, `dsl`, `parser`, `repo structure`, `dead code`, `cli dev`, `tui`, `linter`, `test runner`, `build tool`, `slack bot`, `discord bot`, `webhook`, `websocket`, `c4 model`, `structurizr`

---

### `design` (design system + visual + media, 16 skills)

**Purpose:** design system construction, visual asset generation, slide/video production, brand work.

**Members:** `muse`, `vision`, `atelier`, `canvas`, `frame`, `vitrine`, `palette`, `prose`, `flow`, `pixel`, `forge`, `artisan`, `ink`, `saga`, `cue`, `stage`

**Triggers:** `design system`, `design tokens`, `figma`, `figjam`, `figma make`, `storybook`, `mermaid`, `draw.io`, `ascii diagram`, `svg`, `icon`, `pixel art`, `3d`, `meshy`, `tripo`, `slide`, `marp`, `reveal.js`, `slidev`, `keynote`, `presentation`, `notebooklm`, `video`, `screencast`, `cli demo`, `vhs`, `terminalizer`, `asciinema`, `audio`, `bgm`, `sfx`, `voice synthesis`, `aituber`, `vtuber`, `game design`, `gdd`

---

### `research` (user research + discovery + brainstorming + advisory, 18 skills)

**Purpose:** discovery-side work — user research, brainstorming, strategic decisions, and prose authoring.

**Members:** `field`, `lens`, `cast`, `voice`, `echo`, `trace`, `compete`, `spark`, `flux`, `omen`, `magi`, `rank`, `tome`, `scribe`, `void`, `quill`, `saga`, `pdm`

**Triggers:** `user research`, `interview`, `usability test`, `persona`, `journey map`, `jtbd`, `brainstorm`, `ideate`, `reframe`, `assumption challenge`, `pre-mortem`, `deliberation`, `prioritization`, `mental models`, `strategy simulation`, `yagni`, `scope cut`, `documentation`, `jsdoc`, `tsdoc`, `tome`

---

### `package-gen` (document-package generation, 29 skills)

**Purpose:** end-to-end document package production via the `package` Recipe (12 domain presets — startup / career / learning / hiring / local-gov / etc.). Heavy union with `research`, `design`, and `core`.

**Members:** `scribe`, `tome`, `quill`, `rank`, `spark`, `magi`, `void`, `canon`, `prose`, `saga`, `pulse`, `cast`, `field`, `echo`, `voice`, `compete`, `attest`, `judge`, `cloak`, `vigil`, `stage`, `cue`, `vitrine`, `pixel`, `artisan`, `frame`, `muse`, `palette`, `vision`

**Triggers:** `business plan`, `venture`, `mvp dossier`, `pitch package`, `documentation package`, `package`, `startup dossier`, `domain preset`, `traceability matrix`, `feature_id`, `f-001`

## Optional global add-ons

The following skills remain globally installed but are excluded from broad domain Packs. Load their dedicated profile only when the named environment or risk surface is active.

| Profile | Skills | Trigger anchors | Activation boundary |
|---------|--------|-----------------|---------------------|
| `incident-response` | `chain` | `npm worm`, `Shai-Hulud`, `S1ngularity`, `malware eradication`, `IoC campaign` | Named supply-chain campaign or confirmed malware-response work |
| `legal-jp` | `canon` | `Tokushoho`, `特商法`, `APPI legal review`, `Japanese ToS` | Japanese ToS, Privacy Policy, APPI, or Tokushoho review |
| `personal-env` | `hone` | `dotfiles`, `zsh`, `tmux`, `neovim`, `AppleScript`, `JXA` | Personal dotfiles or macOS Apple Events automation |
| `ai-cli-admin` | `hone` | `Codex config`, `Claude Code hooks`, `agy config`, `AI CLI audit` | AI CLI configuration audit or Claude Code hook administration |

## Project-local extensions

`orbit`, `lore`, and `darwin` are not members of global Packs or profiles. They are available only inside this repository through `.claude/skills/` and `.agents/skills/`; availability and fallback rules live in `_common/PROJECT_LOCAL_SKILLS.md`.

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
2. Architect adds the skill to **at least one** Pack here, or records a justified optional/explicit/project-local placement, and emits `ARCHITECT_TO_NEXUS_HANDOFF` so Nexus's CLASSIFY can adapt.
3. If a pack would grow beyond 30 members, split it (e.g. `infra` → `infra-build` + `infra-data` + `infra-ops`).

When a skill is removed or merged:
- Remove from every pack listing here in the same commit.

## Anti-patterns to avoid

- **Loading `all` as the default.** Negates the entire point of this file. `all` is for discovery sessions only.
- **Pack-by-feature instead of pack-by-domain.** Packs are domains (web, mobile, security…), not features (auth, payment, search). A feature spans multiple packs by design.
- **Duplicating description prose across packs.** Each skill's `description:` lives in its `SKILL.md`; this file only records membership.
- **Treating specialist administration as universal.** Skill authoring, CLI administration, incident campaigns, and project-local extensions are opt-in surfaces, not `core`.
- **Skipping `core`.** Disabling `nexus` or `sherpa` breaks orchestration. Always include `core`.

## Status

This file is **v0.1 (draft membership)**. Membership was derived from each skill's `description:` field — review and revise per workstream evidence. Track corrections in `.agents/PROJECT.md` and propagate to this file.
