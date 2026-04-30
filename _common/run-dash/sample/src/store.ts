import { create } from "zustand";
import type { ApexEvent, AppState, RunSummary } from "./types";
import { initialState, reduce } from "./reducer";

interface DashStore {
  runId: string | null;
  connected: boolean;
  availableRuns: RunSummary[];
  eventsDir: string | null;
  state: AppState;
  setRunId: (runId: string) => void;
  ingest: (ev: ApexEvent) => void;
  reset: () => void;
  setConnected: (v: boolean) => void;
  setAvailableRuns: (runs: RunSummary[]) => void;
  setEventsDir: (dir: string | null) => void;
}

export const useDash = create<DashStore>((set) => ({
  runId: null,
  connected: false,
  availableRuns: [],
  eventsDir: null,
  state: initialState,
  setRunId: (runId) => set({ runId }),
  ingest: (ev) => set((s) => ({ state: reduce(s.state, ev) })),
  reset: () => set({ state: initialState }),
  setConnected: (v) => set({ connected: v }),
  setAvailableRuns: (runs) => set({ availableRuns: runs }),
  setEventsDir: (dir) => set({ eventsDir: dir }),
}));

let currentClose: (() => void) | null = null;

export function startSSE(runId: string): () => void {
  if (currentClose) {
    currentClose();
    currentClose = null;
  }

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

  const close = () => {
    es.close();
    useDash.getState().setConnected(false);
  };
  currentClose = close;
  return close;
}

export function switchRun(runId: string): void {
  startSSE(runId);
}

export async function listRuns(): Promise<{
  runs: RunSummary[];
  eventsDir: string | null;
}> {
  try {
    const r = await fetch("/api/runs");
    const j = (await r.json()) as { runs: RunSummary[]; events_dir?: string };
    return { runs: j.runs ?? [], eventsDir: j.events_dir ?? null };
  } catch {
    return { runs: [], eventsDir: null };
  }
}
