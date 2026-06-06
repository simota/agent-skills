# Official Skill Categories Reference

> Source: "The Complete Guide to Building Skills for Claude" (Anthropic, 2025)

Nexus が CLASSIFY フェーズでタスク分類精度を向上させるための公式カテゴリリファレンス。

---

## 1. 公式3ユースケースカテゴリ

### Category 1: Document & Asset Creation

**定義**: 一貫性のある高品質な出力（文書、プレゼン、アプリ、デザイン、コード等）の生成

**タスク識別シグナル**:
- `"create"`, `"generate"`, `"design"`, `"build"` + 成果物名
- ファイル生成やテンプレート適用の要求
- スタイルガイドやブランド基準への準拠要求

**推奨チェーンパターン**:
- Scribe / Quill / Morph / Dot / Sketch / Clay → 成果物に応じた生成エージェント
- 品質チェック: Warden / Judge

**Key Techniques** (公式):
- Embedded style guides and brand standards
- Template structures for consistent output
- Quality checklists before finalizing

### Category 2: Workflow Automation

**定義**: 一貫した方法論で実行される多段階プロセスの自動化（複数MCP連携含む）

**タスク識別シグナル**:
- `"automate"`, `"workflow"`, `"pipeline"`, `"process"` の言及
- 複数のツール/サービス間の連携要求
- 繰り返し実行されるタスクの効率化

**推奨チェーンパターン**:
- Sherpa（分解） → 各専門エージェント → Radar（検証）
- 大規模: Titan → Nexus チェーン発行

**Key Techniques** (公式):
- Step-by-step workflow with validation gates
- Templates for common structures
- Built-in review and improvement suggestions
- Iterative refinement loops

### Category 3: MCP Enhancement

**定義**: MCPサーバーが提供するツールアクセスに、ワークフロー知識を付加

**タスク識別シグナル**:
- MCP ツール名やサービス名の直接言及
- `"integrate"`, `"connect"`, `"sync"` + 外部サービス
- API連携の最適化要求

**推奨チェーンパターン**:
- Frame / Relay / Navigator → サービス固有のフロー
- Hone（設定最適化）

**Key Techniques** (公式):
- Coordinates multiple MCP calls in sequence
- Embeds domain expertise
- Provides context users would otherwise need to specify
- Error handling for common MCP issues

---

## 2. 公式5パターンとルーティング判断

### Pattern → Chain 最適化マッピング

| Official Pattern | When to Apply | Chain Design Guidance |
|-----------------|---------------|----------------------|
| **Sequential Workflow** | Ordered multi-step, dependencies between steps | Sequential chain, no parallel branches |
| **Multi-MCP Coordination** | Cross-service workflow | Phase-separated chain with data passing, validation gates between phases |
| **Iterative Refinement** | Quality-sensitive output | Loop-capable chain with quality check agent (Judge/Warden) |
| **Context-Aware Tool Selection** | Same outcome, different tools per context | Decision point at CLASSIFY, context-dependent chain selection |
| **Domain-Specific Intelligence** | Regulatory/compliance/domain expertise required | Canon/domain expert injection before execution |

### Pattern Detection Rules for CLASSIFY

```
IF task involves ordered steps with dependencies:
  → Sequential Workflow pattern
  → Use simple sequential chain

IF task spans 2+ external services:
  → Multi-MCP Coordination pattern
  → Design phase-separated chain with inter-phase validation

IF task output requires quality iteration:
  → Iterative Refinement pattern
  → Include quality-check loop (max 3 iterations)

IF same goal achievable with different tools:
  → Context-Aware Tool Selection pattern
  → Add decision logic before chain selection

IF task requires domain expertise (compliance, finance, security):
  → Domain-Specific Intelligence pattern
  → Inject domain expert (Canon, Sentinel, etc.) before execution
```

---

## 3. CLASSIFY フェーズでの公式カテゴリ活用

### 拡張 CLASSIFY プロセス

既存の CLASSIFY（task type, complexity, confidence）に**公式カテゴリ分類**を追加:

1. **Task Type 検出**（既存）: BUG / FEATURE / SECURITY / REFACTOR / OPTIMIZE / REVIEW
2. **Official Category 検出**（新規）: Document & Asset / Workflow Automation / MCP Enhancement
3. **Official Pattern 検出**（新規）: Sequential / Multi-MCP / Iterative / Context-Aware / Domain-Specific
4. **Chain Selection 最適化**: 公式パターンに基づくチェーン調整

### カテゴリ × Task Type マトリクス

| | BUG | FEATURE | SECURITY | REFACTOR | OPTIMIZE | REVIEW |
|--|-----|---------|----------|----------|----------|--------|
| **Document & Asset** | — | Forge→専門→Judge | — | Zen→Judge | — | Judge |
| **Workflow Automation** | Scout→Builder→Radar | Sherpa→Builder→Radar | Sentinel→Builder | Zen→Radar | Bolt→Radar | Judge→Canon |
| **MCP Enhancement** | Scout→Builder→Radar | Frame/Relay→Builder→Radar | Sentinel→Probe | — | Bolt→Tuner | Judge |

---

## 4. 公式成功基準によるVERIFY強化

### VERIFY フェーズでの公式メトリクス参照

チェーン実行後の VERIFY で、公式成功基準を補助的に評価:

| Metric | Check | Pass Criteria |
|--------|-------|--------------|
| Skill trigger accuracy | Description に対する auto-load 率 | 概念的確認（定量測定は別途） |
| Workflow efficiency | チェーンのステップ数と冗長性 | 最小限のエージェント数で完了 |
| Error handling | エラー発生時のリカバリ | L1-L4 ガードレールが機能 |
| Output consistency | 同一タスクの結果一貫性 | 構造的一貫性の確認 |

---

## 5. Problem-first vs Tool-first アプローチ判定

CLASSIFY フェーズで、ユーザーのアプローチを判定しチェーン設計に反映:

| Approach | Detection Signal | Chain Impact |
|----------|-----------------|-------------|
| **Problem-first** | 成果物や目標を記述（"I need to set up..."） | Nexus がツール選択を自動化 |
| **Tool-first** | ツール名やサービス名を直接指定（"I have X MCP..."） | ユーザー指定のツールを尊重しつつ最適化 |

> Problem-first ではチェーン設計の自由度が高い。Tool-first ではユーザーの明示的選択を尊重する。
