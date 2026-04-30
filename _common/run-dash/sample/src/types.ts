// Mirrors EVENTS.md (core + extension subset used by the sample).

export type RunKind =
  | "apex"
  | "feature"
  | "bug"
  | "refactor"
  | "manual"
  | "single-agent"
  | (string & {});

export type Phase =
  | "P0_Bootstrap"
  | "P1_Discovery"
  | "P2_Ideate"
  | "P3_Verdict"
  | "P4_Spec"
  | "P5_Design"
  | "P6_Implementation"
  | "Ship";

export const PHASE_ORDER: Phase[] = [
  "P0_Bootstrap",
  "P1_Discovery",
  "P2_Ideate",
  "P3_Verdict",
  "P4_Spec",
  "P5_Design",
  "P6_Implementation",
  "Ship",
];

export type EventKind =
  | "run_start"
  | "run_end"
  | "phase_enter"
  | "phase_exit"
  | "step_enter"
  | "step_exit"
  | "agent_start"
  | "agent_progress"
  | "agent_end"
  | "tool_use"
  | "checkpoint_wait"
  | "checkpoint_resolved"
  | "risk_gate"
  | "orbit_iter"
  | "engine_switch"
  | "spec_gate"
  | "rca_done"
  | "fix_proposed"
  | "error"
  | "note"
  | (string & {});

export type Engine = "claude_code" | "codex_cli";

export interface ApexEvent {
  ts: string;
  seq: number;
  run_id: string;
  kind: EventKind;
  run_kind?: RunKind;
  recipe?: string;
  phase?: Phase | string;
  agent?: string;
  engine?: Engine;
  parent_agent?: string;
  depth?: number;
  meta?: Record<string, unknown>;
}

export type AgentStatus =
  | "pending"
  | "running"
  | "done"
  | "error"
  | "skipped"
  | "waiting";

export type PhaseStatus = "pending" | "running" | "done" | "failed" | "skipped";

export interface PhaseState {
  status: PhaseStatus;
  startedAt?: string;
  endedAt?: string;
}

export interface StepState {
  status: PhaseStatus;
  startedAt?: string;
  endedAt?: string;
}

export interface ActiveAgent {
  name: string;
  phase?: Phase | string;
  parentAgent?: string;
  depth?: number;
  startedAt: string;
  lastTool?: string;
  progress?: number;
  engine?: Engine;
}

export interface CompletedAgent {
  name: string;
  phase?: Phase | string;
  parentAgent?: string;
  depth?: number;
  startedAt: string;
  endedAt: string;
  status: "done" | "blocked" | "need_info" | "error";
  durationMs?: number;
  engine?: Engine;
}

export interface RiskGate {
  verdict: "Go" | "Conditional-Go" | "No-Go";
  axes: { omen: string; ripple: string; echo: string };
  at: string;
}

export interface OrbitIter {
  iter: number;
  convergence: number;
  costPerTask: number;
  budgetUsed: number;
  budgetMax: number;
  circuit: "green" | "yellow" | "red";
  at: string;
}

export interface CheckpointEntry {
  label: string;
  status:
    | "waiting"
    | "approved"
    | "rejected"
    | "timeout_passed"
    | "timeout_aborted";
  deadline?: string;
  resolvedAt?: string;
}

export interface DynamicNode {
  id: string;            // `${agent}#${seq}`
  agent: string;
  parentId?: string;     // resolved parent DynamicNode id
  startedAt: string;
  endedAt?: string;
  status: AgentStatus;
  engine?: Engine;
  depth?: number;
}

export interface AppState {
  runId?: string;
  runKind?: RunKind;
  recipe?: string;
  goal?: string;
  mode?: string;
  scope?: string;
  startedAt?: string;
  endedAt?: string;
  finalStatus?: string;
  currentPhase?: Phase;
  currentStep?: string;
  phases: Record<Phase, PhaseState>;
  steps: Record<string, StepState>;
  activeAgents: ActiveAgent[];
  completedAgents: CompletedAgent[];
  riskGate?: RiskGate;
  orbit: { iters: OrbitIter[] };
  engine: Engine;
  engineHistory: { from: Engine; to: Engine; at: string }[];
  checkpoints: CheckpointEntry[];
  errors: { ts: string; severity: string; message: string }[];
  toolCounts: Record<string, number>;
  dynamicNodes: DynamicNode[];
  events: ApexEvent[];
}
