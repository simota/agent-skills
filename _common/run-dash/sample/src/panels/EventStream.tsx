import { useEffect, useRef } from "react";
import { useDash } from "../store";
import type { ApexEvent } from "../types";

const KIND_COLOR: Record<string, string> = {
  run_start: "#a78bfa",
  run_end: "#a78bfa",
  phase_enter: "#3b82f6",
  phase_exit: "#3b82f6",
  agent_start: "#06b6d4",
  agent_end: "#10b981",
  agent_progress: "#0ea5e9",
  tool_use: "#94a3b8",
  checkpoint_wait: "#f59e0b",
  checkpoint_resolved: "#f59e0b",
  risk_gate: "#ef4444",
  orbit_iter: "#22c55e",
  engine_switch: "#a78bfa",
  error: "#ef4444",
  note: "#64748b",
};

function digest(ev: ApexEvent): string {
  const m = ev.meta ?? {};
  switch (ev.kind) {
    case "run_start":
      return `goal="${m.goal}" mode=${m.mode} scope=${m.scope}`;
    case "run_end":
      return `status=${m.status} duration_ms=${m.duration_ms}`;
    case "phase_enter":
      return `${ev.phase}`;
    case "phase_exit":
      return `${ev.phase} gate=${m.exit_gate}`;
    case "agent_start":
      return `${ev.agent} @ ${ev.phase} (${ev.engine})`;
    case "agent_end":
      return `${ev.agent} status=${m.status} ${m.duration_ms}ms`;
    case "tool_use":
      return `${ev.agent} tool=${m.tool}`;
    case "risk_gate":
      return `verdict=${m.verdict} omen=${m.omen} ripple=${m.ripple} echo=${m.echo}`;
    case "orbit_iter":
      return `iter=${m.iter} conv=${m.convergence} cost=${m.cost_per_task} circuit=${m.circuit}`;
    case "engine_switch":
      return `${m.from} → ${m.to}`;
    case "checkpoint_wait":
      return `${m.label} mode=${m.mode}`;
    case "checkpoint_resolved":
      return `${m.label} → ${m.outcome}`;
    case "error":
      return `[${m.severity}] ${m.message}`;
    default:
      return JSON.stringify(m);
  }
}

function timeOf(ts: string): string {
  const d = new Date(ts);
  return [d.getHours(), d.getMinutes(), d.getSeconds()]
    .map((n) => String(n).padStart(2, "0"))
    .join(":");
}

export function EventStream() {
  const events = useDash((s) => s.state.events);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.scrollTop = el.scrollHeight;
  }, [events]);

  return (
    <section className="event-stream">
      <header className="event-stream-header">
        <span>events</span>
        <span className="muted">{events.length} buffered</span>
      </header>
      <div className="event-stream-body" ref={ref}>
        {events.map((ev) => (
          <div key={`${ev.run_id}-${ev.seq}`} className="ev-row">
            <span className="ev-time">{timeOf(ev.ts)}</span>
            <span
              className="ev-kind"
              style={{ borderLeftColor: KIND_COLOR[ev.kind] ?? "#64748b" }}
            >
              {ev.kind}
            </span>
            <span className="ev-digest">{digest(ev)}</span>
          </div>
        ))}
        {events.length === 0 && (
          <div className="ev-empty">no events yet — waiting for run_start…</div>
        )}
      </div>
    </section>
  );
}
