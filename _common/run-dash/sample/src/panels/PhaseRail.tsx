import { useDash } from "../store";
import { PHASE_ORDER, type Phase } from "../types";

const SHORT_LABEL: Record<Phase, string> = {
  P0_Bootstrap: "P0",
  P1_Discovery: "P1",
  P2_Ideate: "P2",
  P3_Verdict: "P3",
  P4_Spec: "P4",
  P5_Design: "P5",
  P6_Implementation: "P6",
  Ship: "Ship",
};

const FULL_LABEL: Record<Phase, string> = {
  P0_Bootstrap: "Bootstrap",
  P1_Discovery: "Discovery",
  P2_Ideate: "Ideate",
  P3_Verdict: "Verdict",
  P4_Spec: "Spec",
  P5_Design: "Design",
  P6_Implementation: "Implement",
  Ship: "Ship",
};

export function PhaseRail() {
  const phases = useDash((s) => s.state.phases);
  const current = useDash((s) => s.state.currentPhase);

  return (
    <div className="phase-rail">
      {PHASE_ORDER.map((p) => {
        const st = phases[p].status;
        const isCurrent = current === p;
        return (
          <div
            key={p}
            className={`phase-cell status-${st} ${isCurrent ? "current" : ""}`}
            title={`${p} · ${st}`}
          >
            <span className="phase-short">{SHORT_LABEL[p]}</span>
            <span className="phase-full">{FULL_LABEL[p]}</span>
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
