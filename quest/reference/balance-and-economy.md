# Balance & Economy

**Purpose:** Model game balance and in-game economy as tunable data, and detect dominant/degenerate strategies and economy failure modes.
**Read when:** Tuning balance or designing an economy (`balance` / `economy` recipes).

## Contents
- Balance is a model
- Power curves & difficulty
- Time-to-kill / time-to-goal
- Cost/reward tables
- Dominant & degenerate strategies
- Economy: sources & sinks
- Equilibrium & failure modes
- Monetization neutrality
- Pitfalls

---

## Balance is a model

Never balance by adjective ("feels fair"). Express balance as numbers in tables/curves so it can be tuned, simulated, implemented (Tick), and validated (playtest). Numbers in design docs are *starting points with a tuning range*, not final truth — mark them as such and pair each with a playtest hypothesis.

---

## Power curves & difficulty

- **Player power** and **enemy/challenge power** are two curves over progression. Their gap IS the difficulty.
- Decide the intended gap shape: flat (constant challenge), sawtooth (power spike → world catches up), or widening (power fantasy).
- Express as a formula or table: `enemy_hp(level) = base * growth^level`. Pick `growth` so time-to-kill stays in target as both curves rise.

```
difficulty(t) ≈ challenge_power(t) − player_power(t)
# tune the curves so this stays inside the target band (not too flat = boring, not too high = unfair)
```

---

## Time-to-kill / time-to-goal

The clearest balance metric: how long a core interaction takes.
- Define a **target** (e.g., "a grunt dies in ~1.5 s, a brute in ~6 s") and tune stats to hit it across the power curve.
- Too short = no decisions; too long = grindy. The target encodes the intended feel.
- Works for non-combat too: time-to-build, time-to-unlock, time-to-win.

---

## Cost/reward tables

Every player choice has a cost (time, resource, risk) and a reward (power, progress, currency). Tabulate them and check ratios:

```yaml
upgrade:
  sword_t1: { cost_gold: 100,  dps_gain: 5,   ratio: 0.050 }
  sword_t2: { cost_gold: 300,  dps_gain: 12,  ratio: 0.040 }
  armor_t1: { cost_gold: 120,  ehp_gain: 40,  ratio: 0.333 }
# Compare ratios across options — wildly different ratios create dominant picks.
```

---

## Dominant & degenerate strategies

- **Dominant strategy**: one option is strictly best, collapsing player choice. Detect by comparing cost/reward ratios and win-rates; no option should dominate across contexts.
- **Degenerate strategy**: an unintended exploit that's more effective than playing "as designed" (turtling, farming a safe spot, infinite combo). Enumerate likely exploits and design counters (diminishing returns, scaling threat, soft caps).
- Hand large combination spaces (classes × weapons × enemies) to **Matrix** for coverage analysis.

---

## Economy: sources & sinks

Every resource needs both, named explicitly:

| Resource | Sources (in) | Sinks (out) |
|----------|--------------|-------------|
| Gold | Enemy drops, quest rewards, selling | Upgrades, consumables, repairs |
| Energy | Regen over time, items | Actions, fast-travel |

If a resource has sources but no sinks → inflation (it becomes worthless). Sinks but no sources → starvation/grind. Model the flow rate per session.

---

## Equilibrium & failure modes

- Model net flow: `Δresource/session = sources − sinks`. Decide if it should trend up (power fantasy), flat (tight economy), or be player-controlled.
- **Inflation**: too much income → prices feel trivial, currency dead. Add sinks (repairs, premium upgrades, consumables).
- **Grind wall**: a sink far exceeds realistic income → players stall/churn. Re-tune or add catch-up sources.
- **Dead currency**: a resource with no meaningful sink → remove it or give it purpose.

---

## Monetization neutrality

- Design the gameplay economy **monetization-neutral** first; add IAP hooks without making them mandatory.
- Under a **cosmetic-only** brief: never gate power behind purchase (no pay-to-win).
- Under **progression IAP**: guard against pay-to-win and against tuning the free path into a grind wall that only money skips — that's a design smell, flag it.

---

## Pitfalls

- Balance expressed as adjectives instead of numbers.
- A single dominant option that erases choice.
- Open economy loops (source with no sink, or vice versa).
- A grind wall that exists only to sell the skip.
- Tuning in prose without a target metric (time-to-kill, net flow).
- Not stress-testing the combination space for exploits.
