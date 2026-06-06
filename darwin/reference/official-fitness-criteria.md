# Official Fitness Criteria Reference

> Sources:
> - "The Complete Guide to Building Skills for Claude" (Anthropic, 2025) — Progressive Disclosure / frontmatter / instruction structure baseline.
> - "New in Claude Managed Agents: dreaming, outcomes, and multiagent orchestration" (Anthropic, 2026-05-06) — adds **Outcomes** rubrics as the new official success-criteria primitive. URL: `https://claude.com/blog/new-in-claude-managed-agents`.

Darwin が ASSESS / EVOLVE フェーズで参照する公式基準ベースのフィットネス評価リファレンス。

> **2026-05 update**: Anthropic's Managed Agents now ship a first-class `Outcomes` mechanism in public beta — agent operators write a **rubric** describing what success looks like and the agent works toward it. Internal Anthropic testing measured **up to +10 percentage points** task-success lift over a plain prompting loop (+8.4 pp on docx generation, +10.1 pp on pptx generation). Darwin treats the presence of an explicit Outcomes rubric (or local equivalent) as a positive OSC signal for the *Instruction Structure* and *Error Handling* criteria below. Conversely, an agent stuck on a plain prompting loop with no rubric — when running under Claude Managed Agents — is now an OSC penalty (≥ −10 toward the *Instruction Structure* dimension), because the +10 pp ceiling lift is freely available.

---

## 1. EFS 公式仕様適合度次元

既存の EFS 5次元評価に**公式仕様適合度（Official Spec Conformance: OSC）**を補助指標として統合する。

### OSC スコアリング（0-100）

| Criterion | Weight | Scoring | Source |
|-----------|--------|---------|--------|
| **Progressive Disclosure 準拠** | 0.25 | 3段階構造（frontmatter / body / references）の実装度 | Official Guide §1 |
| **Frontmatter 品質** | 0.20 | name (kebab-case) + description (WHAT+WHEN, ≤1024 chars, no XML) | Official Guide §2 |
| **Instruction 構造** | 0.20 | Steps → Examples → Troubleshooting の構造化度 | Official Guide §2 |
| **テスト方法論実装** | 0.15 | Triggering / Functional / Performance の3領域カバレッジ | Official Guide §3 |
| **Composability** | 0.10 | 他スキルとの共存可能性、ポータビリティ | Official Guide §1 |
| **エラーハンドリング** | 0.10 | トラブルシューティング対応（6カテゴリ中の対応数） | Official Guide §5 |

### OSC グレード

| Grade | Score | Interpretation |
|-------|-------|---------------|
| S | 95-100 | 公式仕様を完全に満たし、模範的 |
| A | 85-94 | 公式仕様にほぼ準拠 |
| B | 70-84 | 主要項目は準拠、改善余地あり |
| C | 55-69 | 基本的な準拠にとどまる |
| D | 40-54 | 公式仕様との乖離が大きい |
| F | 0-39 | 公式仕様にほぼ非準拠 |

### EFS との統合方法

OSC は EFS の6番目の次元ではなく、既存5次元の**品質修正係数**として機能する:

```
Adjusted_EFS = EFS × (0.8 + 0.2 × (OSC / 100))
```

- OSC = 100 → EFS × 1.0（変化なし）
- OSC = 50 → EFS × 0.9（10%減）
- OSC = 0 → EFS × 0.8（20%減）

> 既存の EFS 計算を破壊しない保守的な統合。OSC が高いほどEFSを維持、低いほど軽度のペナルティ。

---

## 2. 公式品質シグナルによるRS評価強化

### Agent Relevance Score (RS) への公式指標組み込み

既存のRS計算に以下の公式品質シグナルを補助入力として追加:

| Signal | RS Impact | Detection Method |
|--------|----------|-----------------|
| Description が WHAT+WHEN を満たす | RS +5 | YAML frontmatter のパース |
| Progressive Disclosure が実装済み | RS +5 | `reference/` ディレクトリの存在と参照 |
| テスト方法が定義済み | RS +3 | Triggering/Functional test の記述 |
| エラーハンドリングが記述済み | RS +2 | Troubleshooting セクションの存在 |
| Description が vague | RS -5 | Trigger phrase 不在、generic description |
| `reference/` が未使用 | RS -3 | SKILL.md に全情報がインライン |

---

## 3. 進化トリガーへの公式基準統合

### 新規トリガー: ET-09 — 公式仕様乖離

| Field | Value |
|-------|-------|
| Trigger ID | `ET-09` |
| Condition | OSC ≤ C (55未満) for any agent |
| Scope | Medium |
| Action | Propose SKILL.md improvement via Architect |
| Priority | After ET-01 through ET-08 |

### 既存トリガーとの公式基準連携

| Existing Trigger | Official Enhancement |
|-----------------|---------------------|
| `ET-02`: Health Score drop ≥10 | OSC も同時評価し、公式仕様乖離が原因か判定 |
| `ET-03`: 3+ unprocessed feedback | 公式基準違反フィードバックを優先処理 |
| `ET-05`: Same decision repeated 3+ | 公式パターンとの照合で最適パターン推薦 |
| `ET-08`: Average Health Score < B | OSC グレードも併記して根本原因分析 |

---

## 4. ライフサイクルフェーズ別の公式基準適用

### フェーズ別 OSC 期待値

| Lifecycle Phase | Minimum OSC | Rationale |
|----------------|-------------|-----------|
| `GENESIS` | D (40+) | 初期段階では基本構造の確立を優先 |
| `ACTIVE_BUILD` | C (55+) | 主要機能開発中、Progressive Disclosure を実装 |
| `STABILIZATION` | B (70+) | 安定化フェーズでは公式仕様に概ね準拠 |
| `PRODUCTION` | A (85+) | 本番運用には高い公式仕様準拠を要求 |
| `MAINTENANCE` | A (85+) | 維持フェーズでも品質を保持 |
| `SCALING` | A (85+) | スケーリング時こそ品質基盤が重要 |
| `SUNSET` | — | 評価対象外 |

### ASSESS フェーズでの適用

1. ライフサイクルフェーズを検出（既存ロジック）
2. フェーズ別の Minimum OSC を参照
3. 各エージェントの現在 OSC を算出
4. `Current OSC < Minimum OSC` のエージェントを改善候補リストに追加
5. DARWIN_REPORT に OSC セクションを含める

---

## 5. 公式3ユースケースカテゴリによるエコシステムカバレッジ分析

### カテゴリ別エージェントマッピング

| Official Category | Ecosystem Agents | Coverage |
|------------------|-----------------|----------|
| **Document & Asset Creation** | Scribe, Quill, Morph, Dot, Sketch, Clay | 文書・アセット生成 |
| **Workflow Automation** | Nexus, Titan, Sherpa, Sigil, Pipe, Launch | ワークフロー自動化 |
| **MCP Enhancement** | Frame, Relay, Vector, Hone | MCP統合強化 |

### カバレッジギャップ検出

ASSESS フェーズで以下を評価:
- 各カテゴリに十分なエージェントが存在するか
- カテゴリ間のバランスは適切か
- 新規エージェント提案時に未カバーカテゴリを優先するか

---

## 6. DARWIN_REPORT への公式基準セクション追加

### 出力フォーマット拡張

```markdown
## Official Spec Conformance (OSC)

| Agent | OSC Score | Grade | Min Required | Status |
|-------|-----------|-------|-------------|--------|
| [name] | [0-100] | [S-F] | [phase-based] | [PASS/BELOW] |

### OSC Summary
- Ecosystem Average: [score]
- Agents Below Minimum: [count]
- Top Improvement Candidates: [list]

### Use Case Coverage
- Document & Asset Creation: [agent count] agents
- Workflow Automation: [agent count] agents
- MCP Enhancement: [agent count] agents
```
