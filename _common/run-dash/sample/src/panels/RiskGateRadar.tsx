import {
  PolarAngleAxis,
  PolarGrid,
  Radar,
  RadarChart,
  ResponsiveContainer,
} from "recharts";
import { useDash } from "../store";

const AXIS_TO_VALUE = (s: string): number => {
  if (s === "pass") return 1;
  if (s === "conditional") return 0.55;
  if (s === "fail") return 0;
  return 0.15; // pending
};

const VERDICT_COLOR: Record<string, string> = {
  Go: "#10b981",
  "Conditional-Go": "#f59e0b",
  "No-Go": "#ef4444",
};

export function RiskGateRadar() {
  const gate = useDash((s) => s.state.riskGate);

  const verdict = gate?.verdict ?? "—";
  const colour = gate ? VERDICT_COLOR[verdict] ?? "#64748b" : "#64748b";

  const data = [
    { axis: "omen", value: AXIS_TO_VALUE(gate?.axes.omen ?? "pending") },
    { axis: "ripple", value: AXIS_TO_VALUE(gate?.axes.ripple ?? "pending") },
    { axis: "echo", value: AXIS_TO_VALUE(gate?.axes.echo ?? "pending") },
  ];

  return (
    <div className="rail-card">
      <header className="rail-card-header">
        <span>Risk Gate</span>
        <span className="badge" style={{ borderColor: colour, color: colour }}>
          {verdict}
        </span>
      </header>
      <div className="radar-host">
        <ResponsiveContainer width="100%" height={160}>
          <RadarChart data={data} outerRadius={55} cx="50%" cy="50%">
            <PolarGrid stroke="rgba(148,163,184,0.25)" />
            <PolarAngleAxis
              dataKey="axis"
              stroke="var(--text-muted)"
              tick={{ fontSize: 10 }}
            />
            <Radar
              dataKey="value"
              stroke={colour}
              fill={colour}
              fillOpacity={0.25}
              isAnimationActive
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>
      <div className="rail-card-axes">
        {(["omen", "ripple", "echo"] as const).map((a) => (
          <div key={a} className={`axis axis-${gate?.axes[a] ?? "pending"}`}>
            <span className="axis-name">{a}</span>
            <span className="axis-value">{gate?.axes[a] ?? "pending"}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
