# Skill Review Criteria Reference

> Source: "The Complete Guide to Building Skills for Claude" (Anthropic, 2025)

Judge が SKILL.md ファイルのレビュー時に参照する公式基準リファレンス。

---

## 1. SKILL.md レビュー対象判定

### レビュー対象条件

以下のいずれかに該当する場合、SKILL.md レビューモードを適用:

- レビュー対象に `SKILL.md` ファイルが含まれる
- レビュー対象に `reference/*.md` ファイル（スキル内）が含まれる
- YAML frontmatter を持つ `.md` ファイルの変更
- `skills/` ディレクトリ配下の変更

### 通常コードレビューとの使い分け

| Aspect | Code Review | SKILL.md Review |
|--------|------------|----------------|
| Primary Tool | `codex review` CLI | 公式基準チェックリスト |
| Focus | Correctness, security, logic | Structure, description quality, progressive disclosure |
| Severity Scale | CRITICAL-INFO (5段階) | CRITICAL-LOW (4段階、公式基準ベース) |
| Routing | Builder / Sentinel / Zen | Sigil / Architect / Gauge |

---

## 2. SKILL.md レビューチェックリスト

### Critical (ブロッキング)

| ID | Check | Rule |
|----|-------|------|
| SK-C01 | `SKILL.md` ファイル名が正確（case-sensitive） | `SKILL.md` のみ許可 |
| SK-C02 | YAML frontmatter `---` デリミタが正しい | 開始・終了の両方が必要 |
| SK-C03 | `name` フィールドが存在する | Required field |
| SK-C04 | `description` フィールドが存在する | Required field |
| SK-C05 | Frontmatter に XML タグ（`<` `>`）がない | Security restriction |
| SK-C06 | `name` に `"claude"` / `"anthropic"` を含まない | Reserved prefix |

### High (要修正)

| ID | Check | Rule |
|----|-------|------|
| SK-H01 | `name` が kebab-case | Regex: `^[a-z0-9]+(-[a-z0-9]+)*$` |
| SK-H02 | `name` がフォルダ名と一致 | String match |
| SK-H03 | `description` が 1024 文字以下 | Official limit |
| SK-H04 | `description` が WHAT を含む | "何をするか" の記述 |
| SK-H05 | `description` が WHEN を含む | "いつ使うか" のトリガー条件 |
| SK-H06 | `description` が vague でない | "Helps with projects" レベルを排除 |
| SK-H07 | Step-by-step 構造が存在する | Heading or numbered list |

### Medium (推奨改善)

| ID | Check | Rule |
|----|-------|------|
| SK-M01 | Examples セクションが存在する | ユーザーシナリオの具体例 |
| SK-M02 | Troubleshooting セクションが存在する | エラー対応の記述 |
| SK-M03 | `reference/` ディレクトリを活用している | Progressive Disclosure |
| SK-M04 | SKILL.md が 5000 words 以下 | Context efficiency |
| SK-M05 | Critical instructions が文書先頭付近 | 重要度の高い指示が上部に |

### Low (任意改善)

| ID | Check | Rule |
|----|-------|------|
| SK-L01 | `compatibility` フィールドが 500 文字以下 | Official limit |
| SK-L02 | Negative trigger がある（必要な場合） | Overtriggering prevention |
| SK-L03 | `metadata` に `author` / `version` がある | Best practice |
| SK-L04 | スキルフォルダに `README.md` がない | Official rule |

---

## 3. Description 品質評価

### Good Description パターン

```yaml
# Pattern: Specific + Actionable + Trigger phrases
description: Analyzes Figma design files and generates developer handoff
documentation. Use when user uploads .fig files, asks for "design specs",
"component documentation", or "design-to-code handoff".
```

**チェックポイント**:
- ✅ 動詞で始まる（何をするか明確）
- ✅ トリガーフレーズを含む（いつ使うか明確）
- ✅ ファイルタイプを言及（対象が明確）

### Bad Description アンチパターン

| Anti-pattern | Example | Issue |
|-------------|---------|-------|
| Too vague | "Helps with projects" | トリガーしない |
| Missing triggers | "Creates documentation systems" | WHEN がない |
| Too technical | "Implements entity model with hierarchical relationships" | ユーザー視点でない |
| Too long (>1024) | — | Frontmatter が肥大化 |

### Verdict Logic

```
IF any SK-C* fails → BLOCK (CRITICAL findings)
IF SK-H04 OR SK-H05 fails → REQUEST CHANGES
IF 3+ SK-M* fail → REQUEST CHANGES (accumulation)
ELSE → APPROVE (with notes if SK-L* issues exist)
```

---

## 4. Progressive Disclosure レビュー

### 3段階構造の検証

| Level | What to Check | Finding if Missing |
|-------|--------------|-------------------|
| 1st (Frontmatter) | `name` + `description` が最小限で十分か | SK-H04, SK-H05 |
| 2nd (Body) | SKILL.md がコア指示に集中しているか | SK-M04 if word count > 5000 |
| 3rd (References) | 詳細が `reference/` に分離されているか | SK-M03 |

### Context Efficiency 評価

```
IF SKILL.md > 5000 words AND reference/ is empty:
  → Finding: SK-M03 + SK-M04
  → Recommendation: "Move detailed documentation to reference/"

IF SKILL.md < 500 words AND reference/ has 5+ files:
  → Note: Good progressive disclosure structure

IF all content is inline AND no reference/ directory:
  → Finding: SK-M03
  → Recommendation: "Consider progressive disclosure structure"
```

---

## 5. レビューレポートフォーマット

### SKILL.md Review Finding

```
ID: [SK-C/H/M/L + NN]
Severity: [CRITICAL | HIGH | MEDIUM | LOW]
Location: [SKILL.md:line or structural]
Standard: Anthropic Agent Skill Specification (2025)
Finding: [specific observation]
Recommendation: [actionable fix]
Remediation: [Sigil | Architect | Gauge]
```

### Summary に追加するセクション

```markdown
## Skill Quality Assessment
- Frontmatter: [PASS | FAIL] ([count] issues)
- Description Quality: [PASS | FAIL] ([count] issues)
- Instruction Structure: [PASS | FAIL] ([count] issues)
- Progressive Disclosure: [PASS | FAIL] ([count] issues)
- Overall: [COMPLIANT | PARTIAL | NON-COMPLIANT]
```

---

## 6. ルーティング

| Finding Type | Route To |
|-------------|---------|
| Frontmatter 構造問題 | Sigil（再生成） or Architect（再設計） |
| Description 品質問題 | Sigil（description 改善） |
| Instruction 構造問題 | Sigil（再構造化） |
| Progressive Disclosure 問題 | Architect（reference 分離設計） |
| エコシステム内部基準違反 | Gauge（16項目チェックリスト） |
