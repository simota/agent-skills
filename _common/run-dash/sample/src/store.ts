import { create } from "zustand";
import type { ApexEvent, AppState } from "./types";
import { initialState, reduce } from "./reducer";

interface DashStore {
  runId: string | null;
  connected: boolean;
  state: AppState;
  setRunId: (runId: string) => void;
  ingest: (ev: ApexEvent) => void;
  reset: () => void;
  setConnected: (v: boolean) => void;
}

export const useDash = create<DashStore>((set) => ({
  runId: null,
  connected: false,
  state: initialState,
  setRunId: (runId) => set({ runId }),
  ingest: (ev) => set((s) => ({ state: reduce(s.state, ev) })),
  reset: () => set({ state: initialState }),
  setConnected: (v) => set({ connected: v }),
}));

export function startSSE(runId: string): () => void {
  const url = `/api/events/${encodeURIComponent(runId)}`;
  const es = new EventSource(url);
  useDash.getState().setRunId(runId);
  useDash.getState().reset();

  es.onopen = () => useDash.getState().setConnected(true);
  es.onerror = () => useDash.getState().setConnected(false);

  es.onmessage = (msg) => {
    if (!msg.data || msg.data === "keepalive") return;
    try {
      const ev = JSON.parse(msg.data) as ApexEvent;
      useDash.getState().ingest(ev);
    } catch (e) {
      console.warn("invalid event", msg.data, e);
    }
  };

  return () => {
    es.close();
    useDash.getState().setConnected(false);
  };
}

export async function listRuns(): Promise<string[]> {
  try {
    const r = await fetch("/api/runs");
    const j = (await r.json()) as { runs: string[] };
    return j.runs ?? [];
  } catch {
    return [];
  }
}
