# JavaScript Ecosystem Anti-Patterns

> node_modules の肥大化、依存関係管理の罠、エコシステム固有の問題、パッケージマネージャー選択

## 1. JavaScript エコシステム 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **JE-01** | **Upgrade Cliff（更新の崖）** | 依存関係のバージョンが大幅に遅れ更新が困難 | 更新に数週間必要、チーム全体がブロック | 継続的な小口更新、Renovate/Dependabot の活用 |
| **JE-02** | **Transitive Bloat（推移的肥大化）** | 直接依存が重い推移的依存を大量に持ち込む | node_modules が 500MB 超、40,000+ ファイル | Bundlephobia/Packagephobia で事前確認、軽量代替を検討 |
| **JE-03** | **Duplicate Dependencies（依存関係の重複）** | 同一パッケージの複数メジャーバージョンが共存 | バンドルサイズ膨張、ランタイムの不整合 | `yarn-deduplicate`、`npm dedupe`、依存関係ツリーの定期整理 |
| **JE-04** | **Dead Dependencies（死んだ依存関係）** | 使用されていないパッケージが残存 | 攻撃面の拡大、不要なバンドルサイズ | `depcheck` / `knip` で定期スキャン、CI に組み込み |
| **JE-05** | **Hidden Config Dependencies（隠れた設定依存）** | Babel/ESLint/Jest 等の設定ファイルが暗黙的にパッケージを参照 | 設定変更時の予期しないエラー、追跡困難 | 設定ファイルの依存関係を明示的にドキュメント化 |
| **JE-06** | **Single-Purpose Micro-Packages（単機能マイクロパッケージ）** | 数行の関数のために外部パッケージを導入 | left-pad 問題、サプライチェーン攻撃リスク | 10行以下の機能は自前実装、ネイティブ API で代替 |
| **JE-07** | **Package Manager Churn（パッケージマネージャー乗り換え）** | npm/yarn/pnpm/bun を頻繁に切り替え | lockfile の不整合、チームの混乱、CI の不安定化 | プロジェクト単位で1つに統一、corepack で管理 |

---

## 2. node_modules 問題の構造的原因と対策

```
根本原因:

  「JavaScript の依存関係マネージャーは実際には依存関係を
   管理していない。ダウンロード・展開ツールに過ぎない。」
  — Christoph Nakazawa (Meta)

  構造的問題:
    → インストール速度は依存グラフの複雑性に比例して劣化
    → 大規模依存関係の追加は全体の開発速度を低下
    → SemVer の範囲解決で不要な重複バージョンが発生
    → インストール後の最適化アルゴリズムが不在

対策マトリクス:

  問題                  | ツール/手法
  ---------------------|----------------------------
  不明な依存関係        | `yarn why`, ripgrep 分析
  未使用パッケージ      | `depcheck`, `knip`, ripgrep
  古いバージョン        | `yarn outdated`, `ncu`
  重複バージョン        | `yarn-deduplicate`, `npm dedupe`
  類似パッケージ併用    | チーム内統一ルール + レビュー
  メンテナンス放棄      | Fork + カスタム公開, resolutions
  サイズ増大            | CI で node_modules サイズ追跡

  根本方針:
    → サードパーティコードを自社コードと同じ厳格さで管理
    → コードレビュー、チームコミュニケーション、継続的監視
```

---

## 3. パッケージマネージャー選択ガイド（2024-2025）

```
主要パッケージマネージャー比較:

  npm:
    ✅ Node.js 同梱、エコシステム標準
    ❌ 大規模プロジェクトでの速度、ディスク使用量
    適用: 小〜中規模プロジェクト、チーム標準が npm

  pnpm:
    ✅ 高速、ディスク効率（コンテンツアドレッサブルストレージ）
    ✅ 厳格なリンク（phantom dependency 防止）
    ❌ 一部ツールとの互換性問題
    適用: モノレポ、ディスク効率が重要な環境

  Yarn (Berry):
    ✅ Plug'n'Play、ゼロインストール
    ✅ `yarn why`, `yarn-deduplicate` 等の分析ツール
    ❌ PnP 移行の学習コスト
    適用: 大規模プロジェクト、厳格な依存管理が必要

  Bun:
    ✅ 極めて高速（Zig ネイティブ実装）
    ✅ パッケージマネージャー + ランタイム + バンドラー統合
    ❌ エコシステム成熟度、Node.js 100% 互換ではない
    適用: 新規プロジェクト、速度が最優先

  選択基準:
    → チームの既存スキル + プロジェクト規模 + CI 環境
    → corepack でバージョン固定、packageManager フィールド宣言
```

---

## 4. サプライチェーンセキュリティ

```
依存関係のセキュリティ対策:

  攻撃面の認識:
    → 典型的な Node.js プロジェクトは数百のサードパーティパッケージに依存
    → 各パッケージが潜在的な攻撃ベクター
    → 古いパッケージ = パッチ未適用のセキュリティホール

  必須対策:
    □ `npm audit` / `pnpm audit` の定期実行
    □ `npm ls --prod` で本番依存関係の可視化
    □ Snyk / Socket.dev による継続的監視
    □ 未使用パッケージの積極的削除（攻撃面縮小）

  高度な対策:
    □ npm overrides / pnpm overrides で脆弱な推移的依存を強制更新
    □ プライベートリポジトリによる承認済みパッケージの管理
    □ lockfile の差分レビューを PR プロセスに組み込み
    □ `socket.dev` による悪意あるパッケージの検出

  ❌ アンチパターン: `npm audit` の警告を無視して本番デプロイ
  ✅ 推奨: セキュリティ監査を CI/CD パイプラインに統合
```

---

## 5. Horizon との連携

```
Horizon での活用:
  1. SCOUT フェーズで JE-01〜07 のスクリーニング
  2. dependency-health-scan.md と連携したエコシステム監査
  3. bundle-size-analysis.md と連携したサイズ最適化
  4. LAB フェーズで代替パッケージの PoC 作成

品質ゲート:
  - バージョン大幅遅延 → 段階的更新計画（JE-01 防止）
  - node_modules 500MB 超 → 依存関係の棚卸し（JE-02 防止）
  - 重複バージョン検出 → dedupe 実行（JE-03 防止）
  - 未使用パッケージ → 削除提案（JE-04 防止）
  - 10行以下の外部依存 → 自前実装提案（JE-06 防止）
  - PM 変更提案 → 移行コスト定量化必須（JE-07 防止）
```

**Source:** [Christoph Nakazawa: Dependency Managers Don't Manage Your Dependencies](https://cpojer.net/posts/dependency-managers-dont-manage-your-dependencies) · [NodeSource: Choosing the Right Package Manager (2024)](https://nodesource.com/blog/nodejs-package-manager-comparative-guide-2024) · [JavaScript Conference: Preventing Dependency Risks](https://javascript-conference.com/blog/node-js-dependency-authentication-security-part-2/)
