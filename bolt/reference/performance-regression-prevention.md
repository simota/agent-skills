# Performance Regression Prevention

> パフォーマンスバジェット、CI/CD 統合、回帰検出、継続的モニタリングのベストプラクティス

## 1. パフォーマンスバジェット設計

### バジェット項目と推奨値

| カテゴリ | メトリクス | バジェット | ツール |
|---------|---------|---------|-------|
| **Core Web Vitals** | LCP | ≤ 2.5s | Lighthouse CI / web-vitals |
| | INP | ≤ 200ms | web-vitals |
| | CLS | ≤ 0.1 | Lighthouse CI |
| **バンドル** | 初期 JS | ≤ 200kB (gzip) | webpack-bundle-analyzer |
| | 初期 CSS | ≤ 50kB (gzip) | bundlesize |
| | 総転送量 | ≤ 500kB | Lighthouse CI |
| **リソース** | 画像総量 | ≤ 500kB | Lighthouse CI |
| | サードパーティ JS | ≤ 100kB | bundlesize |
| | フォント | ≤ 100kB | bundlesize |
| **API** | p95 レスポンス | ≤ 200ms | autocannon |
| | エラー率 | ≤ 0.5% | 監視ツール |
| | スループット | ≥ baseline × 0.9 | autocannon |

---

## 2. CI/CD 統合の 3 層アプローチ

### Tier 1: コミットレベル（毎 PR）

```
実行タイミング: PR 作成/更新ごと
所要時間: < 5 分
目的: 明らかな回帰の早期検出

チェック項目:
  ├── バンドルサイズ変化量（±5% 以上で警告）
  ├── Lighthouse CI スコア（Performance ≥ 90）
  ├── Core Web Vitals しきい値
  └── 新規依存パッケージのサイズ検証

Lighthouse CI 設定例:
  // lighthouserc.js
  module.exports = {
    ci: {
      collect: {
        numberOfRuns: 3,
        url: ['http://localhost:3000/', 'http://localhost:3000/dashboard'],
      },
      assert: {
        assertions: {
          'categories:performance': ['error', { minScore: 0.9 }],
          'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
          'interactive': ['error', { maxNumericValue: 3500 }],
          'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        },
      },
      upload: {
        target: 'temporary-public-storage',
      },
    },
  };
```

### Tier 2: マージレベル（main ブランチ）

```
実行タイミング: main マージ後 / 日次
所要時間: 10-30 分
目的: 実環境に近い条件での包括的検証

チェック項目:
  ├── 負荷テスト（10-20 VU, 2-3 分）
  │   p95 < 200ms, エラー率 < 0.5%
  ├── 過去ベースラインとの比較
  │   p95 回帰 > 10% → アラート
  ├── バンドル詳細分析
  │   webpack-bundle-analyzer レポート
  └── E2E パフォーマンス計測
      主要ユーザーフロー（ログイン→ダッシュボード→操作）

autocannon 負荷テスト例:
  npx autocannon -c 20 -d 120 -p 10 http://localhost:3000/api/users
  # -c: 同時接続数, -d: 秒数, -p: パイプライン数
```

### Tier 3: フルスケール（週次/リリース前）

```
実行タイミング: リリース前 / 週次
所要時間: 30-60 分
目的: 本番トラフィックパターンのシミュレーション

チェック項目:
  ├── 本番同等の負荷テスト（100+ VU）
  ├── 長時間テスト（メモリリーク検出）
  ├── スパイクテスト（急激な負荷増加）
  ├── ストレステスト（限界値の確認）
  └── 全ページの Lighthouse 監査
```

---

## 3. 回帰検出の方法論

### 統計的回帰検出

```
単一実行の比較は信頼性が低い:
  - ネットワーク変動、GC タイミング、キャッシュ状態で結果が変わる
  - 最低 3 回実行の中央値で比較

回帰判定基準:
  ├── バンドルサイズ: ±5% で警告、±10% でブロック
  ├── LCP: 前回 p75 の 110% 超で警告
  ├── API p95: 前回ベースラインの 120% 超で警告
  └── メモリ使用量: 前回の 130% 超で警告

ベースライン管理:
  - 各リリースのパフォーマンスメトリクスを記録
  - 直近 5 リリースの移動平均をベースラインとする
  - 季節変動（トラフィックパターン）を考慮
```

### バンドルサイズ回帰検出

```
GitHub Actions での自動チェック:

  1. base ブランチのバンドルサイズを計測
  2. PR ブランチのバンドルサイズを計測
  3. 差分をコメントとして PR に投稿

ツール:
  - bundlesize: package.json に maxSize 定義
  - size-limit: バンドル + 実行時間の制限
  - @next/bundle-analyzer: Next.js 専用

size-limit 設定例:
  // package.json
  {
    "size-limit": [
      { "path": "dist/index.js", "limit": "200 kB" },
      { "path": "dist/index.css", "limit": "50 kB" }
    ]
  }
```

---

## 4. 本番モニタリング戦略

### RUM (Real User Monitoring)

```
web-vitals によるフィールドデータ収集:

  import { onLCP, onINP, onCLS } from 'web-vitals';

  function sendMetric(metric) {
    navigator.sendBeacon('/api/vitals', JSON.stringify({
      name: metric.name,
      value: metric.value,
      rating: metric.rating, // 'good' | 'needs-improvement' | 'poor'
      navigationType: metric.navigationType,
      url: location.href,
      userAgent: navigator.userAgent,
    }));
  }

  onLCP(sendMetric);
  onINP(sendMetric);
  onCLS(sendMetric);

ダッシュボードで追跡:
  - p50 / p75 / p95 の分布
  - デバイス/ブラウザ/地域別の分布
  - 時系列での傾向（回帰検出）
  - 「poor」評価の割合
```

### Synthetic Monitoring

```
Lighthouse CI + Cron:
  - 毎時間、主要ページを監査
  - スコア変化を検出してアラート

WebPageTest API:
  - 複数地域からの計測
  - 接続速度のシミュレーション（3G/4G/ケーブル）

アラート設定:
  - LCP p75 > 2.5s → Slack 通知
  - INP p75 > 200ms → Slack 通知
  - Performance Score < 85 → PagerDuty
```

---

## 5. ビルド破壊 vs レポーティング

| アプローチ | 説明 | 推奨場面 |
|-----------|------|---------|
| **Build Break** | バジェット超過で CI 失敗 | パフォーマンス文化が確立されたチーム |
| **Report Only** | 超過を通知、デプロイは継続 | パフォーマンス改善を始めたチーム |
| **Async Test** | 非同期でテスト、必須報告なし | パフォーマンス監視を始めたばかりのチーム |

```
段階的導入の推奨:

  Phase 1 (Month 1-2): Report Only
    - Lighthouse CI をセットアップ
    - バンドルサイズを計測開始
    - ベースラインを確立

  Phase 2 (Month 3-4): Selective Break
    - バンドルサイズ超過でのみビルド破壊
    - Core Web Vitals は報告のみ

  Phase 3 (Month 5+): Full Enforcement
    - 全バジェット超過でビルド破壊
    - RUM データと統合
    - 自動回帰検出アラート
```

---

## 6. Bolt との連携

```
Bolt での活用:
  1. PROFILE フェーズでパフォーマンスバジェットの現状確認
  2. SELECT フェーズでバジェット超過項目を優先対象に
  3. OPTIMIZE フェーズで改善後にバジェット内を確認
  4. VERIFY フェーズで CI 回帰テストの PASS を確認

品質ゲート:
  - パフォーマンスバジェット未定義 → 設定を推奨（Tier 1 から段階的に）
  - 最適化 PR にバンドルサイズ変化量なし → 計測データの追加を要求
  - 回帰テストなし → Lighthouse CI 設定を推奨
  - RUM 未導入 → web-vitals 計測コードの追加を推奨

Radar ハンドオフ:
  - パフォーマンスバジェット用のテスト作成は Radar に委譲
  - 負荷テストシナリオの設計は Siege に委譲
```

**Source:** [SpeedCurve: Performance Testing in CI](https://www.speedcurve.com/blog/performance-testing-in-ci-lets-break-the-build/) · [DevOps.com: Integrating Performance Testing into CI/CD](https://devops.com/integrating-performance-testing-into-ci-cd-a-practical-framework/) · [SolidAppMaker: Web Performance in 2026](https://solidappmaker.com/web-performance-in-2026-best-practices-for-speed-security-core-web-vitals/) · [Coherence: Performance Testing in CI/CD Pipelines](https://www.withcoherence.com/articles/performance-testing-in-cicd-pipelines-best-practices)
