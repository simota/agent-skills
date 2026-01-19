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
git clone https://github.com/YOUR_USERNAME/ai-agent-skills.git
cd ai-agent-skills
```

### 新しいエージェントの追加

1. `[AgentName]/SKILL.md` を作成
2. 以下の構造に従う:

```markdown
---
name: AgentName
description: 日本語での説明（1行）
---

You are "AgentName" - [English description of the agent's role].

## Philosophy
[Core principles]

## Boundaries

### Always do:
- [Required behaviors]

### Ask first:
- [Actions requiring confirmation]

### Never do:
- [Prohibited actions]

## INTERACTION_TRIGGERS
[Decision point definitions]

## [Domain-specific sections]
[Templates, patterns, examples]

## AUTORUN Support
[Nexus integration format]

## Nexus Hub Mode
[Hub mode handoff format]

## Output Language
All final outputs must be written in Japanese.

## Git Commit & PR Guidelines
[Commit message conventions]
```

3. `README.md` のエージェント一覧に追加
4. 使用例セクションにサンプルを追加

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
- [ ] README.md を更新した
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
