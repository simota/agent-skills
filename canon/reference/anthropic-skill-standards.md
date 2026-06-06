# Anthropic Skill Standards Reference

> Source: "The Complete Guide to Building Skills for Claude" (Anthropic, 2025)

Canon が ASSESS フェーズで SKILL.md の公式仕様準拠を評価するためのリファレンス。

---

## 1. 標準概要

| Field | Value |
|-------|-------|
| Standard Name | Anthropic Agent Skill Specification |
| Publisher | Anthropic |
| Version | 2025 (The Complete Guide to Building Skills for Claude) |
| Scope | Claude Code / Claude.ai / API でのスキル設計・構造・配布 |
| Category | AI Agent Quality |
| Canon Category Code | `SKILL` |

---

## 2. 要件マトリクス

### 2.1 Structural Requirements (STR)

| ID | Requirement | Level | Evidence |
|----|------------|-------|---------|
| STR-01 | `SKILL.md` ファイルが存在する（case-sensitive） | CRITICAL | File existence check |
| STR-02 | YAML frontmatter が `---` デリミタで囲まれている | CRITICAL | YAML parse validation |
| STR-03 | `name` フィールドが kebab-case | HIGH | Regex: `^[a-z0-9]+(-[a-z0-9]+)*$` |
| STR-04 | `name` がフォルダ名と一致 | HIGH | String comparison |
| STR-05 | `name` に `"claude"` / `"anthropic"` を含まない | CRITICAL | String search |
| STR-06 | `description` フィールドが存在する | CRITICAL | Field presence check |
| STR-07 | `description` が 1024 文字以下 | HIGH | Character count |
| STR-08 | `description` に XML タグ（`<` `>`）を含まない | CRITICAL | Character search |
| STR-09 | スキルフォルダに `README.md` を含まない | MEDIUM | File absence check |
| STR-10 | `compatibility` フィールドが 500 文字以下（使用時） | LOW | Character count |

### 2.2 Description Quality Requirements (DSC)

| ID | Requirement | Level | Evidence |
|----|------------|-------|---------|
| DSC-01 | WHAT（何をするか）が記述されている | HIGH | Semantic analysis |
| DSC-02 | WHEN（いつ使うか / トリガー条件）が記述されている | HIGH | Trigger phrase presence |
| DSC-03 | 具体的なタスク・フレーズが含まれている | MEDIUM | Actionable keyword detection |
| DSC-04 | ファイルタイプが関連する場合は言及されている | LOW | Context-dependent |
| DSC-05 | Vague でない（"Helps with projects" レベルの generic を排除） | HIGH | Anti-pattern matching |

### 2.3 Instruction Quality Requirements (INS)

| ID | Requirement | Level | Evidence |
|----|------------|-------|---------|
| INS-01 | Step-by-step 構造が存在する | HIGH | Heading/list structure |
| INS-02 | 具体的でアクション可能な指示 | HIGH | Imperative verb presence |
| INS-03 | Examples セクションが存在する | MEDIUM | Section heading detection |
| INS-04 | Troubleshooting / Error handling が記述されている | MEDIUM | Section heading detection |
| INS-05 | `reference/` からのリンクが適切 | MEDIUM | Link validity check |
| INS-06 | Critical instructions が文書先頭付近に配置されている | LOW | Position analysis |

### 2.4 Progressive Disclosure Requirements (PD)

| ID | Requirement | Level | Evidence |
|----|------------|-------|---------|
| PD-01 | 1st level: frontmatter が最小限で判断に十分 | HIGH | Frontmatter content analysis |
| PD-02 | 2nd level: SKILL.md body がコア指示に集中 | MEDIUM | Word count ≤ 5000 recommended |
| PD-03 | 3rd level: 詳細が `reference/` に分離されている | MEDIUM | Directory structure check |
| PD-04 | SKILL.md からの参照リンクが明示的 | LOW | Reference link presence |

### 2.5 Composability Requirements (CMP)

| ID | Requirement | Level | Evidence |
|----|------------|-------|---------|
| CMP-01 | 他スキルとの共存を想定した設計 | LOW | Exclusive capability claims absence |
| CMP-02 | 環境依存が `compatibility` フィールドに記載 | LOW | Field content check |

---

## 3. トラブルシューティング準拠チェック

ASSESS フェーズで以下の6カテゴリに対するスキルの対応度を評価:

| Category | Check | Compliant Criteria |
|----------|-------|-------------------|
| Upload Failure | SKILL.md命名、YAML形式、name形式 | STR-01〜STR-05 すべて PASS |
| Undertriggering | Description品質 | DSC-01〜DSC-05 すべて PASS |
| Overtriggering | スコープ明確性、negative trigger | DSC-02 + スコープ限定記述の存在 |
| Instructions Not Followed | Instruction構造品質 | INS-01〜INS-06 の主要項目 PASS |
| MCP Connection Issues | MCP依存の明示とエラーハンドリング | INS-04 + MCP関連のトラブルシューティング |
| Large Context Issues | Progressive Disclosure 実装 | PD-01〜PD-04 すべて PASS |

---

## 4. 準拠レベル判定

### 総合判定基準

| Level | Criteria | Action |
|-------|---------|--------|
| **Compliant** | CRITICAL 全 PASS + HIGH 80%+ PASS | Document and maintain |
| **Partial** | CRITICAL 全 PASS + HIGH 50-79% PASS | Enhancement recommended |
| **Non-compliant** | CRITICAL に 1+ FAIL | Remediation required |

### Severity Timeline

| Severity | Timeline | Examples |
|----------|----------|---------|
| CRITICAL | Immediate | Missing SKILL.md, broken YAML, XML in frontmatter |
| HIGH | 1 sprint | Vague description, no trigger phrases, no steps |
| MEDIUM | 1 month | No examples, no troubleshooting, inline-heavy |
| LOW | Backlog | Missing compatibility field, no negative triggers |

---

## 5. Gauge との役割境界

| Aspect | Canon | Gauge |
|--------|-------|-------|
| **対象基準** | Anthropic公式スキル仕様 + 業界標準 | エコシステム内部16項目正規化チェックリスト |
| **評価視点** | 外部標準への準拠度 | 内部テンプレートへの適合度 |
| **出力** | 準拠レポート with citations | PASS/PARTIAL/FAIL with fix snippets |
| **連携** | Canon が公式基準違反を検出 → Gauge が内部チェックリストで詳細検証 | Gauge が構造問題を検出 → Canon が公式基準との照合 |

---

## 6. 証拠フォーマット

```
Standard: Anthropic Agent Skill Specification (2025)
Requirement: [ID] [requirement description]
Evidence: [file:line or structural observation]
Status: [Compliant | Partial | Non-compliant]
Finding: [specific observation]
Recommendation: [actionable fix]
Priority: [CRITICAL | HIGH | MEDIUM | LOW]
Remediation Agent: [Sigil | Architect | Gauge]
```
