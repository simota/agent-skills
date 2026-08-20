# Contributing / コントリビューションガイド

AI Agent Skills へのコントリビューションを歓迎します！

## 🐛 バグ報告

1. [Issues](../../issues) で既存の報告がないか確認
2. 新規 Issue を作成し、以下を記載:
   - 再現手順
   - 期待される動作
   - 実際の動作
   - 使用プラットフォーム（Claude Code, Codex CLI 等）

## 💡 機能要望

1. [Issues](../../issues) で新規 Issue を作成
2. ユースケースと期待される効果を記載

## 🔧 プルリクエスト

### セットアップ

```bash
# フォーク後
git clone https://github.com/YOUR_USERNAME/agent-skills.git
cd agent-skills
```

### 新しいエージェントの追加

1. `[AgentName]/SKILL.md` を作成
2. `description` は英語で1行（グローバルとproject-localの全スキルで統一）。frontmatter とセクション構成は `_templates/SKILL_TEMPLATE.md` を正とする — 以下は骨格の抜粋:

```markdown
---
name: AgentName
description: "One-line description. What this agent does and when to use it. Don't use for X (Agent), Y (Agent)."
---

# AgentName

> **"Motto — one line that captures the agent's philosophy."**

Identity statement (1-2 lines). What you do, what you deliver, scope per invocation.

## Trigger Guidance

Use AgentName when the task needs:
- [specific task or signal]

Route elsewhere when the task is primarily:
- [adjacent concern]: `AlternativeAgent`

## Core Contract

- [Non-negotiable commitments this agent makes]

## Boundaries

### Always
- [Required behaviors]

### Ask First
- [Actions requiring confirmation]

### Never
- [Prohibited actions]

## Workflow
[Phases and what each produces]

## Recipes / ## Subcommand Dispatch
[Only if the agent defines Recipes — see `_common/RECIPES.md`]

## Output Requirements
[What every deliverable must carry]

## Collaboration
[Inbound / outbound handoffs]

## Reference Map
[Which `reference/*.md` to read at which decision point]

## Operational
[Journal, logging, git conventions]

## AUTORUN Support
[Nexus integration format]

## Nexus Hub Mode
[Hub mode handoff format]
```

上の見出しは `_common/scripts/lint-frontmatter.py` の `ST1`（必須見出し）が実際に検査する集合。省略すると lint が指摘する。

`## INTERACTION_TRIGGERS`（ユーザー確認が必要な決定ポイントの定義）は、それが必要なエージェントでは今も使用される（現状12スキル）。省略可能なセクションであり、必須ではない。

3. 完全なセクション一覧・順序・記法は `_templates/SKILL_TEMPLATE.md` を参照し、それに沿って作成する
4. **ロスターを更新する（手作業のレジストリは自動同期されない）**:
   - `README.md` / `README_ja.md` のエージェント一覧とエージェント数
   - `index.html`（`const AGENTS` 配列・カテゴリ件数・件数を記載した全テキスト）
   - `compass/reference/catalog.md`（カテゴリ節とその件数）
   - `_common/SKILL_PACKS.md`（最低1つのPack、またはoptional／explicit-only／project-local配置に登録する）
   - `AGENTS.md` / `CLAUDE.md` のスキル数
5. 使用例セクションにサンプルを追加
6. lint を通す: `python3 _common/scripts/lint-frontmatter.py --severity error --changed-only` と `python3 _common/scripts/lint-instructions.py --severity error`
7. 契約の配送を確認する: `python3 _common/scripts/lint-contracts.py --severity error`。新規スキルは `_common/*.md` を名指ししても、ディレクトリに `_common` symlink が無ければ実行時に解決しない（CD-4）。`--report` で spine 契約の到達深度を確認できる

### コーディング規約

| 項目 | 規約 |
|------|------|
| エージェント名 | PascalCase（例: Scout, Builder, Artisan） |
| ファイル名 | `[AgentName]/SKILL.md` |
| 出力言語 | 日本語 |
| コード・コミット | 英語 |
| コミット形式 | Conventional Commits |

### コミットメッセージ

```
type(scope): description

Examples:
- feat(agents): add new DataFlow agent
- fix(Builder): resolve type inference issue
- docs(README): update usage examples
```

**type**:
- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメント
- `refactor`: リファクタリング
- `chore`: その他

### PR チェックリスト

- [ ] SKILL.md が規定フォーマットに従っている
- [ ] Boundaries（Always/Ask/Never）が明確
- [ ] AUTORUN Support セクションがある
- [ ] README.md / README_ja.md を更新した
- [ ] ロスター系レジストリ（`index.html`, `compass/reference/catalog.md`, `_common/SKILL_PACKS.md`, `AGENTS.md`, `CLAUDE.md`）を更新した
- [ ] `lint-frontmatter.py` と `lint-instructions.py` が通る
- [ ] `lint-contracts.py` が通る（`_common` symlink が張られ、名指しした契約が実行時に解決する）
- [ ] 使用例を追加した

## 📝 ドキュメント改善

ドキュメントの改善も歓迎します:
- 誤字脱字の修正
- 説明の明確化
- 使用例の追加
- 翻訳の改善

## 🤝 コードオブコンダクト

- 建設的なフィードバックを心がける
- 多様な意見を尊重する
- 初心者に優しく対応する

## 📜 ライセンス

コントリビューションは [MIT License](LICENSE) の下で提供されます。
