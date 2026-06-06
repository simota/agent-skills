# Echo Collaboration Patterns Reference

Detailed collaboration patterns and handoff formats for Echo agent.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT PROVIDERS                          │
│  Field → ペルソナデータ                                │
│  Voice → 実ユーザーフィードバック                           │
│  Pulse → 定量メトリクス                                     │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
            ┌─────────────────┐
            │      ECHO       │
            │  UX検証エンジン │
            └────────┬────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                   OUTPUT CONSUMERS                          │
│  Palette → インタラクション改善                             │
...
```

## Pattern A: Validation Loop (Echo ↔ Palette)

```
Echo（friction発見: -2.5/5）
  ↓ handoff
Palette（改善案: loading state追加）
  ↓ handoff back
Echo（改善後検証: +3.8/5）
  ↓ 検証完了
```

**Handoff Format (Echo → Palette):**
```markdown
## Echo → Palette Handoff

**Friction Point**: [具体的な問題箇所]
**Persona**: [検証ペルソナ]
**Emotion Score**: [Before score]
**Root Cause**: [認知的原因 - mental model gap type]
**User Quote**: [ペルソナの発言]
**Suggested Focus**: [改善の方向性]

→ `/Palette improve interaction`
```

**Handoff Format (Palette → Echo):**
```markdown
## Palette → Echo Validation Request

**Improvement Made**: [実施した改善]
**Target Metric**: [改善したい指標]
**Validation Persona**: [検証すべきペルソナ]
**Expected Outcome**: [期待する結果]

→ `/Echo validate with [persona]`
```

## Pattern B: Hypothesis Generation Loop (Echo → Experiment → Pulse)

```
Echo（フリクション発見 + JTBD分析）
  ↓
Experiment（A/Bテスト仮説設計）
  ↓
Pulse（成功メトリクス定義）
  ↓
実験実行
  ↓
Echo（勝者バリアントをペルソナ検証）
```

**Handoff Format (Echo → Experiment):**
```markdown
## Echo → Experiment Handoff

**Finding**: [発見した問題]
**Location**: [フロー内の位置]
**Affected Personas**: [影響を受けるペルソナ]
**JTBD Insight**: [潜在ニーズ]
**Current Emotion Score**: [現在スコア]

**Hypothesis**: If [変更] then [結果] because [理由]
**Suggested Variants**:
- Control: [現状]
- Variant A: [提案1]
- Variant B: [提案2（オプション）]

**Metrics to Track**:
...
```

## Pattern C: Prediction Validation Loop (Echo ↔ Voice)

```
Echo（フリクション予測）
  ↓
Voice（実ユーザーフィードバック収集）
  ↓
比較・精度測定
  ↓
Echo（シミュレーション精度向上）
```

**Validation Report Format:**
```markdown
## Echo-Voice Prediction Validation

**Flow**: [検証フロー名]
**Period**: [Voice収集期間]

| Echo Prediction | Voice Finding | Match |
|-----------------|---------------|-------|
| [予測1] | [実際のフィードバック] | ✅/❌ |
| [予測2] | [実際のフィードバック] | ✅/❌ |

**Prediction Accuracy**: [%]
**False Positives**: [Echoが予測したが発生しなかった]
**False Negatives**: [Echoが見逃した実際の問題]

**Calibration Actions**:
...
```

## Pattern D: Visualization (Echo → Canvas)

```
Echo（ジャーニーデータ + emotion scores）
  ↓
Canvas（Journey Map / Friction Heatmap生成）
  ↓
ステークホルダー共有
```

**Handoff Format (Echo → Canvas):**
```markdown
## Echo → Canvas Visualization Request

**Visualization Type**: Journey Map | Friction Heatmap | Before/After Comparison
**Flow**: [フロー名]
**Persona**: [ペルソナ名]
**Data**:
| Step | Action | Score | Friction Type |
|------|--------|-------|---------------|
| 1 | [action] | +2 | None |
| 2 | [action] | -1 | Mental Model Gap |
| 3 | [action] | -3 | Cognitive Overload |

**Highlight Points**:
- Peak: Step [N]
- End: Step [N]
...
```

## Pattern E: Root Cause Analysis (Echo → Scout)

UIバグとUXフリクションの切り分け：

```
Echo（「ボタンが反応しない」→ UIバグの可能性）
  ↓
Scout（技術的根本原因分析）
  ↓
Builder or Palette（修正実装）
  ↓
Echo（修正後検証）
```

**Handoff Format (Echo → Scout):**
```markdown
## Echo → Scout Investigation Request

**Symptom**: [ユーザー視点の症状]
**Location**: [発生箇所]
**Persona Quote**: [ペルソナの発言]
**Suspected Type**: UI Bug | UX Design Issue | Both
**Reproduction Steps**: [再現手順（あれば）]

→ `/Scout investigate`
```

## Pattern F: Feature Proposal (Echo → Spark)

潜在ニーズを新機能アイデアに変換：

```
Echo（JTBD分析で潜在ニーズ発見）
  ↓
Spark（機能提案仕様書作成）
  ↓
Echo（提案をペルソナ視点で検証）
```

**Handoff Format (Echo → Spark):**
```markdown
## Echo → Spark Feature Opportunity

**Latent Need Discovered**:
- Functional Job: [達成したいこと]
- Emotional Job: [感じたいこと]
- Social Job: [見られたいこと]

**Evidence**:
- Persona: [ペルソナ]
- Behavior Observed: [観察された行動]
- Friction Score: [スコア]
- User Quote: [発言]

**Opportunity Size**: [影響を受けるペルソナ数/頻度]

...
```

## Pattern G: Persona Generation (Echo ↔ Field)

コード/ドキュメントからペルソナを生成し、Field の実データで検証:

```
Echo（コード/ドキュメント分析 → ペルソナ生成）
  ↓
Field（実ユーザーデータで検証）
  ↓
Echo（ペルソナ精度向上・更新）
```

**Handoff Format (Echo → Field):**
```markdown
## Echo → Field Persona Validation Request

**Generated Persona**: [ペルソナ名]
**Source**: [分析したファイル]
**Key Assumptions**:
- [仮定1: 例「モバイル利用が70%」]
- [仮定2: 例「初回購入者が主要ターゲット」]

**Validation Needed**:
- [ ] ユーザータイプの割合
- [ ] 実際の利用デバイス比率
- [ ] ペインポイントの優先度

→ `/Field validate persona assumptions`
```

**Handoff Format (Field → Echo):**
```markdown
## Field → Echo Persona Update

**Persona**: [ペルソナ名]
**Validation Result**:
| 仮定 | 実データ | ギャップ |
|------|---------|---------|
| モバイル70% | モバイル82% | +12% |
| 初回購入者中心 | リピーター40% | 要ペルソナ追加 |

**Recommended Updates**:
- [Profile 更新内容]
- [Emotion Triggers 更新内容]

→ Echo updates `.agents/personas/{service}/{persona}.md`
```

## Bidirectional Collaboration Matrix

| Partner | Echo → Partner | Partner → Echo |
|---------|----------------|----------------|
| **Field** | ペルソナ検証結果、生成ペルソナの検証依頼 | 実データに基づくペルソナ定義、ペルソナ更新提案 |
| **Voice** | 予測との比較データ | 実ユーザー感情フィードバック |
| **Palette** | フリクションポイント | 改善後の検証依頼 |
| **Experiment** | A/Bテスト仮説 | 勝者バリアント検証依頼 |
| **Growth** | CRO対象フローの検証 | コンバージョン改善策の検証依頼 |
| **Canvas** | ジャーニーデータ | 可視化済みフロー図 |
| **Scout** | UIバグ疑いの調査依頼 | 根本原因に基づく再検証依頼 |
| **Spark** | 潜在ニーズ/JTBD | 新機能案の検証依頼 |
| **Muse** | デザイン一貫性問題 | トークン適用後の検証依頼 |
| **Pulse** | 感情スコアのメトリクス化 | 定量データに基づく検証対象 |

## With Lens (Journey Evidence)

**When to involve Lens:**
- At each step of UX walkthrough
- When friction points are discovered (score -2 or below)
- For before/after UX improvement comparisons
- To document accessibility issues

**Walkthrough Flow with Lens:**
```
1. Echo selects persona
2. Echo → Lens: "Start journey capture"
3. Echo performs each step of the flow
4. Echo → Lens: "Capture step N with emotion score X"
5. Lens captures screenshot with score metadata
6. Echo completes walkthrough
7. Echo → Lens: "Generate journey evidence report"
8. Lens outputs journey map data for Canvas
```

**Handoff to Lens:**
```markdown
## Echo → Lens Journey Capture

- Persona: [persona name]
- Flow: [flow being tested]
- Step: [step number]
- Action: [user action]
- Emotion Score: [score -3 to +3]
- Highlight: [elements to focus on]
- Note: [observation about this step]
```

## Pattern H: Visual Review (Vector → Echo → Canvas)

Flow where Echo reviews Vector screenshots from persona perspective and Canvas visualizes the results.

```
Vector (Screenshot capture)
  ↓ NAVIGATOR_TO_ECHO_HANDOFF
Echo (Visual Persona Review)
  - First Glance analysis
  - Scan Pattern simulation
  - Visual Emotion Scoring
  - Friction Point detection
  ↓ ECHO_TO_CANVAS_VISUAL_HANDOFF
Canvas (Visual Journey Map generation)
  ↓
Stakeholder sharing
```

### Trigger

```
/Echo visual review                    # Start visual review from Vector handoff
/Echo visual review [screenshot_path]  # Review specific screenshot
/Echo visual review with [persona]     # Review with specific persona
```

### Workflow Steps

1. **Vector Screenshot Capture**
   - Capture screenshots at key screen states
   - Record device context (viewport, browser, connection)
   - Document flow information (URL, journey, actions)

2. **Echo Visual Review**
   - RECEIVE: Receive handoff data
   - ORIENT: Understand device context
   - PERCEIVE: First Glance analysis (0-3 sec)
   - REACT: Persona emotional reactions
   - INTERACT: Interaction evaluation
   - SCORE: Visual Emotion Scoring

3. **Canvas Visualization**
   - Visual Journey Map with screenshot references
   - Friction Heatmap on screenshots
   - Before/After comparison (if applicable)

### Handoff Format (Vector → Echo)

```markdown
## NAVIGATOR_TO_ECHO_HANDOFF

**Task ID**: [ID]
**Review Purpose**: [Visual UX Review / Accessibility Audit / Competitor Comparison]

**Screenshots Captured**:
| # | Path | Page State | Context |
|---|------|------------|---------|
| 1 | `.vector/screenshots/[id]/01_landing.png` | Initial load | Homepage after navigation |
| 2 | `.vector/screenshots/[id]/02_form.png` | Form visible | After clicking signup |

**Device Context**:
| Attribute | Value |
|-----------|-------|
| Viewport | 390x844 (iPhone 14 Pro) |
...
```

### Handoff Format (Echo → Canvas)

```markdown
## ECHO_TO_CANVAS_VISUAL_HANDOFF

**Task ID**: [ID]
**Visualization Type**: Visual Journey Map | Friction Heatmap | Before/After

**Flow**: [Flow Name]
**Persona**: [Persona Name]
**Device**: [Device Context]

**Visual Journey Data**:
| Screenshot | State | Score | Friction Type | Note |
|------------|-------|-------|---------------|------|
| 01_landing.png | Initial | +1 | None | Hero clear |
| 02_form.png | Form | −2 | Touch Target | CTA too small |

...
```

### Use Cases

| Scenario | Vector Action | Echo Focus | Canvas Output |
|----------|------------------|------------|---------------|
| **Mobile UX Audit** | Mobile viewport screenshots | Touch targets, thumb zones | Friction Heatmap |
| **Signup Flow Review** | Step-by-step captures | Trust signals, form friction | Visual Journey Map |
| **Error State Analysis** | Error scenarios | Error message clarity | Before/After Template |
| **Competitor Comparison** | Both site screenshots | Feature parity, patterns | Side-by-side Comparison |
| **Accessibility Audit** | High contrast / zoom modes | Readability, contrast | Accessibility Report |

### Detailed Reference

See `reference/visual-review.md` for detailed Visual Review procedures and scoring criteria.
