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
import dagre from "@dagrejs/dagre";
import { useDash } from "../store";
import { AgentNode } from "../nodes/AgentNode";
import type { AgentStatus } from "../types";

const nodeTypes = { agent: AgentNode };
const NODE_W = 140;
const NODE_H = 44;

export function DynamicGraph() {
  const dynamicNodes = useDash((s) => s.state.dynamicNodes);
  const rf = useReactFlow();

  const { nodes, edges } = useMemo(() => {
    if (dynamicNodes.length === 0) return { nodes: [] as Node[], edges: [] as Edge[] };

    const g = new dagre.graphlib.Graph();
    g.setGraph({ rankdir: "TB", nodesep: 36, ranksep: 64, marginx: 12, marginy: 12 });
    g.setDefaultEdgeLabel(() => ({}));

    for (const n of dynamicNodes) {
      g.setNode(n.id, { width: NODE_W, height: NODE_H });
    }
    for (const n of dynamicNodes) {
      if (n.parentId && g.hasNode(n.parentId)) {
        g.setEdge(n.parentId, n.id);
      }
    }
    dagre.layout(g);

    const rfNodes: Node[] = dynamicNodes.map((n) => {
      const pos = g.node(n.id);
      const status: AgentStatus = n.status;
      return {
        id: n.id,
        type: "agent",
        position: { x: pos.x - NODE_W / 2, y: pos.y - NODE_H / 2 },
        data: {
          agentName: n.agent,
          label: n.agent,
          status,
        },
        draggable: false,
      };
    });

    const rfEdges: Edge[] = dynamicNodes
      .filter((n) => n.parentId)
      .map((n) => ({
        id: `e-${n.parentId}-${n.id}`,
        source: n.parentId!,
        target: n.id,
        animated: n.status === "running",
        style: {
          stroke: "rgba(148,163,184,0.5)",
          strokeWidth: 1.2,
        },
      }));

    return { nodes: rfNodes, edges: rfEdges };
  }, [dynamicNodes]);

  useEffect(() => {
    if (nodes.length > 0) {
      const id = setTimeout(() => rf.fitView({ padding: 0.2, duration: 600 }), 50);
      return () => clearTimeout(id);
    }
  }, [nodes.length, rf]);

  if (nodes.length === 0) {
    return <div className="empty-canvas">no agents yet — waiting for agent_start…</div>;
  }

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      nodeTypes={nodeTypes}
      fitView
      fitViewOptions={{ padding: 0.2 }}
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
