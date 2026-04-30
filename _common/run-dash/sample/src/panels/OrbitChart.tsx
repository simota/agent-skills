import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useDash } from "../store";

export function OrbitChart() {
  const iters = useDash((s) => s.state.orbit.iters);

  const data = iters.map((it) => ({
    iter: it.iter,
    convergence: Math.round(it.convergence * 100) / 100,
    cost: Math.round(it.costPerTask * 100) / 100,
    budget: it.budgetUsed,
    circuit: it.circuit,
  }));

  const last = iters.at(-1);
  const circuit = last?.circuit ?? "green";
  const circuitColor =
    circuit === "red" ? "#ef4444" : circuit === "yellow" ? "#f59e0b" : "#10b981";

  return (
    <div className={`mid-card mid-circuit-${circuit}`}>
      <header className="mid-card-header">
        <span>Orbit loop</span>
        <span className="muted">
          {last
            ? `iter=${last.iter} · conv=${last.convergence.toFixed(2)} · budget=${last.budgetUsed}/${last.budgetMax}`
            : "no iterations yet"}
        </span>
        <span className="circuit-dot" style={{ background: circuitColor }} title={`circuit=${circuit}`} />
      </header>
      <div className="chart-host">
        {data.length === 0 ? (
          <div className="chart-empty">awaiting Phase 6…</div>
        ) : (
          <ResponsiveContainer width="100%" height={160}>
            <LineChart data={data} margin={{ top: 8, right: 16, bottom: 4, left: 0 }}>
              <CartesianGrid stroke="rgba(148,163,184,0.15)" strokeDasharray="3 3" />
              <XAxis
                dataKey="iter"
                stroke="var(--text-muted)"
                tick={{ fontSize: 10 }}
              />
              <YAxis
                yAxisId="left"
                domain={[0, 1]}
                stroke="var(--text-muted)"
                tick={{ fontSize: 10 }}
                width={28}
              />
              <YAxis
                yAxisId="right"
                orientation="right"
                stroke="var(--text-muted)"
                tick={{ fontSize: 10 }}
                width={28}
              />
              <Tooltip
                contentStyle={{
                  background: "var(--bg-elev)",
                  border: "1px solid var(--border)",
                  borderRadius: 6,
                  fontSize: 12,
                }}
              />
              <Line
                yAxisId="left"
                type="monotone"
                dataKey="convergence"
                stroke="#10b981"
                strokeWidth={2}
                dot={{ r: 3 }}
                isAnimationActive
              />
              <Line
                yAxisId="right"
                type="monotone"
                dataKey="cost"
                stroke="#a78bfa"
                strokeWidth={2}
                dot={{ r: 3 }}
                isAnimationActive
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}
