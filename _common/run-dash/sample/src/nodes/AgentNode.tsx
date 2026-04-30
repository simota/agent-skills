import { memo } from "react";
import { Handle, Position, type NodeProps } from "@xyflow/react";
import type { AgentStatus } from "../types";

interface AgentNodeData {
  agentName: string;
  label: string;
  status: AgentStatus;
  lastTool?: string;
  [key: string]: unknown;
}

function AgentNodeImpl({ data }: NodeProps) {
  const d = data as AgentNodeData;
  return (
    <div className={`agent-node status-${d.status}`}>
      <Handle type="target" position={Position.Left} className="handle" />
      <div className="agent-node-label">{d.label}</div>
      {d.lastTool && d.status === "running" && (
        <div className="agent-node-sub">tool: {d.lastTool}</div>
      )}
      {d.status === "done" && <div className="agent-node-tick">✓</div>}
      {d.status === "error" && <div className="agent-node-tick error">!</div>}
      <Handle type="source" position={Position.Right} className="handle" />
    </div>
  );
}

export const AgentNode = memo(AgentNodeImpl);
