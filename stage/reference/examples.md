# Stage Examples

> Preview commands assume Marp CLI 4.4.0 (`npx @marp-team/marp-cli@4.4`), reveal.js 6.0.1, and Slidev 52.15.2 as of 2026-05.

## Example 1: LT (5 min) — Product Feature Launch

```markdown
---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# Real-time Collaboration
## チームの生産性を10x にする新機能

Author Name | 2026-04-09

<!-- 30秒 — フック -->

---

# 問題: 非同期のコストは高い

- Slack → メール → ドキュメント → またSlack
- 平均 **23分** のコンテキストスイッチコスト
- チームの **40%** が情報の分散に不満

<!-- 45秒 — 問題定義。数字で説得力を出す -->

---

# 解決: リアルタイムコラボレーション

![bg right:40%](collaboration-demo.png)

- 同一画面でリアルタイム編集
- インライン コメント & リアクション
- 変更の即座な反映

<!-- 60秒 — ソリューション紹介。スクリーンショットを右側に -->

---

# デモ

> ここでライブデモ (2分)

1. ドキュメント作成
2. チームメンバー招待
3. リアルタイム編集
4. コメント & 解決

<!-- 120秒 — ライブデモ。Director/Reel に録画を依頼可能 -->

---

<!-- _class: lead -->

# 本日から利用可能 🚀

**try.example.com/collab**

QRコード → [リンク]

<!-- 30秒 — CTA。QRコードで即座にアクセス -->
```

**Speaker Notes Summary:**
| Slide | Time | Key point |
|-------|------|-----------|
| 1 | 0:00-0:30 | Hook with title |
| 2 | 0:30-1:15 | Problem with stats |
| 3 | 1:15-2:15 | Solution overview |
| 4 | 2:15-4:15 | Live demo |
| 5 | 4:15-5:00 | CTA and close |

## Example 2: Technical Tutorial (15 min)

```markdown
---
marp: true
theme: default
paginate: true
header: "Hono + Cloudflare Workers 入門"
---

<!-- _class: lead -->

# Hono + Cloudflare Workers
## 5分でデプロイするAPI

<!-- 目標: 参加者が自分でAPIをデプロイできるようになる -->

---

# 今日のゴール

✅ Hono の基本を理解する
✅ Cloudflare Workers にデプロイする
✅ 認証ミドルウェアを追加する

**前提:** Node.js 18+, Cloudflare アカウント

---

# Step 1: プロジェクト作成

​```bash
npm create hono@latest my-api
cd my-api
npm install
​```

> `cloudflare-workers` テンプレートを選択

---

# Step 2: ルート定義

​```typescript
import { Hono } from 'hono'

const app = new Hono()

app.get('/', (c) => c.json({ message: 'Hello!' }))
app.get('/users/:id', (c) => {
  const id = c.req.param('id')
  return c.json({ id, name: 'User ' + id })
})

export default app
​```

<!-- ポイント: Express に似た書き方で学習コストが低い -->
```
