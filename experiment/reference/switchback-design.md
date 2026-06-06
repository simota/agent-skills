# Switchback Design Reference

Purpose: Design a switchback (time-series alternation) experiment when user-level randomization is invalidated by interference — marketplaces, logistics, pricing, supply-demand matching. This is a measurement-design reference, not a rollout-risk reference.

## Scope Boundary

- **Experiment `switchback`**: MEASUREMENT design under interference — you cannot trust user-level A/B because treated and control users share the same market. Goal: unbiased average treatment effect on the market.
- **Mend `canary` (elsewhere)**: ROLLOUT risk-control — gradually expose traffic to a new release, watch for regressions, roll back. Goal: safe deployment.

If the question is "will pricing change X improve GMV without breaking supply?" on a shared marketplace → `switchback`. If the question is "does this service deploy introduce errors at 5 % traffic?" → `Mend canary`.

## When Switchback Beats User-Level A/B

User-level randomization is invalid when the treatment **spills over** between arms via a shared resource:

- **Two-sided marketplaces** (Airbnb, DoorDash, Uber, Lyft): treated riders/guests compete for the same drivers/hosts as control.
- **Pricing experiments**: treated users' prices affect control users' inventory availability.
- **Matching / dispatch algorithms**: treated orders consume supply that control orders would have matched.
- **Network / social features**: a treated user's post is seen by control users.

Airbnb's 2018 marketplace meta-experiment (Blake et al.) showed > 20 % of individual-level TATE estimates were attributable to interference bias — eliminated by clustered / market-level designs.

## Design Decisions

| Axis | Options | Default |
|------|---------|---------|
| Unit | Geographic region, time window, region × time | Region × time (DoorDash, Uber) |
| Rotation window | 30 min, 1 h, 4 h, 1 day | 1 h for logistics; 1 day for marketplace pricing |
| Randomization | Simple Bernoulli, block, stratified | Blocked by day-of-week × hour-of-day |
| Carryover handling | Washout period, burn-in, model-based | Washout of ≥ 1 rotation window |
| Estimator | Difference-in-means, fixed-effects regression | Fixed-effects (region + time) |
| Variance | Naïve SE, block bootstrap, Bojinov HAC | Block bootstrap or HAC |

## Rotation Window Selection

Trade-off: shorter windows increase statistical power (more observations) but increase carryover contamination.

Pick the rotation window at **2–5 × the causal-response horizon** of the treatment. For logistics dispatch (response within minutes), 30 min–1 h is standard (DoorDash: 30 min; Uber: 1 h); for pricing (response over hours as users shop), 4 h–1 day is standard (Lyft prime-time: hourly; Airbnb pricing: daily).

If the treatment effect takes > 24 h to manifest (e.g., supply recruitment), switchback is the wrong tool — use **cluster randomization at the city level** with a long run.

## Carryover Handling

The core threat: supply depleted during treatment windows is unavailable in subsequent control windows, biasing control downward (or vice versa).

- **Washout / burn-in**: discard the first X minutes of each rotation from analysis — standard DoorDash practice (discard first 5 min of 30-min windows).
- **Model-based adjustment**: Bojinov, Simchi-Levi, Zhao (Management Science 2023, "Design and Analysis of Switchback Experiments") derive HAC-type variance estimators and optimal design under carryover; the follow-up Xiong-Chin-Taylor (2024, arXiv:2406.06768) framework decomposes estimation error into carryover, periodicity, serial correlation, and simultaneous-experiment interference, and learns an empirical-Bayes rotation schedule that reduces MSE by 33% on ride-sharing data.
- **Balanced Latin squares**: ensure each treatment follows each other treatment equally often across the run — prevents autocorrelation confounding.
- **Randomize interval start / end points** to reduce both bias and variance from simultaneous experiments running on the same fleet (Xiong-Chin-Taylor 2024).
- **Horvitz-Thompson estimation under known assignment mechanism**: exact inference when randomization is transparent (Bojinov & Shephard 2019).

## Block Randomization

Do not use simple Bernoulli — it produces runs of consecutive treatment (or control) windows that amplify carryover and day-of-week confounding.

- **Block by day-of-week × hour-of-day**: pair each (Tue, 14:00) treatment window with a (Tue, 14:00) control window — standard Uber practice.
- **Stratify by region tier**: major metros and tail markets get separate randomization schedules to preserve balance.
- **Pre-register the rotation schedule**: no mid-flight reshuffling. Changing schedules mid-experiment invalidates variance estimates.

## Precedent

- **DoorDash**: 30-min switchback for dispatch / batching algorithms. Fixed-effect regression with market × hour-of-day fixed effects.
- **Uber**: 1-h switchback for pricing, matching. Custom "switchback framework" with automated carryover-aware variance estimation. See Uber Engineering blog (2018, 2020).
- **Lyft**: hourly switchback for ETAs, surge pricing. Block-randomized by day-part.
- **Airbnb**: day-level switchback for ranking + pricing (when market-level cluster is impractical). Post-2018 shift toward market-level cluster randomization for longer-horizon treatments.
- **Literature**: Bojinov, Simchi-Levi, Zhao (2023) *"Design and Analysis of Switchback Experiments"* — *Management Science* (HBR working paper WP21-034); Hu & Wager (2022) *"Switchback Experiments under Geometric Mixing"* (arXiv:2209.00197); Xiong, Chin, Taylor (2024) *"Data-Driven Switchback Experiments: Theoretical Tradeoffs and Empirical Bayes Designs"* (arXiv:2406.06768) — proposes an empirical-Bayes design tuned on prior switchback data from a ride-sharing platform that reduces estimator MSE by **33% vs the status quo design**; identifies the four design tensions as carryover, periodicity, serial correlation, and contamination from simultaneous experiments.

## Sample Size / Duration

- Effective N = number of rotation windows (NOT number of user-events within windows — they are correlated).
- Typical logistics switchback: 2–4 weeks × 24 windows/day × N markets = thousands of windows.
- MDE scales with √(N_windows); adding users within a window does not improve power proportionally.
- Power analysis: use block-bootstrap simulation on historical data at the chosen rotation granularity.

## Anti-Patterns

- Running switchback for a treatment with multi-day response horizon — carryover swamps signal.
- Computing variance as if window observations were independent — under-reports SE by 2–5×.
- Simple Bernoulli rotation producing 6+ consecutive treatment windows — confounded with time-of-day.
- Skipping washout — first minutes of a new window reflect the previous window's supply state.
- Comparing switchback estimates to user-level A/B estimates on the same treatment and picking the prettier one — HARKing dressed up as robustness.
- Switching between switchback and cluster randomization mid-analysis — pick one at design time.

## Switchback vs Cluster Randomization vs User-Level A/B

Three designs sit on a spectrum of interference strength and treatment horizon:

| Design | Interference | Treatment horizon | Effective N | Pick when |
|--------|--------------|-------------------|-------------|-----------|
| User-level A/B | None / negligible | Any | Users | Treated and control users do not compete for shared resources |
| Switchback | Strong, time-local | Minutes–hours | Rotation windows | Response manifests within one rotation; carryover bounded by washout |
| Cluster randomization | Strong, persistent | Days–weeks | Clusters (cities, markets) | Response horizon exceeds feasible rotation; supply/demand accumulates effect |

Airbnb moved many ranking/pricing experiments from user-level to cluster-level (city/market) after the 2018 meta-experiment; DoorDash and Uber keep switchback for dispatch/matching because the response is within minutes.

## Output Checklist

- Unit of rotation (region × time, city × day, etc.).
- Rotation window length and justification against response horizon.
- Randomization schedule (block structure, pre-registered).
- Carryover handling (washout length, estimator).
- Variance estimator (block bootstrap / HAC / model-based).
- Effective N (number of windows, not events).
- Power simulation against historical data.
- Stop rule and minimum run duration.
- Explicit decision: switchback vs cluster vs user-level, with the interference mechanism and response horizon justifying the choice.
