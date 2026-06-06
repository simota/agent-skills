# Handoff Templates

**Purpose:** Saga と他エージェント間のハンドオフテンプレート。
**Read when:** 他エージェントからの入力を受け取る時、または他エージェントへ出力を渡す時。

---

## Inbound Handoffs（Saga への入力）

### CAST_TO_SAGA_HANDOFF

Cast からペルソナ定義を受け取り、ペルソナ別ストーリーを生成する。

```yaml
CAST_TO_SAGA_HANDOFF:
  persona:
    name: "[ペルソナ名]"
    demographics: "[年齢、職業、状況]"
    goals: "[主な目標]"
    frustrations: "[主なフラストレーション]"
    tech_level: "[技術レベル]"
    quotes: "[代表的な発言]"
  request:
    story_type: "[use_case | scenario | onboarding]"
    feature_context: "[対象機能/プロダクト]"
    audience: "[読者ターゲット]"
```

### RESEARCHER_TO_SAGA_HANDOFF

Researcher からリサーチ結果を受け取り、ナラティブに変換する。

```yaml
RESEARCHER_TO_SAGA_HANDOFF:
  research_type: "[interview | usability_test | journey_map | survey]"
  key_findings:
    - "[Finding 1]"
    - "[Finding 2]"
  personas: "[ペルソナ情報（あれば）]"
  journey_map: "[ジャーニーマップ（あれば）]"
  pain_points:
    - "[Pain 1]"
    - "[Pain 2]"
  request:
    story_type: "[customer_success | use_case | scenario]"
    audience: "[読者ターゲット]"
```

### VOICE_TO_SAGA_HANDOFF

Voice から顧客フィードバックインサイトを受け取り、ストーリーに変換する。

```yaml
VOICE_TO_SAGA_HANDOFF:
  feedback_summary:
    positive_themes:
      - "[テーマ1]"
    negative_themes:
      - "[テーマ2]"
    nps_score: "[NPS（あれば）]"
  representative_quotes:
    - "[引用1]"
    - "[引用2]"
  request:
    story_type: "[customer_success | use_case]"
    focus: "[ポジティブ体験 | 課題改善]"
```

### SPARK_TO_SAGA_HANDOFF

Spark から機能提案を受け取り、「なぜ必要か」のナラティブを作成する。

```yaml
SPARK_TO_SAGA_HANDOFF:
  feature:
    name: "[機能名]"
    hypothesis: "[仮説]"
    target_persona: "[ターゲットペルソナ]"
    rice_score: "[RICE Score]"
    acceptance_criteria:
      - "[基準1]"
  request:
    story_type: "[use_case | pitch]"
    audience: "[開発チーム | ステークホルダー | 投資家]"
```

### COMPETE_TO_SAGA_HANDOFF

Compete から競合分析を受け取り、差別化ナラティブを作成する。

```yaml
COMPETE_TO_SAGA_HANDOFF:
  differentiators:
    - "[差別化ポイント1]"
    - "[差別化ポイント2]"
  competitive_landscape: "[市場状況]"
  positioning: "[ポジショニング]"
  request:
    story_type: "[product_narrative | pitch]"
    emphasis: "[差別化 | 市場機会]"
```

---

## Outbound Handoffs（Saga からの出力）

### SAGA_TO_PROSE_HANDOFF

Saga のナラティブから UX コピーの方向性を Prose に渡す。

```yaml
SAGA_TO_PROSE_HANDOFF:
  narrative_summary: "[ナラティブの要約]"
  brand_voice:
    tone: "[トーン: 親しみやすい/プロフェッショナル/etc.]"
    personality: "[パーソナリティ: 頼もしい/共感的/etc.]"
    vocabulary_notes: "[使うべき/避けるべき言葉]"
  key_messages:
    - "[メッセージ1]"
    - "[メッセージ2]"
  transformation_arc:
    before: "[Before の状態]"
    after: "[After の状態]"
  copy_requests:
    - type: "[onboarding | error | cta | tooltip]"
      context: "[使用される画面/状況]"
      tone_note: "[このコピーのトーン指示]"
```

### SAGA_TO_SCRIBE_HANDOFF

Saga のナラティブから PRD のユースケースセクションを Scribe に渡す。

```yaml
SAGA_TO_SCRIBE_HANDOFF:
  use_cases:
    - name: "[ユースケース名]"
      actor: "[アクター]"
      precondition: "[前提条件]"
      main_flow: "[メインフロー要約]"
      narrative_context: "[ストーリーから得た背景]"
      emotional_context: "[ユーザーの感情状態]"
  personas_referenced:
    - "[ペルソナ名]"
  assumptions:
    - "[仮定1]"
```

### SAGA_TO_ACCORD_HANDOFF

Saga のナラティブから L0 ビジョンの顧客体験記述を Accord に渡す。

```yaml
SAGA_TO_ACCORD_HANDOFF:
  vision_narrative: "[プロダクトビジョンのナラティブ]"
  customer_scenarios:
    - persona: "[ペルソナ名]"
      scenario: "[シナリオ要約]"
      desired_outcome: "[期待される成果]"
  transformation:
    before: "[現状]"
    after: "[理想状態]"
  key_value_propositions:
    - "[価値提案1]"
    - "[価値提案2]"
```

### SAGA_TO_DIRECTOR_HANDOFF

Saga のナラティブからデモ動画のシナリオを Director に渡す。

```yaml
SAGA_TO_DIRECTOR_HANDOFF:
  scenario:
    title: "[デモタイトル]"
    duration_target: "[目標尺: 30s / 60s / 120s]"
    persona: "[主人公ペルソナ]"
    narrative_arc:
      setup: "[状況設定]"
      conflict: "[課題の提示]"
      resolution: "[プロダクトによる解決]"
      outcome: "[成果]"
    key_screens:
      - screen: "[画面名]"
        action: "[操作内容]"
        narration: "[ナレーション/テキスト]"
        emotion: "[この時点のユーザー感情]"
  voice_and_tone: "[ナレーションのトーン指示]"
```

### SAGA_TO_PRISM_HANDOFF

Saga のナラティブから NotebookLM ステアリング用コンテンツを Prism に渡す。

```yaml
SAGA_TO_PRISM_HANDOFF:
  narrative_content: "[完成ナラティブ]"
  output_format: "[audio | video | slide]"
  key_messages:
    - "[メッセージ1]"
    - "[メッセージ2]"
  tone_guidance: "[会話調 / プレゼン調 / ドキュメンタリー調]"
  audience: "[ターゲットリスナー/視聴者]"
```
