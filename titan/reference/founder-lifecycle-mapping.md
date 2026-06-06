# Founder Lifecycle ↔ Titan Phase Mapping

Anthropic's *Founder's Playbook* frames the journey from idea to scaled product as a four-stage lifecycle: **Idea → MVP → Launch → Scale**. Titan's phased delivery (DISCOVER → DEFINE → ARCHITECT → BUILD → HARDEN → VALIDATE → LAUNCH → GROW → EVOLVE) is the implementation backbone for this lifecycle. This reference makes the mapping explicit so that Titan-driven work can be communicated in founder vocabulary and gated against stage-appropriate exit criteria.

[Source: claude.com — *The Founder's Playbook* (2026)](https://claude.com/blog/the-founders-playbook)

---

## 1. Stage Mapping

| Founder Stage | Primary Question | Titan Phase(s) | Default Scope |
|---------------|------------------|----------------|---------------|
| **Idea** | Is there a real problem worth solving for a real audience? | `DISCOVER`, `DEFINE` | S / M (single agent or 1-2 specialists) |
| **MVP** | Can a minimal working version of the product solve the problem end-to-end? | `ARCHITECT`, `BUILD`, `VALIDATE` | M / L (Builder + Sherpa + Radar; light Sentinel only if release risk) |
| **Launch** | Can we put it in front of real users with acceptable quality? | `HARDEN`, `LAUNCH` | L (full quality stack: Sentinel + Radar + Guardian + Launch) |
| **Scale** | Can we grow usage, reliability, and team without rebuilding? | `GROW`, `EVOLVE` | L / XL (Rally for parallel feature tracks; Atlas / Schema / Stream for architecture-grade work) |

## 2. Founder's Role Shift

The Playbook's central thesis: **the founder's role shifts from individual contributor to orchestrator** as the company moves through the stages. Titan is built around the same principle — Titan does not write code; it issues chains, tracks state, and enforces forward progress. When a user invokes Titan, treat that invocation as the founder/PM hand-off moment: the user is asking to operate at the orchestrator level, not the IC level.

Practical implication during `JUSTIFY`:
- Reject requests that would push Titan back into IC mode ("just write this small file") → route directly to `Builder` instead.
- Accept requests where the user describes outcomes rather than implementations → Titan stays in chain-issuance mode.

## 3. Stage-Specific Failure Modes (Titan-authored extension)

The *Founder's Playbook* notes that each stage has characteristic failure modes but does not enumerate them in the public excerpt. The table below is **Titan's operational interpretation** — it composes commonly-cited startup failure patterns with Titan's existing refusal triggers. Use as guidance, not as a verbatim Playbook citation:

| Stage | Failure Pattern | Titan Refusal Trigger |
|-------|----------------|------------------------|
| Idea | Premature scaling enthusiasm (jumping to architecture before validating the problem) | User skips `DISCOVER`/`DEFINE` and asks for production-grade L/XL chain without a problem statement → reduce scope, run `DISCOVER` first |
| MVP | False product-market fit signal (mistaking early hype for traction) | User wants new features before VALIDATE has met SUCCESS_CRITERIA → reject scope addition, finish MVP first |
| MVP | AI-generated code tech debt accumulation | Chain output passes tests but skipped Sentinel/Zen → add `Sentinel` and `Zen` to next chain in the same lifecycle |
| Launch | Hypothesis push without validation | LAUNCH phase ships without VALIDATE pass at ≥85% (staging tier) → block LAUNCH, return to VALIDATE |
| Scale | Architecture rebuild masquerading as feature work | GROW chain proposes >30% file rewrite under feature label → reclassify as `EVOLVE`, ask user for explicit reclassification |

## 4. Exit Criteria per Stage (Titan-authored extension)

Use stage-aware exit criteria during `VALIDATE`. The thresholds below are **Titan's operational defaults**, not Playbook-prescribed numbers — the *Founder's Playbook* frames each stage qualitatively but does not publish specific exit thresholds in its public excerpt. Tune to the actual product context; the goal is that each stage gates external visibility more strictly than the next-inner phase:

| Stage | Internal Phase Exit (existing rule) | Stage Exit (Titan default — tune to context) |
|-------|--------------------------------------|----------------------------------|
| Idea | DISCOVER/DEFINE complete | Problem statement is grounded in real-user evidence (multiple interviews, observed pain, or competing-solution analysis). Synthetic evidence from agents alone is not acceptable. |
| MVP | BUILD/VALIDATE at ≥85% staging | Real user can complete the primary journey end-to-end without operator intervention. |
| Launch | HARDEN passes Sentinel + Radar gates | Rollback plan exists; one-line "what to do if it breaks at 3am" is written; observability surfaces the primary failure modes. |
| Scale | GROW/EVOLVE phases produce artifacts | New work is additive — old paths still function; growth does not require coordinated team-wide redeploys. |

## 5. Vocabulary in `TITAN_COMPLETE`

When closing a chain that completes a founder-stage milestone, surface the stage transition in the output:

```yaml
TITAN_COMPLETE:
  founder_stage_entered: MVP        # or: Launch, Scale
  next_stage_gate:                  # what must be true before advancing
    - "Real user completes primary journey unaided"
    - "Three production incidents simulated and recovered"
  recommended_next_focus: HARDEN    # corresponding Titan phase
```

This gives the user (acting as founder/PM) a vocabulary they can use with non-engineering stakeholders without translating from "VALIDATE phase passed at 87% staging tier".

## 6. When This Reference Is the Wrong Tool

- The work is bug-fix or refactor on an existing product → no founder-stage context; use the standard `S/M/L/XL` scope mapping directly.
- The user is an enterprise team, not a founder → use the *Building AI agents for the enterprise* framing instead (different role-shift dynamics, different success metrics). Titan's `L/XL` phased delivery still applies; the founder-stage vocabulary does not.
- Pure architecture / DDD modelling → route to `Atlas`; founder vocabulary adds no value to internal model design.

---

Use this reference during `SCOPE_DETECT` to choose the right framing, and during `COMPLETE` to communicate progress in stage-appropriate language.
