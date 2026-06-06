# Segmentation Methods Reference

Purpose: Ground personas in real segments rather than gut-feel descriptions. Cover RFM scoring (transactional), behavioral cohort analysis, psychographic clustering (Schwartz values + OCEAN), demographic vs behavioral selection, and sample-size discipline.

## Scope Boundary

- **cast `segment`**: Persona segmentation methodology (this document).
- **Researcher (elsewhere)**: Qualitative interview design.
- **Trace (elsewhere)**: Session replay → behavioral pattern.
- **Pulse (elsewhere)**: KPI tracking dimensions.
- **Experiment (elsewhere)**: Segment-conditioned A/B tests.

## Three Segmentation Lenses

| Lens | Question | Data source |
|------|----------|-------------|
| **Transactional** | "How do they buy?" | RFM = Recency / Frequency / Monetary |
| **Behavioral** | "How do they use?" | Event logs, session replays, retention curves |
| **Psychographic** | "What do they value / believe?" | Surveys, interviews, OCEAN, Schwartz |

A robust persona uses *at least two* lenses. Demographic-only personas (age, gender, income) underperform — demographics correlate weakly with behavior.

## RFM Scoring (Transactional)

For e-commerce, SaaS, marketplaces with measurable purchases.

```sql
-- Recency: days since last purchase (lower = better)
-- Frequency: purchase count over window (higher = better)
-- Monetary: total spend over window (higher = better)

WITH rfm_raw AS (
  SELECT
    user_id,
    DATEDIFF(CURRENT_DATE, MAX(order_date)) AS recency_days,
    COUNT(DISTINCT order_id)               AS frequency,
    SUM(order_total)                       AS monetary
  FROM orders
  WHERE order_date >= CURRENT_DATE - INTERVAL '12 months'
  GROUP BY user_id
),
scored AS (
  SELECT
    user_id,
    NTILE(5) OVER (ORDER BY recency_days DESC)   AS r_score,  -- inverted
    NTILE(5) OVER (ORDER BY frequency)           AS f_score,
    NTILE(5) OVER (ORDER BY monetary)            AS m_score
  FROM rfm_raw
)
SELECT user_id, r_score, f_score, m_score,
  CONCAT(r_score, f_score, m_score) AS rfm_segment
FROM scored;
```

Common RFM segments:

| RFM range | Segment label | Strategy |
|-----------|---------------|----------|
| 555-455 | Champions | Reward, advocate program |
| 545-355 | Loyal | Upsell, cross-sell |
| 542-512 | New | Onboard, educate |
| 311-111 | At risk | Win-back campaign |
| 1XX | Hibernating | Reactivation or sunset |

Persona maps to one RFM cluster — e.g. "Aoi: Champion (555)".

## Behavioral Cohort Analysis

For SaaS / content / app: how users *behave* over time.

```python
# Cohort by signup month, retention by week
import pandas as pd

events['cohort'] = events.groupby('user_id')['ts'].transform('min').dt.to_period('M')
events['week_offset'] = ((events['ts'] - events.groupby('user_id')['ts'].transform('min')).dt.days // 7)
retention = events.groupby(['cohort', 'week_offset'])['user_id'].nunique().unstack()
retention_pct = retention.div(retention[0], axis=0)
```

Segments emerge from retention curve shape:
- **Power users**: high week-1, sustained > week-12
- **Trial-only**: high week-0, drop by week-2
- **Sleepers**: low week-1, return at week-8+ (re-engagement)
- **Churned**: < 5% by week-4

Or by feature-use vector:

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

features = ['searches_per_week', 'shares_per_week', 'comments_per_week',
            'sessions_per_week', 'avg_session_min']
X = StandardScaler().fit_transform(users[features])
clusters = KMeans(n_clusters=4, random_state=42, n_init=10).fit_predict(X)
users['behavioral_segment'] = clusters
```

Validate cluster count with elbow method or silhouette score (≥0.4 for usable segments).

## Psychographic Clustering

For brand strategy, retention design — measure values + traits.

### Schwartz Theory of Basic Values

10 universal values arranged on a circumplex:

```
              Self-direction
        Universalism       Stimulation
   Benevolence                  Hedonism
                                  Achievement
   Tradition                  Power
        Conformity         Security
              Conformity
```

Survey: PVQ-21 (Portrait Values Questionnaire) — 21 items, 6-point scale. Ipsative scoring (within-person centered).

### OCEAN (Big Five)

| Trait | High | Low |
|-------|------|-----|
| **Openness** | Curious, creative | Practical, conventional |
| **Conscientiousness** | Organized, dependable | Spontaneous, flexible |
| **Extraversion** | Outgoing, energetic | Reserved, solitary |
| **Agreeableness** | Cooperative, trusting | Competitive, skeptical |
| **Neuroticism** | Anxious, sensitive | Calm, resilient |

Survey: BFI-10 (10 items, fast) or BFI-44 (44 items, research-grade). Always validate scale reliability (α ≥ 0.7).

### Clustering

```python
psych_features = ['openness', 'conscientiousness', 'extraversion',
                  'agreeableness', 'neuroticism',
                  'self_direction', 'security', 'achievement']
# Hierarchical for interpretability
from scipy.cluster.hierarchy import linkage, fcluster
Z = linkage(X_scaled, method='ward')
clusters = fcluster(Z, t=5, criterion='maxclust')
```

## Demographic vs Behavioral

| Dimension | Predictive of behavior? | Use for? |
|-----------|------------------------|----------|
| Age | Weak (varies by domain) | Segment context only |
| Gender | Weak | Inclusive design context |
| Income | Moderate (spending power) | Plan tier targeting |
| Geography | Domain-specific | Localization, latency |
| Job role | Moderate (B2B) | B2B persona context |
| RFM cluster | Strong | Lifecycle marketing |
| Behavioral cluster | Strong | Feature priority |
| Psychographic | Strong (long-term) | Brand, retention |

Demographics describe; behavior + psychographics predict.

## Sample Size Discipline

Per persona segment:
- ≥ 30 observations for descriptive stats
- ≥ 50-100 for K-means stability
- Power calc for any A/B claims (n per arm via standard formulas)

Don't define a persona on n < 10. Either pool segments or label as "exploratory".

## Workflow

```
DATA INVENTORY  →  what behavioral / transactional / psychographic
                   data exists per user
                →  flag missing-data dimensions

LENS SELECT     →  pick ≥2 lenses (transactional + behavioral default)
                →  psychographic if survey budget exists

RFM             →  if transactional data: NTILE 5×5×5 → segment label
                →  named clusters (Champion, At-risk, ...)

BEHAVIORAL      →  retention curve OR feature-use vector
                →  K-means / hierarchical with k validated by silhouette
                →  name clusters by behavior, not demographics

PSYCHOGRAPHIC   →  PVQ-21 / BFI-10 surveys (n≥100)
                →  hierarchical cluster for interpretability
                →  optional, but raises persona quality

OVERLAY         →  demographic crosswalk (age/role) for storytelling
                →  validate that demographics don't dominate

SAMPLE CHECK    →  n≥30 per segment for descriptive
                →  n≥50-100 for K-means
                →  reject thin segments

PERSONA PIN     →  one persona per segment cluster
                →  RFM tier + behavioral segment + (optional) psych profile
                →  cite provenance per attribute

HANDOFF         →  Researcher: validate via interviews
                →  Echo: walkthrough with segment-consistent reactions
                →  Spark: feature priority by behavioral segment
                →  Retain: lifecycle by RFM
                →  Pulse: track segment KPIs
```

## Output Template

```markdown
## Segmentation: [Persona Set]

### Data Inventory
- Transactional: [yes/no] — [N orders / window]
- Behavioral events: [yes/no] — [event vol / window]
- Psychographic survey: [PVQ-21 / BFI-10 / none]
- Demographic: [yes/no] — fields
- Missing: [list]

### RFM Segments
| Segment | n | R | F | M | Persona |
|---------|---|---|---|---|---------|
| Champions (555-455) | 1240 | 1.2d | 12 | $580 | P-001 Aoi |
| Loyal (545-355)     | 3100 | 12d  | 6  | $210 | P-002 Ren |
| New (542-512)       | 850  | 8d   | 1  | $52  | P-003 Hana |
| At risk (311-111)   | 760  | 90d  | 2  | $130 | P-004 Yuto |

### Behavioral Clusters
| Cluster | n | Sessions/wk | Features used | Persona |
|---------|---|-------------|---------------|---------|
| Power | 540 | 12 | search, share, comment | P-001 |
| Casual | 1800 | 2 | search | P-002 |
| ... | ... | ... | ... | ... |

Cluster validity: silhouette = 0.52, elbow at k=4

### Psychographic Profiles (optional)
| Cluster | Top values | Top OCEAN | Persona |
|---------|------------|-----------|---------|
| Achievers | Achievement, Power | High C, low N | P-001 |
| Explorers | Stimulation, Self-direction | High O, high E | P-002 |
| ... | ... | ... | ... |

Survey n=320, BFI-10 α=0.78, PVQ-21 α=0.74

### Per-Persona Segment Tag
```yaml
P-001:
  rfm: 555 (Champion)
  behavioral: Power user
  psychographic: Achiever
  demographics: 32yo, PM, Tokyo (context only)
  evidence: 1240 users in segment
```

### Validation
- Sample size: all segments ≥ 50 ✓
- Silhouette score: ≥ 0.4 ✓
- Survey reliability: α ≥ 0.7 ✓
- Cross-lens coherence: [check that RFM × Behavioral × Psych aren't independent]

### Handoffs
- Researcher: validate top-3 segments via interviews (n=5 each)
- Echo: walkthrough scripts per segment
- Spark: feature priorities by behavioral cluster
- Retain: lifecycle messaging by RFM tier
- Pulse: segment-conditioned KPI dashboards
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Demographics-only persona ("32yo PM, Tokyo") | Add behavioral + transactional lens |
| Cluster count chosen without elbow / silhouette | Validate; pick lowest k that hits silhouette ≥ 0.4 |
| Persona on n < 30 | Either pool or label "exploratory" — don't claim representativeness |
| RFM on a small recent window | ≥ 12-month window unless seasonal product |
| Behavioral cluster labeled by demographics ("young men") | Label by behavior ("power users", "lapsed") |
| Survey scale α < 0.7 | Drop the dimension or use a validated scale |
| Persona attributes not cited to source | Per-attribute provenance: which lens, what data |
| Mixing inferred and self-reported without flag | Flag clearly; bias differs |
| K-means on raw counts | Always StandardScaler / log-transform skewed features |
| Single-lens persona declared "data-driven" | Single-lens = thin; require ≥2 |
| Demographics as primary predictor | Demographics describe; behavior predicts |
| Stable persona not re-checked over time | Drift check at 6mo (cast `evolve`) |
| Equating cluster size to importance | Champion (small) > At-risk (small) > ... by LTV, not headcount |
| Importing US-defined Schwartz scoring on JP / non-Western | Use locally validated translations + ipsative centering |

## Deliverable Contract

When `segment` completes, emit:

- **Data inventory** with available lenses.
- **RFM segments** (if transactional data).
- **Behavioral clusters** with silhouette + elbow validation.
- **Psychographic profiles** (if survey).
- **Per-persona segment tag** with multi-lens fields.
- **Sample size + reliability** validation.
- **Handoffs**: Researcher, Echo, Spark, Retain, Pulse.

## Framework Notes (as of 2026-05)

- **VALS** (Values and Lifestyle Survey, SRI International → Strategic Business Insights): the canonical psychographic segmentation framework. Last major structural revision in 1989 (VALS2). No further structural overhaul has been released; treat VALS as a *historical psychographic baseline* and complement with behavior + JTBD data, especially for digital / online behaviors.
- **JTBD Pyramid™** (AIM Institute, 2025): a recent JTBD extension addressing five common practitioner challenges with the classic Christensen / Ulwick / Moesta frameworks. Useful when the classic functional/emotional/social split underspecifies the job hierarchy.
- **Outcome-Driven Innovation (ODI)** by Tony Ulwick remains the most actionable JTBD variant for quantitative segmentation; Bob Moesta's Demand-Side Sales + "Switch" interview pattern remains the canonical qualitative approach.
- **CliftonStrengths** (Gallup): 34-theme assessment across four domains (Executing / Influencing / Relationship Building / Strategic Thinking); structure is stable through 2026. Useful for *internal* persona work but should not replace OCEAN or Schwartz for external user personas.

## References

- Sherrington, "Customer Segmentation: RFM Analysis" — Direct Marketing
- Christensen, *Competing Against Luck* (2016) — JTBD complement to behavioral
- Wedel + Kamakura, *Market Segmentation* (3rd ed.)
- Schwartz, "An Overview of the Schwartz Theory of Basic Values" (2012)
- Costa + McCrae, *NEO-PI-R* / Big Five history
- Rammstedt + John — BFI-10 (10-item Big Five short form)
- Aldenderfer + Blashfield — *Cluster Analysis* (Sage)
- scikit-learn KMeans / DBSCAN / AgglomerativeClustering docs
- "Behavioral Segmentation" — Amplitude / Heap / Mixpanel guides
- Customer Lifetime Value (CLV) — Fader, Hardie + Lee
- Cooper + Reimann — *About Face* (persona origins, behavioral framing)
- *Lean Analytics* — Croll + Yoskovitz (per-segment metric design)
- Statistical power for clustering — Tibshirani et al., gap statistic
- VALS framework — Strategic Business Insights / SRI International (`sri.com/hoi/vals-market-research/`)
- JTBD Pyramid™ — AIM Institute (2025, `theaiminstitute.com/blog/introducing-the-jobs-to-be-done-pyramid/`)
- Bob Moesta — *Demand-Side Sales 101* + Switch interview methodology
- Tony Ulwick — Outcome-Driven Innovation / Universal Job Map
- CliftonStrengths Technical Report — Gallup
