# API Security Anti-Patterns

> 認証・認可、レート制限、CORS、データ露出、OWASP API Security Top 10の失敗パターン
>
> **2026-05 baseline**: **OWASP API Security Top 10 2023** がいまだ最新版（2025/2026 改訂は未リリース）。新たに **OWASP Top 10 for Agentic Applications 2026**（2025-12 公開、[genai.owasp.org](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)）がエージェント／LLM API を消費する側のリスクをカバー。ASI01 Agent Goal Hijacking が #1。**RFC 9700 / BCP 240**（2025-01 公開）が OAuth 2.0 セキュリティの Best Current Practice として正式化 — PKCE 必須、Implicit 廃止、redirect_uri 完全一致は BCP-grade 要件になった。

## 1. APIセキュリティ 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **AS-01** | **API Key Only Auth（APIキーのみ認証）** | APIキーを唯一の認証手段として使用 | キー漏洩で全アクセス奪取、ローテーション困難 | OAuth 2.0 + mTLS併用、厳格な有効期限/ローテーション、IP制限/デバイスフィンガープリント |
| **AS-02** | **Broken Object Level Authorization（BOLA）** | オブジェクトIDの操作で他ユーザーのデータにアクセス可能 | OWASP API Top 10 第1位、全API攻撃の40%がBOLA | 全DB操作で認可チェック、推測不能なGUID使用、オブジェクトレベル認可テスト |
| **AS-03** | **Wildcard CORS（ワイルドカードCORS）** | `Access-Control-Allow-Origin: *`で全オリジン許可 | 任意ドメインからの認証済みリクエスト受付 | 信頼ドメインのallowlist、メソッド/ヘッダー制限、credentialed requestsの制御 |
| **AS-04** | **No Rate Limiting（レート制限なし）** | リクエスト数制限がなく、DoS/ブルートフォースに脆弱 | 突然のトラフィック急増で全サービスダウン | リクエストクォータ、IP別制限、指数バックオフ、異常トラフィックアラート |
| **AS-05** | **Excessive Data Exposure（過剰データ露出）** | レスポンスに不要な内部データ・機密情報を含める | DB構造・内部ログ・個人情報がレスポンスに混入 | 必要最小限のデータ返却、スキーマバリデーション、データマスキング、レスポンス監査 |
| **AS-06** | **Inconsistent Auth Standards（認証基準不統一）** | チーム・サービスごとに異なる認証方式 | アドホックな回避策、セキュリティギャップの発生 | 全サービス横断の統一認証/認可標準、最小セキュリティ要件の定義 |
| **AS-07** | **Poor Logging and Monitoring（ログ/監視不足）** | 認証試行・異常アクセスのログが未取得 | インシデント発生後に追跡不能、事後分析不可 | 認証試行/過剰リクエスト/異常パターンのログ、オブザーバビリティシステム統合 |

---

## 2. OWASP API Security Top 10（2023）

| 順位 | リスク | 概要 | 検出パターン |
|------|--------|------|-------------|
| **API1** | Broken Object Level Authorization | IDパラメータ操作で他者データアクセス | `GET /api/users/{id}` のid改変でデータ取得 |
| **API2** | Broken Authentication | 認証フローの欠陥 | トークン無期限、弱いパスワードポリシー |
| **API3** | Broken Object Property Level Authorization | オブジェクトプロパティレベルの認可不備 | mass assignment、不要プロパティ返却 |
| **API4** | Unrestricted Resource Consumption | リソース消費制限なし | 無制限ページサイズ、レート制限なし |
| **API5** | Broken Function Level Authorization | 機能レベル認可不備 | 管理者API直接呼出し、メソッド変更で権限昇格 |
| **API6** | Unrestricted Access to Sensitive Business Flows | 機密ビジネスフロー無制限アクセス | 自動化によるチケット買い占め、アカウント大量作成 |
| **API7** | Server-Side Request Forgery (SSRF) | サーバーサイドリクエスト偽造 | URL入力パラメータで内部サービスアクセス |
| **API8** | Security Misconfiguration | セキュリティ設定ミス | TLS未設定、デバッグモード有効、冗長なエラー |
| **API9** | Improper Inventory Management | API資産管理不備 | 古いバージョン放置、Shadow API、未文書化エンドポイント |
| **API10** | Unsafe Consumption of APIs | 安全でないAPI消費 | サードパーティAPI応答の未検証、リダイレクト追従 |

---

## 3. 認証・認可の罠

```
認証設計の失敗:

  ❌ Bearer Token Without Safeguards（無防備なBearerトークン）:
    → トークン漏洩対策なし、audience検証なし、セッション失効弱い
    → 対策: 短い有効期限、refresh token rotation、audience/issuer厳格検証

  ❌ Implicit Flow in Production（本番でImplicit Flow）:
    → OAuth 2.0 Implicit Flowをプロダクションで使用
    → トークンがURLフラグメントに露出、CSRF脆弱性
    → 対策: Authorization Code Flow + PKCE使用（SPAでも）

  ❌ No Scope Granularity（スコープ粒度不足）:
    → `read` / `write` の2スコープのみで全APIアクセス
    → 最小権限原則違反、過剰権限付与
    → 対策: リソース別・操作別のきめ細かいスコープ設計

  ❌ Missing Token Revocation（トークン失効機能なし）:
    → ユーザーアカウント停止後もトークンが有効
    → 退職者・不正アカウントが継続アクセス
    → 対策: トークンブラックリスト、短い有効期限 + リフレッシュトークンローテーション

  ❌ Encryption Weakness（暗号化の弱さ）:
    → HTTP使用、古いTLSバージョン、弱い暗号アルゴリズム
    → 中間者攻撃、データ傍受
    → 対策: TLS 1.2+強制、AES-256、定期的な暗号監査
```

---

## 4. Defense-in-Depth（多層防御）チェックリスト

```
防御層:
  Layer 1 - Gateway: 認証、スキーマバリデーション、レート制限、CORS
  Layer 2 - Application: 認可、入力バリデーション、ビジネスロジック検証
  Layer 3 - Data: 出力フィルタリング、データマスキング、暗号化
  Layer 4 - Network: ネットワークセグメンテーション、WAF、DDoS防御
  Layer 5 - Monitoring: ログ、異常検知、インシデントレスポンス

重要原則:
  - 単一の防御層に依存しない（どの層も突破される可能性がある）
  - 認証 ≠ 認可（認証しても認可チェックは必須）
  - 入力バリデーションはクライアント側だけでなくサーバー側でも
  - エラーレスポンスで内部詳細を漏洩しない
  - 依存関係の定期的なCVEスキャン
```

---

## 5. Gateway との連携

```
Gateway での活用:
  1. SURVEY フェーズで AS-01〜07 のセキュリティスクリーニング
  2. PLAN フェーズでOWASP API Top 10との照合
  3. VERIFY フェーズで認証/認可/CORS設定の確認
  4. PRESENT フェーズでセキュリティ改善レポート

品質ゲート:
  - APIキーのみ認証 → OAuth 2.0 + PKCE提案（AS-01 防止）
  - ID直接参照+認可チェックなし → BOLA検出・修正提案（AS-02 防止）
  - CORS `*` 設定 → 信頼ドメインallowlist提案（AS-03 防止）
  - レート制限未設定 → 429+Retry-After実装提案（AS-04 防止）
  - レスポンスに不要フィールド → 最小データ返却設計（AS-05 防止）
  - 古いAPIバージョン放置 → 非推奨化+削除計画（OWASP API9 防止）
  - OpenAPIにsecuritySchemes未定義 → セキュリティ定義追加（設定ミス 防止）
```

**Source:** [Nordic APIs: 9 Signs You're Doing API Security Wrong](https://nordicapis.com/9-signs-youre-doing-api-security-wrong/) · [Levo.ai: REST API Security Best Practices 2026](https://www.levo.ai/resources/blogs/rest-api-security-best-practices) · [OWASP: API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/) · [CyCognito: API Security 2026 Guide](https://www.cycognito.com/learn/api-security/) · [Calmops: API Security Beyond JWT](https://calmops.com/programming/rust/api-security-beyond-jwt-oauth2-rate-limiting-cors/) · [Wiz: OWASP API Security Top 10](https://www.wiz.io/academy/api-security/owasp-api-security)
