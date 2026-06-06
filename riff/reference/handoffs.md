# Handoff Templates

**Purpose:** Riff と他エージェント間のハンドオフ形式。
**Read when:** セッション成果を他エージェントに引き渡すとき。

---

## Riff → Magi (Decision Handoff)

セッションで浮かび上がった選択肢群を Magi に意思決定依頼する。

```yaml
RIFF_TO_MAGI_HANDOFF:
  context: [ブレストのテーマと背景]
  candidates:
    - name: [選択肢1]
      description: [概要]
      pros: [セッション中に出たメリット]
      cons: [セッション中に出た懸念]
    - name: [選択肢2]
      description: [概要]
      pros: [メリット]
      cons: [懸念]
  evaluation_axes:
    - [セッション中に重要と判断された評価軸1]
    - [評価軸2]
  session_insights:
    - [意思決定に影響する気づき]
  decision_needed: [何を決めてほしいか]
```

---

## Riff → Spark (Feature Seed Handoff)

有望なアイデアの種を Spark に渡して機能提案書に発展させる。

```yaml
RIFF_TO_SPARK_HANDOFF:
  idea_seed:
    title: [アイデアタイトル]
    one_liner: [1行要約]
    origin: [どの問いから生まれたか]
  user_context:
    pain_point: [解決したい課題]
    target_user: [想定ユーザー]
  exploration_notes:
    - [セッション中の探索メモ1]
    - [探索メモ2]
  constraints:
    - [ユーザーが挙げた制約]
  open_questions:
    - [まだ答えが出ていない問い]
```

---

## Riff → Accord (Requirement Seed Handoff)

コンセプトを要件定義の種として Accord に渡す。

```yaml
RIFF_TO_ACCORD_HANDOFF:
  concept:
    title: [コンセプトタイトル]
    summary: [概要 2-3 文]
  stakeholder_perspectives:
    - perspective: [視点1（例: エンドユーザー）]
      needs: [ニーズ]
    - perspective: [視点2（例: 運用チーム）]
      needs: [ニーズ]
  scope_direction:
    must_have: [絶対に必要な要素]
    nice_to_have: [あると良い要素]
    explicitly_excluded: [セッションで除外と判断された要素]
  risks:
    - [リスク]
```

---

## Riff → Void (Pruning Handoff)

広げたアイデアの中から、Void に YAGNI 検証を依頼する。

```yaml
RIFF_TO_VOID_HANDOFF:
  target: [検証対象]
  current_scope:
    - [要素1]
    - [要素2]
    - [要素3]
  suspicion: [過剰と思われる部分]
  session_context: [なぜ過剰と感じたかの対話コンテキスト]
```

---

## Flux → Riff (Reframed Problem Handoff)

Flux のリフレーミング結果を受け取って対話的探索を開始する。

```yaml
FLUX_TO_RIFF_HANDOFF:
  original_problem: [元の問題]
  reframed_as: [リフレーミングされた問題]
  key_assumption_reversed: [反転された前提]
  exploration_request: [Riff に探索してほしい方向性]
```

---

## Field → Riff (Research-to-Brainstorm Handoff)

調査結果を受け取って、そこからアイデアを展開する。

```yaml
RESEARCHER_TO_RIFF_HANDOFF:
  research_topic: [調査テーマ]
  key_findings:
    - [発見1]
    - [発見2]
  implications: [示唆されること]
  brainstorm_request: [Riff に探索してほしい観点]
```
