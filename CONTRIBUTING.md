# Contributing / コントリビューションガイド

AI Agent Skills へのコントリビューションを歓迎します！

リポジトリ構造・正本・検証の全体像は [`docs/REPOSITORY_GUIDE.md`](docs/REPOSITORY_GUIDE.md) も参照してください。

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
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-checks.txt
make check
```

検証には Python 3 と Node.js が必要です（CI は Python 3.12 / Node.js 22）。

検証コマンドは `Makefile` を正とします:

| コマンド | 用途 |
|---|---|
| `make validate` | スキル構造、project-local 配線、Recipes、routing、instructions、contract delivery、lessons、task battery を検証 |
| `make test` | 検証スクリプトと周辺ツールの回帰テストを実行 |
| `make check` | `make validate` + `make test`。PR 前の標準コマンド |
| `make hooks` | リポジトリ管理の pre-commit hook を有効化 |

個別 lint コマンドの羅列をドキュメント側で正本化せず、通常は `make check` を実行してください。検証スクリプトが増減した場合は `Makefile`・CI・hook/installer fixture を同時に更新します。

### 新しいグローバルエージェントの追加

1. 小文字のディレクトリ名で `<skill-name>/SKILL.md` を作成（例: `scout/SKILL.md`）
2. `description` は英語で1行（グローバルとproject-localの全スキルで統一）。frontmatter とセクション構成は `_templates/SKILL_TEMPLATE.md` を正とする — 以下は骨格の抜粋:

```markdown
---
name: agent-name
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

上の見出しは `_common/scripts/lint-frontmatter.py` の `ST1`（必須見出し）が実際に検査する集合です。省略すると lint が指摘します。

`## INTERACTION_TRIGGERS`（ユーザー確認が必要な決定ポイントの定義）は、必要なエージェントで使用する任意セクションです。

3. 完全なセクション一覧・順序・記法は `_templates/SKILL_TEMPLATE.md` を参照し、それに沿って作成する
4. **ロスターを更新する（手作業のレジストリは自動同期されない）**:
   - `README.md` / `README_ja.md` のエージェント一覧とエージェント数
   - `index.html`（`const AGENTS` 配列・`SUBCOMMANDS`・英訳・カテゴリ件数・件数を記載した全テキスト）
   - `compass/reference/catalog.md`（カテゴリ節とその件数）
   - `_common/SKILL_PACKS.md`（最低1つのPack、またはoptional／explicit-only配置に登録する）
   - `AGENTS.md` / `CLAUDE.md` のスキル数
5. Recipes や routing を追加・変更した場合は、それぞれの参照ファイル・生成物・ルーティング面も同期する
6. 使用例セクションにサンプルを追加
7. `make check` を通す
8. warning が残る場合は、その warning の仕様に従ってレビュー済み例外として根拠を残す。単に検証を迂回しない

### project-local スキルの変更

project-local スキルはグローバルロスターとは別の運用拡張です。現在の正本は `.claude/skills/`、クロスツール用ミラーは `.agents/skills/` です。

変更時は以下を守ってください:

1. `.claude/skills/<skill-name>/` を正本として意味的な変更を行う
2. `.agents/skills/<skill-name>/` に同じ内容を再帰的に反映する
3. `_common/` または `_templates/` を参照する場合、**正本とミラーの両方**で共有ルートへ解決する symlink を維持する
4. ロスター・fallback・project-local 契約を変える場合は `_common/PROJECT_LOCAL_SKILLS.md` を更新する
5. `make check` を実行する

`_common/scripts/lint-project-local.py` が次の blocking invariant を検証します:

- `PL-1`: registry、canonical roster、mirror roster が一致する
- `PL-2`: canonical / mirror が symlink target を含め再帰的に一致する
- `PL-3`: `_common/` / `_templates/` の参照が共有ルートへ解決し、具体的な参照ファイルが存在する

手動の `diff -rq` は診断には使えますが、PR 可否の正本は `make check` / `lint-project-local.py` です。

### 共有契約・検証ツールの変更

- `_common/*.md` を追加・変更した場合は contract tier / precedence / reachability を確認する
- 新規スキルが共有契約を名指ししても、実行時に解決する `_common` symlink が無ければ contract delivery は成立しない
- checker の変更には、壊れた状態を再現する回帰テストと修復後の成功ケースを追加する
- checker roster を変えた場合は `Makefile`、CI、hook fixture、installer fixture の同期を確認する

### コーディング規約

| 項目 | 規約 |
|------|------|
| 表示名 | PascalCase（例: Scout, Builder, Artisan） |
| frontmatter の `name`・ディレクトリ名 | 小文字 kebab-case（例: `scout`, `builder`, `artisan`） |
| ファイル名 | `<skill-name>/SKILL.md` |
| 出力言語 | 日本語 |
| コード・コミット | 英語 |
| コミット形式 | Conventional Commits |

### コミットメッセージ

```text
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

- [ ] `SKILL.md` が `_templates/SKILL_TEMPLATE.md` と現在の lint 契約に従っている
- [ ] Boundaries（Always/Ask/Never）が明確
- [ ] AUTORUN Support / Nexus Hub Mode が必要な契約どおりに記述されている
- [ ] グローバルロスター変更時、`README.md` / `README_ja.md` と関連レジストリを同期した
- [ ] `index.html`, `compass/reference/catalog.md`, `_common/SKILL_PACKS.md`, `AGENTS.md`, `CLAUDE.md` のうち影響範囲を更新した
- [ ] project-local 変更時、`.claude/skills/*` と `.agents/skills/*` が一致し、共有 symlink が解決する
- [ ] Recipes / routing / shared contract の変更面を同期した
- [ ] `make check` が通る
- [ ] warning / reviewed exception を増やした場合、根拠と境界を記録した
- [ ] 必要な使用例・説明・変更履歴を更新した

## 📝 ドキュメント改善

ドキュメントの改善も歓迎します:
- 誤字脱字の修正
- 説明の明確化
- 使用例の追加
- 翻訳の改善
- 実装済み invariant とドキュメントの差分解消

ドキュメントの重複を増やすより、可能な限り executable check を正本にし、人向け文書からそこへ誘導してください。

## 🤝 コードオブコンダクト

- 建設的なフィードバックを心がける
- 多様な意見を尊重する
- 初心者に優しく対応する

## 📜 ライセンス

コントリビューションは [MIT License](LICENSE) の下で提供されます。
