import { useEffect, useState } from "react";
import { listRuns, switchRun, useDash } from "../store";

function formatElapsed(ms: number): string {
  const total = Math.floor(ms / 1000);
  const h = Math.floor(total / 3600);
  const m = Math.floor((total % 3600) / 60);
  const s = total % 60;
  if (h > 0) return `${h}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

const RUN_KIND_COLOR: Record<string, string> = {
  apex: "#3b82f6",
  feature: "#10b981",
  bug: "#ef4444",
  refactor: "#f59e0b",
  manual: "#94a3b8",
  "single-agent": "#a78bfa",
};

export function Header() {
  const runId = useDash((s) => s.runId);
  const runKind = useDash((s) => s.state.runKind);
  const recipe = useDash((s) => s.state.recipe);
  const project = useDash((s) => s.state.project);
  const connected = useDash((s) => s.connected);
  const goal = useDash((s) => s.state.goal);
  const mode = useDash((s) => s.state.mode);
  const startedAt = useDash((s) => s.state.startedAt);
  const endedAt = useDash((s) => s.state.endedAt);
  const engine = useDash((s) => s.state.engine);
  const availableRuns = useDash((s) => s.availableRuns);
  const eventsDir = useDash((s) => s.eventsDir);

  const [, force] = useState(0);
  useEffect(() => {
    if (endedAt) return;
    const id = setInterval(() => force((n) => n + 1), 1000);
    return () => clearInterval(id);
  }, [endedAt]);

  // Refresh run list every 5 s so newly-emitted runs appear in the picker
  useEffect(() => {
    const tick = async () => {
      const { runs, eventsDir } = await listRuns();
      useDash.getState().setAvailableRuns(runs);
      useDash.getState().setEventsDir(eventsDir);
    };
    tick();
    const id = setInterval(tick, 5000);
    return () => clearInterval(id);
  }, []);

  const elapsedMs = startedAt
    ? (endedAt ? new Date(endedAt).getTime() : Date.now()) -
      new Date(startedAt).getTime()
    : 0;

  const kindColor = runKind ? RUN_KIND_COLOR[runKind] ?? "#64748b" : "#64748b";

  return (
    <header className="header">
      <div className="header-left">
        <select
          className="run-picker"
          value={runId ?? ""}
          onChange={(e) => switchRun(e.target.value)}
          title={eventsDir ? `events_dir: ${eventsDir}` : "Switch run"}
        >
          {availableRuns.length === 0 && <option value="">— no runs —</option>}
          {availableRuns.map((r) => (
            <option key={r.id} value={r.id}>
              {r.project ? `[${r.project}] ` : ""}
              {r.id}
              {r.runKind ? ` · ${r.runKind}` : ""}
            </option>
          ))}
        </select>
        <span
          className="dot"
          data-on={connected ? "1" : "0"}
          title={connected ? "live" : "disconnected"}
        />
        {runKind && (
          <span
            className="badge run-kind"
            style={{ borderColor: kindColor, color: kindColor }}
            title={recipe ? `recipe: ${recipe}` : `run_kind: ${runKind}`}
          >
            {runKind}
          </span>
        )}
        {project && (
          <span className="badge project" title={`project: ${project}`}>
            {project}
          </span>
        )}
        <span className="goal">{goal ?? "(no goal)"}</span>
        {mode && <span className="badge mode">{mode}</span>}
        <span className={`badge engine engine-${engine}`}>{engine}</span>
      </div>
      <div className="header-right">
        <span className="elapsed">⏱ {formatElapsed(elapsedMs)}</span>
        {endedAt && <span className="badge done">DONE</span>}
        {endedAt && runId && (
          <a
            className="btn-postmortem"
            href={`/api/postmortem/${encodeURIComponent(runId)}`}
            target="_blank"
            rel="noreferrer"
            title="Generate / view postmortem markdown"
          >
            📄 postmortem
          </a>
        )}
      </div>
    </header>
  );
}
