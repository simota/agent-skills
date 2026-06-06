# Performance Optimization Anti-Patterns

> パフォーマンス最適化の落とし穴、早すぎる最適化、最適化順序の誤り、計測なき最適化の問題

## 1. 最適化 10 大アンチパターン

| # | アンチパターン | 症状 | 影響 | 対策 |
|---|-------------|------|------|------|
| **PO-01** | **早すぎる最適化** | ボトルネック特定前にコードを複雑化 | 可読性低下・保守コスト増・実効果なし | 計測→特定→最適化の順序を厳守 |
| **PO-02** | **計測なき最適化** | プロファイリングせず「遅そう」で最適化 | 実際のボトルネックを見逃す | Chrome DevTools / Lighthouse / clinic.js で計測してから着手 |
| **PO-03** | **マイクロ最適化偏重** | ループ内 1ms 削減に集中、アーキ問題を無視 | N+1 クエリ等の大問題が放置される | 影響度の大きい問題から着手（DB > ネットワーク > レンダリング > JS計算） |
| **PO-04** | **過剰メモ化** | 全てに useMemo/useCallback/memo を適用 | コード複雑化・メモ化コスト > 再計算コスト | 計測で効果確認。React Compiler 時代は手動メモ化を減らす方向へ |
| **PO-05** | **最適化の層違い** | フロントエンドで頑張るがバックエンドがボトルネック | 効果が出ない最適化に時間を浪費 | リクエストライフサイクル全体をプロファイリング |
| **PO-06** | **キャッシュ万能思考** | 全てをキャッシュで解決しようとする | 整合性問題・メモリ圧迫・デバッグ困難 | キャッシュは症状の緩和。根本原因（遅いクエリ等）を先に修正 |
| **PO-07** | **ベンチマーク環境乖離** | 開発環境でのみ計測、本番と条件が異なる | 本番で改善されない・悪化する | RUM (Real User Monitoring) + Synthetic Monitoring の併用 |
| **PO-08** | **回帰テスト不在** | 最適化後のパフォーマンス回帰を検知できない | 新機能追加で最適化が無効化される | Performance Budget + CI/CD 統合 |
| **PO-09** | **ライブラリ盲信** | 「軽量」と謳うライブラリを無検証で導入 | 実際はバンドルサイズ増・パフォーマンス悪化 | bundlephobia で事前検証 + 実測 |
| **PO-10** | **単一メトリクス偏重** | LCP だけ、またはバンドルサイズだけに注目 | 他の指標が悪化（INP 悪化、CLS 増加等） | Core Web Vitals 3 指標 + ビジネスメトリクスの総合評価 |

---

## 2. 最適化の正しい順序

```
最適化の ROI が高い順（一般的なWebアプリケーション）:

  1. データベースクエリ（最大効果）
     - N+1 解消: 100→1 クエリ = 40x 高速化
     - インデックス追加: Seq Scan → Index Scan = 10-100x
     - 不要カラム除外: SELECT * → 必要カラム = 2-5x

  2. ネットワーク・API
     - ペイロード削減: 不要データ除外 = レイテンシ改善
     - バッチ API: N リクエスト → 1 リクエスト
     - 圧縮: gzip/brotli = 60-80% 転送量削減

  3. キャッシュ戦略
     - HTTP キャッシュ: 再リクエスト回避
     - CDN: エッジ配信 = TTFB 改善
     - アプリケーションキャッシュ: DB 負荷軽減

  4. フロントエンドレンダリング
     - SSR/SSG: 初期描画高速化
     - コード分割: 初期バンドル削減
     - 仮想化: 大量リスト対応

  5. JavaScript 計算（最小効果）
     - 配列操作最適化: 250 アイテムソート < 2ms
     - 重い計算 → Web Worker
     - デバウンス/スロットル

注意: 5 から始めるのが PO-03 の典型例
      1 から始めるのがプロの最適化
```

---

## 3. 計測の 3 層モデル

| 層 | ツール | メトリクス | タイミング |
|---|--------|---------|---------|
| **開発時** | React DevTools · Chrome Performance · Lighthouse | Render time · Bundle size · LCP/INP/CLS | PR ごと |
| **CI/CD** | Lighthouse CI · webpack-bundle-analyzer · autocannon | Budget 超過 · 回帰検出 · スループット | マージごと |
| **本番** | RUM (web-vitals) · Synthetic Monitoring · APM | p50/p75/p95 · エラー率 · ビジネス影響 | 常時 |

```
計測なしで最適化してはいけない理由:

  人間の直感は信頼できない:
    - 「この関数が遅い」→ 実測するとレンダリングの 2%
    - 「メモ化すれば速くなる」→ メモ化のオーバーヘッド > 再計算コスト
    - 「バンドルが大きい」→ 実は画像が 80%

  正しいアプローチ:
    1. 症状を特定（「ページ読み込みが 5 秒」）
    2. プロファイリングで原因特定（「API レスポンス 3 秒 + レンダリング 1.5 秒」）
    3. 最大要因から対処（「API の N+1 解消 → 3 秒→0.1 秒」）
    4. 効果を計測（「5 秒 → 2.1 秒 = 58% 改善」）
```

---

## 4. 最適化判定フローチャート

```
パフォーマンス問題を検出したら:

  1. 計測した？ → No → 計測してからやり直し
                → Yes ↓

  2. ボトルネックは？
     ├─ DB クエリ → EXPLAIN ANALYZE → インデックス/N+1/クエリ書き換え
     ├─ ネットワーク → ペイロード/リクエスト数/圧縮を確認
     ├─ レンダリング → React DevTools で再レンダリング確認
     ├─ バンドルサイズ → bundle-analyzer で大きいライブラリ特定
     └─ JS 計算 → Chrome Performance で長いタスク特定

  3. 変更は < 50 行？ → No → 分割できないか検討
                     → Yes ↓

  4. テストは通る？ → No → 修正
                   → Yes ↓

  5. 改善を計測した？ → No → 計測
                     → Yes → PR 作成（What/Why/Impact/Measurement）
```

---

## 5. Bolt との連携

```
Bolt での活用:
  1. PROFILE フェーズで PO-01〜10 のチェックリスト適用
  2. SELECT フェーズで最適化の正しい順序を遵守
  3. OPTIMIZE フェーズで計測の 3 層モデルを活用
  4. VERIFY フェーズで回帰テスト実施

品質ゲート:
  - 計測データなしの最適化提案 → ブロック（PO-02 防止）
  - < 1ms の改善 → マイクロ最適化として却下（PO-03 防止）
  - 全関数に useMemo → 過剰メモ化として警告（PO-04 防止）
  - パフォーマンスバジェット未設定 → CI 統合を推奨（PO-08 防止）
```

**Source:** [Stackify: Why Premature Optimization is Evil](https://stackify.com/premature-optimization-evil/) · [Revelo: How to Avoid Premature Optimization](https://www.revelo.com/blog/premature-optimization) · [Landskill: JavaScript Performance Optimization 2026](https://www.landskill.com/blog/javascript-performance-optimization/) · [TechLasi: Software Performance Optimization Tips 2026](https://techlasi.com/savvy/software-performance-optimization-tips/)
