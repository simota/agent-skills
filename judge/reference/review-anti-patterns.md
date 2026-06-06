# Code Review Anti-Patterns

> Review process anti-patterns, behavioral anti-patterns, and countermeasures.

## 1. Process Anti-Patterns (AWS Well-Architected)

| # | Pattern | Symptoms | Impact | Countermeasure |
|---|---------|----------|--------|----------------|
| 1 | **Infrequent Reviews** | Reviews skipped or rarely performed | Missed error detection, isolated development | Make reviews a mandatory pre-merge step |
| 2 | **Excessive Reviewers** | Too many reviewers assigned | Bottleneck, unnecessary delays | Set practical reviewer count based on code complexity |
| 3 | **No Automated Feedback** | No automated tooling used | Extended review time, focus on trivial issues | Run SAST/Linters beforehand; humans focus on higher-order issues |
| 4 | **Large Batch Reviews** | Multiple changes reviewed at once | Difficult to isolate issues, long review cycles | Submit small, focused PRs |
| 5 | **Unconstructive Reviews** | Harsh tone, vague feedback | Lowered developer morale, blocked dialogue | Train on specific, constructive feedback |
| 6 | **No Action on Findings** | Findings left unaddressed | Same issues recur, reviews become perfunctory | Introduce feedback tracking systems |

---

## 2. Behavioral Anti-Patterns

### 8 Major Behavioral Patterns

| Pattern | Description | Judge's Countermeasure |
|---------|-------------|----------------------|
| **Rubber Stamping** | Approving without reading content | Automated review ensures minimum quality baseline |
| **Nit-Picking** | Fixating on style/formatting trivia | Delegate style to Linter/Zen; focus on logic |
| **Long-Running PRs** | PRs stalled in review queue for extended periods | Measure and alert on review turnaround time |
| **Self-Merging** | Approving and merging one's own code | Require at least one other reviewer |
| **Heroing** | One person handles all reviews | Distribute review load via rotation |
| **Over-Helping** | Reviewer rewrites the code | Limit to suggestions; let the author make fixes |
| **"Just One More Thing"** | Repeated additional requests just before approval | Clarify scope; defer additions to follow-up issues |
| **Knowledge Silos** | Only specific individuals review specific areas | Promote cross-reviews and documentation |

---

## 3. Cognitive Biases and Review Quality

### Biases That Affect Reviews

| Bias | Impact | Countermeasure |
|------|--------|----------------|
| **Confirmation Bias** | Only detects issues matching existing beliefs | Checklist-based reviews |
| **Decision Fatigue** | Quality degrades in later portions of review | Keep sessions under 60 minutes; take breaks |
| **Anchoring** | First issue found biases subsequent evaluation | Structured review order (Security → Logic → Performance) |
| **Bandwagon Effect** | Conforming to other reviewers' opinions | Independent review first, then discussion |
| **Halo Effect** | Review depth varies based on author's reputation | Evaluate code only; disregard author identity |

### Judge's Cognitive Bias Countermeasures

```
Judge's automated review is unaffected by cognitive biases:
  ✅ Reviews all files at consistent depth
  ✅ Processes large volumes of code without fatigue
  ✅ Checklist-based approach prevents omissions
  ✅ Applies the same standards regardless of author

However, AI review has limitations:
  ❌ Incomplete understanding of business context
  ❌ Architecture decisions require human judgment
  ❌ Difficult to make judgments based on tacit knowledge
```

---

## 4. Review Scope Anti-Patterns

### "Everything Everywhere All at Once" Pattern

```
❌ Checking all aspects in a single review:
   Correctness + Security + Performance + Style + Tests + Documentation

✅ Separate concerns across reviews (Specialist-Agent pattern):
   Pass 1: Correctness & Logic (Judge)
   Pass 2: Security (Sentinel)
   Pass 3: Performance (Bolt)
   Pass 4: Test Quality (Radar)
```

### Inconsistent Feedback

```
❌ Rejecting patterns that were approved last time
❌ Different standards across reviewers
❌ Unwritten implicit rules

✅ Codify review guidelines
✅ Living Rules (continuously updated team standards)
✅ AI review ensures standard consistency
```

---

## 5. Judge's Anti-Pattern Avoidance

| Anti-Pattern | Judge's Countermeasure |
|-------------|----------------------|
| Style nit-picks | severity=INFO, delegate to Zen |
| Findings buried in noise | Display CRITICAL/HIGH at top |
| No follow-up | Explicitly name remediation agent |
| Insufficient context | Intent-check via PR description + commit message |
| Excessive false positives | Apply filtering from codex-integration.md |

**Source:** [AWS: Anti-patterns for Code Review](https://docs.aws.amazon.com/wellarchitected/latest/devops-guidance/anti-patterns-for-code-review.html) · [CodeRabbit: 5 Code Review Anti-Patterns](https://www.coderabbit.ai/blog/5-code-review-anti-patterns-you-can-eliminate-with-ai) · [IEEE: Anti-patterns in Modern Code Review](https://ieeexplore.ieee.org/document/9425884/) · [Arxiv: Towards Debiasing Code Review](https://arxiv.org/abs/2407.01407)
