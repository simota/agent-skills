# Frontend Performance Anti-Patterns

> React/フロントエンドのパフォーマンス落とし穴、React Compiler の影響、レンダリング最適化の誤り

## 1. React パフォーマンス 10 大アンチパターン

| # | アンチパターン | 問題 | React Compiler で解決？ | 対策 |
|---|-------------|------|---------------------|------|
| **FP-01** | **過剰メモ化** | 全てに useMemo/useCallback → コード複雑化、効果なし | Yes（自動化） | 計測で効果確認。Compiler 時代は手動メモ化を減らす |
| **FP-02** | **親コンポーネント内でコンポーネント定義** | 毎回新しいコンポーネント生成 → 状態リセット | No | コンポーネントをファイルトップレベルに定義 |
| **FP-03** | **インラインオブジェクト/配列** | `style={{}}` 等で毎レンダリング新参照 | Yes（自動化） | Compiler なし: useMemo / 定数化 |
| **FP-04** | **巨大 Context** | 1 つの Context に全状態 → 全 consumer 再レンダリング | No | Context 分割（更新頻度別）· State/Dispatch 分離 |
| **FP-05** | **状態の上げすぎ** | 不要な親まで状態を lift → ツリー全体が再レンダリング | No | 状態は必要最小限のコンポーネントに配置 |
| **FP-06** | **key 属性の誤用** | `key={index}` で配列操作時に意図しない再利用 | No | 安定した一意 ID を key に使用 |
| **FP-07** | **レンダリング中の副作用** | レンダリング中に API コール / DOM 操作 | No（Rules of React 違反で Compiler スキップ） | useEffect / イベントハンドラに移動 |
| **FP-08** | **大量リストの非仮想化** | 1000+ アイテムを全て DOM に描画 | No | @tanstack/react-virtual で仮想化 |
| **FP-09** | **画像の未最適化** | 大きな画像を未圧縮・未リサイズで配信 | No | next/image · WebP/AVIF · lazy loading · srcset |
| **FP-10** | **サードパーティスクリプトの無制限読み込み** | 分析・広告・チャット等を全ページで読み込み | No | defer/async · 遅延読み込み · Partytown |

---

## 2. React Compiler（React Forget）の影響

```
React Compiler とは:
  - Babel プラグインとして動作
  - useMemo / useCallback / memo を自動適用
  - React 19 に含まれていない（別途 opt-in）
  - 2024-2026 にかけて段階的にリリース

Compiler が解決すること:
  ✅ 手動メモ化の管理負荷（FP-01, FP-03）
  ✅ 依存配列の誤り
  ✅ Props の浅い比較による不要な再レンダリング

Compiler が解決しないこと:
  ❌ Context の設計問題（FP-04）
  ❌ 状態配置の設計問題（FP-05）
  ❌ 仮想化の必要性（FP-08）
  ❌ データフェッチング戦略
  ❌ 画像最適化（FP-09）
  ❌ Rules of React 違反コード（サイレントスキップ → 新種のバグ）

Compiler 時代の戦略（2025-2026）:
  1. 新規コード: 手動メモ化を避け、Compiler に任せる
  2. 既存コード: 動作中の useMemo/useCallback は急いで削除しない
  3. アーキテクチャに注力: コンポーネント構成・状態配置・Context 設計
  4. Rules of React を厳守: 違反コードは Compiler が最適化をスキップ

注意: Compiler のテストで 8 件の不要な再レンダリングのうち
       1 件しか修正されなかった報告あり
  → Compiler は万能ではなく、アーキテクチャ設計が依然重要
```

---

## 3. レンダリング最適化の正しい優先順序

```
React レンダリング最適化の ROI 順:

  1. コンポーネント構成の改善（最大効果）
     - 「状態を下げる」: 状態を使うコンポーネントに移動
     - 「children パターン」: 変化しない部分を children として渡す
     - Composition over Memoization

  2. 状態管理の最適化
     - Context 分割（更新頻度別）
     - State/Dispatch 分離パターン
     - 外部状態管理（Zustand, Jotai）で選択的購読

  3. 仮想化
     - 100+ アイテムリスト → @tanstack/react-virtual
     - 仮想スクロールで DOM ノード数を制限

  4. コード分割
     - Route-based: lazy(() => import('./pages/X'))
     - Component-based: 重いコンポーネントの遅延読み込み
     - Library-based: 使用時のみ import

  5. メモ化（最小効果・Compiler で自動化予定）
     - useMemo: 高コスト計算のキャッシュ
     - useCallback: 子コンポーネントへのコールバック安定化
     - memo: 重いコンポーネントの再レンダリング防止

注意: 純粋な JS 操作（250 アイテムのソート）は < 2ms
      レンダリングは 20ms+
  → JS 計算の最適化より、再レンダリング削減が効果的
```

---

## 4. 画像・メディア最適化

| 手法 | 効果 | 実装 |
|------|------|------|
| **WebP/AVIF** | JPEG 比 25-50% 小 | `<picture>` + `<source type="image/avif">` |
| **レスポンシブ画像** | デバイスに合ったサイズ | `srcset` + `sizes` |
| **Lazy Loading** | 初期読み込み削減 | `loading="lazy"` (below-the-fold) |
| **Priority Hints** | LCP 画像を優先 | `fetchpriority="high"` (hero 画像) |
| **next/image** | 自動最適化 | Next.js のビルトイン最適化 |
| **SVG の最適化** | 不要メタデータ削除 | SVGO / svgo-loader |
| **動画の代替** | GIF → MP4/WebM | `<video autoplay muted loop>` |

---

## 5. サードパーティスクリプト管理

```
問題: サードパーティスクリプトが TBT (Total Blocking Time) の主因

分類と優先度:
  Critical (同期): 認証・決済 → <head> 内
  Important (defer): 分析 → defer 属性
  Nice-to-have (lazy): チャット・広告 → ユーザーインタラクション後

対策:
  1. defer/async 属性の適切な使用
  2. Partytown: サードパーティを Web Worker で実行
  3. Facade パターン: 軽量プレースホルダー → インタラクション時にロード
     例: YouTube 埋め込み → サムネイル画像 → クリック時に iframe
  4. Resource Hints:
     - dns-prefetch: DNS 解決を先行
     - preconnect: TCP + TLS を先行
  5. 定期的な監査: Coverage タブで未使用コード率を確認
```

---

## 6. Bolt との連携

```
Bolt での活用:
  1. PROFILE フェーズで FP-01〜10 のチェック
  2. SELECT フェーズでレンダリング最適化の優先順序を適用
  3. OPTIMIZE フェーズで Compiler 対応を考慮した実装
  4. VERIFY フェーズで React DevTools + Lighthouse で検証

品質ゲート:
  - 全コンポーネントに memo → 過剰メモ化として警告（FP-01）
  - コンポーネント内コンポーネント定義 → 外部定義を要求（FP-02）
  - 1000+ アイテムリスト → 仮想化を要求（FP-08）
  - 未最適化画像 → next/image 等の使用を推奨（FP-09）
  - Rules of React 違反 → Compiler スキップリスクとして警告（FP-07）
```

**Source:** [DeveloperWay: React Compiler & React 19](https://www.developerway.com/posts/react-compiler-soon) · [Medium: React Compiler Won't Save You](https://medium.com/@domwozniak/react-compiler-wont-save-you-from-this-performance-mistake-a257541fe533) · [DEV.to: React Performance Optimization 15 Best Practices 2025](https://dev.to/alex_bobes/react-performance-optimization-15-best-practices-for-2025-17l9) · [SitePoint: React 19 Compiler What Senior Developers Need to Know](https://www.sitepoint.com/why-react-19-s-compiler-changes-everything-for-senior-devs/)
