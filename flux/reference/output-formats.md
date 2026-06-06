# Output Formats

**Purpose:** Templates for all Flux deliverables.
**Read when:** You are in the CRYSTALLIZE phase and need to structure the final output.

---

## Contents
- Assumption Map
- Reframed Problem Statements
- Insight Matrix
- Blind Spot Report
- Action Hypothesis
- Full DEEP Mode Deliverable Template

---

## Assumption Map

Surface all assumptions, their confidence levels, reversals, and insights.

```markdown
## Assumption Map

| # | 前提 | 確信度 | 反転 | 洞察 |
|---|------|--------|------|------|
| 1 | [Current assumption] | H/M/L | [What if the opposite?] | [What does the reversal reveal?] |
| 2 | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |

**特に重要な前提** (High confidence + surprising reversal):
- #[N]: [Explanation of why this assumption matters most]

**暗黙の前提** (Assumptions so embedded they're invisible):
- [Assumption that "everyone knows" but nobody states]
```

### Confidence Levels

| Level | Meaning | Reversal Value |
|-------|---------|----------------|
| **H** (High) | Widely accepted, evidence-backed | Low (usually) — but high-confidence reversals are most disruptive |
| **M** (Medium) | Commonly assumed, limited evidence | Medium — good territory for exploration |
| **L** (Low) | Uncertain, contested | High — already questioning, reversal may confirm or surprise |

---

## Reframed Problem Statements

The core deliverable: 3-5 genuinely different ways to see the problem.

```markdown
## 再構成された問題文

### 元の問題文
> [Original problem as stated by user]

### Cynefin 分類: [Clear | Complicated | Complex | Chaotic]

---

### リフレーム 1: [Short label]
**視点**: [What frame/lens produced this]
**問題文**: [Reframed problem statement in 1-3 sentences]
**根拠**: [Why this reframing is valid — which assumptions were challenged/reversed]
**示唆するアクション**: [What actions this framing suggests]
**ソースフレームワーク**: [Which framework(s) generated this]

---

### リフレーム 2: [Short label]
...

### リフレーム 3: [Short label]
...

### リフレーム 4: [Short label] (DEEP mode)
...

### リフレーム 5: [Short label] (DEEP mode, if applicable)
...

---

### リフレーム比較

| # | ラベル | 新規性 | 実行可能性 | リスク | 推奨度 |
|---|--------|--------|-----------|--------|--------|
| 1 | [label] | H/M/L | H/M/L | H/M/L | ★★★☆☆ |
| 2 | [label] | H/M/L | H/M/L | H/M/L | ★★★★☆ |
| ... | ... | ... | ... | ... | ... |
```

### Quality Criteria for Reframed Statements

Each reframing must:
- [ ] Be genuinely different from the original (not just rephrasing).
- [ ] Be different from every other reframing (no duplicates in disguise).
- [ ] Suggest at least one action the original framing would not.
- [ ] Be grounded in a traceable framework application (not arbitrary).
- [ ] Be expressed clearly enough for someone unfamiliar with Flux to understand.

---

## Insight Matrix

Catalog all insights generated during the pipeline, with metadata.

```markdown
## Insight Matrix

| # | 洞察 | ソースフレームワーク | フェーズ | 新規性 | 実行可能性 | 関連リフレーム |
|---|------|---------------------|---------|--------|-----------|-------------|
| 1 | [Insight description] | [Framework name] | [CHALLENGE/COMBINE/SHIFT] | H/M/L | H/M/L | #[N] |
| 2 | ... | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... | ... |

**Top 3 洞察**:
1. **[Most impactful insight]** — [Why it matters]
2. **[Second insight]** — [Why it matters]
3. **[Third insight]** — [Why it matters]

**Serendipity 由来の洞察**:
- [Insights that came from random stimuli, marked with source]
```

### Novelty Scale

| Level | Definition |
|-------|-----------|
| **H** | Completely new perspective; would not emerge from conventional analysis |
| **M** | Known concept applied in a new context or combination |
| **L** | Confirms or slightly extends existing understanding |

### Actionability Scale

| Level | Definition |
|-------|-----------|
| **H** | Can be acted on immediately with clear next steps |
| **M** | Requires further investigation but direction is clear |
| **L** | Theoretical insight; value is in reframing, not direct action |

---

## Blind Spot Report

Document cognitive biases and hidden constraints detected during the process.

```markdown
## Blind Spot Report

### 検出されたバイアス

| バイアス | 兆候 | 影響 | 対策 |
|---------|------|------|------|
| [Bias name] | [How it was detected] | [What it hid or distorted] | [Reframing that counters it] |
| ... | ... | ... | ... |

### 隠れた制約

| 制約 | 種類 | 発見方法 | 解除可能性 |
|------|------|---------|-----------|
| [Hidden constraint] | 技術的/組織的/文化的/心理的 | [Which framework surfaced it] | H/M/L |
| ... | ... | ... | ... |

### 検討されなかった視点

- [Perspective that was absent from the analysis]
- [Stakeholder whose view was not represented]
- [Time horizon that was not considered]
```

### Common Biases Flux Detects

| Bias | Detection Signal | Counter Framework |
|------|-----------------|-------------------|
| Anchoring | First option dominates all discussion | Assumption Reversal |
| Sunk Cost | "We've already invested X" | First Principles |
| Availability | Recent events overweighted | Cross-Domain Analogy |
| Confirmation | Only supporting evidence cited | Devil's Advocate |
| Status Quo | "It's always been this way" | Oblique Strategies |
| Groupthink | No dissent in discussion | Multi-Agent Debate |
| Framing Effect | Problem definition constrains solutions | Reframing (E5) |
| Survivorship | Only looking at successes | Reframing (Iceberg) |

---

## Action Hypothesis

For each promising reframing, suggest a testable hypothesis.

```markdown
## Action Hypotheses

### 仮説 [N]: [Label]
- **元のリフレーム**: #[N]
- **仮説**: もし[action]すれば、[expected outcome]になるだろう。なぜなら[reasoning from reframing]。
- **検証方法**: [How to test this cheaply and quickly]
- **成功指標**: [What would confirm or refute the hypothesis]
- **リスク**: [What could go wrong]
- **推奨エージェント**: [Which agent should take the next step]
```

---

## Full DEEP Mode Deliverable Template

Complete output structure for DEEP mode execution:

```markdown
# Flux 思考屈折レポート

## メタ情報
- **元の問題**: [Original problem]
- **Cynefin 分類**: [Domain]
- **ワークモード**: DEEP
- **適用フレームワーク**: [List]
- **Serendipity 注入**: [Count] 回

---

## 1. Assumption Map
[Full Assumption Map]

## 2. 再構成された問題文
[3-5 Reframed Problem Statements with comparison table]

## 3. Insight Matrix
[Full Insight Matrix with Top 3]

## 4. Blind Spot Report
[Biases + Hidden Constraints + Missing Perspectives]

## 5. Action Hypotheses
[Testable hypotheses for top reframings]

## 6. 推奨ネクストステップ
- **意思決定が必要**: → Magi ([specific question])
- **機能提案に発展**: → Spark ([specific idea])
- **戦略シミュレーション**: → Helm ([specific scenario])
- **アーキテクチャ検討**: → Atlas ([specific reconception])
- **パターン蓄積**: → Lore ([reusable thinking pattern])
```
