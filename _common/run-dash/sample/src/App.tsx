import { useEffect, useState } from "react";
import { ReactFlowProvider } from "@xyflow/react";
import { Header } from "./panels/Header";
import { PhaseRail } from "./panels/PhaseRail";
import { Topology } from "./panels/Topology";
import { EventStream } from "./panels/EventStream";
import { RiskGateRadar } from "./panels/RiskGateRadar";
import { OrbitChart } from "./panels/OrbitChart";
import { ActiveAgents } from "./panels/ActiveAgents";
import { Checkpoints } from "./panels/Checkpoints";
import { listRuns, startSSE, useDash } from "./store";

export default function App() {
  const [bootError, setBootError] = useState<string | null>(null);
  const runId = useDash((s) => s.runId);

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
      <div className="app">
        <Header />
        <PhaseRail />
        <main className="main">
          <div className="canvas-and-mid">
            <div className="canvas-wrap">
              <Topology />
            </div>
            <div className="mid-panel">
              <OrbitChart />
            </div>
          </div>
          <aside className="right-rail">
            <RiskGateRadar />
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
