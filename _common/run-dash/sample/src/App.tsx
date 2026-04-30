import { useEffect, useMemo, useState } from "react";
import { ReactFlowProvider } from "@xyflow/react";
import { Header } from "./panels/Header";
import { PhaseRail } from "./panels/PhaseRail";
import { StepRail } from "./panels/StepRail";
import { Topology } from "./panels/Topology";
import { DynamicGraph } from "./panels/DynamicGraph";
import { Timeline } from "./panels/Timeline";
import { EventStream } from "./panels/EventStream";
import { RiskGateRadar } from "./panels/RiskGateRadar";
import { OrbitChart } from "./panels/OrbitChart";
import { ToolHistogram } from "./panels/ToolHistogram";
import { ActiveAgents } from "./panels/ActiveAgents";
import { Checkpoints } from "./panels/Checkpoints";
import { listRuns, startSSE, useDash } from "./store";
import type { RunKind } from "./types";

type Mode = "apex" | "recipe" | "generic";

function deriveMode(runKind?: RunKind): Mode {
  if (runKind === "apex") return "apex";
  if (runKind === "feature" || runKind === "bug" || runKind === "refactor")
    return "recipe";
  return "generic";
}

export default function App() {
  const [bootError, setBootError] = useState<string | null>(null);
  const runId = useDash((s) => s.runId);
  const runKind = useDash((s) => s.state.runKind);
  const mode = useMemo(() => deriveMode(runKind), [runKind]);

  useEffect(() => {
    let cancel: (() => void) | null = null;
    (async () => {
      const runs = await listRuns();
      if (runs.length === 0) {
        setBootError("No runs found under events/. Add a JSONL file to start.");
        return;
      }
      cancel = startSSE(runs[0]);
    })();
    return () => {
      if (cancel) cancel();
    };
  }, []);

  if (bootError) {
    return <div className="boot-error">{bootError}</div>;
  }

  return (
    <ReactFlowProvider>
      <div className={`app mode-${mode}`}>
        <Header />
        {mode === "apex" && <PhaseRail />}
        {mode === "recipe" && <StepRail />}
        {mode === "generic" && <div className="rail-placeholder" />}
        <main className="main">
          <div className="canvas-and-mid">
            <div className="canvas-wrap">
              {mode === "generic" ? <DynamicGraph /> : <Topology />}
            </div>
            <div className="mid-panel">
              {mode === "generic" ? <Timeline /> : <OrbitChart />}
            </div>
          </div>
          <aside className="right-rail">
            {mode === "apex" && <RiskGateRadar />}
            {mode !== "apex" && <ToolHistogram />}
            <ActiveAgents />
            <Checkpoints />
          </aside>
        </main>
        <EventStream />
        {!runId && <div className="boot-overlay">connecting…</div>}
      </div>
    </ReactFlowProvider>
  );
}
