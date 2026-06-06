# Narrative Frameworks Reference

**Purpose:** Saga が使用するストーリーテリングフレームワークの詳細仕様。
**Read when:** フレームワークの詳細構造、適用ガイドライン、具体的な記入例が必要な時。

---

## 1. StoryBrand SB7 Framework

Donald Miller が提唱した7要素のブランドストーリーフレームワーク。プロダクトメッセージング、LP、ピッチに最適。

### Structure

```
┌─────────────────────────────────────────────────────┐
│  1. HERO (Customer)                                  │
│     顧客が何かを望んでいる                           │
│            ↓                                         │
│  2. PROBLEM                                          │
│     外的・内的・哲学的な問題に直面                    │
│            ↓                                         │
│  3. GUIDE (Your Product)                             │
│     共感 + 権威を持つガイドが現れる                  │
│            ↓                                         │
│  4. PLAN                                             │
│     ガイドが明確なプラン（3ステップ以内）を示す      │
│            ↓                                         │
│  5. CALL TO ACTION                                   │
│     行動を促す（直接的 + 移行的）                    │
│            ↓                                         │
│  ┌────────────┬────────────┐                         │
│  │ 6. FAILURE │ 7. SUCCESS │                         │
│  │ 行動しない │ 行動した   │                         │
│  │ と何が起こ │ 結果の姿   │                         │
│  │ るか       │            │                         │
│  └────────────┴────────────┘                         │
└─────────────────────────────────────────────────────┘
```

### BrandScript Template

```markdown
## BrandScript: [プロダクト名]

### 1. Hero（顧客）
[顧客は誰か。何を望んでいるか]
- 望み: ____

### 2. Problem（問題）
- 外的問題（External）: [具体的・表面的な障壁]
- 内的問題（Internal）: [感情的な不安・フラストレーション]
- 哲学的問題（Philosophical）: [「〜であるべきだ」という信念]
- 悪役（Villain）: [問題を擬人化した存在]

### 3. Guide（ガイド = プロダクト）
- 共感（Empathy）: [「あなたの気持ちはわかります」]
- 権威（Authority）: [実績・数字・証言]

### 4. Plan（プラン）
1. [ステップ1]
2. [ステップ2]
3. [ステップ3]

### 5. Call to Action
- 直接的CTA: [今すぐ〜する]
- 移行的CTA: [まずは〜してみる]

### 6. Failure（失敗）
[行動しないと何を失うか]

### 7. Success（成功）
[行動した結果、どんな姿になるか]
```

### Application Tips
- 問題は3レイヤー（外的/内的/哲学的）すべて埋める
- Guideは「共感」が先、「権威」が後
- Planは3ステップ以内（認知負荷を減らす）
- FailureとSuccessは対比させる

---

## 2. Pixar Story Spine

Pixar の Emma Coats が提唱した6行のストーリーテンプレート。短いシナリオ、社内共有、エレベーターピッチに最適。

### Structure

```markdown
## Story Spine: [タイトル]

**Once upon a time...（昔々…）**
[主人公の日常と世界観]

**Every day...（毎日…）**
[繰り返されるルーティン・現状]

**Until one day...（ある日…）**
[変化のきっかけ・出来事]

**Because of that...（そのせいで…）**
[連鎖する結果①]

**Because of that...（そのせいで…）**
[連鎖する結果②]

**Until finally...（そしてついに…）**
[クライマックス・解決]

**And ever since that day...（それ以来…）**
[新しい日常・変容後の世界]
```

### Product Adaptation

| Spine Element | Product Context |
|--------------|-----------------|
| Once upon a time | ターゲット顧客の現状 |
| Every day | 繰り返される課題・痛み |
| Until one day | プロダクトとの出会い |
| Because of that (×2) | プロダクトがもたらす変化の連鎖 |
| Until finally | 最終的な成果・変容 |
| Ever since that day | 新しい日常 |

### Example

```
Once upon a time, フリーランスの佐藤さんは毎月の請求書を手作業で作っていた。
Every day, Excelを開いて金額を計算し、PDFに変換し、メールで送る作業に2時間かけていた。
Until one day, [プロダクト名]を試してみた。
Because of that, 請求書が取引データから自動生成されるようになった。
Because of that, 月末の2時間が15分に短縮され、未回収も自動リマインドで減った。
Until finally, 佐藤さんは請求業務のストレスから解放され、本業に集中できるようになった。
And ever since that day, 「お金の管理」は不安の種ではなく、ビジネスの味方になった。
```

---

## 3. Hero's Journey (Product Adapted)

Joseph Campbell / Dan Harmon の物語構造をプロダクト文脈に適応。大きな変容ストーリー、ケーススタディに最適。

### Simplified Product Journey (6 Stages)

```
┌─────────────────────────────────────────────┐
│                                             │
│    1. ORDINARY WORLD                        │
│    （顧客の日常・現状の課題）               │
│              ↓                              │
│    2. CALL TO ADVENTURE                     │
│    （変化の必要性に気づく）                 │
│              ↓                              │
│    3. CROSSING THE THRESHOLD                │
│    （プロダクトを試す決断）                 │
│              ↓                              │
│    4. TRIALS & ALLIES                       │
│    （導入の課題・サポートとの出会い）       │
│              ↓                              │
│    5. TRANSFORMATION                        │
│    （劇的な変化・成果）                     │
│              ↓                              │
│    6. RETURN WITH THE ELIXIR                │
│    （新しい日常・他者への共有）             │
│                                             │
└─────────────────────────────────────────────┘
```

### Template

```markdown
## Hero's Journey: [顧客名/ペルソナ名]

### 1. Ordinary World（日常）
[顧客の現状。何に困っているか。どんな日々を送っているか]

### 2. Call to Adventure（冒険への誘い）
[何がきっかけで変化を求めたか。限界点は何だったか]

### 3. Crossing the Threshold（境界の超越）
[プロダクトを選んだ決断。何が後押しになったか]

### 4. Trials & Allies（試練と仲間）
[導入初期の課題。どうやって乗り越えたか。誰が助けたか]

### 5. Transformation（変容）
[具体的な成果。数字・感情の両面で何が変わったか]

### 6. Return with the Elixir（帰還）
[新しい日常。この経験から得た知恵。他者への影響]
```

---

## 4. JTBD Job Story

Clayton Christensen / Alan Klement の JTBD 理論に基づくジョブストーリー。個別機能のユースケース、開発チーム向けに最適。

### Structure

```
When [状況/コンテキスト],
I want to [モチベーション/行動],
so I can [期待する成果].
```

### Extended Job Story Template

```markdown
## Job Story: [機能/ユースケース名]

### Context（状況）
**When** [具体的な状況・トリガー]
- 場所: [どこで]
- タイミング: [いつ]
- 感情状態: [どんな気持ちで]
- 制約: [何に縛られて]

### Motivation（動機）
**I want to** [したい行動]
- 機能的ニーズ: [タスクを完了したい]
- 感情的ニーズ: [安心したい/自信を持ちたい]
- 社会的ニーズ: [認められたい/貢献したい]

### Outcome（成果）
**So I can** [得たい結果]
- 直接的成果: [すぐに得られること]
- 間接的成果: [長期的に得られること]

### Forces（採用/不採用の力学）
| Force | Direction | Description |
|-------|-----------|-------------|
| Push（現状の不満） | → 新しい解決策へ | [何が不満か] |
| Pull（新解決策の魅力） | → 新しい解決策へ | [何が魅力か] |
| Anxiety（不安） | ← 現状維持へ | [何が不安か] |
| Habit（習慣） | ← 現状維持へ | [何が障壁か] |
```

---

## 5. Story Mapping (Jeff Patton)

プロダクト全体のナラティブフローを可視化。プロダクトディスカバリー、ロードマップ設計に最適。

### Structure

```
Backbone（JTBD/大きな活動）
┌──────┬──────┬──────┬──────┬──────┐
│Act 1 │Act 2 │Act 3 │Act 4 │Act 5 │
├──────┼──────┼──────┼──────┼──────┤  ← Walking Skeleton (MVP)
│Step  │Step  │Step  │Step  │Step  │
│1a    │2a    │3a    │4a    │5a    │
├──────┼──────┼──────┼──────┼──────┤  ← Release 2
│Step  │Step  │Step  │Step  │Step  │
│1b    │2b    │3b    │4b    │5b    │
├──────┼──────┼──────┼──────┼──────┤  ← Release 3
│Step  │Step  │Step  │Step  │Step  │
│1c    │2c    │3c    │4c    │5c    │
└──────┴──────┴──────┴──────┴──────┘
```

### Narrative Flow Template

```markdown
## Story Map: [プロダクト/機能名]

### Narrative Backbone
1. **[活動1]** - [ユーザーが最初にすること]
2. **[活動2]** - [次にすること]
3. **[活動3]** - [メインの活動]
4. **[活動4]** - [結果の確認]
5. **[活動5]** - [繰り返し/共有]

### Walking Skeleton（MVP ストーリー）
[最小限のストーリーフロー。各活動の最もシンプルなステップ]

### Release Slices
- **Release 1（MVP）:** [最小限の物語が成立するスライス]
- **Release 2:** [物語を豊かにするスライス]
- **Release 3:** [完全な物語体験のスライス]
```

---

## 6. CAR Framework

Context→Action→Results の3要素。成果重視のケーススタディ、導入事例に最適。

### Template

```markdown
## Case Study: [顧客名/プロジェクト名]

### Context（背景）
[顧客の状況、業界、規模、課題]
- 業界: [___]
- 規模: [___]
- 課題: [___]

### Action（行動）
[何を導入し、どのように活用したか]
- 導入プロセス: [___]
- 活用方法: [___]
- 期間: [___]

### Results（成果）
[具体的な成果。数値で示す]
- 定量成果: [___% 改善 / ___時間削減 / ___円の効果]
- 定性成果: [チームの変化 / 文化の変化]
- 顧客の声: 「[引用]」
```

---

## 7. Promised Land Framework (Andy Raskin)

戦略的ポジショニングナラティブ。資金調達、組織アライメント、セールスデッキに最適。顧客を「約束の地」へ導く物語。

### Structure (5 Elements)

```
┌─────────────────────────────────────────────────────┐
│  1. CHANGE（変化）                                   │
│     世界に起きている大きく否定できない変化を示す     │
│              ↓                                       │
│  2. STAKES（賭け金）                                 │
│     この変化により勝者と敗者が生まれることを示す     │
│              ↓                                       │
│  3. PROMISED LAND（約束の地）                        │
│     顧客が到達すべき魅力的な未来像を描く            │
│     （自社なしでは到達が困難であること）             │
│              ↓                                       │
│  4. MAGIC GIFTS（魔法の贈り物）                     │
│     約束の地へ到達するためのプロダクト機能を         │
│     「贈り物」として紹介する                         │
│              ↓                                       │
│  5. EVIDENCE（証拠）                                 │
│     この物語が実現可能であることを示す証拠           │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Template

```markdown
## Strategic Narrative: [プロダクト名]

### 1. Change（否定できない変化）
[業界/世界に起きている大きな変化。データで裏付ける]

### 2. Stakes（勝者と敗者）
- **勝者:** [この変化に適応した企業/人はどうなるか]
- **敗者:** [適応しなかった企業/人はどうなるか]

### 3. Promised Land（約束の地）
[顧客が到達すべき未来像。具体的で魅力的に描写]
- この未来は、自社プロダクトなしでは到達が困難

### 4. Magic Gifts（魔法の贈り物）
[プロダクトの機能を「約束の地への道具」として紹介]
- Gift 1: [機能→もたらす変化]
- Gift 2: [機能→もたらす変化]
- Gift 3: [機能→もたらす変化]

### 5. Evidence（証拠）
[すでにこの物語が実現している事例・数値]
- [顧客事例/トラクション]
- [業界データ/第三者評価]
```

### Application Tips
- 「約束の地」は顧客にとって魅力的だが、自社なしでは到達困難（improbable）であること
- 機能を「Magic Gifts」として位置付ける—顧客（Hero）が約束の地に到達するための「武器」
- Change は否定できないものを選ぶ—聴衆が「それは違う」と言えないレベル
- Zuora の "Subscription Economy" デッキが代表的成功例

---

## 8. ABT Framework (And, But, Therefore)

Randy Olson が科学コミュニケーションから提唱した3要素の最小ナラティブ構造。ソーシャルメディア投稿、社内コミュニケーション、簡潔なメッセージングに最適。

### Structure

```
[Context] AND [Additional context],
BUT [Tension/problem],
THEREFORE [Resolution/action].
```

### Template

```markdown
## ABT Narrative: [テーマ]

### And（そして）
[状況設定。共有できるコンテキスト。聴衆が「そうだね」と頷ける前提]

### But（しかし）
[テンション。問題・課題・障壁。「だけど…」の転換点]

### Therefore（だから）
[解決。行動・提案・結論。「だから…」の帰結]

### 完成文
[Context] AND [Additional context], BUT [Tension], THEREFORE [Resolution].
```

### Application Tips
- AAA（And, And, And）にならないよう注意—「But」のテンションがないと退屈になる
- DHY（Despite, However, Yet）にならないよう注意—否定が重なると防御的な印象を与える
- 1文で完結させることも、各要素を1段落に展開することも可能
- プレゼンのスライド構成、メールの導入、Slack メッセージにも適用可能

---

## Framework Combination Patterns

複数フレームワークを組み合わせる場合のパターン。

| Combination | Use Case | How |
|-------------|----------|-----|
| SB7 + Pixar | LP + エレベーターピッチ | SB7で構造設計→Pixarで要約版 |
| JTBD + Hero's Journey | 機能提案 + ケーススタディ | JTBDで機能単位→Hero's Journeyで全体像 |
| Story Mapping + JTBD | ロードマップ + 個別ストーリー | Story Mapのbackboneに各JTBDを配置 |
| CAR + SB7 | 事例 + メッセージング | CARで事実→SB7でメッセージ化 |
| Promised Land + SB7 | 戦略ナラティブ + LP/ピッチ | Promised Landで大局→SB7で個別メッセージ |
| ABT + Pixar | ソーシャル + エレベーターピッチ | ABTで要約→Pixarで展開版 |
| Promised Land + CAR | 戦略 + 導入事例 | Promised Landで未来像→CARで証拠 |
