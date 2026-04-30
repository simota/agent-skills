import { useDash } from "../store";

const STATUS_GLYPH: Record<string, string> = {
  waiting: "⏸",
  approved: "✓",
  rejected: "✕",
  timeout_passed: "⤳",
  timeout_aborted: "⏱",
};

export function Checkpoints() {
  const checkpoints = useDash((s) => s.state.checkpoints);
  const errors = useDash((s) => s.state.errors);

  return (
    <div className="rail-card">
      <header className="rail-card-header">
        <span>Checkpoints & errors</span>
      </header>
      <div className="rail-card-body">
        {checkpoints.length === 0 && errors.length === 0 && (
          <div className="rail-empty">none yet</div>
        )}
        {checkpoints.map((c, i) => (
          <div key={`${c.label}-${i}`} className={`checkpoint status-${c.status}`}>
            <span className="ck-glyph">{STATUS_GLYPH[c.status] ?? "•"}</span>
            <span className="ck-label">{c.label}</span>
            <span className="ck-status">{c.status}</span>
          </div>
        ))}
        {errors.slice(-5).reverse().map((e, i) => (
          <div key={`err-${i}`} className={`checkpoint err-${e.severity}`}>
            <span className="ck-glyph">!</span>
            <span className="ck-label">{e.message.slice(0, 60)}</span>
            <span className="ck-status">{e.severity}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
