# UX Principle Conflicts — Arbitration Reference

> **Tier:** `domain` — activates when the task's subject matches. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

Shared cross-skill reference. UX principles are not a ranked list; most of them are **pairs that
trade against each other**. A review that cites one principle and stops has not made a decision —
it has picked a side and hidden the cost.

This file catalogs the recurring conflicts, names the failure produced by optimizing one side
alone, and gives the variables that decide the allocation.

**Consumers:** `palette` (usability review, interaction arbitration) · `vision` (direction
justification, redesign trade-offs) · `muse` (the `decision-priority.md` unit of a delivered
design-system package — see `reference/design-system-context.md` §4) · `magi` (escalation target
when the allocation is contested) · `echo` (explaining *why* a walkthrough friction point is
intentional) · `funnel[premium]` / `funnel` (conversion vs. trust) · `atelier` / `forge` / `artisan`
(implementation-time trade-offs).

**Evidence tier:** practitioner synthesis. These pairings are a working taxonomy, not a standard
and not an experimental result. Cite them as a **structure for the argument**, never as authority
for the verdict. Contrast with `_common/PROPORTION_AND_SPACING.md` §1, where Tier 1-2 numbers are
citable as requirements.

---

## 1. First: this file only handles Trade-offs

`_common/CANDIDATE_SELECTION.md` §4 splits every criterion into **Gate**, **Trade-off**, and
**Preference**. That split runs before this file, and it is not negotiable:

- **Accessibility minimums, legal requirements, rights, confidentiality, and data-protection
  obligations are Gates.** They never enter this matrix. "Accessibility vs. brand expression" is
  not a conflict to allocate — the floor is a boolean, and brand expression competes in the space
  above it.
- Everything below is a genuine Trade-off: raising one side measurably lowers the other.
- If a conflict resolves the same way every time regardless of context, it was a Preference, and
  it belongs in the design system's defaults rather than in an arbitration record.

---

## 2. The conflict matrix

| Principle A | Principle B | Failure from optimizing A alone | Deciding variables |
|---|---|---|---|
| Simplicity | Discoverability | Low-frequency features are hidden until first-time users cannot find them at all | frequency · role · searchability · progressive disclosure |
| Consistency | Context optimization | Uniformity blocks the shortest path for a specific local task | transfer-learning benefit vs. local efficiency |
| Learnability | Expert efficiency | Explanations and stepwise flows slow down repeated work | frequency · expertise · shortcuts |
| Safety | Operation speed | Confirmations reduce mis-operation, then become habitual and unread | consequence severity · reversibility · frequency |
| Information density | Scannability | More visible data enables comparison but raises search noise | screen role · expertise · viewing distance |
| Flexibility | Predictability | Many settings and paths make current state hard to determine | user capability · auditability |
| Automation | User control | Automation raises throughput while overwriting the user's intent | uncertainty · correction cost · explainability |
| Personalization | Stability | Optimization destroys the learned position and order of things | change frequency · explicitness · reset path |
| Emphasis | Visual quiet | Emphasizing everything erases priority | task-level uniqueness · urgency |
| Modal confirmation | Flow continuity | The interruption secures attention but severs context | severity · reversibility · alternative UI |
| Progressive disclosure | Findability | Hiding lowers initial load and conceals that the feature exists | point of need · information scent · search |
| Delight | Clarity | Staging and motion blur state and meaning | purpose · repetition · latency · motion sensitivity |
| Security | Convenience | Friction deters attackers and legitimate users equally | threat model · risk tier · recovery path |
| Business outcome | User benefit | Local conversion gains erode long-term trust and self-determination | incentive alignment · long-horizon metrics |
| Transparency | Information overload | Full disclosure does not produce understanding | layering · summary · access to the original |
| Immediate feedback | Screen stability | Fine-grained change reassures, then becomes noise | change importance · frequency · aggregation |
| Standardization | Exception handling | Shared components make genuinely special work feel unnatural | exception frequency · reuse value · maintenance ownership |
| Reversibility | Finality | An undo grace period delays state commitment and downstream processing | chained processing · legal finality · history |

**The "Failure" column is the load-bearing one.** Naming which side is winning is easy and mostly
uninformative. Stating the concrete damage the win causes is what makes the allocation reviewable
later, and what stops a reviewer from re-litigating the same pair every sprint.

---

## 3. Resolution sheet

Fill this before allocating. An allocation recorded without it is a preference wearing a rationale.

```
Target users and situation of use:
Task frequency and expertise:
Error types and their consequences:
Reversibility and time to recover:
Time pressure and environmental variability:
System uncertainty (how often is the system itself wrong?):
Accessibility requirements in play:
Information sensitivity and permissions:
Alignment between user benefit and business benefit:
Allocation adopted — and the alternative rejected, with its reason:
Verification method, guardrail metric, and the condition that reopens this decision:
```

The last two lines are the ones that get dropped and matter most. A record with no rejected
alternative cannot be re-examined; a record with no reopening condition becomes permanent by
default when the conditions that justified it have changed.

---

## 4. Rules

1. **Never resolve a pair by general priority.** "Consistency wins" and "safety always wins" are
   both wrong as standing rules. Allocate by failure cost and conditions of use.
2. **Both sides get a named cost.** If you cannot state what the losing side gives up, you have
   not identified a real conflict — you have identified a preference.
3. **One-sided optimization is a review finding.** A proposal that improves one axis with no
   stated effect on its pair is incomplete, not clean.
4. **A recurring exception indicts the contract, not the product.** When the same conflict is
   re-allocated the same way across products, the shared component or principle is mis-specified.
   Upstream the resolution instead of re-arbitrating it.
5. **Escalate contested allocations to `magi`**, which carries the Logos/Pathos/Sophia lenses and
   the `Reversibility` / `Threshold` axes (`magi/reference/decision-domains.md`). This file
   supplies the pair and the failure mode; `magi` arbitrates when the deciding variables conflict.
6. **Business-vs-user conflicts get an extra check.** When the allocation favors business outcome,
   verify against `vision/reference/ux-anti-patterns-ethics.md` that the result is not a deceptive
   pattern under another name. Incentive alignment is a deciding variable, not an excuse.

---

## 5. Where the allocation goes

| Destination | What it carries |
|---|---|
| `decision-priority.md` in a delivered design-system package | the standing allocations, so an agent facing the conflict does not pick silently |
| The design/PR record | the resolution sheet for a specific contested decision |
| The guardrail metric | the verification line, so the losing side's cost is observed rather than assumed |
| `magi` decision record | contested allocations, with the rejected alternative preserved |
