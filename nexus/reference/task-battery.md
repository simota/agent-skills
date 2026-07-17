# Nexus Task Battery — Routing Verification Suite

**Purpose:** Standing regression battery for the `classify` flow (`RESOLVE → GATE → MULTI? → REDIRECT? → SELECT → LADDER? → CHAIN_SELECT`). Re-run this battery whenever `routing-matrix.md`, `signal-keywords.md`, or the Recipes table in `nexus/SKILL.md` changes, to prove routing behavior didn't regress.

**Read when:** Verifying a routing-machinery change (LADDER wiring, Recipe additions, Signal Keyword edits) before merge, or re-running the Wish #1 harness regression check.

**Verification depth:** All items verified at routing/chain-selection level (does the item resolve to the expected chain — no full execution required). Items marked **[E2E]** are candidates for real end-to-end execution when validating the harness end-to-end, not just its routing decisions. **Executed status**: Cycle-1 ran 2 live end-to-end probes matching two [E2E] items' shapes — Probe-Redirect (item 7's shape: "improve the design" REDIRECT walk) and Probe-Ladder (item 29's shape: full LADDER walk on the USPTO patent-filing out-of-coverage case). Both are marked **[E2E executed]** below; the remaining [E2E] items (5, 12) are **[E2E pending]** — routing-level only so far, real end-to-end execution not yet run against them.

---

## Battery (35 items)

Items 1-30 are Candidate A's original battery (routing-level verification for the Recipe Families + ambiguous/edge inputs). Items 31-35 are Phase-2 salvage fold-ins (S9): 2 additional ambiguous-anchor stress tests + 3 additional out-of-coverage items (beyond A's patent-filing / travel-booking) to broaden the dim-3 (Coverage closure) proof beyond two data points. C's ecosystem-l10n item was explicitly discarded (S9: "partial overlap" with `polyglot`, not a clean out-of-coverage case).

| # | Input | Family | Expected routing |
|---|-------|--------|-------------------|
| 1 | `/nexus bug` — "login returns 500 after deploy" | Fix | `bug` Recipe directly (subcommand match) |
| 2 | "there's a memory leak in the worker pool" | Fix | `classify` → Signal Keywords → `bug` (memory leak carve-out, not `optimize`) |
| 3 | "CVE-2026-xxxx in our lodash dep" | Fix | `security` |
| 4 | "clean up this module, no behavior change" | Improve | `refactor` |
| 5 | "make the dashboard load faster" **[E2E pending]** | Improve | `optimize` (measure-first) |
| 6 | "polish the checkout flow" | Improve | `kaizen` (overloaded `polish`/`improve` → REDIRECT per signal-keywords.md, resolves to `kaizen` given "existing feature, multi-axis") |
| 7 | "improve the design of this component" (ambiguous) **[E2E executed — Probe-Redirect]** | Improve | REDIRECT one-question: code-design → `anneal`, UI/look-and-feel → `restyle` |
| 8 | "audit this codebase's architecture for weaknesses" | Improve | `anneal` |
| 9 | "redesign the settings screen, make it modern" | Improve | `restyle` |
| 10 | "run this until it's done, don't stop" | Loop | `loop` dispatcher → gates to goal/converge/orbit/apex |
| 11 | "set up a goal to keep the test suite green nightly" | Loop | `goal` (checks for machine-checkable oracle + hard-stop bound) |
| 12 | "add OAuth login" **[E2E pending]** | Build | `feature` |
| 13 | "build this whole idea end to end, 8-25 agent budget ok" | Build | `apex` |
| 14 | "build our whole game vertical slice" | Build | `playable` |
| 15 | "spec out a notifications feature before building" | Discover→build | `spec` (stops at spec; pairs with `feature`) |
| 16 | "give our repo a self-driving team+work plan" | Discover→build | `charter` (stops at doc; pairs with `enact`) |
| 17 | "think through whether microservices are worth it here, no code" | Reason | `gedanken` |
| 18 | "evolve the checkout feature — no code, just direction" | Reason | `delve` (overloaded "evolve a feature" → REDIRECT resolves here since no-code stated explicitly) |
| 19 | "map how this repo works across the 3 services" | Comprehend | `cartograph` |
| 20 | "how did this codebase get the way it is, from git history" | Comprehend | `chronicle` |
| 21 | "what's the one must-have feature here" | Verdict | `essential` |
| 22 | "what feature is dead weight, safe to remove?" | Verdict | `trim` |
| 23 | "clone this competitor's onboarding flow" | Reproduce/Synth | `clone` |
| 24 | "this is a once-in-a-lifetime ask, spare nothing" | Quality-Max | `wish` (always-confirm gate fires) |
| 25 | "give me the best possible design for our flagship screen" | Quality-Max | `runway` |
| 26 | "generate a full research + legal + saas doc package" | Document package | `package` |
| 27 | `/nexus` with no arguments | Meta | `proactive` |
| 28 | "switch to the security-focused skill profile for this sprint" | Meta | `pack` |
| 29 | **[out-of-coverage, E2E executed — Probe-Ladder]** "negotiate and file the actual patent application for this algorithm with the USPTO" | none of 132 | `classify` → REDIRECT fails, SELECT fails (no matrix row: patent prosecution is not code/design/research-artifact work any of the 132 skills claim) → LADDER: `compass(recommend)` returns Gap mode → `architect` gap-fill proposal artifact presented to user (e.g., "no `patent`/IP-filing skill exists; nearest partial-fit is `clause` for ToS/Privacy legal review, not patent prosecution — propose new skill or route to human patent counsel"); `fallback_taken: architect-invoked` |
| 30 | **[out-of-coverage]** "book flights, hotels, and a group dinner reservation for the 12-person team offsite" | none of 132 | Same LADDER path — `compass` Gap mode (no travel/logistics-booking skill in the 132) → `architect` proposal or explicit "route to a human travel coordinator; no in-repo skill covers real-world booking transactions" — never silently answered as generic travel advice; `fallback_taken: architect-invoked` |
| 31 | **[ambiguous stress test]** bare "optimize" (no object, no target, no metric named) | Improve (ambiguous) | `classify` → `GATE` fires (context_confidence < 0.60 or 2+ valid interpretations: perf tuning? DB query? cost? team process?) → ONE focused clarifying question before any chain is selected — never silently guesses `optimize` |
| 32 | **[ambiguous stress test]** bare "landing page" (no verb, no scope) | Build/Improve (overloaded) | `classify` → `REDIRECT` fires on the overloaded `landing page` anchor (routine LP → `bazaar`/`funnel`; wish-grade one-shot LP → `marquee` — per `signal-keywords.md` marquee row) → one-question REDIRECT disambiguation, not a silent default to either |
| 33 | **[out-of-coverage]** "prove this sorting algorithm terminates and is correct using formal methods / theorem proving" | none of 132 | `classify` → REDIRECT fails, SELECT fails (no matrix row: formal verification / theorem-proving toolchains, e.g. Coq/Lean/TLA+, are not claimed by any of the 132 skills — `radar`/`attest` cover empirical test/spec conformance, not machine-checked proof) → LADDER: `compass` Gap mode → `architect` proposal (e.g. "no `formal-verify` skill exists; nearest partial-fit is `attest` for spec-conformance testing, not machine-checked proof — propose new skill or route to a formal-methods specialist"); `fallback_taken: architect-invoked` |
| 34 | **[out-of-coverage]** "negotiate and draft the commercial lease terms for our new office space" | none of 132 | `classify` → REDIRECT fails, SELECT fails (no matrix row: real-estate lease negotiation is not code/design/research-artifact work; `clause` covers ToS/Privacy/Tokushoho only, explicitly excludes other contract types) → LADDER: `compass` Gap mode → `architect` proposal or explicit "route to a commercial real-estate attorney; no in-repo skill covers lease negotiation"; `fallback_taken: architect-invoked` |
| 35 | **[out-of-coverage]** "configure the BACnet/Modbus points list for the building's HVAC controllers" | none of 132 | `classify` → REDIRECT fails, SELECT fails (no matrix row: OT/building-automation protocol configuration — BACnet/Modbus point mapping — is outside every skill's declared scope, including `hearth`/`gear`/`scaffold` which are dev-environment/CI infra, not physical OT/ICS) → LADDER: `compass` Gap mode → `architect` proposal or explicit "route to a building-automation/OT engineer; no in-repo skill covers BACnet/Modbus point configuration"; `fallback_taken: architect-invoked` |

Items 29-30 and 33-35 are the dim-3 proof points (5 total, exceeding the rubric's ≥2 minimum): each must terminate in a named `compass` Gap-mode output and a named `architect` proposal artifact (or an explicit, logged decline recorded as `fallback_taken: neither — reason: <reason>`), never a quietly-generic answer.

---

## Regression discipline

- Re-run items 1-28 whenever `routing-matrix.md`, `signal-keywords.md`, or `nexus/SKILL.md`'s Recipes table changes. Items 1-28 must resolve to byte-identical chain selections across the change — they prove REDIRECT/SELECT priority is untouched.
- Items 29-30 and 33-35 (out-of-coverage) are the only items expected to exercise the LADDER path; re-run them whenever `routing-matrix.md` § LADDER, `compass/SKILL.md` Output Routing "No matching skill" row, or `architect`'s `ARCHITECT_TO_NEXUS_HANDOFF` schema changes.
- Items 31-32 (ambiguous stress tests) are the only items expected to hard-stop at `GATE`/`REDIRECT` with a clarifying question — a regression here means an ambiguous anchor started silently resolving without a question, which is the DC-1-adjacent failure this battery exists to catch.
