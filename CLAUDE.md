# claude-skills

90のグローバルスキルと、このリポジトリ専用の3スキル（`orbit` / `lore` / `darwin`）で構成されるプロンプトエンジニアリングリポジトリ。
成果物はコードではなく SKILL.md ファイル群。

## 構造
- 各スキル: `{skill-name}/SKILL.md` + オプションの `reference/`
- project-localスキル: `.claude/skills/`（正本）+ `.agents/skills/`（同期ミラー）。利用可否とfallbackは `_common/PROJECT_LOCAL_SKILLS.md`
- 共通プロトコル: `_common/` (BOUNDARIES.md, HANDOFF.md 等)
- テンプレート: `_templates/SKILL_TEMPLATE.md`
- エージェントジャーナル: `.agents/` (gitignore対象)
- 外部スキル群: `rig-*` は別リポジトリ (`github.com/simota/rig-agent-skills`) への symlink で `.gitignore` 対象。独自の `core/`・`registry/`・`rig-route` を持つ**完結した別設計**であり、本リポの `_common/` 契約・routing-matrix・Recipe 規約はいずれも適用されない。検査系は symlink を境界として自動除外する（`_common/scripts/_corpus.py`）ため、`rig-*` に対する指摘は出ない。両系統の統合可否は未決。
- 監査成果物: `docs/audit/` (gitignore対象) — 本 repo は監査/レビューの成果物をコミットしない。`verity` / `abide` など report-only レシピの書き込み先はここに限り、結果はコミットメッセージと会話で伝える。

## ルーティング（単一入口）
- 非自明な依頼（複数ステップ・複数領域・スキル選択が自明でないもの）は `nexus` を単一入口とする — 分類 → レシピ/チェーン選択 → 実行までを nexus が担う。
- どのスキルにも該当しない依頼も nexus に投げてよい: LADDER（compass → architect → 明示的フォールバック）がカバレッジを保証する（`nexus/reference/routing-matrix.md` § LADDER）。
- 個別スキルの直接呼び出しは、次の3条件を**すべて**満たす場合に限る: (1) 担当スキルが1つに確定している (2) 成果物が1種類 (3) `_common/BOUNDARIES.md` の境界を1つしか跨がない。1つでも満たさなければ nexus を通す — 「たぶんこのスキル」は条件(1)を満たさない。
- 呼び出し経路にかかわらず、完了判定は `_common/OPERATIONAL.md` § Completion Contract に従う（AC凍結・証拠束縛・型付き繰越・完了スイープ・status非膨張）。nexus 経由かどうかで完了の基準は変わらない。
- 環境レベルの強制（hooks 等によるプロンプト介入）はリポジトリ範囲外のため行わない — 本宣言が単一入口の境界である。
- 自己監査: 30日間隔の監査ルーチンが schedule 登録済み。未登録を検知した場合は `_common/HARNESS_EVOLUTION.md` § Evaluation Cycle の手順で再登録する。

## 規約
- Conventional Commits: `feat(skill-name): description`
- SKILL.md 編集時は既存の CAPABILITIES_SUMMARY コメントブロック形式を維持
- 新規スキル／レシピ／`_common/` プロトコル／ゲートの追加は Complexity Budget（`_common/HARNESS_DEBT.md` §3b）の4項目 `failure` / `effect` / `owner` / `removal` を宣言する。`removal` 空欄は却下 — 既存資産への遡及適用はしない（次に別件で編集する際に付与）
- 実測値（スキル本数等）を散文に直書きしない — 検査が再導出できる形にする（`_common/OPERATIONAL.md` § Derived Numbers）。閾値の定義値はルールなので対象外
- `_common/` は全スキルに影響するため慎重に変更
- 価値が衝突したとき（丁寧さ vs 出荷、安全 vs 使いやすさ）の優先順は `_common/VALUES.md`。文書同士の衝突は § Contract Precedence が別に決める
- Git: @_common/GIT_GUIDELINES.md

## 検査
- `make validate` — 全チェッカーを blocking severity で実行
- `make test` — チェッカーが実際に落ちることを証明する（repoを1箇所ずつ壊す。~20秒）
- `make check` — 上記2つ。CI が走らせるもの
- `make hooks` — clone ごとに1回。pre-commit で `validate` を、`_common/scripts/` に触れたコミットでは `check` を走らせる
- 本リポは main へ直接コミットするため、**hook が実質の強制点**
- **新しい check には、それが落ちるところを見るテストを `_common/scripts/test_checkers.py` に付ける。** テストのない check は常にゼロを返すものと区別がつかない — 実際に2本そうなっていた（`_common/LESSONS.md` L001/L002）
- 機構を伴わない教訓は `_common/LESSONS.md` に入らない。`lint-lessons.py` が「remember to」型の記述を拒否する
