# Priority Poker Delta

Purpose: Rank `pokerplan` facilitation and bias-control contract. Planning Poker and Fibonacci scales are model-known.

## Protocol

1. Define the dimension being voted on; never mix value, effort, risk, and confidence into one unexplained card.
2. Select low/mid/high reference items and calibrate them before novel items.
3. Vote privately and reveal simultaneously.
4. Treat `?` as missing context, not zero.
5. When votes are dispersed, highest and lowest voters explain first; re-vote at most three rounds.
6. Persistent disagreement is an input to Magi, not a reason to force consensus.

Default dispersion gate: re-discuss when the spread crosses more than two Fibonacci steps. Teams may choose another gate, but must record it before voting.

## Required Output

| Item | Dimension | Final votes | Aggregate | Dispersion | Rounds | Confidence | Key disagreement |
|---|---|---|---:|---:|---:|---|---|

Record anchors, participants or represented roles, missing-context cards, and any facilitator override. Feed the resulting component scores into ICE/RICE/WSJF only after preserving their units.

## Reject

- Sequential reveal or leader-first discussion.
- Uncalibrated sessions whose scores are compared across teams or dates.
- Averaging `?` cards into the result.
- More rounds used to wear down dissent.

## Handoff

- Formula scoring -> Rank recipe matching the chosen dimensions.
- Structural disagreement -> Magi.
- Top item decomposition -> Sherpa.
- Missing feature substance -> Spark.
