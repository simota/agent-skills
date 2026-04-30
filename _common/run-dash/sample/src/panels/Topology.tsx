import { useEffect, useMemo } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  type Node,
  type Edge,
  useReactFlow,
} from "@xyflow/react";
import { AGENTS, EDGES, PHASE_GROUPS } from "../topology";
import { useDash } from "../store";
import { AgentNode } from "../nodes/AgentNode";
import type { AgentStatus } from "../types";

const nodeTypes = { agent: AgentNode };

export function Topology() {
  const activeAgents = useDash((s) => s.state.activeAgents);
  const completedAgents = useDash((s) => s.state.completedAgents);
  const currentPhase = useDash((s) => s.state.currentPhase);
  const errors = useDash((s) => s.state.errors);
  const rf = useReactFlow();

  const statusByAgent = useMemo(() => {
    const map = new Map<string, AgentStatus>();
    for (const c of completedAgents) {
      map.set(
        c.name,
        c.status === "error" ? "error" : c.status === "blocked" ? "error" : "done"
      );
    }
    for (const a of activeAgents) map.set(a.name, "running");
    if (errors.length > 0) {
      const last = errors[errors.length - 1];
      // crude heuristic: mark unknown agents only; not propagating per-agent error
      void last;
    }
    return map;
  }, [activeAgents, completedAgents, errors]);

  const lastToolByAgent = useMemo(() => {
    const map = new Map<string, string | undefined>();
    for (const a of activeAgents) map.set(a.name, a.lastTool);
    return map;
  }, [activeAgents]);

  const nodes: Node[] = useMemo(() => {
    const groupNodes: Node[] = PHASE_GROUPS.map((g) => ({
      id: g.id,
      type: "group",
      position: { x: g.x, y: g.y },
      data: { label: g.label },
      style: {
        width: g.w,
        height: g.h,
        backgroundColor: "rgba(59,130,246,0.04)",
        border: "1px dashed rgba(148,163,184,0.25)",
        borderRadius: 12,
      },
      draggable: false,
      selectable: false,
    }));
    const labelNodes: Node[] = PHASE_GROUPS.map((g) => ({
      id: `${g.id}.label`,
      type: "default",
      parentId: g.id,
      position: { x: 12, y: 8 },
      data: { label: g.label },
      style: {
        fontSize: 11,
        background: "transparent",
        border: "none",
        color: "var(--text-muted)",
        padding: 0,
        boxShadow: "none",
      },
      draggable: false,
      selectable: false,
    }));
    const agentNodes: Node[] = AGENTS.map((a) => {
      const status: AgentStatus = statusByAgent.get(a.agentName) ?? "pending";
      return {
        id: a.id,
        type: "agent",
        parentId: a.parent,
        extent: "parent",
        position: { x: a.x, y: a.y },
        data: {
          agentName: a.agentName,
          label: a.label,
          status,
          lastTool: lastToolByAgent.get(a.agentName),
        },
        draggable: false,
      };
    });
    return [...groupNodes, ...labelNodes, ...agentNodes];
  }, [statusByAgent, lastToolByAgent]);

  const edges: Edge[] = useMemo(() => {
    return EDGES.map((e) => {
      const sourceActive = statusByAgent.get(e.source.replace(/^a\./, "")) === "running";
      const targetActive = statusByAgent.get(e.target.replace(/^a\./, "")) === "running";
      const animated = sourceActive || targetActive;
      const isBoundary = e.type === "engineBoundary";
      return {
        id: e.id,
        source: e.source,
        target: e.target,
        label: e.label,
        animated,
        style: {
          stroke: isBoundary ? "#a78bfa" : "rgba(148,163,184,0.5)",
          strokeWidth: isBoundary ? 2 : 1.2,
          strokeDasharray: isBoundary ? "6 4" : undefined,
        },
        labelStyle: { fill: "var(--text-muted)", fontSize: 10 },
        labelBgStyle: { fill: "var(--bg-elev)" },
      };
    });
  }, [statusByAgent]);

  // Camera follow on phase change
  useEffect(() => {
    if (!currentPhase) return;
    const group = PHASE_GROUPS.find((g) => g.phase === currentPhase);
    if (!group) return;
    const cx = group.x + group.w / 2;
    const cy = group.y + group.h / 2;
    rf.setCenter(cx, cy, { zoom: 0.85, duration: 800 });
  }, [currentPhase, rf]);

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      nodeTypes={nodeTypes}
      fitView
      fitViewOptions={{ padding: 0.15 }}
      proOptions={{ hideAttribution: true }}
      minZoom={0.2}
      maxZoom={2}
      nodesDraggable={false}
      nodesConnectable={false}
      elementsSelectable={false}
    >
      <Background gap={24} size={1} color="rgba(148,163,184,0.1)" />
      <Controls showInteractive={false} />
      <MiniMap
        pannable
        zoomable
        nodeColor={(n) => {
          const s = (n.data as { status?: AgentStatus } | undefined)?.status;
          if (s === "running") return "#3b82f6";
          if (s === "done") return "#10b981";
          if (s === "error") return "#ef4444";
          return "#475569";
        }}
        maskColor="rgba(11,18,32,0.7)"
      />
    </ReactFlow>
  );
}
