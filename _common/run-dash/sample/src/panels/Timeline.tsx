import { useEffect, useMemo, useState } from "react";
import { useDash } from "../store";

const ROW_H = 22;
const LABEL_W = 100;
const STATUS_FILL: Record<string, string> = {
  running: "#3b82f6",
  done: "#10b981",
  error: "#ef4444",
  blocked: "#ef4444",
  need_info: "#f59e0b",
};

interface Bar {
  name: string;
  startedAt: string;
  endedAt?: string;
  status: string;
}

export function Timeline() {
  const completed = useDash((s) => s.state.completedAgents);
  const active = useDash((s) => s.state.activeAgents);
  const events = useDash((s) => s.state.events);
  const startedAt = useDash((s) => s.state.startedAt);
  const endedAt = useDash((s) => s.state.endedAt);

  const [, force] = useState(0);
  useEffect(() => {
    if (endedAt) return;
    const id = setInterval(() => force((n) => n + 1), 1000);
    return () => clearInterval(id);
  }, [endedAt]);

  const bars: Bar[] = useMemo(() => {
    const out: Bar[] = [];
    for (const c of completed) {
      out.push({
        name: c.name,
        startedAt: c.startedAt,
        endedAt: c.endedAt,
        status: c.status,
      });
    }
    for (const a of active) {
      out.push({ name: a.name, startedAt: a.startedAt, status: "running" });
    }
    out.sort(
      (a, b) =>
        new Date(a.startedAt).getTime() - new Date(b.startedAt).getTime()
    );
    return out;
  }, [completed, active]);

  if (bars.length === 0) {
    return (
      <div className="timeline-empty">
        no agents yet — timeline will populate as `agent_start` arrives
      </div>
    );
  }

  const t0 = startedAt
    ? new Date(startedAt).getTime()
    : new Date(bars[0].startedAt).getTime();
  const t1 = endedAt ? new Date(endedAt).getTime() : Date.now();
  const span = Math.max(t1 - t0, 1);
  const W = 800;
  const PAD_R = 8;
  const drawW = W - LABEL_W - PAD_R;
  const H = bars.length * ROW_H + 16;

  const toolMarks: { agent: string; ts: string }[] = events
    .filter((e) => e.kind === "tool_use" && e.agent)
    .map((e) => ({ agent: String(e.agent), ts: e.ts }));

  return (
    <div className="timeline-host">
      <svg
        width="100%"
        height={H}
        viewBox={`0 0 ${W} ${H}`}
        preserveAspectRatio="none"
        className="timeline-svg"
      >
        {bars.map((b, i) => {
          const startX =
            LABEL_W +
            ((new Date(b.startedAt).getTime() - t0) / span) * drawW;
          const endX =
            LABEL_W +
            (((b.endedAt ? new Date(b.endedAt).getTime() : t1) - t0) / span) *
              drawW;
          const w = Math.max(endX - startX, 2);
          const fill = STATUS_FILL[b.status] ?? "#64748b";

          const ticks = toolMarks.filter((m) => m.agent === b.name);

          return (
            <g key={`${b.name}-${i}`}>
              <text
                x={4}
                y={i * ROW_H + 14}
                fill="var(--text-muted)"
                fontSize={10}
                fontFamily="JetBrains Mono, monospace"
              >
                {b.name}
              </text>
              <rect
                x={startX}
                y={i * ROW_H + 4}
                width={w}
                height={ROW_H - 6}
                fill={fill}
                opacity={0.75}
                rx={2}
              />
              {ticks.map((tk, j) => {
                const tx =
                  LABEL_W + ((new Date(tk.ts).getTime() - t0) / span) * drawW;
                if (tx < startX || tx > endX) return null;
                return (
                  <line
                    key={j}
                    x1={tx}
                    x2={tx}
                    y1={i * ROW_H + 4}
                    y2={i * ROW_H + ROW_H - 2}
                    stroke="rgba(255,255,255,0.6)"
                    strokeWidth={0.8}
                  />
                );
              })}
            </g>
          );
        })}
      </svg>
    </div>
  );
}
