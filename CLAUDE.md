# claude-skills

136のスキルエージェントで構成されるプロンプトエンジニアリングリポジトリ。
成果物はコードではなく SKILL.md ファイル群。

## 構造
- 各スキル: `{skill-name}/SKILL.md` + オプションの `reference/`
- 共通プロトコル: `_common/` (BOUNDARIES.md, HANDOFF.md 等)
- テンプレート: `_templates/SKILL_TEMPLATE.md`
- エージェントジャーナル: `.agents/` (gitignore対象)

## 規約
- Conventional Commits: `feat(skill-name): description`
- SKILL.md 編集時は既存の CAPABILITIES_SUMMARY コメントブロック形式を維持
- `_common/` は全スキルに影響するため慎重に変更
- Git: @_common/GIT_GUIDELINES.md
