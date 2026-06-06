# Devil's Advocate Reference

Purpose: Formal opposition protocol that assigns a rotating role to argue against the prevailing view, stress-testing high-stakes proposals before commitment. Originating in the Catholic canonization process (advocatus diaboli, 1587-1983) and refined by RAND Corporation strategic planning, the protocol institutionalizes dissent so unanimity is earned, not assumed. Counters groupthink without depending on a naturally contrarian member.

## Scope Boundary

- **magi `devil`**: structured red-team deliberation. A formal DA role is assigned (rotated), tasked with the strongest possible case against the proposal. Output is a stress-test report feeding Magi's standard VOTE, with explicit groupthink check on any 3-0 unanimous result.
- **magi `decide` / `tradeoff` / `arbitrate` / `strategic` (default lanes)**: balanced three-perspective evaluation. DA is auto-triggered only on 3-0 unanimity; `devil` runs the full protocol regardless of consensus shape.
- **magi `sixhat` (elsewhere)**: parallel single-mode rotation including a Black Hat. DA is deeper than Black Hat — it sustains opposition across all modes with formal role separation.
- **magi `delphi` (elsewhere)**: anonymous multi-round convergence. DA is named (or pseudonymous within a session) and oppositional, not consensus-seeking.
- **flux (elsewhere)**: reframes the problem. DA holds the frame fixed and attacks the proposal within it.
- **riff (elsewhere)**: collaborative idea-deepening. DA is adversarial-by-charter; Riff is generative.
- **omen (elsewhere)**: pre-mortem failure-mode enumeration with FMEA scoring. DA is broader (logic, evidence, assumptions, motivations) and qualitative; Omen is quantitative and failure-focused.

## Workflow

```
ASSIGN   →  rotate DA role; never the proposal author, never the same person twice running
         →  brief DA: "build the strongest case against this, in good faith"

PREPARE  →  DA gets isolated prep time (15-30 min); reads same evidence as proponents
         →  DA may consult external sources; produces written attack list

CHALLENGE →  DA presents 3-7 strongest objections in priority order
          →  proponents may not interrupt; one round of clarifying questions only

REBUT    →  proponents respond to each objection; DA may counter once per objection
         →  facilitator scores: addressed / partially addressed / unaddressed

DECIDE   →  unaddressed objections become explicit risks in the risk register
         →  Magi VOTE proceeds with stress-test results integrated; verdict is final
```

## Role Charter

| Aspect | Specification |
|--------|--------------|
| Selection | Rotated; never the proposal author; ideally someone who would otherwise vote APPROVE |
| Mandate | Argue the strongest case against, not personal opinion; intellectual honesty paramount |
| Time-box | 15-30 min prep, 5-10 min present, 10-15 min rebut |
| Tone | Substantive, not theatrical; no ad hominem, no strawmen |
| Termination | Role ends at session close; no carry-over of position to subsequent decisions |
| Anonymization | Optional: present DA findings without attribution to preserve psychological safety |

## RAND Tradition (Method of Multiple Hypotheses)

| Element | Practice |
|---------|----------|
| Independence | DA prepares without seeing proponents' confidence or conclusions |
| Equal evidence | DA gets identical source material — no cherry-picked weak version |
| Best-faith opposition | DA must construct the strongest possible attack, not a token one |
| Documentation | DA's attack list is preserved in the audit trail regardless of outcome |
| Multiple DAs | For irreversible decisions, run 2 DAs in parallel; if both find the same flaw, weight it heavily |

## Intellectual Honesty Rules

- **No strawmanning**: DA must engage the proposal as proponents actually argue it.
- **No ad hominem**: attack the argument, not the person; institutional DA roles forbid personality contests.
- **No tactical opposition**: DA must believe the objection is genuinely strong, not raise weak ones to fill time.
- **Disclose weak objections**: DA explicitly labels low-confidence objections so they're not weighted equally.
- **Concede when bested**: if proponents convincingly rebut, DA acknowledges. The role is to test, not to win.
- **Single-issue depth over breadth**: 3 strong objections beat 10 weak ones; weak objections dilute the signal.

## When to Invoke

| Trigger | Run DA? | Why |
|---------|---------|-----|
| 3-0 unanimous on complex decision | Mandatory | Default Magi rule; unanimity warrants groupthink check |
| Irreversible architecture choice | Strongly recommended | Cost of error is asymmetric |
| High-stakes Go/No-Go (production, public release) | Strongly recommended | Loss-of-life precedent (Challenger, Columbia) |
| Strategy decision with >1yr commitment | Recommended | Long horizon amplifies undetected flaws |
| Reversible, low-stakes | Skip | Overhead exceeds benefit |
| Already split (1-1-1, 0-3) | Skip | Opposition already present; route to disagreement diagnostic |
| Time-critical (<30 min total budget) | Lite version: single objection round, no rebut | Better than nothing |

## Backfire Effects (Mitigation)

| Risk | Mitigation |
|------|-----------|
| Team entrenchment ("DA is just being difficult") | Rotate role; brief explicitly on intellectual honesty rules |
| Dilution (focus shifts to weak objections) | Cap at 3-7 objections; require DA to rank by strength |
| Identity-based dismissal ("of course Alice opposes") | Anonymize DA output; present as "the position requires response to..." |
| Performative opposition (theatrical, not substantive) | Score objections post-hoc on substance; track DA quality across sessions |
| Confirmation reversal (proponents over-defend) | Facilitator times rebuttal and forces concrete response per objection |

## Tie-In With Magi's Logos / Pathos / Sophia

- DA's objections naturally cluster by perspective:
  - **Logos-attack**: technical infeasibility, evidence gaps, logic flaws, calibration issues
  - **Pathos-attack**: human cost, team capacity, ethics, stakeholder harm
  - **Sophia-attack**: opportunity cost, ROI miscalculation, market timing, sunk cost masking
- After DA challenge: each Magi perspective re-votes with DA's objections explicitly considered. Confidence deflation is expected and welcome.
- DA is not a fourth vote — it's a stress test feeding the three votes. Running DA + 3-perspective vote yields stronger calibration than 4 independent voters.
- For 3-0 verdicts: post-DA, if confidence drops below 70, downgrade to "approve with reservations" and elevate unaddressed objections to risk register.

## Anti-Patterns

- Same person plays DA repeatedly — rotates identity-based dismissal into structural one. Rotate; track rotation log.
- DA briefed only on weaknesses ("find what's wrong") — produces tactical opposition. Brief on the full proposal and let DA find the strongest flaws.
- Skipping the rebut phase — DA's objections sit unanswered, decisions ship with hidden risks. Always force concrete rebuttal per objection.
- Treating DA as veto — DA's role is to test, not to block. Unaddressed objections become risks, not stop signs (unless severity warrants).
- Running DA only when convenient — DA on easy decisions and skipping on hard ones inverts the value. Triggers should be threshold-based, not mood-based.
- Over-running DA on reversible low-stakes — overhead destroys throughput; reserve for irreversibility, high-stakes, or unanimity.
- Conflating DA with Black Hat — Black Hat is a 3-5 min mode within Six Hats; DA is a 30-60 min role-charter protocol with independent prep, presentation, rebuttal, and audit trail.
- Authoring proposal and playing DA — the same mind cannot honestly attack its own work; assign DA to someone else, full stop.

## Handoff

- **To Magi VOTE**: DA report (objection list with addressed/partial/unaddressed status) becomes input evidence; perspectives re-evaluate with explicit consideration of DA's strongest unaddressed point.
- **To Omen**: unaddressed Logos-attacks with concrete failure mechanisms escalate to Omen for FMEA-grade quantification.
- **To Flux**: if DA's strongest objection is "wrong frame," halt VOTE and route to Flux for reframing before resuming.
- **To human**: if DA produces an unaddressable objection on an irreversible decision, escalate to human regardless of consensus pattern.
- **To audit trail**: DA name, objections, rebuttal scores, and rotation log preserved; future Magi sessions reference DA quality history for selection.
