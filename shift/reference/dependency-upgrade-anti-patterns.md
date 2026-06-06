# Dependency Upgrade Anti-Patterns

> npm/Node.js 依存関係アップグレードの失敗パターン、バージョン管理の罠、アップデート戦略のベストプラクティス

## 1. 依存関係アップグレード 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **DU-01** | **All-at-Once（一括更新）** | 複数メジャーバージョンを同時に更新 | 解決不能な依存関係コンフリクト、デバッグ不能 | パッチ/マイナーは一括、メジャーは1つずつ個別コミット |
| **DU-02** | **Changelog Skip（変更履歴スキップ）** | Breaking Changes を確認せずにバージョンアップ | 統合失敗、予期しない API 変更、ランタイムエラー | GitHub Releases の "Breaking Changes" セクションを必ず確認 |
| **DU-03** | **Version Drift（バージョン漂流）** | 長期間アップデートせず大きなギャップが蓄積 | Node 16 で最新ライブラリが動かない、Upgrade Cliff 発生 | 定期的な小口アップデート、Renovate/Dependabot 活用 |
| **DU-04** | **Legacy Peer Deps Abuse（--legacy-peer-deps 乱用）** | peer dependency 競合を --legacy-peer-deps で無視 | ランタイムエラー、予期しない動作、根本原因の放置 | 一時的ワークアラウンドとしてのみ使用、根本修正を優先 |
| **DU-05** | **Binary Breakage Blindness（バイナリ破壊の軽視）** | Node メジャーバージョン変更時のネイティブモジュール破壊を無視 | 画像処理・暗号化ツールの動作不良、ビルド失敗 | node_modules + lockfile 削除→再インストール、C++ アドオン確認 |
| **DU-06** | **Manual Version Editing（手動バージョン編集）** | package.json のバージョン番号を手動で書き換え | タイポ、lockfile との不整合、バージョン範囲の誤設定 | `pnpm update -i` / `npx ncu -i` 等のインタラクティブツール使用 |
| **DU-07** | **Ambiguous Versioning（曖昧なバージョン指定）** | `^` や `*` で広いバージョン範囲を許容 | 環境間で異なるバージョンがインストール、再現不能バグ | lockfile のコミット必須、本番向けは厳格なバージョン固定 |

---

## 2. アップデート戦略フレームワーク

```
段階的アップデート手順:

  Step 1: パッチ/マイナー一括更新
    → Green/Yellow（パッチ/マイナー）を全て適用
    → テスト実行 → 単独コミット
    → "chore: update non-breaking dependencies"

  Step 2: メジャーバージョン個別更新
    → 1 パッケージずつメジャーバージョンを更新
    → Changelog の Breaking Changes を確認
    → テスト実行 → パッケージごとに個別コミット

  Step 3: 非推奨パッケージの置換
    → 別チケットとして分離（メンテナンス PR に混ぜない）
    → 代替ライブラリの調査 → PoC → 段階的移行

  Step 4: Node.js ランタイム更新
    → LTS バージョンへの移行
    → engines フィールドで最低バージョンを宣言
    → ネイティブモジュールの動作確認

  自動化:
    → Renovate Bot: パッチ自動マージ、メジャーは PR 作成
    → Dependabot: セキュリティアップデートの自動 PR
    → CI パイプラインでの依存関係更新テスト
```

---

## 3. SemVer 判断基準

```
バージョン番号の意味と対応:

  PATCH (x.y.Z):
    → バグ修正、セキュリティパッチ
    → 通常安全、後方互換
    → 対応: 自動マージ可

  MINOR (x.Y.z):
    → 新機能追加、後方互換を維持
    → 対応: テスト実行後マージ

  MAJOR (X.y.z):
    → 意図的な Breaking Changes
    → API 変更、削除、動作変更
    → 対応: Changelog 確認 → コード修正 → テスト → 個別コミット

  ⚠️ 注意: SemVer は「約束」であり「保証」ではない
    → マイナーでも Breaking Change が含まれることがある
    → テストなしでの更新は常にリスク
```

---

## 4. 依存関係ロック戦略

```
Lockfile 管理のベストプラクティス:

  必須:
    □ package-lock.json / pnpm-lock.yaml / yarn.lock をコミット
    □ CI で lockfile ベースのインストール（npm ci / pnpm install --frozen-lockfile）
    □ 環境間で同一の依存関係ツリーを保証

  プライベートリポジトリ:
    → 企業内パッケージリポジトリの活用
    → 「任意の依存関係アップグレードに対する保護層」
    → 本番環境への昇格時の予期しない動作変更を防止

  engines フィールド:
    → package.json に Node.js/pnpm の最低バージョンを宣言
    → CI/CD で自動検証
    → チーム全員の環境を統一
```

---

## 5. Horizon との連携

```
Horizon での活用:
  1. SCOUT フェーズで DU-01〜07 のスクリーニング
  2. dependency-health-scan.md と連携した定期監査
  3. LAB フェーズで段階的アップデート戦略の適用
  4. PRESENT フェーズで更新レポートの提出

品質ゲート:
  - 一括メジャー更新 → 個別更新に分離（DU-01 防止）
  - Changelog 未確認 → Breaking Changes 確認必須（DU-02 防止）
  - 長期未更新 → 定期更新サイクル設定（DU-03 防止）
  - --legacy-peer-deps 使用 → 根本修正計画必須（DU-04 防止）
  - Node バージョン変更 → ネイティブモジュール検証（DU-05 防止）
  - lockfile 未コミット → コミット必須化（DU-07 防止）
```

**Source:** [DEV.to: Updating Node Dependencies - The 2025 Survival Guide](https://dev.to/sarveshh/updating-node-dependencies-the-2025-survival-guide-1ge4) · [ButterCMS: Strategies for Keeping Dependencies Updated](https://buttercms.com/blog/strategies-for-keeping-your-packages-and-dependencies-updated/) · [4markdown: Full Tutorial on Updating Dependencies](https://4markdown.com/full-tutorial-on-updating-dependencies-in-js-projects/) · [freeCodeCamp: How to Update NPM Dependencies](https://www.freecodecamp.org/news/how-to-update-npm-dependencies/)
