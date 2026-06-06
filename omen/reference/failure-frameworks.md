# Failure Frameworks

**Purpose:** Core failure analysis methodologies.
**Read when:** Executing IMAGINE or ENUMERATE phases.

---

## 1. Pre-mortem (Gary Klein, 2007)

**Concept:** Assume the project has already failed. Work backward to identify causes.

**Procedure:**
1. Present the plan/design/feature to analyze
2. State: "It is 6 months from now. This has failed spectacularly. Why?"
3. Each participant independently writes failure reasons (2-3 minutes)
4. Collect and categorize all failure reasons
5. Rank by plausibility and severity
6. Develop mitigation for top failures

**Why it works:**
- Overcomes "prospective hindsight" — imagining an event has already occurred increases ability to identify reasons by 30% (Mitchell et al., 1989)
- Legitimizes dissent — team members can voice concerns without appearing negative
- Reduces planning fallacy — forces confrontation with failure possibility

**Categories for failure reasons:**
- Technical: architecture, performance, scalability, integration
- Process: timeline, resources, dependencies, communication
- Human: skills gap, turnover, motivation, knowledge silos
- External: market, regulatory, competitive, vendor
- Data: quality, availability, privacy, migration

---

## 2. FMEA (Failure Mode and Effects Analysis)

**Procedure:**
1. List all components/functions of the system
2. For each, identify potential failure modes
3. For each failure mode, determine:
   - **Effect**: What happens when it fails?
   - **Severity** (S): How bad is the effect? (1-10)
   - **Occurrence** (O): How likely is it to happen? (1-10)
   - **Detection** (D): How likely will we detect it before impact? (1-10, inverted)
4. Calculate RPN = S × O × D
5. Prioritize by RPN, take action on highest

**FMEA Table Format:**

| Component | Failure Mode | Effect | S | O | D | RPN | Mitigation |
|-----------|-------------|--------|---|---|---|-----|------------|
| [name] | [how it fails] | [impact] | [1-10] | [1-10] | [1-10] | [S×O×D] | [action] |

---

## 3. Fault Tree Analysis (FTA)

**Concept:** Top-down deductive analysis. Start with the undesired event (top event) and trace causes through logic gates.

**Logic Gates:**
- **AND gate**: All child events must occur for parent to occur
- **OR gate**: Any child event causes parent to occur

**Procedure:**
1. Define the top event (the failure you want to prevent)
2. Identify immediate causes (connect with AND/OR gates)
3. Recurse: each cause becomes a sub-event, trace its causes
4. Continue until reaching basic events (root causes)
5. Identify minimal cut sets (smallest combination of basic events causing top event)

**Mermaid representation:**
```
graph TD
    TOP[System Failure] --> OR1{OR}
    OR1 --> A[Component A Fails]
    OR1 --> AND1{AND}
    AND1 --> B[Component B Fails]
    AND1 --> C[Backup C Fails]
```

---

## 4. Swiss Cheese Model (James Reason)

**Concept:** Defenses are like slices of Swiss cheese — each has holes. Failures occur when holes align across multiple layers.

**Defense Layers (typical):**
1. **Design** — Architecture, type safety, input validation
2. **Process** — Code review, testing, CI/CD gates
3. **Monitoring** — Alerts, logging, health checks
4. **Recovery** — Rollback, circuit breakers, failover

**Analysis procedure:**
1. Identify all defense layers for the system
2. For each layer, identify "holes" (weaknesses, gaps)
3. Check for alignment — where holes in multiple layers overlap
4. Focus mitigation on closing the most dangerous alignments

---

## 5. Murphy's Law Audit

**Concept:** Systematic check based on "anything that can go wrong will go wrong."

**Checklist:**
- [ ] What happens if the network fails mid-operation?
- [ ] What happens if the database is full?
- [ ] What happens if a dependency returns unexpected data?
- [ ] What happens if two users do the same thing simultaneously?
- [ ] What happens if the deployment is rolled back mid-migration?
- [ ] What happens if the config file is missing or malformed?
- [ ] What happens if the external API changes its contract?
- [ ] What happens if the clock skews between services?
- [ ] What happens if a human makes a typo in a manual step?
- [ ] What happens if load is 10x expected?

Customize per domain. The goal is to challenge every implicit assumption of normal operation.
