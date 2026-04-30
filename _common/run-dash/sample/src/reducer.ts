import type {
  ApexEvent,
  AppState,
  DynamicNode,
  Phase,
  PhaseState,
} from "./types";
import { PHASE_ORDER } from "./types";

const EMPTY_PHASES = (): Record<Phase, PhaseState> => {
  const out: Partial<Record<Phase, PhaseState>> = {};
  for (const p of PHASE_ORDER) out[p] = { status: "pending" };
  return out as Record<Phase, PhaseState>;
};

export const initialState: AppState = {
  phases: EMPTY_PHASES(),
  steps: {},
  activeAgents: [],
  completedAgents: [],
  orbit: { iters: [] },
  engine: "claude_code",
  engineHistory: [],
  checkpoints: [],
  errors: [],
  toolCounts: {},
  dynamicNodes: [],
  events: [],
};

const EVENT_BUFFER = 200;

export function reduce(state: AppState, ev: ApexEvent): AppState {
  const next: AppState = {
    ...state,
    phases: { ...state.phases },
    steps: { ...state.steps },
    activeAgents: state.activeAgents.slice(),
    completedAgents: state.completedAgents.slice(),
    orbit: { iters: state.orbit.iters.slice() },
    engineHistory: state.engineHistory.slice(),
    checkpoints: state.checkpoints.slice(),
    errors: state.errors.slice(),
    toolCounts: { ...state.toolCounts },
    dynamicNodes: state.dynamicNodes.slice(),
    events: [...state.events, ev].slice(-EVENT_BUFFER),
  };

  const meta = ev.meta ?? {};

  switch (ev.kind) {
    case "run_start": {
      next.runId = ev.run_id;
      next.runKind = ev.run_kind ?? inferRunKind(ev.run_id);
      next.recipe = ev.recipe ?? (meta.recipe as string | undefined);
      next.project = (meta.project as string | undefined) ?? undefined;
      next.goal = String(meta.goal ?? "");
      next.mode = String(meta.mode ?? "");
      next.scope = String(meta.scope ?? "");
      next.startedAt = ev.ts;
      break;
    }
    case "run_end": {
      next.endedAt = ev.ts;
      next.finalStatus = String(meta.status ?? "completed");
      break;
    }
    case "phase_enter": {
      if (ev.phase && (PHASE_ORDER as string[]).includes(ev.phase)) {
        next.currentPhase = ev.phase as Phase;
        next.phases[ev.phase as Phase] = {
          ...next.phases[ev.phase as Phase],
          status: "running",
          startedAt: ev.ts,
        };
      }
      break;
    }
    case "phase_exit": {
      if (ev.phase && (PHASE_ORDER as string[]).includes(ev.phase)) {
        const gate = String(meta.exit_gate ?? "pass");
        const status =
          gate === "pass" ? "done" : gate === "fail" ? "failed" : "skipped";
        next.phases[ev.phase as Phase] = {
          ...next.phases[ev.phase as Phase],
          status,
          endedAt: ev.ts,
        };
      }
      break;
    }
    case "step_enter": {
      const step = String(meta.step ?? ev.phase ?? "");
      if (step) {
        next.currentStep = step;
        next.steps[step] = {
          status: "running",
          startedAt: ev.ts,
        };
      }
      break;
    }
    case "step_exit": {
      const step = String(meta.step ?? ev.phase ?? "");
      if (step) {
        const gate = String(meta.exit_gate ?? "pass");
        const status =
          gate === "pass" ? "done" : gate === "fail" ? "failed" : "skipped";
        next.steps[step] = {
          ...next.steps[step],
          status,
          endedAt: ev.ts,
        };
      }
      break;
    }
    case "agent_start": {
      if (ev.agent) {
        next.activeAgents = next.activeAgents.filter((a) => a.name !== ev.agent);
        next.activeAgents.push({
          name: ev.agent,
          phase: ev.phase,
          parentAgent: ev.parent_agent,
          depth: ev.depth,
          startedAt: ev.ts,
          engine: ev.engine,
        });
        // Append a dynamic-DAG node (always — generic mode reads this)
        const id = `${ev.agent}#${ev.seq}`;
        const parentId = resolveParentNodeId(next.dynamicNodes, ev);
        const node: DynamicNode = {
          id,
          agent: ev.agent,
          parentId,
          startedAt: ev.ts,
          status: "running",
          engine: ev.engine,
          depth: ev.depth,
        };
        next.dynamicNodes.push(node);
      }
      break;
    }
    case "agent_progress": {
      if (ev.agent) {
        next.activeAgents = next.activeAgents.map((a) =>
          a.name === ev.agent
            ? { ...a, progress: Number(meta.progress ?? a.progress ?? 0) }
            : a
        );
      }
      break;
    }
    case "agent_end": {
      if (ev.agent) {
        const idx = next.activeAgents.findIndex((a) => a.name === ev.agent);
        if (idx >= 0) {
          const active = next.activeAgents[idx];
          next.activeAgents.splice(idx, 1);
          next.completedAgents.push({
            name: active.name,
            phase: active.phase,
            parentAgent: active.parentAgent,
            depth: active.depth,
            startedAt: active.startedAt,
            endedAt: ev.ts,
            status: (meta.status as never) ?? "done",
            durationMs: Number(meta.duration_ms ?? 0),
            engine: active.engine,
          });
        } else {
          next.completedAgents.push({
            name: ev.agent,
            phase: ev.phase,
            parentAgent: ev.parent_agent,
            depth: ev.depth,
            startedAt: ev.ts,
            endedAt: ev.ts,
            status: (meta.status as never) ?? "done",
            durationMs: Number(meta.duration_ms ?? 0),
            engine: ev.engine,
          });
        }
        // Update dynamic node by name (latest matching running)
        const lastIdx = next.dynamicNodes
          .map((n, i) => ({ n, i }))
          .filter(({ n }) => n.agent === ev.agent && n.status === "running")
          .map(({ i }) => i)
          .pop();
        if (lastIdx !== undefined) {
          const status = (meta.status as never) === "error" ? "error" : "done";
          next.dynamicNodes[lastIdx] = {
            ...next.dynamicNodes[lastIdx],
            endedAt: ev.ts,
            status,
          };
        }
      }
      break;
    }
    case "tool_use": {
      if (ev.agent) {
        next.activeAgents = next.activeAgents.map((a) =>
          a.name === ev.agent
            ? { ...a, lastTool: String(meta.tool ?? a.lastTool ?? "") }
            : a
        );
      }
      const tool = String(meta.tool ?? "");
      if (tool) next.toolCounts[tool] = (next.toolCounts[tool] ?? 0) + 1;
      break;
    }
    case "checkpoint_wait": {
      next.checkpoints.push({
        label: String(meta.label ?? "checkpoint"),
        status: "waiting",
        deadline: meta.deadline ? String(meta.deadline) : undefined,
      });
      break;
    }
    case "checkpoint_resolved": {
      const label = String(meta.label ?? "");
      next.checkpoints = next.checkpoints.map((c) =>
        c.label === label
          ? {
              ...c,
              status: (meta.outcome as never) ?? "approved",
              resolvedAt: ev.ts,
            }
          : c
      );
      break;
    }
    case "risk_gate": {
      next.riskGate = {
        verdict: (meta.verdict as never) ?? "Go",
        axes: {
          omen: String(meta.omen ?? "pending"),
          ripple: String(meta.ripple ?? "pending"),
          echo: String(meta.echo ?? "pending"),
        },
        at: ev.ts,
      };
      break;
    }
    case "orbit_iter": {
      next.orbit.iters.push({
        iter: Number(meta.iter ?? 0),
        convergence: Number(meta.convergence ?? 0),
        costPerTask: Number(meta.cost_per_task ?? 0),
        budgetUsed: Number(meta.budget_used ?? 0),
        budgetMax: Number(meta.budget_max ?? 0),
        circuit: (meta.circuit as never) ?? "green",
        at: ev.ts,
      });
      break;
    }
    case "engine_switch": {
      const from = (meta.from as never) ?? next.engine;
      const to = (meta.to as never) ?? "codex_cli";
      next.engineHistory.push({ from, to, at: ev.ts });
      next.engine = to;
      break;
    }
    case "error": {
      next.errors.push({
        ts: ev.ts,
        severity: String(meta.severity ?? "error"),
        message: String(meta.message ?? ""),
      });
      if (next.errors.length > 50) next.errors = next.errors.slice(-50);
      break;
    }
    case "note":
    default:
      break;
  }

  return next;
}

function inferRunKind(runId: string): string {
  const m = runId.match(/^([a-z-]+)-/);
  return m ? m[1] : "manual";
}

function resolveParentNodeId(
  nodes: DynamicNode[],
  ev: ApexEvent
): string | undefined {
  if (!ev.parent_agent) return undefined;
  // Find the most recent running node with matching agent name
  for (let i = nodes.length - 1; i >= 0; i--) {
    if (nodes[i].agent === ev.parent_agent && nodes[i].status === "running") {
      return nodes[i].id;
    }
  }
  return undefined;
}
