# Judge: Code Smell Detection During Review

> Judge レビュー時の構造的コードスメル検出ヒューリスティクスと Severity 加重ルール

For the shared smell taxonomy (definitions, recognition patterns, canonical examples), see
`_common/CODE_SMELL_CATALOG.md`. This file only covers Judge-specific detection-during-review
heuristics, severity weighting, and routing.

---

## 1. 検出レイヤーの位置づけ

```
Judge の検出レイヤー:
  Layer 1: バグパターン    → bug-patterns.md
  Layer 2: 一貫性問題      → consistency-patterns.md
  Layer 3: コードスメル    → 本ファイル + _common/CODE_SMELL_CATALOG.md
  Layer 4: テスト品質      → test-quality-patterns.md

コードスメル = 即座のバグではないが、メンテナンス性・拡張性を劣化させる構造的問題
```

---

## 2. レビュー時の検出ヒューリスティクス

Diff レビュー中に「新規導入された」スメルを検出する手順。既存コードのスメルは対象外。

```
Step 1: 構造変化のあるファイルを抽出
  - +50 行以上の追加 → BLOAT 系の疑い
  - 新規クラス/モジュール → BLOAT-002/CHG-001 の疑い
  - 同一修正が複数ファイル → CHG-002 (Shotgun Surgery)

Step 2: 構造指標を機械的に算出（catalog の Recognition に従う）
  - 関数 LOC、パラメータ数、ネスト深度、CC
  - クラス LOC、メソッド数、依存数

Step 3: しきい値超過のみフラグ（後述マトリクス）

Step 4: route 先エージェントを決定
  - リファクタ系 → Zen
  - アーキテクチャ系 → Atlas
  - 削除系 → Sweep
  - 型設計系 → Quill
```

---

## 3. 検出しきい値マトリクス（Judge 専用）

レビュー時に「報告するか否か」のしきい値。Catalog の Recognition より厳しめ
（レビューノイズを抑えるため）。

| Catalog ID | スメル | 検出指標 | 報告しきい値 | Severity | Route |
|------------|-------|---------|------------|----------|-------|
| BLOAT-001 | Long Function | 関数行数 | > 50 | LOW | → Zen |
| BLOAT-001 | Long Function | パラメータ数 | > 5 | LOW | → Zen |
| BLOAT-002 | God Class | メソッド数 | > 20 | MEDIUM | → Zen |
| BLOAT-002 | God Class | クラス行数 | > 500 | MEDIUM | → Zen |
| BLOAT-005 | Primitive Obsession | 同型パラメータ数 | ≥ 3 | LOW | → Zen / Quill |
| CHG-002 | Shotgun Surgery | 同一修正の散在 | 5+ files | MEDIUM | → Atlas |
| CPL-001 | Feature Envy | チェーン深度 | a.b.c.d | LOW | → Zen |
| CPL-002 | Inappropriate Intimacy | private 越境/循環参照 | 任意 | MEDIUM | → Atlas |
| CTRL-001 | Spaghetti | 循環的複雑度 | > 15 | MEDIUM | → Zen |
| CTRL-001 | Spaghetti | ネスト深度 | > 4 | MEDIUM | → Zen |
| DISP-001 | Dead Code | 未使用 export | 任意 | INFO | → Sweep |
| DISP-004 | Duplicated Logic | 類似ブロック | 3行+ × 2箇所+ | LOW | → Zen |
| DISP-006 | Magic Number | リテラル値 | context 依存 | INFO | → Zen |

---

## 4. Severity 加重ルール

Catalog の baseline severity を、レビュー文脈で上下させる規則。

```
+1 段階 (LOW → MEDIUM, MEDIUM → HIGH):
  - public API / 外部契約に露出
  - hot path (1日10万回以上呼ばれる経路)
  - セキュリティ境界に隣接

-1 段階 (MEDIUM → LOW, LOW → INFO):
  - test / fixture / scripts/ 配下
  - 一時的な migration コード（期限明記あり）
  - prototyping / spike ブランチ
```

---

## 5. レポート出力

### 報告フォーマット

```markdown
## Code Smell Findings

| ID | Type (Catalog) | File:Line | Description | Severity | Route |
|----|----------------|-----------|-------------|----------|-------|
| F-001 | God Class (BLOAT-002) | src/services/UserManager.ts | 35 methods, 890 LOC | MEDIUM | → Zen |
| F-002 | Long Function (BLOAT-001) | src/utils/transform.ts:45 | 120 LOC, 8 params | LOW | → Zen |
| F-003 | Dead Code (DISP-001) | src/legacy/old-helper.ts | Unused export (3 functions) | INFO | → Sweep |
```

### 報告ポリシー

```
1. バグパターンを優先（スメルは補助的情報）
2. MEDIUM 以上のスメルのみ主要レポートに含める
3. INFO / LOW は "Additional Observations" セクションへ
4. 新規導入のスメルのみ報告（既存コードは対象外）
5. route 先エージェントを必ず指定
6. Catalog ID を併記して同義語の混乱を防ぐ
```

---

## 6. フレームワーク固有のスメル（レビュー時の追加チェック）

Catalog の Section 8 に加え、Judge は以下を diff スキャン時に追加チェック。

```
React:
  - Prop Drilling 3層以上 → Context/State 管理を推奨
  - useEffect 依存配列の不備 → bug-patterns.md にルーティング
  - コンポーネント肥大化（300行+）→ 分割推奨 (Route: Zen)

Express / API:
  - Fat Controller (ルートハンドラにビジネスロジック) → Service 層分離 (Route: Atlas)
  - エラーハンドリングの不統一 → consistency-patterns.md にルーティング
  - ミドルウェアチェーンの過度な複雑さ → 簡素化推奨 (Route: Zen)

TypeScript:
  - any 型の多用 → 型定義化 (Route: Quill)
  - type assertion (as) の多用 → 型設計の見直し (Route: Quill)
  - enum vs union type の不統一 → consistency-patterns.md にルーティング
```

---

**Source:** [CodeRabbit: 5 Code Review Anti-Patterns](https://www.coderabbit.ai/blog/5-code-review-anti-patterns-you-can-eliminate-with-ai) · [DZone: Code Review Patterns and Anti-Patterns](https://dzone.com/refcardz/code-review-patterns-and-anti-patterns) · [HackerNoon: Code Review Anti-Patterns](https://hackernoon.com/code-review-anti-patterns-how-to-stop-nitpicking-syntax-and-start-improving-architecture)
