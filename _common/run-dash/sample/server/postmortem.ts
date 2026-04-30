// Generates a postmortem markdown for a completed apex run.
// Spec: _common/apex-dash/POSTMORTEM.md

import * as fs from "node:fs";
import * as path from "node:path";
import { reduce, initialState } from "../src/reducer";
import type { ApexEvent, AppState, Phase } from "../src/types";
import { PHASE_ORDER } from "../src/types";

function readEvents(file: string): ApexEvent[] {
  if (!fs.existsSync(file)) return [];
  const raw = fs.readFileSync(file, "utf8");
  const lines = raw.split("\n").filter((l) => l.trim().length > 0);
  const out: ApexEvent[] = [];
  for (const line of lines) {
    try {
      out.push(JSON.parse(line) as ApexEvent);
    } catch {
      // skip bad lines
    }
  }
  return out;
}

function fold(events: ApexEvent[]): AppState {
  let s = initialState;
  for (const ev of events) s = reduce(s, ev);
  return s;
}

function fmtDuration(ms: number): string {
  if (!ms || ms < 0) return "—";
  const total = Math.floor(ms / 1000);
  const h = Math.floor(total / 3600);
  const m = Math.floor((total % 3600) / 60);
  const sec = total % 60;
  if (h > 0)
    return `${h}:${String(m).padStart(2, "0")}:${String(sec).padStart(2, "0")}`;
  return `${String(m).padStart(2, "0")}:${String(sec).padStart(2, "0")}`;
}

function diffMs(a?: string, b?: string): number {
  if (!a || !b) return 0;
  return new Date(b).getTime() - new Date(a).getTime();
}

interface Bottleneck {
  agent?: { name: string; ms: number; phase?: Phase };
  phase?: { phase: Phase; ms: number };
}

function findBottleneck(state: AppState): Bottleneck {
  const out: Bottleneck = {};
  let maxAgent = 0;
  for (const c of state.completedAgents) {
    const ms = c.durationMs ?? diffMs(c.startedAt, c.endedAt);
    if (ms > maxAgent) {
      maxAgent = ms;
      out.agent = { name: c.name, ms, phase: c.phase };
    }
  }
  let maxPhase = 0;
  for (const p of PHASE_ORDER) {
    const ph = state.phases[p];
    const ms = diffMs(ph.startedAt, ph.endedAt);
    if (ms > maxPhase) {
      maxPhase = ms;
      out.phase = { phase: p, ms };
    }
  }
  return out;
}

export interface GenerateOptions {
  runId: string;
  eventsDir: string;
  specVersion?: string;
}

export async function generatePostmortem(
  runId: string,
  eventsDir: string,
  specVersion = "(unset)"
): Promise<string> {
  const file = path.join(eventsDir, runId, "events.jsonl");
  const events = readEvents(file);
  if (events.length === 0) {
    throw new Error(`no events found for run ${runId}`);
  }
  const state = fold(events);
  const md = render(state, runId, specVersion);
  return md;
}

export async function writePostmortem(
  runId: string,
  eventsDir: string,
  specVersion = "(unset)"
): Promise<string> {
  const md = await generatePostmortem(runId, eventsDir, specVersion);
  const outPath = path.join(eventsDir, runId, "postmortem.md");
  const tmpPath = `${outPath}.tmp`;
  fs.writeFileSync(tmpPath, md, "utf8");
  fs.renameSync(tmpPath, outPath);
  return outPath;
}

function render(state: AppState, runId: string, specVersion: string): string {
  const totalMs = diffMs(state.startedAt, state.endedAt);
  const verdict = state.riskGate?.verdict ?? "(none)";
  const finalEngine = state.engine;
  const bottleneck = findBottleneck(state);

  const phaseRows = PHASE_ORDER.filter((p) => state.phases[p].status !== "pending")
    .map((p) => {
      const ph = state.phases[p];
      const dur = fmtDuration(diffMs(ph.startedAt, ph.endedAt));
      return `| ${p} | ${ph.status} | ${dur} |`;
    })
    .join("\n");

  const agentRows = state.completedAgents
    .map((c) => {
      const dur = fmtDuration(c.durationMs ?? diffMs(c.startedAt, c.endedAt));
      return `| ${c.name} | ${c.phase ?? "—"} | — | ${c.status} | ${dur} |`;
    })
    .join("\n");

  const orbitTotalCost = state.orbit.iters.reduce(
    (sum, it) => sum + (it.costPerTask ?? 0),
    0
  );
  const finalConvergence = state.orbit.iters.at(-1)?.convergence ?? 0;
  const orbitIters = state.orbit.iters.length;
  const circuitTransitions = state.orbit.iters
    .map((it, i, arr) => (i > 0 && arr[i - 1].circuit !== it.circuit ? `${arr[i - 1].circuit}→${it.circuit}@iter${it.iter}` : null))
    .filter(Boolean)
    .join(", ") || "(stable)";

  const engineRows = state.engineHistory
    .map((h) => `| ${h.from} | ${h.to} | ${h.at} | engine_switch |`)
    .join("\n");

  const errorRows = state.errors
    .map((e) => `| ${e.severity} | — | ${e.message.replace(/\|/g, "\\|")} | ${e.ts} |`)
    .join("\n");

  const narrative =
    state.finalStatus === "completed"
      ? `Run completed in ${fmtDuration(totalMs)} with verdict ${verdict}. Engine ended on ${finalEngine}.`
      : `Run ended with status=${state.finalStatus ?? "unknown"} after ${fmtDuration(totalMs)}.`;

  const bottleneckLine = (() => {
    const a = bottleneck.agent;
    const p = bottleneck.phase;
    const parts: string[] = [];
    if (a) parts.push(`top agent: \`${a.name}\` @ ${a.phase ?? "—"} (${fmtDuration(a.ms)})`);
    if (p) parts.push(`top phase: \`${p.phase}\` (${fmtDuration(p.ms)})`);
    return parts.join(" · ") || "(no measurable hotspots)";
  })();

  const lorePatterns: string[] = [];
  if (verdict === "Conditional-Go") lorePatterns.push("Risk Gate Conditional-Go — review omen mitigations");
  if (state.errors.some((e) => e.severity === "fatal")) lorePatterns.push("Fatal error encountered — investigate root cause");
  if (orbitIters >= 5) lorePatterns.push(`High orbit iteration count (${orbitIters}) — possible convergence issue`);
  if (finalConvergence < 0.9 && state.finalStatus === "completed") lorePatterns.push(`Low final convergence (${finalConvergence.toFixed(2)}) despite completion`);
  if (lorePatterns.length === 0) lorePatterns.push("Nominal run — candidate for golden-path memory");

  return `---
run_id: ${runId}
goal: ${state.goal ?? "(none)"}
mode: ${state.mode ?? "—"}
scope: ${state.scope ?? "—"}
status: ${state.finalStatus ?? "unknown"}
started_at: ${state.startedAt ?? "—"}
ended_at: ${state.endedAt ?? "—"}
duration: ${fmtDuration(totalMs)}
final_engine: ${finalEngine}
verdict: ${verdict}
spec_version: ${specVersion}
---

# Postmortem: ${state.goal ?? runId}

## Outcome

${narrative}

## Phase Breakdown

| Phase | Status | Duration |
|-------|--------|----------|
${phaseRows || "| — | — | — |"}

## Agents Executed

| Agent | Phase | Engine | Status | Duration |
|-------|-------|--------|--------|----------|
${agentRows || "| — | — | — | — | — |"}

## Risk Gate

- Verdict: **${verdict}**
- Axes: omen=\`${state.riskGate?.axes.omen ?? "—"}\`, ripple=\`${state.riskGate?.axes.ripple ?? "—"}\`, echo=\`${state.riskGate?.axes.echo ?? "—"}\`

## Orbit (Phase 6)

- Iterations: **${orbitIters}**
- Final convergence: **${finalConvergence.toFixed(2)}**
- Total cost (sum of cost_per_task): **${orbitTotalCost.toFixed(2)}**
- Circuit transitions: ${circuitTransitions}

## Engine Boundary Crossings

| From | To | At | Reason |
|------|----|----|--------|
${engineRows || "| — | — | — | — |"}

## Bottleneck

${bottleneckLine}

## Errors / Warnings

| Severity | Source | Message | At |
|----------|--------|---------|----|
${errorRows || "| — | — | — | — |"}

## Lore Handoff Candidates

${lorePatterns.map((p) => `- ${p}`).join("\n")}
`;
}
