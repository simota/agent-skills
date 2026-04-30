// MVP subset of TOPOLOGY.md — only the agents that appear in the seed run.

import type { Phase } from "./types";

export interface PhaseGroup {
  id: string;
  phase: Phase;
  label: string;
  x: number;
  y: number;
  w: number;
  h: number;
}

export interface AgentNodeDef {
  id: string;
  agentName: string;
  label: string;
  phase: Phase;
  parent: string;
  x: number;
  y: number;
}

export interface EdgeDef {
  id: string;
  source: string;
  target: string;
  label?: string;
  type?: "flow" | "engineBoundary";
}

const PHASE_W = 280;
const PHASE_H = 540;

export const PHASE_GROUPS: PhaseGroup[] = [
  { id: "pg.P1", phase: "P1_Discovery",      label: "P1 · Discovery",     x: 0,           y: 0, w: PHASE_W, h: PHASE_H },
  { id: "pg.P2", phase: "P2_Ideate",         label: "P2 · Ideate",        x: PHASE_W,     y: 0, w: PHASE_W, h: PHASE_H },
  { id: "pg.P3", phase: "P3_Verdict",        label: "P3 · Verdict",       x: PHASE_W * 2, y: 0, w: PHASE_W, h: PHASE_H },
  { id: "pg.P4", phase: "P4_Spec",           label: "P4 · Spec",          x: PHASE_W * 3, y: 0, w: PHASE_W, h: PHASE_H },
  { id: "pg.P5", phase: "P5_Design",         label: "P5 · Design + Risk", x: PHASE_W * 4, y: 0, w: PHASE_W * 2, h: PHASE_H },
  { id: "pg.P6", phase: "P6_Implementation", label: "P6 · Implement",     x: PHASE_W * 6, y: 0, w: PHASE_W, h: PHASE_H },
  { id: "pg.Ship", phase: "Ship",            label: "Ship",               x: PHASE_W * 7, y: 0, w: PHASE_W, h: PHASE_H },
];

export const AGENTS: AgentNodeDef[] = [
  // P1
  { id: "a.plea",       agentName: "plea",       label: "plea",       phase: "P1_Discovery",      parent: "pg.P1", x: 60,  y: 100 },
  { id: "a.researcher", agentName: "researcher", label: "researcher", phase: "P1_Discovery",      parent: "pg.P1", x: 60,  y: 220 },
  // P2
  { id: "a.riff",       agentName: "riff",       label: "riff",       phase: "P2_Ideate",         parent: "pg.P2", x: 60,  y: 200 },
  // P3
  { id: "a.magi",       agentName: "magi",       label: "magi",       phase: "P3_Verdict",        parent: "pg.P3", x: 60,  y: 200 },
  // P4
  { id: "a.accord",     agentName: "accord",     label: "accord",     phase: "P4_Spec",           parent: "pg.P4", x: 60,  y: 200 },
  // P5 Tech
  { id: "a.atlas",      agentName: "atlas",      label: "atlas",      phase: "P5_Design",         parent: "pg.P5", x: 40,  y: 80  },
  { id: "a.schema",     agentName: "schema",     label: "schema",     phase: "P5_Design",         parent: "pg.P5", x: 40,  y: 200 },
  // P5 UX
  { id: "a.vision",     agentName: "vision",     label: "vision",     phase: "P5_Design",         parent: "pg.P5", x: 280, y: 80  },
  { id: "a.muse",       agentName: "muse",       label: "muse",       phase: "P5_Design",         parent: "pg.P5", x: 280, y: 180 },
  { id: "a.forge",      agentName: "forge",      label: "forge",      phase: "P5_Design",         parent: "pg.P5", x: 280, y: 280 },
  { id: "a.echo",       agentName: "echo",       label: "echo",       phase: "P5_Design",         parent: "pg.P5", x: 280, y: 380 },
  // P5 Gate
  { id: "a.omen",       agentName: "omen",       label: "omen",       phase: "P5_Design",         parent: "pg.P5", x: 160, y: 460 },
  { id: "a.ripple",     agentName: "ripple",     label: "ripple",     phase: "P5_Design",         parent: "pg.P5", x: 280, y: 460 },
  { id: "a.gate",       agentName: "gate",       label: "Risk Gate",  phase: "P5_Design",         parent: "pg.P5", x: 400, y: 460 },
  // P6
  { id: "a.orbit",      agentName: "orbit",      label: "orbit",      phase: "P6_Implementation", parent: "pg.P6", x: 60,  y: 80  },
  { id: "a.builder",    agentName: "builder",    label: "builder",    phase: "P6_Implementation", parent: "pg.P6", x: 60,  y: 200 },
  { id: "a.judge",      agentName: "judge",      label: "judge",      phase: "P6_Implementation", parent: "pg.P6", x: 60,  y: 300 },
  { id: "a.radar",      agentName: "radar",      label: "radar",      phase: "P6_Implementation", parent: "pg.P6", x: 60,  y: 400 },
  // Ship
  { id: "a.guardian",   agentName: "guardian",   label: "guardian",   phase: "Ship",              parent: "pg.Ship", x: 60, y: 180 },
  { id: "a.launch",     agentName: "launch",     label: "launch",     phase: "Ship",              parent: "pg.Ship", x: 60, y: 320 },
];

export const EDGES: EdgeDef[] = [
  { id: "e.plea_riff",       source: "a.plea",       target: "a.riff",       type: "flow" },
  { id: "e.researcher_riff", source: "a.researcher", target: "a.riff",       type: "flow" },
  { id: "e.riff_magi",       source: "a.riff",       target: "a.magi",       type: "flow" },
  { id: "e.magi_accord",     source: "a.magi",       target: "a.accord",     type: "flow", label: "verdict + AC" },
  { id: "e.accord_atlas",    source: "a.accord",     target: "a.atlas",      type: "flow" },
  { id: "e.accord_vision",   source: "a.accord",     target: "a.vision",     type: "flow" },
  { id: "e.atlas_schema",    source: "a.atlas",      target: "a.schema",     type: "flow" },
  { id: "e.vision_muse",     source: "a.vision",     target: "a.muse",       type: "flow" },
  { id: "e.muse_forge",      source: "a.muse",       target: "a.forge",      type: "flow" },
  { id: "e.forge_echo",      source: "a.forge",      target: "a.echo",       type: "flow" },
  { id: "e.atlas_gate",      source: "a.atlas",      target: "a.gate",       type: "flow" },
  { id: "e.echo_gate",       source: "a.echo",       target: "a.gate",       type: "flow" },
  { id: "e.omen_gate",       source: "a.omen",       target: "a.gate",       type: "flow" },
  { id: "e.ripple_gate",     source: "a.ripple",     target: "a.gate",       type: "flow" },
  { id: "e.gate_orbit",      source: "a.gate",       target: "a.orbit",      type: "engineBoundary", label: "claude → codex" },
  { id: "e.orbit_builder",   source: "a.orbit",      target: "a.builder",    type: "flow" },
  { id: "e.builder_judge",   source: "a.builder",    target: "a.judge",      type: "flow" },
  { id: "e.builder_radar",   source: "a.builder",    target: "a.radar",      type: "flow" },
  { id: "e.builder_guardian",source: "a.builder",    target: "a.guardian",   type: "flow", label: "loop converged" },
  { id: "e.guardian_launch", source: "a.guardian",   target: "a.launch",     type: "flow" },
];

export function findAgentByName(name: string): AgentNodeDef | undefined {
  return AGENTS.find((a) => a.agentName === name);
}
