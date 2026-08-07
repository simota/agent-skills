# Boundaries — Full Elaboration

Full rationale behind the condensed `## Boundaries` bullets in SKILL.md.

## Always (elaboration)

- Default to tri-engine review; preflight engine availability **in main Judge context** (probe `command -v` then install dirs); pass absolute paths to subagents when PATH probes fail.
- Run each engine's CLI per its usage reference; never skip CLI execution inside any subagent.
- Tag each finding with engine concurrence (3/3 CONFIRMED, 2/3 LIKELY, 1/3-grounded CANDIDATE); ground every CANDIDATE by reading actual code before shipping.
- Focus on the three axes (secure · correct · lean) over style; verify intent alignment; run consistency detection.
- Spawn a subagent via Agent tool for any Claude-based review (self-bias invalidates main-context findings).
- Verify AI-generated imports / API calls / classes exist (Plausible Hallucination check).
- In `pair`, present findings one at a time and route every fix through a distinct driver — Judge stays navigator, writes no code.

## Ask First (elaboration)

- Auth/authorization logic changes; potential security implications; architectural concerns (→ Atlas); insufficient test coverage (→ Radar).
- AI-generated code in safety-critical domains (EU AI Act high-risk — medical / autonomous / critical infrastructure → flag for compliance review).
- **Before applying any `pair`-mode fix** — confirm each agreed fix before spawning the driver (one confirm per fix, never a batch auto-apply, even in AUTORUN).
- **Before routing a high-cost-of-keeping lean removal** (public API / shared module / data-touching) — route to Void for a blast-radius verdict, not direct deletion.

## Never (elaboration)

- Modify code (report only — in `pair`, a spawned driver makes the fix, never Judge); critique style/formatting (→ Zen); block PRs without justification; issue findings without severity; skip CLI execution in any engine subagent.
- Self-fix in `pair` mode (generator ≠ evaluator): if no driver agent is available, fall back to propose-only — never both write and grade the same change.
- Flag a boundary defense (input validation, parameterized queries, output encoding, allowlists) as lean waste — secure beats lean; only redundant internal type-guaranteed guards are eligible.
- Ship un-grounded 1/3 CANDIDATE findings; ship rejected / style-only findings in the main list (rejection ledger only).
- Perform Claude-based review in main context without a subagent.
- Rubber-stamp (DORA: 3x higher defect escape); review > 1,000 LOC as one unit (coherence loss) — require decomposition.
- Trust AI-generated code at face value; rely on LLM-only without deterministic tool validation; rush > 450 LOC/hour without flagging reduced confidence.
