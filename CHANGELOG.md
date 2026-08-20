# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added — contract-delivery checking, and every SKILL.md body under the size advisory (2026-08-20)

- **`_common/scripts/lint-contracts.py` asks whether a contract can reach a running agent.** Nothing under `_common/` loads automatically; it arrives only because a file already open names it, and a reference resolves from the skill's own directory. Neither condition was checked anywhere. CD-1 compares the spine roster in `OPERATIONAL.md` against the files declaring `Tier: spine`; CD-2 measures per-skill reachability depth; CD-3 finds contracts no skill can reach; CD-4/CD-5 catch a named path that resolves for a reader browsing the repo and to nothing for the agent; CD-6 catches a missing tier line. `--report` prints the depth table. Wired into `skill-lint.yml`, `CONTRIBUTING.md`, and the 30-day evaluation cycle.
- **Two findings it produced are fixed.** `WORK_GATE.md` declared `Tier: spine` while Contract Precedence never listed it, and `architect/` named `_templates/SKILL_TEMPLATE.md` without the symlink to reach it.
- **Every spine contract now reaches all 90 skills directly.** `OUTPUT_STYLE.md` was named by 20 skills and `WORK_GATE.md` by none; both arrived only through an intermediate document, which makes "in effect on every run" a claim the corpus did not support. Each `## Operational` section now opens with the same spine line, and the 110 pure-pointer lines it supersedes are gone. With the baseline clean, CD-2 blocks on indirect delivery.

### Changed — SKILL.md bodies moved below the 7000-token advisory (2026-08-20)

- **Corpus body total 615,994 -> 590,524 tokens, and `lint-frontmatter` reports no findings across all 90 skills.** Every reduction is a move or a verified duplicate; no section was summarised away.
- **Eighteen skills now use the Recipes escape hatch** in `_common/RECIPES.md` that only `nexus` had used: the table moves to `reference/recipes-index.md` and the SKILL.md keeps a dispatch allowlist. SKILL.md keeps what is needed to *choose*; the registry holds what is needed to *execute*.
- **Twelve Reference Maps split the way nexus splits its own** — shared-contract rows and a pointer stay, per-file read-triggers move to `reference/reference-index.md`. Rows naming a spine contract moved too, since the spine line now names those files directly.
- **Removed as duplicates:** builder's per-subcommand gate table (`recipe-verify-gates.md` carries all thirteen in fuller form), magi's per-Recipe VERIFY table (`decision-templates.md` likewise), scribe's `## Logging`, nexus's Core Rule 10 and five Reference Map rows repeating a file already named at its decision point, and the `## Git Guidelines` / `## Output Language` restatements in six skills.

### Changed — the recipe-count warning now records its review (2026-08-20)

- **`tome`'s four platform recipes folded back into `article`.** `note` / `zenn` / `qiita` / `devto` shared one reference and one activation condition, and `article` already selects the platform at FRAME — they were parameters, not recipes. All four still dispatch, as documented aliases for `article <platform>`. 16 recipes -> 12.
- **`REC04_REVIEWED` records a completed consolidation review instead of leaving a warning nobody can act on.** The 2026-08-20 review measured, per skill, how many recipes collapse onto one `Read First` set: a recipe with its own method reference is breadth, recipes sharing one reference *and* one activation condition are duplication. Only `tome` had the latter. The other nine entries carry the count reviewed and what the review found, and the exception is bounded by that count — a skill that grows past it warns again.
- **`_common/RECIPES.md` documents the exception** and the test that separates duplication from breadth, so an entry cannot be added to quiet a warning without doing the review.
- **`routing-oracle`'s two RO-3 warnings are left as warnings.** That checker's own note says a reviewed exception downgrades the message and not the severity, because RO-3 guards a correctness property — producer is not verifier — where a stale exception would hide a real defect. Both entries were re-checked against the current chains and still hold.

### Fixed — absorption residue from the 2026-08-20 consolidation (2026-08-20)

- **`magi` kept two marks of absorbing `helm`.** The Strategy Simulation row sat in the two-column Signal Keywords table instead of the five-column Recipes table, so it rendered broken and `simulate` was never registered as a Recipe. The `**vs Helm**` overlap boundary had been renamed to `**vs Magi**`, comparing Magi with Magi. `hone` carried the same defect from absorbing `anvil`.
- **One capability claim had no content behind it.** `magi` claims SWOT and Blue Ocean lenses, but `blue-ocean-strategy.md` and `strategic-calibration.md` were left behind when `helm` was absorbed — four of the six claimed lenses (PESTLE, Porter, Ansoff, BCG) had backing and those two did not. Both files are now in place.

### Removed — over-migration and a cost axis that could not work (2026-08-20)

- **Removed 34 migrated reference files that nothing referenced.** The consolidation carried 88 files into the active tree; 34 were named by no SKILL.md, no Recipe "Read First", and no other reference — a 38% orphan rate against a 7.5% corpus baseline (measured across `scout`, `judge`, `oracle`, `atlas`). The complete pre-merge sets remain in `.archive/` with restore instructions, so nothing left the repository. Two further files orphaned by the removal itself were taken in the same pass; the tree is now stable at 53 with zero dangling pointers. One file with no archive copy (`environment-autorun-schema.md`) was moved into `.archive/anvil/` rather than deleted.
- **Removed the `CST` axis from `WORK_GATE`.** It was self-assigned with no external check and no budget to measure against — `_common/TOKEN_ECONOMY.md` §5 states plainly that no per-skill cost figure is derivable here, and the axis's own definition conceded there is no "over budget" band. An axis that can only ever read ★★★★★ already meets this file's removal condition, so it was met before shipping. `WORK_GATE` is now five starred axes plus `RSK`.
- **Restored `_common/REVERSE_FEEDBACK.md` to a single tier.** Adding `rework_required` had given one file two tiers — `authoring` for most types, binding during user work for one — which the precedence model in `OPERATIONAL.md` § Contract Precedence does not support (one tier per file, stated on the line under the title). The refusal now lives entirely in `_common/HANDOFF.md` § Handoff Admission Gate, message shape included (`HANDOFF_REFUSED`, carrying the numbered condition, the receiver's `IN`, the named missing artifact, and the bounce count). `REVERSE_FEEDBACK.md` is advisory-only again and states so.

### Added — Handoff Admission Gate: quality-based send-back between agents (2026-08-20)

- `_common/HANDOFF.md` § Handoff Admission Gate lets a **receiver refuse a handoff at intake** and return it unworked. Intake is the only point where rework is cheap; once the receiver has built on a bad input, unwinding costs more than the original redo would have.
- **Five refusal conditions, all checkable against something outside the sender's account of its own work**: unresolved `RSK: risk`; a missing field or a locator that does not resolve; an `OUT` rung below the floor the change class requires (`_common/EVIDENCE_LADDER.md` `R01`–`R21`); a `Completed` item presented as `Verified`; or the receiver's own `IN` at ★★☆☆☆ or below with a named item the sender held and did not pass.
- **The sender's own stars never trigger a refusal.** `FIT`, `EVD`, `CLR`, and `CST` are self-assigned testimony with no external check, and `_common/TOKEN_ECONOMY.md` §6 forbids wiring a self-certified figure into a gate. The one star-driven condition uses the **receiver's** `IN` — an independent read of what actually arrived — and still requires naming the missing artifact.
- **One bounce per handoff edge, then escalate.** A second failure on the same condition becomes a typed residual plus a user question; there is no third attempt. When the sender cannot satisfy the refusal because the information does not exist, it converts to a `blocked-external` / `out-of-contract` residual and the receiver proceeds with the gap recorded — a chain never stalls on an unobtainable input.
- **The receiver is accountable for refusing.** A refusal answered with content already present in the original handoff is recorded as a receiver-side defect, because refusal costs the sender a full rerun. Refusal is unavailable at `Skip` tier.
- `_common/REVERSE_FEEDBACK.md` gains the `rework_required` feedback type as the message form of the gate, and its tier line now states the exception: the file is `authoring` for its advisory types, but `rework_required` binds during user work.
- `nexus/reference/output-formats.md` marks a reworked spoke `↺` in the Work Gate Matrix with the refusing skill and the missing item; Nexus arbitrates the one-bounce rule so a silently rerun step cannot report a smaller cost than it paid.
- `nexus/reference/error-handling.md` states the boundary: `L1`–`L5` owns **a step that failed**, the admission gate owns **a step that succeeded and delivered something unusable**. A refusal is not a retry — it consumes the edge's single bounce, not an attempt budget, and returns work to the sender rather than re-running it in place.

### Added — `WORK_GATE`: a per-deliverable verdict every skill emits (2026-08-20)

- `_common/WORK_GATE.md` defines six `★1–5` axes — `IN` (input quality: what the work had to go on) · `FIT` (scope match) · `EVD` (claims tied to checkable evidence) · `OUT` (output quality: the `EVIDENCE_LADDER` rung actually reached) · `CLR` (usable by the named consumer) · `CST` (effort proportional to the deliverable) — plus `RSK` (irreversible / security / privacy / unauthorized spend), which is `pass | risk` and **never starred**: a floor is not a gradient, and `★★★☆☆ safe` invites trading exposure against a well-written report. `RSK: risk` blocks completion.
- **Stars are per-axis and are never summed, averaged, or weighted.** There is no overall rating, no chain average, no gate total. A composite is what lets a bad axis be offset by good ones; `nexus/reference/quality-iteration.md` § UQS is the existing weighted composite and is explicitly not the precedent followed.
- **Bands are coarse on purpose**: assign the highest band whose *complete description* is true, the rule `nexus/reference/confidence-scoring.md` § Discrete Evidence Bands already establishes (*pseudo-precision is not evidence*). `n/a` replaces the stars and carries a reason — never rendered as ★1, never counted as ★5.
- **`IN` separates a bad brief from bad work.** ★1 `IN` with ★4 `OUT` is a good run on a poor request, and nothing in the repository could previously say so. Read as a column across a Nexus chain, a degrading `IN` is a handoff defect no single spoke's gate can show.
- **`OUT` is anchored, not self-graded**: the band is the `E0`–`E6` rung the strongest available check stands on, which a reader can inspect. It subsumes the earlier `VER` axis — `E3`+ requires an oracle independent of the producer, so "independently checked" is the ★3 boundary rather than a separate line.
- **`CST` is stated in observed counts — subagent spawns, files read/written, tool-call rounds — never in tokens.** `_common/TOKEN_ECONOMY.md` §5 is a standing limit: no per-skill token figure is derivable from this repo's data, so a token estimate would be a fabricated measurement. There is no "over budget" band because there is no budget this repository can measure.
- Wired into `_common/OPERATIONAL.md` § Completion Contract, which is `spine` tier and already reaches all 90 skills — no per-skill SKILL.md edit, and no per-skill token cost. Emission scales with the planning tier: Skip emits only `RSK` when not `pass` plus any axis at ★★ or below; Light and Full emit all seven lines.
- `nexus/reference/output-formats.md` § Work Gate Matrix renders spoke gates as skills × axes with no totals; any `RSK: risk` surfaces as a blocker at the top of the envelope.
- Closes a real gap: only 23 of 90 skills wrote code and therefore reached `CODE_QUALITY_GATE`'s `SEC` floor. The other 67 emitted no quality signal at all.
- Stated limit, in the file: stars measure process and evidence, not correctness, and four of the six (`IN`, `FIT`, `CLR`, `CST`) are self-assigned with no external check. The Complexity Budget's `removal` condition includes dropping any single axis that never leaves ★★★★★ across a `darwin` evaluation cycle.

### Changed — consolidate global roster to 90 skills (2026-08-20)

- Retired 10 low-reachability skills into broader owners, preserving their capabilities, recipes, and reference material: `trawl` → `vector`, `grok` + `anvil` (CLI/TUI) → `builder`, `anvil` (personal environment) → `hone`, `bond` → `growth`, `morph` → `scribe`, `mint` → `radar`, `relay` → `gateway`, `riff` → `flux`, `helm` → `magi`, and `tempo` → `weave`.
- Selection evidence was inbound COLLABORATION_PATTERNS partners, `nexus/reference/` routing reachability, and peer SKILL.md mentions — not description similarity. Pack membership was excluded as a retention signal after the audit found semantically broken Tier-3 assignments (`trawl` filed under `package-gen`, `mint` under `ai-eval`).
- Added 12 recipes so every absorbed capability has a reachable owner: `vector crawl`, `builder grammar`/`cli`, `growth retention`, `scribe convert`, `radar fixtures`, `gateway messaging`, `flux ideate`, `magi simulate`, `weave schedule`, `hone env`/`automate`.
- Migrated 69 reference files into namespaced subdirectories under each owner (`vector/reference/crawl/`, `magi/reference/strategy-simulation/`, …); the full pre-merge reference sets remain in `.archive/`.
- Archived the 10 source packages under `.archive/` with owner mappings, a review deadline of 2026-11-18, and explicit restoration steps.
- Updated routing, disambiguation, boundaries, project affinity, skill packs, profiles, catalogs, public documentation, and the generated Recipes directory for the 90-global + 3-project-local roster.
- Extended the task-battery stale-agent guard from 5 to 15 retired names so a reintroduced reference fails the check.

### Changed — consolidate global roster to 100 skills (2026-08-19)

- Absorbed 11 narrowly scoped skills into broader owners while preserving their recipes and reference material: `cull` → `chain`, `director` → `cue`, `harvest` → `launch`, `zine` → `tome`, `sage` + `summon` → `magi`, `sketch` → `builder`, `crest` → `compete`, `clause` → `canon`, `latch` → `hone`, and `hearth` → `anvil`.
- Archived the 11 source packages under `.archive/` with owner mappings, a retain-through date of 2026-11-17, and explicit restoration steps.
- Updated routing, skill packs, profiles, catalogs, public documentation, and the generated Recipes directory for the 100-global + 3-project-local roster.
- Clarified the active-roster counting convention and corrected stale 111/123/124-skill labels in the public catalog and contributor documentation.

### Changed — Builder reference grounding (2026-08-19)

- Replaced 15 general language, architecture, domain, frontend, implementation, and AI-coding primers with `builder/reference/implementation-policy.md`, a repository-first decision and toolchain-grounding policy.
- Rewired Builder recipes and Kotlin/Rust/Swift specialist references to preserve role-specific checklists while requiring local toolchain evidence for version-sensitive claims.
- Removed frozen chapter links and dependency defaults that could override repository conventions or drift from current primary documentation.

### Changed — skill consolidation and profile repair (2026-08-19)

- Absorbed `accord` into `scribe` as the cross-team `unified` L0-L4 recipe while preserving BDD, traceability, stakeholder, RACI, and staged-elaboration references.
- Absorbed `oath` into `canon` as regulatory compliance recipes while preserving SOC 2, PCI-DSS, HIPAA, ISO 27001, GDPR/EU AI Act, audit-readiness, vendor-risk, and Policy as Code references.
- Archived both merged-in skill packages under `.archive/` with 90-day reactivation instructions; roster 124 → 122.
- Repaired all filtered profiles after the 2026-06-06 rename set, removed the retired `mentor` entry, and added `chisel`, `loom`, and `pdm` to their declared packs.

### Added — `chisel` skill: prompt → executable specification (2026-08-18)

Closes a gap no existing skill held: taking a **supplied prompt** as the object and converting its vague wording into rules that can be executed and scored. Roster 123 → 124.

- **New skill `chisel`** (SKILL.md + 5 references): seven-class ambiguity detection (quality / quantity / explanation level / style / design / technical / judgment) plus open semantic detection for missing actors, objects, comparisons, and scope; ten dispositions (`QUANTIFY` / `BEHAVIORALIZE` / `CRITERIA` / `DECOMPOSE` / `AUDIENCE` / `CONDITION` / `DATE` / `PARAMETERIZE` / `KEEP` / `DELETE`); the Numeric Licensing Cascade against fabricated precision; role decomposition into six slots so no bare title or credential claim survives; an **ambiguity budget** so terms left open are deliberate and recorded; and an eight-item Exit Checklist that blocks delivery. Recipes: `spec` (default) / `scan` / `role` / `audit`.
- **Boundary vs `oracle`**: Oracle owns the prompt *system* — few-shot policy, structured output, versioning, eval gates, cost, and the Instruction Boundary / five-layer triage doctrine. Chisel owns the *wording of a supplied prompt* and consumes that doctrine by reference rather than restating it. Measured functional overlap ≈ 24%, under the 30% confirmation threshold.
- **Consistency with existing repo positions**: role decomposition implements nexus's "never personality adoption" for user-supplied prompts; the ambiguity budget imports `AS-09 Over-Specified Process` and the Process Constraint Tiers so that eliminating every vague term is explicitly *not* the goal; the delete test reuses `_common/MECHANISM_SELECTION.md` § Admission.

**Routing:** new `PROMPT_SPEC` task type (`Chisel`) in `nexus/reference/routing-matrix.md` (95 task types); anchors added under *Specialist Skill Anchors* in `nexus/reference/signal-keywords.md`; a four-way disambiguation entry (Chisel / Oracle / Scribe / Attest) added to `nexus/reference/agent-disambiguation.md`; `_common/BOUNDARIES.md`, `compass/reference/catalog.md`, and `architect/reference/agent-categories.md` updated; added to the `ai-eval` Skill Pack. Registered as a task type rather than a Nexus Recipe — it is a single-agent route with no chain template, like `PRIORITIZE` (Rank) or brainstorming (Riff).

### Added — Apple platform coverage: `dock` skill + perf/design-trend references (2026-07-25)

> **Superseded 2026-07-29 (`a9510248`).** `dock` was absorbed into `native` as the `macos`/`macdist` recipes and no longer exists as a standalone skill; `wield`, referenced below, was absorbed into `hearth` as `automate`. The `MACOS_NATIVE` routing chain no longer starts at `Dock`. The entry is kept verbatim as a record of what shipped on 2026-07-25 — see `_common/HARNESS_DEBT.md` § *A Record is not a derived asset*. Roster as of 2026-08-17: **123 skills**.

Closes three verified gaps in Apple-platform knowledge. Agent count 132 → 133.

- **New skill `dock`** (macOS native application development, 277-line SKILL.md + 15 references, ~3.9k lines total): SwiftUI for macOS + AppKit interop, scene/window architecture, menu bar Commands, document-based apps, NavigationSplitView layout, drag & drop / pasteboard / Services, App Sandbox + entitlements, distribution (App Store vs Developer ID, notarization, Sparkle), XPC / SMAppService helpers, Mac HIG + Liquid Glass on macOS Tahoe 26, and the Catalyst-vs-native decision. Boundary: `dock` **builds** Mac apps; `wield` **automates existing** Mac apps via AppleScript/JXA — zero functional overlap.
- **`native/reference/apple-perf.md`** (324 lines): Apple-platform performance measurement — Instruments template decision table, SwiftUI render perf, launch time, hitches, memory, concurrency cost, MetricKit/`os_signpost` field telemetry, CI perf budgets. Resolves the dangling pointer in `bolt/reference/swift-cheatsheet.md` §11, which claimed to defer SwiftUI perf to a Native reference that did not exist.
- **`vision/reference/apple-design-trends.md`** (266 lines): Apple design *direction* (as distinct from HIG's normative rules in `native/reference/ios-hig.md`) — the Liquid Glass era and its tasteful-vs-wrong uses, 6 direction archetypes, Apple Design Award pattern analysis (2025/2026 winners, multi-source verified), macOS-specific direction, cross-platform coherence, and a durability test.

**Routing:** new `MACOS_NATIVE` task type (`Dock → Radar → Vitrine → Launch`) in `nexus/reference/routing-matrix.md` (99 task types); macOS anchors added to `nexus/reference/signal-keywords.md` (§ renamed *Mobile Native Anchors* → *Native App Anchors (mobile + macOS desktop)*); `mobile` Skill Pack extended to native-app scope with `dock` + `wield` (pack name kept for `mobile-dev` profile compatibility).

### Changed — Anthropic Agent Skills official-spec alignment (2026-06-06)

- **Directory convention**: `references/` (plural) → `reference/` (singular) across all 121 skill folders. Matches Anthropic official example layout. 5,048 path references updated across 375 .md files.
- **Frontmatter `description`**: All 124 SKILL.md `description` fields rewritten to start with a gerund (`-ing` form) per official best-practices for model-invoked discovery. Third-person voice and exclusion rules preserved.

### Changed — 9 skill renames for world-view consistency

Non-metaphor / weak-metaphor names replaced with single-word metaphors that fit the established abstract-1-word convention:

| Old → New | Rationale |
|---|---|
| `researcher` → `field` | role name → fieldwork metaphor |
| `navigator` → `vector` | direct descriptor → directional intent |
| `showcase` → `vitrine` | verb compound → display case |
| `retain` → `bond` | English verb → relationship metaphor |
| `comply` → `oath` | English verb → commitment |
| `mentor` → `agora` | role name → learning marketplace |
| `husk` → `cull` | weak fit → selective eradication |
| `lure` → `bazaar` | manipulative → marketplace orchestration |
| `spider` → `trawl` | industry literal → sweep metaphor |

Git history preserved via `git mv`; all cross-references (PascalCase / paths / backticks / chain-DSL delimiters) updated. Tier 2 high-collision names (`schema` / `stream` / `growth` / `palette` / `pixel`) intentionally left as-is to avoid technical-term collisions.

### Changed — Nexus Recipe refinements

- `venture` Recipe row removed; alias only (≡ `package domain=startup`)
- `bug` / `feature` / `refactor` / `optimize` chains surface conditional steps inline (`Sherpa?`, `Muse?`, `Radar?`, `Bolt (code) / Tuner (DB)` branch)
- Hidden ~78 `classify`-only task types now explicitly documented in SKILL.md
- Chain reference Source-of-Truth hierarchy declared in Routing Quick Start
- 4 orphaned `.mmd` flow diagrams linked from corresponding recipe files

### Added

#### New Agents
- **Attest** - 仕様適合検証エージェント。仕様書から受入基準を抽出し、BDDシナリオを生成し、実装が仕様通りか敵対的に検証。CERTIFIED/CONDITIONAL/REJECTED判定を発行。5つのリファレンス（criteria-extraction, verification-methods, bdd-generation, compliance-report, adversarial-probing）を含む
- **Levy** - 日本の確定申告（所得税）をガイドするドメイン知識エージェント。所得分類・控除最適化・税額計算・e-Tax手順をフリーランス/副業サラリーマン向けに解説
- **Helm** - 財務・市場・競合データから短期/中期/長期の経営シミュレーションを実施する経営戦略特化エージェント（SWOT/PESTLE/Porter分析、シナリオプランニング）
- **Pipe** - GHAワークフロー専門エージェント（トリガー戦略、セキュリティ強化、PR自動化、Reusable Workflow設計）
- **Aether** - AITuber（AI VTuber）システムの企画から実装・運用までを一貫支援するフルスタック・オーケストレーター
- **Oracle** - AI/ML設計・評価専門エージェント（プロンプトエンジニアリング、RAG設計、LLMアプリパターン）
- **Beacon** - 可観測性・信頼性エンジニアリング専門エージェント（SLO/SLI設計、分散トレーシング）
- **Siege** - 負荷テスト・カオスエンジニアリング・レジリエンス検証専門エージェント
- **Prose** - ユーザー向けテキスト専門エージェント（マイクロコピー、エラーメッセージ、ボイス＆トーン設計）
- **Latch** - Claude Codeフック管理エージェント（PreToolUse/PostToolUse等のイベントシステム）
- **Relay** - メッセージング統合・Bot開発・リアルタイム通信の設計＋実装エージェント
- **Void** - 引き算設計エージェント。YAGNI検証、スコープカット、複雑性削減提案
- **Totem** - プロジェクトDNAプロファイラー。8次元の文化分析、逸脱検出、オンボーディングガイド
- **Matrix** - ユニバーサル組み合わせ分析エージェント。多次元軸の組み合わせ爆発を制御し、最小カバレッジセット選定・優先順位付けを担当
- **Compass** - 戦略実行モニタリング・前提条件監視・OKRカスケード。Helmのロードマップを受け取りKPI乖離を追跡
- **Refract** - 3軸（視野・視座・視点）リフレーミングエージェント。問題やアイデアを回転させ新たな洞察を生成
- **Darwin** - エコシステム自己進化オーケストレーター。プロジェクトライフサイクル検出、エージェント関連性評価、横断的知識統合

### Enhanced
- **Nexus** - 19種類のルーティングコマンドと42種類のチェーンテンプレートを追加。エージェント重複ペアの曖昧性解消ガイドも追加
- **Orbit** - Gemini TTSによるイテレーション通知（Pattern D）、スクリプト生成機能、ブランチ分離戦略、ループランナー防御パターン・リカバリ拡張、Executor Engine CLI参照、全スクリプトテンプレート拡張、macOS互換性修正
- **Guardian** - Squash最適化エンジン追加（スコアリング、グルーピング、メッセージ合成）
- **Sigil** - `.agents/skills/` サポート追加でポータブルなスキル配置が可能に
- **Bard** - エンジン・エゴアーキテクチャに刷新（Codex/Gemini/Claude各エンジンが固有の声で語る）
- **Cast** - SPEAKモード追加、Google Cloud TTSを第三のエンジンとして統合
- **Titan** - build-firstアプローチ強制。スコープ適応型チェーン、統合プロトコル・自律検証・実行ブートストラップを追加
- **Scaffold** - Terraformオペレーション、コンプライアンス、FinOps参照ドキュメントを追加
- **Hearth** - SKILL.mdと参照ドキュメントを拡充
- **Zen** - 防御的過剰検出パターンを追加
- **Grove/Sweep** - メンテナンスモード、インラインしきい値、クロススキルハンドオフパイプラインを追加
- **Void** - コード以外の全ドメイン（機能・プロセス・ドキュメント・設計・仕様・依存・設定）への引き算フレームワーク汎化
- **Voyager, Vector, Sketch** - 各SKILL.mdを包括的に改善（グレードA相当）
- **Levy** - Interaction Triggers追加（6トリガー+YAMLテンプレート）、Principles番号付きリスト化、Quick Decision判定テーブル2種追加（申告要否・事業所得vs雑所得）

### Changed
- 全エージェントのSKILL.mdを原則中心設計で最適化（コンテキスト削減、28〜91%圧縮）
- 38 SKILL.mdファイルのテンプレート一貫性を強制
- エコシステムへのPipe/Relay/Aether/Oracle/Beacon/Siege/Prose統合（Nexus, Architect, Gearのルーティング更新）
- Titanをbuild-firstエンジンとしてリビルド、参照整理

## [1.0.0] - 2025-01-15

### Added

#### New Agents
- **Artisan** - フロントエンド本番実装の職人（React/Vue/Svelte、Hooks、状態管理）
- **Vitrine** - Storybookストーリー作成・カタログ管理・Visual Regression連携
- **Vision** - クリエイティブディレクション・Design System構築
- **Probe** - セキュリティ動的テスト（DAST）・ペネトレーションテスト
- **Tuner** - DBパフォーマンス最適化・EXPLAIN ANALYZE分析
- **Field** - ユーザーリサーチ設計・インタビューガイド作成
- **Voyager** - E2Eテスト専門（Playwright/Cypress）
- **Judge** - codex reviewによるコードレビュー・PRレビュー自動化・AI幻覚検出
- **Anvil** - Terminal UI構築・CLI開発支援

#### Features
- **AUTORUN_FULL mode** - ガードレール付き完全自動実行モード
- 40種類の専門エージェント体制
- 全エージェントの使用例を完備
- タスクタイプ別チェーンテンプレート（11カテゴリ、41テンプレート）

### Enhanced
- **Vision** - 2025-2026デザイントレンド、AI設計ツール統合（Figma AI、v0、Claude）
- **Artisan** - Vue 3 Composition API、Svelte 5 Runes、スタイリング戦略ガイド
- **Vitrine** - Storybook 8対応、MDX 3ドキュメント、Figma連携
- **Builder** - TDD、Event Sourcing、CQRS、Forgeからの自動引き継ぎ

### Changed
- AUTORUN_FULLをデフォルトモードに設定
- プラットフォーム非依存に対応（Claude Code、Codex CLI、Gemini CLI等）
- エージェント境界定義の明確化（Bolt vs Tuner、Schema vs Tuner等）

### Removed
- **Roadmap** - PM向け機能のため削除
- **Insight** - Spark/Scoutに統合
- **Lens** - Canvas/Showcaseに統合
- **Fixture** - Builder/Radarに統合

## [0.9.0] - 2025-01-08

### Added
- Initial release with 35 agents
- Nexus orchestrator with AUTORUN/GUIDED modes
- Basic agent collaboration framework
- Hub & Spoke architecture

---

## Agent Categories

| Category | Count | Agents |
|----------|-------|--------|
| Orchestration | 8 | Nexus, Sherpa, Architect, Rally, Titan, Sigil, Orbit, Darwin |
| Research & Planning | 10 | Scout, Ripple, Spark, Compete, Voice, Field, Trace, Canon, Lens, Cast |
| Decision & Strategy | 3 | Magi, Helm, Accord |
| Git/PR Management | 4 | Guardian, Harvest, Launch, Trail |
| Quality Assurance | 10 | Radar, Voyager, Sentinel, Probe, Judge, Zen, Sweep, Siege, Void, Attest |
| Implementation | 3 | Builder, Artisan, Forge |
| AI/ML | 1 | Oracle |
| Performance | 2 | Bolt, Tuner |
| Observability/SRE | 2 | Beacon, Mend |
| UI/UX | 8 | Vision, Palette, Muse, Flow, Echo, Vitrine, Prose, Frame |
| Documentation | 3 | Scribe, Quill, Morph |
| Visualization | 2 | Canvas, Sketch |
| Architecture | 4 | Atlas, Horizon, Gateway, Grove |
| Communication | 1 | Relay |
| Data | 2 | Schema, Stream |
| DevOps | 6 | Anvil, Gear, Scaffold, Hearth, Latch, Pipe |
| i18n | 1 | Polyglot |
| Growth | 2 | Growth, Bond |
| Analytics | 3 | Pulse, Experiment, Matrix |
| Operations | 1 | Triage |
| Browser Automation | 2 | Vector, Director |
| **Total** | **78** | |
