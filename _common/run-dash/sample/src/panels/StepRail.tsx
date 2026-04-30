import { useDash } from "../store";

export function StepRail() {
  const steps = useDash((s) => s.state.steps);
  const current = useDash((s) => s.state.currentStep);
  const stepIds = Object.keys(steps);

  if (stepIds.length === 0) {
    return <div className="step-rail step-rail-empty">awaiting first step…</div>;
  }

  return (
    <div className="step-rail" style={{ gridTemplateColumns: `repeat(${stepIds.length}, 1fr)` }}>
      {stepIds.map((id) => {
        const st = steps[id].status;
        const isCurrent = current === id;
        return (
          <div
            key={id}
            className={`phase-cell status-${st} ${isCurrent ? "current" : ""}`}
            title={`${id} · ${st}`}
          >
            <span className="phase-short">{id.slice(0, 2).toUpperCase()}</span>
            <span className="phase-full">{id}</span>
            <span className="phase-icon">
              {st === "done" && "✓"}
              {st === "running" && "●"}
              {st === "failed" && "✕"}
              {st === "skipped" && "—"}
              {st === "pending" && "○"}
            </span>
          </div>
        );
      })}
    </div>
  );
}
