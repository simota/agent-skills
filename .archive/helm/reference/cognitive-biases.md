Purpose: Use this reference to detect and reduce cognitive bias in strategic work. It preserves the top bias patterns, observed rates, and practical debiasing mechanisms Helm should apply.

## Contents
- `CB-01..CB-10`
- Debiasing methods
- Phase risk map
- Helm integration

# Cognitive Biases in Strategic Decision-Making

## Top Biases

| ID | Bias | Observed rate | Strategic impact | Debiasing move |
|---|---|---:|---|---|
| `CB-01` | Confirmation bias | `78.2%` | Evidence is filtered to support the preferred thesis | Use neutral fact-building and counterevidence review |
| `CB-02` | Overconfidence | `71.0%` | Complexity and downside are underestimated | Run a pre-mortem |
| `CB-03` | Anchoring | `59.6%` | First framing dominates decision quality | Evaluate multiple anchors in parallel |
| `CB-04` | Loss aversion | `56.0%` | Necessary exits or pivots are delayed | Make opportunity cost explicit |
| `CB-05` | Action bias | — | Teams act before thinking deeply enough | Force a deliberate evaluation window |
| `CB-06` | Planning fallacy | — | Time, cost, and risk are underestimated | Compare with external reference cases |
| `CB-07` | Groupthink | — | Harmony blocks critique and diversity | Require dissent and structured review |
| `CB-08` | Dunning-Kruger effect | — | Teams overestimate internal capability | Use benchmarking and 360 feedback |
| `CB-09` | Framing effect | — | Choice changes with wording | Reframe the same case multiple ways |
| `CB-10` | Sunflower bias | — | Teams align with leader preference instead of evidence | Anonymous input, leader speaks last |

## Debiasing Toolkit

### Structural Interventions

| Tool | Use | Best for |
|---|---|---|
| Red Team / Devil’s Advocate | Build the strongest argument against the preferred path | confirmation bias, groupthink |
| Pre-mortem | Assume failure first, then work backward | overconfidence, planning fallacy |
| External perspective | Bring in benchmarks or independent review | confirmation bias, anchoring |
| Anonymous voting / Delphi | Collect judgments before social influence kicks in | groupthink, sunflower bias |

### AI- and Data-Assisted Debiasing

| Signal | Use |
|---|---|
| Bias pattern detection | Detect language patterns that imply overconfidence or cherry-picking |
| Scenario diversity scoring | Flag scenario sets that are too homogeneous |
| Accuracy tracking | Feed `FORESIGHT` to see where bias keeps recurring |
| Tool-assisted debiasing | Research suggests up to `16%` improvement in strategic outcomes |

## Phase Risk Map

| Phase | Highest-risk biases | Mandatory check |
|---|---|---|
| Environment analysis | confirmation bias, availability | search for disconfirming evidence |
| Goal setting | overconfidence, planning fallacy | compare against outside benchmarks |
| Strategy design | anchoring, groupthink | run Red Team review |
| Decision-making | loss aversion, framing | restate options from multiple frames |
| Execution planning | planning fallacy, action bias | compare with similar prior cases |
| Monitoring | confirmation bias, sunk-cost logic | predefine kill criteria |

## Helm Integration

1. Apply a bias check in every `SCAN`, `MODEL`, `SIMULATE`, and `ROADMAP` pass.
2. Standardize pre-mortems in `SIMULATE`.
3. Feed detected patterns into `FORESIGHT`.
4. Score scenario diversity before finalizing a strategy package.
5. Include a compact bias risk map in strategic review output when uncertainty is high.

## 2025-2026 Notes

- **Daniel Kahneman (1934-2024)** — *Thinking, Fast and Slow* (2011) author and 2002 Nobel laureate — died **2024-03-27**, age 90 ([Princeton 2024-03-28](https://www.princeton.edu/news/2024/03/28/daniel-kahneman-pioneering-behavioral-psychologist-nobel-laureate-and-giant-field), [NPR 2024-03-27](https://www.npr.org/2024/03/27/1241206604/thinking-fast-slow-psychology-behavioral-economics-daniel-kahneman-obit-nobel)). The System 1 / System 2 framing remains the dominant pop-cognitive model; **Richard Thaler** (Nobel 2017, *Nudge*) and Cass Sunstein continue active publication. There is no single anointed successor — treat the field as plural and beware "argument from authority" framings of Kahneman quotes.
- **AI as bias amplifier and bias-detector — both** — Helm should:
  - Use LLMs to **flag** confirmation-laden phrasing, monolithic scenario sets, and one-sided benefit framing before sign-off.
  - Avoid using LLMs as the **arbiter** of which scenario is "most likely" — RLHF tends to produce overconfident, conventional-wisdom-skewed completions.
  - When facilitating Red Team / Devil's Advocate, instruct the model to defend the minority view *with citations* and reject "balanced both-sides" output as a sunflower-bias artifact.
- **WEIRD critique extension** (2025-): training data for both human-judgment baselines and LLM priors remains heavily Western / English / late-2010s-internet — apply geographic and temporal debiasing when the simulation crosses borders or addresses pre-2020 historical analogs.
