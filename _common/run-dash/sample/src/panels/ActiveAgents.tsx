import { useEffect, useState } from "react";
import { useDash } from "../store";

function formatElapsed(startedAt: string): string {
  const ms = Date.now() - new Date(startedAt).getTime();
  const total = Math.max(0, Math.floor(ms / 1000));
  const m = Math.floor(total / 60);
  const s = total % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

export function ActiveAgents() {
  const active = useDash((s) => s.state.activeAgents);
  const [, force] = useState(0);

  useEffect(() => {
    if (active.length === 0) return;
    const id = setInterval(() => force((n) => n + 1), 1000);
    return () => clearInterval(id);
  }, [active.length]);

  return (
    <div className="rail-card">
      <header className="rail-card-header">
        <span>Active agents</span>
        <span className="muted">{active.length}</span>
      </header>
      <div className="rail-card-body">
        {active.length === 0 && <div className="rail-empty">none active</div>}
        {active.map((a) => (
          <div key={a.name} className="agent-card">
            <div className="agent-card-row1">
              <span className="agent-card-dot" />
              <span className="agent-card-name">{a.name}</span>
              <span className="agent-card-elapsed">
                {formatElapsed(a.startedAt)}
              </span>
            </div>
            <div className="agent-card-row2">
              {a.phase && <span className="agent-card-phase">{a.phase}</span>}
              {a.lastTool && (
                <span className="agent-card-tool">tool: {a.lastTool}</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
