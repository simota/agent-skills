# Official Pattern Taxonomy Reference

> Source: "The Complete Guide to Building Skills for Claude" (Anthropic, 2025)

Lore が CATALOG / PROPAGATE フェーズで参照する公式パターン統合リファレンス。

---

## 1. 公式パターンとLoreパターン分類の統合マッピング

### 公式5パターン → Lore Taxonomy 変換

| Official Pattern | Lore Domain | Lore Type | Default Confidence | Scope |
|-----------------|-------------|-----------|-------------------|-------|
| Sequential Workflow Orchestration | `PROCESS` | `SUCCESS` | `ESTABLISHED` | `ECOSYSTEM` |
| Multi-MCP Coordination | `INFRA` | `SUCCESS` | `ESTABLISHED` | `ECOSYSTEM` |
| Iterative Refinement | `PROCESS` | `HEURISTIC` | `ESTABLISHED` | `ECOSYSTEM` |
| Context-Aware Tool Selection | `APP` | `HEURISTIC` | `ESTABLISHED` | `ECOSYSTEM` |
| Domain-Specific Intelligence | `DESIGN` | `SUCCESS` | `ESTABLISHED` | `ECOSYSTEM` |

> 公式パターンは Anthropic による観察に基づく `ESTABLISHED` レベル。エコシステム内での実証が蓄積すれば `FOUNDATIONAL` に昇格可能。

### 公式3ユースケースカテゴリ → Lore Domain 変換

| Official Category | Primary Lore Domain | Secondary Domain |
|------------------|--------------------|-----------------|
| Document & Asset Creation | `APP` | `DESIGN` |
| Workflow Automation | `PROCESS` | `INFRA` |
| MCP Enhancement | `INFRA` | `APP` |

---

## 2. 公式品質シグナルとLore証拠分類の統合

### 定量シグナル

| Official Metric | Lore Evidence Type | Threshold | Mapping |
|----------------|-------------------|-----------|---------|
| Trigger rate 90%+ | Execution evidence | ≥ 90% auto-load | `SUCCESS` pattern if met; `FAILURE` if consistently below |
| 0 failed API calls | Execution evidence | 0 failures per workflow | `SUCCESS` if met; `ANTI` if consistently failing |
| Workflow efficiency (token reduction) | Performance evidence | Baseline comparison | `TRADEOFF` pattern with quantitative data |

### 定性シグナル

| Official Metric | Lore Evidence Type | Assessment |
|----------------|-------------------|-----------|
| No next-step prompting needed | User behavior evidence | `SUCCESS` when observed; `FAILURE` as anti-pattern |
| Correction-free execution | Consistency evidence | 3-5 identical runs → `PATTERN` confidence |
| First-try accessibility | Usability evidence | New user feedback → `EMERGING` then `PATTERN` |

---

## 3. 公式反復シグナルとLore腐敗検出の統合

### Undertriggering → Knowledge Gap Detection

| Official Signal | Lore Mapping | Action |
|----------------|-------------|--------|
| Skill doesn't load when expected | `FAILURE` pattern candidate | Register as `META-FAILURE-NNN` |
| Users manually enabling skills | Usability gap evidence | Propagate to Sigil (description improvement) |
| Support questions about usage | Knowledge gap signal | Propagate to Architect (trigger guidance review) |

### Overtriggering → Anti-Pattern Detection

| Official Signal | Lore Mapping | Action |
|----------------|-------------|--------|
| Skill loads for irrelevant queries | `ANTI` pattern candidate | Register as `META-ANTI-NNN` |
| Users disabling skills | Negative evidence | Propagate to Sigil (negative trigger addition) |
| Confusion about purpose | Design gap signal | Propagate to Architect (scope clarification) |

### Execution Issues → Failure Pattern Detection

| Official Signal | Lore Mapping | Action |
|----------------|-------------|--------|
| Inconsistent results | `FAILURE` pattern candidate | Cross-reference with other agent journals |
| API call failures | `INFRA-FAILURE-NNN` | Propagate to Mend (remediation pattern) |
| User corrections needed | Instruction quality gap | Propagate to Sigil (instruction improvement) |

---

## 4. CATALOG フェーズでの公式パターン照合ルール

### 新規パターン登録時の公式照合

1. **分類前チェック**: 新規パターン候補が公式5パターンのいずれかに該当するか確認
2. **該当する場合**: 公式パターンの variant として登録（ID に `-V` suffix）
3. **該当しない場合**: 通常の新規パターンとして登録
4. **矛盾する場合**: 公式パターンとの差異を明示的に記録し、evidence count ≥ 3 で独立パターンとして昇格

### 公式基準によるパターン品質評価

登録済みパターンが以下の公式基準を満たしているか定期的に評価:

| Criterion | Check | Source |
|-----------|-------|--------|
| Progressive Disclosure 準拠 | パターンが3段階構造を反映しているか | Official Guide §1 |
| Description 品質 | WHAT+WHEN 構造を含むか | Official Guide §2 |
| テスト可能性 | 3 Areas (Triggering/Functional/Performance) で検証可能か | Official Guide §3 |
| エラーハンドリング | トラブルシューティング6カテゴリに対応するか | Official Guide §5 |

---

## 5. PROPAGATE フェーズでの公式基準配信ルール

### 配信対象と公式基準の関連性

| Consumer Agent | Relevant Official Knowledge | Propagation Trigger |
|---------------|---------------------------|-------------------|
| **Sigil** | Description記述ルール、Instruction構造、テスト方法論 | Skill生成品質の低下パターン検出時 |
| **Architect** | 5パターン、成功基準フレームワーク、Progressive Disclosure | 新エージェント設計品質の低下パターン検出時 |
| **Gauge** | Frontmatter検証仕様、トラブルシューティング6カテゴリ | 監査精度の低下パターン検出時 |
| **Darwin** | 品質シグナル（定量/定性）、反復シグナル | EFS評価精度の改善機会検出時 |
| **Nexus** | 3ユースケースカテゴリ、パターン選択ガイド | ルーティング精度の低下パターン検出時 |

### LORE_INSIGHT での公式基準参照フォーマット

```
LORE_INSIGHT:
  Pattern: [ID]
  Official_Alignment: [ALIGNED | VARIANT | NOVEL | CONTRADICTS]
  Official_Reference: "The Complete Guide to Building Skills for Claude" §[section]
  Evidence: [agent, date, context]
  Implication: [what this means for the consumer]
```
