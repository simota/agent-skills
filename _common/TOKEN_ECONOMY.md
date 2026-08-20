# Token Economy — Repository Standard

> **Tier:** `authoring` — activates when creating or auditing skills, not during user work. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

**Purpose:** Governs where this repository spends effort optimizing token cost, and what
counts as a valid token claim. Companion to [`_common/scripts/token-economy.py`](scripts/token-economy.py),
the instrument that produces the numbers this document is derived from.

**Read when:** Proposing a token/cost optimization, citing a token figure in a PR or audit,
attributing a cost increase to a repo change, or deciding whether TES/UQS/the 70% context
trigger should gate anything.

**Source:** `token-economy.py` run against 59 sessions of this repo's transcripts,
2026-07-20..2026-08-18, deduped globally by `requestId`. Re-run the script before citing any
number below as current — this document states the *rules*; the script is the *measurement*.

---

## 1. What is worth optimizing, and what is not

By raw token count the corpus splits
`cache_read 98.3% / cache_creation 1.3% / output 0.4% / input 0.004%`.

**Token counts are not costs, and this document's rules are cost rules.** Cached reads bill
at ~0.1x a fresh input token, cache writes at 1.25x (5-minute TTL) or 2x (1-hour TTL), fresh
input at 1x (Anthropic prompt-caching documentation). Re-weighting the same corpus by those
multipliers — output priced at 5x input, an **UNVERIFIED** assumption, so the sensitivity is
shown — gives:

**Snapshot notice (same rule as §2):** the table below is computed from one dated run of
`token-economy.py`, **2026-08-18**, whose TOTALS were
`cache_read 1,180,768,307 / cache_creation 15,674,068 / input 50,600 / output 4,288,202`.
Those four numbers are the table's only inputs; with the multipliers stated above, every cell
is exactly reproducible from them. The corpus is live (§3.5, §5), so a fresh run gives
slightly different totals and therefore slightly different cells — that drift is expected and
is not an error in the table. **Re-derive from a current run before citing a cell elsewhere;
do not treat these percentages as constants.**

| weighting | cache_read | cache_creation | output |
|---|---|---|---|
| raw tokens | 98.3% | 1.3% | 0.4% |
| cost, 1h TTL (write 2x, output 5x) | 69.1% | 18.3% | 12.5% |
| cost, 5min TTL (write 1.25x, output 5x) | 74.2% | 12.3% | 13.5% |
| cost, 1h TTL, output 3x | 72.7% | 19.3% | 7.9% |
| cost, 1h TTL, output 10x | 61.4% | 16.3% | 22.3% |

Cache reads remain the dominant cost in every scenario (61-74%), so §2 stands. But the
`cache_creation` share that body size actually touches is **12-19% of cost, not 1.3%** — an
order of magnitude larger than the raw-token figure suggests. Any claim of the form
"X is only N% of spend" derived from raw token counts is inadmissible under §3 unless it has
been re-weighted.

**The two levers are a product, not a pair.** On-demand content is written once and then
re-read every subsequent turn, so a token loaded into context costs
`2.0 + 0.1 x (turns remaining)`:

| turns remaining when loaded | effective cost per token |
|---|---|
| 0 | 2.0x |
| 10 | 3.0x |
| 50 | 7.0x |
| 100 | 12.0x |
| 200 | 22.0x |

A 6,400-token SKILL.md body read with 100 turns still to run costs ~76,800 token-equivalents
— **12x its nominal size**. Body size therefore matters in proportion to session length, and
shortening sessions (§2) reduces the value of compressing bodies, while long sessions
multiply it.

**Rule:** Do not justify SKILL.md/`_common/` body compression with the raw-token 1.3%
figure, and do not dismiss it with that figure either. Compression is worth doing when the
content is loaded early in long sessions, and close to worthless when sessions are short —
so **fix session length first (§2), then re-measure before deciding whether compression is
still worth the risk of content loss.** The prior token-headroom campaign (see the
`project_skill_token_headroom` memory) stopped on the judgement that further compression
risked losing content for diminishing gain; that judgement is not overturned here, but the
ceiling it was weighed against was understated.

**Consequence of violating this rule:** a cost claim is made on raw token shares, and is
wrong by roughly an order of magnitude in either direction — either chasing a lever
dismissed as 1.3% when it is 12-19%, or compressing content in sessions short enough that
the saving never materialises.

---

## 2. The primary lever: session length

**Snapshot notice:** every figure in this section is `token-economy.py --redact-sessions`
output from the run dated **2026-08-18** (59 sessions, 5,359 deduped turns). The transcript
corpus is live and grows continuously (§3.5, §5) — a re-run will produce slightly different
values. Treat the numbers below as of that run, not as a fixed constant; re-derive before
citing them elsewhere.

Cache-read concentrates in long sessions, not large SKILL.md bodies:

- Top 5 of 59 sessions = **49.9%** of all cache_read. The single largest session (698
  turns) alone = **27.5%** of the whole corpus.
- Turns beyond session-local index 100 = **49.5%** of all cache_read, contributed by 15 of
  59 sessions (the 101-200 and 201+ length buckets below: 10 + 5 sessions).
- Median session length is **67 turns** — well under the 100-turn mark where longtail cost
  starts dominating.

Session length, not skill body size, is the dominant cost variable this repo can influence.

**Cost per turn rises with session length — measured, not assumed.** Median cache_read
per turn, bucketed by total session length (59 sessions, deduped by `requestId`; from
`token-economy.py`'s `== SESSION LENGTH ECONOMICS ==` output):

| session length (turns) | sessions | median turns | median cache_read/turn | share of all cache_read |
|---|---|---|---|---|
| 1-25    |  7 |  16 |  75,317 |  0.7% |
| 26-50   | 12 |  42 | 110,512 |  4.7% |
| 51-100  | 25 |  73 | 138,402 | 22.4% |
| 101-200 | 10 | 128 | 197,168 | 22.4% |
| 201+    |  5 | 239 | 262,996 | 49.9% |

A 201+ turn session pays **3.5x** per turn what a <=25-turn session pays. Because total
cost is turns x per-turn cost, and per-turn cost itself climbs with turn count, total cost
grows **superlinearly (roughly quadratically) in session length, not linearly** — a session
twice as long costs more than twice as much.

The bucket table above compares *different* sessions, so on its own it is confounded: it is
equally consistent with "heavy sessions simply run longer" (a selection effect), which would
mean splitting relocates cost rather than reducing it. Two further measurements settle this
in favour of causation (same script section):

1. **Growth is within-session and universal.** Across all 47 sessions of >=40 turns, mean
   cache_read per turn in the third quarter of turns (of 4 equal turn-order chunks) exceeds
   the first quarter in **47 of 47** — median **1.81x**, minimum 1.39x, maximum 2.77x. There
   is no counterexample in the corpus.
2. **Long sessions do not start expensive.** Grouped by the length they eventually reached,
   median mean-cache_read-per-turn over each session's **first 20 turns only** is 89,624
   (41-100 turns), 86,857 (101-200), and 95,042 (201+) — indistinguishable, and not
   monotonic. Sessions that became expensive were not heavy from the outset; they became
   expensive by running long.

So the cost is caused by session length, not merely correlated with it. Splitting the same
total work across shorter sessions genuinely reduces spend rather than moving it.
Median-based, order-of-magnitude estimates (**not measured splits** — no session was
actually run both ways to confirm):

- one 200-turn session ~ 200 x 262,996 ~ **52.6M**
- two 100-turn sessions ~ 2 x 100 x 197,168 ~ **39.4M** (-25%)
- four 50-turn sessions ~ 4 x 50 x 110,512 ~ **22.1M** (-58%)

**Compaction is not the backstop — it is reactive and pays the peak before it fires.**
Inside the largest session (698 turns), mean cache_read per turn by decile runs 139,598 /
289,379 / 426,363 / 564,072 / 719,171 / 881,738 / 415,159 / 243,802 / 411,219 / 565,165. The
drop at decile 7-8 is compaction firing — but consumption climbs again afterward, and the
peak (decile 6, 881,738/turn) was already paid before compaction triggered. A rule that
waits for compaction to act is a rule that pays the peak every time; a rule tied to a turn
count acts before the peak is reached.

**Rule:** Close a session and hand off (`_common/HANDOFF.md`) at or before **turn ~50**, not
at turn 100 and not by waiting for compaction to trigger. Turn ~50 is the last band still
inside the cheaper half of the table above (110,512/turn at the 26-50 bucket) — continuing
past it walks straight into the 51-100 bucket, where per-turn cost is already 25% higher and
where 25 of 59 sessions (the largest single bucket) already live. A session under ~50 turns
is unremarkable; a session crossing 50 should be evaluated for a handoff, and a session
crossing 100 should be treated as already late.

**Consequence of violating this rule:** every turn spent past the ~50-turn boundary is spent
at a strictly higher marginal cache_read rate than the same turn would cost in a fresh
session (measured: 110,512 -> 138,402 -> 197,168 -> 262,996 per-turn as buckets rise), and
letting sessions run to compaction means paying a peak (up to 881,738/turn, observed) that a
turn-count-based handoff would have avoided entirely. This compounds the same concentration
`token-economy.py`'s P1/P2 findings already flag (`TE-CONCENTRATION`, `TE-LONGTAIL`).

---

## 2b. When you do cut: the removal order, and what is never removed

§1 and §2 decide *whether* to compress. This section governs *how*, and exists because the previous
headroom campaign lost facts to compression rather than to any measurement error
(`project_skill_token_headroom`). A budget without a stated removal order does not shrink content — it
shrinks whatever the compressor noticed last, and what a compressor notices last is the short clause.

**Budget is a partition, not a ceiling.** State the parts before cutting, so a cut is charged to a named
line rather than taken from wherever it is easiest:

| Line | Holds |
|---|---|
| `instruction` | contract, rules, gates — the behavior the file exists to fix |
| `state` | task, scope, and what has already been decided |
| `core_evidence` | the claims the instruction depends on |
| `exception` | prohibitions, negations, carve-outs, units, deadlines, thresholds |
| `citation` | pointers back to the authority for each claim |
| `output_reserve` | room for the response itself |

`exception` is a **reserved line, not a residual**. It is the first thing a summarizer drops — it reads as
detail — and the last thing that can be reconstructed from what remains, because nothing left in the text
implies it was ever there.

**Removal order.** When the content exceeds the budget, remove in this order and stop as soon as it fits:

1. **Exact duplicates** — the same claim stated twice in the same scope.
2. **Redundant support for a claim already carried** — a second, weaker source for a point the primary
   source already settles. Verify it is the *same* claim first (see below).
3. **Examples** — shrink to one, then to zero. An example is an aid to the rule, never the rule.
4. **Detail replaced by a pointer** — move the body to `reference/` and leave the load-bearing sentence plus
   the path. This is a relocation, not a deletion, and only counts if the pointer is actually reachable.
5. **Split the unit** — one file becomes two, each with its own trigger.
6. **Decline** — report that the content does not fit under the stated bound, and what was left out. Not
   fitting is a finding, not a failure to be hidden by cutting into the floor.

**Floors — never cut to make something fit.** Cutting into any of these is a defect regardless of the
saving:

- **`exception` content**: prohibitions, negations ("never", "do not", "unless"), numeric bounds, units,
  effective dates, and thresholds. A rule that survives without its exception is a *different rule*, and it
  reads as correct.
- **`core_evidence` before `examples`.** Deleting the reason and keeping the illustration is the most common
  form of this failure.
- **The authority a claim rests on.** A claim compressed away from its citation becomes unfalsifiable, and
  the next editor cannot tell whether it was ever verified.
- **Contract-bearing language** — thresholds, modes, safety rules, handoff contracts, and output
  requirements stay explicit (`nexus` Core Rule #4).

**Rung 2 requires an identity check, not a similarity check.** Two passages that look like the same claim
may differ in scope, authority, or applicability — measured on this repo, **2 of 4** proposed
deduplications were false positives that would have removed distinct content
(`feedback_dedup_verify_by_merge`). Before removing either, verify the merged result loses no net line and
no condition; if the two differ in *when* they apply or *who* they bind, they are not duplicates.

**Verify by retention, not by length.** A compression is accepted when the preserved categories survive it,
not when the file got shorter. Check each `exception` item present before the cut is still present after,
by reading for it specifically — a diff shows what left, but only a checklist shows whether what left
mattered.

**Consequence of violating this rule:** the file gets shorter and quietly weaker. The loss is undetectable
by re-reading the result, because a rule stripped of its exception is fluent, plausible, and wrong only in
the cases it was written for.

---

## 3. Measurement hygiene — required of any future token claim in this repo

Any token/cost figure cited in a PR, audit, or `_common/` doc must satisfy all of the
following, or be labeled as not satisfying them:

1. **Global `requestId` dedup, not per-file.** The same API response is written to more
   than one `.jsonl` file; a per-file dedup overcounts. Dedup across the whole corpus first.
2. **Never sum `thinking_tokens` into a total.** It is a subset of `output_tokens`
   (`output_tokens_details.thinking_tokens`), not an independent quantity. Report it only as
   "N% of output," never added on top.
3. **Declare subset-vs-independent for every quantity cited**, not only thinking tokens.
   State explicitly which of `input` / `cache_creation` / `cache_read` / `output` a number
   belongs to before combining it with anything else.
4. **Label any `char_count / 3.5` figure as an unverified proxy.** No offline tokenizer
   exists for Claude models in this repo. `lint-frontmatter.py`'s S2 check and any similar
   estimate must carry "(estimate, unverified)" or equivalent — never presented as a
   measured token count.
5. **Handle the live-corpus self-pollution problem.** The transcript corpus grows while it
   is being measured, because the measuring session runs inside the measured directory
   (observed: +6.7M tokens / +0.58% during one 30-minute measurement run). Any report citing
   an exact total must either snapshot the file list before running the script or state the
   run's own contribution is included and therefore the total is a lower bound as of
   snapshot time, not a fixed fact.

**Consequence of violating this rule:** the figure is not admissible as evidence in a PR
description, audit finding, or `_common/` doc — it must be re-derived from a fresh
`token-economy.py` run satisfying all five points before being cited again.

---

## 4. Attribution rule: check CLI version before blaming a repo change

The always-on prefix cost (turn-0 cache_read/cache_creation) is CLI-version-determined, not
repo-content-determined:

- Turn-0 warm cache_read is near-constant *within* a CLI version and steps only at version
  boundaries (2.1.227 -> single value 25,183; 2.1.234 -> single value 27,835).
- The largest observed step (+2,102 tokens at 2026-08-18T01:35, CLI 2.1.234) **preceded**
  the `_common/` commits a prior analysis had blamed for it, by 8-10 hours. The attribution
  was backwards.
- Cold-start total prefix has not grown over the measured window: median 72,735 at CLI
  2.1.215 vs. 67,855 at 2.1.234 — flat to slightly down.

**Rule:** Before attributing any always-on prefix increase to a repo/`_common/` change, run
`token-economy.py` and compare the turn-0 figures grouped by `version` (the "ALWAYS-ON
PREFIX" section of its output). If the step in cost aligns with a CLI version boundary and
not with a commit timestamp in this repo, the correct attribution is the CLI release, not
the repo change. Falsification procedure: find the timestamp of the suspected commit and
the timestamp of the nearest CLI version step in the script's per-version breakdown; if the
version step predates the commit, the commit is cleared.

**Consequence of violating this rule:** a repeat of the exact misattribution already made
once in this repo — reverting or trimming a `_common/` file that did not cause the cost
increase, while the actual cause (a CLI release) goes unaddressed.

---

## 5. Standing limits — what this repo cannot measure

State these once here rather than re-discovering them per audit:

- **No per-skill cost figure is derivable.** `attributionSkill` is null on ~65% of records
  and its null rate is version-biased. It marks which skill was active, never what that
  skill's SKILL.md cost in tokens. Do not construct or cite a per-skill cost ranking from
  this data.
- **Sub-agent internal cost is unrecoverable.** `isSidechain` is `false` on every record
  despite 255 observed `Agent` tool_use spawns in the window. Sub-agent token spend must be
  reported as an event count (spawns), never estimated as tokens.
- **No offline tokenizer exists for Claude models.** Any repo-text token figure is a
  `char_count / 3.5` proxy (see §3.4), never a measurement of what the API actually
  tokenizes.
- **The corpus is live and growing during measurement.** There is no way to get a frozen
  snapshot from live session data short of copying the `.jsonl` files aside before running
  the script (see §3.5).

**What would settle these, if it changes:** a future CLI release that sets `isSidechain`
correctly on sub-agent records would unlock recoverable sub-agent cost; a non-null,
non-version-biased `attributionSkill` field would unlock per-skill attribution; neither
exists today, and no workaround inside this repo substitutes for them.

---

## 6. Disposition of TES / UQS / the 70% context trigger

All three are formulas defined in `_common/HARNESS_EVOLUTION.md` and
`nexus/reference/context-strategy.md` with zero implementing code anywhere in the repo
(`grep -rl "CES\|TES\|UQS" **/*.py` returns nothing).

- **TES** (`output_information_tokens / total_tokens_consumed`, HARNESS_EVOLUTION.md:55) —
  no code computes `output_information_tokens`; it is not a field this repo's transcripts
  expose or derive.
- **UQS** (`Σ (normalized_agent_score × weight)`, HARNESS_EVOLUTION.md:56) — depends on
  per-agent evaluator scores that are never persisted, so it has no data source today.
- **The 70% context-usage trigger** (`nexus/reference/context-strategy.md:200`,
  `handoff` fallback trigger at `:221`) — no counting mechanism exists to know current
  context usage as a percentage; the 1,000-2,000 token handoff target it feeds has never
  been measured against actual handoff sizes.

**Disposition: applied.** All three items below are now in the corpus — the 70% trigger is gone
from `nexus/reference/context-strategy.md:200`, and `HARNESS_EVOLUTION.md` marks TES
`specified, not implemented`, drops it from the grading band, and removes it from the
`CES/TES` rollback and evaluation-ladder thresholds. What follows is the reasoning, kept
because the *rule* it establishes outlives the three fixes: **a formula with no data source
is never presented with a grade band or wired into a gate.** Re-apply it to the next metric,
do not re-execute the three fixes.
- Replace the 70% context-usage trigger with the turn-index rule in §2 (hand off at or
  before turn ~50; past 100 is already late), which `token-economy.py` can actually check
  via `TE-LONGTAIL`. A percentage of an unmeasured
  quantity is not an actionable trigger; a turn index in an existing transcript is.
- Retire TES. Its numerator has no data source in this repo and none is planned; keeping an
  unimplemented formula in a reference doc invites citing it as if it were computed.
- Do not retire the UQS *name* (CES's `User_Satisfaction` term and Nexus quality grading
  already reference it structurally), but its formula must not be presented as computed
  until an evaluator pipeline actually persists `normalized_agent_score` per agent. Mark it
  in `HARNESS_EVOLUTION.md` as "specified, not implemented" until that exists.

**Why this mattered enough to fix:** between this section being written and being applied, an
audit found the `HARNESS_EVOLUTION.md` hard constraint *"if CES or TES drops more than 0.10,
rollback immediately"* still live — a guard that reads as covering two metrics while one of
them can never fire. That is the failure mode in general form: an unmeasurable term inside a
gate does not merely fail to help, it makes the gate *look* stronger than it is. A metric that
nothing computes must be labelled at every site that cites it, not only at the site that
defines it.

---

## Summary table

| # | Rule | Forcing evidence | Consequence if violated |
|---|------|-------------------|--------------------------|
| 1 | Never argue body size from raw token shares; fix session length first, then re-measure | cache_creation is 1.3% of tokens but 12-19% of cost; a loaded token costs 2.0 + 0.1 x turns-remaining (12x at 100 turns) | A cost claim wrong by ~an order of magnitude, in either direction |
| 2 | Hand off at or before turn ~50; past 100 is already late | per-turn cost 110,512 (26-50) -> 138,402 (51-100) -> 262,996 (201+); within-session Q3>Q1 in 47/47 sessions; first-20-turn cost equal regardless of eventual length | Every later turn billed at a strictly higher marginal rate; compaction peak (881,738/turn observed) paid instead of avoided |
| 2b | Cut in the stated order; never cut into `exception`, evidence-before-examples, or a claim's authority; verify by retention, not by length | the prior headroom campaign lost facts to compression, not to mismeasurement; 2 of 4 proposed dedups were false positives | The file gets shorter and quietly weaker — a rule stripped of its exception reads as correct |
| 3 | 5-point measurement hygiene checklist | dedup, thinking-subset, proxy-labeling, live-corpus findings | Figure inadmissible as cited evidence |
| 4 | Check CLI version before blaming a repo change | +2,102 step preceded blamed commit by 8-10h | Repeat of an already-made misattribution |
| 5 | State standing limits, don't re-derive them | isSidechain always false; attributionSkill 65% null; no tokenizer | Wasted re-investigation of known dead ends |
| 6 | Retire 70%/TES; mark UQS unimplemented | zero implementing code for any of the three | Next reader treats unimplemented formulas as live gates |

---

## How this is run

`python3 _common/scripts/token-economy.py --severity warning` — run manually before citing
any figure in this doc, and automatically as step 3b of the 30-day self-audit routine
(`_common/HARNESS_EVOLUTION.md` § Evaluation Cycle). A P0 (`TE-INTEGRITY`) finding from that
run means the transcript data itself is broken (a billed record lost its `requestId`/usage,
or duplicate copies disagree) — fix the data problem before trusting any other number from
that run; P1/P2 findings are the cost signals this document is built on.

**Caveat for pasted output:** default output (text or `--json`) prints full session UUIDs,
which locate a local transcript file — do not paste it into a commit message or shared doc.
Pass `--redact-sessions` first; that form replaces every UUID with a stable short index
(`session-01`, ...) and is the one safe to paste.

---

## Open questions

- **Does a per-CLI-version turn-0 baseline need to be re-captured after every CLI bump, or
  can §4's falsification procedure run against whichever versions are present in the current
  window?** Settled by: confirming whether `token-economy.py`'s by-version breakdown remains
  populated as old sessions age out of the transcript retention window; if old versions
  disappear before a new one accumulates enough turn-0 samples, the comparison in §4 loses
  its baseline.
- **What turn-index threshold should replace "~100" as a hard number, if one is ever
  needed?** Settled by: tracking whether `TE-LONGTAIL`'s fixed threshold (currently 100,
  40% share) continues to hold as more sessions accumulate past the current 59-session
  window — this document uses the observed value, not a re-derived one, and should be
  revisited once the window roughly doubles.
