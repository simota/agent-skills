import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useDash } from "../store";

export function ToolHistogram() {
  const counts = useDash((s) => s.state.toolCounts);
  const data = Object.entries(counts)
    .map(([tool, count]) => ({ tool, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 6);

  return (
    <div className="rail-card">
      <header className="rail-card-header">
        <span>Tool use</span>
        <span className="muted">top 6</span>
      </header>
      <div style={{ height: 160 }}>
        {data.length === 0 ? (
          <div className="rail-empty">no tool calls yet</div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={data}
              margin={{ top: 4, right: 8, left: 0, bottom: 4 }}
            >
              <CartesianGrid
                stroke="rgba(148,163,184,0.15)"
                strokeDasharray="3 3"
              />
              <XAxis
                dataKey="tool"
                stroke="var(--text-muted)"
                tick={{ fontSize: 10 }}
              />
              <YAxis
                stroke="var(--text-muted)"
                tick={{ fontSize: 10 }}
                width={28}
                allowDecimals={false}
              />
              <Tooltip
                contentStyle={{
                  background: "var(--bg-elev)",
                  border: "1px solid var(--border)",
                  borderRadius: 6,
                  fontSize: 12,
                }}
              />
              <Bar dataKey="count" fill="#a78bfa" radius={[3, 3, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}
