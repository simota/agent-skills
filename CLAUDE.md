# claude-skills

124のスキルエージェントで構成されるプロンプトエンジニアリングリポジトリ。
成果物はコードではなく SKILL.md ファイル群。

## 構造
- 各スキル: `{skill-name}/SKILL.md` + オプションの `reference/`
- 共通プロトコル: `_common/` (BOUNDARIES.md, HANDOFF.md 等)
- テンプレート: `_templates/SKILL_TEMPLATE.md`
- エージェントジャーナル: `.agents/` (gitignore対象)
- 監査成果物: `docs/audit/` (gitignore対象) — 本 repo は監査/レビューの成果物をコミットしない。`verity` / `abide` など report-only レシピの書き込み先はここに限り、結果はコミットメッセージと会話で伝える。

## ルーティング（単一入口）
- 非自明な依頼（複数ステップ・複数領域・スキル選択が自明でないもの）は `nexus` を単一入口とする — 分類 → レシピ/チェーン選択 → 実行までを nexus が担う。
- どのスキルにも該当しない依頼も nexus に投げてよい: LADDER（compass → architect → 明示的フォールバック）がカバレッジを保証する（`nexus/reference/routing-matrix.md` § LADDER）。
- 個別スキルの直接呼び出しは引き続き可能（担当が自明な単発作業向け）。
- 環境レベルの強制（hooks 等によるプロンプト介入）はリポジトリ範囲外のため行わない — 本宣言が単一入口の境界である。
- 自己監査: 30日間隔の監査ルーチンが schedule 登録済み。未登録を検知した場合は `_common/HARNESS_EVOLUTION.md` § Evaluation Cycle の手順で再登録する。

## 規約
- Conventional Commits: `feat(skill-name): description`
- SKILL.md 編集時は既存の CAPABILITIES_SUMMARY コメントブロック形式を維持
- `_common/` は全スキルに影響するため慎重に変更
- Git: @_common/GIT_GUIDELINES.md
