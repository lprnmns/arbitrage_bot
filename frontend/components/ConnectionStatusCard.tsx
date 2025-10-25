"use client";

import type { HeartbeatPayload } from "../hooks/useMockFeed";

interface ConnectionStatusCardProps {
  status: string;
  heartbeat: HeartbeatPayload | null;
}

export function ConnectionStatusCard({ status, heartbeat }: ConnectionStatusCardProps) {
  const ts = heartbeat ? new Date(heartbeat.ts).toLocaleTimeString() : "--";
  return (
    <div className="dashboard-card" style={{ marginBottom: "1.5rem" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h1 style={{ margin: 0 }}>Dashboard</h1>
          <p style={{ color: "#91a9ff", marginTop: "0.25rem" }}>Phase 1 - HL stream wiring</p>
        </div>
        <span className="status-pill">
          <span style={{ width: 8, height: 8, borderRadius: "50%", background: status === "open" ? "#4ee1ad" : "#ff6b6b" }} />
          {status}
        </span>
      </div>
      <div style={{ marginTop: "1.5rem" }}>
        <p style={{ color: "#c3d3ff" }}>
          WebSocket heartbeat exposes env + infra health; Info WS ingestion writes ticks/trades to SQLite for HYPE/SOL/BTC.
        </p>
        <code style={{ background: "rgba(0,0,0,0.35)", padding: "0.5rem 0.75rem", borderRadius: 8 }}>
          Last heartbeat: {ts} - Mode: {heartbeat?.mode ?? "--"}
        </code>
      </div>
    </div>
  );
}
