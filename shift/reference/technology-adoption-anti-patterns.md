# Technology Adoption Anti-Patterns

> 技術選定の失敗パターン、Hype Cycle の罠、評価フレームワーク、Resume Driven Development の回避

## 1. 技術採用 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **TA-01** | **Resume Driven Development（履歴書駆動開発）** | エンジニアのキャリア目的で技術を選定 | 「Rust で書き直そう」「Kubernetes 入れよう」（不要なのに） | ビジネス要件・チーム能力・プロジェクト規模に基づく判断 |
| **TA-02** | **Hype Driven Adoption（ハイプ駆動採用）** | トレンドや話題性だけで技術を導入 | 「みんな使ってる」「HackerNews で人気」が根拠 | Gartner Hype Cycle の位置確認、Trough of Disillusionment 後を待つ |
| **TA-03** | **FAANG Cargo Cult（FAANG カーゴカルト）** | 大企業の事例を自社のコンテキスト無視でコピー | Google規模の技術を10人チームで採用、過剰な複雑性 | 自社の規模・制約・チーム能力に適合する技術を選定 |
| **TA-04** | **Shiny Object Syndrome（新しい物好き症候群）** | 常に最新技術に飛びつき既存を放棄 | 半年ごとにフレームワーク変更、完成しないプロジェクト | 「Good Enough」な技術は変えない、変更コストを定量化 |
| **TA-05** | **Premature Optimization（早すぎる最適化）** | 将来の問題に対して先回りで技術投資 | ユーザー100人でマイクロサービス化、不要なスケーラビリティ対策 | YAGNI 原則、現在の問題に集中、将来は将来対応 |
| **TA-06** | **Innovator's Dilemma（イノベーターのジレンマ）** | 既存技術に固執し破壊的変化を見逃す | 「jQuery で十分」が5年間続く、チームのスキル陳腐化 | 定期的な技術レーダー作成、20%の探索時間確保 |
| **TA-07** | **AI Hype Trap（AI ハイプの罠）** | AI/LLM を万能と過信し不適切に適用 | text-to-SQL の精度不足、AI生成コードの品質未検証 | AI の限界を理解、人間のレビュー必須、適用領域を限定 |

---

## 2. 技術評価フレームワーク

```
Tech Maturity Matrix（2×2 評価）:

  技術成熟度（X軸）:
    Research → Proof of Concept → Early Adoption → Full Adoption

  ビジネス適用性（Y軸）:
    Low → Medium → High

  判断ロジック:
    高成熟度 × 高適用性 → 積極採用（Adopt）
    高成熟度 × 低適用性 → 監視（Watch）
    低成熟度 × 高適用性 → 実験（Trial）
    低成熟度 × 低適用性 → 回避（Avoid）

Gartner Hype Cycle の5段階:
  1. Innovation Trigger（技術の引き金）
  2. Peak of Inflated Expectations（過度な期待のピーク）
  3. Trough of Disillusionment（幻滅の谷）→ ここで脱落多数
  4. Slope of Enlightenment（啓発の坂）
  5. Plateau of Productivity（生産性の安定期）→ 本番採用はここ

  ⚠️ 注意: 実際に Hype Cycle を通過する技術は約20%
  → 大半は Stage 3 で消滅する

Adoption Curve とキャズム:
  Innovators (2.5%) → Early Adopters (13.5%)
    → [CHASM] →
  Early Majority (34%) → Late Majority (34%) → Laggards (16%)
  → キャズムを超えない技術はエンタープライズには危険
```

---

## 3. 実質と誇大宣伝の判別基準

```
技術の「実質性」を判断する 5 つの指標:

  1. ユーザー準備度:
     → チームの学習コストは許容範囲か？
     → 採用企業のケーススタディが存在するか？

  2. ビジネスモデル持続性:
     → OSS の資金源は？ 単一企業依存のリスクは？
     → ライセンス変更の前例は？（Redis, Elasticsearch 等）

  3. インフラ成熟度:
     → ツールチェーン（CI/CD, 監視, デバッグ）は整備されているか？
     → ホスティング・デプロイの選択肢は十分か？

  4. 規制・倫理的実現性:
     → コンプライアンス要件を満たせるか？
     → データプライバシーの懸念はないか？

  5. エコシステム健全性:
     → Stack Overflow の質問数・回答率
     → npm weekly downloads の推移
     → GitHub stars の成長率（急増→急落は危険信号）
     → コントリビューター数とコミット頻度

  失敗した技術の教訓:
    → Google Glass: プライバシー懸念 + コスト
    → Segway: ユーザー行動とのミスマッチ
    → Deno (初期): エコシステム不足
    → text-to-SQL: 精度が期待に達しない
```

---

## 4. Thoughtworks Technology Radar 活用法

```
Technology Radar の 4 リング:

  Adopt（採用）:
    → 業界で広く実証済み、本番利用に推奨
    → Horizon: 既存プロジェクトへの導入を積極的に検討

  Trial（試行）:
    → リスクを管理できるプロジェクトで実験的に使用
    → Horizon: PoC 作成の対象として適切

  Assess（評価）:
    → どう影響するか探索する価値がある
    → Horizon: SCOUT フェーズでの調査対象

  Hold（保留）:
    → 新規プロジェクトでの採用は推奨しない
    → Horizon: 既存利用の置換を検討

  活用方法:
    → 半年ごとの Technology Radar 確認
    → プロジェクトの技術スタックとの照合
    → Hold に入った技術の代替案調査を SCOUT に追加
```

---

## 5. Horizon との連携

```
Horizon での活用:
  1. SCOUT フェーズで TA-01〜07 のスクリーニング
  2. Technology Radar との定期照合
  3. LAB フェーズで Tech Maturity Matrix 評価
  4. PRESENT フェーズで採用判断の根拠提示

品質ゲート:
  - 「みんな使ってる」が根拠 → Hype Cycle 位置確認必須（TA-02 防止）
  - FAANG 事例コピー → 自社規模適合性検証（TA-03 防止）
  - 頻繁なフレームワーク変更 → 変更コスト定量化必須（TA-04 防止）
  - 不要な先行投資 → YAGNI チェック（TA-05 防止）
  - 5年間技術変更なし → 技術レーダー確認（TA-06 防止）
  - AI 万能論 → 適用領域限定 + レビュー必須（TA-07 防止）
```

**Source:** [Product Leadership: Emerging Technologies - Adopt or Avoid](https://www.productleadership.com/blog/emerging-technologies-adopt-or-avoid/) · [Thoughtworks Technology Radar](https://www.thoughtworks.com/radar) · [Gartner Hype Cycle Methodology](https://www.gartner.com/en/research/methodologies/gartner-hype-cycle)
