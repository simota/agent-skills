#!/usr/bin/env python3
"""
Measure token economy across Claude Code session transcripts for this repository.

Reads the JSONL session transcripts written by Claude Code under
`~/.claude/projects/<project-dir>/*.jsonl` and reports where cache/input/output
tokens actually go: totals, session concentration, the always-on prefix cost
per CLI version, and integrity checks on the dedup assumption itself.

Data model (verified against the live transcript corpus, do not re-derive):

  1. Only records with `type == "assistant"` carry usage, at `message.usage`.
  2. `requestId` repeats: the same API response is written to the log more than
     once, with IDENTICAL usage. Dedup is by `requestId` and MUST be GLOBAL
     ACROSS ALL FILES -- a requestId can appear in more than one file, and a
     per-file dedup overcounts.
  3. `output_tokens_details.thinking_tokens` is a SUBSET of `output_tokens`.
     It must NEVER be added into a total; it is reported as a declared subset
     with its share of output.
  4. Non-overlapping total = cache_read_input_tokens + cache_creation_input_tokens
     + input_tokens + output_tokens.
  5. `isSidechain` is false on every record even though `Agent` tool_use calls
     occur -- sub-agent internal cost is not recoverable from this transcript.
     Agent spawns are counted as an independent event counter, never as tokens.
  6. `attributionSkill` is null on a majority of records and its null-rate
     varies by CLI `version`. It indicates which skill was active, not what a
     SKILL.md cost -- never presented as a per-skill cost here.
  7. A small number of assistant records are synthetic interruption placeholders,
     not billed API calls: `message.id` does not start with `msg_`, or every
     usage field is zero together with `stop_reason == "stop_sequence"` and no
     `requestId`. These are EXCLUDED from the corpus before any total or
     integrity check runs, and counted separately as `skipped_synthetic` -- they
     must never trigger TE-INTEGRITY, and never be silently folded into "missing".

One file == one session: `sessionId` on every assistant record equals the
`.jsonl` filename stem (verified, 0 mismatches across the corpus). "Turn index"
below is a session-local index: assistant records within one session, deduped
by requestId, ordered by `timestamp`, 0-based.

Findings (each paired with an action via the exit code):
  P0 TE-INTEGRITY     a genuine anomaly on a BILLED record only (synthetic
                       interruption placeholders are excluded first, see data
                       model point 7): a requestId with conflicting usage
                       across copies, or a billed record with no requestId.
  P1 TE-CONCENTRATION any single session > 15% of the window's total cache_read.
  P2 TE-LONGTAIL       turns beyond index 100 (session-local) > 40% of the
                       window's total cache_read.
  P3 TE-ATTRIBUTION    attributionSkill null-rate > 90% for the newest CLI
                       version present in the window.

Severity tiers:
  --severity warning  (default)  print findings, exit 0
  --severity error    exit 1 if any P0/P1 finding is reported

Usage:
  python3 _common/scripts/token-economy.py [--project-dir NAME]
                                            [--repo-root PATH]
                                            [--severity warning|error]
                                            [--json]
                                            [--redact-sessions]

Output safety: default text and `--json` output both print full session UUIDs
(SESSION CONCENTRATION rows, TE-CONCENTRATION findings, JSON top_sessions). A
UUID locates a local transcript file, so that output is NOT the form to paste
into a commit message or shared doc. Pass `--redact-sessions` to replace every
UUID with a stable short index (`session-01`, ...) before printing -- that
form is safe to paste. Redaction is off by default; the operator still needs
the real id locally to find the transcript.

Exit codes:
  0  no blocking findings under the chosen severity
  1  blocking findings present
  2  internal error (bad path, unreadable transcripts, etc.)
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

DEFAULT_PROJECT_DIR = "-Users-simota--claude-skills"
LONGTAIL_INDEX = 100
LONGTAIL_SHARE_THRESHOLD = 0.40
CONCENTRATION_SHARE_THRESHOLD = 0.15
ATTRIBUTION_NULL_THRESHOLD = 0.90
TOP_N_SESSIONS = 5
TAIL_INDICES = (25, 50, 100, 200)
SESSION_LENGTH_BUCKETS = ((1, 25), (26, 50), (51, 100), (101, 200), (201, None))
GROWTH_MIN_TURNS = 40
ONSET_TURNS = 20
ONSET_BUCKETS = ((41, 100), (101, 200), (201, None))


@dataclass
class Finding:
    item: str
    priority: str
    message: str


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)

    def add(self, item: str, priority: str, message: str) -> None:
        self.findings.append(Finding(item, priority, message))

    def by_priority(self, p: str) -> list[Finding]:
        return [f for f in self.findings if f.priority == p]


@dataclass
class Turn:
    session: str
    timestamp: str
    version: str | None
    attribution_null: bool
    input_tokens: int
    cache_creation: int
    cache_read: int
    output_tokens: int
    thinking_tokens: int


def is_synthetic_record(message: dict, reqid: str | None) -> bool:
    """True if `message` is a synthetic interruption placeholder, not a billed
    API call (data model point 7 in the module docstring). Two independent
    signals, either one is sufficient:
      - `message.id` does not start with `msg_` (billed responses always do).
      - every usage field is zero AND stop_reason == "stop_sequence" AND there
        is no requestId (the shape of an interrupted-turn placeholder).
    """
    msgid = message.get("id") or ""
    if not msgid.startswith("msg_"):
        return True
    usage = message.get("usage")
    if usage is not None:
        all_zero = (
            usage.get("input_tokens", 0) == 0
            and usage.get("cache_creation_input_tokens", 0) == 0
            and usage.get("cache_read_input_tokens", 0) == 0
            and usage.get("output_tokens", 0) == 0
        )
        if all_zero and message.get("stop_reason") == "stop_sequence" and reqid is None:
            return True
    return False


def version_key(v: str | None) -> tuple:
    if not v:
        return (-1,)
    parts = []
    for p in v.split("."):
        try:
            parts.append(int(p))
        except ValueError:
            parts.append(0)
    return tuple(parts)


def load_turns(project_dir: Path, report: Report) -> tuple[list[Turn], int, int, int]:
    """Return (deduped turns, missing_usage_or_reqid count, agent_spawn count,
    skipped_synthetic count)."""
    files = sorted(project_dir.glob("*.jsonl"))
    if not files:
        print(f"error: no .jsonl transcripts found in {project_dir}", file=sys.stderr)
        sys.exit(2)

    seen: dict[str, tuple] = {}  # requestId -> (usage_key, turn)
    turns: list[Turn] = []
    missing = 0
    agent_spawns = 0
    skipped_synthetic = 0

    for fp in files:
        with fp.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("type") != "assistant":
                    continue

                message = rec.get("message") or {}
                for block in message.get("content") or []:
                    if isinstance(block, dict) and block.get("type") == "tool_use" \
                            and block.get("name") == "Agent":
                        agent_spawns += 1

                reqid = rec.get("requestId")

                # Classify BEFORE the integrity check: a synthetic interruption
                # placeholder was never a billed API call, so it cannot be
                # "missing" data from one -- it is excluded from the corpus
                # entirely and counted separately (data model point 7).
                if is_synthetic_record(message, reqid):
                    skipped_synthetic += 1
                    continue

                usage = message.get("usage")
                if usage is None or reqid is None:
                    missing += 1
                    continue

                usage_key = (
                    usage.get("input_tokens", 0),
                    usage.get("cache_creation_input_tokens", 0),
                    usage.get("cache_read_input_tokens", 0),
                    usage.get("output_tokens", 0),
                )

                if reqid in seen:
                    if seen[reqid][0] != usage_key:
                        report.add("TE-INTEGRITY", "P0",
                                   f"requestId {reqid} has conflicting usage across "
                                   f"copies: {seen[reqid][0]} vs {usage_key}")
                    continue

                otd = usage.get("output_tokens_details") or {}
                turn = Turn(
                    session=rec.get("sessionId") or fp.stem,
                    timestamp=rec.get("timestamp") or "",
                    version=rec.get("version"),
                    attribution_null=rec.get("attributionSkill") is None,
                    input_tokens=usage.get("input_tokens", 0),
                    cache_creation=usage.get("cache_creation_input_tokens", 0),
                    cache_read=usage.get("cache_read_input_tokens", 0),
                    output_tokens=usage.get("output_tokens", 0),
                    thinking_tokens=otd.get("thinking_tokens", 0),
                )
                seen[reqid] = (usage_key, turn)
                turns.append(turn)

    if missing:
        report.add("TE-INTEGRITY", "P0",
                   f"{missing} billed assistant record(s) missing requestId and/or "
                   f"usage (synthetic placeholders already excluded)")

    return turns, missing, agent_spawns, skipped_synthetic


def compute(turns: list[Turn]) -> dict:
    totals = {
        "input": sum(t.input_tokens for t in turns),
        "cache_creation": sum(t.cache_creation for t in turns),
        "cache_read": sum(t.cache_read for t in turns),
        "output": sum(t.output_tokens for t in turns),
    }
    grand_total = sum(totals.values())
    thinking_total = sum(t.thinking_tokens for t in turns)

    by_session: dict[str, list[Turn]] = {}
    for t in turns:
        by_session.setdefault(t.session, []).append(t)
    for lst in by_session.values():
        lst.sort(key=lambda t: t.timestamp)

    session_cache_read = {
        sid: sum(t.cache_read for t in lst) for sid, lst in by_session.items()
    }
    session_order = sorted(session_cache_read.items(), key=lambda kv: -kv[1])
    total_cache_read = totals["cache_read"] or 1
    top_n = session_order[:TOP_N_SESSIONS]
    top_n_share = sum(v for _, v in top_n) / total_cache_read

    tail_shares = {}
    for n in TAIL_INDICES:
        tail_sum = 0
        for lst in by_session.values():
            for idx, t in enumerate(lst):
                if idx > n:
                    tail_sum += t.cache_read
        tail_shares[n] = tail_sum / total_cache_read

    by_version: dict[str, dict[str, list[int]]] = {}
    for lst in by_session.values():
        if not lst:
            continue
        t0 = lst[0]
        v = t0.version or "unknown"
        bucket = by_version.setdefault(v, {"cold_creation": [], "warm_read": []})
        if t0.cache_read == 0:
            bucket["cold_creation"].append(t0.cache_creation)
        else:
            bucket["warm_read"].append(t0.cache_read)

    versions_present = sorted({t.version for t in turns if t.version}, key=version_key)
    newest_version = versions_present[-1] if versions_present else None
    newest_turns = [t for t in turns if t.version == newest_version]
    newest_null_rate = (
        sum(1 for t in newest_turns if t.attribution_null) / len(newest_turns)
        if newest_turns else 0.0
    )

    # ALWAYS-ON vs ON-DEMAND (D2): the always-on prefix is *re-read on every
    # turn* of a session, not paid once -- that repetition is the entire reason
    # it is called always-on. Counting only turn-0's own usage (as a prior
    # version of this script did) understates it by the session's turn count.
    # This is an ESTIMATE, not a measured field: it assumes session_prefix
    # (below) stays constant across the whole session. Both quantities are
    # shares of cache_read specifically (what they partition), not of
    # grand_total.
    always_on_cache_read = 0
    for lst in by_session.values():
        if not lst:
            continue
        t0 = lst[0]
        if t0.cache_read > 0:
            session_prefix = t0.cache_read
        else:
            # cold start: turn 0 creates the cache rather than reading it: use
            # the smallest non-zero cache_read later in the session as the
            # estimated steady-state prefix, or 0 if the session never warmed.
            nonzero_reads = [t.cache_read for t in lst if t.cache_read > 0]
            session_prefix = min(nonzero_reads) if nonzero_reads else 0
        always_on_cache_read += session_prefix * len(lst)
    on_demand_cache_read = totals["cache_read"] - always_on_cache_read

    return {
        "totals": totals,
        "grand_total": grand_total,
        "thinking_total": thinking_total,
        "session_count": len(by_session),
        "session_order": session_order,
        "session_turns": {sid: len(lst) for sid, lst in by_session.items()},
        "median_session_turns": median([len(lst) for lst in by_session.values()]),
        "top_n": top_n,
        "top_n_share": top_n_share,
        "tail_shares": tail_shares,
        "by_version": by_version,
        "newest_version": newest_version,
        "newest_null_rate": newest_null_rate,
        "total_cache_read": totals["cache_read"],
        "always_on_cache_read": always_on_cache_read,
        "on_demand_cache_read": on_demand_cache_read,
    }


def stats(values: list[int]) -> dict:
    if not values:
        return {"n": 0, "min": 0, "max": 0, "mean": 0.0}
    return {
        "n": len(values),
        "min": min(values),
        "max": max(values),
        "mean": sum(values) / len(values),
    }


def median(values: list) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2


def mean_cache_read(chunk: list[Turn]) -> float:
    if not chunk:
        return 0.0
    return sum(t.cache_read for t in chunk) / len(chunk)


def split_chunks(lst: list, k: int) -> list[list]:
    """Split lst into k contiguous chunks as evenly as possible, remainder
    distributed to the first chunks (same convention as numpy.array_split)."""
    n = len(lst)
    base = n // k
    rem = n % k
    chunks = []
    idx = 0
    for i in range(k):
        size = base + (1 if i < rem else 0)
        chunks.append(lst[idx:idx + size])
        idx += size
    return chunks


def bucket_for_length(n: int, buckets: tuple) -> tuple | None:
    for lo, hi in buckets:
        if hi is None:
            if n >= lo:
                return (lo, hi)
        elif lo <= n <= hi:
            return (lo, hi)
    return None


def compute_session_length_economics(turns: list[Turn]) -> dict:
    """SESSION LENGTH ECONOMICS: does cost per turn rise with how long a
    session runs, and is that growth within-session (causal) or merely a
    selection effect (heavy sessions simply run longer)? Four measurements,
    all from the same deduped turns this module already builds -- no second
    data source.
    """
    by_session: dict[str, list[Turn]] = {}
    for t in turns:
        by_session.setdefault(t.session, []).append(t)
    for lst in by_session.values():
        lst.sort(key=lambda t: t.timestamp)

    total_cache_read = sum(t.cache_read for t in turns) or 1

    # 1. Median cache_read/turn by total session length. Per session first
    # (its own mean cache_read/turn), then median of those across the bucket
    # -- one data point per session, not one per turn, so a long session
    # cannot dominate a bucket's median the way it dominates a raw sum.
    bucket_data = {b: {"turn_counts": [], "per_turn_means": [], "cache_read_sum": 0}
                   for b in SESSION_LENGTH_BUCKETS}
    for lst in by_session.values():
        n = len(lst)
        b = bucket_for_length(n, SESSION_LENGTH_BUCKETS)
        if b is None:
            continue
        session_cache_read = sum(t.cache_read for t in lst)
        bucket_data[b]["turn_counts"].append(n)
        bucket_data[b]["per_turn_means"].append(session_cache_read / n)
        bucket_data[b]["cache_read_sum"] += session_cache_read

    length_buckets = []
    for lo, hi in SESSION_LENGTH_BUCKETS:
        d = bucket_data[(lo, hi)]
        length_buckets.append({
            "range": f"{lo}-{hi}" if hi is not None else f"{lo}+",
            "sessions": len(d["turn_counts"]),
            "median_turns": median(d["turn_counts"]),
            "median_cache_read_per_turn": median(d["per_turn_means"]),
            "share_of_total_cache_read": d["cache_read_sum"] / total_cache_read,
        })

    # 2. Within-session growth: split each session (>= GROWTH_MIN_TURNS turns)
    # into 4 contiguous chunks by turn order; ratio = chunk-3 mean / chunk-1
    # mean cache_read-per-turn. A session whose first chunk never reads cache
    # (mean == 0, pure cold-start creation) has no defined ratio and is
    # excluded, not zero-filled.
    growth_ratios = []
    growth_excluded = 0
    for lst in by_session.values():
        if len(lst) < GROWTH_MIN_TURNS:
            continue
        chunks = split_chunks(lst, 4)
        q1_mean = mean_cache_read(chunks[0])
        q3_mean = mean_cache_read(chunks[2])
        if q1_mean <= 0:
            growth_excluded += 1
            continue
        growth_ratios.append(q3_mean / q1_mean)

    growth = {
        "n": len(growth_ratios),
        "excluded_zero_q1": growth_excluded,
        "n_exceeding_1x": sum(1 for r in growth_ratios if r > 1.0),
        "median_ratio": median(growth_ratios),
        "min_ratio": min(growth_ratios) if growth_ratios else 0.0,
        "max_ratio": max(growth_ratios) if growth_ratios else 0.0,
    }

    # 3. Onset check: mean cache_read/turn over each session's first
    # ONSET_TURNS turns only, grouped by the length the session eventually
    # reached. Distinguishes "became expensive" (flat here, rises later) from
    # "started expensive" (already high here).
    onset_data = {b: [] for b in ONSET_BUCKETS}
    for lst in by_session.values():
        n = len(lst)
        if n < ONSET_TURNS:
            continue
        b = bucket_for_length(n, ONSET_BUCKETS)
        if b is None:
            continue
        onset_data[b].append(mean_cache_read(lst[:ONSET_TURNS]))

    onset = []
    for lo, hi in ONSET_BUCKETS:
        vals = onset_data[(lo, hi)]
        onset.append({
            "range": f"{lo}-{hi}" if hi is not None else f"{lo}+",
            "sessions": len(vals),
            "median_first20_cache_read_per_turn": median(vals),
        })

    # 4. Per-decile mean cache_read/turn for the single largest session by
    # total cache_read (compaction visibility: does cost keep climbing inside
    # the one session that carries the most weight in the whole corpus?).
    largest_sid = max(by_session, key=lambda sid: sum(t.cache_read for t in by_session[sid])) \
        if by_session else None
    decile_means: list[float] = []
    if largest_sid is not None:
        decile_means = [mean_cache_read(c) for c in split_chunks(by_session[largest_sid], 10)]

    return {
        "length_buckets": length_buckets,
        "growth": growth,
        "onset": onset,
        "largest_session": largest_sid,
        "largest_session_turns": len(by_session[largest_sid]) if largest_sid else 0,
        "largest_session_decile_means": decile_means,
    }


def build_session_redaction(session_ids: set[str]) -> dict[str, str]:
    """Stable UUID -> short-index mapping, sorted so the same session id always
    gets the same index across runs (as long as the session set is unchanged)."""
    return {sid: f"session-{i + 1:02d}" for i, sid in enumerate(sorted(session_ids))}


def session_label(sid: str, redact_map: dict[str, str] | None) -> str:
    return redact_map[sid] if redact_map else sid


def evaluate_findings(stats_d: dict, report: Report,
                       redact_map: dict[str, str] | None = None) -> None:
    for sid, cr in stats_d["session_order"]:
        share = cr / (stats_d["total_cache_read"] or 1)
        if share > CONCENTRATION_SHARE_THRESHOLD:
            report.add("TE-CONCENTRATION", "P1",
                       f"session {session_label(sid, redact_map)} is {share * 100:.1f}% "
                       f"of total cache_read "
                       f"(> {CONCENTRATION_SHARE_THRESHOLD * 100:.0f}% threshold)")

    longtail_share = stats_d["tail_shares"].get(LONGTAIL_INDEX, 0.0)
    if longtail_share > LONGTAIL_SHARE_THRESHOLD:
        report.add("TE-LONGTAIL", "P2",
                   f"turns beyond index {LONGTAIL_INDEX} contribute "
                   f"{longtail_share * 100:.1f}% of total cache_read "
                   f"(> {LONGTAIL_SHARE_THRESHOLD * 100:.0f}% threshold)")

    if stats_d["newest_version"] and stats_d["newest_null_rate"] > ATTRIBUTION_NULL_THRESHOLD:
        report.add("TE-ATTRIBUTION", "P3",
                   f"attributionSkill null-rate for newest version "
                   f"{stats_d['newest_version']} is {stats_d['newest_null_rate'] * 100:.1f}% "
                   f"(> {ATTRIBUTION_NULL_THRESHOLD * 100:.0f}% threshold)")


def render_text(stats_d: dict, sle_d: dict, agent_spawns: int, missing: int, skipped_synthetic: int,
                 report: Report, redact_map: dict[str, str] | None = None) -> str:
    out = []
    t = stats_d["totals"]
    grand_total = stats_d["grand_total"]
    gt = grand_total or 1  # divide-by-zero guard for the percentage math below only

    out.append("== TOTALS ==")
    out.append(f"  cache_read       {t['cache_read']:>14,}  ({t['cache_read'] / gt * 100:5.1f}%)")
    out.append(f"  cache_creation   {t['cache_creation']:>14,}  ({t['cache_creation'] / gt * 100:5.1f}%)")
    out.append(f"  input            {t['input']:>14,}  ({t['input'] / gt * 100:5.1f}%)")
    out.append(f"  output           {t['output']:>14,}  ({t['output'] / gt * 100:5.1f}%)")
    out.append(f"  TOTAL            {grand_total:>14,}")
    out_share = (stats_d["thinking_total"] / t["output"] * 100) if t["output"] else 0.0
    out.append(f"  thinking (subset of output, NOT in total)  {stats_d['thinking_total']:>14,}  "
               f"({out_share:5.1f}% of output)")
    out.append("")

    out.append("== SESSION CONCENTRATION ==")
    out.append(f"  sessions: {stats_d['session_count']}")
    out.append(f"  median session length: {stats_d['median_session_turns']:.0f} turns")
    out.append(f"  top {TOP_N_SESSIONS} sessions by cache_read:")
    for sid, cr in stats_d["top_n"]:
        turns_n = stats_d["session_turns"][sid]
        share = cr / (stats_d["total_cache_read"] or 1) * 100
        out.append(f"    {session_label(sid, redact_map)}  turns={turns_n:<5} "
                   f"cache_read={cr:>14,}  ({share:5.1f}%)")
    out.append(f"  top {TOP_N_SESSIONS} share of total cache_read: {stats_d['top_n_share'] * 100:.1f}%")
    for n in TAIL_INDICES:
        out.append(f"  cumulative share from turns beyond index {n}: "
                   f"{stats_d['tail_shares'][n] * 100:.1f}%")
    out.append("")

    out.append("== ALWAYS-ON PREFIX (per CLI version, turn 0 of each session) ==")
    for v in sorted(stats_d["by_version"].keys(), key=version_key):
        b = stats_d["by_version"][v]
        cold = stats(b["cold_creation"])
        warm = stats(b["warm_read"])
        out.append(f"  version {v}")
        out.append(f"    cold start (cache_read==0): n={cold['n']:<3} "
                   f"cache_creation min={cold['min']:,} max={cold['max']:,} "
                   f"mean={cold['mean']:,.0f}")
        out.append(f"    warm start (cache_read>0):  n={warm['n']:<3} "
                   f"cache_read min={warm['min']:,} max={warm['max']:,} "
                   f"mean={warm['mean']:,.0f}")
    out.append("")

    out.append("== ALWAYS-ON vs ON-DEMAND (share of cache_read) ==")
    always_on = stats_d["always_on_cache_read"]
    on_demand = stats_d["on_demand_cache_read"]
    cache_read_total = stats_d["total_cache_read"] or 1
    out.append("  ALWAYS-ON = per-session prefix (turn-0 cache_read if warm, else the "
               "smallest non-zero cache_read later in the session) x that session's "
               "turn count, summed; ON-DEMAND = cache_read - ALWAYS-ON. Both are "
               "shares of cache_read (what they partition), not of TOTAL.")
    out.append(f"  ALWAYS-ON   {always_on:>14,}  ({always_on / cache_read_total * 100:5.1f}% of cache_read)")
    out.append(f"  ON-DEMAND   {on_demand:>14,}  ({on_demand / cache_read_total * 100:5.1f}% of cache_read)")
    out.append("  ESTIMATE, not measured: assumes each session's prefix stays constant "
               "across every turn of that session. If the cached prefix actually grows "
               "turn over turn (plausible, since context accumulates), this UNDERSTATES "
               "true ALWAYS-ON cost and OVERSTATES ON-DEMAND's share.")
    out.append("")

    out.append("== SESSION LENGTH ECONOMICS ==")
    out.append("  median cache_read/turn by total session length (median across sessions of "
               "each session's own mean cache_read/turn; share is of total cache_read):")
    out.append(f"  {'length (turns)':<16}{'sessions':>9}{'median turns':>14}"
               f"{'median cache_read/turn':>26}{'share of total':>16}")
    for b in sle_d["length_buckets"]:
        out.append(f"  {b['range']:<16}{b['sessions']:>9}{b['median_turns']:>14,.0f}"
                   f"{b['median_cache_read_per_turn']:>26,.0f}{b['share_of_total_cache_read'] * 100:>15.1f}%")
    out.append("")
    g = sle_d["growth"]
    out.append(f"  within-session growth (chunk-3/chunk-1 mean cache_read-per-turn over 4 equal "
               f"chunks of turn order, sessions >= {GROWTH_MIN_TURNS} turns):")
    out.append(f"    n={g['n']}  (excluded {g['excluded_zero_q1']} with zero chunk-1 mean)  "
               f"exceeding 1.0x: {g['n_exceeding_1x']}/{g['n']}")
    out.append(f"    ratio median={g['median_ratio']:.2f}x  min={g['min_ratio']:.2f}x  "
               f"max={g['max_ratio']:.2f}x")
    out.append("")
    out.append(f"  onset check -- median of each session's mean cache_read/turn over its FIRST "
               f"{ONSET_TURNS} turns, grouped by the length it eventually reached (distinguishes "
               f"\"became expensive\" from \"started expensive\"):")
    for o in sle_d["onset"]:
        out.append(f"    reached {o['range']:<8} turns: n={o['sessions']:<3}  "
                   f"median first-{ONSET_TURNS} cache_read/turn={o['median_first20_cache_read_per_turn']:>12,.0f}")
    out.append("")
    if sle_d["largest_session"] is not None:
        out.append(f"  per-decile mean cache_read/turn, single largest session by cache_read "
                   f"({session_label(sle_d['largest_session'], redact_map)}, "
                   f"{sle_d['largest_session_turns']} turns):")
        out.append("    " + " / ".join(f"{v:,.0f}" for v in sle_d["largest_session_decile_means"]))
    out.append("")

    out.append("== INTEGRITY ==")
    out.append(f"  skipped_synthetic (interruption placeholders, not billed calls): "
               f"{skipped_synthetic}")
    out.append(f"  missing requestId/usage on billed records: {missing}")
    total_turns = sum(stats_d["session_turns"].values())
    out.append(f"  deduped turns counted: {total_turns}")
    out.append(f"  Agent tool_use spawns (event count, not tokens): {agent_spawns}")
    out.append("")

    if report.findings:
        out.append(f"== FINDINGS ({len(report.findings)}) ==")
        for priority in ("P0", "P1", "P2", "P3"):
            bucket = report.by_priority(priority)
            if not bucket:
                continue
            out.append(f"[{priority}] {len(bucket)}")
            for f in bucket:
                out.append(f"  {f.item:16s} {f.message}")
    else:
        out.append("== FINDINGS ==")
        out.append("  none")

    return "\n".join(out) + "\n"


def render_json(stats_d: dict, sle_d: dict, agent_spawns: int, missing: int, skipped_synthetic: int,
                 report: Report, redact_map: dict[str, str] | None = None) -> str:
    payload = {
        "totals": stats_d["totals"],
        "grand_total": stats_d["grand_total"],
        "thinking_total": stats_d["thinking_total"],
        "session_count": stats_d["session_count"],
        "median_session_turns": stats_d["median_session_turns"],
        "top_sessions": [
            {"session": session_label(sid, redact_map),
             "turns": stats_d["session_turns"][sid], "cache_read": cr}
            for sid, cr in stats_d["top_n"]
        ],
        "top_n_share": stats_d["top_n_share"],
        "tail_shares": stats_d["tail_shares"],
        "always_on_prefix": {
            v: {
                "cold_creation": stats(b["cold_creation"]),
                "warm_read": stats(b["warm_read"]),
            }
            for v, b in stats_d["by_version"].items()
        },
        "always_on_vs_on_demand": {
            "note": "ALWAYS-ON = per-session prefix (turn-0 cache_read if warm, else "
                    "the smallest non-zero cache_read later in the session) x that "
                    "session's turn count, summed; ON-DEMAND = cache_read - "
                    "ALWAYS-ON. Both are shares of cache_read, not of grand_total. "
                    "ESTIMATE, not measured: assumes each session's prefix stays "
                    "constant across every turn. If the cached prefix actually grows "
                    "turn over turn, this UNDERSTATES ALWAYS-ON and OVERSTATES "
                    "ON-DEMAND's share.",
            "always_on_cache_read": stats_d["always_on_cache_read"],
            "on_demand_cache_read": stats_d["on_demand_cache_read"],
        },
        "session_length_economics": {
            "length_buckets": sle_d["length_buckets"],
            "growth": sle_d["growth"],
            "onset": sle_d["onset"],
            "largest_session": session_label(sle_d["largest_session"], redact_map)
            if sle_d["largest_session"] is not None else None,
            "largest_session_turns": sle_d["largest_session_turns"],
            "largest_session_decile_means": sle_d["largest_session_decile_means"],
        },
        "integrity": {
            "skipped_synthetic": skipped_synthetic,
            "missing_requestid_or_usage_on_billed": missing,
            "deduped_turns": sum(stats_d["session_turns"].values()),
            "agent_spawns": agent_spawns,
        },
        "findings": [asdict(f) for f in report.findings],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", default=DEFAULT_PROJECT_DIR,
                        help="Claude Code project directory name under "
                             "~/.claude/projects/ (default: this repo's)")
    parser.add_argument("--repo-root", default=None,
                        help="repo root, reserved for future repo-file checks "
                             "(unused by the current checks)")
    parser.add_argument("--severity", choices=("warning", "error"), default="warning")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of text")
    parser.add_argument("--redact-sessions", action="store_true",
                        help="replace session UUIDs with stable short indices "
                             "(session-01, ...) -- the safe-to-paste output form")
    args = parser.parse_args()

    projects_root = Path.home() / ".claude" / "projects"
    project_dir = Path(args.project_dir)
    if not project_dir.is_absolute():
        project_dir = projects_root / args.project_dir
    if not project_dir.is_dir():
        print(f"error: project dir not found: {project_dir}", file=sys.stderr)
        return 2

    report = Report()
    turns, missing, agent_spawns, skipped_synthetic = load_turns(project_dir, report)
    stats_d = compute(turns)
    sle_d = compute_session_length_economics(turns)
    redact_map = (build_session_redaction({t.session for t in turns})
                  if args.redact_sessions else None)
    evaluate_findings(stats_d, report, redact_map)

    if args.json:
        print(render_json(stats_d, sle_d, agent_spawns, missing, skipped_synthetic, report, redact_map))
    else:
        sys.stdout.write(render_text(stats_d, sle_d, agent_spawns, missing, skipped_synthetic,
                                      report, redact_map))

    if args.severity == "error":
        blocking = report.by_priority("P0") + report.by_priority("P1")
        return 1 if blocking else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
