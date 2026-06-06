# Backend Performance Anti-Patterns

> Node.js/バックエンドのパフォーマンス落とし穴、メモリリーク、イベントループブロック、非同期処理の問題

## 1. Node.js パフォーマンス 8 大アンチパターン

| # | アンチパターン | 症状 | 検出方法 | 対策 |
|---|-------------|------|---------|------|
| **BP-01** | **イベントループブロック** | 全リクエストが遅延、CPU 100% | `process.hrtime` でラグ計測 | 重い計算は Worker Threads / `setImmediate()` で分割 |
| **BP-02** | **メモリリーク** | メモリ使用量が単調増加、OOM クラッシュ | `--inspect` + heap snapshot 比較 | リソースクリーンアップ・キャッシュ上限・WeakRef 活用 |
| **BP-03** | **無制限キャッシュ** | Map/Object に際限なくデータ蓄積 | heap snapshot で大きい Map を特定 | LRU + maxSize + TTL でキャッシュ制限 |
| **BP-04** | **同期ファイル I/O** | `readFileSync` 等がイベントループをブロック | `--prof` + 同期 API 検索 | `fs.promises` / Stream API に置換 |
| **BP-05** | **クロージャによる参照保持** | コールバック内で大きなオブジェクトを保持 | heap snapshot で想定外の参照確認 | 必要なデータのみクロージャに渡す・明示的 null 化 |
| **BP-06** | **イベントリスナー未解除** | `EventEmitter.listenerCount` が増加し続ける | MaxListeners 警告 | `removeListener` / `once` / AbortController で確実に解除 |
| **BP-07** | **文字列連結ループ** | 大量データの文字列 `+=` 連結 | CPU プロファイルで文字列操作が上位 | `Array.push` + `join()` / Buffer / Stream に置換 |
| **BP-08** | **コネクションプール枯渇** | DB 接続タイムアウト、リクエスト遅延 | コネクション数監視 | プールサイズ適正化 + 接続リーク検出 + タイムアウト設定 |

---

## 2. イベントループブロックの検出と対策

```
イベントループの仕組み:

  ┌─────────────────────────────┐
  │        timers (setTimeout)   │
  ├─────────────────────────────┤
  │   pending callbacks          │
  ├─────────────────────────────┤
  │   idle, prepare             │
  ├─────────────────────────────┤
  │   poll (I/O callbacks)      │ ← ここで大半の処理
  ├─────────────────────────────┤
  │   check (setImmediate)      │
  ├─────────────────────────────┤
  │   close callbacks           │
  └─────────────────────────────┘

ブロックの原因:
  - JSON.parse/stringify of 大きなオブジェクト
  - 暗号化操作（crypto.pbkdf2Sync）
  - 正規表現の ReDoS (Catastrophic Backtracking)
  - 大量データのソート/フィルタ
  - 同期ファイル I/O (fs.*Sync)

検出コード:
  const start = process.hrtime.bigint();
  setImmediate(() => {
    const lag = Number(process.hrtime.bigint() - start) / 1e6;
    if (lag > 100) alert(`Event loop lag: ${lag}ms`);
  });

対策パターン:
  1. 分割: setImmediate() でバッチ処理を分割
  2. Worker Threads: CPU 集約処理をオフロード
  3. Stream: 大きなデータをチャンク処理
  4. 非同期 API: fs.readFile → fs.promises.readFile
```

---

## 3. メモリリークパターンと対策

### よくあるリークパターン

```
パターン 1: 無制限キャッシュ
  ❌ const cache = new Map(); // 無制限に成長
  ✅ LRU キャッシュ + maxSize + TTL

パターン 2: イベントリスナー未解除
  ❌ emitter.on('data', handler); // 解除忘れ
  ✅ emitter.once('data', handler); // 自動解除
  ✅ const ac = new AbortController();
     emitter.on('data', handler, { signal: ac.signal });
     ac.abort(); // 一括解除

パターン 3: クロージャの参照保持
  ❌ function process(hugeData) {
       return () => console.log(hugeData.length); // hugeData 全体を保持
     }
  ✅ function process(hugeData) {
       const len = hugeData.length; // 必要な値のみ抽出
       return () => console.log(len);
     }

パターン 4: Timer の未クリア
  ❌ setInterval(check, 1000); // 永久に実行
  ✅ const id = setInterval(check, 1000);
     // クリーンアップ時: clearInterval(id);

パターン 5: DB コネクションリーク
  ❌ const conn = await pool.connect();
     await conn.query(sql); // エラー時 release されない
  ✅ try { ... } finally { conn.release(); }
     // または pool.query() を使用（自動 release）
```

### メモリ監視

```
監視メトリクス:
  - process.memoryUsage().heapUsed — ヒープ使用量
  - process.memoryUsage().external — C++ オブジェクト
  - process.memoryUsage().rss — 常駐セットサイズ

アラートしきい値:
  - heapUsed > 70% of max-old-space-size → 警告
  - heapUsed が 10 分で 50MB+ 増加 → リーク疑い
  - rss > 1.5GB（デフォルト設定）→ OOM 危険
```

---

## 4. 非同期処理のアンチパターン

```
❌ Sequential await (直列実行):
  const user = await getUser(id);
  const orders = await getOrders(id);
  const reviews = await getReviews(id);
  // 合計: user時間 + orders時間 + reviews時間

✅ Parallel await (並列実行):
  const [user, orders, reviews] = await Promise.all([
    getUser(id),
    getOrders(id),
    getReviews(id),
  ]);
  // 合計: max(user時間, orders時間, reviews時間)

❌ Unhandled Promise rejection:
  someAsyncFn(); // エラーがどこにも捕捉されない

✅ Always handle errors:
  someAsyncFn().catch(handleError);
  // または try/catch で wrap

❌ Promise.all で 1 つの失敗が全体を止める:
  await Promise.all([critical(), optional()]); // optional 失敗で全停止

✅ Promise.allSettled で個別処理:
  const results = await Promise.allSettled([critical(), optional()]);
  const settled = results.map(r =>
    r.status === 'fulfilled' ? r.value : null
  );
```

---

## 5. Stream 処理のベストプラクティス

```
大きなデータ処理で Stream が必須な場面:
  - ファイルサイズ > 100MB
  - DB から大量行を取得
  - CSV/JSON のバッチ処理
  - HTTP レスポンスのストリーミング

❌ ファイル全体をメモリに読み込み:
  const data = fs.readFileSync('large.csv', 'utf8');
  const lines = data.split('\n'); // メモリ 2 倍使用

✅ Stream で行ごとに処理:
  import { createReadStream } from 'fs';
  import { createInterface } from 'readline';

  const rl = createInterface({
    input: createReadStream('large.csv'),
    crlfDelay: Infinity,
  });

  for await (const line of rl) {
    processLine(line); // 1 行ずつ処理、メモリ一定
  }

Pipeline パターン（Node.js 推奨）:
  import { pipeline } from 'stream/promises';
  await pipeline(
    createReadStream('input.csv'),
    new Transform({ transform(chunk, enc, cb) { /* ... */ } }),
    createWriteStream('output.csv')
  );
```

---

## 6. Bolt との連携

```
Bolt での活用:
  1. PROFILE フェーズで BP-01〜08 のスクリーニング
  2. SELECT フェーズでイベントループラグ計測結果を根拠に
  3. OPTIMIZE フェーズで非同期パターン・Stream 適用
  4. VERIFY フェーズでメモリ監視 + 負荷テスト

品質ゲート:
  - 同期 I/O 使用 → 非同期 API への置換を要求（BP-04 防止）
  - Map/Object キャッシュに maxSize なし → LRU 化を要求（BP-03 防止）
  - await の直列実行 → Promise.all への並列化を提案
  - Worker Threads なしの CPU 集約処理 → オフロードを推奨（BP-01 防止）
```

**Source:** [MarkAICode: Node.js 22 LTS Performance Optimization](https://markaicode.com/nodejs-22-lts-performance-optimization-memory-event-loop/) · [TechDots: Optimizing Node.js Performance](https://www.techdots.dev/blog/optimizing-node-js-performance-memory-management-event-loop-and-async-best-practices) · [DZone: Node.js Performance Tuning](https://dzone.com/articles/nodejs-performance-tuning-advanced-techniques) · [Last9: Monitoring Node.js Key Metrics](https://last9.io/blog/node-js-key-metrics/)
